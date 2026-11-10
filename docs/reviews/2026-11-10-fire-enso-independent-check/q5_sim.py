"""Question 5: the same null test on a 50-year record (as in real-indices-2: targets years 1-49, controls 2..48 against all 49 rotations 1..49).
Pure-noise field, dense (every cell-month in use, like a drought field), on South and Southeast Asia's cell geometry; candidates: the ONI (1950-1999) and 31 decoys.
Usage: q5_sim.py FIRST_SEED N OUT.jsonl"""
import json, sys
import numpy as np
sys.path.insert(0, "src"); sys.path.insert(0, "docs/reviews/2026-11-10-fire-enso-independent-check")
from causal_atlas import links, decoy, fire, field
from causal_atlas.screen import gate
import q4_sim

NY = 50
FITN = 12 * NY
YEARS = np.arange(1, NY)
ALL = list(range(1, NY))
CUT = [s for s in ALL if s not in (1, NY - 1)]

first, n, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
_, lat, lon, _ = fire.box("south_southeast_asia")
oni = field.oni()
q4_sim.FIT = FITN
for seed in range(first, first + n):
    rng = np.random.default_rng(seed)
    # reuse the 22-year generator's shape: build NY years by stacking; the generator is written for 22 years, so draw it on a longer clock here
    k = 300
    w = rng.normal(0, 1 / 2.0, (k, 2)); ph = rng.uniform(0, 2 * np.pi, k)
    basis = np.sqrt(2 / k) * np.cos(np.c_[lat, lon * np.cos(np.radians(lat))] @ w.T + ph)
    e = rng.standard_normal((FITN, k)); a = np.zeros((FITN, k))
    for t in range(FITN):
        a[t] = (0.6 * a[t - 1] if t else 0) + e[t]
    v = (basis @ (a / a.std()).T + 0.5 * rng.standard_normal((len(lat), FITN))).reshape(len(lat), NY, 12)
    y = np.clip((v - v.mean(1, keepdims=True)) / v.std(1, keepdims=True), -3, 3).reshape(len(lat), -1)
    drivers = [oni[:FITN], *decoy.make(seed, 900, oni)[:, :FITN]]
    ym = links.by_month(y, YEARS)
    tt = np.stack([links.strengths(ym, x, YEARS, ALL).sum(axis=(1, 2)) for x in drivers])
    tm = links.by_month(links.tiles(lat, lon) @ y, YEARS)
    ee = np.stack([links.sharpest(tm, x, YEARS, ALL)[0] for x in drivers])
    r = {"mode": "noise50", "field": "south_southeast_asia", "seed": seed}
    for label, c in (("cut", CUT), ("full", ALL)):
        cols = [0] + c
        r[label] = {"broad": gate(tt[:, cols])[0], "sharp": links.step_down(ee[:, cols])[0]}
    r["argmax_broad_rot"] = int(np.argmax(((tt - tt.mean(1, keepdims=True)) / tt.std(1, ddof=1, keepdims=True)).max(0))) % 22
    r["argmax_sharp_rot"] = int(np.argmax(ee.max(0))) % 22
    with open(out, "a") as f:
        f.write(json.dumps(r) + "\n")
