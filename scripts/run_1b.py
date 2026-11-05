"""One 1b replicate through baseline, model, interval and both shuffles. Appends one JSON line."""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

PERMS = 19
SUB_CELLS = 2000


def subpanel(lat, lon, cells=SUB_CELLS):
    """The cells nearest the median latitude and longitude, fixed before any detector result."""
    dist = (lat - np.median(lat)) ** 2 + (lon - np.median(lon)) ** 2
    return np.sort(np.argsort(dist, kind="stable")[:cells])


def replicate(panel, seed, size, timing=False):
    _, lat, lon = load()
    if size == "sub":
        keep = subpanel(lat, lon)
        lat, lon = lat[keep], lon[keep]
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    n = len(lat)
    tau = np.arange(d.TRAIN[0], d.HELD[1] + 1)
    months = len(tau)
    target = y[:, tau].ravel().astype(np.float32)
    in_month = np.tile(tau, n)
    fit_rows = in_month <= d.VALID[1]
    held_rows = in_month >= d.HELD[0]
    base = d.base_features(y, lat, lon)
    obs = y[:, d.HELD[0] : d.HELD[1] + 1]
    shape = (n, d.HELD[1] - d.HELD[0] + 1)

    def m_skill(dr, on, b):
        X = np.hstack([base, d.input_features(dr, on)])
        return d.fit_predict(X, target, fit_rows, held_rows).reshape(shape)

    started = time.time()
    b = d.fit_predict(base, target, fit_rows, held_rows).reshape(shape)
    after_b = time.time()
    m = m_skill(drought, oni, b)
    after_m = time.time()
    observed = float(d.skill(obs, m, b))
    if timing:
        return dict(panel=panel, seed=seed, size=size, cells=n, rows=int(fit_rows.sum()),
                    b_seconds=round(after_b - started, 1), m_seconds=round(after_m - after_b, 1),
                    skill=observed, events_held=int(obs.sum()))
    low, high = d.block_interval(obs, m, b)
    shifts = [float(d.skill(obs, m_skill(d.circular_shift(drought, k), d.circular_shift(oni, k), b), b))
              for k in range(1, d.SHIFTS + 1)]
    perms = [float(d.skill(obs, m_skill(d.year_permutation(drought, 5000 + i), d.year_permutation(oni, 5000 + i), b), b))
             for i in range(PERMS)]
    months_held = np.arange(d.HELD[0], d.HELD[1] + 1)
    rate, no_link = g["rate"], g["rate_no_link"]
    out = dict(panel=panel, seed=seed, size=size, cells=n, skill=observed, ci=[low, high],
               shift_max=max(shifts), shift_median=float(np.median(shifts)),
               perm_max=max(perms), perm_median=float(np.median(perms)),
               circular=d.verdict(observed, low, shifts), permutation=d.verdict(observed, low, perms),
               b0_skill_of_b=float(d.skill(obs, b, np.maximum(d.naive_b0(y)[:, -shape[1]:], 1e-3))),
               events_held=int(obs.sum()), seconds=round(time.time() - started, 1))
    if rate is not None and no_link is not None and panel.startswith("planted"):
        linked = g["linked"].any(axis=1) if g["linked"].ndim > 1 else g["linked"]
        out.update(best_all=float(d.skill(y[:, 36:], rate[:, 36:], no_link[:, 36:])),
                   best_held=float(d.skill(obs, rate[:, months_held], no_link[:, months_held])),
                   best_lead3=float(d.skill(y[:, 36:], *[r[:, 36:] for r in synth.lead_rates(panel, lat, lon, seed, lead=3)])),
                   linked_share=float(linked.mean()),
                   linked_rate_share=float(no_link[linked][:, 36:].sum() / no_link[:, 36:].sum()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("panel")
    ap.add_argument("seed", type=int)
    ap.add_argument("size", choices=["sub", "full"])
    ap.add_argument("--timing", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "results" / "1b-replicates.jsonl"))
    a = ap.parse_args()
    result = replicate(a.panel, a.seed, a.size, a.timing)
    if a.timing:
        print(json.dumps(result))
    else:
        with open(a.out, "a") as f:
            f.write(json.dumps(result) + "\n")
