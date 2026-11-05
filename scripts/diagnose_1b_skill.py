"""Where the first run's skill sits: seeds 1010, 1012, 1015, 1011, with a noise-column control. First-run design."""
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

TOP = 10
OUT = ROOT / "results" / "1b-diagnostic.jsonl"


def cell_deviance(y, mu):
    mu = np.maximum(mu, 1e-9)
    return 2 * (xlogy(y, y / mu) - (y - mu))


_, lat, lon = load()
for seed in (1010, 1012, 1015, 1011):
    g = synth.generate("planted_3.00", lat, lon, seed)
    y = g["y"]
    tau = np.arange(d.TRAIN[0], d.HELD[1] + 1)
    target = y[:, tau].ravel().astype(np.float32)
    in_month = np.tile(tau, len(lat))
    fit, held = in_month <= d.VALID[1], in_month >= d.HELD[0]
    base = d.base_features(y, lat, lon)
    obs = y[:, d.HELD[0] : d.HELD[1] + 1]
    b = d.fit_predict(base, target, fit, held).reshape(obs.shape)
    m = d.fit_predict(np.hstack([base, d.input_features(g["drought"], g["oni"])]), target, fit, held).reshape(obs.shape)
    noise = np.random.default_rng(seed).normal(size=(base.shape[0], 1)).astype(np.float32)
    n = d.fit_predict(np.hstack([base, noise]), target, fit, held).reshape(obs.shape)
    db, dm = cell_deviance(obs, b), cell_deviance(obs, m)
    gain = db - dm
    order = np.argsort(-np.abs(gain), axis=None)[:TOP]
    keep = np.ones(obs.shape, bool)
    keep[np.unravel_index(order, obs.shape)] = False
    top = [dict(cell=int(c), month=int(t) + d.HELD[0], obs=int(obs[c, t]), b=round(float(b[c, t]), 1), m=round(float(m[c, t]), 1),
                gain=round(float(gain[c, t]), 1))
           for c, t in zip(*np.unravel_index(order, obs.shape))]
    out = dict(seed=seed, skill=float(1 - dm.sum() / db.sum()), skill_noise_control=float(d.skill(obs, n, b)),
               skill_without_top=float(1 - dm[keep].sum() / db[keep].sum()),
               top_share_of_abs_gain=float(np.abs(gain[~keep]).sum() / np.abs(gain).sum()),
               obs_p999=float(np.quantile(obs[obs > 0], 0.999)), obs_max=int(obs.max()), b_max=float(b.max()), m_max=float(m.max()), top=top)
    with OUT.open("a") as f:
        f.write(json.dumps(out) + "\n")
