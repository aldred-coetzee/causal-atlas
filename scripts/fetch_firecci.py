"""ESA Fire_cci FireCCILT11: AVHRR-LTDR burned area, grid product v1.1, global 0.25 degree, one file per month, 1982 to 2018 without 1994. About 7.2 GB.

A stopped run picks up where it left off. Writes data/firecci.sha256, one line per file, and prints the checksum of that listing for data/manifest.toml."""
import hashlib
import http.client
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "data" / "raw" / "firecci"
SUMS = ROOT / "data" / "firecci.sha256"
BASE = "https://dap.ceda.ac.uk/neodc/esacci/fire/data/burned_area/AVHRR-LTDR/grid/v1.1"
YEARS = [y for y in range(1982, 2019) if y != 1994]  # the makers left 1994 out: too little input that year
SIZE = 16663142  # every file, per CEDA's listing read 2026-11-10
TRIES = 5


def name(year, month):
    return f"{year}{month:02d}01-ESACCI-L4_FIRE-BA-AVHRR-LTDR-fv1.1.nc"


def sha(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def fetch(year, month):
    dest = DIR / name(year, month)
    if dest.exists() and dest.stat().st_size == SIZE:
        return dest
    # An honest agent, with no contact details.
    req = urllib.request.Request(f"{BASE}/{year}/{dest.name}", headers={"User-Agent": "causal-atlas-fetch/0.1"})
    part = dest.with_suffix(".part")
    # A connection can drop mid-file and leave a short body: a file is kept only at its full size.
    for attempt in range(TRIES):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp, open(part, "wb") as out:
                while chunk := resp.read(1 << 20):
                    out.write(chunk)
        except (OSError, http.client.HTTPException) as e:
            print(f"{dest.name}: {e}", flush=True)
        if part.exists() and part.stat().st_size == SIZE:
            part.rename(dest)
            return dest
        time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"{dest.name}: not fetched whole in {TRIES} tries")


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    for year in YEARS:
        for month in range(1, 13):
            dest = fetch(year, month)
            lines.append(f"{sha(dest)}  {dest.name}\n")
        print(year, flush=True)
    SUMS.write_text("".join(lines))
    print(f"{len(lines)} files, {len(lines) * SIZE} bytes, listing sha256:{hashlib.sha256(SUMS.read_bytes()).hexdigest()}", file=sys.stdout, flush=True)


if __name__ == "__main__":
    main()
