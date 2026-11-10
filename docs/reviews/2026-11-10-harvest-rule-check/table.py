"""Recompute the step 1 table from the rows, and look at how the real alignment ranks among the shifts on records with no link."""
import json
from collections import defaultdict

import numpy as np

rows = [json.loads(s) for s in open("results/harvest-drought.jsonl")]
g = defaultdict(list)
for r in rows:
    g[r["panel"], r["variant"]].append(r)
for (p, v), rs in sorted(g.items()):
    s = np.array([r["s"] for r in rs])
    seeds = sorted(r["seed"] for r in rs)
    print(f"{p:8s} {v:9s} n={len(rs):2d} seeds {seeds[0]}-{seeds[-1]} pass={sum(r['passes'] for r in rs):2d} S min/med/max {s.min():+.4%} {np.median(s):+.4%} {s.max():+.4%}"
          f" model.ok={sum(r['model']['ok'] for r in rs)} flat.ok={sum(r['flat']['ok'] for r in rs)} kept clear={sum(r['kept']['ci'][0] > 0 and r['kept']['beats'] == r['kept']['shifts'] for r in rs)}")
print()
print("No-link panels: shifts beaten by the real alignment (uniform 0..62 expected if shifts are a fair null)")
for v in ("year_end", "mid_year"):
    for name in ("model", "flat"):
        b = np.array([r[name]["beats"] for r in rows if r["panel"] in ("none", "drift", "step") and r["variant"] == v])
        ex = np.array([r[name]["excess"] for r in rows if r["panel"] in ("none", "drift", "step") and r["variant"] == v])
        sm = np.array([r[name]["s"] - r[name]["shift_mean"] for r in rows if r["panel"] in ("none", "drift", "step") and r["variant"] == v])
        print(v, name, "n", len(b), "mean beats", b.mean().round(1), "(31 expected)", "share beating >=59:", (b >= 59).mean().round(3), "(~0.08 expected)",
              "beats all:", (b == 62).sum(), "| S minus mean shift S: mean", f"{sm.mean():+.5f}", "sd", f"{sm.std():.5f}", "share >0", (sm > 0).mean().round(2))
    for p in ("none", "drift", "step"):
        b = np.array([r["model"]["beats"] for r in rows if r["panel"] == p and r["variant"] == v])
        print("   ", p, sorted(b.tolist()))
