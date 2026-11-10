"""A candidate repair, not registered: the adjusted outcome taken out by bands of this month's share observed AND then of the month before's. Usage: run_fix.py SHARE SEED [SEED ...] (lagged instrument, SHARE of a planted link)"""
import sys
from pathlib import Path
import numpy as np
here = Path(__file__).resolve().parent
sys.path[:0] = [str(here), str(here.parents[2] / "scripts")]
from causal_atlas import fire, local
import run_local
from run_continents import verdict
from run_fire import YEARS
import reader_panel

share, seeds = float(sys.argv[1]), [int(s) for s in sys.argv[2:]]
orig = run_local.outcome
def outcome(data, kind):
    if kind != "twice":
        return orig(data, kind)
    y, x, s, used, lat, lon = data
    group = local.blocks(lat, lon)
    before = np.concatenate([np.zeros((len(s), 1), s.dtype), s[:, :-1]], axis=1)
    y = local.adjusted(local.adjusted(y, s, used, group, YEARS), before, used, group, YEARS)
    return orig((y, x, s, used, lat, lon), "plain")
run_local.outcome = outcome
for seed in seeds:
    burned, seen, moisture, lat, lon, _ = reader_panel.make(seed, share=share, instrument=1.0, lagged=True)
    y, used = fire.standard(burned, seen)
    kept = used.any(axis=1)
    y = np.clip(y, -fire.CLIP, fire.CLIP).reshape(len(y), -1)
    data = (y[kept], local.departure(moisture[kept], 0), fire.share(seen)[kept], used[kept], lat[kept], lon[kept])
    for k in ("plain", "adjusted", "twice"):
        model, info, parts = run_local.scored(data, k)
        v = verdict(*parts)
        print(f"link {share} lagged seed {seed} {k:8s} k={info['k']:.2f} S={v['s']:+.4f} ci=({v['ci'][0]:+.4f},{v['ci'][1]:+.4f}) beats={v['beats']}/14 passes={v['passes']}", flush=True)
