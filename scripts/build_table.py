"""Build the three tables of the held data in one shape (data/table/): `build_table.py [source ...]` saves each named source's part, then joins every saved part. No source named builds all of them. Nothing here relates one series to another."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from causal_atlas import table  # noqa: E402
from causal_atlas.panel import RAW  # noqa: E402

ORDER = ("faostat", "drought", "indices", "fire", "ged", "prices", "wdi", "faostat_cp", "faostat_pe")


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
