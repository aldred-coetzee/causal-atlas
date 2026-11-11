"""The held data in one shape: three tables (series, place, obs) built from the files already held, one adapter a source. Each adapter returns a Part: its series rows, its observations and the names of its places. Nothing here sets one series beside another."""
import html
import json
import re
import tomllib
from collections import namedtuple
from pathlib import Path

import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import shapefile
from shapely import contains_xy
from shapely.geometry import shape

from causal_atlas.panel import RAW, ROOT
from causal_atlas.yields import BY_NAME, TOTALS

OUT = ROOT / "data" / "table"
PARTS = OUT / "parts"
SERIES_FIELDS = ("series_id", "source", "domain", "measures", "unit", "kind", "transform", "place_level", "period", "licence")
OBS_SCHEMA = pa.schema([("series_id", pa.string()), ("place_id", pa.string()), ("period", pa.string()), ("value", pa.float64()), ("flag", pa.string())])
Part = namedtuple("Part", "series obs names notes")

FAO_YIELD, FAO_AREA, FAO_PRODUCTION = "5412", "5312", "5510"
FAO_ELEMENTS = {FAO_YIELD: ("yield", "kg/ha", "log", "harvested production per hectare harvested"), FAO_AREA: ("area_harvested", "ha", "log1p", "area harvested"), FAO_PRODUCTION: ("production", "t", "log1p", "production")}
FAO_FLAGS = {"A": "official", "E": "estimated", "I": "imputed"}  # M never carries a value; X and anything else is "other"
STAPLES = ("maize", "millet", "rice", "sorghum", "wheat", "wheat_flour")  # the plain price columns of prices.py: prices as collected
WDI_LICENCE, WDI_COUNTRIES, WDI_YEARS = "CC BY-4.0", 100, 30  # the series file's own spelling; an indicator is kept with this many countries each holding this many yearly values
WDI_DOMAINS = {"economic policy & debt": "economy", "health": "health", "social protection & labor": "social", "education": "education", "private sector & trade": "trade", "environment": "environment",
               "public sector": "public sector", "financial sector": "finance", "infrastructure": "infrastructure", "poverty": "poverty", "trade": "trade", "gender": "social", "policy & institutions": "public sector"}
WDI_RATE = re.compile(r"%|percent|\bper [\d,]+|\bratio\b|\brate\b|\bgrowth\b|\bshare\b|\bproportion\b")  # per capita, per hectare and the like are quantities, not rates
WDI_INDEX = re.compile(r"\bindex\b|\bscore\b|\bscale\b|\brating\b|\bdistance to frontier\b")
CLIMATE_UNITS = {"qbo.50mb.data": "m/s", "qbo.data": "m/s", "sunspot.long.data": "count", "tornado.us.mon.data": "count"}


def manifest():
    """data/manifest.toml as a dict."""
    return tomllib.loads((ROOT / "data" / "manifest.toml").read_text())


def licence(m, key):
    """The licence line the manifest holds for a source."""
    return m[key]["licence"]


def series_row(series_id, source, domain, measures, unit, kind, transform, place_level, period, lic):
    """One row of the series table."""
    return dict(zip(SERIES_FIELDS, (series_id, source, domain, measures, unit, kind, transform, place_level, period, lic)))


def obs_table(series_id, place, period, value, flag=None):
    """Observations as an Arrow table; flag is None, one value, or a list as long as the rest."""
    n = len(value)
    flag = [flag] * n if not isinstance(flag, (list, tuple, np.ndarray)) else list(flag)
    return pa.table({"series_id": pa.array([series_id] * n if isinstance(series_id, str) else series_id, pa.string()), "place_id": pa.array(place, pa.string()),
                     "period": pa.array(period, pa.string()), "value": pa.array(np.asarray(value, dtype=float), pa.float64()), "flag": pa.array(flag, pa.string())}, schema=OBS_SCHEMA)


def natural_earth(path=None):
    """Natural Earth's countries by UN M49 code (three-digit text): name, ISO codes, shape. The same codes yields.borders uses, so a point lands in the same country as there."""
    reader = shapefile.Reader(str(path or RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    fields = [f[0] for f in reader.fields[1:]]
    out = {}
    for r in reader.iterShapeRecords():
        rec = dict(zip(fields, r.record))
        code = BY_NAME.get(rec["ADM0_A3"], str(rec["UN_A3"]).zfill(3))
        if code not in ("-99", "-099"):
            out[code] = {"name": rec["NAME"], "iso": {rec["ADM0_A3"], rec["ISO_A3_EH"], rec["ISO_A3"]} - {"-99"}, "shape": shape(r.shape.__geo_interface__)}
    return out


def middle(geom):
    """A country's latitude and longitude: the centre of its largest part, so overseas pieces do not pull it."""
    part = max(geom.geoms, key=lambda g: g.area) if hasattr(geom, "geoms") else geom
    c = part.centroid
    return float(c.y), float(c.x)


def place_table(names, countries):
    """The place table for every place id that appears: Natural Earth's name and middle where it has the code, else the name the source gave; `world` is its own place."""
    rows = []
    for pid in sorted(names):
        if pid == "world":
            rows.append({"place_id": "world", "level": "world", "parent": None, "name": "World", "lat": None, "lon": None})
        elif pid in countries:
            lat, lon = middle(countries[pid]["shape"])
            rows.append({"place_id": pid, "level": "country", "parent": "world", "name": countries[pid]["name"], "lat": lat, "lon": lon})
        else:
            rows.append({"place_id": pid, "level": "country", "parent": "world", "name": names[pid], "lat": None, "lon": None})
    return rows


def assign(lat, lon, countries):
    """The M49 code of the country each point lies in ('' for none), tested against each country's shape in code order, a point going to the first that holds it."""
    lat, lon = np.asarray(lat, dtype=float), np.asarray(lon, dtype=float)
    code = np.full(len(lat), "", dtype="U3")
    for c in sorted(countries):
        west, south, east, north = countries[c]["shape"].bounds
        near = np.flatnonzero((code == "") & (lat >= south) & (lat <= north) & (lon >= west) & (lon <= east))
        if len(near):
            code[near[contains_xy(countries[c]["shape"], lon[near], lat[near])]] = c
    return code


def periods(first_year, months):
    """`YYYY-MM` for each of `months` months from January of first_year."""
    return [f"{first_year + t // 12}-{t % 12 + 1:02d}" for t in range(months)]


def slug(text):
    """Lower-case letters, digits and underscores of a name."""
    return re.sub(r"[^a-z0-9]+", "_", html.unescape(text).lower()).strip("_")


def faostat(csv, countries_unused=None):
    """FAOSTAT crops: yield, area harvested and production of every crop (an item with an area harvested row, item code under 1700), by country and year, with the source's flag. Rows with no value and the China total are set aside and counted."""
    con = duckdb.connect()
    con.execute(f"""create view f as select * from read_csv('{csv}', header=true, all_varchar=true, encoding='utf-8')
        where cast("Item Code" as int) < 1700 and cast("Area Code" as int) < 5000 and "Element Code" in ('{FAO_YIELD}', '{FAO_AREA}', '{FAO_PRODUCTION}')""")
    con.execute(f"""create view crops as select distinct "Item Code" as i from f where "Element Code" = '{FAO_AREA}'""")
    totals = ", ".join(f"'{t}'" for t in TOTALS)
    con.execute(f"""create view k as select "Element Code" as e, cast("Item Code" as int) as item, replace("Area Code (M49)", '''', '') as m49, Area as area, Year as y,
        try_cast(Value as double) as v, Flag as flag from f where "Item Code" in (select i from crops)""")
    notes = {"rows with no value (all flagged M)": con.execute("select count(*) from k where v is null").fetchone()[0],
             "rows of the China total (M49 159)": con.execute(f"select count(*) from k where m49 in ({totals}) and v is not null").fetchone()[0]}
    names = dict(con.execute(f"select m49, min(area) from k where m49 not in ({totals}) group by m49 order by m49").fetchall())
    items = con.execute(f"select \"Item Code\", any_value(Item) from f where \"Item Code\" in (select i from crops) group by 1 order by cast(\"Item Code\" as int)").fetchall()
    m = manifest()
    series = []
    for e, (what, unit, transform, text) in FAO_ELEMENTS.items():
        for code, item in items:
            series.append(series_row(f"faostat_qcl:{what}:{int(code)}", "faostat_qcl", "crops", f"{text.capitalize()} of {item} (FAOSTAT item {int(code)})", unit, "level", transform, "country", "year", licence(m, "faostat_qcl")))
    flags = "case " + " ".join(f"when flag = '{k}' then '{v}'" for k, v in FAO_FLAGS.items()) + " else 'other' end"
    elements = "case " + " ".join(f"when e = '{k}' then '{v[0]}'" for k, v in FAO_ELEMENTS.items()) + " end"
    t = con.sql(f"""select 'faostat_qcl:' || {elements} || ':' || item as series_id, m49 as place_id, y as period, v as value, {flags} as flag
        from k where v is not null and m49 not in ({totals}) order by series_id, place_id, period""").to_arrow_table()
    return Part(series, t.cast(OBS_SCHEMA), names, notes)


def drought_obs(x, codes, first_year):
    """Observations of the drought series from the array yields.drought gives (countries by months from January of first_year): every finite value, with the country's code."""
    ps, pl, pr, vs = [], [], [], []
    stamp = periods(first_year, x.shape[1])
    for i, code in enumerate(codes):
        ok = np.flatnonzero(np.isfinite(x[i]))
        pl += [str(code)] * len(ok)
        pr += [stamp[t] for t in ok]
        vs.append(x[i][ok])
    value = np.concatenate(vs) if vs else np.array([])
    return obs_table("spei:spei3:country_mean", pl, pr, value)


def drought(countries):
    """Drought (SPEI-3): the country mean by month, as yields.drought makes it for the harvest test, for every country Natural Earth holds; countries with no cell that has a value every month have none."""
    from causal_atlas import yields

    codes = np.array(sorted(countries))
    x, cells, _ = yields.drought(codes)
    m = manifest()
    row = series_row("spei:spei3:country_mean", "spei", "climate", "SPEI-3 (3-month standardised precipitation-evapotranspiration index), mean over the half-degree cells whose centre lies in the country and that have a value every month 1960 to 2024",
                     "standard deviations", "index", "none", "country", "month", licence(m, "spei"))
    return Part([row], drought_obs(x, codes, yields.FIRST_YEAR - 1), {}, {"countries with a drought series": int((cells > 0).sum()), "countries tried": len(codes)})


def psl_read(path):
    """A monthly series in NOAA PSL's layout (a year, then twelve values) as {(year, month): value}, whatever years the file holds. Values below -90 and the file's own missing marker (the single number after its last year) are left out."""
    rows, marker = {}, None
    for line in open(path, errors="replace"):
        p = line.split()
        if len(p) == 13 and p[0].isdigit():
            try:
                rows[int(p[0])] = [float(v) for v in p[1:]]
            except ValueError:
                pass
        elif rows and marker is None and len(p) == 1:
            try:
                marker = float(p[0])
            except ValueError:
                pass
    return {(y, i + 1): v for y, vs in rows.items() for i, v in enumerate(vs) if v >= -90 and v != marker}


def climate_series(series_id, source, text, unit, kind, transform, lic, values):
    """A world series by month: its series row and observations."""
    keys = sorted(values)
    obs = obs_table(series_id, ["world"] * len(keys), [f"{y}-{mo:02d}" for y, mo in keys], [values[k] for k in keys])
    return series_row(series_id, source, "climate", text, unit, kind, transform, "world", "month", lic), obs


def indices(oni_path, candidates_dir, listing, wanted):
    """The ONI and the candidate climate indices, as world series by month. `listing` is the fetch's listing.json (label by file); `wanted` the file names the manifest holds."""
    m = manifest()
    labels = {i["file"]: html.unescape(i["label"]) for i in listing}
    series, tables = [], []
    s, o = climate_series("oni:oni:nino34_3month", "oni", "Oceanic Nino Index: 3-month running mean of sea-surface temperature anomaly in the Nino 3.4 region, centred on the month", "degrees C", "index", "none", licence(m, "oni"), psl_read(oni_path))
    series.append(s), tables.append(o)
    for f in wanted:
        kind = "count" if CLIMATE_UNITS.get(f) == "count" else "index"
        s, o = climate_series(f"candidates:{f}:monthly", f"candidates.{f}", f"{labels.get(f, f)} (NOAA PSL monthly time series, file {f})", CLIMATE_UNITS.get(f, "as published"), kind, "log1p" if kind == "count" else "none",
                              m["candidates"][f]["licence"], psl_read(Path(candidates_dir) / f))
        series.append(s), tables.append(o)
    return Part(series, pa.concat_tables(tables), {"world": "World"}, {})


def fire_obs(burned, flat, first_year, absent):
    """Burned area per country and month from the cube (months by cells, km2) and each cell's country code ('' for none): the sum over the country's cells. The month `absent` year, whose values are NaN, is left out."""
    ps, pl, vs = [], [], []
    stamp = periods(first_year, burned.shape[0])
    for c in sorted(set(flat) - {""}):
        total = burned[:, np.flatnonzero(flat == c)].astype(np.float64).sum(axis=1)
        ok = np.flatnonzero(np.isfinite(total))
        pl += [c] * len(ok)
        ps += [stamp[t] for t in ok]
        vs.append(total[ok])
    return obs_table("firecci:burned_area:country_total", pl, ps, np.concatenate(vs) if vs else np.array([]))


def fire(countries):
    """Burned area (Fire_cci) by country and month: the sum over the 0.5 degree cells whose centre lies in the country, km2 as the makers give it, 1982 to 2018 without 1994."""
    from causal_atlas import fire as f

    burned, _, burnable = f.grid()
    lat, lon = 89.75 - 0.5 * np.arange(360), -179.75 + 0.5 * np.arange(720)
    glon, glat = np.meshgrid(lon, lat)
    flat = assign(glat.ravel(), glon.ravel(), countries)
    m = manifest()
    row = series_row("firecci:burned_area:country_total", "firecci", "fire", "Burned area: the sum over the half-degree cells whose centre lies in the country (each the sum of four quarter-degree cells), as the makers give it, with no correction for the share of land observed",
                     "km2", "level", "log1p", "country", "month", licence(m, "firecci"))
    cells = burned.reshape(burned.shape[0], -1)
    notes = {"land cells with burnable land": int((burnable > 0).sum()), "of them inside no country": int(((burnable.ravel() > 0) & (flat == "")).sum())}
    return Part([row], fire_obs(cells, flat, f.FIRST_YEAR, f.ABSENT), {}, notes)


def ged_counts(csv, countries):
    """UCDP GED events and best-estimate deaths by country and month of the event's start. A point goes to the country whose shape holds it; events outside every shape are counted and set aside. Returns (code, month, events, deaths) rows and the set-aside count."""
    con = duckdb.connect()
    con.execute(f"""create view e as select left(date_start, 7) as mo, try_cast(latitude as double) as lat, try_cast(longitude as double) as lon, country,
        try_cast(best as double) as deaths from read_csv('{csv}', header=true, all_varchar=true)""")
    pts = con.execute("select distinct lat, lon from e where lat is not null and lon is not null order by lat, lon").fetchnumpy()
    code = assign(pts["lat"], pts["lon"], countries)
    con.register("pts", pa.table({"lat": pts["lat"], "lon": pts["lon"], "code": code}))
    rows = con.execute("""select p.code, e.mo, count(*) as events, sum(e.deaths) as deaths from e join pts p on e.lat = p.lat and e.lon = p.lon
        where p.code <> '' group by 1, 2 order by 1, 2""").fetchall()
    total = con.execute("select count(*) from e").fetchone()[0]
    kept = sum(r[2] for r in rows)
    named = con.execute("""select count(*) from e join pts p on e.lat = p.lat and e.lon = p.lon where p.code = ''""").fetchone()[0]
    return rows, {"events in the file": total, "events inside a country's shape": kept, "events outside every shape (set aside)": named, "events with no coordinates (set aside)": total - kept - named}


def ged(csv, countries):
    """Organised-violence events and deaths (UCDP GED) by country and month: two count series, a month with no event simply has no row."""
    rows, notes = ged_counts(csv, countries)
    m = manifest()
    out = []
    for key, text, unit in (("events", "Events of organised violence with at least one death, by start month", "events"), ("deaths_best", "Deaths in those events, the file's best estimate", "deaths")):
        out.append(series_row(f"ucdp_ged:{key}:country_total", "ucdp_ged", "conflict", text + ", by country (the country whose shape holds the event's point)", unit, "count", "log1p", "country", "month", licence(m, "ucdp_ged")))
    t = [obs_table(f"ucdp_ged:{key}:country_total", [r[0] for r in rows], [r[1] for r in rows], [r[i] for r in rows]) for key, i in (("events", 2), ("deaths_best", 3))]
    return Part(out, pa.concat_tables(t), {}, notes)


def prices(csv, countries):
    """Staple prices by country and month: the median over the markets with a price as collected (the plain item columns, never the file's model estimates). The file's ISO3 code is matched to Natural Earth's codes."""
    iso = {i: c for c, d in countries.items() for i in d["iso"]}
    con = duckdb.connect()
    cols = ", ".join(f'try_cast("{c}" as double) as "{c}"' for c in STAPLES)
    con.execute(f"""create view p as select ISO3, geo_id, left(price_date, 7) as mo, {cols} from read_csv('{csv}', header=true, all_varchar=true)""")
    long = f"(unpivot p on {', '.join(STAPLES)} into name item value price)"
    got = con.execute(f"select ISO3, item, mo, median(price) as price from {long} where price > 0 group by all order by all").fetchall()
    unmapped = sorted({r[0] for r in got if r[0] not in iso})
    got = [r for r in got if r[0] in iso]
    m = manifest()
    series = [series_row(f"rtfp:{s}:median_market", "rtfp", "prices", f"Price of {s.replace('_', ' ')} as collected: the median over the country's markets with a price that month", "local currency per unit as collected (currency differs by country)", "level", "log", "country", "month", licence(m, "rtfp")) for s in STAPLES]
    tables = [obs_table(f"rtfp:{s}:median_market", [iso[r[0]] for r in got if r[1] == s], [r[2] for r in got if r[1] == s], [r[3] for r in got if r[1] == s]) for s in STAPLES]
    return Part(series, pa.concat_tables(tables), {}, {"ISO3 codes with no Natural Earth match (set aside)": unmapped})


def wdi_unit(name, measure):
    """An indicator's unit: the bracket that ends its name, else the series file's unit of measure, else 'as published'."""
    m = re.search(r"\(([^()]*)\)\s*$", name)
    return m.group(1) if m else (measure or "as published")


def wdi_shape(name, unit, lowest):
    """(kind, transform) of an indicator from its name and unit text and its lowest value: rates and shares and indices are taken as they are (`none`); a quantity is `log` if every value is above zero, `log1p` if none is below zero, else `none`. Never `count`: a missing year is not a zero."""
    text = f"{name} {unit}".lower()
    if WDI_INDEX.search(text):
        return "index", "none"
    if WDI_RATE.search(text):
        return "rate", "none"
    return "level", "log" if lowest > 0 else "log1p" if lowest == 0 else "none"


def wdi(data_csv, series_csv, country_csv, countries, min_countries=WDI_COUNTRIES, min_years=WDI_YEARS):
    """World Development Indicators by country and year: countries only (the country file gives a region to countries and none to aggregates), ISO3 matched to Natural Earth's codes. An indicator is kept if its licence is CC BY-4.0 in the series file and `min_countries` mapped countries each have `min_years` yearly values; the counts kept and dropped by each condition go in the notes."""
    iso = {i: c for c, d in countries.items() for i in d["iso"]}
    con = duckdb.connect()
    con.execute("set threads=3")
    for name, path in (("cn", country_csv), ("sr", series_csv), ("d", data_csv)):
        con.execute(f"create view {name} as select * from read_csv('{path}', header=true, all_varchar=true)")
    con.register("isomap", pa.table({"code": list(iso), "m49": [iso[k] for k in iso]}))
    years = [r[0] for r in con.execute("select column_name from (describe d) where regexp_matches(column_name, '^[0-9]{4}$') order by 1").fetchall()]
    con.execute("create table c as select \"Country Code\" as code, \"Short Name\" as name from cn where coalesce(Region, '') <> ''")
    cast = ", ".join(f'try_cast("{y}" as double) as "{y}"' for y in years)
    con.execute(f"""create table va as select ind, cc, cast(year as int) as year, v from (unpivot (select "Indicator Code" as ind, "Country Code" as cc, {cast} from d)
        on {", ".join(f'"{y}"' for y in years)} into name year value v) where v is not null""")
    con.execute("create table v as select va.ind, m.m49 as place, va.year, va.v from va join c on c.code = va.cc join isomap m on m.code = va.cc")
    con.execute("create table meta as select \"Series Code\" as ind, \"Indicator Name\" as name, Topic as topic, \"Unit of measure\" as measure, \"License Type\" as lic from sr")
    con.execute(f"""create table enough as select ind from (select ind, place from v group by 1, 2 having count(*) >= {min_years}) group by 1 having count(*) >= {min_countries}""")
    con.execute(f"create table kept as select m.*, (select min(v) from v where v.ind = m.ind) as lowest from meta m where lic = '{WDI_LICENCE}' and ind in (select ind from enough) order by ind")
    one = lambda q: con.execute(q).fetchone()[0]
    unmapped = sorted(r[0] for r in con.execute("select code from c where code not in (select code from isomap)").fetchall())
    series, kinds, domains = [], {}, {}
    m = manifest()
    for ind, name, topic, measure, lowest in con.execute("select ind, name, topic, measure, lowest from kept").fetchall():
        first = (topic or "").split(":")[0].strip().lower()
        domain = WDI_DOMAINS.get(first) or slug(first) or "other"
        unit = wdi_unit(name, measure)
        kind, transform = wdi_shape(name, unit, lowest)
        kinds[f"{kind}/{transform}"] = kinds.get(f"{kind}/{transform}", 0) + 1
        domains[domain] = domains.get(domain, 0) + 1
        series.append(series_row(f"wdi:{ind}", "wdi", domain, name, unit, kind, transform, "country", "year", licence(m, "wdi")))
    obs = con.sql("select 'wdi:' || ind as series_id, place as place_id, cast(year as varchar) as period, v as value, null as flag from v where ind in (select ind from kept) order by series_id, place_id, period").to_arrow_table()
    notes = {"indicators in the series file": one("select count(*) from meta"),
             "dropped by licence (not CC BY-4.0 in the series file)": one(f"select count(*) from meta where coalesce(lic, '') <> '{WDI_LICENCE}'"),
             f"dropped by the count rule alone ({min_countries} countries with {min_years} yearly values; any licence)": one("select count(*) from meta where ind not in (select ind from enough)"),
             "dropped by the count rule after the licence": one(f"select count(*) from meta where lic = '{WDI_LICENCE}' and ind not in (select ind from enough)"),
             "indicators kept": one("select count(*) from kept"), "kept by domain": dict(sorted(domains.items())), "kept by kind and transform": dict(sorted(kinds.items())),
             "aggregate and unclassified codes in the data file (dropped)": one("select count(distinct cc) from va where cc not in (select code from c)"),
             "values in those codes (dropped)": one("select count(*) from va where cc not in (select code from c)"),
             "country codes with no Natural Earth match (set aside)": unmapped, "values in those codes (set aside)": one("select count(*) from va where cc in (select code from c where code not in (select code from isomap))")}
    names = dict(con.execute("select m.m49, c.name from c join isomap m on m.code = c.code order by 1").fetchall())
    return Part(series, obs.cast(OBS_SCHEMA), names, notes)


def write_part(name, part):
    """Save a source's part under data/table/parts."""
    PARTS.mkdir(parents=True, exist_ok=True)
    pq.write_table(part.obs, PARTS / f"{name}.obs.parquet")
    (PARTS / f"{name}.meta.json").write_text(json.dumps({"series": part.series, "names": part.names, "notes": part.notes}, indent=1, sort_keys=True))


def assemble(parts_dir, out_dir, countries):
    """Join the saved parts into series, place and obs under out_dir: sorted, so a second build gives identical tables. Fails if a series, place and period occur twice."""
    parts_dir, out_dir = Path(parts_dir), Path(out_dir)
    metas = [json.loads(p.read_text()) for p in sorted(parts_dir.glob("*.meta.json"))]
    series = sorted((s for m in metas for s in m["series"]), key=lambda s: s["series_id"])
    names = {k: v for m in metas for k, v in m["names"].items()}
    con = duckdb.connect()
    con.execute("set threads=3")
    con.execute(f"create table obs as select * from read_parquet('{parts_dir}/*.obs.parquet') order by series_id, place_id, period")
    dup = con.execute("select count(*) from (select 1 from obs group by series_id, place_id, period having count(*) > 1)").fetchone()[0]
    if dup:
        raise ValueError(f"{dup} series, place and period occur more than once")
    used = {r[0] for r in con.execute("select distinct place_id from obs").fetchall()}
    place = place_table({p: names.get(p, p) for p in used}, countries)
    con.register("s", pa.Table.from_pylist(series))
    con.register("pl", pa.Table.from_pylist(place, schema=pa.schema([("place_id", pa.string()), ("level", pa.string()), ("parent", pa.string()), ("name", pa.string()), ("lat", pa.float64()), ("lon", pa.float64())])))
    con.execute("""create table series as select s.series_id, source, domain, measures, unit, kind, transform, place_level, s.period, o."first", o."last", licence
        from s join (select series_id, min(period) as "first", max(period) as "last" from obs group by 1) o using (series_id) order by series_id""")
    con.execute("create table place as select * from pl order by place_id")
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in ("series", "place", "obs"):
        con.execute(f"copy {t} to '{out_dir / (t + '.parquet')}' (format parquet)")
    return {t: con.execute(f"select count(*) from {t}").fetchone()[0] for t in ("series", "place", "obs")}
