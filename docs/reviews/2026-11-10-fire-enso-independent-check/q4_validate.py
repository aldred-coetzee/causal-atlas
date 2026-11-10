"""Check that q4_sim's split of links.both reproduces links.both itself, on a committed row (Africa, seed 17111, kind real)."""
import json, sys
import numpy as np
sys.path.insert(0, "src"); sys.path.insert(0, "docs/reviews/2026-11-10-fire-enso-independent-check")
from causal_atlas import fire, decoy
import q4_sim
y, lat, lon, _ = fire.box("africa")
d = decoy.make(17111, fire.MONTHS, fire.oni())[:, :264]
t, e = q4_sim.stats(y[:, :264].astype(np.float64), [fire.oni()[:264], *d], lat, lon)
b, s = q4_sim.gates(t, e, q4_sim.CUT)
row = next(r for r in map(json.loads, open("results/fire-enso.jsonl")) if r["kind"] == "real" and r["field"] == "africa" and r["seed"] == 17111)
print("mine", b, s, " committed", row["broad"]["leads"], row["sharp"]["leads"], " bar", round(float(np.delete(e, 0, 1)[:, [i - 1 for i in q4_sim.CUT]].max()), 3), row["sharp"]["bar"])
