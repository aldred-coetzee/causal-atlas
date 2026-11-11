"""Reader's check, question 2: do rows chosen on the early years stand above zero on the scored years more than chance would put them, in worlds where nothing predicts?
For each world: the swarm, the steward with the registered floor (the rows the count sends) and with no floor (forty rows, the lift of each known). Each set is read by the referee as the count reads it. Prints one JSON line a world: the bar, and for every row its lift, family, and its standing (t) in each read held to the bar.
Seeds 47900 to 47999 only.

    carry.py <panel> <places> <seeds...>     panel: a world where nothing predicts (none, none_strong, ...) or path_<kind>
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import run_finders as rf2  # noqa: E402
from causal_atlas import finders as fd  # noqa: E402
from causal_atlas import referee as rf  # noqa: E402

panel, places = sys.argv[1], int(sys.argv[2])
seeds = [int(s) for s in sys.argv[3:]]
assert all(47900 <= s <= 47999 for s in seeds)
how, path = {**rf2.rb.PANELS[panel][0], "places": places}, rf2.rb.PANELS[panel][1]
for seed in seeds:
    t0 = time.time()
    w = rf2.made(how, path, seed)
    v = fd.view(w["values"], w["group"], rf2.FIRST, np.flatnonzero(np.asarray(w["role"]) == "outcome"))
    board = fd.swarm(v)
    out = {"panel": panel, "places": places, "seed": seed}
    for name, floor in (("floor", fd.FLOOR), ("none", -np.inf)):
        rows = fd.steward(board, floor=floor)
        res = rf.judge(w["values"], w["group"], rf2.FIRST, [fd.proposal(r) for r in rows], seed=seed, labels=False)
        out[name] = {"bar": res["bar"], "passed": res["passed"],
                     "rows": [{"lift": round(r["lift"], 2), "family": r["family"], "member": r["member"], "places": "all" if isinstance(r["where"], str) else int(r["where"].sum()),
                               "rel": rf2.stands(r, w)[0], "t": [q[f]["t"] for f in rf.READS], "s": [q[f]["s"] for f in rf.READS], "check": q["recent"]["t"], "passes": q["passes"]}
                              for r, q in zip(rows, res["proposals"])]}
    out["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(out), flush=True)
