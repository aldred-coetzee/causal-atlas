"""Rebuild the made-up table of results/crops-drought.md from the rows, and say which condition decided each failure."""
import json, sys
from collections import defaultdict
import numpy as np
rows = [json.loads(s) for s in open(sys.argv[1]) if s.strip()]
FEW = (30, 15)
def why(v):
    out = []
    for name in ("model", "flat"):
        q = v[name]
        if not (q["records"] >= FEW[0] and q["countries"] >= FEW[1]): out.append(name + ":few")
        if not q["ci"][0] > 0: out.append(name + ":ci")
        if q["beats"] != q["shifts"]: out.append(name + ":beats%d" % q["beats"])
        if not q["without_best"] > 0: out.append(name + ":wobest")
        if not all(q["below"].values()): out.append(name + ":below[" + ",".join(k for k, b in q["below"].items() if not b) + "]")
    return out
g = defaultdict(list)
for r in rows:
    if r["kind"] == "made_up": g[r["panel"], r["variant"]].append(r)
eq = tot = 0
for (p, v), rs in g.items():
    s = sorted(r["levels"]["1.5"]["model"]["s"] for r in rs)
    nread = sum(r["passes"] for r in rs)
    print(f"{p:10s} {v:9s} n={len(rs):2d} read={nread:2d} S model median={np.median(s)*100:.2f}% min={s[0]*100:.2f}% max={s[-1]*100:.2f}%",
          " levels read 1.0/1.5/2.0:", [sum(r["levels"][k]["passes"] for r in rs) for k in ("1.0", "1.5", "2.0")])
    for r in sorted(rs, key=lambda r: r["seed"]):
        L = r["levels"]["1.5"]
        lo = min(L["model"]["ci"][0], L["flat"]["ci"][0])
        w = why(L)
        tag = "READ" if r["passes"] else "no"
        if r["passes"] != (not w): print("  MISMATCH", r["seed"])
        if (r["passes"] and lo < 0.002) or (not r["passes"] and len(w) == 1) or p not in ("leak","leak_drift","leak_step","none","full_leak"):
            print(f"   {r['seed']} {tag:4s} S={L['model']['s']*100:.2f}/{L['flat']['s']*100:.2f} lo={L['model']['ci'][0]*100:.2f}/{L['flat']['ci'][0]*100:.2f} rec={L['model']['records']} ctry={L['model']['countries']} beats={L['model']['beats']}/{L['flat']['beats']} word={r['word']} fails={w}")
        for k in ("1.0","1.5","2.0"):
            for d in ("model","flat"):
                tot += 1; eq += abs(r["levels"][k][d]["s"]-r["levels"][k][d]["unscaled"])<1e-9
print("S equals unscaled S in", eq, "of", tot, "readings")
