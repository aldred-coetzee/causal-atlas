"""Item 6: the third of records chosen before 2005. Rebuilds the choice from the run's per-record errors, checks it against the stored list, and puts an interval on the later-half S by resampling countries; also the later-half S of the other two thirds and of the whole panel."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np, json
from causal_atlas import harvest
p, country, cereal = common.real()
rows = [json.loads(s) for s in open(os.path.join(common.ROOT, "results", "harvest-drought.jsonl"))]
for upto, var in ((6, "year_end"), (4, "mid_year")):
    r = harvest.run(p["logy"], p["official"], country, cereal, p["x"], p["lat"], p["lon"], common.FIRST, upto, shifts=[])
    b, m, pick = r["unit_base"], r["unit_model"][:, :, 0], r["pick"]
    half = 19
    able = pick[:, :half].sum(1) >= 10
    early = np.where(able, 1 - m[:, :half].sum(1) / np.maximum(b[:, :half].sum(1), 1e-12), -np.inf)
    top = np.argsort(-early)[:int(round(able.sum() / 3))]
    stored = [r_ for r_ in rows if r_["kind"] == "real" and r_["variant"] == var][0]["kept_units"]
    rest = np.setdiff1d(np.flatnonzero(able), top)
    L = lambda u: 1 - m[u, half:].sum() / b[u, half:].sum()
    print(var, "same choice as stored:", sorted(top.tolist()) == sorted(stored), "kept", len(top), "countries", len(np.unique(country[top])))
    print("  later-half S: kept %.2f%%, other ranked %.2f%%, unranked %.2f%%, whole panel %.2f%%" % (100 * L(top), 100 * L(rest), 100 * L(np.flatnonzero(~able)), 100 * L(np.arange(len(b)))))
    rng = np.random.default_rng(24008)
    cs = np.unique(country[top])
    bc = np.array([b[top][country[top] == c, half:].sum() for c in cs]); mc = np.array([m[top][country[top] == c, half:].sum() for c in cs])
    bs = [1 - mc[k].sum() / bc[k].sum() for k in (rng.integers(len(cs), size=(2000, len(cs))))]
    print("  kept later-half S, interval resampling countries: %s" % [round(100 * v, 2) for v in np.percentile(bs, [2.5, 97.5])])
    # how concentrated: share of kept later gain from top 10 countries
    g = bc - mc; o = np.argsort(-g)
    print("  share of kept later gain from its top 10 countries: %.0f%%" % (100 * g[o[:10]].sum() / g.sum()))
    # early-gain vs late-gain rank correlation among ranked
    lg = 1 - m[able, half:].sum(1) / np.maximum(b[able, half:].sum(1), 1e-12)
    from scipy.stats import spearmanr
    print("  rank correlation of a record's early gain with its later gain: %.2f" % spearmanr(early[able], lg)[0], flush=True)
