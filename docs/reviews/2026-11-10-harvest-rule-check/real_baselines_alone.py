"""The seven baselines on the real yields alone (no drought value is read: only the country middles are used, for neighbours), 1986 to 2024, beside two of my made-up records: mean squared error per scored figure in the rule's units, how many figures are scored, and which baseline is chosen."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path("synth").resolve()))
import harvest_panel  # noqa: E402

from causal_atlas import harvest  # noqa: E402


def look(name, y, off, country, cereal, lat, lon):
    s = harvest.scale(y)
    base = harvest.baselines(y, off, harvest.neighbours(country, cereal, lat, lon))
    err = {b: np.clip((y - v) / s, -4, 4) for b, v in base.items()}
    target = off & np.all([np.isfinite(e) for e in err.values()], axis=0)
    zb = {b: np.where(target, e, 0) for b, e in err.items()}
    sq = {b: np.cumsum((v**2).sum(axis=0)) for b, v in zb.items()}
    chosen = [min(harvest.BASELINES, key=lambda b: sq[b][t - 1]) if t else "last" for t in range(y.shape[1])]
    sc = slice(25, y.shape[1])
    n = target[:, sc].sum()
    per = {b: float((zb[b][:, sc] ** 2).sum() / n) for b in harvest.BASELINES}
    clipped = float((np.abs(np.where(target, err["blend"], 0))[:, sc] >= 4).sum() / n)
    by_year = target[:, sc].sum(axis=0)
    top = np.sort((zb[chosen[40]][:, sc] ** 2).sum(axis=1))[::-1]
    print(name, "scored", int(n), "per year", int(by_year.min()), "to", int(by_year.max()), "| error per figure:", {b: round(v, 3) for b, v in per.items()},
          "| chosen 1986-2024:", sorted(set(chosen[25:])), f"| share of blend errors clipped {clipped:.3%} | share of squared error in the top 5% of records {top[: len(top) // 20].sum() / top.sum():.2f}", flush=True)


z = np.load("data/panel/real/yields.npz")
codes = z["codes"]
country = np.searchsorted(codes, z["code"])
cereal = np.array([("Wheat", "Maize (corn)", "Rice", "Barley", "Sorghum", "Millet").index(i) for i in z["item"]])
look("real", z["logy"], z["official"], country, cereal, z["lat"], z["lon"])
for seed in (23012, 23013):
    w = harvest_panel.make(seed, kind="none")
    look(f"made-up none {seed}", w["logy"], w["official"], w["country"], w["cereal"], w["lat"], w["lon"])
