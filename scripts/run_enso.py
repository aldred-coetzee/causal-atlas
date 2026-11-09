"""Real known-answer test: is the ONI named, among decoys, as a driver of drought over Africa, with where and when. Rule: results/real-enso-drought.md."""
import json
import sys
from pathlib import Path

import numpy as np

from causal_atlas import decoy, field, links

OUT = Path(__file__).resolve().parents[1] / "results" / "real-enso-drought.jsonl"
SAVE = field.PANEL / "real"
SEEDS = range(11001, 11021)
RULER_SEEDS = range(11101, 11111)
DISCOVERY = 600  # months: 1950-01 to 1999-12
YEARS = np.arange(1, DISCOVERY // 12)
SHIFTS = range(1, DISCOVERY // 12)
CLIP = 3.0
SHARES = (0.02, 0.05, 0.15, 0.40)
AREAS = (0.05, 0.25)
RULER_LAG = 5


def data():
    y, kept = field.spei()
    lat, lon = field.cells()
    return np.clip(y, -CLIP, CLIP), field.oni(), lat[kept], lon[kept]


def row(kind, seed, out, **more):
    r = {"kind": kind, "seed": seed, "leads": out["leads"], "top": out["top"], "z": [round(v, 3) for v in out["z"]], **more}
    with open(OUT, "a") as f:
        f.write(json.dumps(r) + "\n")
    print(r, flush=True)


def discover():
    y, x, _, _ = data()
    y, x = y[:, :DISCOVERY], x[:DISCOVERY]
    for seed in SEEDS:
        d = decoy.make(seed, field.MONTHS, field.oni())[:, :DISCOVERY]
        row("real", seed, links.search(y, [x, *d], YEARS, SHIFTS))
        row("no_oni", seed, links.search(y, list(d), YEARS, SHIFTS))
        order = np.random.default_rng(seed).permutation(DISCOVERY // 12)
        mixed = y.reshape(len(y), -1, 12)[:, order].reshape(len(y), -1)
        row("years_mixed", seed, links.search(mixed, [x, *d], YEARS, SHIFTS))


def planted(y, lat, lon, z, seed, share, area):
    """y with a link from z added in the nearest cells to a seeded centre, in three consecutive target months, at RULER_LAG."""
    rng = np.random.default_rng(seed)
    c = rng.integers(len(y))
    dist = (lat - lat[c]) ** 2 + ((lon - lon[c]) * np.cos(np.radians(lat[c]))) ** 2
    cells = np.argsort(dist)[: int(area * len(y))]
    m0 = int(rng.integers(12))
    months = [(m0 + k) % 12 for k in range(3)]
    t = np.arange(12, y.shape[1])
    t = t[np.isin(t % 12, months)]
    out = y.copy()
    out[np.ix_(cells, t)] += np.sqrt(share / (1 - share)) * z[t - RULER_LAG]
    return out, cells, months


def ruler():
    y, x, lat, lon = data()
    y, x = y[:, :DISCOVERY], x[:DISCOVERY]
    for seed in RULER_SEEDS:
        d = decoy.make(seed, field.MONTHS, field.oni())[:, :DISCOVERY]
        for share in SHARES:
            for area in AREAS:
                yp, cells, months = planted(y, lat, lon, d[0], seed, share, area)
                out = links.search(yp, [x, *d], YEARS, SHIFTS)
                more = {"share": share, "area": area, "found": 1 in out["leads"], "false": [c for c in out["leads"] if c > 1]}
                if more["found"]:
                    sig = links.significant(links.correlations(yp, d[0], YEARS), len(YEARS))
                    inside = np.zeros(len(y), bool)
                    inside[cells] = True
                    hit = sig[RULER_LAG][months]
                    more["claims"] = int(sig.sum())
                    more["claims_true_cells"] = round(float(sig[:, :, inside].sum() / max(sig.sum(), 1)), 3)
                    more["true_cell_months_claimed"] = round(float(hit[:, inside].mean()), 3)
                row("ruler", seed, out, **more)


def where():
    """The ONI's map on the discovery years, saved for marking."""
    y, x, lat, lon = data()
    r = links.correlations(y[:, :DISCOVERY], x[:DISCOVERY], YEARS)
    np.savez(SAVE / "oni_discovery.npz", r=r.astype(np.float32), sig=links.significant(r, len(YEARS)), lat=lat, lon=lon)


# Mark D5: box (south, north, west, east), target months (0 is January; SPEI-3 there covers that month and the two before), expected sign under El Niño.
REGIONS = {
    "southern_africa": ((-35, -15, 15, 40), (0, 1, 2), -1),
    "east_africa": ((-7, 5, 29, 42), (11, 0), 1),
    "sahel": ((11, 15, -17, 40), (8, 9), -1),
}
MAP_LAGS = range(5)


def mapmark():
    """Each region's mean correlation with the ONI in its season at lags 0 to 4, against the same for every whole-year shift."""
    y, x, lat, lon = data()
    y, x = y[:, :DISCOVERY], x[:DISCOVERY]
    for name, ((s, n, w, e), months, sign) in REGIONS.items():
        box = (lat >= s) & (lat <= n) & (lon >= w) & (lon <= e)
        vals = []
        for shift in (0, *SHIFTS):
            r = links.correlations(y[box], np.roll(x, 12 * shift), YEARS, tuple(MAP_LAGS))
            vals.append(float(r[:, list(months)].mean()))
        got, rest = sign * vals[0], sign * np.array(vals[1:])
        full = links.correlations(y, x, YEARS)
        sig = links.significant(full, len(YEARS))[: len(MAP_LAGS)][:, list(months)][:, :, box]
        rr = full[: len(MAP_LAGS)][:, list(months)][:, :, box]
        r = {"kind": "map", "region": name, "cells": int(box.sum()), "expected": sign, "mean_r": round(vals[0], 4),
             "beats_shifts": int((got > rest).sum()), "of": len(rest), "right_sign": bool(got > 0),
             "cells_claimed": round(float(sig.any(axis=(0, 1)).mean()), 3),
             "claims_right_sign": round(float((np.sign(rr[sig]) == sign).mean()), 3) if sig.any() else None}
        with open(OUT, "a") as f:
            f.write(json.dumps(r) + "\n")
        print(r, flush=True)


if __name__ == "__main__":
    {"discover": discover, "ruler": ruler, "where": where, "mapmark": mapmark}[sys.argv[1]]()
