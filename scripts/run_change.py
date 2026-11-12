"""The read of changes counted on made-up tables beside the read of levels. The rule and the marks are in results/change-count.md, committed before any counted seed.

    count <panel> [from to]   read a panel's tables (or its seeds from..to), each way kept once
    table                     the marks against what was kept
"""
import fcntl
import json
import sys
import warnings
from argparse import Namespace
from pathlib import Path

import numpy as np

import lab_levels as ll  # the maker's arguments, the two ways and what counts as heard

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "results" / "change-count.jsonl"
WAYS = ("asis", "change")
BASE = dict(synth=None, share=0.35, places=166, series=120, years=64, first=35, last=54, fixed=None, paths=0, path_kind="mixed", path_size=1.0, no_gaps=False, sizes="0.35,0.20,0.10", plant="none", frac=0.25, outcomes_from=None)
PANELS = {  # name: (what differs from BASE, first seed, tables)
    "nothing": ({}, 63001, 100),
    "path_1": ({"paths": 6}, 63201, 50),
    "path_2": ({"paths": 6, "path_size": 2.0}, 63301, 50),
    "links": ({"plant": "added"}, 63401, 60),
    "earlier": ({"synth": "steady", "places": 120, "series": 40, "years": 60, "last": 60}, 63501, 40),
}
NOTHING = ("nothing", "path_1", "path_2")
MOST_FALSE = {"change": 16, "either": 20}
LEAST = {0.35: 0.50, 0.20: 0.18}
MOST_OTHER = 6


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def count(panel, lo=None, hi=None):
    how, start, n = PANELS[panel]
    a = Namespace(**{**BASE, **how})
    for seed in range(start, start + n):
        if (lo and seed < lo) or (hi and seed > hi):
            continue
        done = {r["way"] for r in rows() if r["panel"] == panel and r["seed"] == seed}
        if set(WAYS) <= done:
            continue
        try:
            p, before, after, truth, paths = ll.world(a, seed)
        except ValueError as e:
            got = [{"panel": panel, "seed": seed, "way": w, "refused": str(e)} for w in WAYS if w not in done]
        else:
            got = []
            for w in WAYS:
                if w in done:
                    continue
                q, v, names, answer = ll.way(w, p, after)
                got.append({"panel": panel, "way": w, **ll.pipeline(q, v, seed, a.first, a.last, truth, names, answer, paths)})
        with OUT.open("a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            if any(x["panel"] == panel and x["seed"] == seed and x["way"] in {g["way"] for g in got} for x in rows()):
                sys.exit(f"{panel} seed {seed}: kept by another run, not kept twice")
            for g in got:
                f.write(json.dumps(g, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x)) + "\n")
        for g in got:
            print(f"{panel} {g['way']} seed {seed}: " + (g.get("refused") or f"bar {g['bar']:.2f}, {g['passed']} of {g['sent']} passed" + (f", heard {sum(x['heard'] for x in g['links'])} of {len(g['links'])}" if "links" in g else "") + f", {g['seconds']}s"), flush=True)


def interval(hit, draws=2000):
    """90% interval of a share of links heard, by tables drawn again. hit: one list of true and false for each table."""
    rng = np.random.default_rng(0)
    h, n = np.array([sum(x) for x in hit], float), np.array([len(x) for x in hit], float)
    k = rng.integers(0, len(h), (draws, len(h)))
    return np.quantile(h[k].sum(axis=1) / n[k].sum(axis=1), [0.05, 0.95])


def table():
    kept = rows()
    assert len({(r["panel"], r["seed"], r["way"]) for r in kept}) == len(kept), "a seed kept twice"
    by = {}
    for r in kept:
        if "refused" not in r:
            by.setdefault((r["panel"], r["seed"]), {})[r["way"]] = r
    both = {k: x for k, x in by.items() if set(WAYS) <= set(x)}
    false = {"asis": 0, "change": 0, "either": 0}
    for p in PANELS:
        got = [x for (q, _), x in sorted(both.items()) if q == p]
        refused = sorted({r["seed"] for r in kept if r["panel"] == p and "refused" in r})
        note = f"; refused {refused}" if refused else ""
        any_ = {w: [x[w]["passed"] > 0 for x in got] for w in WAYS}
        either = [a or c for a, c in zip(any_["asis"], any_["change"])]
        if p in NOTHING:
            for w in WAYS:
                false[w] += sum(any_[w])
            false["either"] += sum(either)
            lab = {w: sum(x[w]["passed"] > 0 and all(y["label"] for y in x[w]["passes"]) for x in got) for w in WAYS}
            print(f"{p}: {len(got)} tables; with any pass: levels {sum(any_['asis'])}, changes {sum(any_['change'])}, either {sum(either)}; of those, every pass labelled together: levels {lab['asis']}, changes {lab['change']}; a path's own pair: levels {sum(any(y['kind'] == 'path' for y in x['asis']['passes']) for x in got)}, changes {sum(any(y['kind'] == 'path' for y in x['change']['passes']) for x in got)}{note}")
            continue
        other = {w: sum(any(y["kind"] == "other" for y in x[w]["passes"]) for x in got) for w in WAYS}
        print(f"{p}: {len(got)} tables; with a pass naming nothing planted: levels {other['asis']}, changes {other['change']}" + (f" (mark for changes at most {MOST_OTHER}: {'held' if other['change'] <= MOST_OTHER else 'MISSED'})" if p == "links" else "") + note)
        for share in sorted({y["share"] for x in got for y in x["asis"]["links"]}, reverse=True):
            hit = {w: [[y["heard"] for y in x[w]["links"] if y["share"] == share] for x in got] for w in WAYS}
            hit["either"] = [[a or c for a, c in zip(u, v)] for u, v in zip(hit["asis"], hit["change"])]
            line = []
            for w, name in (("asis", "levels"), ("change", "changes"), ("either", "either")):
                h, n = sum(map(sum, hit[w])), sum(map(len, hit[w]))
                lo, hi = interval(hit[w])
                mark = f"; mark {LEAST[share]:.0%}: {'held' if h / n >= LEAST[share] else 'MISSED'}" if p == "links" and w == "change" and share in LEAST else ""
                line.append(f"{name} {h} of {n} ({h / n:.0%}, {lo:.0%} to {hi:.0%}{mark})")
            print(f"   {share:.0%}: heard by " + "; ".join(line))
    for w, name in (("change", "the read of changes"), ("either", "either read")):
        print(f"where nothing predicts, {name}: {false[w]} tables with any pass (mark at most {MOST_FALSE[w]}: {'held' if false[w] <= MOST_FALSE[w] else 'MISSED'})")
    print(f"where nothing predicts, the read of levels: {false['asis']} tables with any pass")


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    if sys.argv[1] == "count":
        count(sys.argv[2], *(int(x) for x in sys.argv[3:5]))
    elif sys.argv[1] == "table":
        table()
