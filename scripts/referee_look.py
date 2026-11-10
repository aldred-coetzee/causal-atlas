"""A check after the count of Stage A1 (results/finders-stage-a1.md): the worlds with a pass that nothing planted stands behind, made again from their seeds to see what passed. It changes no count and writes nothing.

    referee_look.py
"""
import sys
from pathlib import Path

import numpy as np

from causal_atlas import referee as rf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_referee as rr  # noqa: E402

table_panel = rr.table_panel


def drift_pairs(seed, outcomes=8, local=24):
    """The two (outcome, series) pairs the generator gives one curving drift, in half the groups of places. Drawn here as synth/table_panel.py draws its layout; if that changes, this is wrong."""
    r = np.random.default_rng(np.random.SeedSequence(seed).spawn(7)[1])
    out = r.permutation(outcomes)[:2]
    r.permutation(outcomes)
    return list(zip(out.tolist(), (outcomes + r.permutation(local))[:2].tolist()))


for r in rr.rows():
    nothing = r["panel"] in rr.NOTHING
    if not (r["passed"] if nothing else any(v["passed"] for k, v in r["keen"].items() if k.endswith("other"))):
        continue
    w = table_panel.make(r["seed"], **rr.PANELS[r["panel"]][0])
    props = [p for t in w["truth"] for p in (rr.answer(t, way) for way in rr.WAYS) if p is not None]
    na, left = len(props), rr.SENT - len(props)
    props += rr.keen(w["values"], w["role"], w["group"], rr.FIRST, left - left // 2, left // 2)
    res = rf.judge(w["values"], w["group"], rr.FIRST, props, seed=r["seed"])
    assert abs(res["bar"] - r["bar"]) < 1e-9, "not the world that was counted"
    pairs = drift_pairs(r["seed"])
    print(f"\n{r['panel']} seed {r['seed']}, bar {res['bar']:.2f}; planted {[(t['outcome'], t['inputs']) for t in w['truth']]}; pairs given one drift {pairs}")
    v = w["values"]
    for p, q in zip(props[na:], res["proposals"][na:]):
        rel, inside = rr.relation(p, w["truth"], v)
        if not q["passes"] or not (rel == "other" or nothing):
            continue
        o, s = p["outcome"], p["inputs"][0][0]
        where = np.ones(v.shape[1], bool) if isinstance(p["where"], str) else np.asarray(p["where"], bool)
        near = sorted(((abs(rr._together(v[s], v[x])), x, str(w["role"][x])) for x in range(len(v)) if x != s), reverse=True)[:3]
        print(f"  {p['by']}: outcome {o}, series {s} ({w['role'][s]}), {int(where.sum())} places; t {q['fell']['t']:.2f} as it fell, {q['flat']['t']:.2f} level and line out; "
              f"share removed {100 * q['fell']['s']:.2f}% and {100 * q['flat']['s']:.2f}%; the pair shares a drift: {(o, s) in pairs}")
        print(f"     series closest to it by rank: {[(round(a, 2), x, role) for a, x, role in near]}")
        for name, sl in (("years the finders saw", slice(rf.MIN_PAST, rr.FIRST)), ("years scored", slice(rr.FIRST, None))):
            a, b = v[s][where][:, sl], v[o][where][:, sl]
            print(f"     {name}: by rank, same year {rr._together(a, b):+.2f}, series a year before {rr._together(a[:, :-1], b[:, 1:]):+.2f}, outcome a year before {rr._together(a[:, 1:], b[:, :-1]):+.2f}")
