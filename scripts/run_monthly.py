"""The monthly read counted on made-up tables. The rule and the marks are in results/monthly-count.md, committed before any counted seed.

    count <panel> ...   read a panel's worlds, each kept once
    table               the marks against what was kept
"""
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

import lab_monthly as lm  # relation and tally: what counts as heard
import lab_monthly_worlds as mw  # the maker: numpy only
from causal_atlas import months

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "results" / "monthly-count.jsonl"
PLACES, MONTHS, FIRST, WORLDS = 120, 600, 360, 60
PANELS = {  # name: (kind, what the maker is given, first seed)
    "plain": ("none", {}, 62001),
    "same_month": ("same_month", {"share": 0.35}, 62101),
    "wander": ("none", {"wander": 0.3}, 62201),
    "steady_10": ("steady", {"share": 0.10}, 62301),
    "steady_04": ("steady", {"share": 0.04}, 62401),
    "burst_10": ("burst", {"share": 0.10}, 62501),
    "window_10": ("window", {"share": 0.10}, 62601),
}
NOTHING = ("plain", "same_month", "wander")
LEAST = {"steady_10": 0.90, "steady_04": 0.75, "burst_10": 0.80, "window_10": 0.70}
MOST_FALSE, MOST_OTHER = 15, 12


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def world(panel, seed):
    kind, how, _ = PANELS[panel]
    t0 = time.time()
    try:
        w = mw.make(seed, kind, places=PLACES, months=MONTHS, frac=0.5, lag=1 + seed % 6, **how)
    except ValueError as e:
        return {"panel": panel, "seed": seed, "refused": str(e)}
    outcomes = np.flatnonzero(np.asarray(w["role"]) == "outcome")
    board, sent, res = months.read(w["values"], w["group"], FIRST, outcomes, seed=seed)
    t = lm.tally(sent, res, w["truth"])
    return {"panel": panel, "seed": seed, "lag": 1 + seed % 6, "links": len(w["truth"]), "posted": len(board), **t, "seconds": round(time.time() - t0, 1)}


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
        print(f"{panel} seed {seed}: " + (r.get("refused") or f"bar {r['bar']}, {r['passed']} of {r['sent']} passed, heard {len(r['heard'])} of {r['links']}, {r['seconds']}s"), flush=True)


def interval(heard, links, draws=2000):
    rng = np.random.default_rng(0)
    heard, links = np.asarray(heard, float), np.asarray(links, float)
    k = rng.integers(0, len(heard), (draws, len(heard)))
    return np.quantile(heard[k].sum(axis=1) / links[k].sum(axis=1), [0.05, 0.95])


def table():
    kept = rows()
    assert len({(r["panel"], r["seed"]) for r in kept}) == len(kept), "a seed kept twice"
    false = 0
    for p in PANELS:
        got = [r for r in kept if r["panel"] == p and "refused" not in r]
        refused = [r["seed"] for r in kept if r["panel"] == p and "refused" in r]
        note = f", refused {refused}" if refused else ""
        if p in NOTHING:
            n = sum(r["passed"] > 0 for r in got)
            false += n
            print(f"{p}: {len(got)} worlds, {n} with any pass ({sum(r['passed'] for r in got)} passes){note}")
            continue
        heard, links = [len(r["heard"]) for r in got], [r["links"] for r in got]
        lo, hi = interval(heard, links) if got else (np.nan, np.nan)
        share = sum(heard) / max(sum(links), 1)
        by = {k: f"{sum(len(r['heard']) for r in got if r['lag'] == k)}/{sum(r['links'] for r in got if r['lag'] == k)}" for k in range(1, 7)}
        print(f"{p}: {len(got)} worlds, heard {sum(heard)} of {sum(links)} ({share:.0%}, 90% interval {lo:.0%} to {hi:.0%}; mark {LEAST[p]:.0%}: {'held' if share >= LEAST[p] else 'MISSED'}); by lag {by}; worlds with a pass naming nothing planted {sum(r['other'] > 0 for r in got)}, part {sum(r['part'] > 0 for r in got)}{note}")
    other = sum(r["other"] > 0 for r in kept if r["panel"] not in NOTHING and "refused" not in r)
    print(f"where nothing predicts: {false} worlds with any pass (mark at most {MOST_FALSE}: {'held' if false <= MOST_FALSE else 'MISSED'})")
    print(f"linked worlds with a pass naming nothing planted: {other} (mark at most {MOST_OTHER}: {'held' if other <= MOST_OTHER else 'MISSED'})")


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    if sys.argv[1] == "count":
        for panel in sys.argv[2:]:
            count(panel)
    elif sys.argv[1] == "table":
        table()
