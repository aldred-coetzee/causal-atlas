"""Stage A2 of docs/plan-finders-and-referee.md: the finders and the board on made-up tables. The swarm of src/causal_atlas/finders.py reads the early years, the steward sends forty rows, the referee reads them once. What knows the planted truth is here, not in the finders: the answers, and which sent row names what.

    run_finders.py smoke <kind> <places> <share> <seeds...>   development: prints, writes nothing; seeds from the smoke range only
    run_finders.py count <panel>...                           the registered seeds of each panel, once each, a row a world
    run_finders.py table                                      the panels against their marks

The rule and the marks are in results/finders-stage-a2.md, committed before any counted seed.
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

from causal_atlas import finders as fd
from causal_atlas import referee as rf

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_referee as rr  # noqa: E402
import run_referee_b as rb  # noqa: E402
import shared_paths  # noqa: E402
import table_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "finders-stage-a2.jsonl"
FIRST, SENT = rr.FIRST, fd.SENT
HALF = 0.5  # a gathered term counts as the planted mode when at least this share of its weight is on the mode's members
SMOKE = range(47001, 48000)
SIZES = ((120, 0.35), (240, 0.35), (480, 0.20))  # places, and the share a link has at that size, as the label's count had them
NOTHING = ("none", "none_strong", "none_plain", "none_rough", "none_gaps", "same_year")  # worlds where nothing predicts a year ahead, as the referee's second count made them
KINDS = rb.KINDS
WORLDS = {"nothing": (30, 30, 15), "path": (15, 15, 8), "link": (20, 20, 10)}  # worlds a panel, by size
PANELS = {}  # name: (what it is, places, how the world is made, the kind of shared path added or None, seeds)
for j, (places, share) in enumerate(SIZES):
    for i, k in enumerate(NOTHING):
        PANELS[f"{k}_{places}"] = ("nothing", places, {**rb.PANELS[k][0], "places": places}, None, range(48001 + 1000 * j + 100 * i, 48001 + 1000 * j + 100 * i + WORLDS["nothing"][j]))
    for i, k in enumerate(rb.PATHS):
        PANELS[f"path_{k}_{places}"] = ("path", places, {"kind": "none", "places": places}, k, range(51001 + 1000 * j + 100 * i, 51001 + 1000 * j + 100 * i + WORLDS["path"][j]))
    for i, k in enumerate(KINDS):
        PANELS[f"{k}_{places}"] = ("link", places, {"kind": k, **rr.HOW.get(k, {}), "share": share, "places": places}, None, range(54001 + 1000 * j + 100 * i, 54001 + 1000 * j + 100 * i + WORLDS["link"][j]))
MARKED = ("steady", "threshold", "extremes", "pair", "flip", "many", "hidden")  # the kinds of link with a mark for being heard; a sign that turns on a state and a link from a series common to all places have none
LEAST = {120: {k: 20 for k in MARKED} | {"steady": 45}, 240: {k: 30 for k in MARKED} | {"steady": 45}, 480: {k: 15 for k in MARKED} | {"steady": 25}}  # links heard from the board, of 60, 60 and 30


def made(how, path, seed):
    w = table_panel.make(seed, **how)
    return shared_paths.add(w, seed, path) if path else w


def planted(t):
    """The series a planted link is made of: its inputs, and the series whose state turns its sign where there is one."""
    return frozenset(int(s) for s, _ in t["inputs"]) | (frozenset([int(t["state"])]) if "state" in t else frozenset())


def stands(row, w):
    """How a sent row stands to what was planted on its outcome. full: it names the link's series and no other (for a link of many weak series, at least HALF its weight is on them). part: it names some of them, or them and others. copy: a series it names is a near copy of a planted input. path: its outcome and series share a slow path. other: none of these. And the link, and the share of the row's places the link is in."""
    names, o = row["names"], row["outcome"]
    if any(p["outcome"] == o and names == {int(p["series"])} for p in w.get("paths", [])):
        return "path", None, None
    for i, t in enumerate(w["truth"]):
        if t["outcome"] != o:
            continue
        inside = None if isinstance(row["where"], str) else float((row["where"] & t["places"]).sum() / row["where"].sum())
        mine = planted(t)
        if t["kind"] == "many":
            wt = np.ones(len(row["inputs"])) if row.get("weights") is None else np.asarray(row["weights"]) ** 2
            on = float(sum(x for (s, _), x in zip(row["inputs"], wt) if s in mine) / wt.sum())
            return ("full" if row["form"] == "mode" and on >= HALF else "part" if names & mine else "other"), i, inside
        if names == mine:
            return "full", i, inside
        if names & mine:
            return "part", i, inside
        if len(names) <= 2 and max(abs(rr._together(w["values"][s], w["values"][a])) for s in names for a, _ in t["inputs"]) >= rr.COPY:
            return "copy", i, inside
        return "other", i, inside
    return "other", None, None


def on(row, w, i):
    """The share of a row's weight that sits on the series of planted link i: one when it names only them, small when a wide term happens to hold one of them."""
    if i is None:
        return None
    wt = np.ones(len(row["inputs"])) if row.get("weights") is None else np.asarray(row["weights"]) ** 2
    mine = planted(w["truth"][i])
    return round(float(sum(x for (s, _), x in zip(row["inputs"], wt) if s in mine) / wt.sum()), 3)


def stopped(q, bar):
    """What kept a row from passing, of the rules beside the bar: None when it passed or did not stand above the bar both ways; else the rules it failed (the check, how widely it applies, a gain, the gain without its best year)."""
    two = [q[f] for f in rf.READS]
    if q["passes"] or any(r["t"] is None or r["t"] <= bar for r in two):
        return None
    c = q[rf.CHECKS[0]]
    why = [] if c["ok"] else ["check"]
    why += ["wide"] if any(r["groups"] < rf.GROUPS or r["years"] < rf.YEARS for r in two) else []
    why += ["gain"] if any(not r["s"] > 0 for r in two) else []
    why += ["best"] if any(not r["without_best"] > 0 for r in two) else []
    return why


def read(w, rows, seed, answers=False):
    """One reading by the referee: the rows, with the planted links' own answers in their own places put first when `answers`, and the rows cut to keep SENT in all."""
    told = [rr.answer(t, "true") for t in w["truth"]] if answers else []
    rows = rows[: SENT - len(told)]
    res = rf.judge(w["values"], w["group"], FIRST, told + [fd.proposal(r) for r in rows], seed=seed)
    out = []
    for r, q in zip(rows, res["proposals"][len(told):]):
        rel, link, inside = stands(r, w)
        out.append({"family": r["family"], "member": r["member"], "form": r["form"], "event": r["event"], "chosen": r["chosen"], "agree": len(r["families"]), "lift": round(r["lift"], 2), "rel": rel, "link": link,
                    "inside": inside, "on": on(r, w, link), "named": len(r["names"]), "t": [q[f]["t"] and round(q[f]["t"], 2) for f in rf.READS], "check": q[rf.CHECKS[0]]["t"] and round(q[rf.CHECKS[0]]["t"], 2), "stopped": stopped(q, res["bar"]),
                    "places": "all" if isinstance(r["where"], str) else int(r["where"].sum()), "passes": q["passes"], "size": q["size"], "label": q["label"]["together"] if q["label"] else None, "back": bool(q["label"]["back"]) if q["label"] else None, "same": q["label"]["same"] if q["label"] else None})
    return {"bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "answers": [{"link": i, "passes": q["passes"], "label": q["label"]["together"] if q["label"] else None} for i, q in enumerate(res["proposals"][: len(told)])], "rows": out}


def world(how, path, seed, floor=fd.FLOOR, first=True, told=True):
    """One made-up world, read once in each arrangement: the swarm's forty; the first round's forty, where they differ; the answers and the swarm's rows under one bar. And where each family ranked each planted link."""
    t0 = time.time()
    w = made(how, path, seed)
    v = fd.view(w["values"], w["group"], FIRST, np.flatnonzero(np.asarray(w["role"]) == "outcome"))
    board = fd.swarm(v)
    t1 = time.time()
    both, one = fd.steward(board, floor=floor), fd.steward(board, floor=floor, rounds=1)
    out = {"seed": seed, "board": read(w, both, seed), "posted": len(board), "swarm_s": round(t1 - t0, 1)}
    same = [(r["outcome"], r["names"], r["family"], r["tag"]) for r in both] == [(r["outcome"], r["names"], r["family"], r["tag"]) for r in one]
    if first:
        out["first"] = out["board"] if same else read(w, one, seed)
    if told and w["truth"]:
        out["told"] = read(w, both, seed, answers=True)
    best, _, queue = fd.ranked(board, floor)
    out["ranks"] = [{f: next((n for n, k in enumerate(queue[f]) if stands(best[k], w)[:2] == ("full", i)), None) for f in fd.ORDER} for i in range(len(w["truth"]))]
    return {**out, "seconds": round(time.time() - t0, 1)}


def heard(reading, i):
    """The rows of a reading that name link i in full and passed."""
    return [r for r in reading["rows"] if r["link"] == i and r["rel"] == "full" and r["passes"]]


def passed(r, rel, reading="board"):
    """A world's passes that stand to the planted truth as `rel`."""
    return [x for x in r[reading]["rows"] if x["passes"] and x["rel"] == rel]


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def keep(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r) + "\n").encode())
    os.close(f)


def mid(xs):
    return float(np.median(xs)) if len(xs) else float("nan")


def table():
    rs = rows()
    mine = {name: [r for r in rs if r["panel"] == name] for name in PANELS}
    of = lambda what, places: [n for n in PANELS if PANELS[n][0] == what and PANELS[n][1] == places]
    print("Where nothing predicts\n\n| Panel | Worlds | with any pass | Rows posted | Rows sent, middle (most) | Bar, middle | Seconds, middle |\n|---|---|---|---|---|---|---|")
    for name in PANELS:
        m = mine[name]
        if m and PANELS[name][0] == "nothing":
            sent = [r["board"]["sent"] for r in m]
            print(f"| {name} | {len(m)} | {sum(r['board']['passed'] > 0 for r in m)} | {mid([r['posted'] for r in m]):.0f} | {mid(sent):.0f} ({max(sent)}) | {mid([r['board']['bar'] for r in m if r['board']['sent']]):.2f} | {mid([r['seconds'] for r in m]):.0f} |")
    print("\nA shared slow path\n\n| Panel | Worlds | with a path row sent | with a path's pass | with one unlabelled | Path passes | labelled | Worlds with a pass naming nothing planted | Rows sent, middle |\n|---|---|---|---|---|---|---|---|---|")
    for name in PANELS:
        m = mine[name]
        if m and PANELS[name][0] == "path":
            ps = [passed(r, "path") for r in m]
            flat = [x for p in ps for x in p]
            print(f"| {name} | {len(m)} | {sum(any(x['rel'] == 'path' for x in r['board']['rows']) for r in m)} | {sum(bool(p) for p in ps)} | {sum(any(not x['label'] for x in p) for p in ps)} | {len(flat)} | {sum(x['label'] for x in flat)} | {sum(bool(passed(r, 'other')) for r in m)} | {mid([r['board']['sent'] for r in m]):.0f} |")
    print("\nPlanted links\n\n| Panel | Worlds | Links | Heard from the board | in round one alone | Answer passed beside the board | Heard, by family | Worlds with a pass naming nothing planted | Passes of a near copy | of a part | A link's passes labelled | Rows sent, middle | Bar, middle | Seconds, middle |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name in PANELS:
        m = mine[name]
        if m and PANELS[name][0] == "link":
            links = [(r, i) for r in m for i in range(len(r["ranks"]))]
            fam = {f: sum(any(x["family"] == f for x in heard(r["board"], i)) for r, i in links) for f in fd.ORDER}
            full = [x for r in m for x in passed(r, "full")]
            print(f"| {name} | {len(m)} | {len(links)} | {sum(bool(heard(r['board'], i)) for r, i in links)} | {sum(bool(heard(r['first'], i)) for r, i in links)} | {sum(a['passes'] for r in m for a in r['told']['answers'])} | " + ", ".join(f"{f} {n}" for f, n in fam.items() if n)
                  + f" | {sum(bool(passed(r, 'other')) for r in m)} | {sum(len(passed(r, 'copy')) for r in m)} | {sum(len(passed(r, 'part')) for r in m)} | {sum(x['label'] for x in full)} of {len(full)} | {mid([r['board']['sent'] for r in m]):.0f} | {mid([r['board']['bar'] for r in m if r['board']['sent']]):.2f} | {mid([r['seconds'] for r in m]):.0f} |")
    print("\nBeside the marks, asked for by the independent reading before the count\n\n| Places | Worlds | Bar where rows were sent: middle (least to most) | Worlds with a bar under 2 | Rows above the bar both ways that did not pass | stopped by the check | by how widely it applies | by no gain | by its best year | Sent rows' middle scored t, lift 3 to 4 | 4 to 5 | above 5 |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for what in ("nothing", "path", "link"):
        for places, _ in SIZES:
            m = [r for n in of(what, places) for r in mine[n]]
            bars = [r["board"]["bar"] for r in m if r["board"]["sent"]]
            xs = [x for r in m for x in r["board"]["rows"]]
            held = [x for x in xs if x["stopped"] is not None]
            low = lambda x: min(x["t"]) if None not in x["t"] else float("nan")
            band = lambda a, b: mid([low(x) for x in xs if a <= x["lift"] < b and None not in x["t"]])
            if m:
                print(f"| {what}, {places} | {len(m)} | {mid(bars):.2f} ({min(bars, default=float('nan')):.2f} to {max(bars, default=float('nan')):.2f}) | {sum(b < 2 for b in bars)} | {len(held)} | " + " | ".join(str(sum(k in x["stopped"] for x in held)) for k in ("check", "wide", "gain", "best")) + f" | {band(3, 4):.2f} | {band(4, 5):.2f} | {band(5, 1e9):.2f} |")
    print("\nPasses that name a planted link in part, by family: how many, and the middle share of the row's weight on the link's series\n")
    for places, _ in SIZES:
        part = [x for n in of("link", places) for r in mine[n] for x in passed(r, "part")]
        print(f"   {places} places: " + (", ".join(f"{f} {sum(x['family'] == f for x in part)} (share {mid([x['on'] for x in part if x['family'] == f]):.2f})" for f in fd.ORDER if any(x["family"] == f for x in part)) or "none"))
        m = mine[f"shared_{places}"]
        print(f"   {places} places: passes of a near copy, where the link is from a series common to all places: {sum(len(passed(r, 'copy')) for r in m)} in {sum(bool(passed(r, 'copy')) for r in m)} of {len(m)} worlds; in the other kinds: {sum(len(passed(r, 'copy')) for n in of('link', places) if n != f'shared_{places}' for r in mine[n])}")
        full = [x["inside"] for n in of("link", places) for r in mine[n] for x in passed(r, "full") if x["inside"] is not None]
        print(f"   {places} places: of the places a heard row applies to, the middle share where the link acts: {mid(full):.2f} over {len(full)} rows; under a half in {sum(x < 0.5 for x in full)}")
        paths = [r for n in of("path", places) for r in mine[n]]
        got = sum(bool(passed(r, "path")) for r in paths)
        print(f"   {places} places: path worlds in which a path's pair passed at all: {got} of {len(paths)}" + ("; under 11, so mark 4 here says the swarm rarely sends a path that passes and does not test the label" if got < 11 else ""))
    print()
    for places, _ in SIZES:
        for label, names, got in ((f"Mark 1, worlds where nothing predicts with any pass, {places} places", of("nothing", places), lambda r: r["board"]["passed"] > 0),
                                  (f"Mark 2, worlds with a link or a path and a pass naming nothing planted, {places} places", of("link", places) + of("path", places), lambda r: bool(passed(r, "other"))),
                                  (f"Mark 4, path worlds with a path's pass left unlabelled, {places} places", of("path", places), lambda r: any(not x["label"] for x in passed(r, "path")))):
            m = [r for n in names for r in mine[n]]
            n = sum(len(PANELS[g][4]) for g in names)
            print(f"{label}: {sum(got(r) for r in m)} of {len(m)} worlds read ({n} registered), at most {rb.at_most(n)}")
        for k in MARKED:
            m = mine[f"{k}_{places}"]
            links = [(r, i) for r in m for i in range(len(r["ranks"]))]
            print(f"Mark 3, {k} heard from the board, {places} places: {sum(bool(heard(r['board'], i)) for r, i in links)} of {len(links)} links read, at least {LEAST[places][k]}")
    print("\nThe plan's rule for keeping a family: best or second best at getting a link heard for some kind at some size")
    kept = set()
    for name in PANELS:
        if PANELS[name][0] == "link" and mine[name]:
            links = [(r, i) for r in mine[name] for i in range(len(r["ranks"]))]
            fam = sorted(((sum(any(x["family"] == f for x in heard(r["board"], i)) for r, i in links), f) for f in fd.ORDER), reverse=True)
            top = [f for n, f in fam if n and n >= fam[1][0]]
            kept |= set(top)
            print(f"   {name}: " + ", ".join(f"{f} {n}" for n, f in fam) + f"; best or second: {top}")
    print(f"Kept: {[f for f in fd.ORDER if f in kept]}; dropped: {[f for f in fd.ORDER if f not in kept]}")


def show(r, links):
    b = r["board"]
    false = [x for x in b["rows"] if x["passes"] and x["rel"] in ("other", "copy")]
    part = [x for x in b["rows"] if x["passes"] and x["rel"] == "part"]
    junk = sorted((x["lift"] for x in b["rows"] if x["rel"] in ("other", "copy")), reverse=True)
    print(f"   lifts of rows naming nothing planted: {junk[:6]} ... {len(junk)} in all; of rows naming a link in full: {sorted((x['lift'] for x in b['rows'] if x['rel'] == 'full'), reverse=True)}")
    paths = [(x["member"], x["lift"], "PASS" if x["passes"] else "-", x["label"]) for x in b["rows"] if x["rel"] == "path"]
    print(f"seed {r['seed']}: bar {b['bar'] or 0:.2f}, {b['passed']} of {b['sent']} passed, swarm {r['swarm_s']}s, all {r['seconds']}s; false {[(x['family'], x['member'], x['rel'], x['label'], x['lift']) for x in false]}; part {[(x['family'], x['form']) for x in part]}; paths {paths}")
    for i in range(links):
        sent = [(x["member"], x["lift"], x["inside"] and round(x["inside"], 2), x["places"], "PASS" if x["passes"] else "-") for x in b["rows"] if x["link"] == i and x["rel"] == "full"]
        told = r.get("told", {}).get("answers", [])
        print(f"   link {i}: answer {'PASS' if told and told[i]['passes'] else '-'}; ranks {r['ranks'][i]}; sent {sent}; first round heard {len(heard(r['first'], i)) if 'first' in r else None}", flush=True)


if __name__ == "__main__":
    assert rf.READS == ("mean", "line") and rf.CHECKS == ("recent",) and rf.BACK == 2.0, "the referee as decisions 0060 and 0061 left it"
    cmd = sys.argv[1]
    if cmd == "count":
        assert fd.FLOOR == 3.0 and fd.SENT == 40, "the steward as decision 0062 left it"
        for panel in sys.argv[2:]:
            _, _, how, path, seeds = PANELS[panel]
            done = {(r["panel"], r["seed"]) for r in rows()}
            for seed in seeds:
                if (panel, seed) in done:
                    print(f"{panel} seed {seed}: already read, not read again", flush=True)
                    continue
                r = {"panel": panel, **world(how, path, seed)}
                keep(r)
                b = r["board"]
                print(f"{panel} seed {seed}: bar {b['bar'] or 0:.2f}, {b['passed']} of {b['sent']} passed, {r['seconds']}s", flush=True)
    elif cmd == "table":
        table()
    if cmd == "smoke":
        opts = dict((a[2:].split("=") + [""])[:2] for a in sys.argv if a.startswith("--"))
        args = [a for a in sys.argv if not a.startswith("--")]
        kind, places, share = args[2], int(args[3]), float(args[4])
        seeds = [int(s) for s in args[5:]]
        assert all(s in SMOKE for s in seeds), "smoke seeds only"
        if kind in rb.PANELS:  # a world where nothing predicts, or a shared slow path, as the referee's second count made them
            how, path = {**rb.PANELS[kind][0], "places": places}, rb.PANELS[kind][1]
        else:
            how, path = {"kind": kind, **rr.HOW.get(kind, {}), "share": share, "places": places}, None
        tot = np.zeros(5, int)
        for seed in seeds:
            r = world(how, path, seed, floor=float(opts.get("floor", fd.FLOOR)), first="quick" not in opts, told="quick" not in opts)
            n = len(r["ranks"])
            show(r, n)
            tot += [n, sum(bool(t["passes"]) for t in r.get("told", {}).get("answers", [])), sum(bool(heard(r["board"], i)) for i in range(n)), sum(x["passes"] and x["rel"] == "other" for x in r["board"]["rows"]), sum(x["passes"] and x["rel"] == "copy" for x in r["board"]["rows"])]
        print(f"{kind} {places} {share}: links {tot[0]}, answer passed {tot[1]}, heard from the board {tot[2]}, passes naming nothing planted {tot[3]}, passes of a near copy {tot[4]}")
