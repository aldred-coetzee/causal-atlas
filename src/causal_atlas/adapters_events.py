"""Three sources of events and disease in the shape of table.py, one adapter a source: earthquakes (USGS ComCat), protests against governments (Mass Mobilization) and dengue cases (OpenDengue), by country and month, and dengue also by year. Each returns a table.Part; the licence line is passed in, not read from the manifest. Zero is written where the source watched a country-month and recorded nothing; nothing is written where it did not watch. Nothing here sets one series beside another."""
import calendar
from datetime import date, timedelta

import duckdb
import pyarrow as pa

from causal_atlas.table import OBS_SCHEMA, Part, assign, obs_table, series_row

QUAKE_FLOOR = 5.0  # magnitude: the floor at which the catalogue's yearly count holds steady from 1973 (docs/reading/sources-events.md)
QUAKE_FIRST, QUAKE_LAST = 1973, 2025  # the NEIC PDE's first year in ComCat to the last whole year
MM_LAST = "2020-03"  # the release's stated end, 2020-03-31
DEADLY = ("beatings", "shootings", "killings")  # the manual's "deadly or potentially deadly force"

# Mass Mobilization's Polity country codes to ISO 3166 alpha-3, matched to Natural Earth's codes as table.prices does. Codes of states that ended or split while the
# file runs (West and East Germany 1990, Czechoslovakia 1990-92, Yugoslavia 1990-92 and 1992-2006 with Serbia and Montenegro, the USSR 1990-91) have no one place now:
# they are set aside and counted. Two codes a country (Ethiopia 529 and 530, Yemen 678 and 679) cover different years and go to one place.
POLITY_ISO3 = {
    "20": "CAN", "40": "CUB", "41": "HTI", "42": "DOM", "51": "JAM", "70": "MEX", "90": "GTM", "91": "HND", "92": "SLV", "93": "NIC", "94": "CRI", "95": "PAN",
    "100": "COL", "101": "VEN", "110": "GUY", "115": "SUR", "130": "ECU", "135": "PER", "140": "BRA", "145": "BOL", "150": "PRY", "155": "CHL", "160": "ARG", "165": "URY",
    "200": "GBR", "205": "IRL", "210": "NLD", "211": "BEL", "212": "LUX", "220": "FRA", "225": "CHE", "230": "ESP", "235": "PRT", "255": "DEU", "290": "POL", "305": "AUT",
    "310": "HUN", "316": "CZE", "317": "SVK", "325": "ITA", "339": "ALB", "341": "KOS", "342": "SRB", "343": "MKD", "344": "HRV", "346": "BIH", "348": "MNE", "349": "SVN",
    "350": "GRC", "352": "CYP", "355": "BGR", "359": "MDA", "360": "ROU", "365": "RUS", "366": "EST", "367": "LVA", "368": "LTU", "369": "UKR", "370": "BLR", "371": "ARM",
    "372": "GEO", "373": "AZE", "375": "FIN", "380": "SWE", "385": "NOR", "390": "DNK",
    "402": "CPV", "404": "GNB", "411": "GNQ", "420": "GMB", "432": "MLI", "433": "SEN", "434": "BEN", "435": "MRT", "436": "NER", "437": "CIV", "438": "GIN", "439": "BFA",
    "450": "LBR", "451": "SLE", "452": "GHA", "461": "TGO", "471": "CMR", "475": "NGA", "481": "GAB", "482": "CAF", "483": "TCD", "484": "COG", "490": "COD", "500": "UGA",
    "501": "KEN", "510": "TZA", "516": "BDI", "517": "RWA", "520": "SOM", "522": "DJI", "525": "SSD", "529": "ETH", "530": "ETH", "531": "ERI", "540": "AGO", "541": "MOZ",
    "551": "ZMB", "552": "ZWE", "553": "MWI", "560": "ZAF", "565": "NAM", "570": "LSO", "571": "BWA", "572": "SWZ", "580": "MDG", "581": "COM", "590": "MUS",
    "600": "MAR", "615": "DZA", "616": "TUN", "620": "LBY", "625": "SDN", "630": "IRN", "640": "TUR", "645": "IRQ", "651": "EGY", "652": "SYR", "660": "LBN", "663": "JOR",
    "670": "SAU", "678": "YEM", "679": "YEM", "690": "KWT", "692": "BHR", "694": "QAT", "696": "ARE", "698": "OMN",
    "700": "AFG", "701": "TKM", "702": "TJK", "703": "KGZ", "704": "UZB", "705": "KAZ", "710": "CHN", "712": "MNG", "713": "TWN", "731": "PRK", "732": "KOR", "740": "JPN",
    "750": "IND", "760": "BTN", "770": "PAK", "771": "BGD", "775": "MMR", "780": "LKA", "790": "NPL", "800": "THA", "811": "KHM", "812": "LAO", "816": "VNM", "820": "MYS",
    "830": "SGP", "840": "PHL", "850": "IDN", "860": "TLS", "910": "PNG"}
POLITY_ENDED = {"260": "West Germany", "265": "East Germany", "315": "Czechoslovakia", "345": "Yugoslavia", "347": "Yugoslavia, then Serbia and Montenegro", "364": "USSR"}


def months(first, last):
    """`YYYY-MM` from first to last inclusive, both `YYYY-MM`."""
    y, m = int(first[:4]), int(first[5:])
    out = []
    while f"{y}-{m:02d}" <= last:
        out.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def iso_to_m49(countries):
    """Natural Earth's ISO alpha-3 codes (all three it gives a country) to its M49 code."""
    return {i: c for c, d in countries.items() for i in d["iso"]}


def usgs_quakes(csvs, countries, lic, floor=QUAKE_FLOOR, first=QUAKE_FIRST, last=QUAKE_LAST):
    """Earthquakes of magnitude `floor` and above by month, from ComCat CSVs: the count and the summed seismic moment by country (the country whose shape holds the epicentre), and the count for the world, at sea included. The catalogue watches the whole earth, so every country and month in the span is written, zero where nothing was recorded; epicentres in no country's shape are counted and set aside from the country series."""
    con = duckdb.connect()
    con.execute("set threads=1")
    files = ", ".join(f"'{p}'" for p in sorted(map(str, csvs)))
    con.execute(f"""create table q as select distinct id, left(time, 7) as mo, try_cast(latitude as double) as lat, try_cast(longitude as double) as lon, try_cast(mag as double) as mag
        from read_csv([{files}], header=true, all_varchar=true) where type = 'earthquake'""")
    one = lambda s: con.execute(s).fetchall()[0][0]
    notes = {"earthquakes in the files": one("select count(*) from q")}
    con.execute(f"create table k as select * from q where mag >= {floor} and mo between '{first}-01' and '{last}-12' and lat is not null and lon is not null")
    notes[f"earthquakes of magnitude {floor} or more, {first} to {last}"] = one("select count(*) from k")
    pts = con.execute("select distinct lat, lon from k order by lat, lon").fetchnumpy()
    con.register("pts", pa.table({"lat": pts["lat"], "lon": pts["lon"], "code": assign(pts["lat"], pts["lon"], countries)}))
    con.execute("create table a as select k.*, p.code from k join pts p using (lat, lon)")
    notes["epicentres inside a country's shape"] = one("select count(*) from a where code <> ''")
    notes["epicentres in no country's shape, at sea or off the map (world series only)"] = one("select count(*) from a where code = ''")
    span = months(f"{first}-01", f"{last}-12")
    con.register("grid", pa.table({"code": [c for c in sorted(countries) for _ in span], "mo": span * len(countries)}))
    rows = con.execute("""select g.code, g.mo, count(a.id), coalesce(sum(power(10, 1.5 * a.mag + 9.1)), 0) from grid g left join a on a.code = g.code and a.mo = g.mo
        group by 1, 2 order by 1, 2""").fetchall()
    world = con.execute("""select g.mo, count(a.id) from (select distinct mo from grid) g left join a using (mo) group by 1 order by 1""").fetchall()
    where = "by country (the country whose shape holds the epicentre)"
    series = [series_row("usgs_quakes:events:country_total", "usgs_quakes", "disasters", f"Earthquakes of magnitude {floor} or more, by month of origin (UTC), {where}", "events", "count", "log1p", "country", "month", lic),
              series_row("usgs_quakes:moment:country_total", "usgs_quakes", "disasters", f"Summed seismic moment of those earthquakes, from each one's catalogue magnitude as 10^(1.5 M + 9.1), {where}", "N m", "level", "log1p", "country", "month", lic),
              series_row("usgs_quakes:events:world", "usgs_quakes", "disasters", f"Earthquakes of magnitude {floor} or more anywhere, at sea included, by month of origin (UTC)", "events", "count", "log1p", "world", "month", lic)]
    obs = pa.concat_tables([obs_table("usgs_quakes:events:country_total", [r[0] for r in rows], [r[1] for r in rows], [r[2] for r in rows]),
                            obs_table("usgs_quakes:moment:country_total", [r[0] for r in rows], [r[1] for r in rows], [r[3] for r in rows]),
                            obs_table("usgs_quakes:events:world", ["world"] * len(world), [r[0] for r in world], [r[1] for r in world])])
    return Part(series, obs.cast(OBS_SCHEMA), {"world": "World"}, notes)


def mass_mobilization(csv, countries, lic, last=MM_LAST):
    """Protests against governments by country and month of their start (Mass Mobilization): all protests, those where protesters used violence, and those the state met with beatings, shootings or killings. The file holds a row for every country-year it searched, a row with protest = 0 where it found none, so every month of a country-year in the file (to `last`) is written, zero where no protest started; countries and years not in the file are not written."""
    con = duckdb.connect()
    con.execute("set threads=1")
    resp = " or ".join(f"stateresponse{i} in ({', '.join(repr(d) for d in DEADLY)})" for i in range(1, 8))
    con.execute(f"""create table m as select ccode, try_cast(year as int) as y, protest = '1' as p, try_cast(startyear as int) as sy, try_cast(startmonth as int) as sm,
        coalesce(protesterviolence = '1', false) as viol, coalesce({resp}, false) as deadly from read_csv('{csv}', header=true, all_varchar=true)""")
    one = lambda s: con.execute(s).fetchall()[0][0]
    to_m49 = iso_to_m49(countries)
    codes = [r[0] for r in con.execute("select distinct ccode from m order by 1").fetchall()]
    place = {c: to_m49.get(POLITY_ISO3.get(c)) for c in codes}
    notes = {"rows in the file": one("select count(*) from m"), "protests in the file": one("select count(*) from m where p"),
             "country codes of states that ended or split (set aside; protests)": {POLITY_ENDED.get(c, c): one(f"select count(*) from m where p and ccode = '{c}'") for c in codes if c in POLITY_ENDED},
             "country codes with no Natural Earth match (set aside; protests)": {c: one(f"select count(*) from m where p and ccode = '{c}'") for c in codes if c not in POLITY_ENDED and place[c] is None}}
    con.register("pl", pa.table({"ccode": list(place), "code": [place[c] or "" for c in place]}))
    con.execute("create table w as select distinct code, y from m join pl using (ccode) where code <> ''")
    watched = [(c, mo) for c, y in con.execute("select code, y from w order by 1, 2").fetchall() for mo in months(f"{y}-01", min(f"{y}-12", last))]
    con.register("grid", pa.table({"code": [w[0] for w in watched], "mo": [w[1] for w in watched]}))
    con.execute("create table e as select code, sy || '-' || lpad(cast(sm as varchar), 2, '0') as mo, viol, deadly from m join pl using (ccode) where p and code <> ''")
    notes["protests with no start month (set aside)"] = one("select count(*) from e where mo is null")
    notes["protests starting outside a watched country-month (set aside)"] = one("select count(*) from e left join grid g using (code, mo) where e.mo is not null and g.code is null")
    notes["protests counted"] = one("select count(*) from e join grid using (code, mo)")
    rows = con.execute("""select g.code, g.mo, count(e.mo), count(e.mo) filter (where e.viol), count(e.mo) filter (where e.deadly)
        from grid g left join e using (code, mo) group by 1, 2 order by 1, 2""").fetchall()
    text = {"protests": "Protests against the government of 50 or more people, by month of their start",
            "protests_violent": "Those protests where the protesters used violence against the state",
            "protests_met_with_force": "Those protests the state met with beatings, shootings or killings"}
    series = [series_row(f"mass_mobilization:{k}:country_total", "mass_mobilization", "unrest", v + ", by country (the country the file names)", "protests", "count", "log1p", "country", "month", lic) for k, v in text.items()]
    obs = pa.concat_tables([obs_table(f"mass_mobilization:{k}:country_total", [r[0] for r in rows], [r[1] for r in rows], [r[i] for r in rows]) for i, k in enumerate(text, start=2)])
    return Part(series, obs.cast(OBS_SCHEMA), {}, notes)


def wednesdays(y, m, weekday):
    """How many days of a month fall on `weekday` (Monday 0): the number of whole weeks whose middle day is that weekday that a month holds."""
    return sum(1 for d in range(1, calendar.monthrange(y, m)[1] + 1) if date(y, m, d).weekday() == weekday)


def opendengue(csv, countries, lic):
    """Dengue cases by country and month, and by year, from OpenDengue's national extract (one row a country and span, at week, month or year). A month is written from the source's month row, or else from its weeks, each week going to the month that holds its middle day, and only when every week of that month is present; a year is written from the source's year row, or else as the sum of twelve written months. A record of 0 is a zero the source wrote; a month or year with no record is not written. The flag is `imputed` where the source marks a record imputed or zero-filled, else empty."""
    con = duckdb.connect()
    con.execute("set threads=1")
    con.execute(f"""create table d as select ISO_A0 as iso, T_res as t, cast(calendar_start_date as date) as s, cast(calendar_end_date as date) as e, try_cast(dengue_total as double) as v,
        (UUID ilike '%(imputed)%' or UUID ilike '%(zero filling)%') as imp from read_csv('{csv}', header=true, all_varchar=true)""")
    one = lambda s: con.execute(s).fetchall()[0][0]
    to_m49 = iso_to_m49(countries)
    isos = [r[0] for r in con.execute("select distinct iso from d order by 1").fetchall()]
    con.register("pl", pa.table({"iso": isos, "code": [to_m49.get(i, "") for i in isos]}))
    notes = {"rows in the file": one("select count(*) from d"), "rows by step": dict(con.execute("select t, count(*) from d group by 1 order by 1").fetchall()),
             "countries with no Natural Earth match (set aside; rows)": dict(con.execute("select iso, count(*) from d join pl using (iso) where code = '' group by 1 order by 1").fetchall()),
             "rows with no value (set aside)": one("select count(*) from d where v is null")}
    con.execute("create table r as select code, t, s, e, v, imp from d join pl using (iso) where code <> '' and v is not null")
    ok_month = "t = 'Month' and day(s) = 1 and e = last_day(s)"
    ok_week = "t = 'Week' and e - s = 6"
    ok_year = "t = 'Year' and month(s) = 1 and day(s) = 1 and month(e) = 12 and day(e) = 31 and year(s) = year(e)"
    notes["rows whose span is not a whole calendar month, a seven-day week or a calendar year (set aside)"] = one(f"select count(*) from r where not (({ok_month}) or ({ok_week}) or ({ok_year}))")
    con.execute(f"create table wk as select code, strftime(s + 3, '%Y-%m') as mo, isodow(s + 3) - 1 as wd, v, imp from r where {ok_week}")
    weeks = con.execute("select code, mo, wd, count(*), sum(v), bool_or(imp) from wk group by 1, 2, 3 order by 1, 2, 3").fetchall()
    whole = {(c, mo): (v, imp) for c, mo, wd, n, v, imp in weeks if n == wednesdays(int(mo[:4]), int(mo[5:]), wd)}
    notes["months with some of their weeks missing (not written)"] = len({(c, mo) for c, mo, *_ in weeks} - set(whole))
    own = {(c, mo): (v, imp) for c, mo, v, imp in con.execute(f"select code, strftime(s, '%Y-%m'), v, imp from r where {ok_month}").fetchall()}
    notes["months with both a month row and whole weeks (the month row kept)"] = len(set(own) & set(whole))
    month = {**whole, **own}
    years = {}
    for (c, mo), (v, imp) in month.items():
        years.setdefault((c, mo[:4]), []).append((v, imp))
    summed = {k: (sum(x[0] for x in vs), any(x[1] for x in vs)) for k, vs in years.items() if len(vs) == 12}
    own_y = {(c, str(y)): (v, imp) for c, y, v, imp in con.execute(f"select code, year(s), v, imp from r where {ok_year}").fetchall()}
    notes["years with both a year row and twelve written months (the year row kept)"] = len(set(own_y) & set(summed))
    notes["years from a year row"], notes["years summed from twelve months"] = len(own_y), len(set(summed) - set(own_y))
    year = {**summed, **own_y}
    flag = lambda imp: "imputed" if imp else ""
    text = "Dengue cases as reported (the case definition differs by source: suspected, confirmed or both), by country"
    series = [series_row("opendengue:cases:country_total", "opendengue", "health", text + ", by month (from the month's row, or from all its weeks, a week counted in the month holding its middle day)", "cases", "count", "log1p", "country", "month", lic),
              series_row("opendengue:cases:country_total:year", "opendengue", "health", text + ", by calendar year (from the year's row, or the sum of its twelve months)", "cases", "count", "log1p", "country", "year", lic)]
    obs = pa.concat_tables([obs_table(sid, [k[0] for k in ks], [k[1] for k in ks], [src[k][0] for k in ks], [flag(src[k][1]) for k in ks])
                            for sid, src in (("opendengue:cases:country_total", month), ("opendengue:cases:country_total:year", year)) for ks in [sorted(src)]])
    return Part(series, obs.cast(OBS_SCHEMA), {}, notes)
