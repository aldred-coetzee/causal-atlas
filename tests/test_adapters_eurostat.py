"""The general Eurostat adapter on small made-up files in the SDMX-CSV layout of the dissemination API."""
import pytest

from causal_atlas import adapters_eurostat as ae

LIC = "made-up licence text"
ISO2 = {"AA": "001", "BB": "002", "GR": "003", "DE": "004", "FR": "005", "GB": "006"}
MONTHLY = "DATAFLOW,LAST UPDATE,freq,s_adj,unit,geo,TIME_PERIOD,OBS_VALUE,OBS_FLAG,CONF_STATUS"
LEAD = "ESTAT:MADE_UP(1.0),01/01/26 00:00:00"
SPEC = ae.Cut("made_up", "thing", {"s_adj": "NSA", "unit": "NR"}, "A made-up count", "things", "made-up")


def write(tmp_path, head, rows, name="t.csv"):
    p = tmp_path / name
    p.write_text(head + "\n" + "\n".join(rows) + "\n")
    return str(p)


def obs(part):
    return {(r["series_id"], r["place_id"], r["period"]): (r["value"], r["flag"]) for r in part.obs.to_pylist()}


def test_monthly_cut_flags_and_places(tmp_path):
    rows = [f"{LEAD},M,NSA,NR,AA,2000-01,10,,", f"{LEAD},M,NSA,NR,AA,2000-02,11,e,", f"{LEAD},M,NSA,NR,AA,2000-03,12,u,",
            f"{LEAD},M,NSA,NR,AA,2000-04,,,C", f"{LEAD},M,NSA,NR,AA,2000-05,,,", f"{LEAD},M,NSA,NR,AA,2000-06,13,f,",
            f"{LEAD},M,SA,NR,AA,2000-01,99,,", f"{LEAD},M,NSA,I21,AA,2000-01,99,,",
            f"{LEAD},Q,NSA,NR,AA,2000-Q1,33,,", f"{LEAD},A,NSA,NR,AA,2000,120,,",
            f"{LEAD},M,NSA,NR,EL,2000-01,5,,", f"{LEAD},M,NSA,NR,UK,2000-01,0,,", f"{LEAD},M,NSA,NR,DE,2000-01,6,,",
            f"{LEAD},M,NSA,NR,EU27_2020,2000-01,500,,", f"{LEAD},M,NSA,NR,XK,2000-01,1,,"]
    part = ae.eurostat_months(write(tmp_path, MONTHLY, rows), "made_up", ISO2, LIC, SPEC)
    assert obs(part) == {("made_up:thing", "001", "2000-01"): (10.0, None),
                         ("made_up:thing", "001", "2000-02"): (11.0, "estimated"),
                         ("made_up:thing", "001", "2000-03"): (12.0, "other"),
                         ("made_up:thing", "003", "2000-01"): (5.0, None),
                         ("made_up:thing", "006", "2000-01"): (0.0, None),
                         ("made_up:thing", "004", "2000-01"): (6.0, None)}  # DE is kept when the file holds no DE_TOT
    n = part.notes
    assert n["rows in the file"] == 15
    assert n["rows outside the cut (not used)"] == 2
    assert n["rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)"] == 2
    assert n["rows with no value (set aside)"] == 2
    assert n["of which marked confidential"] == 1
    assert n["rows flagged as a forecast (set aside)"] == 1
    assert n["codes set aside because the file holds the longer or whole record (rows)"] == {}
    assert n["codes with no Natural Earth match: groups of countries and others (set aside; rows)"] == {"EU27_2020": 1, "XK": 1}
    assert n["values equal to zero"] == 1
    s = part.series[0]
    assert (s["series_id"], s["source"], s["domain"], s["unit"]) == ("made_up:thing", "made_up", "made-up", "things")
    assert (s["kind"], s["transform"], s["place_level"], s["period"], s["licence"]) == ("level", "log1p", "country", "month", LIC)  # a zero rules out a plain log; never count
    assert part.names == {}


def test_month_column_layout_and_codes_that_give_way(tmp_path):
    head = "DATAFLOW,LAST UPDATE,freq,unit,month,geo,TIME_PERIOD,OBS_VALUE,OBS_FLAG,CONF_STATUS"
    lead = f"{LEAD},A,NR"
    rows = [f"{lead},M01,AA,2000,10,,", f"{lead},M12,AA,2000,12,p,", f"{lead},TOTAL,AA,2000,120,,", f"{lead},UNK,AA,2000,1,,",
            f"{lead},M01,DE_TOT,1970,7,,", f"{lead},M01,DE,1991,8,,", f"{lead},M01,FR,1995,9,,", f"{lead},M01,FX,1970,4,,"]
    spec = ae.Cut("made_up", "births", {"unit": "NR"}, "Made-up births", "births", "people")
    part = ae.eurostat_months(write(tmp_path, head, rows), "made_up", ISO2, LIC, spec)
    assert obs(part) == {("made_up:births", "001", "2000-01"): (10.0, None), ("made_up:births", "001", "2000-12"): (12.0, "other"),
                         ("made_up:births", "004", "1970-01"): (7.0, None), ("made_up:births", "005", "1995-01"): (9.0, None)}
    assert part.notes["rows of the cut that are not a month: a year's total, an unknown month, a quarter or a year (not used)"] == 2
    assert part.notes["codes set aside because the file holds the longer or whole record (rows)"] == {"DE": 1, "FX": 1}
    assert part.series[0]["transform"] == "log"


def test_transform_by_lowest_value(tmp_path):
    rows = [f"{LEAD},M,NSA,NR,AA,2000-01,-1.5,,", f"{LEAD},M,NSA,NR,AA,2000-02,2,,"]
    part = ae.eurostat_months(write(tmp_path, MONTHLY, rows), "made_up", ISO2, LIC, SPEC)
    assert (part.series[0]["kind"], part.series[0]["transform"]) == ("level", "none")


def test_a_cut_on_a_column_the_file_lacks_is_an_error(tmp_path):
    spec = ae.Cut("made_up", "thing", {"sex": "T"}, "", "", "")
    with pytest.raises(ValueError, match="sex"):
        ae.eurostat_months(write(tmp_path, MONTHLY, [f"{LEAD},M,NSA,NR,AA,2000-01,1,,"]), "made_up", ISO2, LIC, spec)


def test_a_cut_that_leaves_two_rows_a_month_is_an_error(tmp_path):
    rows = [f"{LEAD},M,NSA,NR,AA,2000-01,1,,", f"{LEAD},M,SA,NR,AA,2000-01,2,,"]
    spec = ae.Cut("made_up", "thing", {"unit": "NR"}, "", "", "")
    with pytest.raises(ValueError, match="two rows"):
        ae.eurostat_months(write(tmp_path, MONTHLY, rows), "made_up", ISO2, LIC, spec)


def test_every_table_names_its_cut():
    assert len(ae.TABLES) == 8
    assert len({c.source for c in ae.TABLES.values()}) == 8
    for c in ae.TABLES.values():
        assert c.source.startswith("eurostat_") and c.cut and c.measures and c.unit and c.domain
        assert "SA" not in c.cut.values() and "SCA" not in c.cut.values()  # unadjusted wherever the table offers both
