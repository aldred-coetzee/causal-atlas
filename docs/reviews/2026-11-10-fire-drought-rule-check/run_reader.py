"""The reader's own made-up panels, through the registered preparation and method; nothing is written to results/. Usage: run_reader.py curve|lagged AMOUNT SEED [SEED ...]"""
import sys
from pathlib import Path
import numpy as np
here = Path(__file__).resolve().parent
sys.path[:0] = [str(here), str(here.parents[2] / "scripts")]
from causal_atlas import fire, local
import run_local
from run_continents import verdict
import reader_panel

kind, amount, seeds = sys.argv[1], float(sys.argv[2]), [int(s) for s in sys.argv[3:]]
for seed in seeds:
    if kind == "curve":
        burned, seen, moisture, lat, lon, _ = reader_panel.make(seed, curve=amount)
    else:
        burned, seen, moisture, lat, lon, _ = reader_panel.make(seed, instrument=amount, lagged=True)
    y, used = fire.standard(burned, seen)
    kept = used.any(axis=1)
    y = np.clip(y, -fire.CLIP, fire.CLIP).reshape(len(y), -1)
    data = (y[kept], local.departure(moisture[kept], 0), fire.share(seen)[kept], used[kept], lat[kept], lon[kept])
    out = {}
    for k in run_local.KINDS:
        model, info, parts = run_local.scored(data, k)
        v = verdict(*parts)
        out[k] = v["passes"]
        sh = np.array(v["shifted"])
        print(f"{kind} {amount} seed {seed} {k:8s} k={info['k']:.2f} claimed={info['claimed']:6d} S={v['s']:+.4f} ci=({v['ci'][0]:+.4f},{v['ci'][1]:+.4f}) beats={v['beats']}/14 shifts mean={sh.mean():+.4f} passes={v['passes']}", flush=True)
    print(f"{kind} {amount} seed {seed} LINK={run_local.link(out)} sight={out['sight']}", flush=True)
