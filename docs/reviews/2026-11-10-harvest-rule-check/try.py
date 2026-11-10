"""Run one modified made-up record through the detector exactly as the real record will be run (first year 20, 62 shifts unless told), and write the verdict to my own log. Usage: try.py label seed [key=value ...] [shifts=n]"""
import json
import sys
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
sys.path.insert(0, str(here))
import panel_mod  # noqa: E402

from causal_atlas import harvest  # noqa: E402

label, seed = sys.argv[1], int(sys.argv[2])
kw, upto, shifts = {}, 6, None
for a in sys.argv[3:]:
    k, v = a.split("=")
    if k == "upto":
        upto = int(v)
    elif k == "shifts":
        shifts = range(2, 2 + int(v))
    else:
        kw[k] = v if k in ("kind", "shape") else float(v)
w = panel_mod.make(seed, **kw)
r = harvest.run(w["logy"], w["official"], w["country"], w["cereal"], w["x"], w["lat"], w["lon"], 20, upto, shifts=shifts)
v, k = harvest.reading(r), harvest.kept(r)
out = {"label": label, "seed": seed, "kw": kw, "upto": upto, "shifts": len(r["model"][0]) - 1, "passes": v["passes"],
       "model": {a: v["model"][a] for a in ("s", "ci", "beats", "excess", "excess_ci", "ok")},
       "flat": {a: v["flat"][a] for a in ("s", "ci", "beats", "excess", "excess_ci", "ok")},
       "below": all(v["below"].values()), "without_best": v["without_best"], "kept_s": k["s"], "kept_ci": k["ci"], "kept_beats": k["beats"]}
with open(here / "runs.jsonl", "a") as f:
    f.write(json.dumps(out) + "\n")
m, fl = out["model"], out["flat"]
print(label, seed, "PASS" if out["passes"] else "no", f"S {m['s']:+.4f} ci {m['ci'][0]:+.4f} beats {m['beats']} ex_ci {m['excess_ci'][0]:+.4f} ok {m['ok']} | flat S {fl['s']:+.4f} ci {fl['ci'][0]:+.4f} beats {fl['beats']} ok {fl['ok']} | below {out['below']} wb {out['without_best']:+.4f}", flush=True)
