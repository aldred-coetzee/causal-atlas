"""Exploration on a spent period, marking nothing: how far the forecast score on the four entered fields moves when the drought index is re-scaled on the fitting years and El Niño is measured on a fixed base. Registered in results/real-enso-continents.md before it was computed."""
import json
import sys
from pathlib import Path

import numpy as np

from causal_atlas import field, forecast, links
from causal_atlas.panel import RAW
from run_continents import NAMED, SCORED, marks, verdict
from run_continents import rows as scored_rows
from run_enso import CLIP, DISCOVERY

OUT = Path(__file__).resolve().parents[1] / "results" / "explore-bases.jsonl"
VARIANTS = {"A": ("as_made", "oni"), "B": ("refit", "oni"), "C": ("as_made", "fixed"), "D": ("refit", "fixed")}
FIT_YEARS = DISCOVERY // 12


def drought(which, how):
    """Region averages for one field and their mean. refit: each cell and calendar month re-centred and re-scaled on the fitting years, before the clip."""
    y, lat, lon = field.box(which)
    if how == "refit":
        m = y.reshape(len(y), -1, 12).astype(np.float64)
        spread = m[:, :FIT_YEARS].std(axis=1, keepdims=True)
        assert (spread > 0).all()
        y = ((m - m[:, :FIT_YEARS].mean(axis=1, keepdims=True)) / spread).reshape(len(y), -1).astype(np.float32)
    y = links.tiles(lat, lon) @ np.clip(y, -CLIP, CLIP)
    return y, np.repeat(y.mean(axis=0, keepdims=True), len(y), axis=0)


def fixed():
    """Niño 3.4 by month on the field's clock: each calendar month's mean over the fitting years taken off, then a three-month mean centred on each month, as the ONI has."""
    by_year = {}
    for line in open(RAW / "candidates" / "nina34.anom.data"):
        p = line.split()
        if len(p) == 13 and p[0].isdigit():
            by_year[int(p[0])] = [float(v) for v in p[1:]]
    x = np.array([by_year[y] for y in range(field.FIRST_YEAR - 1, field.LAST_YEAR + 2)])
    assert (x > -90).all()
    x = (x - x[1 : 1 + FIT_YEARS].mean(axis=0)).ravel()
    return np.convolve(x, np.ones(3) / 3, mode="same")[12:-12]


def run(variant, entered):
    how, driver = VARIANTS[variant]
    x = field.oni() if driver == "oni" else fixed()
    out, pool = [], None
    for which in entered:
        y, near = drought(which, how)
        model = forecast.fit(y, near, x, DISCOVERY)
        parts = [*forecast.score(model, x, SCORED), forecast.errors(y, near, model["claimed"], DISCOVERY, SCORED)]
        out.append({"kind": "field", "variant": variant, "field": which, "baseline": model["baseline"], "k": round(model["k"], 3), "claimed": int(model["claimed"].sum()), **verdict(*parts)})
        pool = parts if pool is None else [p + q if not isinstance(p, dict) else {k: p[k] + q[k] for k in p} for p, q in zip(pool, parts)]
    out.append({"kind": "pooled", "variant": variant, "drought": how, "driver": driver, **verdict(*pool)})
    return out


def indices():
    """The two El Niño series side by side: correlation and mean difference (fixed base less ONI) on the fitting years and on the scored years."""
    a, b = field.oni(), fixed()
    out = {"kind": "indices"}
    for name, part in (("fit", slice(0, DISCOVERY)), ("scored", slice(DISCOVERY, field.MONTHS))):
        out[name] = {"r": round(float(np.corrcoef(a[part], b[part])[0, 1]), 4), "mean_oni": round(float(a[part].mean()), 3), "mean_fixed": round(float(b[part].mean()), 3), "largest_gap": round(float(np.abs(b[part] - a[part]).max()), 3)}
    return out


if __name__ == "__main__":
    done = scored_rows()
    entered = [f for f in field.BOXES if marks(done)[0][f] >= NAMED]
    found = [r for v in sys.argv[1:] or VARIANTS for r in run(v, entered)]
    was = next(r for r in done if r["kind"] == "pooled" and r["scale"] == "region")
    for r in found:
        if (r["kind"], r["variant"]) == ("pooled", "A"):
            assert abs(r["s"] - was["s"]) < 1e-9, "variant A is not the model as scored"
        print({k: v for k, v in r.items() if k != "shifted"}, flush=True)
    if len(sys.argv) == 1:  # the whole exploration: the rows are rewritten, and are deterministic
        found.append(indices())
        print(found[-1])
        OUT.write_text("".join(json.dumps(r) + "\n" for r in found))
