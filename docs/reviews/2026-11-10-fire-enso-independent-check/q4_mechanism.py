"""Question 4, the mechanism: how closely does a candidate's broad-gate value at the real alignment move with its value at the copies moved one year either way (left out since decision 0044), compared with how closely any other copy moves with its own neighbours (kept)? Real South and Southeast Asia fitting field, decoys only."""
import sys
import numpy as np
sys.path.insert(0, "src"); sys.path.insert(0, "docs/reviews/2026-11-10-fire-enso-independent-check")
from causal_atlas import fire, decoy, links
import q4_sim
y, lat, lon, used = fire.box("south_southeast_asia")
y = y[:, :264].astype(float)
ym = links.by_month(y, q4_sim.YEARS)
T = []
for seed in range(960000, 960006):
    d = decoy.make(seed, fire.MONTHS, fire.oni(), count=32)[:, :264]
    T += [links.strengths(ym, x, q4_sim.YEARS, q4_sim.ALL).sum(axis=(1, 2)) for x in d]
T = np.array(T)  # candidates x 22 rotations
z = (T - T.mean(1, keepdims=True)) / T.std(1, keepdims=True)
c = lambda a, b: np.corrcoef(z[:, a], z[:, b % 22])[0, 1]
print(f"{len(T)} decoys. corr over decoys of the broad value: real alignment with the copy one year later {c(0, 1):+.2f}, one year earlier {c(0, 21):+.2f}")
print("kept copies with their own neighbours (s, s+1), s = 2..19:", round(float(np.mean([c(s, s + 1) for s in range(2, 20)])), 2), " copies two apart:", round(float(np.mean([c(s, s + 2) for s in range(2, 19)])), 2))
