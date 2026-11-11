"""Monthly Eurostat tables by country in the shape of table.py: one general function for a table in Eurostat's SDMX-CSV layout and a stated cut, returning a table.Part, and the cut of each of eight tables (unemployment, industrial production, retail trade, electricity, nights at tourist accommodation, air passengers, first-time asylum applicants, live births). The licence line is passed in. A month with no row is not written: Eurostat leaves a row out where it has no figure and writes a zero where it counted none, so a missing month is nothing, not a zero, and no series here is of kind `count`. Nothing here sets one series beside another."""
from collections import namedtuple

import duckdb
import pyarrow as pa

from causal_atlas.adapters_money_people import EUROSTAT_GEO, eurostat_flag
from causal_atlas.table import OBS_SCHEMA, Part, series_row

GIVES_WAY = {"DE": "DE_TOT", "FX": "FR"}  # set aside only when the file also holds the code named: DE (Germany from 1991) for DE_TOT (the same territory, from 1960); FX (metropolitan France) for FR (the whole country)

# One table's cut: the source name, the series' slug, {column: the one code kept}, what it measures, its unit and its domain.
Cut = namedtuple("Cut", "source slug cut measures unit domain")
TABLES = {
    "une_rt_m": Cut("eurostat_unemployment", "unemployed", {"s_adj": "NSA", "age": "TOTAL", "unit": "THS_PER", "sex": "T"},
                    "Unemployed persons in the month, the table's total over age, both sexes, not seasonally adjusted (Eurostat une_rt_m)", "thousand persons", "economy"),
    "sts_inpr_m": Cut("eurostat_industry", "production_index", {"indic_bt": "PRD", "nace_r2": "B-D", "s_adj": "NSA", "unit": "I21"},
                      "Production in industry (NACE B to D: mining and quarrying, manufacturing, electricity and gas supply), volume index, unadjusted (Eurostat sts_inpr_m)", "index (2021 = 100)", "economy"),
    "sts_trtu_m": Cut("eurostat_retail", "turnover_index", {"indic_bt": "NETTUR", "nace_r2": "G47", "s_adj": "NSA", "unit": "I21"},
                      "Net turnover of retail trade except motor vehicles (NACE G47), value index, unadjusted (Eurostat sts_trtu_m)", "index (2021 = 100)", "trade"),
    "nrg_cb_em": Cut("eurostat_electricity", "available_internal_market", {"nrg_bal": "AIM", "siec": "E7000", "unit": "GWH"},
                     "Electricity available to the internal market in the month (Eurostat nrg_cb_em)", "GWh", "energy"),
    "tour_occ_nim": Cut("eurostat_tourism", "nights", {"c_resid": "TOTAL", "unit": "NR", "nace_r2": "I551-I553"},
                        "Nights spent at tourist accommodation (hotels, holiday and short-stay accommodation, camping grounds), residents and non-residents (Eurostat tour_occ_nim)", "nights", "travel"),
    "avia_paoc": Cut("eurostat_air", "passengers_on_board", {"freq": "M", "unit": "PAS", "tra_meas": "PAS_BRD", "tra_cov": "TOTAL", "schedule": "TOTAL"},
                     "Air passengers on board at the country's reporting airports, arrivals and departures, all flights (Eurostat avia_paoc)", "passengers", "travel"),
    "migr_asyappctzm": Cut("eurostat_asylum", "first_time_applicants", {"unit": "PER", "citizen": "TOTAL", "sex": "T", "applicant": "FRST", "age": "TOTAL"},
                           "First-time asylum applicants in the month, all citizenships, both sexes, all ages, rounded by Eurostat to the nearest 5 (Eurostat migr_asyappctzm)", "persons", "migration"),
    "demo_fmonth": Cut("eurostat_births", "live_births", {"unit": "NR"},
                       "Live births in the month of occurrence (Eurostat demo_fmonth)", "live births", "people"),
}


def shape(lowest):
    """(kind, transform) for a quantity or an index by its lowest value, as table.wdi_shape treats a quantity: `log` if every value is above zero, `log1p` if none is below zero, else `none`. Always `level`, never `count`: a missing month is not a zero."""
    return "level", "log" if lowest > 0 else "log1p" if lowest == 0 else "none"


def eurostat_months(csv, table, iso2, lic, spec=None):
    """One Eurostat table in SDMX-CSV (from the dissemination API) as a Part, by country and month: the rows of `spec.cut` (default TABLES[table]) only. A month is TIME_PERIOD when it reads YYYY-MM, or TIME_PERIOD and a `month` column (M01 to M12) where the table has one; a year's total, an unknown month, a quarter or a year are not used and are counted. Rows with no value (confidential ones among them) and rows flagged as a forecast are set aside and counted; groups of countries and codes with no Natural Earth two-letter match are set aside and counted, and DE and FX give way as GIVES_WAY says. Flags as eurostat_flag reads them."""
    spec = spec or TABLES[table]
    con = duckdb.connect(config={"threads": 1, "memory_limit": "1GB"})
    con.execute(f"create view e as select * from read_csv('{csv}', header=true, all_varchar=true)")
    cols = [r[0] for r in con.execute("describe e").fetchall()]
    missing = [k for k in spec.cut if k not in cols]
    if missing:
        raise ValueError(f"{table}: the cut names columns the file does not hold: {missing}")
    one = lambda q: con.execute(q).fetchall()[0][0]
    keep = " and ".join(f""""{k}" = '{v}'""" for k, v in spec.cut.items()) or "true"
    month = ("""case when regexp_matches(month, '^M(0[1-9]|1[0-2])$') and regexp_matches(TIME_PERIOD, '^[0-9]{4}$') then TIME_PERIOD || '-' || substr(month, 2) end""" if "month" in cols
             else """case when regexp_matches(TIME_PERIOD, '^[0-9]{4}-(0[1-9]|1[0-2])$') then TIME_PERIOD end""")
    conf = "CONF_STATUS" if "CONF_STATUS" in cols else "null"
    con.execute(f"create table c as select geo, {month} as period, try_cast(OBS_VALUE as double) as v, OBS_FLAG as f, {conf} as conf from e where {keep}")
    notes = {"rows in the file": one("select count(*) from e"), "rows outside the cut (not used)": one(f"select count(*) from e where not ({keep})"),
             "rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)": one("select count(*) from c where period is null")}
    con.execute("delete from c where period is null")
    notes["rows with no value (set aside)"] = one("select count(*) from c where v is null")
    notes["of which marked confidential"] = one("select count(*) from c where v is null and coalesce(conf, '') <> ''")
    notes["rows flagged as a forecast (set aside)"] = one("select count(*) from c where v is not null and contains(coalesce(f, ''), 'f')")
    got = con.execute("select geo, period, v, f from c where v is not null and not contains(coalesce(f, ''), 'f') order by all").fetchall()
    held = {g for g, *_ in got}
    rows, unmatched, skipped = [], {}, {}
    for geo, period, v, f in got:
        if GIVES_WAY.get(geo) in held:
            skipped[geo] = skipped.get(geo, 0) + 1
            continue
        place = iso2.get(EUROSTAT_GEO.get(geo, geo))
        if place is None:
            unmatched[geo] = unmatched.get(geo, 0) + 1
            continue
        rows.append((f"{spec.source}:{spec.slug}", place, period, v, eurostat_flag(f)))
    notes["codes set aside because the file holds the longer or whole record (rows)"] = skipped
    notes["codes with no Natural Earth match: groups of countries and others (set aside; rows)"] = unmatched
    rows.sort()
    if len({r[1:3] for r in rows}) != len(rows):
        raise ValueError(f"{table}: two rows for one place and month; the cut does not settle one series")
    notes["values equal to zero"] = sum(1 for r in rows if r[3] == 0)
    t = pa.table({k: [r[i] for r in rows] for i, k in enumerate(OBS_SCHEMA.names)}, schema=OBS_SCHEMA)
    kind, transform = shape(min((r[3] for r in rows), default=1))
    series = [series_row(f"{spec.source}:{spec.slug}", spec.source, spec.domain, spec.measures, spec.unit, kind, transform, "country", "month", lic)]
    return Part(series, t, {}, notes)
