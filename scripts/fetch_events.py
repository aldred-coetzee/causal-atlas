"""Three small sources of events and disease, each into its own folder under data/raw/: the USGS earthquake catalogue (ComCat) at magnitude 4.5 and above, one query a year, 1973 to 2025; Mass Mobilization protest data, version 5 (Harvard Dataverse), the original CSV and the users' manual; OpenDengue V1.3.1, the national and the highest temporal extracts (figshare, the release's own record). `fetch_events.py [usgs] [mm] [dengue]`; none named fetches all three. A file already held is not fetched again. Unpack the OpenDengue zips with: python -I -m zipfile -e data/raw/opendengue/<file>.zip data/raw/opendengue/<national or temporal>"""
import hashlib
import sys
import time

from _download import RAW, download

USGS = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&eventtype=earthquake&orderby=time-asc&minmagnitude=4.5&starttime={y}-01-01T00:00:00&endtime={y}-12-31T23:59:59.999"
USGS_YEARS = range(1973, 2026)  # the NEIC PDE's first year in ComCat to the last whole year
USGS_LIMIT = 20000  # the API's most events a query; a year at the limit would be cut short
# The record lists the file as its tab-separated copy, but the MD5 it states is that of the CSV as deposited, which is what format=original returns.
MM = {"mmALL_073120_csv.csv": ("https://dataverse.harvard.edu/api/access/datafile/4291456?format=original", "e6fa8a2e9d120eff0167a788e8a3ea7f"),
      "MM_users_manual_0515.pdf": ("https://dataverse.harvard.edu/api/access/datafile/2775560", "efb7ca11ee0eadae9122b2b7cee08560")}
DENGUE = {"National_extract_V1_3_1.zip": ("https://ndownloader.figshare.com/files/71041980", "5b5ea930dc3cc24ede9704c4553d449e"),
          "Temporal_extract_V1_3_1.zip": ("https://ndownloader.figshare.com/files/71041986", "4f88cec8df68f1ba8d3f21c1def60ed7"),
          "metadata_main.json": ("https://ndownloader.figshare.com/files/54855152", "a7da0d360b1300f1354d66de5b19539d")}


def md5(path):
    """The MD5 of a file, to set beside the one its repository states."""
    h = hashlib.md5()
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


def usgs():
    """One CSV a year; a short pause between queries, and a year that comes back at the API's limit stops the run."""
    (RAW / "usgs_quakes").mkdir(parents=True, exist_ok=True)
    for y in USGS_YEARS:
        name = f"usgs_quakes/m4.5_{y}.csv"
        if held(name):
            continue
        dest = fetch(USGS.format(y=y), name)
        with open(dest, encoding="utf-8") as f:
            rows = sum(1 for _ in f) - 1
        print(f"  {y}: {rows} events", flush=True)
        if rows >= USGS_LIMIT:
            raise SystemExit(f"{y} returned {rows} events, the API's limit: fetch it by month")
        time.sleep(2)


def checked(folder, files):
    """Each file fetched once, its MD5 set beside the one the repository's record states."""
    (RAW / folder).mkdir(parents=True, exist_ok=True)
    for name, (url, want) in files.items():
        if not held(f"{folder}/{name}"):
            fetch(url, f"{folder}/{name}")
            time.sleep(2)
        got = md5(RAW / folder / name)
        verdict = "no MD5 in the record for this file" if want is None else "matches the record" if got == want else "DIFFERS from the record " + want
        print(f"  {name} md5 {got} {verdict}", flush=True)


if __name__ == "__main__":
    wanted = sys.argv[1:] or ["usgs", "mm", "dengue"]
    if "usgs" in wanted:
        usgs()
    if "mm" in wanted:
        checked("mass_mobilization", MM)
    if "dengue" in wanted:
        checked("opendengue", DENGUE)
