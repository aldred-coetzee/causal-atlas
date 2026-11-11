"""Reader's checks on made-up tables only. Smoke seeds 47990 to 47999. Nothing here reads data/.

1. How often the confirmation rule passes on ten scored years where nothing predicts:
   one slope proposal at a time, read alone as `confirm` reads it (bar for one row).
2. Whether `marks` counts a seed twice when its row is kept twice.
"""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "synth"), str(ROOT / "scripts")]
import table_panel as tp  # noqa: E402
from causal_atlas import referee as rf  # noqa: E402
import run_stage_b as sb  # noqa: E402

SEEDS = range(47990, 48000)

# 1. chance confirmation on ten scored years
tried = passed = 0
for seed in SEEDS:
    w = tp.make(seed, "none", places=120, years=64)
    v, g = np.asarray(w["values"], float), np.asarray(w["group"])
    first = v.shape[2] - 10
    role = np.asarray(w["role"])
    outs, others = np.flatnonzero(role == "outcome"), np.flatnonzero(role != "outcome")
    rng = np.random.default_rng(seed)
    for o in outs:
        s = int(rng.choice(others))
        res = rf.judge(v, g, first, [rf.proposal(int(o), [(s, 1)])], seed=seed, labels=False)
        q = res["proposals"][0]
        tried += 1
        passed += bool(sb.confirmed(q, res["bar"]))
    print(f"seed {seed}: groups {len(np.unique(g))}, years {v.shape[2]}, scored {v.shape[2] - first}; so far {passed} of {tried} confirmed", flush=True)
print(f"chance confirmations: {passed} of {tried}")

# 2. marks with one seed kept twice and one missing
fake = [{"step": "years", "seed": s, "board": {"passed": 0}} for s in sb.SEEDS["years"][:-1]]
fake.append({"step": "years", "seed": sb.SEEDS["years"][0], "board": {"passed": 0}})
print("years runs held:", len({r["seed"] for r in fake}), "distinct of", len(sb.SEEDS["years"]), "; marks says:", sb.marks(fake)["years"])

# 3. gathered rows when an allowed series has no values in the finders' years
from causal_atlas import finders as fd  # noqa: E402
w = tp.make(47990, "none", places=120, years=64)
v = np.array(w["values"], float)
role = np.asarray(w["role"])
o = int(np.flatnonzero(role == "outcome")[0])
S = len(v)
ok = np.zeros((S, S), bool)
mine = [s for s in range(S) if role[s] != "outcome"][:6]
ok[o, mine] = True
v[mine[-1], :, :] = np.nan  # one allowed series empty
view = fd.view(v, w["group"], 35, [o], allowed=ok)
for r in fd.gathered(view, o, []):
    print(r["member"], "names", sorted(r["names"]), "barred among them:", sorted(set(r["names"]) - set(mine)))
