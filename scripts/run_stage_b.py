"""Stage B of docs/plan-finders-and-referee.md: the first read across the real table, between separate data sets, by country and year. The rule and the marks are in results/stage-b-first-read.md, committed before any real series was set beside another; decision 0063.

    run_stage_b.py panel                      build the panel by the count rule and print its counts (each series alone)
    run_stage_b.py rehearse <kind> <seeds...>  development: made-up worlds through the swarm as it runs here; smoke seeds only, prints, writes nothing
    run_stage_b.py places | years | planted   the placebo and known-answer runs, each registered seed once, a row a run
    run_stage_b.py real once                  the real read: refused unless both placebo marks hold, and refused a second time
    run_stage_b.py confirm once               what passed, read on the last ten years
    run_stage_b.py table                      the runs against their marks

What knows a planted truth or how a table was rearranged is here, not in the finders or the referee.
"""
import csv
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

from causal_atlas import finders as fd
from causal_atlas import referee as rf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "stage-b-first-read.jsonl"
HOLD = ROOT / "data" / "panel" / "stage-b"  # not committed
TABLE = ROOT / "data" / "table"
YEARS = np.arange(1961, 2025)
FIRST, LAST = 35, 54  # the finders see the years before FIRST (1961 to 1995); the referee is given the years before LAST and scores 1996 to 2014; 2015 to 2024 is opened by `confirm` alone
NEED = ((1961, 1995, 25), (1996, 2014, 15), (2015, 2024, 8))  # values a place needs in each stretch to count for a series
PLACES, THIRD, MIDDLE, SMALL = 60, 1 / 3, 30, 5
SETS = {"faostat_qcl": "crops", "wdi": "world bank", "faostat_pe": "exchange rates"}  # everything else read here is climate
TIED = {"crops": lambda r: "Food and Agriculture Organization" in r["Source"],  # the Bank's series that are FAO's figures passed on
        "exchange rates": lambda r: "current US$" in r["Indicator Name"] or "LCU per US$" in r["Indicator Name"]}  # a rate, or a value turned into dollars at the year's rate
SEEDS = {"places": range(58001, 58021), "years": range(58101, 58109), "planted": range(58201, 58207)}
MOST = {"places": 2, "years": 1}  # runs with any pass, at most
REAL, CONFIRM = 58900, 58901  # the referee's draws for the real read and for the last ten years
APART, ROUND = 10, (10, 44)  # years any two sets stand apart when years are moved round; years a common series is moved when places are. Years are moved round within the years before LAST only: nothing of 2015 to 2024 enters a placebo
SIZES, LINKS, QUARTER = (0.35, 0.20, 0.10), 3, 0.25  # planted links: three of each size a table, in whole groups holding a quarter of the places
WIDE = [m for m in fd.MEMBERS if m is not fd.pairs]  # the swarm less the member that tries every pair
SMOKE = list(range(47953, 47960)) + list(range(47990, 48000))


def build():
    """The panel by the count rule: series by places by 1961 to 2024, the table's transform applied, months made years, missing where a place does not count, and each series that differs by place as its departure from the year's middle."""
    import duckdb
    import shapefile

    con = duckdb.connect()
    con.sql("set threads = 2")
    s, o, p = (f"'{TABLE / f}'" for f in ("series.parquet", "obs.parquet", "place.parquet"))
    mine = "(s.period = 'year' and s.source in ('faostat_qcl', 'wdi', 'faostat_pe')) or (s.period = 'month' and (s.source in ('spei', 'oni') or s.source like 'candidates.%'))"
    series = con.sql(f"select series_id, source, kind, transform, place_level, period, measures from {s} s where {mine} order by series_id").fetchall()
    places = [r[0] for r in con.sql(f"select place_id from {p} where level = 'country' order by place_id").fetchall()]
    si, pi = {r[0]: i for i, r in enumerate(series)}, {q: i for i, q in enumerate(places)}
    raw = np.full((len(series), len(places), len(YEARS)), np.nan)
    year = con.sql(f"select o.series_id, o.place_id, cast(o.period as integer), o.value from {o} o join {s} s using (series_id) where s.period = 'year' and ({mine}) and o.value is not null and not isnan(o.value) and cast(o.period as integer) between {YEARS[0]} and {YEARS[-1]}").fetchall()
    month = con.sql(f"select o.series_id, o.place_id, cast(substr(o.period, 1, 4) as integer) y, count(*), avg(o.value), sum(o.value) from {o} o join {s} s using (series_id) where s.period = 'month' and ({mine}) and o.value is not null and not isnan(o.value) group by 1, 2, 3 having y between {YEARS[0]} and {YEARS[-1]}").fetchall()
    count = {r[0] for r in series if r[2] == "count"}
    for sid, place, y, v in year:
        if place in pi:
            raw[si[sid], pi[place], y - YEARS[0]] = v
    for sid, place, y, n, mean, total in month:  # a count: the sum of twelve months; anything else: the mean of at least ten
        v = (total if n == 12 else np.nan) if sid in count else (mean if n >= 10 else np.nan)
        if place == "world":
            raw[si[sid], :, y - YEARS[0]] = v
        elif place in pi:
            raw[si[sid], pi[place], y - YEARS[0]] = v
    with np.errstate(divide="ignore", invalid="ignore"):
        for i, r in enumerate(series):
            if r[3] == "log":
                raw[i] = np.where(raw[i] > 0, np.log(raw[i]), np.nan)
            elif r[3] == "log1p":
                raw[i] = np.where(raw[i] >= 0, np.log1p(raw[i]), np.nan)
    common = np.array([r[4] == "world" for r in series])
    have = np.isfinite(raw)
    counts = np.all([have[:, :, (YEARS >= a) & (YEARS <= b)].sum(axis=2) >= n for a, b, n in NEED], axis=0)  # series by places
    first = np.where(common, counts.all(axis=1), counts.sum(axis=1) >= PLACES)
    keep_p = counts[first & ~common].mean(axis=0) >= THIRD
    keep_s = np.where(common, counts.all(axis=1), counts[:, keep_p].sum(axis=1) >= PLACES)
    v = np.where(counts[:, :, None], raw, np.nan)[keep_s][:, keep_p]
    series, common, places = [r for r, k in zip(series, keep_s) if k], common[keep_s], [q for q, k in zip(places, keep_p) if k]
    with np.errstate(invalid="ignore"), __import__("warnings").catch_warnings():
        __import__("warnings").simplefilter("ignore", RuntimeWarning)
        mid = np.where(np.isfinite(v).sum(axis=1) >= MIDDLE, np.nanmedian(v, axis=1), np.nan)
    v = np.where(common[:, None, None], v, v - mid[:, None, :])
    # groups of places: Natural Earth's subregions, the small ones pooled within their UN region
    from causal_atlas import table as tb
    reader = shapefile.Reader(str(tb.RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    fields = [f[0] for f in reader.fields[1:]]
    sub = {}
    for rec in reader.iterRecords():
        rec = dict(zip(fields, rec))
        sub[tb.BY_NAME.get(rec["ADM0_A3"], str(rec["UN_A3"]).zfill(3))] = (rec["SUBREGION"], rec["REGION_UN"])
    label = {q: sub[q][0] for q in places}
    size = lambda g: sum(x == g for x in label.values())
    for region in sorted({sub[q][1] for q in places}):
        subs = sorted({sub[q][0] for q in places if sub[q][1] == region})
        small = [g for g in subs if size(g) < SMALL]
        if not small:
            continue
        big = sorted((g for g in subs if size(g) >= SMALL), key=lambda g: (size(g), g))
        to = f"{region}: other" if sum(size(g) for g in small) >= SMALL or not big else big[0]
        label.update({q: to for q in places if sub[q][0] in small})
    names = sorted(set(label.values()))
    sets = [SETS.get(r[1], "climate") for r in series]
    HOLD.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(HOLD / "panel.npz", values=v, common=common, group=np.array([names.index(label[q]) for q in places]), ids=np.array([r[0] for r in series]), sets=np.array(sets), places=np.array(places), groups=np.array(names),
                        measures=np.array([r[6] for r in series]))
    return panel()


def panel():
    z = np.load(HOLD / "panel.npz")
    p = {k: z[k] for k in z.files}
    p["allowed"] = (p["sets"][:, None] != p["sets"][None, :]) & ~tied(p)
    p["outcomes"] = np.flatnonzero(~p["common"])
    return p


def tied(p):
    """Pairs a row may not name though they are in different sets: a World Bank series made from another set's figures, with any series of that set. Read from the Bank's own list of its series, each alone."""
    with open(ROOT / "data" / "raw" / "wdi" / "WDISeries.csv", encoding="utf-8-sig", newline="") as f:
        bank = {"wdi:" + r["Series Code"]: r for r in csv.DictReader(f)}
    no = np.zeros((len(p["ids"]),) * 2, bool)
    for other, made in TIED.items():
        mine = np.array([s == "world bank" and made(bank[i]) for i, s in zip(p["ids"], p["sets"])])
        no |= mine[:, None] & (p["sets"] == other)[None, :]
    return no | no.T


def describe(p):
    v, sets = p["values"], p["sets"]
    print(f"{len(v)} series, {v.shape[1]} places, {len(YEARS)} years, {len(p['groups'])} groups of places; {int(np.isfinite(v[~p['common']]).sum()):,} values that differ by place")
    for k in sorted(set(sets)):
        print(f"   {k}: {int((sets == k).sum())} series, {int(((sets == k) & p['common']).sum())} of them common to all places")
    no = tied(p)
    for other in TIED:
        print(f"   World Bank series a row may not name with {other}: {int(no[:, sets == other].any(axis=1).sum())}")
    print(f"   pairs of series in different sets: {int((sets[:, None] != sets[None, :]).sum()) // 2:,}; of them a row may not name: {int(no.sum()) // 2:,}")
    here = np.isfinite(v[~p["common"]]).any(axis=2).sum(axis=1)
    print(f"   places a series that differs by place has: least {here.min()}, middle {int(np.median(here))}, most {here.max()}")
    print("   groups: " + ", ".join(f"{g} {int((p['group'] == i).sum())}" for i, g in enumerate(p["groups"])))


def moved(p, how, seed):
    """The panel with the links between its sets broken. places: crops, exchange rates and drought each with their own reordering of the places, the common series moved round in years. years: each set but the World Bank's moved round by its own number of years, any two sets at least APART years apart."""
    rng = np.random.default_rng(seed)
    v, sets, common = p["values"].copy(), p["sets"], p["common"]
    if how == "places":
        for k in (sets == "crops", sets == "exchange rates", (sets == "climate") & ~common):
            v[k] = v[k][:, rng.permutation(v.shape[1])]
        v[common, :, :LAST] = np.roll(v[common][:, :, :LAST], int(rng.integers(ROUND[0], ROUND[1] + 1)), axis=2)
        return v
    n = LAST
    while True:
        by = [0] + [int(x) for x in rng.integers(1, n, 3)]
        if all(min((a - b) % n, (b - a) % n) >= APART for i, a in enumerate(by) for b in by[:i]):
            break
    for k, shift in zip(("crops", "exchange rates", "climate"), by[1:]):
        v[sets == k, :, :LAST] = np.roll(v[sets == k][:, :, :LAST], shift, axis=2)
    return v


def plant(p, v, seed):
    """Nine steady links a year ahead put into a table: an outcome and an input from another set, both among the series that differ by place, in whole groups, at least five, holding at least a quarter of the places. Each adds to the outcome a multiple of the input the year before, sized place by place so that the year-to-year changes of what is added are the stated share of the outcome's year-to-year movement there afterwards (spreads taken over the years before LAST)."""
    rng = np.random.default_rng(seed)
    v, vary = v.copy(), np.flatnonzero(~p["common"])
    outs, truth = rng.choice(vary, LINKS * len(SIZES), replace=False), []
    for n, o in enumerate(outs):
        x = int(rng.choice([s for s in vary if p["allowed"][o, s] and s not in outs]))
        where, groups, took = np.zeros(v.shape[1], bool), list(rng.permutation(len(p["groups"]))), 0
        while where.sum() < QUARTER * v.shape[1] or took < rf.GROUPS:  # the referee passes no row that applies in fewer groups than that
            where, took = where | (p["group"] == groups.pop()), took + 1
        share = SIZES[n // LINKS]
        with np.errstate(invalid="ignore", divide="ignore"), __import__("warnings").catch_warnings():
            __import__("warnings").simplefilter("ignore", RuntimeWarning)
            early = v[x][:, :LAST]
            moves = np.nanstd(np.diff(early, axis=1), axis=1)
            z = np.nan_to_num((v[x] - np.nanmean(early, axis=1, keepdims=True)) / np.where(moves > 0, moves, np.nan)[:, None])
            step = np.nan_to_num(np.nanstd(np.diff(v[o][:, :LAST], axis=1), axis=1))
            memory = float(np.nanmedian([np.corrcoef(a[1:][np.isfinite(a[1:] + a[:-1])], a[:-1][np.isfinite(a[1:] + a[:-1])])[0, 1] for a in early[where] if np.isfinite(a[1:] + a[:-1]).sum() > 10] or [np.nan]))
        v[o][where, 1:] += np.sqrt(share / (1 - share)) * step[where, None] * z[where, :-1]
        truth.append({"outcome": int(o), "input": x, "share": share, "where": where, "memory": round(memory, 2)})
    return v, truth


def reading(p, v, rows, seed, told=()):
    """One reading by the referee of the years before LAST: the rows, with any answers put first and the rows cut to keep fd.SENT in all."""
    rows = rows[: fd.SENT - len(told)]
    res = rf.judge(v[:, :, :LAST], p["group"], FIRST, list(told) + [fd.proposal(r) for r in rows], seed=seed)
    out = []
    for r, q in zip(rows, res["proposals"][len(told):]):
        two = [q[f] for f in rf.READS]
        row = {"outcome": str(p["ids"][r["outcome"]]), "names": [str(p["ids"][s]) for s in sorted(r["names"])] if len(r["names"]) <= 4 else len(r["names"]), "sets": sorted({str(p["sets"][s]) for s in r["names"]}), "family": r["family"], "member": r["member"],
               "form": r["form"], "event": r["event"], "chosen": r["chosen"], "agree": len(r["families"]), "lift": round(r["lift"], 2), "places": "all" if isinstance(r["where"], str) else int(r["where"].sum()),
               "t": [x["t"] and round(x["t"], 2) for x in two], "s": [x["s"] and round(x["s"], 4) for x in two], "span": [x["span"] for x in two], "without_best": [x["without_best"] and round(x["without_best"], 4) for x in two],
               "groups": [x["groups"] for x in two], "years": [x["years"] for x in two], "check": q[rf.CHECKS[0]]["t"] and round(q[rf.CHECKS[0]]["t"], 2), "passes": q["passes"], "size": q["size"],
               "label": q["label"]["together"] if q["label"] else None, "back": bool(q["label"]["back"]) if q["label"] else None, "same": q["label"]["same"] if q["label"] else None}
        if q["passes"]:  # enough to send the same row again on the last ten years
            row["row"] = {"outcome": int(r["outcome"]), "inputs": [[int(a), int(b)] for a, b in r["inputs"]], "form": r["form"], "where": r["where"] if isinstance(r["where"], str) else [int(x) for x in np.flatnonzero(r["where"])], "level": r.get("level"),
                          "groups": None if r.get("groups") is None else [int(x) for x in r["groups"]], "state": None if r.get("state") is None else [int(x) for x in r["state"]], "weights": r.get("weights"), "event": r["event"]}
        out.append(row)
    return {"bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "answers": [{"passes": q["passes"], "size": q["size"], "t": [q[f]["t"] and round(q[f]["t"], 2) for f in rf.READS]} for q in res["proposals"][: len(told)]], "rows": out}, rows


def run(p, v, seed, truth=None):
    """The whole pipeline once on a table: the swarm as it runs here on the early years, the steward's rows, the referee."""
    t0 = time.time()
    board = fd.swarm(fd.view(v[:, :, :LAST], p["group"], FIRST, p["outcomes"], allowed=p["allowed"]), WIDE)
    t1 = time.time()
    rows = fd.steward(board)
    out = {"seed": seed, "posted": len(board), "swarm_s": round(t1 - t0), "board": reading(p, v, rows, seed)[0]}
    if truth:
        told, kept = reading(p, v, rows, seed, [rf.proposal(t["outcome"], [(t["input"], 1)], "slope", t["where"]) for t in truth])
        hit = lambda rs, sent, t: any(q["passes"] and r["outcome"] == t["outcome"] and r["names"] == {t["input"]} for q, r in zip(rs, sent))
        ranks = [next((n for n, r in enumerate(sorted((r for r in board if r["outcome"] == t["outcome"]), key=lambda r: -r["lift"])) if r["names"] == {t["input"]}), None) for t in truth]
        out["told"] = told
        out["links"] = [{"outcome": str(p["ids"][t["outcome"]]), "input": str(p["ids"][t["input"]]), "share": t["share"], "memory": t["memory"], "places": int(t["where"].sum()), "heard": hit(out["board"]["rows"], rows, t), "heard_told": hit(told["rows"], kept, t),
                         "answer": a["passes"], "answer_size": a["size"], "answer_t": a["t"], "rank": k, "sent": any(r["outcome"] == t["outcome"] and r["names"] == {t["input"]} for r in rows)} for t, a, k in zip(truth, told["answers"], ranks)]
    return {**out, "seconds": round(time.time() - t0)}


def fmt(x):
    return "none" if x is None or x != x else f"{x:.2f}"


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def keep(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r, default=lambda x: x.tolist()) + "\n").encode())
    os.close(f)


def marks(rs):
    """For each placebo: runs done, runs with any pass, and whether the mark holds (None until every run is in)."""
    out = {}
    for step in MOST:
        m = [r for r in rs if r["step"] == step]
        bad = sum(r["board"]["passed"] > 0 for r in m)
        out[step] = (len(m), bad, None if len(m) < len(SEEDS[step]) else bad <= MOST[step])
    return out


def confirmed(q, bar):
    """The rule for the last ten years: above the bar for one row and something off the baseline's error, both ways it is read, in at least five groups and five years."""
    return all(q[f]["t"] is not None and q[f]["t"] > bar and q[f]["s"] > 0 and q[f]["groups"] >= 5 and q[f]["years"] >= 5 for f in rf.READS)


def table():
    rs = rows()
    for step, (n, bad, ok) in marks(rs).items():
        m = [r for r in rs if r["step"] == step]
        print(f"{step}: {n} of {len(SEEDS[step])} runs, {bad} with any pass (at most {MOST[step]}): {'not all run' if ok is None else 'holds' if ok else 'MISSED'}")
        if m:
            print(f"   rows posted, middle {np.median([r['posted'] for r in m]):.0f}; sent, middle {np.median([r['board']['sent'] for r in m]):.0f} (most {max(r['board']['sent'] for r in m)}); bar, middle {fmt(np.median([r['board']['bar'] for r in m if r['board']['sent'] and r['board']['bar'] is not None] or [np.nan]))}; seconds, middle {np.median([r['seconds'] for r in m]):.0f}")
            for r in m:
                for x in r["board"]["rows"]:
                    if x["passes"]:
                        print(f"   seed {r['seed']}: {x['names']} -> {x['outcome']} ({x['member']}, lift {x['lift']}, t {x['t']}, label {x['label']})")
    m = [r for r in rs if r["step"] == "planted"]
    if m:
        print(f"planted: {len(m)} of {len(SEEDS['planted'])} runs")
        for share in SIZES:
            ls = [x for r in m for x in r["links"] if x["share"] == share]
            print(f"   {share:.0%}: {len(ls)} links; sent {sum(x['sent'] for x in ls)}; heard from the board {sum(x['heard'] for x in ls)}; answer passed when handed over {sum(x['answer'] for x in ls)}; size given, middle {np.median([x['answer_size'] for x in ls if x['answer_size'] is not None] or [np.nan]):.3f}; rank on its outcome's board, middle {np.median([x['rank'] for x in ls if x['rank'] is not None] or [np.nan]):.0f} ({sum(x['rank'] is None for x in ls)} not posted)")
        print(f"   runs with a pass that names no planted link: {sum(any(x['passes'] and not any(l['outcome'] == x['outcome'] and x['names'] == [l['input']] for l in r['links']) for x in r['board']['rows']) for r in m)}")
    for r in rs:
        if r["step"] == "real":
            b = r["board"]
            print(f"real: {r['posted']} rows posted, {b['sent']} sent, bar {fmt(b['bar'])}, {b['passed']} passed")
            for x in b["rows"]:
                print(f"   {'PASS' if x['passes'] else '    '} {x['names']} ({', '.join(x['sets'])}) -> {x['outcome']}: {x['member']}, {x['form']}, places {x['places']}, lift {x['lift']}, t {x['t']}, s {x['s']}, label {x['label']}")
        if r["step"] == "confirm":
            for x in r["rows"]:
                print(f"confirm: {x['names']} -> {x['outcome']}: {'confirmed' if x['confirmed'] else 'not confirmed'}, bar {fmt(x['bar'])}, t {x['t']}, s {x['s']}, groups {x['groups']}, years {x['years']}")


def rehearse(kind, seeds):
    """Made-up worlds through the swarm as it runs here: outcomes in one set and every other series in another, departures from the year's middle, no every-pair member. Development; prints only."""
    sys.path.insert(0, str(ROOT / "synth"))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import run_finders as rn
    assert all(s in SMOKE for s in seeds), "smoke seeds only"
    how = {"kind": kind, **rn.rr.HOW.get(kind, {}), "share": 0.35, "places": 240}
    for seed in seeds:
        w = rn.made(how, None, seed)
        role = np.asarray(w["role"]) == "outcome"
        v = np.array(w["values"], float)
        common = ~(np.nanstd(v, axis=1).max(axis=1) > 1e-9 * np.nanstd(v, axis=(1, 2)))
        w["values"] = np.where(common[:, None, None], v, v - np.nanmedian(v, axis=1, keepdims=True))
        for way, members, allowed in (("as counted", None, None), ("as run here", WIDE, role[:, None] != role[None, :])):
            t0 = time.time()
            board = fd.swarm(fd.view(w["values"], w["group"], rn.FIRST, np.flatnonzero(role), allowed=allowed), members)
            r = rn.read(w, fd.steward(board), seed)
            print(f"{kind} seed {seed}, {way}: {len(board)} posted, {r['sent']} sent, bar {r['bar']:.2f}, {r['passed']} passed; links heard {sum(bool(rn.heard(r, i)) for i in range(len(w['truth'])))} of {len(w['truth'])}; "
                  f"passes naming nothing planted {sum(x['passes'] and x['rel'] == 'other' for x in r['rows'])}; {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "panel":
        describe(build())
    elif cmd == "rehearse":
        rehearse(sys.argv[2], [int(s) for s in sys.argv[3:]])
    elif cmd == "table":
        table()
    elif cmd in SEEDS:
        p, done = panel(), {(r["step"], r["seed"]) for r in rows()}
        for seed in [int(s) for s in sys.argv[2:]] or SEEDS[cmd]:
            assert seed in SEEDS[cmd], "registered seeds only"
            if (cmd, seed) in done:
                continue
            v = moved(p, "places" if cmd == "planted" else cmd, seed)
            v, truth = plant(p, v, seed) if cmd == "planted" else (v, None)
            r = {"step": cmd, **run(p, v, seed, truth)}
            keep(r)
            print(f"{cmd} seed {seed}: {r['posted']} posted, {r['board']['sent']} sent, bar {fmt(r['board']['bar'])}, {r['board']['passed']} passed" + (f"; heard {sum(x['heard'] for x in r['links'])} of {len(r['links'])}" if truth else "") + f", {r['seconds']}s", flush=True)
    elif cmd == "real" and sys.argv[2:] == ["once"]:
        rs = rows()
        assert not any(r["step"] == "real" for r in rs), "the real read has been made"
        assert all(ok for _, _, ok in marks(rs).values()), f"the placebo marks do not all hold: {marks(rs)}"
        p = panel()
        r = {"step": "real", **run(p, p["values"], REAL)}
        keep(r)
        table()
    elif cmd == "confirm" and sys.argv[2:] == ["once"]:
        rs = rows()
        assert not any(r["step"] == "confirm" for r in rs), "the last ten years have been read"
        real = [r for r in rs if r["step"] == "real"]
        assert len(real) == 1, "no real read to confirm"
        p, out = panel(), []
        for x in real[0]["board"]["rows"]:
            if not x["passes"]:
                continue
            q = x["row"]
            where = q["where"] if isinstance(q["where"], str) else np.isin(np.arange(p["values"].shape[1]), q["where"])
            prop = rf.proposal(q["outcome"], [tuple(i) for i in q["inputs"]], q["form"], where, level=q["level"], groups=None if q["groups"] is None else np.array(q["groups"]), state=None if q["state"] is None else tuple(q["state"]), weights=q["weights"], event=q["event"])
            res = rf.judge(p["values"], p["group"], LAST, [prop], seed=CONFIRM, labels=False)
            g = res["proposals"][0]
            out.append({"outcome": x["outcome"], "names": x["names"], "bar": res["bar"], "confirmed": bool(confirmed(g, res["bar"])), **{k: [g[f][k] if k in ("groups", "years") else g[f][k] and round(g[f][k], 4) for f in rf.READS] for k in ("t", "s", "without_best", "groups", "years")}})
        keep({"step": "confirm", "seed": CONFIRM, "rows": out})
        table()
    else:
        sys.exit(__doc__)
