"""The same statistic as share_before.py, on the reader's made-up panels: lagged instrument (seed 20041) and same-month instrument as registered (seed 20042)."""
import sys
from pathlib import Path
import numpy as np
here = Path(__file__).resolve().parent
sys.path[:0] = [str(here), str(here.parents[2] / "scripts")]
from causal_atlas import fire, local
from run_fire import YEARS
import reader_panel
for seed, lagged in [(int(a), True) for a in sys.argv[1:]] or ((20041, True), (20042, False)):
    burned, seen, *_ , lat, lon, _ = reader_panel.make(seed, instrument=1.0, lagged=lagged)
    y, used = fire.standard(burned, seen)
    kept = used.any(axis=1)
    y, used, s, lat, lon = np.clip(y, -3, 3).reshape(len(y), -1)[kept][:, : fire.FIT], used[kept], fire.share(seen)[kept][:, : fire.FIT].astype(float), lat[kept], lon[kept]
    a = local.adjusted(y, s, used, local.blocks(lat, lon), YEARS)
    before = np.concatenate([np.zeros((len(s), 1)), s[:, :-1]], axis=1)
    m = used[:, np.arange(y.shape[1]) % 12] & (np.abs(s) < 0.5) & (y != 0)
    m[:, :12] = False; m[:, 144:157] = False
    band = np.digitize(before, local.CUTS)
    print("lagged" if lagged else "same-month", " ".join(f"{a[m & (band == b)].mean():+.3f}" for b in range(5)), f"r={np.corrcoef(a[m], before[m])[0, 1]:+.3f}")
