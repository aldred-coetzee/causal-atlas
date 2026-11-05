"""Pure null, trained on 36 to 194: what do the inputs cost on the scored window? No shuffles."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

TRAIN = (36, 194)
SCORED = (195, 434)
OUT = ROOT / "results" / "1b-null-deficit.jsonl"

_, lat, lon = load()
for seed in range(9001, 9006):
    g = synth.generate("pure_null", lat, lon, seed)
    y = g["y"]
    tau = np.arange(d.TRAIN[0], d.HELD[1] + 1)
    target = y[:, tau].ravel().astype(np.float32)
    in_month = np.tile(tau, len(lat))
    fit_rows, score_rows = in_month <= TRAIN[1], in_month >= SCORED[0]
    base = d.base_features(y, lat, lon)
    inputs = d.input_features(g["drought"], g["oni"], train_months=TRAIN)
    obs = y[:, SCORED[0] : SCORED[1] + 1]
    b = d.fit_predict(base, target, fit_rows, score_rows).reshape(obs.shape)
    out = dict(seed=seed)
    for name, cols in (("both", inputs), ("drought", inputs[:, :4]), ("oni", inputs[:, 4:])):
        m = d.fit_predict(np.hstack([base, cols]), target, fit_rows, score_rows).reshape(obs.shape)
        out[name] = float(d.skill(obs, m, b))
        out[name + "_ci"] = list(d.block_interval(obs, m, b))
    with OUT.open("a") as f:
        f.write(json.dumps(out) + "\n")
