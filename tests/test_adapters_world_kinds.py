"""The adapters for refugees, tropical cyclones, electricity and commodity prices on tiny made-up files written here, never the real data."""
import json
import zipfile
from xml.sax.saxutils import escape

from shapely.geometry import box

from causal_atlas import adapters_world_kinds as wk

COUNTRIES = {"001": {"name": "Alpha", "iso": {"AAA"}, "shape": box(0, 0, 10, 10)}, "002": {"name": "Beta", "iso": {"BBB"}, "shape": box(20, 0, 30, 10)},
             "003": {"name": "Gamma", "iso": {"CCC"}, "shape": box(-160, 0, -150, 10)}}


def table_of(part):
    return {(r["series_id"], r["place_id"], r["period"]): (r["value"], r["flag"]) for r in part.obs.to_pylist()}


def values(part, series_id, place):
    return {k[2]: v[0] for k, v in table_of(part).items() if k[0] == series_id and k[1] == place}


def kinds(part):
    return {s["series_id"]: (s["kind"], s["transform"], s["period"]) for s in part.series}


def unhcr_files(tmp_path):
    def item(year, side, iso, name, refugees, asylum_seekers):
        row = {"year": year, "coo_iso": "-", "coo_name": "-", "coa_iso": "-", "coa_name": "-", "refugees": refugees, "asylum_seekers": asylum_seekers, "idps": "0"}
        row.update({f"{side}_iso": iso, f"{side}_name": name})
        return row
    origin = [item(1990, "coo", "AAA", "Alpha", 1200, "0"),  # an asylum seeker zero before the first year: not collected
              item(1993, "coo", "AAA", "Alpha", "0", 40),  # a zero the source wrote beside a figure that is not zero
              item(1994, "coo", "AAA", "Alpha", 900, "-"),  # a dash: no figure
              item(1993, "coo", "XXA", "Stateless", 10, 5)]  # no country
    asylum = [item(1993, "coa", "BBB", "Beta", 300, 7)]
    paths = []
    for name, items in (("o.json", origin), ("a.json", asylum)):
        (tmp_path / name).write_text(json.dumps({"page": 1, "items": items}), encoding="utf-8")
        paths.append(tmp_path / name)
    return paths


def test_unhcr_writes_given_zeros_leaves_missing_years_and_starts_asylum_seekers_in_1993(tmp_path):
    part = wk.unhcr(*unhcr_files(tmp_path), COUNTRIES, "CC BY 4.0")
    assert values(part, "unhcr:refugees:country_of_origin", "001") == {"1990": 1200, "1993": 0, "1994": 900}
    assert values(part, "unhcr:asylum_seekers:country_of_origin", "001") == {"1993": 40}  # 1990's "0" is before 1993; 1994's dash is nothing
    assert values(part, "unhcr:refugees:country_of_asylum", "002") == {"1993": 300}
    assert values(part, "unhcr:asylum_seekers:country_of_asylum", "002") == {"1993": 7}
    assert part.notes["codes with no Natural Earth match (set aside; rows)"] == {"XXA (Stateless; by origin)": 1}
    assert kinds(part)["unhcr:refugees:country_of_origin"] == ("level", "log1p", "year")
    assert kinds(part)["unhcr:refugees:country_of_asylum"] == ("level", "log", "year")
    assert {s["licence"] for s in part.series} == {"CC BY 4.0"}


IB_HEADER = "SID,SEASON,NUMBER,BASIN,SUBBASIN,NAME,ISO_TIME,NATURE,LAT,LON,WMO_WIND,WMO_PRES,WMO_AGENCY,TRACK_TYPE,DIST2LAND,LANDFALL,IFLAG,USA_AGENCY,USA_ATCF_ID,USA_LAT,USA_LON,USA_RECORD,USA_STATUS,USA_WIND"


def ib_file(path):
    rows = [(" ", "Year", "degrees_north", "degrees_east", "kts", ""),  # the file's line of units
            ("S1", "2000-03-31 21:00:00", 5, 5, 40, "main"),  # storm S1 inside Alpha at the end of March
            ("S1", "2000-04-01 00:00:00", 5, 6, 55, "main"),  # and into April
            ("S1", "2000-04-01 03:00:00", 5, 15, 65, "main"),  # at sea
            ("S1", "2000-04-01 06:00:00", 5, 7, "", "main"),  # inside Alpha with no wind
            ("S1", "2000-04-01 09:00:00", 5, 25, 99, "spur-other"),  # a spur track inside Beta: set aside
            ("S2", "2000-04-02 00:00:00", 5, 25, 30, "main"),  # strongest wind 30 kt: not counted
            ("S3", "2000-05-10 00:00:00", 5, 205, 50, "PROVISIONAL"),  # longitude past 180: Gamma, a provisional track
            ("S4", "1999-12-31 21:00:00", 5, 25, 45, "main"),  # before the span: set aside, but the storm counts in January
            ("S4", "2000-01-01 00:00:00", 5, 25, 35, "main")]
    lines = [",".join([str(s), "2000", "1", "NA", "MM", "X", str(t), "TS", str(lat), str(lon), "", "", "", track, "", "", "", "", "", "", "", "", "", str(w)]) for s, t, lat, lon, w, track in rows]
    path.write_text(IB_HEADER + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def test_ibtracs_counts_storms_by_shape_and_month_with_zeros_and_writes_wind_only_where_one_passed(tmp_path):
    ib_file(tmp_path / "ib.csv")
    part = wk.ibtracs(tmp_path / "ib.csv", COUNTRIES, "public domain", first="2000-01", last="2000-06")
    alpha = values(part, "ibtracs:storms:country_total", "001")
    assert len(alpha) == 6 and {k: v for k, v in alpha.items() if v} == {"2000-03": 1, "2000-04": 1}
    beta = values(part, "ibtracs:storms:country_total", "002")
    assert {k: v for k, v in beta.items() if v} == {"2000-01": 1}  # S4 in January; the spur and the weak storm are not counted
    assert values(part, "ibtracs:max_wind:country_total", "001") == {"2000-03": 40, "2000-04": 55}  # the 65 kt was at sea
    assert values(part, "ibtracs:max_wind:country_total", "002") == {"2000-01": 35}  # the 45 kt was before the span
    got = table_of(part)
    assert got[("ibtracs:storms:country_total", "003", "2000-05")] == (1, "provisional")
    assert got[("ibtracs:max_wind:country_total", "003", "2000-05")] == (50, "provisional")
    world = values(part, "ibtracs:storms:world", "world")
    assert world == {"2000-01": 1, "2000-02": 0, "2000-03": 1, "2000-04": 1, "2000-05": 1, "2000-06": 0}
    assert part.notes["positions on spur tracks (set aside)"] == 1
    assert part.notes["storms whose strongest USA_WIND reaches 34.0 kt (counted)"] == 3
    assert part.notes["positions of counted storms outside the span (set aside)"] == 1
    assert part.notes["positions of counted storms in no country's shape, at sea (world series only)"] == 1
    assert kinds(part)["ibtracs:storms:country_total"][0] == "count" and kinds(part)["ibtracs:max_wind:country_total"][0] == "level"
    assert part.names == {"world": "World"}


EMBER_HEADER = "Area,ISO 3 code,{when},Area type,Electricity source,Is aggregated source,Generation (TWh),Share of generation (%)"


def ember_files(tmp_path):
    monthly = [("Alpha", "AAA", "2020-01-01", "Country or economy", "Total generation", "True", 10.0),
               ("Alpha", "AAA", "2020-01-01", "Country or economy", "Coal", "False", 4.0),
               ("Alpha", "AAA", "2020-02-01", "Country or economy", "Total generation", "True", 11.0),  # no coal row in February: nothing
               ("Alpha", "AAA", "2020-01-01", "Country or economy", "Bioenergy", "False", 1.0),  # not asked for
               ("Europe", "", "2020-01-01", "Region", "Total generation", "True", 99.0),  # a region: not taken
               ("Kosovo", "XKX", "2020-01-01", "Country or economy", "Total generation", "True", 0.5)]  # no Natural Earth match
    yearly = [("Alpha", "AAA", "1990", "Country or economy", "Total generation", "True", 120.0),
              ("Alpha", "AAA", "1990", "Country or economy", "Nuclear", "False", 0.0),  # a zero the source wrote
              ("Beta", "BBB", "1990", "Country or economy", "Nuclear", "False", 2.0)]
    paths = []
    for name, when, rows in (("m.csv", "Date", monthly), ("y.csv", "Year", yearly)):
        (tmp_path / name).write_text(EMBER_HEADER.format(when=when) + "\n" + "\n".join(",".join(map(str, r)) + ",1" for r in rows) + "\n", encoding="utf-8")
        paths.append(tmp_path / name)
    return paths


def test_ember_takes_countries_monthly_and_yearly_and_leaves_missing_months_empty(tmp_path):
    part = wk.ember(*ember_files(tmp_path), COUNTRIES, "CC BY 4.0")
    assert values(part, "ember:generation_total:country_total", "001") == {"2020-01": 10.0, "2020-02": 11.0}
    assert values(part, "ember:generation_coal:country_total", "001") == {"2020-01": 4.0}
    assert values(part, "ember:generation_nuclear:country_total:year", "001") == {"1990": 0.0}
    assert values(part, "ember:generation_nuclear:country_total:year", "002") == {"1990": 2.0}
    assert {k[1] for k in table_of(part)} == {"001", "002"}
    assert part.notes["rows of countries with no Natural Earth match (set aside; by month)"] == {"XKX": 1}
    assert kinds(part)["ember:generation_nuclear:country_total:year"] == ("level", "log1p", "year")
    assert kinds(part)["ember:generation_total:country_total"] == ("level", "log", "month")
    assert not any("bioenergy" in s for s in kinds(part))


def write_xlsx(path, sheets):
    """A minimal workbook: each sheet a list of rows, each row a list of cells from column A; text goes to the shared strings, ("e", text) is an error cell."""
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    strings, files = [], {}
    for n, rows in enumerate(sheets.values(), start=1):
        out = []
        for r, row in enumerate(rows, start=1):
            cells = []
            for c, v in enumerate(row):
                ref = f"{'ABCDEFGHIJ'[c]}{r}"
                if v is None:
                    continue
                if isinstance(v, tuple):
                    cells.append(f'<c r="{ref}" t="e"><v>{escape(v[1])}</v></c>')
                elif isinstance(v, str):
                    strings.append(v)
                    cells.append(f'<c r="{ref}" t="s"><v>{len(strings) - 1}</v></c>')
                else:
                    cells.append(f'<c r="{ref}"><v>{v}</v></c>')
            out.append(f'<row r="{r}">{"".join(cells)}</row>')
        files[f"xl/worksheets/sheet{n}.xml"] = f'<worksheet xmlns="{main}"><sheetData>{"".join(out)}</sheetData></worksheet>'
    names = "".join(f'<sheet name="{escape(s)}" sheetId="{n}" r:id="rId{n}"/>' for n, s in enumerate(sheets, start=1))
    files["xl/workbook.xml"] = f'<workbook xmlns="{main}" xmlns:r="{rel}"><sheets>{names}</sheets></workbook>'
    files["xl/_rels/workbook.xml.rels"] = ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                                          + "".join(f'<Relationship Id="rId{n}" Type="x" Target="worksheets/sheet{n}.xml"/>' for n in range(1, len(sheets) + 1)) + "</Relationships>")
    files["xl/sharedStrings.xml"] = f'<sst xmlns="{main}">' + "".join(f"<si><t>{escape(s)}</t></si>" for s in strings) + "</sst>"
    with zipfile.ZipFile(path, "w") as z:
        for name, text in files.items():
            z.writestr(name, text)


def pink_files(tmp_path):
    names = [None, "Crude oil, average", "Natural gas index", "Rice, Thai 25% ", "DAP **"]
    units = [None, "($/bbl)", "(2010=100)", "($/mt)", "($/mt)"]
    monthly = [["World Bank Commodity Price Data"], [], names, units,
               ["2000M01", 25.5, 80, 200, "…"], ["2000M02", 26.0, 81, 0, 150], ["2000M03", 27.25, 82, ("e", "#VALUE!"), ".."], ["Note: a footnote"]]
    annual = [["Annual Prices (Nominal)"], names, units, ["1999", "…", 70, "…", 140], ["2000", 26.25, 81, 210, 150]]
    write_xlsx(tmp_path / "m.xlsx", {"Description": [["x"]], wk.PINK_MONTHLY_SHEET: monthly})
    write_xlsx(tmp_path / "a.xlsx", {wk.PINK_ANNUAL_SHEET: annual})
    return tmp_path / "m.xlsx", tmp_path / "a.xlsx"


def test_pink_sheet_world_prices_by_month_and_by_year_only_where_the_year_reaches_further_back(tmp_path):
    part = wk.pink_sheet(*pink_files(tmp_path), "CC BY 4.0")
    assert values(part, "pink_sheet:crude_oil_average:world", "world") == {"2000-01": 25.5, "2000-02": 26.0, "2000-03": 27.25}
    assert values(part, "pink_sheet:dap:world", "world") == {"2000-02": 150}  # "…" and ".." are nothing
    assert values(part, "pink_sheet:dap:world:year", "world") == {"1999": 140, "2000": 150}  # the year reaches back to 1999, the month to 2000
    assert values(part, "pink_sheet:rice_thai_25:world", "world") == {"2000-01": 200}  # a zero and an error cell set aside
    assert "pink_sheet:crude_oil_average:world:year" not in kinds(part)  # both records begin in 2000
    assert not any("natural_gas_index" in s for s in kinds(part))
    assert part.notes["cells that are not numbers above zero (set aside; monthly)"] == {"Rice, Thai 25% 2000M02: 0": 1, "Rice, Thai 25% 2000M03: #VALUE!": 1}
    assert part.notes["index columns left out"] == ["Natural gas index"]
    assert {s["unit"] for s in part.series} == {"$/bbl", "$/mt"}
    assert {s["place_level"] for s in part.series} == {"world"} and part.names == {"world": "World"}
    assert kinds(part)["pink_sheet:dap:world"] == ("level", "log", "month")
