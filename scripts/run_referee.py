"""Stage A1 of docs/plan-finders-and-referee.md: tests of the test. The referee on made-up tables, with two proposers that stand in for finders: the answer, which is told the planted link, and a keen one, which sends whatever fitted the early years best. The rule and the marks are in results/finders-stage-a1.md, committed before any counted seed.

    run_referee.py smoke <panel> <seeds...>    development: prints, writes nothing; seeds from the smoke range only
    run_referee.py count <panel> [part parts]  the registered seeds of a panel, once each, a row a world
    run_referee.py table                       the panels against their marks
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

from causal_atlas import referee as rf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import table_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "finders-stage-a1.jsonl"
FIRST = 35  # the first year the referee scores: finders see years 0 to 34 of 60
SENT = 40  # proposals a world, the answers among them
SET = 0.25  # the share of the groups of places in a set the keen proposer names
COPY = 0.5  # a keen proposal's series counts as a near copy of a planted input when their ranks, each place's middle value taken off, go together at least this closely over the whole table
WIDE = 480  # places in the wide worlds, four times the usual: what more places would hear
WAYS = ("true", "all", "claim")  # where an answer is sent: the places the link is in; all places; by each place's own past
LINKED = ("steady", "threshold", "extremes", "pair", "flip", "flip_state", "many", "hidden")
HOW = {"flip_state": {"kind": "flip", "flip": "state"}, "shared": {"kind": "steady", "source": "shared"}}
PANELS = {  # name: (how the world is made, seeds)
    "none_plain": ({"kind": "none", "nuisance": 0.0, "rough": 0.0}, range(28001, 28101)),
    "none": ({"kind": "none"}, range(28101, 28201)),
    "none_strong": ({"kind": "none", "nuisance": 2.0}, range(28201, 28301)),
    "none_rough": ({"kind": "none", "rough": 2.0}, range(28301, 28401)),
    "none_gaps": ({"kind": "none", "gaps": 0.1}, range(28401, 28501)),
    "same_year": ({"kind": "same_year", "share": 0.35}, range(28501, 28601)),
}
for i, k in enumerate(LINKED + ("shared",)):
    PANELS[f"{k}_35"] = ({"kind": k, **HOW.get(k, {}), "share": 0.35}, range(29001 + 100 * i, 29031 + 100 * i))
    PANELS[f"{k}_20"] = ({"kind": k, **HOW.get(k, {}), "share": 0.20}, range(30001 + 100 * i, 30031 + 100 * i))
    PANELS[f"{k}_20_wide"] = ({"kind": k, **HOW.get(k, {}), "share": 0.20, "places": WIDE}, range(31001 + 100 * i, 31031 + 100 * i))
NOTHING = ("none_plain", "none", "none_strong", "none_rough", "none_gaps", "same_year")  # worlds where nothing predicts
SMOKE = range(27001, 27100)


def answer(t, way):
    """The planted link as a proposal, in the form its kind calls for. A same-year link is sent a year ahead, where it has nothing to say."""
    ins = [(s, max(lag, 1)) for s, lag in t["inputs"]]
    kind, kw = t["kind"], {}
    if kind == "threshold":
        form, kw = "hinge", {"level": t.get("quantile", 0.8)}
    elif kind == "extremes":
        form, kw = "tail", {"level": t.get("quantile", 0.9)}
    elif kind == "pair":
        form = "product"
    elif kind == "flip" and "sign" in t:
        form, kw = "by_group", {"groups": (t["sign"] > 0).astype(int)}
    elif kind == "flip":
        form, kw = "by_state", {"state": (t["state"], 1)}
    elif kind == "many":
        form = "mode"
    else:
        form = "slope"
    if way == "claim" and form in ("by_group", "by_state"):
        return None  # by claim is for a single term
    return rf.proposal(t["outcome"], ins, form, {"true": t["places"], "all": "all", "claim": "claim"}[way], by="answer", **kw)


def keen(values, role, group, first, n_all, n_set):
    """What a keen finder would send, from the years before `first` alone: for every outcome and every other series a year before, the slopes that fitted best over all places; and the slopes that fitted best in the quarter of the groups of places where each went most its pooled way. Nothing here knows what was planted."""
    comp = rf.comparable(values[:, :, :first])
    groups = np.unique(group)
    size = max(int(round(SET * len(groups))), rf.GROUPS)
    member = np.array([group == g for g in groups]) * 1.0
    everywhere, somewhere = [], []
    for o in np.flatnonzero(role == "outcome"):
        r = comp[o][:, 1:]
        for s in range(len(values)):
            if s == o:
                continue
            z = comp[s][:, :-1]
            ok = np.isfinite(r) & np.isfinite(z)
            rr, zz = np.where(ok, r, 0.0), np.where(ok, z, 0.0)
            a, b, c = member @ (rr * zz).sum(axis=1), member @ (rr * rr).sum(axis=1), member @ (zz * zz).sum(axis=1)
            with np.errstate(divide="ignore", invalid="ignore"):
                everywhere.append((abs(a.sum()) / np.sqrt(b.sum() * c.sum()), o, s))
                by_group = np.nan_to_num(np.sign(a.sum()) * a / np.sqrt(b * c), nan=-np.inf)
                top = np.argsort(-by_group)[:size]
                somewhere.append((abs(a[top].sum()) / np.sqrt(b[top].sum() * c[top].sum()), o, s, tuple(top)))
    everywhere.sort(reverse=True)
    somewhere.sort(reverse=True)
    out = [rf.proposal(o, [(s, 1)], by="keen-all") for _, o, s in everywhere[:n_all]]
    return out + [rf.proposal(o, [(s, 1)], where=np.isin(group, groups[list(top)]), by="keen-set") for _, o, s, top in somewhere[:n_set]]


def relation(p, truth, values):
    """How a keen proposal stands to what was planted on its outcome: it names a planted input; its series is a near copy of one; or neither. And, where it names a set of places, the share of that set the link is in."""
    o, s = p["outcome"], p["inputs"][0][0]
    out, inside = "other", None
    for t in truth:
        if t["outcome"] != o:
            continue
        if not isinstance(p["where"], str):
            inside = float((np.asarray(p["where"], bool) & t["places"]).sum() / np.asarray(p["where"], bool).sum())
        ins = [a for a, _ in t["inputs"]]
        if s in ins:
            return "names", inside
        if max(abs(_together(values[s], values[a])) for a in ins) >= COPY:
            out = "copy"
    return out, inside


def _together(a, b):
    """How closely two series go together, by rank, each place's middle value taken off: a spike in one does not hide a copy."""
    a, b = a - np.nanmedian(a, axis=1, keepdims=True), b - np.nanmedian(b, axis=1, keepdims=True)
    ok = np.isfinite(a) & np.isfinite(b)
    ra, rb = np.argsort(np.argsort(a[ok])), np.argsort(np.argsort(b[ok]))
    return float(np.corrcoef(ra, rb)[0, 1])


def world(panel, seed):
    """One made-up world, read once: the answers, where there is one, and keen proposals up to SENT, under one bar."""
    how = PANELS[panel][0]
    t0 = time.time()
    w = table_panel.make(seed, **how)
    props, tags = [], []
    for i, t in enumerate(w["truth"]):
        for way in WAYS:
            p = answer(t, way)
            if p is not None:
                props.append(p)
                tags.append((i, way))
    left = SENT - len(props)
    props += keen(w["values"], w["role"], w["group"], FIRST, left - left // 2, left // 2)
    res = rf.judge(w["values"], w["group"], FIRST, props, seed=seed)

    def small(r):
        return {"passes": r["passes"], "size": r["size"], "s": [r["fell"]["s"], r["flat"]["s"]], "t": [r["fell"]["t"], r["flat"]["t"]], "span": r["fell"]["span"],
                "without_best": r["fell"]["without_best"], "plain": r["fell"]["plain"], "place_years": r["fell"]["place_years"], "places": r["fell"]["places"]}

    answers = [{"link": i, "way": way, **small(r)} for (i, way), r in zip(tags, res["proposals"])]
    kept = {}
    for p, r in zip(props[len(tags):], res["proposals"][len(tags):]):
        rel, inside = relation(p, w["truth"], w["values"])
        k = kept.setdefault(f"{p['by']} {rel}", {"sent": 0, "passed": 0, "largest_t": 0.0, "largest_either": 0.0, "passed_inside": []})
        ts = [r["fell"]["t"] or 0.0, r["flat"]["t"] or 0.0]
        k["sent"], k["passed"] = k["sent"] + 1, k["passed"] + r["passes"]
        k["largest_t"], k["largest_either"] = max(k["largest_t"], min(ts)), max(k["largest_either"], max(ts))
        if r["passes"] and inside is not None:
            k["passed_inside"].append(round(inside, 2))
    return {"panel": panel, "seed": seed, **{k: v for k, v in how.items()}, "bar": res["bar"], "sent": res["sent"], "passed": res["passed"],
            "answers": answers, "keen": kept, "chosen": res["chosen"], "seconds": round(time.time() - t0, 1)}


def row(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r) + "\n").encode())
    os.close(f)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def show(r):
    print(f"{r['panel']} seed {r['seed']}: bar {r['bar']:.2f}, sent {r['sent']}, answers passed {sum(a['passes'] for a in r['answers'])} of {len(r['answers'])}; "
          + "; ".join(f"{k} {v['passed']} of {v['sent']}, largest t {v['largest_t']:.2f} (either form {v['largest_either']:.2f})" + (f", share of each passed set the link is in {v['passed_inside']}" if v["passed_inside"] else "")
                      for k, v in r["keen"].items()) + f"; {r['seconds']}s", flush=True)
    for a in r["answers"]:
        print(f"   link {a['link']} {a['way']:5s} {'PASS' if a['passes'] else '    '} S {100 * a['s'][0]:6.2f}% ({100 * a['span'][0]:6.2f} to {100 * a['span'][1]:6.2f}), level and line out {100 * a['s'][1]:6.2f}%; t {a['t'][0] or 0:5.2f} and {a['t'][1] or 0:5.2f}; "
              f"without best year {100 * a['without_best']:.2f}%; {a['place_years']} place-years in {a['places']} places", flush=True)


def tally(rs):
    """Of a panel's worlds: for each way an answer was sent, how many of the links passed; the keen proposals by how they stand to what was planted; and how many worlds had a pass that nothing planted stands behind (where nothing predicts, any pass at all; where a link is planted, a keen pass that names neither a planted input nor a near copy of one)."""
    out = {"worlds": len(rs), "false_worlds": sum(r["passed"] > 0 if r["panel"] in NOTHING else any(v["passed"] for k, v in r["keen"].items() if k.endswith("other")) for r in rs)}
    for r in rs:
        for k, v in r["keen"].items():
            got = out.setdefault(k, [0, 0])
            got[0], got[1] = got[0] + v["passed"], got[1] + v["sent"]
    for way in WAYS:
        a = [a for r in rs for a in r["answers"] if a["way"] == way]
        out[way] = (sum(x["passes"] for x in a), len(a), float(np.median([x["size"] for x in a if x["size"] is not None])) if a else None)
    return out


def table():
    rs = rows()
    kinds = [f"keen-{a} {b}" for b in ("names", "copy", "other") for a in ("all", "set")]
    print("| Panel | Worlds | Answer in the true places | for all places | by claim | " + " | ".join(kinds) + " | Worlds with a pass nothing stands behind |")
    print("|---|---|---|---|---|" + "---|" * len(kinds) + "---|")
    for name in PANELS:
        mine = [r for r in rs if r["panel"] == name]
        if not mine:
            continue
        t = tally(mine)
        cells = [f"{t[w][0]} of {t[w][1]} (middle size {100 * t[w][2]:.1f}%)" if t[w][1] else "" for w in WAYS]
        cells += [f"{t[k][0]} of {t[k][1]}" if k in t else "" for k in kinds]
        print(f"| {name} | {t['worlds']} | " + " | ".join(cells) + f" | {t['false_worlds']} |")
    nothing = [r for r in rs if r["panel"] in NOTHING]
    if nothing:
        any_pass = sum(r["passed"] > 0 for r in nothing)
        print(f"\nWorlds where nothing predicts: {any_pass} of {len(nothing)} with any pass at all, the answers of same_year among them.")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "smoke":
        panel, seeds = sys.argv[2], [int(s) for s in sys.argv[3:]]
        assert all(s in SMOKE for s in seeds), "smoke seeds only"
        got = []
        for seed in seeds:
            got.append(world(panel, seed))
            show(got[-1])
        print("TALLY", panel, tally(got))
    elif cmd == "count":
        panel = sys.argv[2]
        part, parts = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 3 else (0, 1)
        done = {(r["panel"], r["seed"]) for r in rows()}
        for seed in list(PANELS[panel][1])[part::parts]:
            if (panel, seed) in done:
                print(f"{panel} seed {seed}: already read, not read again", flush=True)
                continue
            r = world(panel, seed)
            row(r)
            show(r)
    elif cmd == "table":
        table()
