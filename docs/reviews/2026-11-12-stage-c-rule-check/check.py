"""Made-up arrays only. Two checks on the changed table, seeds 59001 to 59003 (smoke).
1. After the change, does a component common to all places in a year come back (the median across places of the changed departures), and how big is it beside the spread of changes across places?
2. Where a planted input is missing, the planted addition is zero in that year; as a change that is a jump. How big beside the outcome's own changes?"""
import sys
import warnings
import numpy as np
sys.path.insert(0, "scripts")
import lab_level_worlds as lw
import run_stage_c as sc

warnings.simplefilter("ignore")

def common_part(x):
    c = sc.change(x)
    med = np.nanmedian(c, axis=1)               # series by years: what is common to all places in a year, after the change
    sd = np.nanstd(c, axis=1)                    # spread across places
    r = np.nanmedian(np.abs(med[:, 1:]) / sd[:, 1:], axis=1)
    return np.nanmedian(r), np.nanpercentile(r, 90)

# (a) the count's own made-up kind
w = lw.make(59001)
print("made-up kind of the count: |year's median of changes| / spread of changes across places, middle series %.3f, 90th pct %.3f" % common_part(w["values"][~w["common"]]))

# (b) series whose places differ in level by 20 times a year's move, about a third of places entering late (as WDI series often do)
rng = np.random.default_rng(59002)
S, P, T = 50, 166, 64
lvl = 20 * rng.standard_normal((S, P, 1))
x = lvl + np.cumsum(rng.standard_normal((S, P, T)), axis=2)
late = np.where(rng.random((S, P)) < 0.33, rng.integers(1, 10, (S, P)), 0)
x[np.arange(T)[None, None, :] < late[:, :, None]] = np.nan
mid = np.nanmedian(x, axis=1)
d = x - mid[:, None, :]
print("places 20 moves apart, a third entering late: middle %.3f, 90th pct %.3f" % common_part(d))
d0 = x.copy()
print("same, levels without the year's middle taken off first, for scale: middle %.3f" % common_part(d0)[0])

# 2. the zero where the input is missing, as a change
rng = np.random.default_rng(59003)
xi = lvl[0] + np.cumsum(rng.standard_normal((P, T)), axis=1)  # an input that keeps its level
xi[rng.random((P, T)) < 0.1] = np.nan
o = np.cumsum(rng.standard_normal((P, T)), axis=1)
p = {"common": np.array([False, False]), "allowed": np.array([[False, True], [True, False]]), "group": np.repeat(np.arange(17), 10)[:P], "groups": np.arange(17)}
p["group"] = np.concatenate([p["group"], np.full(P - len(p["group"]), 16)])
import run_stage_b as sb
v = np.stack([o, xi])
# plant directly with the runner's arithmetic on one pair, share 0.35
share, LAST = 0.35, 54
early = xi[:, :LAST]
moves = np.nanstd(np.diff(early, axis=1), axis=1)
z = np.nan_to_num((xi - np.nanmean(early, axis=1, keepdims=True)) / moves[:, None])
step = np.nanstd(np.diff(o[:, :LAST], axis=1), axis=1)
add = np.zeros_like(o)
add[:, 1:] = np.sqrt(share / (1 - share)) * step[:, None] * z[:, :-1]
dadd = sc.change(add)
dx = sc.change(xi)
seam = ~np.isfinite(np.roll(dx, 1, axis=1))  # input change the year before missing: the addition's change is not what a link of changes would give
seam[:, :2] = False
ok = np.isfinite(dadd) & ~seam
print("planted addition as a change: typical size where the input is there %.2f, where the input was missing the year before %.2f (outcome's own change spread %.2f); share of outcome-years hit %.3f" % (
    np.nanmedian(np.abs(dadd[ok])), np.nanmedian(np.abs(dadd[seam & np.isfinite(dadd)])), np.nanmedian(step), (seam & np.isfinite(dadd)).mean()))
