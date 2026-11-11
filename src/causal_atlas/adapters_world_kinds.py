"""Four sources of kinds the table lacked, each covering most of the world, in the shape of table.py, one adapter a source: people forced to move (UNHCR's refugee statistics, by
country of origin and by country of asylum, by year), tropical cyclones (NOAA's IBTrACS best tracks, by country and month, and for the world), electricity generation by source
(Ember, by country, by month and by year) and commodity prices (the World Bank's "Pink Sheet", world series by month, and by year where the yearly record reaches further back).
Each returns a table.Part; the licence line is passed in, not read from the manifest. Each function says, for each series, whether a period with no row is a zero or nothing,
and why. The cut kept is fixed by the brief: totals and physical quantities as the source gives them, no figure per head or per unit of output, a monthly record where the source
has one and the yearly one beside it only where it reaches further back. Nothing here sets one series beside another."""
import json
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

import duckdb
import pyarrow as pa

from causal_atlas.adapters_events import iso_to_m49, months
from causal_atlas.table import OBS_SCHEMA, Part, assign, obs_table, series_row, slug

# UNHCR: in both files no asylum seeker figure other than "0" is written before 1993, so the earlier zeros are read as not collected and the two asylum seeker series begin
# in 1993 (counted from the files, docs/reading/sources-world-kinds.md). Codes that name no country (stateless, unknown, Tibetan) are set aside and counted.
UNHCR_ASYLUM_SEEKERS_FIRST = 1993
UNHCR_FIGURES = {"refugees": "Refugees under UNHCR's mandate", "asylum_seekers": "Asylum seekers (pending cases)"}
UNHCR_SIDES = {"origin": ("coo_iso", "coo_name", "by country of origin"), "asylum": ("coa_iso", "coa_name", "by country of asylum")}

# IBTrACS: the archive's technical document (section 8.2) offers the file from 1980 as "considered by many to be the modern era, since geostationary satellite coverage was
# nearly global", and its Table 2 gives position errors as larger before 1980; the file used is that one. A storm is counted if its strongest wind in the US agencies' column (one averaging period, 1 minute, for every basin) reaches tropical storm strength, 34 knots.
IB_FIRST, IB_LAST = "1980-01", "2026-10"  # the last whole month before the file was fetched on 2026-11-11
IB_STORM_KT = 34.0

# Ember: the electricity sources asked for, by the file's own names (matched without regard to case).
EMBER_SOURCES = {"total generation": "total", "coal": "coal", "gas": "gas", "wind": "wind", "solar": "solar", "hydro": "hydro", "nuclear": "nuclear"}

# The Pink Sheet: the sheets read, and the markers the workbook uses for a period with no price.
PINK_MONTHLY_SHEET, PINK_ANNUAL_SHEET = "Monthly Prices", "Annual Prices (Nominal)"
PINK_MISSING = {"", "…", "...", "..", ".."}

XLSX = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def shape(lowest):
    """Kind and transform of a level series from its lowest value: log when every value is above zero, log1p when zeros occur, none otherwise."""
    return "level", "log" if lowest > 0 else "log1p" if lowest == 0 else "none"


def number(v):
    """An integer or a number written as text ("0" in UNHCR's files); None for anything else ("-")."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return float(v)
    try:
        return float(str(v).strip())
    except ValueError:
        return None


def unhcr(origin_json, asylum_json, countries, lic, asylum_seekers_first=UNHCR_ASYLUM_SEEKERS_FIRST):
    """Refugees and asylum seekers by year, once by country of origin and once by country of asylum, from the two answers of UNHCR's population API. A country-year has a
    row in the source only where some figure for it is not zero, and the source writes a zero as "0" where another figure in the row is not; so a year with no row is written
    as nothing, not as zero (the API does not say whether such a country was watched and had none, or was not reported), and a "0" in a row is written as 0. Asylum seekers
    are written from `asylum_seekers_first` only: before it neither file holds any figure but "0", read as not collected. Kind level, not count: these are stocks at the end of
    the year, not events in it."""
    m49 = iso_to_m49(countries)
    values, names, notes = defaultdict(float), {}, {}
    unmatched, repeated = Counter(), Counter()
    seen = set()
    for side, path in (("origin", origin_json), ("asylum", asylum_json)):
        iso_key, name_key, _ = UNHCR_SIDES[side]
        with open(path, encoding="utf-8") as f:
            items = json.load(f)["items"]
        notes[f"rows in the file (by {side})"] = len(items)
        for it in items:
            iso, year = str(it.get(iso_key, "")).strip(), int(it["year"])
            code = m49.get(iso)
            if code is None:
                unmatched[f"{iso} ({str(it.get(name_key, '')).strip()}; by {side})"] += 1
                continue
            if (side, code, year) in seen:
                repeated[f"{iso} (by {side})"] += 1
            seen.add((side, code, year))
            for fig in UNHCR_FIGURES:
                v = number(it.get(fig))
                if v is None or (fig == "asylum_seekers" and year < asylum_seekers_first):
                    continue
                values[(fig, side, code, str(year))] += v
    notes["codes with no Natural Earth match (set aside; rows)"] = dict(unmatched)
    notes["codes with more than one row in a year (their figures summed; rows)"] = dict(repeated)
    series, obs = [], []
    for fig, text in UNHCR_FIGURES.items():
        for side, (_, _, where) in UNHCR_SIDES.items():
            keys = sorted(k for k in values if k[0] == fig and k[1] == side)
            if not keys:
                continue
            sid = f"unhcr:{fig}:country_of_{side}"
            kind, transform = shape(min(values[k] for k in keys))
            since = f", from {asylum_seekers_first}" if fig == "asylum_seekers" else ""
            series.append(series_row(sid, "unhcr", "people", f"{text}, {where}, at the end of each calendar year{since}", "people", kind, transform, "country", "year", lic))
            obs.append(obs_table(sid, [k[2] for k in keys], [k[3] for k in keys], [values[k] for k in keys]))
    return Part(series, pa.concat_tables(obs).cast(OBS_SCHEMA), names, notes)


def ibtracs(csv, countries, lic, first=IB_FIRST, last=IB_LAST, storm_kt=IB_STORM_KT):
    """Tropical cyclones by month from the IBTrACS CSV. Spur tracks (the archive's alternative positions beside a storm's main track) are set aside. A storm is counted if its
    strongest wind in USA_WIND anywhere in its life reaches `storm_kt`; every position of a counted storm is then used, whatever the agencies call its nature at that time.
    Positions are placed in a country by the country's shape (Natural Earth), month by the UTC month of the position's time; positions before `first` or after `last` are set
    aside. Three series:
    - storms per country and month: storms with at least one position inside the country's shape. The archive gathers every agency's tracks over the whole globe, so every
      country and month in the span is written, zero where no counted storm passed: a zero here is an observed zero.
    - the strongest wind per country and month: the highest USA_WIND at a position inside the shape. Written only where a counted storm passed and some position inside carries
      a wind; nothing elsewhere, because a month with no storm has no storm wind to record, and zero would claim a calm the series does not measure.
    - storms per month for the world: counted storms with any position in the month, at sea included; every month written, zero where none.
    A month to which a provisional track (one not yet reanalysed by its agency) contributes is flagged "provisional"."""
    con = duckdb.connect(config={"threads": 1, "memory_limit": "1GB"})
    con.execute(f"""create table p as select SID as sid, TRACK_TYPE as track, ISO_TIME as t, try_cast(LAT as double) as lat, try_cast(LON as double) as lon,
        try_cast(nullif(trim(USA_WIND), '') as double) as wind from read_csv('{csv}', header=true, all_varchar=true) where trim(SID) <> ''""")
    one = lambda s: con.execute(s).fetchall()[0][0]
    notes = {"positions in the file": one("select count(*) from p"), "storms in the file": one("select count(distinct sid) from p"),
             "positions on spur tracks (set aside)": one("select count(*) from p where lower(track) like '%spur%'")}
    con.execute("delete from p where lower(track) like '%spur%'")
    con.execute(f"""create table s as select sid from p group by sid having max(wind) >= {storm_kt}""")
    notes[f"storms whose strongest USA_WIND reaches {storm_kt} kt (counted)"] = one("select count(*) from s")
    notes[f"storms set aside: no USA_WIND, or below {storm_kt} kt"] = one("select count(distinct sid) from p") - one("select count(*) from s")
    rows = con.execute(f"""select p.sid, left(t, 7) as mo, lat, case when lon > 180 then lon - 360 else lon end as lon, wind, track ilike '%provisional%' as prov
        from p join s using (sid) where lat is not null and lon is not null order by p.sid, t""").fetchall()
    con.close()
    inside = [r for r in rows if first <= r[1] <= last]
    notes["positions of counted storms outside the span (set aside)"] = len(rows) - len(inside)
    code = assign([r[2] for r in inside], [r[3] for r in inside], countries)
    notes["positions of counted storms in no country's shape, at sea (world series only)"] = int((code == "").sum())
    span = months(first, last)
    world, world_prov = defaultdict(set), set()
    passes, wind, prov = defaultdict(set), {}, set()
    for (sid, mo, _, _, w, pv), c in zip(inside, code):
        world[mo].add(sid)
        if pv:
            world_prov.add(mo)
        if not c:
            continue
        passes[(c, mo)].add(sid)
        if pv:
            prov.add((c, mo))
        if w is not None and w == w:
            wind[(c, mo)] = max(wind.get((c, mo), w), w)
    flag = lambda key, pv: "provisional" if key in pv else ""
    grid = [(c, mo) for c in sorted(countries) for mo in span]
    wk = sorted(wind)
    where = "positions every three hours or so placed in a country by its shape (Natural Earth), month of the position's time (UTC)"
    series = [series_row("ibtracs:storms:country_total", "ibtracs", "disasters", f"Tropical cyclones (lifetime strongest wind at least {storm_kt:g} kt, US agencies' 1-minute winds) with a position inside the country, {where}", "storms", "count", "log1p", "country", "month", lic),
              series_row("ibtracs:max_wind:country_total", "ibtracs", "disasters", f"Strongest wind (USA_WIND, 1-minute sustained) at a position of such a storm inside the country, {where}; written only where a storm passed", "kt", *shape(min(wind.values()) if wind else 1.0), "country", "month", lic),
              series_row("ibtracs:storms:world", "ibtracs", "disasters", f"Tropical cyclones (lifetime strongest wind at least {storm_kt:g} kt) with any position in the month, at sea included", "storms", "count", "log1p", "world", "month", lic)]
    obs = pa.concat_tables([obs_table("ibtracs:storms:country_total", [g[0] for g in grid], [g[1] for g in grid], [len(passes.get(g, ())) for g in grid], [flag(g, prov) for g in grid]),
                            obs_table("ibtracs:max_wind:country_total", [k[0] for k in wk], [k[1] for k in wk], [wind[k] for k in wk], [flag(k, prov) for k in wk]),
                            obs_table("ibtracs:storms:world", ["world"] * len(span), span, [len(world.get(mo, ())) for mo in span], [flag(mo, world_prov) for mo in span])])
    notes["country-months with a storm"] = len(passes)
    notes["country-months with a storm but no wind at a position inside (no wind written)"] = len(set(passes) - set(wind))
    return Part(series, obs.cast(OBS_SCHEMA), {"world": "World"}, notes)


def ember(monthly_csv, yearly_csv, countries, lic):
    """Electricity generation in TWh by country, in all and from coal, gas, wind, solar, hydro and nuclear, from Ember's monthly and yearly files. Both are taken whole: the
    yearly file reaches further back (from 1985) and holds far more countries than the monthly, so the brief's rule keeps it beside the monthly. Regions and the world, which
    Ember estimates, are not taken. A period with no row is written as nothing, not zero: Ember's methodology speaks of "the few cases where a specific fuel is not
    available in monthly data", so a missing month is a figure not given, not a fuel not used; the yearly file writes its zeros as rows of its own. Zeros the source wrote are kept."""
    m49 = iso_to_m49(countries)
    con = duckdb.connect(config={"threads": 1, "memory_limit": "1GB"})
    wanted = ", ".join(f"'{k}'" for k in EMBER_SOURCES)
    series, obs, notes = [], [], {}
    for period, path, col in (("month", monthly_csv, "Date"), ("year", yearly_csv, "Year")):
        rows = con.execute(f"""select "ISO 3 code", lower(trim("Electricity source")), "{col}", try_cast("Generation (TWh)" as double)
            from read_csv('{path}', header=true, all_varchar=true) where "Area type" = 'Country or economy' and lower(trim("Electricity source")) in ({wanted})""").fetchall()
        unmatched, empty, values = Counter(), 0, defaultdict(dict)
        for iso, src, when, v in rows:
            code = m49.get((iso or "").strip())
            if code is None:
                unmatched[iso] += 1
                continue
            if v is None:
                empty += 1
                continue
            values[EMBER_SOURCES[src]][(code, when[:7] if period == "month" else when[:4])] = v
        notes[f"rows of countries with no Natural Earth match (set aside; by {period})"] = dict(unmatched)
        notes[f"rows with no generation figure (set aside; by {period})"] = empty
        for key in EMBER_SOURCES.values():
            got = values.get(key)
            if not got:
                continue
            sid = f"ember:generation_{key}:country_total" + (":year" if period == "year" else "")
            what = "Electricity generation in all" if key == "total" else f"Electricity generation from {key}"
            ks = sorted(got)
            series.append(series_row(sid, "ember", "energy", f"{what}, by country, by calendar {period} (Ember)", "TWh", *shape(min(got.values())), "country", period, lic))
            obs.append(obs_table(sid, [k[0] for k in ks], [k[1] for k in ks], [got[k] for k in ks]))
    con.close()
    return Part(series, pa.concat_tables(obs).cast(OBS_SCHEMA), {}, notes)


def xlsx_rows(path, sheet):
    """The rows of one sheet of an .xlsx workbook as (row number, {column letter: text}), read with the standard library: shared strings resolved, empty cells left out."""
    with zipfile.ZipFile(path) as z:
        book = ET.fromstring(z.read("xl/workbook.xml"))
        target = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        where = {s.get("name"): target[s.get("{%s}id" % XLSX["r"])] for s in book.find("m:sheets", XLSX)}
        strings = []
        if "xl/sharedStrings.xml" in z.namelist():
            strings = ["".join(t.text or "" for t in si.iter("{%s}t" % XLSX["m"])) for si in ET.fromstring(z.read("xl/sharedStrings.xml"))]
        part = where[sheet].lstrip("/")
        root = ET.fromstring(z.read(part if part.startswith("xl/") else "xl/" + part))
    for row in root.iter("{%s}row" % XLSX["m"]):
        out = {}
        for c in row.findall("m:c", XLSX):
            t, v = c.get("t"), c.find("m:v", XLSX)
            if t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % XLSX["m"]))
            elif v is None:
                continue
            else:
                val = strings[int(v.text)] if t == "s" else v.text
            out[re.match(r"[A-Z]+", c.get("r")).group()] = val
        yield int(row.get("r")), out


def pink_table(path, sheet, pattern):
    """One price sheet of the Pink Sheet: {clean name: (unit, {period: value})}. The data rows are those whose first cell matches `pattern`; the names are two rows above the
    first of them and the units one row above, as both workbooks lay them out. A column whose unit is an index (`=100`) is not a price and is left out."""
    rows = list(xlsx_rows(path, sheet))
    by_number = dict(rows)
    first = next(i for i, (_, r) in enumerate(rows) if re.fullmatch(pattern, r.get("A", "").strip()))
    names, units = by_number.get(rows[first][0] - 2, {}), by_number.get(rows[first][0] - 1, {})
    out, missing, skipped, bad = {}, 0, [], Counter()
    for col, raw in names.items():
        if col == "A":
            continue
        name = re.sub(r"\s+", " ", raw.replace("*", "")).strip()
        unit = units.get(col, "").strip().strip("()")
        if "=100" in unit:
            skipped.append(name)
            continue
        got = {}
        for _, r in rows[first:]:
            when = r.get("A", "").strip()
            if not re.fullmatch(pattern, when):
                continue
            v = r.get(col, "").strip()
            if v in PINK_MISSING:
                missing += 1
                continue
            try:
                x = float(v)
            except ValueError:  # a spreadsheet error such as "#VALUE!": set aside, counted
                bad[f"{name} {when}: {v}"] += 1
                continue
            if x <= 0:  # a price of zero or less is no price: set aside, counted
                bad[f"{name} {when}: {v}"] += 1
                continue
            got[when[:4] + "-" + when[5:] if "M" in when else when] = x
        out[name] = (unit, got)
    return out, missing, skipped, dict(bad)


def pink_sheet(monthly_xlsx, annual_xlsx, lic):
    """The World Bank's commodity prices in nominal US dollars, each a world series (place `world`): every price of the monthly sheet by month, and the annual sheet's price by
    year beside it only where the yearly record begins in an earlier year than the monthly one (the brief's rule; the yearly series is then written whole). A period the
    workbook marks as unavailable ("..", "…") is written as nothing: a price not given is not a price of zero. A cell holding a spreadsheet error, or a price of zero or less
    (the monthly sheet writes 0 for Thai 25% rice from March to June 2008), is set aside and named in the notes. Indices are left out."""
    monthly, m_missing, m_skipped, m_bad = pink_table(monthly_xlsx, PINK_MONTHLY_SHEET, r"\d{4}M\d{2}")
    annual, a_missing, a_skipped, a_bad = pink_table(annual_xlsx, PINK_ANNUAL_SHEET, r"\d{4}")
    notes = {"cells marked unavailable (not written; monthly)": m_missing, "cells marked unavailable (not written; annual)": a_missing,
             "cells that are not numbers above zero (set aside; monthly)": m_bad, "cells that are not numbers above zero (set aside; annual)": a_bad,
             "index columns left out": sorted(set(m_skipped) | set(a_skipped)),
             "annual prices with no monthly column of the same name (not written)": sorted(set(annual) - set(monthly))}
    series, obs, yearly = [], [], []
    for name, (unit, got) in sorted(monthly.items()):
        if not got:
            continue
        sid = f"pink_sheet:{slug(name)}:world"
        ks = sorted(got)
        series.append(series_row(sid, "pink_sheet", "prices", f"{name}, world price by month, nominal (World Bank commodity price data)", unit, *shape(min(got.values())), "world", "month", lic))
        obs.append(obs_table(sid, ["world"] * len(ks), ks, [got[k] for k in ks]))
        a_unit, a_got = annual.get(name, ("", {}))
        if a_got and min(a_got) < min(ks)[:4]:
            yearly.append(f"{name} ({min(a_got)}, monthly from {min(ks)[:4]})")
            ys = sorted(a_got)
            series.append(series_row(sid + ":year", "pink_sheet", "prices", f"{name}, world price by year, nominal (World Bank commodity price data)", a_unit, *shape(min(a_got.values())), "world", "year", lic))
            obs.append(obs_table(sid + ":year", ["world"] * len(ys), ys, [a_got[k] for k in ys]))
    notes["prices whose yearly record begins earlier than the monthly (yearly written)"] = yearly
    return Part(series, pa.concat_tables(obs).cast(OBS_SCHEMA), {"world": "World"}, notes)
