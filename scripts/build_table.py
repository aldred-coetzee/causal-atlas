"""Build the three tables of the held data in one shape (data/table/): `build_table.py [source ...]` saves each named source's part, then joins every saved part. No source named builds all of them. Nothing here relates one series to another."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from causal_atlas import adapters_eurostat as eurostat  # noqa: E402
from causal_atlas import adapters_events as events  # noqa: E402
from causal_atlas import adapters_money_people as money  # noqa: E402
from causal_atlas import adapters_world_kinds as world  # noqa: E402
from causal_atlas import table  # noqa: E402
from causal_atlas.panel import RAW  # noqa: E402

ORDER = ("faostat", "drought", "indices", "fire", "ged", "prices", "wdi", "faostat_cp", "faostat_pe", "bis_cbpol", "bis_long_cpi", "bis_spp", "bis_tc", "bis_eer", "hfd_stff", "eurostat_deaths", "usgs_quakes", "mass_mobilization", "opendengue",
         "eurostat_unemployment", "eurostat_industry", "eurostat_retail", "eurostat_electricity", "eurostat_tourism", "eurostat_air", "eurostat_asylum", "eurostat_births",
         "unhcr", "ibtracs", "ember", "pink_sheet")
EUROSTAT = {c.source: t for t, c in eurostat.TABLES.items()}  # the source name in the manifest: Eurostat's table code


def run(name, countries):
    """The part for one source, from the files held."""
    if name == "faostat":
        return table.faostat(RAW / "faostat" / "Production_Crops_Livestock_E_All_Data_(Normalized).csv")
    if name == "drought":
        return table.drought(countries)
    if name == "indices":
        listing = json.loads((RAW / "candidates" / "listing.json").read_text())
        return table.indices(RAW / "oni.data", RAW / "candidates", listing, list(table.manifest()["candidates"]))
    if name == "fire":
        return table.fire(countries)
    if name == "ged":
        return table.ged(RAW / "ged" / "GEDEvent_v26_1.csv", countries)
    if name == "prices":
        return table.prices(RAW / "rtfp" / "WLD_RTFP_mkt_2026-11-02.csv", countries)
    if name == "wdi":
        return table.wdi(RAW / "wdi" / "WDICSV.csv", RAW / "wdi" / "WDISeries.csv", RAW / "wdi" / "WDICountry.csv", countries)
    if name == "faostat_cp":
        return table.faostat_cp(RAW / "faostat_prices" / "cp" / "ConsumerPriceIndices_E_All_Data_(Normalized).csv", countries)
    if name == "faostat_pe":
        return table.faostat_pe(RAW / "faostat_prices" / "pe" / "Exchange_rate_E_All_Data_(Normalized).csv", countries)
    if name.startswith("bis_"):
        return money.bis(next((RAW / "bis" / name.removeprefix("bis_").upper()).glob("*.csv")), name, money.iso2_codes(countries)[0], table.licence(table.manifest(), name))
    if name == "hfd_stff":
        return money.hfd_stff(RAW / "hfd_stff" / "stff.csv", RAW / "hfd_stff" / "stffadj.csv", countries, table.licence(table.manifest(), name))
    if name == "eurostat_deaths":
        return money.eurostat_deaths(RAW / "eurostat_deaths" / "demo_mmonth.csv", money.iso2_codes(countries)[0], table.licence(table.manifest(), name))
    if name == "usgs_quakes":
        return events.usgs_quakes(sorted((RAW / "usgs_quakes").glob("m4.5_*.csv")), countries, table.licence(table.manifest(), name))
    if name == "mass_mobilization":
        return events.mass_mobilization(RAW / "mass_mobilization" / "mmALL_073120_csv.csv", countries, table.licence(table.manifest(), name))
    if name == "opendengue":
        return events.opendengue(RAW / "opendengue" / "national" / "National_extract_V1_3_1.csv", countries, table.licence(table.manifest(), name))
    if name in EUROSTAT:
        return eurostat.eurostat_months(RAW / "eurostat" / EUROSTAT[name] / f"{EUROSTAT[name]}.csv", EUROSTAT[name], money.iso2_codes(countries)[0], table.licence(table.manifest(), name))
    if name == "unhcr":
        return world.unhcr(RAW / "unhcr" / "population_by_origin.json", RAW / "unhcr" / "population_by_asylum.json", countries, table.licence(table.manifest(), name))
    if name == "ibtracs":
        return world.ibtracs(RAW / "ibtracs" / "ibtracs.since1980.list.v04r01.csv", countries, table.licence(table.manifest(), name))
    if name == "ember":
        return world.ember(RAW / "ember" / "release_generation_monthly_global.csv", RAW / "ember" / "release_generation_yearly_global.csv", countries, table.licence(table.manifest(), name))
    if name == "pink_sheet":
        return world.pink_sheet(RAW / "pink_sheet" / "CMO-Historical-Data-Monthly.xlsx", RAW / "pink_sheet" / "CMO-Historical-Data-Annual.xlsx", table.licence(table.manifest(), name))
    raise SystemExit(f"unknown source {name}; choose from {ORDER}")


if __name__ == "__main__":
    wanted = sys.argv[1:] or list(ORDER)
    countries = table.natural_earth()
    for name in wanted:
        t = time.time()
        part = run(name, countries)
        table.write_part(name, part)
        print(f"{name}: {part.obs.num_rows} observations, {len(part.series)} series, {time.time() - t:.0f} s", part.notes, flush=True)
    t = time.time()
    print("assembled", table.assemble(table.PARTS, table.OUT, countries), f"{time.time() - t:.0f} s")
    notes = {p.stem.removesuffix(".meta"): json.loads(p.read_text())["notes"] for p in sorted(table.PARTS.glob("*.meta.json"))}
    (table.OUT / "notes.json").write_text(json.dumps(notes, indent=1, sort_keys=True))
