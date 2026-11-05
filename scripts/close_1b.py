"""Close 1b: marks on the nulls, the missed planted mark, and detection by each replicate's held-out worth."""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

rows = [json.loads(line) for line in open(ROOT / "results" / "1b-replicates.jsonl")]
_, lat, lon = load()
held = d.HELD[0]
for r in rows:
    if r["panel"].startswith("planted"):
        y = synth.generate(r["panel"], lat, lon, r["seed"])["y"]
        with_link, no_link = synth.lead_rates(r["panel"], lat, lon, r["seed"], lead=3)
        r["worth_held_lead3"] = float(d.skill(y[:, held:], with_link[:, held:], no_link[:, held:]))


def interval(k, n):
    ci = binomtest(k, n).proportion_ci(method="exact")
    return [round(ci.low, 3), round(ci.high, 3)]


out = {"panels": {}}
for panel in sorted({r["panel"] for r in rows}):
    p = [r for r in rows if r["panel"] == panel]
    n = len(p)
    entry = {"n": n, "criterion_1_alone": sum(r["circular"]["first"] for r in p)}
    for scheme in ("circular", "permutation"):
        k = sum(r[scheme]["all"] for r in p)
        entry[scheme] = {"detected": k, "interval": interval(k, n)}
    shuffled = [r for r in p if r["shuffled"]]
    entry["shuffled_n"] = len(shuffled)
    entry["shift_median_largest"] = max((abs(r["shift_median"]) for r in shuffled), default=None)
    entry["perm_median_largest"] = max((abs(r["perm_median"]) for r in shuffled), default=None)
    entry["skill_median"] = float(np.median([r["skill"] for r in p]))
    out["panels"][panel] = entry
planted = [r for r in rows if r["panel"].startswith("planted")]
for floor in (0.02, 0.05):
    q = [r for r in planted if r["worth_held_lead3"] >= floor]
    k = {s: sum(r[s]["all"] for r in q) for s in ("circular", "permutation")}
    out[f"worth_at_least_{floor}"] = {"n": len(q), "detected": k, "circular_interval": interval(k["circular"], len(q)) if q else None}
    below = [r for r in planted if r["worth_held_lead3"] < floor]
    out[f"worth_below_{floor}"] = {"n": len(below), "detected_circular": sum(r["circular"]["all"] for r in below)}
out["replicates"] = [
    {k: r.get(k) for k in ("panel", "seed", "skill", "worth_held_lead3", "best_lead3", "linked_rate_share")}
    | {"circular": r["circular"]["all"], "permutation": r["permutation"]["all"]}
    for r in planted
]
(ROOT / "results" / "1b-summary.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: v for k, v in out.items() if k != "replicates"}))
