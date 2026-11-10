"""Leak check of my own: on a made-up record, replace every yield, every official flag and every driver month from a cut year on with noise (and some NaN), and compare everything the detector says about the years before the cut. Shifts are few, for time; the yield-only change is checked under every shift column."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path("synth").resolve()))
import harvest_panel  # noqa: E402

from causal_atlas import harvest  # noqa: E402

seed, cut = int(sys.argv[1]), int(sys.argv[2])
w = harvest_panel.make(seed, kind="link", share=0.2)
args = [w[k] for k in ("logy", "official", "country", "cereal", "x", "lat", "lon")]
SH = [2, 7, 30, 63]
a = harvest.run(*args, first=20, shifts=SH)
rng = np.random.default_rng(seed + 1)
y2, o2, x2 = w["logy"].copy(), w["official"].copy(), w["x"].copy()
y2[:, cut:] = 7 + 3 * rng.standard_normal(y2[:, cut:].shape)
y2[:, cut:][rng.random(y2[:, cut:].shape) < 0.2] = np.nan
o2[:, cut:] = rng.random(o2[:, cut:].shape) < 0.5
o2 &= np.isfinite(y2)
x2[:, 12 * (cut + 1):] = 5 * rng.standard_normal(x2[:, 12 * (cut + 1):].shape)
for label, yy, oo, xx in (("yields and flags only", y2, o2, w["x"]), ("driver only", w["logy"], w["official"], x2), ("all", y2, o2, x2)):
    b = harvest.run(yy, oo, w["country"], w["cereal"], xx, w["lat"], w["lon"], first=20, shifts=SH)
    bef = a["years"] < cut
    n = bef.sum()
    res = {
        "base": np.array_equal(a["base"][bef], b["base"][bef]),
        "alone": all(np.array_equal(a["alone"][k][bef], b["alone"][k][bef]) for k in harvest.BASELINES),
        "chosen": a["chosen"][:n] == b["chosen"][:n],
        "weights": np.array_equal(a["weights"][bef], b["weights"][bef]),
        "model as fell": np.array_equal(a["model"][bef, 0], b["model"][bef, 0]),
        "unit model as fell": np.array_equal(a["unit_model"][:, :n, 0], b["unit_model"][:, :n, 0]),
        "pick": np.array_equal(a["pick"][:, :n], b["pick"][:, :n]),
        "model all shifts": np.array_equal(a["model"][bef], b["model"][bef]),
        "flat all": np.array_equal(a["flat"][bef], b["flat"][bef]),
        "changed after": not np.array_equal(a["model"][~bef, 0], b["model"][~bef, 0]),
    }
    print(seed, cut, label, n, res, flush=True)
