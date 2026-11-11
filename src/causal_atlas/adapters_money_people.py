"""Money, births and deaths by country, in the shape of table.py: BIS policy rates, long consumer prices, residential property prices, credit and effective exchange rates; the Human Fertility Database's monthly births (Short-Term Fertility Fluctuations); Eurostat's deaths by month. One function a source, each returning a table.Part; the licence text is passed in. Nothing here sets one series beside another."""
import duckdb
import pyarrow as pa
import shapefile

from causal_atlas.panel import RAW
from causal_atlas.table import OBS_SCHEMA, Part, series_row
from causal_atlas.yields import BY_NAME

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
BIS_FLAGS = {"E": "estimated", "B": "other"}  # A (normal value) carries no flag; M and H (missing) never carry a value here
HFD_NATIONAL = {"DEUTNP": "DEU", "FRATNP": "FRA", "GBR_NP": "GBR"}  # the database's codes for a whole country's population; other codes with a suffix are parts of a country
EUROSTAT_GEO = {"EL": "GR", "UK": "GB", "DE_TOT": "DE"}  # Eurostat's own spellings; DE_TOT is Germany including the former GDR, the same territory as Germany today, from 1960
EUROSTAT_SKIP = {"DE": "Germany from 1991 only (DE_TOT is the longer record of the same territory)", "FX": "Metropolitan France (FR is the country Natural Earth draws)"}

# The series kept from each BIS file: (slug, condition on the codes, measures, unit, kind, transform, how a period is made).
# Price indices are level/log as in table.faostat_cp; a per cent is rate/none as in table.wdi_shape.
BIS_PICKS = {
    "bis_cbpol": [("policy_rate", "FREQ = 'M'", "Central bank policy rate, end of month", "percent per year", "rate", "none", "month")],
    "bis_long_cpi": [("cpi_index", "FREQ = 'M' and UNIT_MEASURE = '628'", "Consumer price index, long series as the BIS assembles it, by month", "index (2010 = 100)", "level", "log", "month"),
                     ("cpi_index:year", "FREQ = 'A' and UNIT_MEASURE = '628'", "Consumer price index, long series as the BIS assembles it, the year's value", "index (2010 = 100)", "level", "log", "year")],
    "bis_spp": [("nominal_index", "FREQ = 'Q' and VALUE = 'N' and UNIT_MEASURE = '628'", "Residential property prices, nominal: the mean of the year's four quarterly values, years with all four only", "index (2010 = 100)", "level", "log", "mean4")],
    "bis_tc": [(s, f"FREQ = 'Q' and TC_BORROWERS = '{b}' and TC_LENDERS = '{l}' and VALUATION = '{v}' and UNIT_TYPE = '770' and TC_ADJUST = 'A'", f"{t}, per cent of GDP, adjusted for breaks: the fourth quarter's end-of-period value", "percent of GDP", "rate", "none", "q4")
               for s, b, l, v, t in (("private_nonfinancial", "P", "A", "M", "Credit to the private non-financial sector from all sectors, market value"),
                                     ("households", "H", "A", "M", "Credit to households and non-profit institutions serving households from all sectors, market value"),
                                     ("nonfinancial_corporations", "N", "A", "M", "Credit to non-financial corporations from all sectors, market value"),
                                     ("private_nonfinancial_banks", "P", "B", "M", "Credit to the private non-financial sector from domestic banks, market value"),
                                     ("government_nominal", "G", "A", "N", "Credit to general government from all sectors, nominal value"))],
    "bis_eer": [(f"{t.lower()}_{b.lower()}", f"FREQ = 'M' and EER_TYPE = '{t[0]}' and EER_BASKET = '{b[0]}'", f"{t} effective exchange rate, {b.lower()} basket, average of the month", "index (2020 = 100)", "level", "log", "month")
                for t in ("Nominal", "Real") for b in ("Broad", "Narrow")],
}
BIS_AREA = {"bis_tc": "BORROWERS_CTY"}  # every other BIS file names its place REF_AREA


def iso2_codes(countries, path=None):
    """Natural Earth's two-letter codes (ISO_A2, else ISO_A2_EH) to the table's place ids, by table.natural_earth's code rule, for the codes in `countries` only. A two-letter code claimed by two places is left out and returned beside the map."""
    reader = shapefile.Reader(str(path or RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    fields = [f[0] for f in reader.fields[1:]]
    seen = {}
    for r in reader.iterRecords():
        rec = dict(zip(fields, r))
        code = BY_NAME.get(rec["ADM0_A3"], str(rec["UN_A3"]).zfill(3))
        if code in countries:
            for a2 in {rec["ISO_A2"], rec["ISO_A2_EH"]} - {"-99"}:
                seen.setdefault(a2, set()).add(code)
    return {a2: c.pop() for a2, c in seen.items() if len(c) == 1}, sorted(a2 for a2, c in seen.items() if len(c) > 1)


def bis_view(con, csv):
    """A BIS flat CSV as view `v`: each column named by the code before its colon (FREQ, REF_AREA, ...), each value cut to the code before ': ', the place's name kept as AREA_NAME and the value as a number."""
    cols = [r[0] for r in con.execute(f"describe select * from read_csv('{csv}', header=true, all_varchar=true)").fetchall()]
    keep = {c.split(":")[0]: c for c in cols}
    area = next(k for k in ("REF_AREA", "BORROWERS_CTY") if k in keep)
    sel = [f"""split_part("{c}", ':', 1) as {k}""" for k, c in keep.items() if k not in ("TIME_PERIOD", "OBS_VALUE")]
    con.execute(f"""create or replace view v as select {', '.join(sel)}, trim(substr("{keep[area]}", strpos("{keep[area]}", ':') + 1)) as AREA_NAME,
        "{keep['TIME_PERIOD']}" as TIME_PERIOD, try_cast("{keep['OBS_VALUE']}" as double) as OBS_VALUE from read_csv('{csv}', header=true, all_varchar=true)""")


def bis(csv, source, iso2, lic, picks=None):
    """One BIS bulk file (the flat CSV) as a Part: the series in BIS_PICKS[source] by country. Rows with no time period (the file's series-level rows), rows marked missing or with no value, and places with no Natural Earth two-letter match (groups of economies) are set aside and counted. A quarterly series becomes yearly: `q4` takes the fourth quarter's end-of-period value, `mean4` the mean of the four quarters where all four are present."""
    picks = picks or BIS_PICKS[source]
    con = duckdb.connect(config={"threads": 1, "memory_limit": "1GB"})
    bis_view(con, csv)
    area = BIS_AREA.get(source, "REF_AREA")
    one = lambda q: con.execute(q).fetchall()[0][0]
    union = " union all ".join(f"select '{s}' as k, {area} as a, AREA_NAME as name, TIME_PERIOD as t, OBS_VALUE as v, OBS_STATUS as st, '{rule}' as rule from v where TIME_PERIOD is not null and {cond}"
                               for s, cond, _, _, _, _, rule in picks)
    con.execute(f"create table a as {union}")
    notes = {"rows in the file": one("select count(*) from v"), "series-level rows with no time period (not observations)": one("select count(*) from v where TIME_PERIOD is null"),
             "rows of the kept series": one("select count(*) from a"), "rows marked missing or with no value (set aside)": one("select count(*) from a where v is null or isnan(v) or st in ('M', 'H')")}
    con.register("iso", pa.table({"a": list(iso2), "place": [iso2[k] for k in iso2]}))
    con.execute("create table b as select a.*, iso.place from a join iso using (a) where v is not null and not isnan(v) and coalesce(st, '') not in ('M', 'H')")
    notes["places with no Natural Earth match (set aside; rows)"] = dict(con.execute("select a || ' ' || any_value(name), count(*) from a where a not in (select a from iso) and v is not null group by a order by 1").fetchall())
    flag = "case " + " ".join(f"when st = '{k}' then '{f}'" for k, f in BIS_FLAGS.items()) + " end"
    con.execute(f"""create table o as
        select k, place, t as period, v, {flag} as flag from b where rule in ('month', 'year')
        union all select k, place, left(t, 4), v, {flag} from b where rule = 'q4' and t like '%-Q4'
        union all select k, place, left(t, 4), avg(v), case when count(st) filter (where st <> 'A') > 0 then 'other' end from b where rule = 'mean4' group by k, place, left(t, 4) having count(distinct t) = 4""")
    if any(p[6] == "mean4" for p in picks):
        notes["years with fewer than four quarters (not made into a year)"] = one("select count(*) from (select 1 from b where rule = 'mean4' group by k, place, left(t, 4) having count(distinct t) < 4)")
    lowest = dict(con.execute("select k, min(v) from o group by 1").fetchall())
    series = []
    for s, _, text, unit, kind, transform, rule in picks:
        if transform == "log" and lowest.get(s, 1) <= 0:  # a log needs every value above zero, as table.wdi_shape asks
            transform = "log1p" if lowest[s] == 0 else "none"
        series.append(series_row(f"{source}:{s}", source, "finance" if source != "bis_long_cpi" else "prices", text, unit, kind, transform, "country", "month" if rule == "month" else "year", lic))
    t = con.sql(f"select '{source}:' || k as series_id, place as place_id, period, v as value, flag from o order by 1, 2, 3").to_arrow_table()
    names = dict(con.execute("select place, any_value(name) from b group by 1 order by 1").fetchall())
    return Part(series, t.cast(OBS_SCHEMA), names, notes)


def hfd_place(code, iso3):
    """The table's place id for an HFD country code: a plain three-letter code through Natural Earth's ISO3 codes, the whole-country codes in HFD_NATIONAL likewise; parts of countries give None."""
    return iso3.get(HFD_NATIONAL.get(code, code))


def hfd_stff(crude_csv, adjusted_csv, countries, lic):
    """Births and the total fertility rate by country and month, from the HFD's Short-Term Fertility Fluctuations: crude (stff.csv) and seasonally and calendar adjusted (stffadj.csv, from 2012). A '.' is no value. Births whose month is unknown and the year's totals are not used and are counted; codes for parts of a country (England and Wales, Scotland, Northern Ireland, Quebec) are set aside."""
    iso3 = {i: c for c, d in countries.items() for i in d["iso"]}
    con = duckdb.connect(config={"threads": 1, "memory_limit": "1GB"})
    plan = (("births", crude_csv, "", "Live births in the month, as counted (crude)", "births", "level", "log1p"),
            ("tfr", crude_csv, "TFR", "Total fertility rate of the month (crude), the database's estimate", "births per woman", "rate", "none"),
            ("births_adjusted", adjusted_csv, "", "Live births in the month, seasonally and calendar adjusted by the database", "births", "level", "log"),
            ("tfr_adjusted", adjusted_csv, "TFR", "Total fertility rate of the month, seasonally and calendar adjusted by the database", "births per woman", "rate", "none"))
    rows, notes, names = [], {}, {}
    for key, path, prefix, *_ in plan:
        con.execute(f"create or replace view h as select * from read_csv('{path}', header=true, all_varchar=true)")
        cols = ", ".join(f'"{prefix}{m}"' for m in MONTHS)
        got = con.execute(f"""select CountryCode, Year, month, try_cast(val as double) from (unpivot (select CountryCode, Year, {cols} from h) on {cols} into name month value val)
            where val <> '.' and try_cast(val as double) is not null""").fetchall()
        for code, year, month, value in got:
            place = hfd_place(code, iso3)
            if place is None:
                notes.setdefault("country codes with no whole-country match (set aside; values)", {}).setdefault(code, 0)
                notes["country codes with no whole-country match (set aside; values)"][code] += 1
                continue
            names[place] = countries[place]["name"]
            rows.append((f"hfd_stff:{key}", place, f"{int(year)}-{MONTHS.index(month[len(prefix):]) + 1:02d}", value))
        if key == "births":
            notes["rows with births of unknown month (not used)"] = con.execute("select count(*) from h where UNK not in ('.', '0')").fetchall()[0][0]
    series = [series_row(f"hfd_stff:{k}", "hfd_stff", "people", text, unit, kind, transform, "country", "month", lic) for k, _, _, text, unit, kind, transform in plan]
    rows.sort()
    t = pa.table({"series_id": [r[0] for r in rows], "place_id": [r[1] for r in rows], "period": [r[2] for r in rows], "value": [r[3] for r in rows], "flag": [None] * len(rows)}, schema=OBS_SCHEMA)
    return Part(series, t, names, notes)


def eurostat_flag(f):
    """A Eurostat flag in the table's words: estimated if it holds e, other for any other flag, empty for none (a flag holding f, forecast, is set aside before this)."""
    return None if not f else "estimated" if "e" in f else "other"


def eurostat_deaths(csv, iso2, lic):
    """Deaths by country and month from Eurostat's demo_mmonth (SDMX-CSV). The year's total and deaths of unknown month are not used and are counted; rows with no value or a forecast flag are set aside; groups of countries and the codes in EUROSTAT_SKIP are set aside."""
    con = duckdb.connect(config={"threads": 1, "memory_limit": "1GB"})
    con.execute(f"create view e as select geo, TIME_PERIOD as y, month, try_cast(OBS_VALUE as double) as v, OBS_FLAG as f from read_csv('{csv}', header=true, all_varchar=true)")
    one = lambda q: con.execute(q).fetchall()[0][0]
    notes = {"rows in the file": one("select count(*) from e"), "rows of the year's total or an unknown month (not used)": one("select count(*) from e where month in ('TOTAL', 'UNK')")}
    con.execute("create table m as select * from e where regexp_matches(month, '^M(0[1-9]|1[0-2])$')")
    notes["rows with no value (set aside)"] = one("select count(*) from m where v is null")
    notes["rows flagged as a forecast (set aside)"] = one("select count(*) from m where v is not null and contains(coalesce(f, ''), 'f')")
    got = con.execute("select geo, y, month, v, f from m where v is not null and not contains(coalesce(f, ''), 'f') order by all").fetchall()
    rows, unmatched, skipped = [], {}, {}
    for geo, y, month, v, f in got:
        if geo in EUROSTAT_SKIP:
            skipped[geo] = skipped.get(geo, 0) + 1
            continue
        place = iso2.get(EUROSTAT_GEO.get(geo, geo))
        if place is None:
            unmatched[geo] = unmatched.get(geo, 0) + 1
            continue
        rows.append(("eurostat_deaths:deaths", place, f"{y}-{month[1:]}", v, eurostat_flag(f)))
    notes["codes set aside by choice (rows)"] = skipped
    notes["codes with no Natural Earth match: groups of countries and others (set aside; rows)"] = unmatched
    rows.sort()
    t = pa.table({k: [r[i] for r in rows] for i, k in enumerate(OBS_SCHEMA.names)}, schema=OBS_SCHEMA)
    series = [series_row("eurostat_deaths:deaths", "eurostat_deaths", "people", "Deaths in the month (all ages, both sexes), Eurostat demo_mmonth", "deaths", "level", "log1p", "country", "month", lic)]
    return Part(series, t, {}, notes)
