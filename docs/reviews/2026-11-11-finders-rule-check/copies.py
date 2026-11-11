"""Reader's check, question 3: in worlds of the kind 'shared' (a link from a series common to all places), how many other series go with a planted input closely enough (ranks at 0.5 or more, the harness's COPY) that a pass naming them would be called a near copy and not counted as naming nothing planted. Seeds 47960 to 47979."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import run_finders as rf2  # noqa: E402
for kind in ("shared", "steady"):
    tot = []
    for seed in range(47960, 47980):
        w = rf2.made({"kind": kind, **rf2.rr.HOW.get(kind, {}), "share": 0.35, "places": 120}, None, seed)
        role = np.asarray(w["role"])
        n = 0
        for t in w["truth"]:
            ins = {a for a, _ in t["inputs"]}
            near = [s for s in range(len(role)) if s not in ins and role[s] != "outcome" and max(abs(rf2.rr._together(w["values"][s], w["values"][a])) for a in ins) >= rf2.rr.COPY]
            n += len(near)
            tot.append((seed, t["outcome"], sorted(ins), [(s, role[s]) for s in near]))
        print(kind, seed, n, [x[3] for x in tot[-3:]])
