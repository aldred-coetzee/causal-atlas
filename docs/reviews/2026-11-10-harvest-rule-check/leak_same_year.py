"""Does a year's own yield or flag reach its own forecast? Change only year `cut` (yield and flag) and compare every baseline's forecast, the scale, the choice and the driver's term at that year."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path("synth").resolve()))
import harvest_panel  # noqa: E402

from causal_atlas import harvest  # noqa: E402


def parts(y, o, w):
    s = harvest.scale(y)
    base = harvest.baselines(y, o, harvest.neighbours(w["country"], w["cereal"], w["lat"], w["lon"]))
    err = {b: np.clip((y - v) / s, -4, 4) for b, v in base.items()}
    target = o & np.all([np.isfinite(e) for e in err.values()], axis=0)
    zb = {b: np.where(target, e, 0) for b, e in err.items()}
    sq = {b: np.cumsum((v**2).sum(axis=0)) for b, v in zb.items()}
    chosen = [min(harvest.BASELINES, key=lambda b: sq[b][t - 1]) if t else harvest.BASELINES[0] for t in range(y.shape[1])]
    pools = np.stack(harvest.pooling(w["country"], w["cereal"], w["lat"], w["lon"]))
    term, wt = harvest.terms(zb, target, chosen, harvest.seasons(w["x"], y.shape[1]), w["country"], pools, 20)
    return s, base, chosen, term


w = harvest_panel.make(23002, kind="link", share=0.2)
for cut in (30, 44, 63):
    y2, o2 = w["logy"].copy(), w["official"].copy()
    y2[:, cut] += 2.0
    o2[:, cut] = ~o2[:, cut] & np.isfinite(y2[:, cut])
    a, b = parts(w["logy"], w["official"], w), parts(y2, o2, w)
    print(cut, "scale", np.array_equal(a[0][:, cut], b[0][:, cut], equal_nan=True),
          "baselines", all(np.array_equal(a[1][k][:, cut], b[1][k][:, cut], equal_nan=True) for k in a[1]),
          "chosen", a[2][cut] == b[2][cut], "term", np.array_equal(a[3][:, cut], b[3][:, cut]), flush=True)
