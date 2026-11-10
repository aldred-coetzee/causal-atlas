"""Stage A1c of docs/plan-finders-and-referee.md: the label a pass carries, counted on fresh seeds. The second count (results/finders-stage-a1b.md) showed that the referee passes a series and an outcome that only move slowly together. Decision 0061 gives each pass a label, "may be moving together", when it also stands turned round or is as strong in the same year. Two questions: of the passes that are a shared slow path, how many go unlabelled; and of the passes that are a planted lead, how many are labelled. At three sizes of table, the middle one near the real table's. The rule and the marks are in results/finders-stage-a1c.md, committed before any counted seed.

    run_referee_c.py smoke <panel> <seeds...>   development: prints, writes nothing; smoke seeds only
    run_referee_c.py count <panel> [part parts] the registered seeds of a panel, once each, a row a world
    run_referee_c.py table                      the panels against their marks
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

from causal_atlas import referee as rf

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import run_referee as rr  # noqa: E402
import run_referee_b as rb  # noqa: E402
import shared_paths  # noqa: E402
import table_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "finders-stage-a1c.jsonl"
FIRST, SENT, SMOKE = rb.FIRST, rb.SENT, rb.SMOKE
SIZES = ((120, 0.35), (240, 0.35), (480, 0.20))  # places, and the share a link has at that size; the real yearly table has 218 places
BESIDE = (("steady", "cycle"), ("steady", "wander"), ("hidden", "wander"))  # a kind of link, and the shape of slow path its first link's outcome and series are also given
PANELS = {}  # name: (how the world is made, the kind of shared path added or None, the shape put beside the first link or None, seeds)
for j, (places, share) in enumerate(SIZES):
    for i, k in enumerate(rb.PATHS):
        PANELS[f"path_{k}_{places}"] = ({"kind": "none", "places": places}, k, None, range(38001 + 1000 * j + 100 * i, 38031 + 1000 * j + 100 * i))
    for i, k in enumerate(rb.KINDS):
        PANELS[f"{k}_{places}"] = ({"kind": k, **rr.HOW.get(k, {}), "share": share, "places": places}, None, None, range(41001 + 1000 * j + 100 * i, 41021 + 1000 * j + 100 * i))
    for i, (k, shape) in enumerate(BESIDE):
        PANELS[f"{k}+{shape}_{places}"] = ({"kind": k, "share": share, "places": places}, None, shape, range(44001 + 1000 * j + 100 * i, 44016 + 1000 * j + 100 * i))


def beside(w, seed, shape):
    """A slow path of one of the helper's shapes given to the first planted link's own outcome and series, in the link's places: a lead and a shared path in one pair. This session's composition, from synth/shared_paths.py's makers."""
    t = w["truth"][0]
    o, s = t["outcome"], t["inputs"][0][0]
    where = np.flatnonzero(t["places"])
    r = np.random.default_rng([seed, 4242])
    unit, _ = shared_paths._paths(r, where, shape, w["values"].shape[2])
    size = shared_paths._sizes(r, len(where))[:, None] * unit
    new = w["values"].copy()
    new[o, where] += shared_paths._spread(w["values"][o, where])[:, None] * size
    new[s, where] += r.choice([-1, 1]) * shared_paths._spread(w["values"][s, where])[:, None] * size
    return {**w, "values": new}


def small(r):
    """What is kept of one proposal's reading: whether it passed, and if it did, its label."""
    lb = r["label"]
    if lb is None:
        return {"passes": False}
    return {"passes": True, "together": lb["together"], "back": lb["back"], "same": lb["same"], "t": lb["t"], "back_t": max(lb["back_t"], default=None), "same_t": lb["same_t"]}


def world(panel, seed):
    """One made-up world, read once, forty proposals under one bar: the answers where a link is planted; the pairs that share a slow path, sent directly; and keen proposals up to SENT. Every pass carries the referee's label."""
    how, path, shape, _ = PANELS[panel]
    t0 = time.time()
    w = table_panel.make(seed, **how)
    if path:
        w = shared_paths.add(w, seed, path)
    if shape:
        w = beside(w, seed, shape)
    v, group = w["values"], w["group"]
    props, tags = [], []
    for i, t in enumerate(w["truth"]):
        for way in rr.WAYS:
            p = rr.answer(t, way)
            if p is not None:
                props.append(p)
                tags.append(("answers", i, way))
    pairs = [(p["outcome"], p["series"], p["places"]) for p in w["paths"]] if path else []
    for i, (o, s, places) in enumerate(pairs):
        q, h = rb.sets(v, group, o, s)
        for way, where in (("all", "all"), ("claim", "claim"), ("quarter", q), ("half", h), ("true", places)):
            props.append(rf.proposal(o, [(s, 1)], where=where, by="direct"))
            tags.append(("direct", i, way))
    left = SENT - len(props)
    keen = rr.keen(v, w["role"], group, FIRST, left - left // 2, left // 2)
    res = rf.judge(v, group, FIRST, props + keen, seed=seed)
    out = {"panel": panel, "seed": seed, "bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "answers": [], "direct": [], "keen": []}
    for (what, i, way), r in zip(tags, res["proposals"]):
        out[what].append({"of": i, "way": way, **small(r)})
    named = {(o, s) for o, s, _ in pairs}
    first = (w["truth"][0]["outcome"], w["truth"][0]["inputs"][0][0]) if shape else None
    for p, r in zip(keen, res["proposals"][len(tags):]):
        if r["passes"]:
            rel, _ = rr.relation(p, w["truth"], v)
            pair = (p["outcome"], p["inputs"][0][0])
            out["keen"].append({"rel": "path" if pair in named else "beside" if pair == first else rel, "by": p["by"], **small(r)})
    return {**out, "seconds": round(time.time() - t0, 1)}


def row(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r) + "\n").encode())
    os.close(f)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def passes(r, kind):
    """A world's passes of one kind. path: a pair sharing a path, sent directly or by the keen proposer. lead: a planted link, by its answer in any way or a keen proposal naming a planted input; where a path was put beside the first link, that link's are left out. beside: the first link's, where a path was put beside it."""
    shape = PANELS[r["panel"]][2]
    if kind == "path":
        return [a for a in r["direct"] if a["passes"]] + [a for a in r["keen"] if a["rel"] == "path"]
    if kind == "beside":
        return [a for a in r["answers"] if a["passes"] and a["of"] == 0 and shape] + [a for a in r["keen"] if a["rel"] == "beside"]
    return [a for a in r["answers"] if a["passes"] and not (a["of"] == 0 and shape)] + [a for a in r["keen"] if a["rel"] == "names"]


def show(r):
    print(f"{r['panel']} seed {r['seed']}: bar {r['bar']:.2f}, {r['passed']} of {r['sent']} passed, {r['seconds']}s; " + "; ".join(
        f"{k}: {len(passes(r, k))} passed, {sum(a['together'] for a in passes(r, k))} labelled" for k in ("path", "lead", "beside") if passes(r, k)), flush=True)


def tally(m, kind):
    """Worlds with a pass of the kind; with one unlabelled; with one labelled; and the passes: all, labelled, by turning round, by the same year."""
    ps = [passes(r, kind) for r in m]
    flat = [a for p in ps for a in p]
    return (sum(bool(p) for p in ps), sum(any(not a["together"] for a in p) for p in ps), sum(any(a["together"] for a in p) for p in ps),
            len(flat), sum(a["together"] for a in flat), sum(bool(a["back"]) for a in flat), sum(a["same"] for a in flat))


def table():
    rs = rows()
    mine = {name: [r for r in rs if r["panel"] == name] for name in PANELS}
    head = "| Panel | Worlds | with a pass | with one unlabelled | with one labelled | Passes | labelled | by turning round | by the same year |\n|---|---|---|---|---|---|---|---|---|"
    for title, kind, use in (("A shared slow path", "path", lambda n: PANELS[n][1]), ("A planted lead", "lead", lambda n: not PANELS[n][1]), ("A lead and a path in one pair", "beside", lambda n: PANELS[n][2])):
        print(f"\n{title}\n\n{head}")
        for name in PANELS:
            if mine[name] and use(name):
                print(f"| {name} | {len(mine[name])} | " + " | ".join(str(x) for x in tally(mine[name], kind)) + " |")
    print("\n| Panel | Answers in the link's own places passed | for all places | by claim |\n|---|---|---|---|")
    for name in PANELS:
        if mine[name] and not PANELS[name][1] and not PANELS[name][2]:
            a = [a for r in mine[name] for a in r["answers"]]
            print(f"| {name} | " + " | ".join(f"{sum(x['passes'] for x in a if x['way'] == w)} of {sum(x['way'] == w for x in a)}" for w in rr.WAYS) + " |")
    print()
    for places, _ in SIZES:
        for label, kind, which, use in (("Mark 1, a path's pass left unlabelled", "path", 1, lambda n: PANELS[n][1]), ("Mark 2, a lead's pass labelled", "lead", 2, lambda n: not PANELS[n][1] and not PANELS[n][2])):
            names = [n for n in PANELS if n.endswith(f"_{places}") and use(n)]
            m = [r for n in names for r in mine[n]]
            n = sum(len(PANELS[g][3]) for g in names)
            print(f"{label}, {places} places: {tally(m, kind)[which]} of {len(m)} worlds read ({n} registered), at most {rb.at_most(n)}")


if __name__ == "__main__":
    assert rf.READS == ("mean", "line") and rf.CHECKS == ("recent",) and rf.BACK == 2.0, "the referee as decisions 0060 and 0061 left it"
    cmd = sys.argv[1]
    if cmd == "smoke":
        panel, seeds = sys.argv[2], [int(s) for s in sys.argv[3:]]
        assert all(s in SMOKE for s in seeds), "smoke seeds only"
        for seed in seeds:
            show(world(panel, seed))
    elif cmd == "count":
        panel = sys.argv[2]
        part, parts = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 3 else (0, 1)
        done = {(r["panel"], r["seed"]) for r in rows()}
        for seed in list(PANELS[panel][3])[part::parts]:
            if (panel, seed) in done:
                print(f"{panel} seed {seed}: already read, not read again", flush=True)
                continue
            r = world(panel, seed)
            row(r)
            show(r)
    elif cmd == "table":
        table()
