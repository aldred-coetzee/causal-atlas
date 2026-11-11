"""The adapters for earthquakes, protests and dengue on tiny made-up files written here, never the real data."""
from shapely.geometry import box

from causal_atlas import adapters_events as ev

COUNTRIES = {"001": {"name": "Alpha", "iso": {"AAA", "CAN"}, "shape": box(0, 0, 10, 10)}, "002": {"name": "Beta", "iso": {"BBB", "MEX"}, "shape": box(20, 0, 30, 10)}}


def table_of(part):
    return {(r["series_id"], r["place_id"], r["period"]): (r["value"], r["flag"]) for r in part.obs.to_pylist()}


def values(part, series_id, place):
    return {k[2]: v[0] for k, v in table_of(part).items() if k[0] == series_id and k[1] == place}


QUAKE_HEADER = "time,latitude,longitude,depth,mag,magType,id,type"


def quake_files(tmp_path):
    one = [("2000-03-05T01:02:03.000Z", 5, 5, 10, 5.5, "mb", "a1", "earthquake"),
           ("2000-03-09T01:02:03.000Z", 5, 5, 10, 4.8, "mb", "a2", "earthquake"),  # below the floor
           ("2000-05-01T00:00:00.000Z", 5, 15, 10, 6.0, "mww", "a3", "earthquake"),  # between the two shapes: at sea
           ("1999-12-31T23:59:59.000Z", 5, 5, 10, 7.0, "mww", "a0", "earthquake"),  # before the span
           ("2000-06-01T00:00:00.000Z", 5, 5, 0, 5.2, "ml", "x1", "quarry blast")]  # not an earthquake
    two = [("2000-12-31T23:00:00.000Z", 5, 25, 10, 5.0, "mwc", "b1", "earthquake"),
           ("2000-03-05T01:02:03.000Z", 5, 5, 10, 5.5, "mb", "a1", "earthquake")]  # the same event in a second file
    paths = []
    for name, rows in (("q1.csv", one), ("q2.csv", two)):
        (tmp_path / name).write_text(QUAKE_HEADER + "\n" + "\n".join(",".join(map(str, r)) for r in rows) + "\n", encoding="utf-8")
        paths.append(tmp_path / name)
    return paths


def test_quakes_count_every_watched_month_with_zeros_and_set_sea_aside_from_countries(tmp_path):
    part = ev.usgs_quakes(quake_files(tmp_path), COUNTRIES, "public domain", floor=5.0, first=2000, last=2000)
    alpha = values(part, "usgs_quakes:events:country_total", "001")
    assert len(alpha) == 12 and alpha["2000-03"] == 1 and sum(alpha.values()) == 1
    beta = values(part, "usgs_quakes:events:country_total", "002")
    assert len(beta) == 12 and beta["2000-12"] == 1 and sum(beta.values()) == 1
    world = values(part, "usgs_quakes:events:world", "world")
    assert len(world) == 12 and {k: v for k, v in world.items() if v} == {"2000-03": 1, "2000-05": 1, "2000-12": 1}
    moment = values(part, "usgs_quakes:moment:country_total", "001")
    assert abs(moment["2000-03"] / 10 ** (1.5 * 5.5 + 9.1) - 1) < 1e-9 and moment["2000-04"] == 0
    assert part.notes["epicentres in no country's shape, at sea or off the map (world series only)"] == 1
    assert part.notes["earthquakes in the files"] == 5  # the quarry blast is not one; the repeated event counts once
    assert {s["licence"] for s in part.series} == {"public domain"} and {s["period"] for s in part.series} == {"month"}
    assert part.names == {"world": "World"}


MM_HEADER = "id,country,ccode,year,protest,startmonth,startyear,protesterviolence," + ",".join(f"stateresponse{i}" for i in range(1, 8))


def mm_file(path):
    rows = [("20", 1990, 1, 3, 1, ["arrests", "killings"]), ("20", 1990, 1, 3, 0, ["accomodation"]),
            ("20", 1991, 0, "", "", []),  # searched, no protest found: the year is watched and every month is zero
            ("70", 2020, 1, 2, 0, ["beatings"]),  # the file ends in March 2020
            ("260", 1990, 1, 5, 0, []), ("999", 1990, 1, 5, 0, [])]  # a state that ended; a code with no match
    lines = [f'{i},"x",{c},{y},{p},{m},{y if p else ""},{v},' + ",".join((r + [""] * 7)[:7]) for i, (c, y, p, m, v, r) in enumerate(rows)]
    path.write_text(MM_HEADER + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def test_protests_write_zero_in_searched_years_only_and_set_aside_ended_states(tmp_path):
    mm_file(tmp_path / "m.csv")
    part = ev.mass_mobilization(tmp_path / "m.csv", COUNTRIES, "CC0 1.0")
    alpha = values(part, "mass_mobilization:protests:country_total", "001")
    assert len(alpha) == 24 and alpha["1990-03"] == 2 and sum(alpha.values()) == 2 and alpha["1991-07"] == 0
    assert values(part, "mass_mobilization:protests_violent:country_total", "001")["1990-03"] == 1
    assert values(part, "mass_mobilization:protests_met_with_force:country_total", "001")["1990-03"] == 1
    beta = values(part, "mass_mobilization:protests:country_total", "002")
    assert beta == {"2020-01": 0, "2020-02": 1, "2020-03": 0}
    assert values(part, "mass_mobilization:protests_met_with_force:country_total", "002")["2020-02"] == 1
    assert part.notes["country codes of states that ended or split (set aside; protests)"] == {"West Germany": 1}
    assert part.notes["country codes with no Natural Earth match (set aside; protests)"] == {"999": 1}
    assert part.notes["protests counted"] == 3


DENGUE_HEADER = "adm_0_name,ISO_A0,calendar_start_date,calendar_end_date,Year,dengue_total,T_res,UUID"


def dengue_file(path):
    rows = [("AAA", f"2010-{m:02d}-01", f"2010-{m:02d}-{[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]}", m, "Month", "SRC-1" if m != 6 else "SRC-1 (Imputed)") for m in range(1, 13)]
    rows += [("AAA", "2011-01-01", "2011-01-31", 0, "Month", "SRC-1"),  # a zero the source wrote
             ("AAA", "2009-01-01", "2009-12-31", 5, "Year", "SRC-2"),
             ("AAA", "2012-02-01", "2012-02-29", 99, "Month", "SRC-1")]
    rows += [("AAA", s, e, 1, "Week", "SRC-3") for s, e in (("2012-01-29", "2012-02-04"), ("2012-02-05", "2012-02-11"), ("2012-02-12", "2012-02-18"), ("2012-02-19", "2012-02-25"), ("2012-02-26", "2012-03-03"))]
    rows += [("BBB", s, e, v, "Week", "SRC-4") for s, e, v in (("2015-02-01", "2015-02-07", 1), ("2015-02-08", "2015-02-14", 2), ("2015-02-15", "2015-02-21", 3), ("2015-02-22", "2015-02-28", 4))]
    rows += [("BBB", s, e, 1, "Week", "SRC-4") for s, e in (("2015-03-01", "2015-03-07"), ("2015-03-08", "2015-03-14"), ("2015-03-15", "2015-03-21"))]  # a week missing
    rows += [("BBB", "2016-01-01", "2016-01-14", 3, "Week", "SRC-4"),  # not a whole week, month or year
             ("ZZZ", "2010-01-01", "2010-01-31", 7, "Month", "SRC-5")]
    path.write_text(DENGUE_HEADER + "\n" + "\n".join(f'"x",{i},{s},{e},{s[:4]},{v},{t},"{u}"' for i, s, e, v, t, u in rows) + "\n", encoding="utf-8")


def test_dengue_months_from_rows_or_whole_weeks_and_years_from_rows_or_twelve_months(tmp_path):
    dengue_file(tmp_path / "d.csv")
    part = ev.opendengue(tmp_path / "d.csv", COUNTRIES, "CC BY 4.0")
    got = table_of(part)
    month, year = "opendengue:cases:country_total", "opendengue:cases:country_total:year"
    assert got[(month, "001", "2010-06")] == (6.0, "imputed") and got[(month, "001", "2010-05")] == (5.0, "")
    assert got[(month, "001", "2011-01")] == (0.0, "")
    assert got[(month, "001", "2012-02")] == (99.0, "")  # the month row, not its weeks
    assert got[(month, "002", "2015-02")] == (10.0, "")  # four whole weeks, each in the month of its middle day
    assert (month, "002", "2015-03") not in got and (month, "001", "2011-02") not in got
    assert got[(year, "001", "2010")] == (78.0, "imputed") and got[(year, "001", "2009")] == (5.0, "")
    assert (year, "001", "2011") not in got and (year, "001", "2012") not in got
    assert {k[1] for k in got} == {"001", "002"}
    assert part.notes["countries with no Natural Earth match (set aside; rows)"] == {"ZZZ": 1}
    assert part.notes["months with some of their weeks missing (not written)"] == 1
    assert part.notes["months with both a month row and whole weeks (the month row kept)"] == 1
    assert part.notes["rows whose span is not a whole calendar month, a seven-day week or a calendar year (set aside)"] == 1
    assert {s["period"] for s in part.series} == {"month", "year"}


def test_months_and_weekday_counts():
    assert ev.months("2019-11", "2020-02") == ["2019-11", "2019-12", "2020-01", "2020-02"]
    assert ev.wednesdays(2012, 2, 2) == 5 and ev.wednesdays(2015, 2, 2) == 4
