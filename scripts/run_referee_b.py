"""Stage A1b of docs/plan-finders-and-referee.md: the referee counted again after the shared-curve hole (decision 0060), on fresh seeds. Three questions: does it still pass things where nothing predicts, with the pairs that share the generator's curving drift sent to it directly and with four times the places; what does it do with a slow path shared by a series and an outcome, of shapes it was not shaped on (synth/shared_paths.py); and what did closing the hole cost of what it can hear. The rule and the marks are in results/finders-stage-a1b.md, committed before any counted seed.

    run_referee_b.py smoke <panel> <seeds...>   development: prints, writes nothing; smoke seeds only
    run_referee_b.py time <panel> <seeds...>    the seconds a world takes and nothing else, for panels whose worlds are not to be looked at before the count; smoke seeds only
    run_referee_b.py count <panel> [part parts] the registered seeds of a panel, once each, a row a world
    run_referee_b.py table                      the panels against their marks
"""
import json
import os
import sys
import time
from math import comb
from pathlib import Path

import numpy as np

from causal_atlas import referee as rf

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import run_referee as rr  # noqa: E402
import shared_paths  # noqa: E402
import table_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "finders-stage-a1b.jsonl"
FIRST, SENT, WIDE = rr.FIRST, rr.SENT, rr.WIDE
SHARES = (0.25, 0.5)  # the shares of the groups of places a directly sent pair is also sent for: those where it fitted the early years best
KINDS = rr.LINKED + ("shared",)
PATHS = shared_paths.KINDS + ("mixed",)
SMOKE = range(32001, 33000)
PANELS = {  # name: (how the world is made, the kind of shared path added or None, seeds)
    "none": ({"kind": "none"}, None, range(33001, 33101)),
    "none_strong": ({"kind": "none", "nuisance": 2.0}, None, range(33101, 33201)),
    "none_plain": ({"kind": "none", "nuisance": 0.0, "rough": 0.0}, None, range(33201, 33251)),
    "none_rough": ({"kind": "none", "rough": 2.0}, None, range(33301, 33351)),
    "none_gaps": ({"kind": "none", "gaps": 0.1}, None, range(33401, 33451)),
    "same_year": ({"kind": "same_year", "share": 0.35}, None, range(33501, 33551)),
    "none_wide": ({"kind": "none", "places": WIDE}, None, range(33601, 33701)),
    "none_strong_wide": ({"kind": "none", "nuisance": 2.0, "places": WIDE}, None, range(33701, 33801)),
}
NOTHING = tuple(PANELS)  # worlds where nothing predicts: any pass at all is a false pass
for i, k in enumerate(PATHS):
    PANELS[f"path_{k}"] = ({"kind": "none"}, k, range(34001 + 100 * i, 34041 + 100 * i))
    PANELS[f"path_{k}_wide"] = ({"kind": "none", "places": WIDE}, k, range(35001 + 100 * i, 35041 + 100 * i))
for i, k in enumerate(KINDS):
    PANELS[f"{k}_35"] = ({"kind": k, **rr.HOW.get(k, {}), "share": 0.35}, None, range(36001 + 100 * i, 36031 + 100 * i))
    PANELS[f"{k}_20_wide"] = ({"kind": k, **rr.HOW.get(k, {}), "share": 0.20, "places": WIDE}, None, range(37001 + 100 * i, 37031 + 100 * i))
FORESEEN = tuple(f"path_{k}{w}" for w in ("", "_wide") for k in shared_paths.KINDS if shared_paths.FORESEEABLE[k])
HEARD = ("steady_35", "flip_35", "hidden_35")  # the kinds Stage A1 heard at 35%


def drift_pairs(seed, outcomes=8, local=24):
    """The two (outcome, series) pairs the generator gives one curving drift, in half the groups of places. Drawn here as synth/table_panel.py draws its layout; if that changes, this is wrong (tests/test_referee_b.py holds it to the generator)."""
    r = np.random.default_rng(np.random.SeedSequence(seed).spawn(7)[1])
    out = r.permutation(outcomes)[:2]
    r.permutation(outcomes)
    return list(zip(out.tolist(), (outcomes + r.permutation(local))[:2].tolist()))


def sets(values, group, o, s, first=FIRST):
    """The groups of places where series s a year before went most with outcome o over the years before `first`, its pooled way: the best quarter and the best half, as places. What a finder of where would name for the pair."""
    comp = rf.comparable(values[:, :, :first])
    groups = np.unique(group)
    member = np.array([group == g for g in groups]) * 1.0
    r, z = comp[o][:, 1:], comp[s][:, :-1]
    ok = np.isfinite(r) & np.isfinite(z)
    r, z = np.where(ok, r, 0.0), np.where(ok, z, 0.0)
    a, b, c = member @ (r * z).sum(axis=1), member @ (r * r).sum(axis=1), member @ (z * z).sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        order = np.argsort(-np.nan_to_num(np.sign(a.sum()) * a / np.sqrt(b * c), nan=-np.inf))
    return [np.isin(group, groups[order[: max(int(round(sh * len(groups))), rf.GROUPS)]]) for sh in SHARES]


def small(r):
    """What is kept of one proposal's reading: whether it passed; whether it passed the two reads held to the bar, whatever the check said; and the check's own reading."""
    return {"passes": r["passes"], "held": bool(r["mean"]["ok"] and r["line"]["ok"]), "size": r["size"], "s": [r["mean"]["s"], r["line"]["s"]], "t": [r["mean"]["t"], r["line"]["t"]],
            "check": [r["recent"]["t"], r["recent"]["s"]], "span": r["mean"]["span"], "places": r["mean"]["places"]}


def world(panel, seed):
    """One made-up world, read once, forty proposals under one bar: the answers where a link is planted, each also turned round (the outcome a year before for the series, in the link's places); the pairs that share a slow path, sent directly, where the script knows them; and keen proposals up to SENT."""
    how, path, _ = PANELS[panel]
    t0 = time.time()
    w = table_panel.make(seed, **how)
    if path:
        w = shared_paths.add(w, seed, path)
    v, group = w["values"], w["group"]
    props, tags = [], []

    def send(p, *tag):
        if p is not None:
            props.append(p)
            tags.append(tag)

    for i, t in enumerate(w["truth"]):
        for way in rr.WAYS:
            send(rr.answer(t, way), "answers", i, way)
        s = t["inputs"][0][0]
        if w["role"][s] == "local":
            send(rf.proposal(s, [(t["outcome"], 1)], where=t["places"], by="back"), "answers", i, "back")
    drift = drift_pairs(seed) if how.get("nuisance", 1.0) > 0 else []
    pairs = [(p["outcome"], p["series"], p["places"]) for p in w["paths"]] if path else [(o, s, None) for o, s in drift_pairs(seed)] if panel in NOTHING else []
    for i, (o, s, places) in enumerate(pairs):
        q, h = sets(v, group, o, s)
        for way, where in (("all", "all"), ("claim", "claim"), ("quarter", q), ("half", h)) + ((("true", places),) if places is not None else ()):
            send(rf.proposal(o, [(s, 1)], where=where, by="direct"), "direct", i, way)
        if places is not None:
            send(rf.proposal(s, [(o, 1)], where=places, by="back"), "direct", i, "back")
    left = SENT - len(props)
    keen = rr.keen(v, w["role"], group, FIRST, left - left // 2, left // 2)
    res = rf.judge(v, group, FIRST, props + keen, seed=seed)
    out = {"panel": panel, "seed": seed, "bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "answers": [], "direct": [], "keen": {}}
    for (what, i, way), r in zip(tags, res["proposals"]):
        out[what].append({"of": i, "way": way, **small(r)})
    named = {(o, s) for o, s, _ in pairs} if path else set()
    for p, r in zip(keen, res["proposals"][len(tags):]):
        rel, inside = rr.relation(p, w["truth"], v)
        pair = (p["outcome"], p["inputs"][0][0])
        rel = rel if rel != "other" else "path" if pair in named else "drift" if pair in drift else "other"
        k = out["keen"].setdefault(f"{p['by']} {rel}", {"sent": 0, "passed": 0, "held": 0})
        s = small(r)
        k["sent"], k["passed"], k["held"] = k["sent"] + 1, k["passed"] + s["passes"], k["held"] + s["held"]
    return {**out, "chosen": res["chosen"], "seconds": round(time.time() - t0, 1)}


def row(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r) + "\n").encode())
    os.close(f)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def show(r):
    def line(what):
        ways = sorted({a["way"] for a in r[what]})
        return f"{what} " + ", ".join(f"{w} {sum(a['passes'] for a in r[what] if a['way'] == w)} of {sum(a['way'] == w for a in r[what])} (held {sum(a['held'] for a in r[what] if a['way'] == w)})" for w in ways)

    print(f"{r['panel']} seed {r['seed']}: bar {r['bar']:.2f}, passed {r['passed']} of {r['sent']}; " + "; ".join([line(w) for w in ("answers", "direct") if r[w]]
          + [f"{k} {x['passed']} of {x['sent']} (held {x['held']})" for k, x in r["keen"].items()]) + f"; {r['seconds']}s", flush=True)


def keen_passes(r, *rels, key="passed"):
    return sum(x[key] for k, x in r["keen"].items() if k.split()[1] in rels)


def falsely(r):
    """Whether a world has a pass that nothing stands behind. Where nothing predicts: any pass at all. With a shared path added: any pass that does not name a path's pair (a path's pair, either way round, is counted on its own). Beside a planted link: a keen pass that names neither a planted input nor a near copy of one."""
    if r["panel"] in NOTHING:
        return r["passed"] > 0
    return keen_passes(r, "other", "drift") > 0


def by_path(r, key="passed"):
    """Whether a world has a pass, forwards, that names a pair sharing a path: sent directly in any of its ways, or by the keen proposer."""
    return any(a["passes" if key == "passed" else key] for a in r["direct"] if a["way"] != "back") or keen_passes(r, "path", key=key) > 0


def both_ways(items):
    """Of the proposals sent for the true places: how many passed, and how many of those passed turned round as well."""
    fwd = {a["of"]: a["passes"] for a in items if a["way"] == "true"}
    back = {a["of"]: a["passes"] for a in items if a["way"] == "back"}
    return sum(fwd.values()), sum(fwd[i] and back.get(i, False) for i in fwd), sum(back.values()), len(back)


def at_most(n, p=0.05, tail=0.03):
    """The count a true rate of p would exceed less than `tail` of the time in n worlds."""
    k, above = 0, 1.0 - (1 - p) ** n
    while above > tail:
        k += 1
        above -= comb(n, k) * p**k * (1 - p) ** (n - k)
    return k


def table():
    rs = rows()
    mine = {name: [r for r in rs if r["panel"] == name] for name in PANELS}
    ways = ("all", "claim", "quarter", "half")
    print("| Panel | Worlds | With any pass | Drift pairs sent directly: passes (held before the check) | Keen passes |\n|---|---|---|---|---|")
    for name in NOTHING:
        m = mine[name]
        if m:
            d = [a for r in m for a in r["direct"]]
            print(f"| {name} | {len(m)} | {sum(falsely(r) for r in m)} | {sum(a['passes'] for a in d)} of {len(d)} ({sum(a['held'] for a in d)}) | {sum(keen_passes(r, 'other', 'drift', 'names', 'copy') for r in m)} |")
    print("\n| Panel | Worlds | With a path's pair passing (held before the check) | By way: " + ", ".join(ways) + ", true places | Turned round, true places | Both ways | With any other pass |\n|---|---|---|---|---|---|---|")
    for name in PANELS:
        m = mine[name]
        if m and PANELS[name][1]:
            d = [a for r in m for a in r["direct"]]
            fwd, both, back, n = map(sum, zip(*(both_ways(r["direct"]) for r in m)))
            print(f"| {name} | {len(m)} | {sum(by_path(r) for r in m)} ({sum(by_path(r, 'held') for r in m)}) | " + ", ".join(str(sum(a["passes"] for a in d if a["way"] == w)) for w in ways + ("true",))
                  + f" of {n} each | {back} of {n} | {both} of {fwd} | {sum(falsely(r) for r in m)} |")
    print("\n| Panel | Worlds | Answer in the true places (held before the check) | for all places | by claim | Turned round | Both ways | Keen: names, copy, other | Worlds with a pass nothing stands behind |\n|---|---|---|---|---|---|---|---|---|")
    for name in PANELS:
        m = mine[name]
        if m and name not in NOTHING and not PANELS[name][1]:
            a = [a for r in m for a in r["answers"]]
            got = {w: [x for x in a if x["way"] == w] for w in rr.WAYS}
            fwd, both, back, n = map(sum, zip(*(both_ways(r["answers"]) for r in m)))
            print(f"| {name} | {len(m)} | {sum(x['passes'] for x in got['true'])} of {len(got['true'])} ({sum(x['held'] for x in got['true'])}) | " + " | ".join(f"{sum(x['passes'] for x in got[w])} of {len(got[w])}" for w in ("all", "claim"))
                  + f" | {back} of {n} | {both} of {fwd} | " + ", ".join(str(sum(keen_passes(r, k) for r in m)) for k in ("names", "copy")) + f", {sum(keen_passes(r, 'other', 'drift') for r in m)} | {sum(falsely(r) for r in m)} |")
    print()
    for label, names in (("Mark 1, each panel where nothing predicts", [(n,) for n in NOTHING]), ("Mark 1, the eight together", [NOTHING]), ("Mark 2, foreseeable paths, 120 places", [FORESEEN[:3]]), ("Mark 2, foreseeable paths, 480 places", [FORESEEN[3:]]),
                         ("Mark 3, other passes beside a path", [tuple(n for n in PANELS if PANELS[n][1])]), ("Mark 3, other passes beside a link", [tuple(n for n in PANELS if n not in NOTHING and not PANELS[n][1])])):
        for group in names:
            m = [r for n in group for r in mine[n]]
            n = sum(len(PANELS[g][2]) for g in group)
            got = sum(by_path(r) for r in m) if label.startswith("Mark 2") else sum(falsely(r) for r in m)
            print(f"{label}{' ' + group[0] if len(group) == 1 else ''}: {got} of {len(m)} read ({n} registered), at most {at_most(n)}")
    for name in HEARD:
        a = [a for r in mine[name] for a in r["answers"] if a["way"] == "true"]
        print(f"Mark 4, {name}: {sum(x['passes'] for x in a)} of {len(a)}, at least 72 of 90")


if __name__ == "__main__":
    assert rf.READS == ("mean", "line") and rf.CHECKS == ("recent",), "the referee as decision 0060 left it"
    cmd = sys.argv[1]
    if cmd in ("smoke", "time"):
        panel, seeds = sys.argv[2], [int(s) for s in sys.argv[3:]]
        assert all(s in SMOKE for s in seeds), "smoke seeds only"
        assert cmd == "time" or not PANELS[panel][1], "the shapes of synth/shared_paths.py are not looked at before the count: time only"
        for seed in seeds:
            r = world(panel, seed)
            show(r) if cmd == "smoke" else print(f"{panel} seed {seed}: sent {r['sent']}, {r['seconds']}s", flush=True)
    elif cmd == "count":
        panel = sys.argv[2]
        part, parts = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 3 else (0, 1)
        done = {(r["panel"], r["seed"]) for r in rows()}
        for seed in list(PANELS[panel][2])[part::parts]:
            if (panel, seed) in done:
                print(f"{panel} seed {seed}: already read, not read again", flush=True)
                continue
            r = world(panel, seed)
            row(r)
            show(r)
    elif cmd == "table":
        table()
