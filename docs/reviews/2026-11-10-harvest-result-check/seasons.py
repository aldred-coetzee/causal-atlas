"""Item 5/8: which of the six values carry the gain. Runs the project's forecast with the season list replaced in memory only (the file is not changed): the four values of the harvest year alone, the two of the year before alone. Also: does last September's drought explain last year's baseline error (a rebound channel)?"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
from causal_atlas import harvest
import own
p, country, cereal = common.real()
full = harvest.SEASONS
for name, ss in (("harvest year only (Mar, Jun, Sep, Dec)", full[2:]), ("year before only (Sep-1, Dec-1)", full[:2]), ("Sep-1, Dec-1, Mar, Jun (= mid-year)", full[:4]), ("Mar, Jun only", full[2:4])):
    harvest.SEASONS = ss
    r = harvest.run(p["logy"], p["official"], country, cereal, p["x"], p["lat"], p["lon"], common.FIRST, len(ss))
    m, b = r["model"], r["base"]
    s = 1 - m[:, 0].sum() / b.sum(); sh = 1 - m[:, 1:].sum(0) / b.sum()
    fs = 1 - r["flat"][:, 0].sum() / b.sum()
    print("%-42s S %.2f%% %s shift mean %.2f%% beaten %d/62 flat S %.2f%%" % (name, 100 * s, [round(100 * v, 2) for v in common.boot(m[:, 0], b, 24004)], 100 * sh.mean(), (s > sh).sum(), 100 * fs), flush=True)
harvest.SEASONS = full
# rebound channel: own mean3 error of year t-1 against Sep and Dec SPEI of year t-1 (= the Sep-1, Dec-1 values of year t), and this year's error against them
o = own.Own(p, country, cereal, "mean3")
f = own.drivers(p["x"], o.T)[country]
ok = o.target & np.isfinite(f).all(2)
prev = np.full(o.z.shape, np.nan); prev[:, 1:] = np.where(ok[:, :-1], o.z[:, :-1], np.nan)
for k, lab in ((0, "Sep-1"), (1, "Dec-1")):
    a = ok & np.isfinite(prev)
    a[:, :20] = False
    print(lab, "pooled corr with this year's error %+.3f, with last year's error %+.3f" % (np.corrcoef(o.z[a], f[:, :, k][a])[0, 1], np.corrcoef(prev[a], f[:, :, k][a])[0, 1]))
a = ok & np.isfinite(prev); a[:, :20] = False
print("this year's error vs last year's error, pooled corr %+.3f" % np.corrcoef(o.z[a], prev[a])[0, 1])
