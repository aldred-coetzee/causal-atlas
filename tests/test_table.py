"""The table adapters on tiny made-up files written here, never the real data."""
import duckdb
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from shapely.geometry import box

from causal_atlas import table

AREAS = {"A": {"name": "Alpha", "iso": {"AAA"}, "shape": box(0, 0, 10, 10)}, "B": {"name": "Beta", "iso": {"BBB"}, "shape": box(20, 0, 30, 10)}}
COUNTRIES = {"001": AREAS["A"], "002": AREAS["B"]}
FAO_HEADER = '"Area Code","Area Code (M49)","Area","Item Code","Item","Element Code","Element","Year Code","Year","Unit","Value","Flag","Note"'


def fao_file(path):
    rows = [  # area, m49, item code, item, element code, year, value, flag
        (2, "'004", "Wheatland", 15, "Wheat", 5412, 1961, "2000", "A"), (2, "'004", "Wheatland", 15, "Wheat", 5412, 1962, "2100", "E"),
        (2, "'004", "Wheatland", 15, "Wheat", 5312, 1961, "100", "A"), (2, "'004", "Wheatland", 15, "Wheat", 5510, 1961, "200", "X"),
        (2, "'004", "Wheatland", 15, "Wheat", 5510, 1962, "", "M"),
        (41, "'156", "Chin\u00e2, mainland", 15, "Wheat", 5412, 1961, "3000", "A"), (351, "'159", "China", 15, "Wheat", 5412, 1961, "3000", "A"),
        (2, "'004", "Wheatland", 882, "Raw milk of cattle", 5510, 1961, "50", "A"),  # no area harvested: not a crop
        (2, "'004", "Wheatland", 2000, "Sum of crops", 5412, 1961, "9", "A"), (5100, "'002", "Africa", 15, "Wheat", 5412, 1961, "9", "A"),
        (2, "'004", "Wheatland", 15, "Wheat", 5312, 1962, "0", "I")]
    path.write_text(FAO_HEADER + "\n" + "\n".join(f'{a},"{m}","{n}",{ic},"{it}",{e},"x",{y},{y},"u",{v},{f},' for a, m, n, ic, it, e, y, v, f in rows) + "\n", encoding="utf-8")


def table_of(part):
    return {(r["series_id"], r["place_id"], r["period"]): (r["value"], r["flag"]) for r in part.obs.to_pylist()}


def test_faostat_gives_crops_by_country_and_year_with_the_flag_and_sets_aside_sums(tmp_path):
    fao_file(tmp_path / "f.csv")
    part = table.faostat(tmp_path / "f.csv")
    got = table_of(part)
    assert got == {("faostat_qcl:yield:15", "004", "1961"): (2000.0, "official"), ("faostat_qcl:yield:15", "004", "1962"): (2100.0, "estimated"),
                   ("faostat_qcl:yield:15", "156", "1961"): (3000.0, "official"), ("faostat_qcl:area_harvested:15", "004", "1961"): (100.0, "official"),
                   ("faostat_qcl:area_harvested:15", "004", "1962"): (0.0, "imputed"), ("faostat_qcl:production:15", "004", "1961"): (200.0, "other")}
    assert {s["series_id"] for s in part.series} == {"faostat_qcl:yield:15", "faostat_qcl:area_harvested:15", "faostat_qcl:production:15"}
    assert part.names == {"004": "Wheatland", "156": "Chin\u00e2, mainland"}
    assert part.notes["rows with no value (all flagged M)"] == 1 and part.notes["rows of the China total (M49 159)"] == 1
    assert {s["transform"] for s in part.series if "yield" in s["series_id"]} == {"log"}


def test_drought_rows_keep_finite_months_on_the_clock_from_the_year_before():
    x = np.array([[0.5, np.nan, -1.0] + [0.0] * 9, [np.nan] * 12])
    t = table.drought_obs(x, ["004", "008"], 1960)
    rows = [(r["place_id"], r["period"], r["value"]) for r in t.to_pylist()]
    assert rows[0] == ("004", "1960-01", 0.5) and rows[1] == ("004", "1960-03", -1.0)
    assert len(rows) == 11 and all(r[0] == "004" for r in rows)


def test_a_psl_file_is_read_whatever_its_years_and_the_marker_is_left_out(tmp_path):
    f = tmp_path / "x.data"
    f.write_text(" 1950 1951\n1950 " + " ".join(["1.5"] * 12) + "\n1951 " + " ".join(["-99.9"] * 6 + ["2.0"] * 6) + "\n  -99.9\nsome footer\n")
    got = table.psl_read(f)
    assert len(got) == 18 and got[(1950, 1)] == 1.5 and (1951, 1) not in got and got[(1951, 12)] == 2.0


def test_indices_are_world_series_by_month(tmp_path, monkeypatch):
    (tmp_path / "oni.data").write_text(" 2000 2000\n2000 " + " ".join(["0.1"] * 12) + "\n  -99.9\n")
    (tmp_path / "c").mkdir()
    (tmp_path / "c" / "a.data").write_text(" 2000 2000\n2000 " + " ".join(str(i) for i in range(12)) + "\n  -99.9\n")
    monkeypatch.setattr(table, "manifest", lambda: {"oni": {"licence": "L1"}, "candidates": {"a.data": {"licence": "L2"}}})
    part = table.indices(tmp_path / "oni.data", tmp_path / "c", [{"file": "a.data", "label": "A &amp; B"}], ["a.data"])
    got = table_of(part)
    assert got[("oni:oni:nino34_3month", "world", "2000-12")] == (0.1, None) and got[("candidates:a.data:monthly", "world", "2000-03")] == (2.0, None)
    assert [s["series_id"] for s in part.series] == ["oni:oni:nino34_3month", "candidates:a.data:monthly"]
    assert "A & B" in part.series[1]["measures"] and part.series[1]["licence"] == "L2"


def test_points_go_to_the_country_that_holds_them_and_outside_points_to_none():
    code = table.assign([5, 5, 5, 50], [5, 25, 15, 5], COUNTRIES)
    assert list(code) == ["001", "002", "", ""]


def test_fire_sums_a_countrys_cells_and_leaves_out_months_with_no_data():
    burned = np.array([[1.0, 2.0, 4.0], [np.nan, np.nan, np.nan], [3.0, 5.0, 7.0]])
    t = table.fire_obs(burned, np.array(["001", "001", ""]), 1993, 1994)
    assert [(r["place_id"], r["period"], r["value"]) for r in t.to_pylist()] == [("001", "1993-01", 3.0), ("001", "1993-03", 8.0)]


def test_ged_counts_events_and_deaths_by_country_and_start_month(tmp_path):
    (tmp_path / "g.csv").write_text("date_start,latitude,longitude,country,best\n2000-01-05 00:00:00,5,5,Alpha,3\n2000-01-20 00:00:00,6,6,Alpha,2\n2000-02-01 00:00:00,5,25,Beta,10\n2000-02-01 00:00:00,50,50,Sea,1\n2000-02-01 00:00:00,,,X,1\n")
    rows, notes = table.ged_counts(tmp_path / "g.csv", COUNTRIES)
    assert rows == [("001", "2000-01", 2, 5.0), ("002", "2000-02", 1, 10.0)]
    assert notes["events outside every shape (set aside)"] == 1 and notes["events with no coordinates (set aside)"] == 1


def test_prices_are_the_median_of_collected_prices_by_country_and_month(tmp_path):
    cols = ",".join(("ISO3", "geo_id", "price_date") + table.STAPLES)
    row = lambda iso, g, d, maize: f"{iso},{g},{d}," + ",".join([maize] + [""] * 5)
    (tmp_path / "p.csv").write_text("\n".join([cols, row("AAA", "m1", "2010-03-01", "1"), row("AAA", "m2", "2010-03-01", "5"), row("AAA", "m3", "2010-03-01", "2"), row("AAA", "m3", "2010-04-01", ""), row("ZZZ", "m9", "2010-03-01", "7")]) + "\n")
    part = table.prices(tmp_path / "p.csv", COUNTRIES)
    assert table_of(part) == {("rtfp:maize:median_market", "001", "2010-03"): (2.0, None)}
    assert part.notes["ISO3 codes with no Natural Earth match (set aside)"] == ["ZZZ"]


def parts(tmp_path, order=(0, 1)):
    """Two saved parts with an overlapping place and a world series."""
    a = table.Part([table.series_row("s:a:1", "s", "crops", "A", "u", "level", "log", "country", "year", "L")], table.obs_table("s:a:1", ["001", "002", "001"], ["2001", "2001", "2000"], [3.0, 4.0, 5.0], ["official", None, None]), {"001": "Alpha", "999": "Gone"}, {})
    b = table.Part([table.series_row("s:b:1", "s", "climate", "B", "u", "index", "none", "world", "month", "L")], table.obs_table("s:b:1", ["world"], ["2000-01"], [1.0]), {"world": "World"}, {})
    for i in order:
        table.write_part("ab"[i], (a, b)[i])


@pytest.fixture
def parts_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(table, "PARTS", tmp_path / "parts")
    return tmp_path


def test_assemble_gives_sorted_tables_with_first_and_last_and_places(parts_dir):
    parts(parts_dir)
    sizes = table.assemble(table.PARTS, parts_dir / "out", COUNTRIES)
    assert sizes == {"series": 2, "place": 3, "obs": 4}
    con = duckdb.connect()
    s = con.execute(f"select series_id, \"first\", \"last\", place_level from '{parts_dir / 'out' / 'series.parquet'}' order by 1").fetchall()
    assert s == [("s:a:1", "2000", "2001", "country"), ("s:b:1", "2000-01", "2000-01", "world")]
    p = con.execute(f"select place_id, level, parent, name from '{parts_dir / 'out' / 'place.parquet'}' order by 1").fetchall()
    assert p == [("001", "country", "world", "Alpha"), ("002", "country", "world", "Beta"), ("world", "world", None, "World")]
    o = con.execute(f"select * from '{parts_dir / 'out' / 'obs.parquet'}'").fetchall()
    assert o == sorted(o, key=lambda r: r[:3]) and o[0] == ("s:a:1", "001", "2000", 5.0, None)


def test_a_second_build_gives_identical_tables(parts_dir):
    parts(parts_dir)
    table.assemble(table.PARTS, parts_dir / "one", COUNTRIES)
    parts(parts_dir, order=(1, 0))
    table.assemble(table.PARTS, parts_dir / "two", COUNTRIES)
    for t in ("series", "place", "obs"):
        assert pq.read_table(parts_dir / "one" / f"{t}.parquet").equals(pq.read_table(parts_dir / "two" / f"{t}.parquet"))


def test_a_repeated_series_place_and_period_stops_the_build(parts_dir):
    parts(parts_dir)
    table.write_part("c", table.Part([], table.obs_table("s:a:1", ["001"], ["2000"], [9.0]), {}, {}))
    with pytest.raises(ValueError):
        table.assemble(table.PARTS, parts_dir / "out", COUNTRIES)


def test_series_ids_are_stable_names_of_source_what_and_detail(tmp_path):
    fao_file(tmp_path / "f.csv")
    ids = sorted(s["series_id"] for s in table.faostat(tmp_path / "f.csv").series)
    assert ids == sorted(ids) and all(i.count(":") == 2 for i in ids)
    assert pa.types.is_floating(table.OBS_SCHEMA.field("value").type)
