"""Question 4: which kinds of decoy the step 1 false alarms named, by gate (decoy i: i % 3 = 0 a surrogate of the ONI's spectrum, 1 an AR(1), 2 a noisy 2-7 year cycle), and the AR(1) persistence of those named."""
import json, sys
from collections import Counter
import numpy as np
sys.path.insert(0, "src")
from causal_atlas import decoy, fire
R = [json.loads(s) for s in open("results/fire-enso.jsonl")]
names = {0: "surrogate", 1: "AR(1)", 2: "cycle"}
for kind in ("real", "years_mixed"):
    for gate in ("broad", "sharp"):
        c = Counter(names[(l - 1) % 3] for r in R if r["kind"] == kind for l in r[gate]["leads"] if l > 0)
        print(kind, gate, dict(c))
# persistence of named AR(1) decoys: refit phi from the series
phis = []
for r in R:
    if r["kind"] in ("real", "years_mixed"):
        for l in r["leads"]:
            if l > 0 and (l - 1) % 3 == 1:
                x = decoy.make(r["seed"], fire.MONTHS, fire.oni())[l - 1]
                phis.append(round(float(np.corrcoef(x[:-1], x[1:])[0, 1]), 2))
print("lag-1-month autocorrelation of the named AR(1) decoys:", sorted(phis), " (drawn uniformly from 0.5 to 0.98)")
