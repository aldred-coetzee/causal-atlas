"""The country drought series alone (no yield is loaded for the real record), set beside the made-up moisture of a few of my seeds: memory from year to year at the six fixed months, drift, the jump at the wrap the shifts make, and whether the spread changes over the record."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path("synth").resolve()))
sys.path.insert(0, "src")
import harvest_panel  # noqa: E402

from causal_atlas import harvest  # noqa: E402


def describe(name, x, years=64):
    f = harvest.seasons(x, years)  # countries, years, 6
    r1 = np.nanmean([np.corrcoef(f[c, 1:, k], f[c, :-1, k])[0, 1] for c in range(len(f)) for k in range(6)])
    r2 = np.nanmean([np.corrcoef(f[c, 2:, k], f[c, :-2, k])[0, 1] for c in range(len(f)) for k in range(6)])
    t = np.arange(years) - (years - 1) / 2
    ann = f.mean(axis=2)
    slope = (ann - ann.mean(axis=1, keepdims=True)) @ t / (t @ t) * years  # change over the record, in the driver's units
    sd = ann.std(axis=1)
    early, late = f[:, :20].std(axis=1).mean(axis=1), f[:, -20:].std(axis=1).mean(axis=1)
    jump = x[:, -60:].mean(axis=1) - x[:, :60].mean(axis=1)
    # residual curvature after a straight line: share of the annual series' variance in a quadratic beyond the line
    q = t**2 - (t**2).mean()
    res = ann - ann.mean(axis=1, keepdims=True) - np.outer((ann - ann.mean(axis=1, keepdims=True)) @ t / (t @ t), t)
    curve = (res @ q) ** 2 / (q @ q) / (res**2).sum(axis=1)
    print(f"{name:14s} n={len(x):3d} lag1 {r1:+.3f} lag2 {r2:+.3f} | change over record / annual sd: median {np.median(np.abs(slope) / sd):.2f}, 90th pct {np.percentile(np.abs(slope) / sd, 90):.2f}; share drying {np.mean(slope < 0):.2f}"
          f" | season sd late/early: median {np.median(late / early):.2f}, 10th {np.percentile(late / early, 10):.2f}, 90th {np.percentile(late / early, 90):.2f}"
          f" | last 5 yrs minus first 5 / monthly sd: median {np.median(np.abs(jump) / x.std(axis=1)):.2f} | quadratic share of detrended annual var: median {np.median(curve):.3f} 90th {np.percentile(curve, 90):.3f}")


z = np.load("data/panel/real/yields.npz")
x = z["x"]
cells = z["cells"]
print("real: countries", len(x), "months", x.shape[1], "finite", bool(np.isfinite(x).all()), "cells <5:", int((cells < 5).sum()))
describe("real", x)
# countries whose early seasons barely move (station-poor stretches)
f = harvest.seasons(x, 64)
lo = f[:, :25].std(axis=1).min(axis=1)
print("real: least season sd over 1961-1985 by country, smallest five:", np.round(np.sort(lo)[:5], 3))
for kind in ("none", "drift", "step"):
    for seed in (23010, 23011):
        w = harvest_panel.make(seed, kind=kind)
        describe(f"made-up {kind} {seed}", w["x"])
