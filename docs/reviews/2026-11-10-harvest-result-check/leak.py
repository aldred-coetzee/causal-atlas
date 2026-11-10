"""Item 2: leak checks on the real path. From a cut year on, replace yields (with noise), flags (random) and drought (noise); check nothing for earlier years changes."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
from causal_atlas import harvest
p, country, cereal = common.real()
y0, off0, x0 = p["logy"], p["official"], p["x"]
args = lambda y, o, x, sh: harvest.run(y, o, country, cereal, x, p["lat"], p["lon"], common.FIRST, 6, shifts=sh)
sh = [2, 17, 40]
r0 = args(y0, off0, x0, sh)
base0 = harvest.baselines(y0, off0, harvest.neighbours(country, cereal, p["lat"], p["lon"]))
sc0 = harvest.scale(y0)
rng = np.random.default_rng(24003)
for cut in (34, 44, 54):  # 1995, 2005, 2015
    for what in ("yields", "drought", "both"):
        y, o, x = y0.copy(), off0.copy(), x0.copy()
        if what in ("yields", "both"):
            y[:, cut:] = np.where(np.isfinite(y[:, cut:]), y[:, cut:] + rng.normal(0, 1, y[:, cut:].shape), np.nan)
            o[:, cut:] = rng.random(o[:, cut:].shape) < 0.5
        if what in ("drought", "both"):
            x[:, 12 * (cut + 1):] = rng.normal(0, 1, x[:, 12 * (cut + 1):].shape)  # drought months of year `cut` on (x starts a year earlier)
        r = args(y, o, x, sh)
        k = cut - (common.FIRST + harvest.WARM)  # scored-year index of the cut
        d = lambda a, b: float(np.nanmax(np.abs(np.nan_to_num(a) - np.nan_to_num(b)))) if np.size(a) else 0.0
        out = {"model_as_fell": d(r["unit_model"][:, :k, 0], r0["unit_model"][:, :k, 0]),
               "model_shifts": d(r["unit_model"][:, :k, 1:], r0["unit_model"][:, :k, 1:]),
               "flat": d(r["flat"][:k], r0["flat"][:k]),
               "base": d(r["unit_base"][:, :k], r0["unit_base"][:, :k]),
               "weights": d(r["weights"][:k], r0["weights"][:k]),
               "pick": int((r["pick"][:, :k] != r0["pick"][:, :k]).sum()),
               "chosen": int(sum(a != b for a, b in zip(r["chosen"][:k], r0["chosen"][:k])))}
        if what != "drought":
            b = harvest.baselines(y, o, harvest.neighbours(country, cereal, p["lat"], p["lon"]))
            out["baselines<=cut"] = max(d(b[n][:, :cut + 1], base0[n][:, :cut + 1]) for n in b)
            out["scale<=cut"] = d(harvest.scale(y)[:, :cut + 1], sc0[:, :cut + 1])
        print(1961 + cut, what, out, flush=True)
