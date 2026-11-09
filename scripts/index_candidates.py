"""Every series on NOAA PSL's page of monthly time series, and the candidate rule of results/real-indices.md applied to them. Nothing here reads a drought value."""
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

from _download import RAW, download
from causal_atlas import field
from run_enso import DISCOVERY

PAGE = "https://psl.noaa.gov/data/timeseries/month/"
HOST = "https://psl.noaa.gov"
DIR = "candidates"
LAGS = range(-12, 13)
ONI_LIKE = 0.6  # largest absolute correlation with the ONI: at or above, it is El Niño by another name
TREND = 0.25  # share of variance a straight line explains: at or above, it is mostly a trend
SAME = 0.9  # absolute correlation with a series already kept: at or above, it is that series again
LEFT_OUT = "Precipitation Time-series"  # the outcome is built from rainfall


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causal-atlas-fetch/0.1"})
    return urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")


def fetch():
    """The page, each listed series' description file, and the one or two data files it names. Order is the page's."""
    (RAW / DIR).mkdir(parents=True, exist_ok=True)
    page = get(PAGE)
    (RAW / DIR / "page.html").write_text(page)
    listing = []
    for ds in dict.fromkeys(re.findall(r'href="/data/timeseries/month/DS/(\w+)/?"', page)):
        about = json.loads(get(f"{PAGE}{ds}/keyvalues.json"), strict=False)
        for n in ("", "2"):
            if about.get(f"dataprefix{n}"):
                stem = about[f"dataprefix{n}"]
                listing.append({"page": ds, "file": f"{stem}.data", "label": about.get(f"dataprefix{n}name", ""), "url": f"{HOST}{about[f'timeprefix{n}']}{stem}.data", "source": about.get("source"), "from": about.get("sourcedata")})
                try:
                    download(listing[-1]["url"], f"{DIR}/{stem}.data")
                except Exception as e:
                    listing[-1]["error"] = str(e)
                time.sleep(0.3)
    (RAW / DIR / "listing.json").write_text(json.dumps(listing, indent=1))


def read(path):
    """The 900 months from 1950-01 in PSL's layout, NaN where missing: no row for the year, a value below -90, or the file's own missing value, which is the line after its last year."""
    rows, marker = {}, None
    for line in open(path, errors="replace"):
        p = line.split()
        if len(p) == 13 and p[0].isdigit():
            try:
                rows[int(p[0])] = [float(v) for v in p[1:]]
            except ValueError:
                pass
        elif rows and marker is None and len(p) == 1:
            try:
                marker = float(p[0])
            except ValueError:
                pass
    x = np.array([rows.get(y, [np.nan] * 12) for y in range(field.FIRST_YEAR, field.LAST_YEAR + 1)]).ravel()
    x[x < -90] = np.nan
    if marker is not None:
        x[x == marker] = np.nan
    return x


def anomaly(x):
    """Departure from the series' own calendar-month means over the discovery years."""
    x = x.reshape(-1, 12)
    return (x - x[: DISCOVERY // 12].mean(axis=0)).ravel()


def measure(x, oni):
    """On the discovery years, for the series as it would be used: the share of variance a straight line explains, and the largest absolute correlation with the ONI at any lag in LAGS."""
    a = anomaly(x)[:DISCOVERY]
    if a.std() == 0:
        return float("nan"), float("nan")
    line = np.corrcoef(np.arange(DISCOVERY), a)[0, 1] ** 2
    inner = slice(12, DISCOVERY - 12)
    r = max(abs(np.corrcoef(a[inner], oni[inner.start + lag : inner.stop + lag])[0, 1]) for lag in LAGS)
    return float(line), float(r)


def table():
    """One row per listed file, in the page's order: months missing, the two measurements, and whether its page is in the section left out."""
    oni = field.oni()
    page = (RAW / DIR / "page.html").read_text()
    start = page.index(LEFT_OUT)
    left_out = set(re.findall(r"month/DS/(\w+)", page[start : page.index("<caption", start)]))
    out = []
    for item in json.loads((RAW / DIR / "listing.json").read_text()):
        path = RAW / DIR / item["file"]
        x = read(path) if path.exists() else np.full(field.MONTHS, np.nan)
        missing = int(np.isnan(x).sum())
        line, r = measure(x, oni) if not missing else (float("nan"), float("nan"))
        out.append({**item, "missing": missing, "line": line, "oni": r, "left_out": item["page"] in left_out})
    return out


def verdict(rows):
    """Why each row is in or out, by the rule in its order. A file listed twice counts once."""
    kept, out = {}, []
    for t in rows:
        if t["file"] in {v["file"] for v, _ in out}:
            continue
        if t["missing"]:
            why = f"{t['missing']} months missing"
        elif t["left_out"]:
            why = "rainfall"
        elif t["oni"] >= ONI_LIKE:
            why = "El Niño by another name"
        elif t["line"] >= TREND:
            why = "mostly a trend"
        else:
            a = anomaly(read(RAW / DIR / t["file"]))[:DISCOVERY]
            twin = next((k for k, b in kept.items() if abs(np.corrcoef(a, b)[0, 1]) >= SAME), None)
            why = f"the same as {twin}" if twin else "in"
            if not twin:
                kept[t["file"]] = a
        out.append((t, why))
    return out


def kept():
    return tuple(t["file"] for t, why in verdict(table()) if why == "in")


if __name__ == "__main__":
    if sys.argv[1:] == ["fetch"]:
        fetch()
    for t, why in verdict(table()):
        print(f"{t['page']:22s} {t['file']:30s} line {t['line']:.2f}  oni {t['oni']:.2f}  {why}  {t.get('error', '')}")
    print(len(kept()), "in:", kept())
