"""Fitting years only (1982-2003), no drought: does the registered adjusted burned area still move with the share observed in the month BEFORE? Mean adjusted value by band of last month's standardised share, used cell-months with this month's share inside the middle band (so this month's share cannot explain it)."""
import sys
import numpy as np
sys.path.insert(0, "scripts")
from causal_atlas import fire, local
from run_fire import YEARS
for name in fire.FIELDS:
    y, lat, lon, used = fire.box(name)
    s = fire.sight(name)
    y, s = y[:, : fire.FIT].astype(np.float64), s[:, : fire.FIT].astype(np.float64)  # nothing after 2003 kept
    group = local.blocks(lat, lon)
    a = local.adjusted(y, s, used, group, YEARS)
    before = np.concatenate([np.zeros((len(s), 1)), s[:, :-1]], axis=1)
    m = used[:, np.arange(y.shape[1]) % 12] & (np.abs(s) < 0.5) & (y != 0)
    m[:, :12] = False
    m[:, 12 * 12 : 12 * 13] = False  # 1994
    m[:, 12 * 13] = False  # January 1995: its month before is absent
    band = np.digitize(before, local.CUTS)
    out = [f"{a[m & (band == b)].mean():+.3f} (n={int((m & (band == b)).sum())})" for b in range(5)]
    r = np.corrcoef(a[m], before[m])[0, 1]
    print(f"{name:20s} by band of last month's share: {' '.join(out)}  r={r:+.3f}")
