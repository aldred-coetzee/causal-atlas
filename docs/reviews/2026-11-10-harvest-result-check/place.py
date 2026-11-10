"""Item 4: wrong place, right year. Each country given the drought series of a country more than 5,000 km away (random among those, five draws), and the driver with each month's cross-country mean removed. Scored with the project's run (62 shifts) and with this review's own forecast D."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
from causal_atlas import harvest
import own
p, country, cereal = common.real()
x = p["x"]; C = len(x)
d = harvest.apart(p["lat"], p["lon"])
mine = own.Own(p, country, cereal, "mean3")


def score(name, xx, upto=6):
    r = harvest.run(p["logy"], p["official"], country, cereal, xx, p["lat"], p["lon"], common.FIRST, upto)
    m, base = r["model"], r["base"]
    s = 1 - m[:, 0].sum() / base.sum(); shs = 1 - m[:, 1:].sum(0) / base.sum()
    fs = 1 - r["flat"][:, 0].sum() / base.sum(); fsh = 1 - r["flat"][:, 1:].sum(0) / base.sum()
    o = mine.run(xx)
    print(name, "upto", upto, "| project: S %.2f%% %s, shifts mean %.2f%% max %.2f%% beaten %d/62; flat S %.2f%% beaten %d/62" % (100 * s, [round(100 * v, 2) for v in common.boot(m[:, 0], base, 24004)], 100 * shs.mean(), 100 * shs.max(), (s > shs).sum(), 100 * fs, (fs > fsh).sum()),
          "| own D: S %.2f%%" % (100 * own.S(o, "D")), flush=True)


rng = np.random.default_rng(24007)
for draw in range(5):
    part = np.array([rng.choice(np.flatnonzero(d[c] > 5000)) for c in range(C)])
    print(" draw", draw, "median distance %.0f km" % np.median(d[np.arange(C), part]))
    score("distant draw %d" % draw, x[part])
ym = x - np.nanmean(x, axis=0, keepdims=True)
score("cross-country monthly mean removed", ym)
score("cross-country monthly mean removed", ym, 4)
# the removed part alone: every country given the world mean
score("world mean only", np.repeat(np.nanmean(x, axis=0, keepdims=True), C, axis=0))
