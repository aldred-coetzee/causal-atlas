"""Do B and M differ in level, in training as well as scored months? Seeds 1010, 1012, 1015, 1011, first-run design."""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.special import xlogy

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

OUT = ROOT / "results" / "1b-level.jsonl"


def dev(y, mu):
    mu = np.maximum(mu, 1e-9)
    return float((2 * (xlogy(y, y / mu) - (y - mu))).sum())


_, lat, lon = load()
for seed in (1010, 1012, 1015, 1011):
    g = synth.generate("planted_3.00", lat, lon, seed)
    y = g["y"]
    tau = np.arange(d.TRAIN[0], d.HELD[1] + 1)
    target = y[:, tau].ravel().astype(np.float32)
    in_month = np.tile(tau, len(lat))
    fit, held = in_month <= d.VALID[1], in_month >= d.HELD[0]
    both = fit | held
    base = d.base_features(y, lat, lon)
    X = np.hstack([base, d.input_features(g["drought"], g["oni"])])
    b = d.fit_predict(base, target, fit, both)
    m = d.fit_predict(X, target, fit, both)
    fit_part, held_part = fit[both], held[both]
    ty, hy = target[fit].astype(float), target[held].astype(float)
    tb, tm, hb, hm = b[fit_part], m[fit_part], b[held_part], m[held_part]
    out = dict(seed=seed, train_skill=1 - dev(ty, tm) / dev(ty, tb), train_total_obs=ty.sum(), train_total_b=float(tb.sum()), train_total_m=float(tm.sum()),
               held_skill=1 - dev(hy, hm) / dev(hy, hb), held_total_obs=hy.sum(), held_total_b=float(hb.sum()), held_total_m=float(hm.sum()),
               held_skill_level_matched=1 - dev(hy, hm * hy.sum() / hm.sum()) / dev(hy, hb * hy.sum() / hb.sum()),
               held_dev_b=dev(hy, hb), held_dev_m=dev(hy, hm))
    with OUT.open("a") as f:
        f.write(json.dumps(out) + "\n")
