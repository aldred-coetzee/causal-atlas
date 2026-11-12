"""The monthly read counted again on made-up tables, with a pass called a lead only when its label does not say the two series move together, and with gaps and late starts in two panels. The rule and the marks are in results/monthly-lead-count.md, committed before any counted seed; decision 0068.

    count <panel> ...   read a panel's worlds, each kept once
    table               the marks against what was kept
"""
import copy
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

import lab_monthly as lm  # relation and tally: what counts as heard
import lab_monthly_worlds as mw  # the maker: numpy only
import run_monthly as rm
from causal_atlas import months

OUT = Path(__file__).resolve().parents[1] / "results" / "monthly-lead-count.jsonl"
PLACES, MONTHS, FIRST, WORLDS = rm.PLACES, rm.MONTHS, rm.FIRST, rm.WORLDS
PANELS = {  # name: (kind, what the maker is given, first seed, gaps)
    "plain": ("none", {}, 65001, False),
    "same_month": ("same_month", {"share": 0.35}, 65101, False),
    "same_month_gaps": ("same_month", {"share": 0.35}, 65201, True),
    "steady_10": ("steady", {"share": 0.10}, 65301, False),
    "steady_04": ("steady", {"share": 0.04}, 65401, False),
    "burst_10": ("burst", {"share": 0.10}, 65501, False),
    "window_10": ("window", {"share": 0.10}, 65601, False),
    "steady_10_gaps": ("steady", {"share": 0.10}, 65701, True),
}
NOTHING = ("plain", "same_month", "same_month_gaps")
LEAST = {"steady_10": 0.85, "steady_04": 0.70, "burst_10": 0.75, "window_10": 0.60, "steady_10_gaps": 0.70}
MOST_FALSE, MOST_OTHER = 9, 12


def gaps(v, seed):
    """Late starts and missing months, as real monthly series have them: a third of each series' places start up to ten years late; half lose a run of one to twelve months, three times over; three in a hundred of all months go singly."""
    rng = np.random.default_rng([seed, 7])
    v = v.copy()
    S, P, T = v.shape
    t = np.arange(T)[None, None, :]
    start = np.where(rng.random((S, P)) < 1 / 3, rng.integers(1, 121, (S, P)), 0)
    v[t < start[:, :, None]] = np.nan
    for _ in range(3):
        a, n, hit = rng.integers(0, T, (S, P)), rng.integers(1, 13, (S, P)), rng.random((S, P)) < 0.5
        v[(t >= a[:, :, None]) & (t < (a + n)[:, :, None]) & hit[:, :, None]] = np.nan
    v[rng.random(v.shape) < 0.03] = np.nan
    return v


def leads(res):
    """The referee's answer with a pass kept only where its label does not say the two move together."""
    out = copy.deepcopy(res)
    for p in out["proposals"]:
        if p["passes"] and (p.get("label") is None or p["label"]["together"]):
            p["passes"] = False
    out["passed"] = sum(bool(p["passes"]) for p in out["proposals"])
    return out


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def world(panel, seed):
    kind, how, _, holes = PANELS[panel]
    t0 = time.time()
    try:
        w = mw.make(seed, kind, places=PLACES, months=MONTHS, frac=0.5, lag=1 + seed % 6, **how)
    except ValueError as e:
        return {"panel": panel, "seed": seed, "refused": str(e)}
    v = gaps(w["values"], seed) if holes else w["values"]
    outcomes = np.flatnonzero(np.asarray(w["role"]) == "outcome")
    board, sent, res = months.read(v, w["group"], FIRST, outcomes, seed=seed)
    return {"panel": panel, "seed": seed, "lag": 1 + seed % 6, "links": len(w["truth"]), "posted": len(board), "any": lm.tally(sent, res, w["truth"]), "lead": lm.tally(sent, leads(res), w["truth"]), "seconds": round(time.time() - t0, 1)}


def count(panel):
    start = PANELS[panel][2]
    for seed in range(start, start + 99):
        kept = [r for r in rows() if r["panel"] == panel]
        if sum("refused" not in r for r in kept) >= WORLDS:
            break
        if any(r["seed"] == seed for r in kept):
            continue
        r = world(panel, seed)
        if any(x["panel"] == panel and x["seed"] == seed for x in rows()):
            sys.exit(f"{panel} seed {seed}: kept by another run, not kept twice")
        with OUT.open("a") as f:
            f.write(json.dumps(r) + "\n")
        print(f"{panel} seed {seed}: " + (r.get("refused") or f"bar {r['any']['bar']}, {r['any']['passed']} of {r['any']['sent']} passed, {r['lead']['passed']} as leads, heard as a lead {len(r['lead']['heard'])} of {r['links']}, {r['seconds']}s"), flush=True)


def table():
    kept = rows()
    assert len({(r["panel"], r["seed"]) for r in kept}) == len(kept), "a seed kept twice"
    false = 0
    for p in PANELS:
        got = [r for r in kept if r["panel"] == p and "refused" not in r]
        refused = [r["seed"] for r in kept if r["panel"] == p and "refused" in r]
        note = f", refused {refused}" if refused else ""
        if p in NOTHING:
            n = sum(r["lead"]["passed"] > 0 for r in got)
            false += n
            print(f"{p}: {len(got)} worlds, {n} with any lead ({sum(r['lead']['passed'] for r in got)} leads); with any pass {sum(r['any']['passed'] > 0 for r in got)} ({sum(r['any']['passed'] for r in got)} passes){note}")
            continue
        heard, either, links = [len(r["lead"]["heard"]) for r in got], [len(r["any"]["heard"]) for r in got], [r["links"] for r in got]
        lo, hi = rm.interval(heard, links) if got else (np.nan, np.nan)
        share = sum(heard) / max(sum(links), 1)
        by = {k: f"{sum(len(r['lead']['heard']) for r in got if r['lag'] == k)}/{sum(r['links'] for r in got if r['lag'] == k)}" for k in range(1, 7)}
        print(f"{p}: {len(got)} worlds, heard as a lead {sum(heard)} of {sum(links)} ({share:.0%}, 90% interval {lo:.0%} to {hi:.0%}; mark {LEAST[p]:.0%}: {'held' if share >= LEAST[p] else 'MISSED'}); heard by any pass {sum(either)}; by lag {by}; worlds with a lead naming nothing planted {sum(r['lead']['other'] > 0 for r in got)}, part {sum(r['lead']['part'] > 0 for r in got)}{note}")
    other = sum(r["lead"]["other"] > 0 for r in kept if r["panel"] not in NOTHING and "refused" not in r)
    print(f"where nothing predicts: {false} worlds with any lead (mark at most {MOST_FALSE}: {'held' if false <= MOST_FALSE else 'MISSED'})")
    print(f"linked worlds with a lead naming nothing planted: {other} (mark at most {MOST_OTHER}: {'held' if other <= MOST_OTHER else 'MISSED'})")


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    if sys.argv[1:2] == ["count"]:
        for panel in sys.argv[2:]:
            count(panel)
    elif sys.argv[1:2] == ["table"]:
        table()
    else:
        sys.exit(__doc__)
