"""A lab for the second set of finders (docs/specs/2026-11-11-parallel-helpers.md, brief C). Prototypes of members that might hear what the first set does not, and the harness that tries them on made-up worlds. Development only: smoke seeds 59001 to 59999, never a count; every number it prints is a development number.

Two parts. The first holds the prototype members: they read a view of the early years as the members of src/causal_atlas/finders.py do, and import nothing that knows what was planted. The second is the harness, which alone makes the worlds and knows the truth.

    lab_second_set.py lost <kind> <places> <seeds...>      question 1: where a planted link of that kind is lost
    lab_second_set.py try <ask> <kind> <places> <seeds...> questions 2 and 3: the first set beside the prototypes, link by link; <ask> names the arrangements read (shared, state, lag, all)
    lab_second_set.py lag <years> <places> <seeds...>      question 3: a steady link planted that many years before

Kinds are those of scripts/run_finders.py (links, and the worlds where nothing predicts). Outputs go to data/panel/second-set/.
"""
import os

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from contextlib import contextmanager  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402

from causal_atlas import finders as fd  # noqa: E402
from causal_atlas import referee as rf  # noqa: E402

# ---------------------------------------------------------------------------------------------------------------------
# Part one: prototype members. Nothing below this line and above the harness knows what was planted.
# ---------------------------------------------------------------------------------------------------------------------

LONG = (3, 4, 5)  # the lags a long-lag member proposes
FAR = max(LONG)  # the other alignments of a long-lag member start this many years round: nearer, one of its lags would stand a year or two before the outcome


def _commons(v):
    return [int(q) for q in np.flatnonzero(v["common"])]


def _memory(v, q):
    """How much of a common series' departure carries to the next year, from the early years of the series alone."""
    c = np.nan_to_num(v["comp"][q, 0, rf.MIN_PAST:])
    den = float((c[:-1] * c[:-1]).sum())
    return float(np.clip((c[1:] * c[:-1]).sum() / den, 0.0, 0.95)) if den > 0 else 0.0


def common_slope(v, o, board, lag=1):
    """The plain line, for the series common to all places only: the same terms as the slope member's, ranked among themselves."""
    qs = _commons(v)
    if len(qs) < 2:
        return []
    z = fd.lagged(v, "slope", lag)[qs]
    return fd._post(v, o, z, [(q,) for q in qs], lambda i, way, a: {"inputs": [(qs[i], lag)], "form": "slope"}, "slope", f"common lag {lag}", 1)


def common_new(v, o, board):
    """What was new in a common series the year before: the series less the share of the year before that which its own memory carries, as a term of two lags the referee reads as a mode."""
    qs = _commons(v)
    if len(qs) < 2:
        return []
    one, two = fd.lagged(v, "slope", 1)[qs], fd.lagged(v, "slope", 2)[qs]
    phi = np.array([_memory(v, q) for q in qs])
    z = (one - phi[:, None, None] * two) / np.sqrt(1 + phi * phi)[:, None, None]
    return fd._post(v, o, z, [(q,) for q in qs], lambda i, way, a: {"inputs": [(qs[i], 1), (qs[i], 2)], "form": "mode", "weights": [1.0, -float(phi[i])]}, "slope", "common, what was new", 1)


def state_pairs(v, o, board):
    """A series that differs by place times a series common to all places, a year before: what the product says beyond the plain lines through the two. The smooth form of a sign that turns on a state; few enough terms to run on a wide table."""
    key = ("lab state pairs",)
    if key not in v["cache"]:
        z = fd.lagged(v, "slope", 1)
        qs = _commons(v)
        names = [(s, q) for s in range(len(z)) if s not in qs for q in qs]
        if names:
            i, j = (np.array(x) for x in zip(*names))
            v["cache"][key] = names, fd.beyond(z[i] * z[j], [z[i], z[j]])
        else:
            v["cache"][key] = names, None
    names, z = v["cache"][key]
    if not names:
        return []
    return fd._post(v, o, z, names, lambda i, way, a: {"inputs": [(names[i][0], 1), (names[i][1], 1)], "form": "product"}, "shape", "state product", 1)


def _far(v):
    """The view with only the other alignments at which none of the long lags stands a year or two before the outcome: a link a year or two before is the first set's to hear, and is not to count against a longer lag of the same series, nor to be counted for it."""
    return {**v, "shifts": tuple(k for k in v["shifts"] if k >= FAR)}


def long_slope(v, o, board, far=True):
    """The plain line three, four and five years before, as one member: every series at every one of those lags is a term, and the lift is taken above the best of all of them at the other alignments."""
    n = len(v["comp"])
    z = np.concatenate([fd.lagged(v, "slope", k) for k in LONG])
    return fd._post(_far(v) if far else v, o, z, fd._single(v) * len(LONG), lambda i, way, a: {"inputs": [(i % n, LONG[i // n])], "form": "slope"}, "slope", "lags 3 to 5" + ("" if far else ", near"), 1)


def long_window(v, o, board, far=True):
    """Three to five years before, taken together: one term a series, the sum of the three lags, read by the referee as a mode."""
    z = sum(fd.lagged(v, "slope", k) for k in LONG) / np.sqrt(len(LONG))
    return fd._post(_far(v) if far else v, o, z, fd._single(v), lambda i, way, a: {"inputs": [(i, k) for k in LONG], "form": "mode", "weights": [1.0] * len(LONG)}, "slope", "window 3 to 5" + ("" if far else ", near"), 1)


PROTOTYPES = {"common": common_slope, "common_new": common_new, "state_pairs": state_pairs, "long": long_slope, "window": long_window,
              "long_near": lambda v, o, b: long_slope(v, o, b, False), "window_near": lambda v, o, b: long_window(v, o, b, False)}

# ---------------------------------------------------------------------------------------------------------------------
# Part two: the harness. It makes the worlds and knows what was planted; no member reads anything from here.
# ---------------------------------------------------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "data" / "panel" / "second-set"
SEEDS = range(59001, 60000)
FIRST = 35


def _harness():
    import run_finders as rn
    import run_referee as rr
    import run_referee_b as rb
    import table_panel
    return rn, rr, rb, table_panel


def made(kind, places, share, seed, lag=1):
    """A made-up world. With `lag` above one, a steady link planted that many years before: the world is made a little longer and each planted input, with any near copy of it, is read that much later, so that what the outcome followed a year before now stands `lag` years before."""
    rn, rr, rb, table_panel = _harness()
    assert seed in SEEDS, "smoke seeds 59001 to 59999 only"
    if kind in rb.PANELS:
        return rn.made({**rb.PANELS[kind][0], "places": places}, rb.PANELS[kind][1], seed)
    how = {"kind": kind, **rr.HOW.get(kind, {}), "share": share, "places": places}
    if lag == 1:
        return table_panel.make(seed, **how)
    w = table_panel.make(seed, **how, years=60 + lag - 1)
    x = w["values"]
    ins = {int(s) for t in w["truth"] for s, _ in t["inputs"]}
    move = set(ins)
    for c in np.flatnonzero(np.asarray(w["role"]) == "local"):
        if int(c) not in ins and any(abs(rr._together(x[c][:, :60], x[s][:, :60])) >= rr.COPY for s in ins):
            move.add(int(c))
    v = x[:, :, :60].copy()
    for s in move:
        v[s] = x[s][:, lag - 1: lag - 1 + 60]
    truth = [{**t, "inputs": [(s, lag) for s, _ in t["inputs"]]} for t in w["truth"]]
    return {**w, "values": v, "truth": truth, "moved": sorted(move)}


def parts(stand):
    """fd.lift taken apart: each term's standing in its own spreads, and what is taken off for the best of the member's terms at a typical other alignment."""
    true, other = stand[:, 0], stand[:, 1:]
    n = other.shape[1]
    s, ss = other.sum(axis=1, keepdims=True), (other * other).sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        z = (true - s[:, 0] / n) / np.sqrt(np.maximum(ss[:, 0] / n - (s[:, 0] / n) ** 2, 0))
        m = (s - other) / (n - 1)
        rest = (other - m) / np.sqrt(np.maximum((ss - other * other) / (n - 1) - m * m, 0))
    ok = np.isfinite(z) & np.isfinite(rest).all(axis=1)
    return z, float(rest[ok].max(axis=0).mean()), rest


def standing(v, o, z, names):
    """A stack of terms as fd._post ranks it, kept whole: the standing at every alignment, the lift, and the lift's two parts."""
    use = [i for i, n in enumerate(names) if o not in n]
    a, c, b = fd.sums(z[use], fd.residual(v, o), v["shifts"])
    stand = fd.scan(a @ v["member"].T, c @ v["member"].T, b @ v["member"].T, v["size"])[0]
    zz, off, _ = parts(stand)
    return use, stand, fd.lift(stand), zz, off


def full(row, t, rn):
    """Whether a row names a planted link in full, and at its lag."""
    names = rn.planted(t)
    if t["kind"] == "many":
        return False
    return row["names"] == names and row["outcome"] == t["outcome"]


def at_lag(row, t):
    return sorted(k for _, k in row["inputs"]) == sorted(k for _, k in t["inputs"]) or row["form"] == "mode" and any(k == t["inputs"][0][1] for _, k in row["inputs"])


@contextmanager
def state_by_mean(values):
    """For a reading by the referee in this process only: a by_state proposal's state is taken as the side of its own past mean in every read, as the proposal's description has it, where the referee as it stands takes the side in each read's own form. The module on disk is not touched."""
    mean = rf.comparable(values, "mean")
    old = rf.terms

    def terms(p, comp):
        if p["form"] != "by_state":
            return old(p, comp)
        s, k = p["state"]
        swapped = np.array(comp, copy=True)
        swapped[s] = mean[s]
        return old(p, swapped)

    rf.terms = terms
    try:
        yield
    finally:
        rf.terms = old


def brief(q, bar=None):
    """One judged proposal, short."""
    t = [q[f]["t"] for f in rf.READS + rf.CHECKS]
    return {"t": [None if x is None else round(x, 2) for x in t], "passes": bool(q["passes"]), "size": None if q["size"] is None else round(q["size"], 4)}


def judged(w, props, seed):
    return rf.judge(w["values"], w["group"], FIRST, props, seed=seed, labels=False)


def boards(w, extra=()):
    """The first set's board on a world, and each prototype's rows beside it."""
    v = fd.view(w["values"], w["group"], FIRST, np.flatnonzero(np.asarray(w["role"]) == "outcome"))
    t0 = time.time()
    board = fd.swarm(v)
    t1 = time.time()
    more = {}
    for name in extra:
        t2 = time.time()
        more[name] = [r for o in v["outcomes"] for r in PROTOTYPES[name](v, o, board)]
        more[name + "_s"] = round(time.time() - t2, 1)
    return v, board, more, round(t1 - t0, 1)


def reading(w, rows, seed, rn, told=False):
    """One reading by the referee of rows the steward sent, each labelled against what was planted; with `told`, the planted answers in their own places are put first under the same bar."""
    rr = _harness()[1]
    ans = [rr.answer(t, "true") for t in w["truth"]] if told else []
    rows = rows[: fd.SENT - len(ans)]
    if not rows and not ans:
        return {"bar": None, "sent": 0, "passed": 0, "rows": [], "answers": []}
    res = judged(w, ans + [fd.proposal(r) for r in rows], seed)
    out = []
    for r, q in zip(rows, res["proposals"][len(ans):]):
        rel, link, inside = rn.stands(r, w)
        out.append({"family": r["family"], "member": r["member"], "form": r["form"], "outcome": r["outcome"], "names": sorted(r["names"])[:6], "lags": sorted({k for _, k in r["inputs"]}), "lift": round(r["lift"], 2), "rel": rel, "link": link,
                    "inside": inside, "places": "all" if isinstance(r["where"], str) else int(r["where"].sum()), **brief(q), "stopped": rn.stopped(q, res["bar"])})
    return {"bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "rows": out, "answers": [brief(q) for q in res["proposals"][: len(ans)]]}


def memory(x):
    """A series' year-to-year carry over the whole table, for the harness's notes."""
    c = x - np.nanmean(x, axis=-1, keepdims=True)
    return float(np.nansum(c[..., 1:] * c[..., :-1]) / np.nansum(c[..., :-1] ** 2))


def lost(kind, places, share, seeds):
    """Question 1. For each planted link: how its own member ranked it, whether the steward sent it, and what the referee made of the row and of the answer; for a sign that turns on a state, the answer read three ways."""
    rn, rr, rb, _ = _harness()
    for seed in seeds:
        t0 = time.time()
        w = made(kind, places, share, seed)
        v, board, _, swarm_s = boards(w)
        sent = fd.steward(board)
        told = reading(w, sent, seed, rn, told=True)
        comp = {f: rf.comparable(w["values"], f) for f in ("mean", "line", "recent")}
        links = []
        for i, t in enumerate(w["truth"]):
            o, (s, _) = t["outcome"], t["inputs"][0]
            mine = [r for r in board if full(r, t, rn)]
            best = {}
            for r in mine:
                if r["member"] not in best or r["lift"] > best[r["member"]]:
                    best[r["member"]] = round(r["lift"], 2)
            rows = [x for x in told["rows"] if x["link"] == i and x["rel"] == "full"]
            d = {"link": i, "outcome": o, "input": int(s), "posted": best, "above_floor": {m: bool(x >= fd.FLOOR) for m, x in best.items()}, "sent": [(x["member"], x["lift"], x["t"], x["passes"], x["stopped"]) for x in rows],
                 "heard": any(x["passes"] for x in rows), "answer": told["answers"][i], "input_memory": round(memory(w["values"][s]), 2)}
            if kind == "shared":
                use, stand, up, zz, off = standing(v, o, fd.lagged(v, "slope", 1), fd._single(v))
                j = use.index(int(s))
                other = stand[j, 1:]
                d["slope"] = {"stand": round(float(stand[j, 0]), 2), "other_mean": round(float(other.mean()), 2), "other_sd": round(float(other.std()), 2), "other_at_3_4_5": [round(float(x), 2) for x in other[:3]],
                              "other_at_minus_3_4_5": [round(float(x), 2) for x in other[::-1][:3]], "z": round(float(zz[j]), 2), "off": round(off, 2), "lift": round(float(up[j]), 2), "rank": int((up > up[j]).sum())}
            if "state" in t:
                q = int(t["state"])
                d["state"], d["state_memory"] = q, round(memory(w["values"][q]), 2)
                x = w["values"][q, 0]
                true = np.where((x - x.mean()) / x.std() >= 0, 1.0, -1.0)[FIRST - 1: -1]
                d["side_agrees"] = {f: round(float((np.where(comp[f][q, 0, FIRST - 1: -1] > 0, 1.0, -1.0) == true).mean()), 2) for f in comp}
            links.append(d)
        row = {"kind": kind, "places": places, "seed": seed, "bar": told["bar"], "sent": told["sent"], "passed": told["passed"], "links": links, "swarm_s": swarm_s}
        if kind == "flip_state":
            ans = [rr.answer(t, "true") for t in w["truth"]]
            prod = [rf.proposal(t["outcome"], [t["inputs"][0], (t["state"], 1)], "product", t["places"], by="answer as a product") for t in w["truth"]]
            both = judged(w, ans + prod, seed)
            with state_by_mean(w["values"]):
                held = judged(w, ans, seed)
            for i, d in enumerate(links):
                d["answer_as_coded"], d["answer_as_product"], d["answer_state_by_mean"] = brief(both["proposals"][i]), brief(both["proposals"][len(ans) + i]), brief(held["proposals"][i])
            row["bars"] = {"coded_and_product": round(both["bar"], 2), "by_mean": round(held["bar"], 2)}
        row["seconds"] = round(time.time() - t0, 1)
        keep(f"lost-{kind}-{places}", row)
        print(f"seed {seed}: bar {told['bar']:.2f}, {told['passed']} of {told['sent']} passed, {row['seconds']}s", flush=True)
        for d in links:
            print("   " + json.dumps(d), flush=True)


def keep(name, row):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.jsonl", "a") as f:
        f.write(json.dumps(row, default=lambda x: x.tolist() if hasattr(x, "tolist") else str(x)) + "\n")


EVERY = ("every pair",)  # left out where a table is too wide for it, as on the first read of the real table
ARRANGE = {  # the boards read on a world, by the question asked: (members of the first set left out, prototypes added, whether a state's side is read by its past mean in every read)
    "shared": {"first": ((), (), False), "common": ((), ("common",), False), "common_new": ((), ("common_new",), False), "both": ((), ("common", "common_new"), False)},
    "state": {"first": ((), (), False), "first_by_mean": ((), (), True), "wide": (EVERY, (), False), "wide_pairs": (EVERY, ("state_pairs",), False), "wide_by_mean": (EVERY, (), True), "wide_pairs_by_mean": (EVERY, ("state_pairs",), True)},
    "lag": {"first": ((), (), False), "long": ((), ("long",), False), "window": ((), ("window",), False), "long_near": ((), ("long_near",), False), "window_near": ((), ("window_near",), False), "long_window": ((), ("long", "window"), False)},
    "all": {"first": ((), (), False), "first_by_mean": ((), (), True), "common": ((), ("common",), False), "long": ((), ("long",), False), "window": ((), ("window",), False),
            "second": ((), ("common", "long"), False), "second_by_mean": ((), ("common", "long"), True),
            "wide": (EVERY, (), False), "wide_second_by_mean": (EVERY, ("common", "long", "state_pairs"), True)},
}


def trial(kind, places, share, seeds, lag=1, ask="all", name=None):
    """Questions 2 and 3. Each world read once in each arrangement, each under its own bar: what is sent, what passes, which planted links are heard and through which member."""
    rn = _harness()[0]
    arrange = ARRANGE[ask]
    extra = sorted({p for _, add, _ in arrange.values() for p in add})
    for seed in seeds:
        t0 = time.time()
        w = made(kind, places, share, seed, lag)
        v, board, more, swarm_s = boards(w, extra)
        row = {"kind": kind, "places": places, "share": share, "lag": lag, "seed": seed, "swarm_s": swarm_s, "proto_s": {k: x for k, x in more.items() if k.endswith("_s")}, "links": len(w["truth"]), "arr": {}}
        for a, (drop, add, by_mean) in arrange.items():
            rows = [r for r in board if r["member"] not in drop] + [r for p in add for r in more[p]]
            if by_mean:
                with state_by_mean(w["values"]):
                    res = reading(w, fd.steward(rows), seed, rn)
            else:
                res = reading(w, fd.steward(rows), seed, rn)
            heard = []
            for i, t in enumerate(w["truth"]):
                got = [x for x in res["rows"] if x["link"] == i and x["rel"] == "full" and x["passes"]]
                heard.append({"any": bool(got), "at_lag": any(t["inputs"][0][1] in x["lags"] for x in got), "members": sorted({x["member"] for x in got})})
            floor = {}
            for r in rows:
                if r["lift"] >= fd.FLOOR:
                    floor[r["member"]] = floor.get(r["member"], 0) + 1
            row["arr"][a] = {"bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "heard": heard, "above_floor": floor,
                             "passes": [(x["member"], x["rel"], x["lift"], x["lags"], x["names"], x["t"]) for x in res["rows"] if x["passes"]],
                             "sent_by": {m: sum(x["member"] == m for x in res["rows"]) for m in sorted({x["member"] for x in res["rows"]})},
                             "full_sent": [[(x["member"], x["lift"], x["lags"], x["t"], x["passes"]) for x in res["rows"] if x["link"] == i and x["rel"] == "full"] for i in range(len(w["truth"]))]}
        row["seconds"] = round(time.time() - t0, 1)
        keep(name or f"try-{ask}-{kind}-{places}" + (f"-lag{lag}" if lag > 1 else ""), row)
        print(f"seed {seed} ({row['seconds']}s): " + "; ".join(f"{a}: bar {(x['bar'] or 0):.2f}, {x['passed']}/{x['sent']}, heard {sum(h['any'] for h in x['heard'])}/{len(x['heard'])}" for a, x in row["arr"].items()), flush=True)


def table(name):
    """A file of trial rows, added up."""
    rows = [json.loads(s) for s in open(OUT / f"{name}.jsonl")]
    print(f"{name}: {len(rows)} worlds, seeds {min(r['seed'] for r in rows)} to {max(r['seed'] for r in rows)}")
    for a in rows[0]["arr"]:
        xs = [r["arr"][a] for r in rows]
        links = [h for x in xs for h in x["heard"]]
        by = {}
        for h in links:
            for m in h["members"]:
                by[m] = by.get(m, 0) + 1
        other = [p for x in xs for p in x["passes"] if p[1] == "other"]
        bars = [x["bar"] for x in xs if x["sent"]]
        print(f"   {a}: heard {sum(h['any'] for h in links)} of {len(links)} (at the planted lag {sum(h['at_lag'] for h in links)}), by {by}; worlds with any pass {sum(x['passed'] > 0 for x in xs)}; passes naming nothing planted {len(other)} {[(p[0], p[2]) for p in other]}; "
              f"rows sent, middle {np.median([x['sent'] for x in xs]):.0f} (most {max(x['sent'] for x in xs)}); bar, middle {np.median(bars) if bars else float('nan'):.2f}")
        fl = {}
        for x in xs:
            for m, n in x["above_floor"].items():
                fl[m] = fl.get(m, 0) + n
        print(f"      rows above the floor, by member, all worlds: {fl}")


if __name__ == "__main__":
    cmd, args = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    opts = dict((a[2:].split("=") + [""])[:2] for a in sys.argv if a.startswith("--"))
    if cmd == "lost":
        lost(args[0], int(args[1]), float(opts.get("share", 0.35)), [int(s) for s in args[2:]])
    elif cmd == "try":  # try <which arrangements> <kind> <places> <seeds...>
        trial(args[1], int(args[2]), float(opts.get("share", 0.35)), [int(s) for s in args[3:]], ask=args[0])
    elif cmd == "lag":  # lag <years> <places> <seeds...>
        trial("steady", int(args[1]), float(opts.get("share", 0.35)), [int(s) for s in args[2:]], lag=int(args[0]), ask="lag")
    elif cmd == "table":
        for a in args:
            table(a)
