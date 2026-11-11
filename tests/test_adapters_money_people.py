"""The money and people adapters on small made-up files in each source's own layout."""
import pytest

from causal_atlas import adapters_money_people as amp

LIC = "made-up licence text"
ISO2 = {"AA": "001", "BB": "002", "GR": "003", "DE": "004", "FR": "005", "GB": "006"}
COUNTRIES = {"001": {"name": "Alpha", "iso": {"AAA"}}, "002": {"name": "Beta", "iso": {"BBB"}},
             "004": {"name": "Delta", "iso": {"DEU"}}, "006": {"name": "Zeta", "iso": {"GBR"}}}

BIS_HEAD = "STRUCTURE,STRUCTURE_ID,ACTION,FREQ:Frequency,REF_AREA:Reference area,TIME_PERIOD:Time period or range,OBS_VALUE:Observation Value,UNIT_MEASURE:Unit of measure,VALUE:Value,OBS_STATUS:Observation Status"


def bis_file(tmp_path, rows, head=BIS_HEAD):
    p = tmp_path / "bis.csv"
    p.write_text(head + "\n" + "\n".join(rows) + "\n")
    return str(p)


def obs(part):
    return {(r["series_id"], r["place_id"], r["period"]): (r["value"], r["flag"]) for r in part.obs.to_pylist()}


def test_bis_monthly_rate(tmp_path):
    lead = "dataflow,BIS:WS_CBPOL(1.0): Central bank policy rates,I"
    csv = bis_file(tmp_path, [
        f"{lead},M: Monthly,AA: Alphaland,2000-01,1.5,368: Per cent,,A: Normal value",
        f"{lead},M: Monthly,AA: Alphaland,2000-02,1.75,368: Per cent,,E: Estimated value",
        f"{lead},M: Monthly,AA: Alphaland,2000-03,,368: Per cent,,M: Missing value",
        f"{lead},M: Monthly,BB: Betaland,2000-01,0,368: Per cent,,A: Normal value",
        f"{lead},M: Monthly,XM: Euro area,2000-01,3,368: Per cent,,A: Normal value",
        f"{lead},D: Daily,AA: Alphaland,2000-01-03,1.5,368: Per cent,,A: Normal value",
        f"{lead},M: Monthly,AA: Alphaland,,,368: Per cent,,",
    ])
    part = amp.bis(csv, "bis_cbpol", ISO2, LIC)
    assert obs(part) == {("bis_cbpol:policy_rate", "001", "2000-01"): (1.5, None),
                         ("bis_cbpol:policy_rate", "001", "2000-02"): (1.75, "estimated"),
                         ("bis_cbpol:policy_rate", "002", "2000-01"): (0.0, None)}
    s = part.series[0]
    assert (s["kind"], s["transform"], s["period"], s["licence"]) == ("rate", "none", "month", LIC)
    assert part.notes["series-level rows with no time period (not observations)"] == 1
    assert part.notes["rows marked missing or with no value (set aside)"] == 1
    assert part.notes["places with no Natural Earth match (set aside; rows)"] == {"XM Euro area": 1}
    assert part.names == {"001": "Alphaland", "002": "Betaland"}


def test_bis_quarters_to_years_by_mean_of_four(tmp_path):
    lead = "dataflow,BIS:WS_SPP(1.0): Property prices,I"
    rows = [f"{lead},Q: Quarterly,AA: Alphaland,2001-Q{q},{v},628: Index,N: Nominal,A: Normal value" for q, v in zip((1, 2, 3, 4), (90, 100, 110, 120))]
    rows += [f"{lead},Q: Quarterly,AA: Alphaland,2002-Q{q},100,628: Index,N: Nominal,A: Normal value" for q in (1, 2, 3)]
    rows += [f"{lead},Q: Quarterly,AA: Alphaland,2001-Q1,50,628: Index,R: Real,A: Normal value"]
    part = amp.bis(bis_file(tmp_path, rows), "bis_spp", ISO2, LIC)
    assert obs(part) == {("bis_spp:nominal_index", "001", "2001"): (105.0, None)}
    assert part.notes["years with fewer than four quarters (not made into a year)"] == 1
    s = part.series[0]
    assert (s["kind"], s["transform"], s["period"]) == ("level", "log", "year")


def test_bis_fourth_quarter_and_log_fallback(tmp_path):
    head = "FREQ:Frequency,BORROWERS_CTY:Borrowers' country,TIME_PERIOD:Time period or range,OBS_VALUE:Observation Value,OBS_STATUS:Observation Status"
    rows = [f"Q: Quarterly,AA: Alphaland,2001-Q{q},{v},A: Normal value" for q, v in zip((1, 2, 3, 4), (1, 2, 3, 4))]
    rows += ["Q: Quarterly,BB: Betaland,2001-Q4,0,A: Normal value"]
    picks = [("x", "FREQ = 'Q'", "made-up", "index", "level", "log", "q4")]
    part = amp.bis(bis_file(tmp_path, rows, head), "bis_tc", ISO2, LIC, picks)
    assert obs(part) == {("bis_tc:x", "001", "2001"): (4.0, None), ("bis_tc:x", "002", "2001"): (0.0, None)}
    assert part.series[0]["transform"] == "log1p"  # a zero in the series rules out a plain log


def hfd_files(tmp_path):
    months = ",".join(amp.MONTHS)
    tfr = ",".join("TFR" + m for m in amp.MONTHS)
    crude = tmp_path / "stff.csv"
    crude.write_text(f"CountryCode,Area,Year,{months},UNK,TOT,{tfr},TFRTOT\n"
                     + "AAA,1,2000," + ",".join(str(100 + i) for i in range(12)) + ",5,1171," + ",".join(["1.5"] * 12) + ",1.5\n"
                     + "BBB,1,2000,0," + ",".join(["."] * 11) + ",.,.," + ",".join(["."] * 12) + ",.\n"
                     + "GBR_NP,1,2000," + ",".join(["7"] * 12) + ",0,84," + ",".join(["."] * 12) + ",.\n"
                     + "GBR_SCO,1,2000," + ",".join(["3"] * 12) + ",.,36," + ",".join(["."] * 12) + ",.\n")
    adjusted = tmp_path / "stffadj.csv"
    adjusted.write_text(f"CountryCode,Area,Year,{months},{tfr}\n"
                        + "AAA,1,2012," + ",".join(["100.5"] * 12) + "," + ",".join(["1.4"] * 11) + ",.\n")
    return str(crude), str(adjusted)


def test_hfd_births_and_rates(tmp_path):
    part = amp.hfd_stff(*hfd_files(tmp_path), COUNTRIES, LIC)
    o = obs(part)
    assert o[("hfd_stff:births", "001", "2000-01")] == (100.0, None)
    assert o[("hfd_stff:births", "001", "2000-12")] == (111.0, None)
    assert o[("hfd_stff:births", "002", "2000-01")] == (0.0, None)  # a zero count is kept, a '.' is no value
    assert ("hfd_stff:births", "002", "2000-02") not in o
    assert o[("hfd_stff:births", "006", "2000-06")] == (7.0, None)  # GBR_NP is the whole country
    assert sum(1 for k in o if k[0] == "hfd_stff:tfr") == 12
    assert sum(1 for k in o if k[0] == "hfd_stff:births_adjusted") == 12
    assert sum(1 for k in o if k[0] == "hfd_stff:tfr_adjusted") == 11
    assert part.notes["country codes with no whole-country match (set aside; values)"] == {"GBR_SCO": 12}
    assert part.notes["rows with births of unknown month (not used)"] == 1
    kinds = {s["series_id"]: (s["kind"], s["transform"]) for s in part.series}
    assert kinds == {"hfd_stff:births": ("count", "log1p"), "hfd_stff:tfr": ("rate", "none"),
                     "hfd_stff:births_adjusted": ("level", "log"), "hfd_stff:tfr_adjusted": ("rate", "none")}
    assert all(s["licence"] == LIC for s in part.series)


def test_eurostat_deaths(tmp_path):
    lead = "ESTAT:DEMO_MMONTH(1.0),23/09/26 23:00:00,A,NR"
    rows = [f"{lead},M01,AA,2000,10,,", f"{lead},M02,AA,2000,11,e,", f"{lead},M03,AA,2000,12,p,",
            f"{lead},M04,AA,2000,,,", f"{lead},M05,AA,2000,13,f,", f"{lead},TOTAL,AA,2000,46,,", f"{lead},UNK,AA,2000,0,,",
            f"{lead},M01,EL,2000,5,,", f"{lead},M01,DE_TOT,2000,6,,", f"{lead},M01,DE,2000,6,,", f"{lead},M01,FX,2000,7,,",
            f"{lead},M01,EU27_2020,2000,99,,", f"{lead},M01,UK,2000,0,,"]
    p = tmp_path / "demo_mmonth.csv"
    p.write_text("DATAFLOW,LAST UPDATE,freq,unit,month,geo,TIME_PERIOD,OBS_VALUE,OBS_FLAG,CONF_STATUS\n" + "\n".join(rows) + "\n")
    part = amp.eurostat_deaths(str(p), ISO2, LIC)
    assert obs(part) == {("eurostat_deaths:deaths", "001", "2000-01"): (10.0, None),
                         ("eurostat_deaths:deaths", "001", "2000-02"): (11.0, "estimated"),
                         ("eurostat_deaths:deaths", "001", "2000-03"): (12.0, "other"),
                         ("eurostat_deaths:deaths", "003", "2000-01"): (5.0, None),
                         ("eurostat_deaths:deaths", "004", "2000-01"): (6.0, None),
                         ("eurostat_deaths:deaths", "006", "2000-01"): (0.0, None)}
    assert part.notes["rows of the year's total or an unknown month (not used)"] == 2
    assert part.notes["rows with no value (set aside)"] == 1
    assert part.notes["rows flagged as a forecast (set aside)"] == 1
    assert part.notes["codes set aside by choice (rows)"] == {"DE": 1, "FX": 1}
    assert part.notes["codes with no Natural Earth match: groups of countries and others (set aside; rows)"] == {"EU27_2020": 1}
    s = part.series[0]
    assert (s["kind"], s["transform"], s["period"], s["licence"]) == ("count", "log1p", "month", LIC)


@pytest.mark.parametrize("flag,word", [(None, None), ("", None), ("e", "estimated"), ("ep", "estimated"), ("p", "other"), ("b", "other")])
def test_eurostat_flag(flag, word):
    assert amp.eurostat_flag(flag) == word


def test_iso2_codes(tmp_path):
    shapefile = pytest.importorskip("shapefile")
    w = shapefile.Writer(str(tmp_path / "ne"), shapeType=shapefile.POINT)
    for f in ("ADM0_A3", "UN_A3", "ISO_A2", "ISO_A2_EH"):
        w.field(f, "C")
    for rec in (("AAA", "001", "AA", "AA"), ("NOR", "-99", "-99", "NO"), ("CCC", "003", "CC", "CC"), ("DDD", "004", "CC", "CC"), ("EEE", "999", "EE", "EE")):
        w.point(0, 0)
        w.record(*rec)
    w.close()
    got, clashes = amp.iso2_codes({"001", "578", "003", "004"}, tmp_path / "ne.shp")
    assert got == {"AA": "001", "NO": "578"}
    assert clashes == ["CC"]
