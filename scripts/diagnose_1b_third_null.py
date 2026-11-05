import sys, json
from pathlib import Path
import numpy as np
ROOT = Path("/home/aldred/projects/causal-atlas")
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth
from causal_atlas import detector as d, nested as n
from causal_atlas.panel import load
FIRST, LAST_TRAIN, SCORED = 36, 194, 195
_, lat, lon = load()
for seed in (9001, 2001, 9004):
    g = synth.generate("pure_null", lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    cells, T = y.shape
    tau = np.arange(FIRST, T); target = y[:, tau].ravel().astype(float); month = np.tile(tau, cells); fit = month <= LAST_TRAIN
    raw = d.fit_predict(d.base_features(y, lat, lon), target.astype(np.float32), fit, np.ones(len(target), bool)).astype(float)
    full = np.zeros((cells, T)); full[:, FIRST:] = raw.reshape(cells, len(tau))
    b = np.maximum(raw * n.level_factor(y, full, lat, lon, FIRST)[:, FIRST:].ravel(), n.FLOOR)
    where = np.repeat(np.stack([lat, lon], axis=1), len(tau), axis=0).astype(np.float32)
    plain = lambda r: np.hstack([where, np.log(r)[:, None].astype(np.float32)])
    r = n.apply_trees(plain(b), target, b, fit, 40)
    x = np.hstack([plain(r), d.input_features(drought, oni, train_months=(FIRST, LAST_TRAIN))])
    score = month >= SCORED; obs, ref = target[score].reshape(cells, -1), r[score].reshape(cells, -1)
    out = dict(seed=seed, in_sample_inputs_t100=round(float(d.skill(obs, n.apply_trees(x, target, r, score, 100)[score].reshape(cells, -1), ref)), 4))
    base = dict(n.G_SETTINGS); n.G_SETTINGS.update(max_leaf_nodes=31, min_samples_leaf=50, l2_regularization=1)
    out["in_sample_big_t300"] = round(float(d.skill(obs, n.apply_trees(x, target, r, score, 300)[score].reshape(cells, -1), ref)), 4)
    n.G_SETTINGS.clear(); n.G_SETTINGS.update(base)
    print(json.dumps(out), flush=True)
