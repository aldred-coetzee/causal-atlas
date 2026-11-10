"""Stage A1 (results/finders-stage-a1.md): what the rows say beside the registered table. The marks with exact intervals over worlds, the answers three ways with intervals from drawing worlds again, the keen proposals that name a planted input, sizes, bars, seconds. Reads the rows only; makes no world.

    referee_summary.py [rows file]
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import beta

ROWS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "results" / "finders-stage-a1.jsonl"
rows = [json.loads(s) for s in open(ROWS)]
NOTHING = ("none_plain", "none", "none_strong", "none_rough", "none_gaps", "same_year")
KINDS = ("steady", "threshold", "extremes", "pair", "flip", "flip_state", "many", "hidden", "shared")


def exact(k, n, level=0.95):
    a = (1 - level) / 2
    return (0.0 if k == 0 else beta.ppf(a, k, n - k + 1), 1.0 if k == n else beta.ppf(1 - a, k + 1, n - k))


def boot(per_world, draws=2000, seed=1):
    """Interval for links passed of links sent, worlds drawn again."""
    rng = np.random.default_rng(seed)
    x = np.array(per_world, float)
    idx = rng.integers(0, len(x), (draws, len(x)))
    share = x[idx, 0].sum(axis=1) / x[idx, 1].sum(axis=1)
    return np.quantile(share, [0.025, 0.975])


print("rows", len(rows), "distinct", len({(r["panel"], r["seed"]) for r in rows}))
print("\n== mark 1: worlds with any pass, where nothing predicts")
tot = 0
for p in NOTHING:
    mine = [r for r in rows if r["panel"] == p]
    k = sum(r["passed"] > 0 for r in mine)
    tot += k
    keen_t = max(max(v["largest_t"] for v in r["keen"].values()) for r in mine)
    ans = sum(a["passes"] for r in mine for a in r["answers"])
    print(f"{p:12s} {k} of {len(mine)}  interval {100*exact(k,len(mine))[0]:.1f}% to {100*exact(k,len(mine))[1]:.1f}%; passes in all {sum(r['passed'] for r in mine)}; answers passed {ans}; largest smaller-form t of a keen proposal {keen_t:.2f}; mean bar {np.mean([r['bar'] for r in mine]):.2f}; mean seconds {np.mean([r['seconds'] for r in mine]):.1f}")
n = sum(r["panel"] in NOTHING for r in rows)
print(f"all: {tot} of {n}, interval {100*exact(tot,n)[0]:.2f}% to {100*exact(tot,n)[1]:.2f}%")

print("\n== mark 2: linked worlds with a keen pass that names neither a planted input nor a near copy")
linked = [r for r in rows if r["panel"] not in NOTHING]
k = sum(any(v["passed"] for kk, v in r["keen"].items() if kk.endswith("other")) for r in linked)
print(f"{k} of {len(linked)}, interval {100*exact(k,len(linked))[0]:.2f}% to {100*exact(k,len(linked))[1]:.2f}%")
for r in linked:
    for kk, v in r["keen"].items():
        if kk.endswith("other") and v["passed"]:
            print("   ", r["panel"], r["seed"], kk, v["passed"])
sent_other = sum(v["sent"] for r in linked for kk, v in r["keen"].items() if kk.endswith("other"))
print("keen 'other' proposals sent in linked worlds:", sent_other)

print("\n== mark 3 and beside: answers, links passed of links sent (interval over worlds), middle size of all sent / of passed")
for suffix in ("35", "20", "20_wide"):
    print(f"-- {suffix}")
    for kind in KINDS:
        mine = [r for r in rows if r["panel"] == f"{kind}_{suffix}"]
        if not mine:
            continue
        cells = []
        for way in ("true", "all", "claim"):
            per = [(sum(a["passes"] for a in r["answers"] if a["way"] == way), sum(a["way"] == way for a in r["answers"])) for r in mine]
            got, sent = sum(a for a, _ in per), sum(b for _, b in per)
            if not sent:
                cells.append(f"{way}: none sent")
                continue
            lo, hi = boot(per)
            sizes = [a["size"] for r in mine for a in r["answers"] if a["way"] == way and a["size"] is not None]
            passed = [a["size"] for r in mine for a in r["answers"] if a["way"] == way and a["passes"]]
            cells.append(f"{way}: {got} of {sent} ({100*lo:.0f}% to {100*hi:.0f}%), size {100*np.median(sizes):.1f}%" + (f" / passed {100*np.median(passed):.1f}%" if passed else ""))
        print(f"{kind:11s} worlds {len(mine)}; " + "; ".join(cells) + f"; mean bar {np.mean([r['bar'] for r in mine]):.2f}; mean s {np.mean([r['seconds'] for r in mine]):.1f}")

print("\n== beside: keen proposals that name a planted input, passed of sent; share of each passed set inside the link's places (middle, and how many at least 0.8)")
for suffix in ("35", "20", "20_wide"):
    print(f"-- {suffix}")
    for kind in KINDS:
        mine = [r for r in rows if r["panel"] == f"{kind}_{suffix}"]
        out = []
        for by in ("keen-all", "keen-set"):
            for rel in ("names", "copy"):
                vs = [r["keen"][f"{by} {rel}"] for r in mine if f"{by} {rel}" in r["keen"]]
                got, sent = sum(v["passed"] for v in vs), sum(v["sent"] for v in vs)
                inside = [x for v in vs for x in v["passed_inside"]]
                out.append(f"{by} {rel} {got} of {sent}" + (f" (inside: middle {np.median(inside):.2f}, {sum(x >= 0.8 for x in inside)} of {len(inside)} at least 0.8)" if inside else ""))
        worlds_named = sum(any(r["keen"].get(f"keen-set {rel}", {}).get("passed", 0) or r["keen"].get(f"keen-all {rel}", {}).get("passed", 0) for rel in ("names",)) for r in mine)
        print(f"{kind:11s} " + "; ".join(out) + f"; worlds with a keen pass naming a planted input: {worlds_named} of {len(mine)}")

print("\ntotal seconds", sum(r["seconds"] for r in rows))
