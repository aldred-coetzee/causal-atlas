"""Item 3: what carries the gain. Post-hoc sums from one run of the project's model, and re-runs with records left out."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
from causal_atlas import harvest, yields
p, country, cereal = common.real()
names = p["codes"]


def go(keep, upto=6, shifts=()):
    cs = np.unique(country[keep])
    return harvest.run(p["logy"][keep], p["official"][keep], np.searchsorted(cs, country[keep]), cereal[keep], p["x"][cs], p["lat"][cs], p["lon"][cs], common.FIRST, upto, shifts=list(shifts))


for upto, var in ((6, "year_end"), (4, "mid_year")):
    r = go(np.ones(len(country), bool), upto)
    b, m = r["unit_base"], r["unit_model"][:, :, 0]
    S = lambda u: 1 - m[u].sum() / b[u].sum()
    print("==", var, "S %.2f%%" % (100 * S(slice(None))))
    gc = np.array([(b[country == c] - m[country == c]).sum() for c in range(len(names))])
    order = np.argsort(-gc)
    print(" share of total gain (base-model) from top 10 countries: %.0f%%; from top 20: %.0f%%" % (100 * gc[order[:10]].sum() / gc.sum(), 100 * gc[order[:20]].sum() / gc.sum()))
    print(" top 10 countries:", [str(c) for c in names[order[:10]]], "gain shares", [round(100 * v / gc.sum()) for v in gc[order[:10]]])
    for n in (10, 20, 30):
        drop = np.isin(country, order[:n])
        print(" without top %d countries, post hoc S %.2f%%" % (n, 100 * S(~drop)), end="")
        rr = go(~drop, upto)
        print(", refitted S %.2f%%" % (100 * (1 - rr["unit_model"][:, :, 0].sum() / rr["unit_base"].sum())), flush=True)
    k = 0
    while S(~np.isin(country, order[:k])) > 0:
        k += 1
    print(" countries removed (largest contributors first) before post-hoc S reaches zero:", k, "of", len(names))
    for c in range(6):
        rr = go(cereal != c, upto)
        print(" without %s: post hoc S %.2f%%, refitted %.2f%%" % (yields.CEREALS[c], 100 * S(cereal != c), 100 * (1 - rr["unit_model"][:, :, 0].sum() / rr["unit_base"].sum())), flush=True)
    # years
    gy = b.sum(0) - m.sum(0)
    oy = np.argsort(-gy)
    print(" years by gain, top 5:", [int(1986 + i) for i in oy[:5]], "shares %", [round(100 * v / gy.sum()) for v in gy[oy[:5]]])
    k = 0
    while 1 - m[:, np.sort(oy[k:])].sum() / b[:, np.sort(oy[k:])].sum() > 0:
        k += 1
    print(" years removed (best first) before S reaches zero:", k, "of 39")
    print(" S without best 3 / 5 years: %.2f%% / %.2f%%" % tuple(100 * (1 - m[:, np.sort(oy[j:])].sum() / b[:, np.sort(oy[j:])].sum()) for j in (3, 5)))
    # intervals: by years (as reported), by countries, by both
    rng = np.random.default_rng(24005)
    bc = np.array([b[country == c].sum(0) for c in range(len(names))]); mc = np.array([m[country == c].sum(0) for c in range(len(names))])  # countries x years
    by_c, both = [], []
    for _ in range(2000):
        cc = rng.integers(len(names), size=len(names)); yy = rng.integers(39, size=39)
        by_c.append(1 - mc[cc].sum() / bc[cc].sum())
        both.append(1 - mc[cc][:, yy].sum() / bc[cc][:, yy].sum())
    print(" interval, years resampled: %s; countries resampled: %s; both: %s" % (common.boot(m.sum(0), b.sum(0), 24006), [round(v, 4) for v in np.percentile(by_c, [2.5, 97.5])], [round(v, 4) for v in np.percentile(both, [2.5, 97.5])]), flush=True)
