"""Question 4: is there a trend or step in the fitting years of each field (standardised burned area and what the satellite saw)? Field mean by year, 1982-2003, its correlation with the year, and the year-to-year autocorrelation. Fitting columns only."""
import sys
import numpy as np
sys.path.insert(0, "src")
from causal_atlas import fire
yrs = np.array([j for j in range(22) if j != 12])
for f in fire.FIELDS:
    y = fire.box(f)[0][:, :264].astype(float).reshape(-1, 22, 12)
    s = fire.sight(f)[:, :264].astype(float).reshape(-1, 22, 12)
    out = []
    for nm, a in (("burned", y), ("sight", s)):
        m = a.mean(axis=(0, 2))[yrs]
        cells = a[:, yrs].mean(2)  # cells x years
        rc = np.array([np.corrcoef(c, yrs)[0, 1] for c in cells if c.std() > 0])
        out.append(f"{nm}: r(year) of field mean {np.corrcoef(m, yrs)[0, 1]:+.2f}, lag-1 autocorr {np.corrcoef(m[:-1], m[1:])[0, 1]:+.2f}, early-vs-late (82-92 vs 95-03) {m[:11].mean():+.2f}/{m[11:].mean():+.2f}, cells with |r(year)|>0.43 (p<.05): {np.mean(np.abs(rc) > 0.433):.2f}")
    print(f, "|", " | ".join(out))
