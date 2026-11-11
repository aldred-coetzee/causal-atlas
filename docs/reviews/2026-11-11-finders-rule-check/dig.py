"""Reader's check: one row of smoke world 47925 ('none', 120 places) that stood 4.7 spreads above zero on the scored years and did not pass. What is it, and why did it not pass."""
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import run_finders as rf2  # noqa: E402
from causal_atlas import finders as fd, referee as rf  # noqa: E402
seed = int(sys.argv[1]) if len(sys.argv) > 1 else 47925
w = rf2.made({**rf2.rb.PANELS["none"][0], "places": 120}, None, seed)
v = fd.view(w["values"], w["group"], rf2.FIRST, np.flatnonzero(np.asarray(w["role"]) == "outcome"))
rows = fd.steward(fd.swarm(v))
res = rf.judge(w["values"], w["group"], rf2.FIRST, [fd.proposal(r) for r in rows], seed=seed, labels=False)
print("bar", res["bar"])
for r, q in zip(rows, res["proposals"]):
    s = [x for x, _ in r["inputs"]]
    print(r["family"], r["member"], "outcome", r["outcome"], w["role"][r["outcome"]], "series", s, [w["role"][x] for x in s], "lift", round(r["lift"], 2), "places", "all" if isinstance(r["where"], str) else int(r["where"].sum()), "passes", q["passes"])
    for f in rf.READS + rf.CHECKS:
        print("   ", f, {k: q[f][k] for k in ("t", "s", "without_best", "groups", "years", "places", "ok")})
