"""Item 2, part 2: the admission rule (30 official years over the whole record) and the flat driver (a whole-record line). Each scored with the project's run, 62 shifts on the model side; flat side included."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
from causal_atlas import harvest, yields


def score(name, y, o, ctry, cer, x, lat, lon, shifts=None):
    r = harvest.run(y, o, ctry, cer, x, lat, lon, common.FIRST, 6, shifts=shifts)
    m = r["model"]; base = r["base"]
    s = 1 - m[:, 0].sum() / base.sum(); shs = 1 - m[:, 1:].sum(0) / base.sum() if m.shape[1] > 1 else np.array([np.nan])
    fs = 1 - r["flat"][:, 0].sum() / base.sum()
    print(name, "records", len(y), "scored", r["scored"], "S %.2f%% %s" % (100 * s, [round(100 * v, 2) for v in common.boot(m[:, 0], base, 24004)]),
          "shift mean %.2f%% max %.2f%% beaten %d/%d" % (100 * np.nanmean(shs), 100 * np.nanmax(shs), (s > shs).sum(), len(shs)), "flat S %.2f%%" % (100 * fs), flush=True)


p, country, cereal = common.real()
# (a) a flat driver built from the past only: each country and calendar month, the line through that month's values in the years before, taken out
x = p["x"]; C, M = x.shape; Y = M // 12
q = x.reshape(C, Y, 12)
cf = np.full(q.shape, np.nan)
for t in range(10, Y):
    k = np.arange(t) - t  # years before, 0 is the year itself
    w = q[:, :t]
    km = k.mean(); wm = w.mean(1)
    b = ((k - km)[None, :, None] * (w - wm[:, None])).sum(1) / ((k - km) ** 2).sum()
    cf[:, t] = q[:, t] - (wm + b * (0 - km))
cf = np.nan_to_num(cf).reshape(C, M)  # the first ten years zero: before any scored or fitted year that matters? see note in report
score("causal-flat driver", p["logy"], p["official"], country, cereal, cf, p["lat"], p["lon"])
# (b) admission
t = yields.table()
keep = ~np.isin(t["m49"].astype(str), yields.TOTALS)
t = {k: v[keep] for k, v in t.items()}
key = np.char.add(np.char.add(t["m49"].astype(str), "|"), t["item"].astype(str))
names, unit = np.unique(key, return_inverse=True)
logy, off = np.full((len(names), yields.YEARS), np.nan), np.zeros((len(names), yields.YEARS), bool)
logy[unit, t["yr"]] = np.log(t["kg"]); off[unit, t["yr"]] = t["official"]
code = np.array([n.split("|")[0] for n in names]); item = np.array([n.split("|")[1] for n in names])
codes = np.unique(code)
xd, cells, mid = yields.drought(codes)
has = cells[np.searchsorted(codes, code)] > 0
early = off[:, :25].sum(1)  # official years 1961 to 1985
for name, adm in (("admit 30 over whole record (as run)", off.sum(1) >= 30), ("admit 20 over whole record", off.sum(1) >= 20), ("admit 40 over whole record", off.sum(1) >= 40),
                  ("admit 15 official years before 1986 only", early >= 15), ("admit any record with 10+ official years", off.sum(1) >= 10)):
    k = adm & has
    used = np.isin(codes, code[k])
    cs = codes[used]
    score(name, logy[k], off[k], np.searchsorted(cs, code[k]), np.array([yields.CEREALS.index(i) for i in item[k]]), xd[used], mid[used, 0], mid[used, 1])
