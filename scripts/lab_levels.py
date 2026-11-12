"""Development only: why a link planted into series that keep their level is not heard, and ways to hear it. Made-up tables only; smoke seeds 61001 to 61999; no number here is a count. Brief: docs/specs/2026-11-11-parallel-helpers-fourth-wave.md (helper G); notes: docs/reading/series-that-keep-their-level.md.

    lab_levels.py check                      the copied `plant` gives the same table as the registered one; the shape of a made-up table
    lab_levels.py run <name> [options]       tables through the swarm, the steward and the referee, a row a table appended to data/panel/levels/<name>.jsonl
    lab_levels.py table <name>...            what the rows say

Two halves that do not meet. The ways (`WAYS`: a step that makes a new panel from a table, or a change to the baselines in this process alone) see a table and nothing else. The harness makes the tables (scripts/lab_level_worlds.py and synth/table_panel.py, which alone know what was planted), runs a way, and says afterwards what was heard. finders.py and referee.py are imported and not edited; `pipeline` is `run` and `reading` of scripts/run_stage_b.py copied with the first scored year and the last year as arguments (the registered ones are fixed at 35 and 54), and the every-pair member left out as there.
"""
import argparse
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

from causal_atlas import finders as fd
from causal_atlas import referee as rf

ROOT = Path(__file__).resolve().parents[1]
HOLD = ROOT / "data" / "panel" / "levels"  # not committed
SMOKE = range(61001, 62000)
WIDE = [m for m in fd.MEMBERS if m is not fd.pairs]
_BASELINES = rf.baselines


# ---- the ways: each sees a table (values, groups of places, which series are common, which a row may name) and nothing of what was planted ----

def change(v):
    """Each series as its change from the year before."""
    out = np.full(v.shape, np.nan)
    out[..., 1:] = v[..., 1:] - v[..., :-1]
    return out


def unpredicted(v, group):
    """Each series as what its own past did not predict: the value less the referee's own baseline for it (rf.baselines, chosen again for each place and year from earlier years alone). In the first years, before a baseline can be chosen, the change from the year before."""
    out = change(v)
    rows = np.arange(v.shape[1])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for s in range(len(v)):
            b, chosen = _BASELINES(v[s], group)
            e = v[s] - np.take_along_axis(b, chosen[None], 0)[0]
            out[s][:, rf.WARM + 2:] = e[:, rf.WARM + 2:]
    return out


def beside(p, v, copies, only):
    """Outcomes kept as they are; a second copy of every series put beside the table for rows to name. only: rows may name the copies alone; else a row may name a series as it is or its copy."""
    n = len(v)
    allowed = np.zeros((2 * n, 2 * n), bool)
    allowed[:n, n:] = p["allowed"]
    if not only:
        allowed[:n, :n] = p["allowed"]
    q = {**p, "common": np.tile(p["common"], 2), "sets": np.tile(p["sets"], 2), "ids": np.concatenate([p["ids"], np.char.add(p["ids"].astype(str), "'")]), "allowed": allowed, "outcomes": p["outcomes"]}
    return q, np.concatenate([v, copies]), (lambda x: {x + n} if only else {x, x + n}), (lambda x: x + n)


def more_baselines(y, group):
    """rf.baselines with three more ways of carrying a place's own slow movement forward: the last value with the last change again; the last value with the place's mean change so far; the last value with a share of the last change, the share fitted over all places and earlier years."""
    b, _ = _BASELINES(y, group)
    last, before = rf._lag(y, 1), rf._lag(y, 2)
    step = last - before
    d = np.where(np.isfinite(step), step, 0.0)
    n = rf._before(np.isfinite(rf._lag(y, 0) - last) * 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        usual = rf._before(np.nan_to_num(y - last)) / n
    extra = np.array([last + step, last + usual, last + rf._share(y - last, step) * d])
    extra[:, rf._mean(y)[2] < 3] = np.nan
    b = np.concatenate([b, extra])
    return b, rf._choose(y, b)


def way(name, p, v):
    """The table as a way reads it: the panel's facts, the values, the names a planted input may be heard under, and the name its answer is handed over under."""
    same = (lambda x: {x}), (lambda x: x)
    rf.baselines = more_baselines if name == "baseline" else _BASELINES
    if name in ("asis", "baseline"):
        return p, v, *same
    if name == "change":
        return p, change(v), *same
    if name == "unpredicted":
        return p, unpredicted(v, p["group"]), *same
    if name in ("change_beside", "change_only"):
        return beside(p, v, change(v), name.endswith("only"))
    if name in ("unpredicted_beside", "unpredicted_only"):
        return beside(p, v, unpredicted(v, p["group"]), name.endswith("only"))
    raise SystemExit(f"no such way: {name}")


WAYS = ("asis", "change", "unpredicted", "baseline", "change_only", "change_beside", "unpredicted_only", "unpredicted_beside")


# ---- the harness: makes the tables, knows what was planted, says what was heard ----

def pipeline(p, v, seed, first, last, truth=(), names=None, answer=None, paths=()):
    """run_stage_b.run with the years as arguments: the swarm on the early years, the steward's rows, the referee; then the same with the answers put first; then the answers alone under a bar of their own."""
    t0 = time.time()
    seen = v[:, :, :last]
    board = fd.swarm(fd.view(seen, p["group"], first, p["outcomes"], allowed=p["allowed"]), WIDE)
    t1 = time.time()
    rows = fd.steward(board)
    res = rf.judge(seen, p["group"], first, [fd.proposal(r) for r in rows], seed=seed)
    planted = {(t["outcome"], frozenset([x])) for t in truth for x in names(t["input"])}
    pairs = {(a, frozenset([x])) for q in paths for a, c in (q["pair"], q["pair"][::-1]) for x in (names(c) if names else {c})}
    kinds = [("link" if (r["outcome"], r["names"]) in planted else "path" if (r["outcome"], r["names"]) in pairs else "part" if any(o == r["outcome"] and x & r["names"] for o, x in planted) else "other") for r in rows]
    passes = [{"kind": k, "family": r["family"], "member": r["member"], "lift": round(r["lift"], 2), "n": len(r["names"]), "t": [q[f]["t"] and round(q[f]["t"], 2) for f in rf.READS], "label": q["label"]["together"] if q["label"] else None}
              for r, q, k in zip(rows, res["proposals"], kinds) if q["passes"]]
    out = {"seed": seed, "series": len(v), "posted": len(board), "sent": res["sent"], "bar": res["bar"], "passed": res["passed"], "passes": passes, "swarm_s": round(t1 - t0)}
    if truth:
        ans = [rf.proposal(t["outcome"], [(answer(t["input"]), 1)], "slope", t["where"]) for t in truth]
        kept = rows[: fd.SENT - len(ans)]
        told = rf.judge(seen, p["group"], first, ans + [fd.proposal(r) for r in kept], seed=seed, labels=False)
        alone = rf.judge(seen, p["group"], first, ans, seed=seed, labels=False)
        hit = lambda rs, sent, t: any(q["passes"] and r["outcome"] == t["outcome"] and r["names"] in [frozenset([x]) for x in names(t["input"])] for q, r in zip(rs, sent))
        ts = lambda q: [q[f]["t"] and round(q[f]["t"], 2) for f in rf.READS + rf.CHECKS]
        links = []
        for t, a, b in zip(truth, told["proposals"], alone["proposals"]):
            mine = sorted((r for r in board if r["outcome"] == t["outcome"]), key=lambda r: -r["lift"])
            rank = next((n for n, r in enumerate(mine) if (r["outcome"], r["names"]) in planted), None)
            links.append({"share": t["share"], "places": int(t["where"].sum()), "memory": t.get("memory"), "outcome_memory": t.get("outcome_memory"), "rank": rank, "lift": None if rank is None else round(mine[rank]["lift"], 2),
                          "sent": any((r["outcome"], r["names"]) in planted and r["outcome"] == t["outcome"] for r in rows), "heard": hit(res["proposals"], rows, t), "heard_told": hit(told["proposals"][len(ans):], kept, t),
                          "answer": a["passes"], "answer_t": ts(a), "answer_size": a["size"], "alone": b["passes"], "alone_t": ts(b)})
        out.update({"links": links, "told_bar": told["bar"], "alone_bar": alone["bar"]})
    return {**out, "seconds": round(time.time() - t0)}


def goes(p, before, after, truth, first, last):
    """Where a planted addition goes, link by link, on the table as it is (levels): how much of what was added is left in the baseline's error (the error with the link less the error without it, as shares of the addition's spread), which baseline the outcome's places used in the scored years, and how what is left goes with the input the year before read as its level and read as its change."""
    comp = rf.comparable(after[:, :, :last], "mean")
    out = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for t in truth:
            o, x, w = t["outcome"], t["input"], t["where"]
            m, s = np.nanmean(before[o][:, :first], axis=1, keepdims=True), np.nanstd(before[o][:, :first], axis=1, keepdims=True)
            y0, y1 = (before[o][:, :last] - m) / s, (after[o][:, :last] - m) / s
            (b0, c0), (b1, c1) = rf.baselines(y0, p["group"]), rf.baselines(y1, p["group"])
            e0, e1 = y0 - np.take_along_axis(b0, c0[None], 0)[0], y1 - np.take_along_axis(b1, c1[None], 0)[0]
            added, left = (y1 - y0)[w][:, rf.WARM:], (e1 - e0)[w][:, rf.WARM:]
            level = rf._lag(comp[x], 1)[w][:, rf.WARM:]
            moved = (rf._lag(comp[x], 1) - rf._lag(comp[x], 2))[w][:, rf.WARM:]
            err = e1[w][:, rf.WARM:]
            ok = np.isfinite(added + left + level + moved + err)
            r = lambda a, c: float(np.corrcoef(a[ok], c[ok])[0, 1])
            out.append({"share": t["share"], "left": float(np.var(left[ok]) / np.var(added[ok])), "added_of_error_before": float(np.var(added[ok]) / np.var(e0[w][:, rf.WARM:][ok])), "left_of_error": float(np.var(left[ok]) / np.var(err[ok])),
                        "left_with_level": r(left, level), "left_with_change": r(left, moved), "error_with_level": r(err, level), "error_with_change": r(err, moved),
                        "chosen": [int(n) for n in np.bincount(c1[w][:, first:last].ravel(), minlength=6)]})
    return out


def world(a, seed):
    """A table by the arguments, with what was planted: values before and after, the panel's facts, the truth, the shared paths."""
    import lab_level_worlds as lw
    if a.synth:  # the made-up tables of the finders' count: forty series, 60 years, links put into what the outcome's history leaves
        sys.path.insert(0, str(ROOT / "synth"))
        import table_panel
        w = table_panel.make(seed, a.synth, share=a.share, places=a.places)
        v, role = np.array(w["values"], float), np.asarray(w["role"])
        common = ~(np.nanstd(v, axis=1).max(axis=1) > 1e-9 * np.nanstd(v, axis=(1, 2)))
        out = role == "outcome"
        p = {"group": np.asarray(w["group"]), "groups": np.unique(w["group"]), "common": common, "sets": np.where(out, "o", "i"), "ids": np.array([f"s{i:02d}" for i in range(len(v))]), "allowed": ~np.eye(len(v), dtype=bool), "outcomes": np.flatnonzero(out)}
        truth = [{"outcome": int(t["outcome"]), "input": int(t["inputs"][0][0]), "share": t["share"], "where": np.asarray(t["places"])} for t in w["truth"]]
        return p, v, v, truth, []
    fixed = dict(kv.split("=") for kv in a.fixed.split(",")) if a.fixed else None
    kw = dict(places=a.places, years=a.years, series=a.series, fixed=fixed and {k: float(x) for k, x in fixed.items()}, paths=a.paths, path_kind=a.path_kind, path_size=a.path_size, gaps=not a.no_gaps,
              need=tuple(n for n in ((0, a.first, 25), (a.first, a.last, 15), (a.last, a.years, 8)) if n[1] <= a.years))
    sizes = tuple(float(x) for x in a.sizes.split(","))
    if a.plant == "shock":
        kw["shock"] = {"sizes": sizes, "frac": a.frac, "from": a.outcomes_from}
    w = lw.make(seed, **kw)
    before, after, truth = w["values"], w["values"], w["truth"]
    if a.plant == "added":
        after, truth = lw.plant(w, before, seed, sizes=sizes, frac=a.frac, last=a.last, outcomes_from=a.outcomes_from)
    for t in truth:
        t["memory"], t["outcome_memory"] = round(lw.memory(before[t["input"]][t["where"], : a.last]), 2), round(lw.memory(before[t["outcome"]][t["where"], : a.last]), 2)
    return w, before, after, truth, w["paths"]


def keep(name, row):
    HOLD.mkdir(parents=True, exist_ok=True)
    with open(HOLD / f"{name}.jsonl", "a") as f:
        f.write(json.dumps(row, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x)) + "\n")


def run(a):
    warnings.simplefilter("ignore", RuntimeWarning)  # places with no value in a stretch of years
    for seed in a.seeds:
        if seed not in SMOKE:
            raise SystemExit("smoke seeds 61001 to 61999 only")
        p, before, after, truth, paths = world(a, seed)
        for name in a.ways.split(","):
            q, v, names, answer = way(name, p, after)
            r = pipeline(q, v, seed, a.first, a.last, truth, names, answer, paths)
            if name == "asis" and truth and a.goes:
                r["goes"] = goes(p, before, after, truth, a.first, a.last)
            keep(a.name, {"way": name, **{k: x for k, x in vars(a).items() if k not in ("seeds", "ways", "cmd", "names")}, **r})
            print(f"{a.name} {name} seed {seed}: {r['posted']} posted, {r['sent']} sent, bar {r['bar']:.2f}, {r['passed']} passed" + (f"; heard {sum(x['heard'] for x in r['links'])}, handed over {sum(x['answer'] for x in r['links'])}, alone {sum(x['alone'] for x in r['links'])} of {len(r['links'])}" if truth else "")
                  + f"; {r['seconds']}s", flush=True)
        rf.baselines = _BASELINES


def table(names):
    mid = lambda xs: float(np.median(xs)) if len(xs) else float("nan")
    for name in names:
        rs = [json.loads(s) for s in open(HOLD / f"{name}.jsonl")]
        for w in dict.fromkeys(r["way"] for r in rs):
            m = [r for r in rs if r["way"] == w]
            other = sum(any(x["kind"] == "other" for x in r["passes"]) for r in m)
            print(f"{name} | {w}: {len(m)} tables (seeds {min(r['seed'] for r in m)} to {max(r['seed'] for r in m)}), {m[0]['series']} series; posted, middle {mid([r['posted'] for r in m]):.0f}; sent, middle {mid([r['sent'] for r in m]):.0f}; bar, middle {mid([r['bar'] for r in m if r['sent']]):.2f}; "
                  f"tables with any pass {sum(r['passed'] > 0 for r in m)}, with a pass naming nothing planted {other}, of a shared path's pair {sum(any(x['kind'] == 'path' for x in r['passes']) for r in m)} "
                  f"(unlabelled {sum(any(x['kind'] == 'path' and not x['label'] for x in r['passes']) for r in m)}), of a part {sum(any(x['kind'] == 'part' for x in r['passes']) for r in m)}; seconds, middle {mid([r['seconds'] for r in m]):.0f}")
            for r in m:
                for x in r["passes"]:
                    if x["kind"] != "link":
                        print(f"      seed {r['seed']}: a pass of {x['kind']}: {x['member']}, {x['n']} named, lift {x['lift']}, t {x['t']}, label {x['label']}")
            for share in sorted({x["share"] for r in m for x in r.get("links", [])}, reverse=True):
                ls = [x for r in m for x in r["links"] if x["share"] == share]
                t = lambda k: mid([min(x[k][:2]) for x in ls if None not in x[k][:2]])
                print(f"   {share:.0%}: {len(ls)} links; sent {sum(x['sent'] for x in ls)}; heard from the board {sum(x['heard'] for x in ls)}; answer passed handed over {sum(x['answer'] for x in ls)} (lesser t, middle {t('answer_t'):.2f}; bar {mid([r['told_bar'] for r in m]):.2f}); "
                      f"answers alone {sum(x['alone'] for x in ls)} (bar {mid([r['alone_bar'] for r in m]):.2f}); size, middle {mid([x['answer_size'] for x in ls if x['answer_size'] is not None]):.3f}; "
                      f"rank, middle {mid([x['rank'] for x in ls if x['rank'] is not None]):.0f} ({sum(x['rank'] is None for x in ls)} not posted); lift, middle {mid([x['lift'] for x in ls if x['lift'] is not None]):.1f}; "
                      f"memory of input {mid([x['memory'] for x in ls if x['memory'] is not None]):.2f}, of outcome {mid([x['outcome_memory'] for x in ls if x['outcome_memory'] is not None]):.2f}")
            gs = [g for r in m if isinstance(r.get("goes"), list) for g in r["goes"]]
            if gs:
                k = lambda key: mid([g[key] for g in gs])
                print(f"   where the addition goes ({len(gs)} links): left in the baseline's error {k('left'):.2f} of its spread; that is {k('left_of_error'):.2f} of the error; what is left goes with the input's level at {k('left_with_level'):.2f}, with its change at {k('left_with_change'):.2f}; "
                      f"the whole error with the level at {k('error_with_level'):.3f}, with the change at {k('error_with_change'):.3f}; baselines used (mean, last, mean and share, line, group, recent line): {np.sum([g['chosen'] for g in gs], axis=0).tolist()}")


def check(seed=61001):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import lab_level_worlds as lw
    import run_stage_b as sb  # read only: importing defines names and runs nothing
    w = lw.make(seed)
    v = w["values"]
    a, ta = sb.plant(w, v, seed)
    b, tb = lw.plant(w, v, seed)
    print("the copied plant gives the registered one's table:", bool(np.array_equal(a, b, equal_nan=True) and all(x["outcome"] == y["outcome"] and x["input"] == y["input"] and (x["where"] == y["where"]).all() for x, y in zip(ta, tb))))
    vary = np.flatnonzero(~w["common"])
    mem = np.array([lw.memory(v[s][:, :54]) for s in vary])
    print(f"{len(v)} series, {v.shape[1]} places in {len(w['groups'])} groups (sizes {np.bincount(w['group']).min()} to {np.bincount(w['group']).max()}), {v.shape[2]} years; values missing {np.isnan(v[vary]).mean():.0%}")
    print("places a series has: least, middle, most:", [int(x) for x in np.quantile(np.isfinite(v[vary]).any(axis=2).sum(axis=1), [0, 0.5, 1])])
    print("one year goes with the next, by series: least, tenth, middle, nine tenths, most:", [round(float(x), 2) for x in np.nanquantile(mem, [0, 0.1, 0.5, 0.9, 1])], "; above a half:", int((mem > 0.5).sum()), "of", len(mem))
    print("sets:", {k: int((w["sets"] == k).sum()) for k in np.unique(w["sets"])}, "; places a link is put in:", [int(t["where"].sum()) for t in ta])


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("check", "run", "table"))
    ap.add_argument("names", nargs="*")
    ap.add_argument("--seeds", type=lambda s: [int(x) for part in s.split(",") for x in (range(int(part.split("-")[0]), int(part.split("-")[1]) + 1) if "-" in part else [part])], default=[])
    ap.add_argument("--ways", default="asis")
    ap.add_argument("--plant", choices=("added", "shock", "none"), default="added")
    ap.add_argument("--sizes", default="0.35,0.20,0.10")
    ap.add_argument("--frac", type=float, default=0.25)
    ap.add_argument("--outcomes-from", default=None)
    ap.add_argument("--fixed", default=None, help="set=memory,... : every series of a set given that memory exactly")
    ap.add_argument("--places", type=int, default=166)
    ap.add_argument("--series", type=int, default=120)
    ap.add_argument("--years", type=int, default=64)
    ap.add_argument("--first", type=int, default=35)
    ap.add_argument("--last", type=int, default=54)
    ap.add_argument("--paths", type=int, default=0)
    ap.add_argument("--path-kind", default="mixed")
    ap.add_argument("--path-size", type=float, default=1.0)
    ap.add_argument("--no-gaps", action="store_true")
    ap.add_argument("--goes", action="store_true")
    ap.add_argument("--synth", default=None, help="a kind of synth/table_panel.py, with --share and --places")
    ap.add_argument("--share", type=float, default=0.35)
    a = ap.parse_args()
    if a.cmd == "check":
        check(*a.seeds[:1])
    elif a.cmd == "table":
        table(a.names)
    else:
        a.name = a.names[0]
        run(a)
