"""Four sources of kinds the table lacks, for most of the world, each into its own folder under data/raw/:
UNHCR's refugee population statistics (its public API, every year, once by country of origin and once by country of asylum);
NOAA's IBTrACS best tracks, version v04r01, the file of storms since 1980 with its two documents;
Ember's electricity generation by country, monthly and yearly, with its methodology;
the World Bank's commodity prices (the "Pink Sheet"), monthly and yearly.
`fetch_world_kinds.py [unhcr] [ibtracs] [ember] [pink]`; none named fetches all four.
A file already held is not fetched again; its size and SHA-256 are printed either way.
None of these needs an account, a key, a form or an email address."""
import hashlib
import sys
import time

from _download import RAW, download

UNHCR_API = "https://api.unhcr.org/population/v1/population/?limit=100000&yearFrom=1951&yearTo=2026&{side}_all=true"
UNHCR = {"population_by_origin.json": UNHCR_API.format(side="coo"),
         "population_by_asylum.json": UNHCR_API.format(side="coa")}

IB = "https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/"
IBTRACS = {"ibtracs.since1980.list.v04r01.csv": IB + "access/csv/ibtracs.since1980.list.v04r01.csv",
           "IBTrACS_version4r01_Technical_Details.pdf": IB + "doc/IBTrACS_version4r01_Technical_Details.pdf",
           "IBTrACS_v04r01_column_documentation.pdf": IB + "doc/IBTrACS_v04r01_column_documentation.pdf"}

EM = "https://files.ember-energy.org/public-downloads/"
EMBER = {"release_generation_monthly_global.csv": EM + "generation/outputs/release_generation_monthly_global.csv",
         "release_generation_yearly_global.csv": EM + "generation/outputs/release_generation_yearly_global.csv",
         "ember_electricity_data_methodology.pdf": EM + "ember_electricity_data_methodology.pdf"}

PS = "https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/"
PINK = {"CMO-Historical-Data-Monthly.xlsx": PS + "CMO-Historical-Data-Monthly.xlsx",
        "CMO-Historical-Data-Annual.xlsx": PS + "CMO-Historical-Data-Annual.xlsx"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            h.update(chunk)
    return h.hexdigest()


def held(name):
    """True if the file is already under data/raw/ and not empty (a file is only given its name once whole: see fetch)."""
    p = RAW / name
    return p.exists() and p.stat().st_size > 0


def fetch(url, name):
    """Download under a `.part` name and rename when done, so a run stopped midway never leaves a file that looks whole."""
    part = download(url, name + ".part")
    return part.rename(RAW / name)


def get(folder, files):
    """Each file fetched once, with a short pause between requests; size and SHA-256 printed for every file held."""
    (RAW / folder).mkdir(parents=True, exist_ok=True)
    for name, url in files.items():
        if not held(f"{folder}/{name}"):
            fetch(url, f"{folder}/{name}")
            time.sleep(2)
        p = RAW / folder / name
        print(f"  {folder}/{name} {p.stat().st_size} bytes sha256 {sha256(p)}", flush=True)


if __name__ == "__main__":
    wanted = sys.argv[1:] or ["unhcr", "ibtracs", "ember", "pink"]
    for key, folder, files in (("unhcr", "unhcr", UNHCR), ("ibtracs", "ibtracs", IBTRACS),
                               ("ember", "ember", EMBER), ("pink", "pink_sheet", PINK)):
        if key in wanted:
            get(folder, files)
