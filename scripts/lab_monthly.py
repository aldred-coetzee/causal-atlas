"""Reading by month: prototypes and a harness for the design work that comes before a registered rule (docs/specs/2026-11-11-parallel-helpers-second-wave.md, brief E; notes in docs/reading/reading-by-month.md).

Made-up tables only. Every number this prints is a development number: smoke seeds 60001 to 60999, never in a count. The finders and the referee are imported and not edited; where a setting of theirs is changed it is changed in this process alone, and put back.

Part one holds the prototypes: ways to shape a monthly table before the finders and the referee read it. Nothing in part one imports the world maker or is told what was planted.
Part two is the harness: it makes worlds (scripts/lab_monthly_worlds.py), runs each way, and alone knows the truth.

    PYTHONPATH=src python scripts/lab_monthly.py asis season+near 60101 24 4
    PYTHONPATH=src python scripts/lab_monthly.py ways steady 60201 10
    PYTHONPATH=src python scripts/lab_monthly.py base 60401 6
"""
import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

from causal_atlas import finders as fd
from causal_atlas import referee as rf

YEAR = 12
OUT = Path("data/panel/monthly")

# ---------------------------------------------------------------------------------------------------------------------
# Part one: prototypes. Nothing here knows what was planted.
# ---------------------------------------------------------------------------------------------------------------------

LAGS = (1, 2, 3, 4, 5, 6)  # months before, each a member of the slope family
WINDOWS = ((1, 2, 3), (4, 5, 6), (1, 2, 3, 4, 5, 6))  # a series over several months before, as one term
SCALED = {"MIN_PAST": 24, "WARM": 24, "SPAN": 36, "OWN": 120.0, "QUIET": 12}  # the settings counted in years, made two or three years of months
FEATURES = ("mean", "peak", "worst three", "months beyond")
_REFEREE_DRAWS, _REFEREE_LEVEL = rf._draws, rf._level


class using:
    """Settings of the finders and the referee, changed for the length of a block in this process only."""

    def __init__(self, **kw):
        self.kw = kw

    def __enter__(self):
        self.old = {k: getattr(fd if k == "QUIET" else rf, k) for k in self.kw}
        for k, x in self.kw.items():
            setattr(fd if k == "QUIET" else rf, k, x)

    def __exit__(self, *a):
        for k, x in self.old.items():
            setattr(fd if k == "QUIET" else rf, k, x)


def _before(a):
    """The sum over the steps before each step."""
    c = np.cumsum(a, axis=-1)
    return np.concatenate([np.zeros_like(c[..., :1]), c[..., :-1]], axis=-1)


def season_out(values, least=2, last=None):
    """Each value less the mean of the same calendar month in earlier years: all of them, or the `last` of them. Nothing where fewer than `least` earlier years have the month. Month 0 is taken as a January; only the earlier years go in, so the result may be used at its own date."""
    v = np.asarray(values, float)
    out = np.full(v.shape, np.nan)
    for m in range(YEAR):
        x = v[..., m::YEAR]
        ok = np.isfinite(x)
        n, s = _before(ok * 1.0), _before(np.where(ok, x, 0.0))
        if last is not None:
            n[..., last:], s[..., last:] = n[..., last:] - n[..., :-last], s[..., last:] - s[..., :-last]
        with np.errstate(divide="ignore", invalid="ignore"):
            out[..., m::YEAR] = np.where(n >= least, x - s / n, np.nan)
    return out


def months_out(d):
    """What a series' own month before leaves: each departure less a share of last month's, the share fitted over all places on earlier months alone. d: places by months, the season already out."""
    last = np.full(d.shape, np.nan)
    last[..., 1:] = d[..., :-1]
    ok = np.isfinite(d) & np.isfinite(last)
    num, den = _before(np.where(ok, d * last, 0.0).sum(axis=-2)), _before(np.where(ok, last * last, 0.0).sum(axis=-2))
    with np.errstate(divide="ignore", invalid="ignore"):
        share = np.nan_to_num(num / den)
    return d - share[..., None, :] * last


def whole_years(first, block=YEAR):
    """The referee's draw of groups and steps, with the steps drawn a whole year (or `block` months) at a time: every month of a drawn year is taken together, as often as its year. The groups are drawn as the referee draws them."""

    def draws(groups, steps, n, seed):
        rng = np.random.default_rng(seed)
        year = (first + np.arange(steps)) // block
        year = year - year[0]
        k = int(year[-1]) + 1
        cg = rng.multinomial(groups, np.full(groups, 1 / groups), n).astype(float)
        return cg, rng.multinomial(k, np.full(k, 1 / k), n).astype(float)[:, year]

    return draws


def window(v, o, board, lags):
    """A series over several months before, as one term: the sum of it at each of `lags`."""
    z = sum(fd.lagged(v, "slope", k) for k in lags) / np.sqrt(len(lags))
    return fd._post(v, o, z, fd._single(v), lambda i, way, a: {"inputs": [(i, k) for k in lags], "form": "mode"}, "slope", f"lags {lags[0]} to {lags[-1]}", 1)


def tail_at(v, o, board, q, lag):
    """A tail event in a series `lag` months before."""
    z = fd.lagged(v, "tail", 1, q)
    z = np.concatenate([np.zeros(z.shape[:2] + (lag - 1,)), z[:, :, : z.shape[2] - (lag - 1)]], axis=2)
    return fd._post(v, o, z, fd._single(v), lambda i, way, a: {"inputs": [(i, lag)], "form": "tail", "level": q}, "extremes", f"tail {q} lag {lag}", 1)


def month_members(lags=LAGS, windows=WINDOWS, tails=(3, 6)):
    """The members as counted, with the plain line at each of `lags` months before, the windows, and the two tail members at `tails` months before as well."""
    first = [(lambda v, o, b, k=k: fd.slope(v, o, b, k)) for k in lags] + [(lambda v, o, b, w=w: window(v, o, b, w)) for w in windows]
    extra = [(lambda v, o, b, q=q, k=k: tail_at(v, o, b, q, k)) for q in fd.TAILS for k in tails]
    return first + fd.MEMBERS[2:12] + extra + fd.MEMBERS[12:]


def read_table(values, group, first, outcomes, members=None, allowed=None, bars=("steps",), seed=0, labels=False):
    """The finders on the steps before `first`, the steward, and the referee on the rest. `bars`: "steps" draws single steps again as the referee does; "years" draws whole years of months. Returns the rows sent and the referee's result under each bar."""
    board = fd.swarm(fd.view(values, group, first, outcomes, allowed), members)
    rows = fd.steward(board)
    return board, rows, judged(values, group, first, rows, bars, seed, labels)


def judged(values, group, first, rows, bars=("steps",), seed=0, labels=False):
    """The referee on the rows, under each bar. For speed over hundreds of steps the referee's level of a series' own past is taken from the finders' function, which gives the same numbers by one sort a step."""
    out = {}
    for b in bars:
        rf._draws, rf._level = _REFEREE_DRAWS if b == "steps" else whole_years(first), fd.level
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                out[b] = rf.judge(values, group, first, [fd.proposal(r) for r in rows], seed=seed, labels=labels)
        finally:
            rf._draws, rf._level = _REFEREE_DRAWS, _REFEREE_LEVEL
    return out


def _top(x, k):
    """The mean of the k largest of the last axis; nothing where any is missing."""
    return np.where(np.isfinite(x).all(axis=-1), np.sort(np.nan_to_num(x), axis=-1)[..., -k:].mean(axis=-1), np.nan)


def yearly_features(values, outcomes, half=False, q=0.9):
    """Way (b): a monthly table made yearly. Each outcome becomes one yearly series; every other series becomes four: over twelve months, its mean, its peak, the mean of its worst three months, and how many months stood beyond the level q of its own earlier months. All on the series with its season out.
    half=False: the outcome is its mean over the calendar year, the features are of the calendar year, and the referee sets a year's outcome beside the features of the year before.
    half=True: the outcome is its mean over July to December less what its own June says of that (a share fitted on earlier years alone), the features are of the twelve months to June, and are stored a year early so that the referee's one year before is those twelve months.
    Returns the yearly table, the yearly outcomes, and for each yearly series the monthly series it came from and what it is."""
    v = np.asarray(values, float)
    d = season_out(v)
    S, P, T = v.shape
    Y = T // YEAR
    outs = [int(o) for o in outcomes]
    table, source = [], []
    for o in outs:
        if half:
            late = d[o, :, : Y * YEAR].reshape(P, Y, YEAR)[:, :, 6:].mean(axis=2)
            june = d[o, :, 5 : Y * YEAR : YEAR]
            ok = np.isfinite(late) & np.isfinite(june)
            with np.errstate(divide="ignore", invalid="ignore"):
                share = np.nan_to_num(_before(np.where(ok, late * june, 0.0).sum(axis=0)) / _before(np.where(ok, june * june, 0.0).sum(axis=0)))
            table.append(late - share[None, :] * june)
        else:
            table.append(v[o, :, : Y * YEAR].reshape(P, Y, YEAR).mean(axis=2))
        source.append((o, "outcome"))
    for s in range(S):
        if s in outs:
            continue
        f = {k: np.full((P, Y), np.nan) for k in FEATURES}
        for y in range(Y):
            a = y * YEAR + (6 if half else 0)  # the first of the twelve months stored at index y: January, or July so that they end in the June of the year after
            if a + YEAR > T:
                continue
            x = d[s, :, a : a + YEAR]
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                lv = np.nanquantile(d[s, :, :a], q, axis=1) if a >= 3 * YEAR else np.full(P, np.nan)
            whole = np.isfinite(x).all(axis=1)
            f["mean"][:, y] = np.where(whole, np.nan_to_num(x).mean(axis=1), np.nan)
            f["peak"][:, y] = _top(x, 1)
            f["worst three"][:, y] = _top(x, 3)
            f["months beyond"][:, y] = np.where(whole & np.isfinite(lv), (x > lv[:, None]).sum(axis=1), np.nan)
        for k in FEATURES:
            table.append(f[k])
            source.append((s, k))
    return np.array(table), list(range(len(outs))), source


def by_calendar_month(values, outcomes, lags=LAGS):
    """Way (c): one calendar month at a time across years. For each calendar month a yearly table of its own: each outcome in that month, less its season and what its own month before says (both from earlier dates alone); and every other series as it stood each of `lags` months before that month, stored a year early so that the referee's one year before is that many months before.
    Returns the twelve tables, the yearly outcomes of one table, and for each series of one table the monthly series it came from and the months before."""
    v = np.asarray(values, float)
    S, P, T = v.shape
    Y = T // YEAR
    outs = [int(o) for o in outcomes]
    rest = np.array([months_out(season_out(v[o])) for o in outs])
    tables = []
    source = [(o, 0) for o in outs] + [(s, j) for s in range(S) if s not in outs for j in lags]
    for m in range(YEAR):
        t = [rest[i][:, m : Y * YEAR : YEAR] for i in range(len(outs))]
        for s, j in source[len(outs):]:
            x = np.full((P, Y), np.nan)
            got = v[s][:, YEAR + m - j : T : YEAR]
            x[:, : got.shape[1]] = got[:, :Y]
            t.append(x)
        tables.append(np.array(t))
    return tables, list(range(len(outs))), source


def read_by_calendar_month(values, group, first_year, outcomes, lags=LAGS, members=None, seed=0, labels=False):
    """Way (c) read: the finders on each calendar month's table, one board, one steward, and the referee on the twelve tables stacked, so that every month's rows are held to one bar."""
    tables, outs, source = by_calendar_month(values, outcomes, lags)
    n = len(source)
    board = []
    for m, t in enumerate(tables):
        for r in fd.swarm(fd.view(t, group, first_year, outs), members):
            r = dict(r)
            r["outcome"] = r["outcome"] + m * n
            r["inputs"] = [(s + m * n, k) for s, k in r["inputs"]]
            r["names"] = frozenset(s + m * n for s in r["names"])
            if r.get("state") is not None:
                r["state"] = (r["state"][0] + m * n, r["state"][1])
            board.append(r)
    rows = fd.steward(board)
    stacked = np.concatenate(tables)
    return board, rows, judged(stacked, group, first_year, rows, ("steps",), seed, labels), [(m,) + source[i] for m in range(YEAR) for i in range(n)]


def baseline_errors(v, group, first):
    """Question 3: for one outcome (places by months), the mean squared error on the months from `first` of several ways of saying next month from the past alone, each in units of the place's own spread about its season over the early months.
    mean: the past mean. last: last month. year ago: the same month a year before. season: the same month over all earlier years. season+last: that, with a share of last month's departure from its season. six raw: the referee's six baselines, chosen by place, on the months as they are. six season out: the same six on the months with the season out (the same month in earlier years, with the month before, the place's line and its group's month before to choose among). six recent season: the same with the season from the last eight years only."""
    v = np.asarray(v, float)
    d = season_out(v)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        unit = np.nanstd(d[:, :first], axis=1, keepdims=True)
        mean = rf._mean(v)[0]
        last = rf._lag(v, 1)
        e = {"mean": v - mean, "last": v - last, "year ago": v - rf._lag(v, YEAR), "season": d, "season+last": months_out(d)}
        for name, x in (("six raw", v), ("six season out", d), ("six recent season", season_out(v, last=8))):
            y = x / unit
            b, chosen = rf.baselines(y, group)
            e[name] = (y - np.take_along_axis(b, chosen[None], 0)[0]) * unit
    ok = np.all([np.isfinite(x[:, first:]) for x in e.values()], axis=0)
    return {k: float((((x / unit)[:, first:]) ** 2)[ok].mean()) for k, x in e.items()}


# ---------------------------------------------------------------------------------------------------------------------
# Part two: the harness. It makes the worlds and alone knows what was planted.
# ---------------------------------------------------------------------------------------------------------------------

CELLS = {  # question 1: the same seeds in each, so that what differs is the season and the memory alone
    "season+near": dict(season=1.0, memory="near"),
    "near": dict(season=0.0, memory="near"),
    "season": dict(season=1.0, memory="none"),
    "as yearly": dict(season=0.0, memory="loose"),
    "same month": dict(season=1.0, memory="near", kind="same_month"),
    "wander": dict(season=1.0, memory="near", wander=0.3),
    "linked 1": dict(season=1.0, memory="near", kind="steady", lag=1),  # and two where something does, to see what the finders as they are hear
    "linked 3": dict(season=1.0, memory="near", kind="steady", lag=3),
    "linked 1, no season": dict(season=0.0, memory="near", kind="steady", lag=1),
}
PLACES, FRAC = 60, 0.5
WIDE = [m for m in fd.MEMBERS if m is not fd.pairs]


def relation(outcome, named, truth):
    """What a row is to what was planted: full (the link's outcome and exactly its input), part (its input with something else), other."""
    for i, d in enumerate(truth):
        s = {int(x) for x, _ in d["inputs"]}
        if d["outcome"] == outcome and s <= set(named):
            return ("full" if s == set(named) else "part"), i
    return "other", None


def tally(rows, res, truth, who=None, months=None):
    """One way on one world: rows sent, the bar, and what passed, set against the truth. `who` turns a series of the table read into the monthly series it came from; `months` an input into how many months before it stands."""
    who = (lambda s: s) if who is None else who
    months = (lambda s, k: k) if months is None else months
    out = {"sent": len(rows), "bar": None if not np.isfinite(res["bar"]) else round(res["bar"], 2), "passed": res["passed"], "full": 0, "part": 0, "other": 0, "heard": [], "passes": []}
    best = None
    for r, p in zip(rows, res["proposals"]):
        ts = [p[f]["t"] for f in rf.READS]
        t = None if any(x is None for x in ts) else min(ts)
        rel, i = relation(who(r["outcome"]), {who(s) for s in r["names"]}, truth)
        if rel == "full" and t is not None and (best is None or t > best):
            best = t
        if not p["passes"]:
            continue
        predicts = i is not None and truth[i]["predicts"]
        kind = rel if predicts or rel == "other" else "same month"
        out[kind] = out.get(kind, 0) + 1
        if rel == "full" and predicts and i not in out["heard"]:
            out["heard"].append(i)
        out["passes"].append({"is": kind, "by": f"{r['family']}: {r['member']}", "lags": sorted({int(months(s, k)) for s, k in r["inputs"]}), "t": None if t is None else round(t, 2), "size": p["size"],
                              "together": None if p.get("label") is None else p["label"]["together"]})
    out["best_true_t"] = None if best is None else round(best, 2)
    return out


def world(seed, kind="none", months=480, **kw):
    import lab_monthly_worlds as mw  # the world maker: imported here and nowhere in part one

    assert 60001 <= seed <= 60999, "smoke seeds only"
    kind = kw.pop("kind", kind)
    try:
        return mw.make(seed, kind, places=int(kw.pop("places", PLACES)), months=months, frac=FRAC, **kw)
    except ValueError as e:  # a seed whose layout leaves too few series free of drift for the links: no world is made, and the seed is written down as passed over
        write("passed-over", {"seed": seed, "kind": kind, "why": str(e)})
        return None


def write(name, line):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.jsonl", "a") as f:
        f.write(json.dumps(line) + "\n")
    print(json.dumps(line), flush=True)


def job_asis(cell, seed0, n, bare=0, months=360):
    """Question 1: the finders and the referee as they are, on monthly worlds where nothing predicts a month ahead (and, in the linked cells, where something does)."""
    first = int(0.6 * months) // YEAR * YEAR
    for seed in range(seed0, seed0 + n):
        w = world(seed, months=months, **CELLS[cell])
        if w is None:
            continue
        t0 = time.time()
        outs = np.flatnonzero(w["role"] == "outcome")
        board, rows, res = read_table(w["values"], w["group"], first, outs, bars=("steps", "years"), seed=seed)
        lifted = {f: int(sum(r["family"] == f and r["lift"] >= fd.FLOOR for r in board)) for f in fd.ORDER}
        line = {"job": "asis", "cell": cell, "seed": seed, "months": months, "first": first, "lifted": lifted, "top_lift": round(max((r["lift"] for r in board), default=float("nan")), 2)}
        for b in res:
            line[b] = tally(rows, res[b], w["truth"])
        if seed < seed0 + bare:  # and, for the first `bare` worlds, with the steward's floor taken away and twenty rows sent, to see what the referee alone does with a monthly table
            rows = fd.steward(board, sent=20, share=4, floor=-np.inf)
            res = judged(w["values"], w["group"], first, rows, ("steps", "years"), seed)
            for b in res:
                line[b + ", no floor"] = tally(rows, res[b], w["truth"])
        line["secs"] = round(time.time() - t0, 1)
        write("asis", line)


def job_ways(kind, seed0, n, months=480, ways="a0,a1,a2,by,bh,c", **kw):
    """Question 2: each way on the same worlds. The planted lag runs over one to six months with the seed.
    a0: the season out, everything else as counted (members at one and two months before; bars by single months and by whole years).
    a1: the season out, members at one to six months before and the windows; both bars. a2: as a1 with the settings counted in years made two or three years of months; bar by whole years.
    a9: as a2 with the steward's floor taken away and twenty rows sent, under both bars.
    by: yearly features of the calendar year before against the calendar year's outcome. bh: yearly features of the twelve months to June against July to December. c: one calendar month at a time."""
    first = int(0.6 * months) // YEAR * YEAR
    for seed in range(seed0, seed0 + n):
        lag = 1 + seed % 6
        w = world(seed, kind, months=months, lag=lag, **kw)
        if w is None:
            continue
        x, g, truth = w["values"], w["group"], w["truth"]
        outs = np.flatnonzero(w["role"] == "outcome")
        line = {"job": "ways", "kind": kind, "seed": seed, "lag": lag, "months": months, "first": first, **{k: v for k, v in kw.items()}}
        d = season_out(x)
        for way in ways.split(","):
            t0 = time.time()
            if way == "a0":
                _, rows, res = read_table(d, g, first, outs, bars=("steps", "years"), seed=seed, labels=True)
                line[way] = {b: tally(rows, res[b], truth) for b in res}
            elif way == "a1":
                _, rows, res = read_table(d, g, first, outs, month_members(), bars=("steps", "years"), seed=seed, labels=True)
                line[way] = {b: tally(rows, res[b], truth) for b in res}
            elif way == "a2":
                with using(**SCALED):
                    _, rows, res = read_table(d, g, first, outs, month_members(), bars=("years",), seed=seed, labels=True)
                line[way] = {b: tally(rows, res[b], truth) for b in res}
            elif way == "a9":  # a2 with the steward's floor taken away and twenty rows sent, under both bars: what the referee alone does with months whose season is out
                with using(**SCALED):
                    rows = fd.steward(fd.swarm(fd.view(d, g, first, outs), month_members()), sent=20, share=4, floor=-np.inf)
                    res = judged(d, g, first, rows, ("steps", "years"), seed)
                line[way] = {b: tally(rows, res[b], truth) for b in res}
            elif way in ("by", "bh"):
                table, youts, source = yearly_features(x, outs, half=way == "bh")
                _, rows, res = read_table(table, g, first // YEAR, youts, WIDE, seed=seed, labels=True)
                line[way] = {"steps": tally(rows, res["steps"], truth, lambda s: source[s][0])}
            elif way == "c":
                _, rows, res, source = read_by_calendar_month(x, g, first // YEAR, outs, members=WIDE, seed=seed, labels=True)
                line[way] = {"steps": tally(rows, res["steps"], truth, lambda s: source[s][1], lambda s, k: source[s][2] + YEAR * (k - 1))}
            line[way]["secs"] = round(time.time() - t0, 1)
        write("ways", line)


def job_base(seed0, n, months=480):
    """Question 3: what each way of saying next month from the past leaves, on worlds where nothing predicts."""
    first = int(0.6 * months) // YEAR * YEAR
    for seed in range(seed0, seed0 + n):
        for cell in ("season+near", "season", "near", "wander"):
            w = world(seed, months=months, **CELLS[cell])
            e = [baseline_errors(w["values"][o], w["group"], first) for o in np.flatnonzero(w["role"] == "outcome")]
            write("base", {"job": "base", "cell": cell, "seed": seed, **{k: round(float(np.mean([x[k] for x in e])), 4) for k in e[0]}})


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    job, a = sys.argv[1], sys.argv[2:]
    if job == "asis":
        job_asis(a[0], int(a[1]), int(a[2]), *(int(x) for x in a[3:5]))
    elif job == "ways":
        extra = dict(x.split("=") for x in a[3:])
        ways = extra.pop("ways", "a0,a1,a2,by,bh,c")
        months = int(extra.pop("months", 480))
        job_ways(a[0], int(a[1]), int(a[2]), months=months, ways=ways, **{k: float(v) if k != "memory" else v for k, v in extra.items()})
    elif job == "base":
        job_base(int(a[0]), int(a[1]))
    else:
        raise SystemExit(f"no such job: {job}")
