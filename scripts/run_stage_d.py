"""The first read across the real table by month: between separate data sets, by country and month, 1980 to 2024. The rule and the marks are in results/stage-d-monthly-read.md, committed before any real monthly series was set beside another; decision 0069.

    run_stage_d.py panel                      build the panel by the count rule and print its counts (each series alone)
    run_stage_d.py rehearse <seeds...>        development: a made-up table of the panel's shape through the whole read, for the time it takes; smoke seeds only, prints, writes nothing
    run_stage_d.py places | years | planted   the placebo and known-answer runs, each registered seed once, a row a run
    run_stage_d.py real once                  the real read: refused unless both placebo marks hold and the planted runs are in, and refused a second time
    run_stage_d.py confirm once               what passed, read on 2020 to 2024
    run_stage_d.py table                      the runs against their marks

What knows a planted truth or how a table was rearranged is here, not in the finders or the referee. The read is causal_atlas.months, as counted on made-up tables, less two members the table is too wide for.
"""
import json
import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np

from causal_atlas import finders as fd
from causal_atlas import months as mo
from causal_atlas import referee as rf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "stage-d-monthly-read.jsonl"
HOLD = ROOT / "data" / "panel" / "stage-d"  # not committed
TABLE = ROOT / "data" / "table"
START, MONTHS = 1980, 540  # month 0 is January 1980, the last December 2024
FIRST, LAST = 348, 480  # the finders see the months before FIRST (1980 to 2008); the referee is given the months before LAST and scores 2009 to 2019; 2020 to 2024 is opened by `confirm` alone
NEED = ((0, FIRST, 96), (FIRST, LAST, 108), (LAST, MONTHS, 48))  # months with a value a place needs in each stretch to count for a series
PLACES, THIRD, MIDDLE, SMALL, SPREAD = 40, 1 / 2, 30, 5, 8  # places a series needs; the share of series a place needs (a half: five series are zero-filled everywhere, so a third would keep every place); places behind a month's middle; a group of places smaller than this is pooled; groups a series' places must be spread over
SETS = {"prices and money": ("pink_sheet", "faostat_cp", "faostat_pe", "bis_long_cpi", "bis_eer", "bis_cbpol", "rtfp"),
        "climate": ("oni", "spei", "ibtracs", "firecci"),  # and every candidates.* index
        "earthquakes": ("usgs_quakes",),
        "conflict and protest": ("ucdp_ged", "mass_mobilization"),
        "health and people": ("opendengue", "eurostat_births", "eurostat_deaths", "hfd_stff"),
        "energy and activity": ("ember", "eurostat_electricity", "eurostat_industry", "eurostat_retail", "eurostat_unemployment", "eurostat_air", "eurostat_tourism"),
        "asylum": ("eurostat_asylum",)}
STILL = "prices and money"  # the set left where it is when the others are moved
ZERO = {"ucdp_ged": ("1989-01", "2025-12")}  # a source that writes no row for a month with no event, and the months it watched: no row there is a zero
SEEDS = {"places": range(66001, 66021), "years": range(66101, 66109), "planted": range(66201, 66213)}
MOST = {"places": 2, "years": 1}  # runs with any lead, at most
REAL, CONFIRM = 66900, 66901  # the referee's draws for the real read and for 2020 to 2024
APART = 4  # years any two sets stand apart when they are moved round. Moved by whole years, so a month stays in its season, and within the months before LAST only: nothing of 2020 to 2024 enters a placebo
SIZES, LINKS, QUARTER = (0.20, 0.10, 0.04), 2, 0.25  # planted links: two of each size a table (fourteen series differ by place: more outcomes could leave one with no input outside its set), in whole groups holding a quarter of the places
CONFIRMED = (5, 36)  # groups and months a row must apply in, in 2020 to 2024, to be confirmed
SMOKE = range(60911, 60931)


def members():
    return [m for m in mo.members() if m not in (fd.pairs, fd.by_state)]  # the month members less the one that tries every pair and the one that tries every series against every common series' side (92 common series here: some ten thousand terms of half a megabyte): too wide a table for either


def set_of(source):
    return "climate" if source.startswith("candidates.") else next(k for k, v in SETS.items() if source in v)


def month(s):
    return (int(s[:4]) - START) * 12 + int(s[5:7]) - 1


def build():
    """The panel by the count rule: series by places by the months of 1980 to 2024, the table's transform applied, missing where a place does not count, and each series that differs by place as its departure from the month's middle across places."""
    import duckdb
    import shapefile

    from causal_atlas import table as tb

    con = duckdb.connect()
    con.sql("set threads = 2")
    s, o, p = (f"'{TABLE / f}'" for f in ("series.parquet", "obs.parquet", "place.parquet"))
    series = con.sql(f"select series_id, source, kind, transform, place_level from {s} where period = 'month' order by series_id").fetchall()
    places = [r[0] for r in con.sql(f"select place_id from {p} where level = 'country' order by place_id").fetchall()]
    si, pi = {r[0]: i for i, r in enumerate(series)}, {q: i for i, q in enumerate(places)}
    raw = np.full((len(series), len(places), MONTHS), np.nan)
    for i, r in enumerate(series):  # a zero where a source that writes no row for an empty month was watching
        if r[1] in ZERO:
            a, b = (month(x) for x in ZERO[r[1]])
            raw[i, :, max(a, 0): min(b + 1, MONTHS)] = 0.0
    obs = con.sql(f"select o.series_id, o.place_id, o.period, o.value from {o} o join {s} s using (series_id) where s.period = 'month' and o.value is not null and not isnan(o.value) and o.period >= '{START}-01' and o.period <= '{START + MONTHS // 12 - 1}-12'").fetchall()
    for sid, place, when, v in obs:
        if place == "world":
            raw[si[sid], :, month(when)] = v
        elif place in pi:
            raw[si[sid], pi[place], month(when)] = v
    with np.errstate(divide="ignore", invalid="ignore"):
        for i, r in enumerate(series):
            if r[3] == "log":
                raw[i] = np.where(raw[i] > 0, np.log(raw[i]), np.nan)
            elif r[3] == "log1p":
                raw[i] = np.where(raw[i] >= 0, np.log1p(raw[i]), np.nan)
    common = np.array([r[4] == "world" for r in series])
    have = np.isfinite(raw)
    counts = np.all([have[:, :, a:b].sum(axis=2) >= n for a, b, n in NEED], axis=0)  # series by places
    first = np.where(common, counts.all(axis=1), counts.sum(axis=1) >= PLACES)
    keep_p = counts[first & ~common].mean(axis=0) >= THIRD
    # groups of the kept places: Natural Earth's subregions, the small ones pooled within their UN region
    reader = shapefile.Reader(str(tb.RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    fields = [f[0] for f in reader.fields[1:]]
    sub = {}
    for rec in reader.iterRecords():
        rec = dict(zip(fields, rec))
        sub[tb.BY_NAME.get(rec["ADM0_A3"], str(rec["UN_A3"]).zfill(3))] = (rec["SUBREGION"], rec["REGION_UN"])
    kept = [q for q, k in zip(places, keep_p) if k]
    label = {q: sub[q][0] for q in kept}
    size = lambda g: sum(x == g for x in label.values())
    for region in sorted({sub[q][1] for q in kept}):
        subs = sorted({sub[q][0] for q in kept if sub[q][1] == region})
        small = [g for g in subs if size(g) < SMALL]
        if not small:
            continue
        big = sorted((g for g in subs if size(g) >= SMALL), key=lambda g: (size(g), g))
        to = f"{region}: other" if sum(size(g) for g in small) >= SMALL or not big else big[0]
        label.update({q: to for q in kept if sub[q][0] in small})
    names = sorted(set(label.values()))
    group = np.array([names.index(label[q]) for q in kept])
    counts = counts[:, keep_p]
    spread = np.array([len(set(group[c])) for c in counts])
    keep_s = np.where(common, counts.all(axis=1), (counts.sum(axis=1) >= PLACES) & (spread >= SPREAD))
    v = np.where(counts[:, :, None], raw[:, keep_p], np.nan)[keep_s]
    series, common = [r for r, k in zip(series, keep_s) if k], common[keep_s]
    with np.errstate(invalid="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        mid = np.where(np.isfinite(v).sum(axis=1) >= MIDDLE, np.nanmedian(v, axis=1), np.nan)
    v = np.where(common[:, None, None], v, v - mid[:, None, :])
    HOLD.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(HOLD / "panel.npz", values=v, common=common, group=group, ids=np.array([r[0] for r in series]), sets=np.array([set_of(r[1]) for r in series]), places=np.array(kept), groups=np.array(names))
    return panel()


def panel():
    z = np.load(HOLD / "panel.npz")
    p = {k: z[k] for k in z.files}
    p["allowed"] = p["sets"][:, None] != p["sets"][None, :]  # a row names only series outside its outcome's set; every tie in docs/tied-series.md among monthly series lies inside one set
    p["outcomes"] = np.flatnonzero(~p["common"])
    return p


def describe(p):
    v, sets, common = p["values"], p["sets"], p["common"]
    print(f"{len(v)} series, {v.shape[1]} places, {v.shape[2]} months, {len(p['groups'])} groups of places; {int(np.isfinite(v[~common]).sum()):,} values that differ by place")
    for k in sorted(set(sets)):
        print(f"   {k}: {int((sets == k).sum())} series, {int(((sets == k) & common).sum())} of them common to all places")
    for i in np.flatnonzero(~common):
        here = np.isfinite(v[i]).any(axis=1)
        when = np.flatnonzero(np.isfinite(v[i]).any(axis=0))
        print(f"   {p['ids'][i]} ({sets[i]}): {int(here.sum())} places in {len(set(p['group'][here]))} groups, {START + when[0] // 12}-{when[0] % 12 + 1:02d} to {START + when[-1] // 12}-{when[-1] % 12 + 1:02d}")
    print("   groups: " + ", ".join(f"{g} {int((p['group'] == i).sum())}" for i, g in enumerate(p["groups"])))


def shifts(rng, n):
    """A whole number of years for each of n sets, any two at least APART years apart round the years before LAST, and each as far from none at all."""
    years = LAST // 12
    while True:
        by = [0] + [int(x) for x in rng.integers(1, years, n)]
        if all(min((a - b) % years, (b - a) % years) >= APART for i, a in enumerate(by) for b in by[:i]):
            return [12 * b for b in by[1:]]


def moved(p, how, seed):
    """The panel with the links between its sets broken. places: every set but STILL has its series that differ by place given one reordering of the places, its own; each set's common series are moved round by its own number of years. years: every set but STILL is moved round by its own number of years, whole. Sets stay whole, so what is tied inside a set stays tied."""
    rng = np.random.default_rng(seed)
    v, sets, common = p["values"].copy(), p["sets"], p["common"]
    names = sorted(set(sets))
    if how == "places":
        for k in names:
            if k != STILL:
                v[(sets == k) & ~common] = v[(sets == k) & ~common][:, rng.permutation(v.shape[1])]
        own = [k for k in names if ((sets == k) & common).any()]
        for k, by in zip(own, shifts(rng, len(own))):
            v[(sets == k) & common, :, :LAST] = np.roll(v[(sets == k) & common][:, :, :LAST], by, axis=2)
        return v
    refuse(how != "years", "no such rearrangement")
    rest = [k for k in names if k != STILL]
    for k, by in zip(rest, shifts(rng, len(rest))):
        v[sets == k, :, :LAST] = np.roll(v[sets == k][:, :, :LAST], by, axis=2)
    return v


def plant(p, v, seed):
    """Six steady links put into a table: an outcome and an input from another set, both among the series that differ by place, the input one to six months before, in whole groups of places. Each adds to the outcome a multiple of the input, sized place by place so that the month-to-month changes of what is added are the stated share of the outcome's month-to-month movement there afterwards (spreads taken over the months before LAST). A link stands only in places where both series move; groups are added until those places are a quarter of all and lie in at least as many groups as the referee asks, or the groups run out."""
    rng = np.random.default_rng(seed)
    v, vary = v.copy(), np.flatnonzero(~p["common"])
    with np.errstate(invalid="ignore", divide="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        moves = np.nan_to_num(np.nanstd(np.diff(v[:, :, :LAST], axis=2), axis=2))  # series by places
        mean = np.nanmean(v[:, :, :LAST], axis=2)
    outs, truth = rng.choice(vary, LINKS * len(SIZES), replace=False), []
    for n, o in enumerate(outs):
        x = int(rng.choice([s for s in vary if p["allowed"][o, s] and s not in outs]))
        lag = int(rng.integers(1, 7))
        live = (moves[o] > 0) & (moves[x] > 0)
        where, groups = np.zeros(v.shape[1], bool), list(rng.permutation(len(p["groups"])))
        while groups and (where.sum() < QUARTER * v.shape[1] or len(set(p["group"][where])) < rf.GROUPS):
            where = where | ((p["group"] == groups.pop()) & live)
        share = SIZES[n // LINKS]
        z = np.nan_to_num((v[x] - mean[x][:, None]) / np.where(moves[x] > 0, moves[x], np.nan)[:, None])
        v[o][where, lag:] += np.sqrt(share / (1 - share)) * moves[o][where, None] * z[where, :-lag]
        truth.append({"outcome": int(o), "input": x, "lag": lag, "share": share, "where": where})
    return v, truth


def reading(p, d, rows, seed, first=FIRST, told=()):
    """One reading by the referee of the months given: the rows, with any answers put first and the rows cut to keep fd.SENT in all. A lead is a pass whose label does not say the two move together (decision 0068)."""
    rows = rows[: fd.SENT - len(told)]
    res = rf.judge(d, p["group"], first, list(told) + [fd.proposal(r) for r in rows], seed=seed, labels=True, draw=mo.whole_years(first), settings=mo.READ, level_fn=fd.level)
    lead = lambda q: bool(q["passes"] and q["label"] is not None and not q["label"]["together"])
    out = []
    for r, q in zip(rows, res["proposals"][len(told):]):
        two = [q[f] for f in rf.READS]
        row = {"outcome": str(p["ids"][r["outcome"]]), "names": [str(p["ids"][s]) for s in sorted(r["names"])] if len(r["names"]) <= 4 else len(r["names"]), "sets": sorted({str(p["sets"][s]) for s in r["names"]}), "family": r["family"], "member": r["member"],
               "form": r["form"], "event": r["event"], "chosen": r["chosen"], "agree": len(r["families"]), "lift": round(r["lift"], 2), "places": "all" if isinstance(r["where"], str) else int(r["where"].sum()),
               "t": [x["t"] and round(x["t"], 2) for x in two], "s": [x["s"] and round(x["s"], 4) for x in two], "without_best": [x["without_best"] and round(x["without_best"], 4) for x in two],
               "groups": [x["groups"] for x in two], "months": [x["years"] for x in two], "check": q[rf.CHECKS[0]]["t"] and round(q[rf.CHECKS[0]]["t"], 2), "passes": q["passes"], "lead": lead(q), "size": q["size"],
               "label": q["label"]["together"] if q["label"] else None, "back": bool(q["label"]["back"]) if q["label"] else None, "same": q["label"]["same"] if q["label"] else None}
        if q["passes"]:  # enough to send the same row again on 2020 to 2024
            row["row"] = {"outcome": int(r["outcome"]), "inputs": [[int(a), int(b)] for a, b in r["inputs"]], "form": r["form"], "where": r["where"] if isinstance(r["where"], str) else [int(x) for x in np.flatnonzero(r["where"])], "level": r.get("level"),
                          "groups": None if r.get("groups") is None else [int(x) for x in r["groups"]], "state": None if r.get("state") is None else [int(x) for x in r["state"]], "weights": r.get("weights"), "event": r["event"]}
        out.append(row)
    answers = [{"passes": q["passes"], "lead": lead(q), "size": q["size"], "t": [q[f]["t"] and round(q[f]["t"], 2) for f in rf.READS]} for q in res["proposals"][: len(told)]]
    return {"bar": res["bar"], "sent": res["sent"], "passed": res["passed"], "leads": sum(x["lead"] for x in out), "answers": answers, "rows": out}, rows


def run(p, v, seed, truth=None):
    """The whole read once on a table: the season step, the swarm on the early months, the steward's rows, the referee."""
    t0 = time.time()
    d = mo.season_out(v[:, :, :LAST])
    board = fd.swarm(fd.view(d, p["group"], FIRST, p["outcomes"], p["allowed"], settings=mo.READ, quiet=mo.QUIET), members())
    t1 = time.time()
    rows = fd.steward(board)
    out = {"seed": seed, "posted": len(board), "swarm_s": round(t1 - t0), "board": reading(p, d, rows, seed)[0]}
    if truth:
        told, kept = reading(p, d, rows, seed, told=[rf.proposal(t["outcome"], [(t["input"], t["lag"])], "slope", t["where"]) for t in truth])
        hit = lambda rs, sent, t: any(q["lead"] and r["outcome"] == t["outcome"] and r["names"] == {t["input"]} for q, r in zip(rs, sent))
        ranks = [next((n for n, r in enumerate(sorted((r for r in board if r["outcome"] == t["outcome"]), key=lambda r: -r["lift"])) if r["names"] == {t["input"]}), None) for t in truth]
        out["told"] = told
        out["links"] = [{"outcome": str(p["ids"][t["outcome"]]), "input": str(p["ids"][t["input"]]), "lag": t["lag"], "share": t["share"], "places": int(t["where"].sum()), "heard": hit(out["board"]["rows"], rows, t), "heard_told": hit(told["rows"], kept, t),
                         "answer": a["lead"], "answer_pass": a["passes"], "answer_size": a["size"], "answer_t": a["t"], "rank": k, "sent": any(r["outcome"] == t["outcome"] and r["names"] == {t["input"]} for r in rows)} for t, a, k in zip(truth, told["answers"], ranks)]
    return {**out, "seconds": round(time.time() - t0)}


def fmt(x):
    return "none" if x is None or x != x else f"{x:.2f}"


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def keep(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r, default=lambda x: x.tolist()) + "\n").encode())
    os.close(f)


def refuse(when, why):
    """Stop here. Not an assert: those can be switched off."""
    if when:
        sys.exit("refused: " + why)


def only_once(step):
    """A marker made before a step that is run once, so that two commands started together cannot both run it. Made with an exclusive create; never removed by the script."""
    try:
        os.close(os.open(HOLD / f"stage-d-{step}.started", os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644))
    except FileExistsError:
        sys.exit(f"refused: the {step} step has been started")


def marks(rs):
    """For each placebo: registered seeds run, runs with any lead, and whether the mark holds (None until every seed is in). Every placebo and planted run kept is of a registered seed and kept once."""
    out = {}
    for step, seeds in SEEDS.items():
        got = [r["seed"] for r in rs if r["step"] == step]
        refuse(len(got) != len(set(got)) or not set(got) <= set(seeds), f"{step}: a seed kept twice or not registered: {sorted(got)}")
    for step in MOST:
        m = [r for r in rs if r["step"] == step]
        bad = sum(r["board"]["leads"] > 0 for r in m)
        out[step] = (len(m), bad, None if {r["seed"] for r in m} != set(SEEDS[step]) else bad <= MOST[step])
    return out


def confirmed(q, bar):
    """The rule for 2020 to 2024: above the bar for one row and something off the baseline's error, both ways it is read, in at least five groups and thirty-six months."""
    return all(q[f]["t"] is not None and q[f]["t"] > bar and q[f]["s"] > 0 and q[f]["groups"] >= CONFIRMED[0] and q[f]["years"] >= CONFIRMED[1] for f in rf.READS)


def show(x):
    return f"{x['names']} ({', '.join(x['sets'])}) -> {x['outcome']}: {x['member']}, {x['form']}, places {x['places']}, lift {x['lift']}, t {x['t']}, s {x['s']}, moving together {x['label']}"


def table():
    rs = rows()
    for step, (n, bad, ok) in marks(rs).items():
        m = [r for r in rs if r["step"] == step]
        print(f"{step}: {n} of {len(SEEDS[step])} runs, {bad} with any lead (at most {MOST[step]}): {'not all run' if ok is None else 'holds' if ok else 'MISSED'}; with any pass {sum(r['board']['passed'] > 0 for r in m)}")
        if m:
            print(f"   rows posted, middle {np.median([r['posted'] for r in m]):.0f}; sent, middle {np.median([r['board']['sent'] for r in m]):.0f}; bar, middle {fmt(np.median([r['board']['bar'] for r in m if r['board']['sent'] and r['board']['bar'] is not None] or [np.nan]))}; seconds, middle {np.median([r['seconds'] for r in m]):.0f}")
            for r in m:
                for x in r["board"]["rows"]:
                    if x["passes"]:
                        print(f"   seed {r['seed']}: {'LEAD' if x['lead'] else 'pass'} {show(x)}")
    m = [r for r in rs if r["step"] == "planted"]
    if m:
        print(f"planted: {len(m)} of {len(SEEDS['planted'])} runs")
        for share in SIZES:
            ls = [x for r in m for x in r["links"] if x["share"] == share]
            print(f"   {share:.0%}: {len(ls)} links; sent {sum(x['sent'] for x in ls)}; heard as a lead from the board {sum(x['heard'] for x in ls)}; a lead when handed over {sum(x['answer'] for x in ls)} (a pass {sum(x['answer_pass'] for x in ls)}); places, middle {np.median([x['places'] for x in ls]):.0f}; rank on its outcome's board, middle {np.median([x['rank'] for x in ls if x['rank'] is not None] or [np.nan]):.0f} ({sum(x['rank'] is None for x in ls)} not posted)")
        named = lambda r, x: any(l["outcome"] == x["outcome"] and x["names"] == [l["input"]] for l in r["links"])
        print(f"   runs with a lead that names no planted link: {sum(any(x['lead'] and not named(r, x) for x in r['board']['rows']) for r in m)}")
    for r in rs:
        if r["step"] == "real":
            b = r["board"]
            print(f"real: {r['posted']} rows posted, {b['sent']} sent, bar {fmt(b['bar'])}, {b['passed']} passed, {b['leads']} of them leads")
            for x in b["rows"]:
                print(f"   {'LEAD' if x['lead'] else 'PASS' if x['passes'] else '    '} {show(x)}")
        if r["step"] == "confirm":
            for x in r["rows"]:
                print(f"confirm: {x['names']} -> {x['outcome']} ({'lead' if x['lead'] else 'moving together'}): {'confirmed' if x['confirmed'] else 'not confirmed'}, bar {fmt(x['bar'])}, t {x['t']}, s {x['s']}, groups {x['groups']}, months {x['months']}")


def rehearse(seeds):
    """A made-up table of the panel's shape, gaps and sets through the whole read: every series a walk of its own, nothing linked. For the time a run takes; prints only."""
    refuse(not all(s in SMOKE for s in seeds), "smoke seeds only")
    p = panel()
    for seed in seeds:
        rng = np.random.default_rng(seed)
        v = 0.2 * rng.normal(size=p["values"].shape).cumsum(axis=2) + rng.normal(size=p["values"].shape)
        v[p["common"]] = v[p["common"]][:, :1]
        v[~np.isfinite(p["values"])] = np.nan  # where each real series has a value, and nothing of the values
        r = run(p, v, seed)
        print(f"seed {seed}: {r['posted']} posted in {r['swarm_s']}s, {r['board']['sent']} sent, bar {fmt(r['board']['bar'])}, {r['board']['passed']} passed, {r['board']['leads']} leads, {r['seconds']}s", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "panel":
        describe(build())
    elif cmd == "rehearse":
        rehearse([int(s) for s in sys.argv[2:]])
    elif cmd == "table":
        table()
    elif cmd in SEEDS:
        p, done = panel(), lambda: {(r["step"], r["seed"]) for r in rows()}
        for seed in [int(s) for s in sys.argv[2:]] or SEEDS[cmd]:
            refuse(seed not in SEEDS[cmd], "registered seeds only")
            if (cmd, seed) in done():
                continue
            v = moved(p, "places" if cmd == "planted" else cmd, seed)
            v, truth = plant(p, v, seed) if cmd == "planted" else (v, None)
            r = {"step": cmd, **run(p, v, seed, truth)}
            if (cmd, seed) in done():  # another process ran the same seed meanwhile: the first kept stands
                continue
            keep(r)
            print(f"{cmd} seed {seed}: {r['posted']} posted, {r['board']['sent']} sent, bar {fmt(r['board']['bar'])}, {r['board']['passed']} passed, {r['board']['leads']} leads" + (f"; heard {sum(x['heard'] for x in r['links'])} of {len(r['links'])}" if truth else "") + f", {r['seconds']}s", flush=True)
    elif cmd == "real" and sys.argv[2:] == ["once"]:
        rs = rows()
        refuse(any(r["step"] == "real" for r in rs), "the real read has been made")
        refuse(not all(ok for _, _, ok in marks(rs).values()), f"the placebo marks do not all hold: {marks(rs)}")
        refuse({r["seed"] for r in rs if r["step"] == "planted"} != set(SEEDS["planted"]), "the planted runs are not all in: a silence could not be read")
        only_once("real")
        p = panel()
        keep({"step": "real", **run(p, p["values"], REAL)})
        table()
    elif cmd == "confirm" and sys.argv[2:] == ["once"]:
        rs = rows()
        refuse(any(r["step"] == "confirm" for r in rs), "2020 to 2024 has been read")
        real = [r for r in rs if r["step"] == "real"]
        refuse(len(real) != 1, "no real read to confirm")
        only_once("confirm")
        p, out = panel(), []
        d = mo.season_out(p["values"])
        for x in real[0]["board"]["rows"]:
            if not x["passes"]:
                continue
            q = x["row"]
            where = q["where"] if isinstance(q["where"], str) else np.isin(np.arange(d.shape[1]), q["where"])
            prop = rf.proposal(q["outcome"], [tuple(i) for i in q["inputs"]], q["form"], where, level=q["level"], groups=None if q["groups"] is None else np.array(q["groups"]), state=None if q["state"] is None else tuple(q["state"]), weights=q["weights"], event=q["event"])
            res = rf.judge(d, p["group"], LAST, [prop], seed=CONFIRM, labels=False, draw=mo.whole_years(LAST), settings=mo.READ, level_fn=fd.level)
            g = res["proposals"][0]
            out.append({"outcome": x["outcome"], "names": x["names"], "lead": x["lead"], "bar": res["bar"], "confirmed": bool(confirmed(g, res["bar"])), **{k: [g[f][k] if k == "groups" else g[f][k] and round(g[f][k], 4) for f in rf.READS] for k in ("t", "s", "without_best", "groups")}, "months": [g[f]["years"] for f in rf.READS]})
        keep({"step": "confirm", "seed": CONFIRM, "rows": out})
        table()
    else:
        sys.exit(__doc__)
