"""The second read across the real table: the yearly panel of the first read with every series written as its change from the year before in the same place. The rule and the marks are in results/stage-c-second-read.md, committed before any run; decision 0067.

    run_stage_c.py places | years | planted   the placebo and known-answer runs on the changed table, each registered seed once, a row a run
    run_stage_c.py real once                  the real read: refused unless both placebo marks hold and the planted runs are in, and refused a second time
    run_stage_c.py confirm once               what passed, read on the last ten years
    run_stage_c.py table                      the runs against their marks

The panel, the ties, the swarm, the steward, the referee and the rule for the last ten years are the first read's (run_stage_b.py), unchanged. What is new is here: the changed table, the order in which a table is rearranged, planted and changed, the seeds and the file the runs are kept in.
"""
import sys

import numpy as np

import run_stage_b as sb
from causal_atlas import referee as rf

OUT = sb.ROOT / "results" / "stage-c-second-read.jsonl"
SEEDS = {"places": range(64001, 64021), "years": range(64101, 64109), "planted": range(64201, 64213)}
MOST = {"places": 2, "years": 1}  # runs with any pass, at most
REAL, CONFIRM = 64900, 64901  # the referee's draws for the real read and for the last ten years
LAST = sb.LAST

# the first read's bookkeeping (rows, keep, once, marks, table) reads these names from its own module: point them at this read's file, seeds and marks
sb.OUT, sb.SEEDS, sb.MOST = OUT, SEEDS, MOST


def change(v):
    """Each series as its change from the year before in the same place: missing where either year is missing, and in the first year."""
    out = np.full(v.shape, np.nan)
    out[..., 1:] = v[..., 1:] - v[..., :-1]
    return out


def changed(p, how=None, seed=None, plant=False):
    """The changed table, with the links between its sets broken when asked.

    how None: the table as it is, changed. places: crops, exchange rates and drought each with their own reordering of the places; links planted, if asked, in the values as they stand (levels, as in the count on made-up tables); then every series changed; then the common series moved round in years. years: every series changed, then each set but the World Bank's moved round by its own number of years, any two sets at least sb.APART years apart. Years are moved round after the change, so no change is taken across a seam, and within the years before LAST only: nothing of 2015 to 2024 enters the years a placebo, a planted run or the real read sees."""
    v, sets, common, truth = p["values"].copy(), p["sets"], p["common"], None
    if how is None:
        return change(v), truth
    rng = np.random.default_rng(seed)
    if how == "places":
        for k in (sets == "crops", sets == "exchange rates", (sets == "climate") & ~common):
            v[k] = v[k][:, rng.permutation(v.shape[1])]
        by = int(rng.integers(sb.ROUND[0], sb.ROUND[1] + 1))
        if plant:
            v, truth = sb.plant(p, v, seed)
        v = change(v)
        v[common, :, :LAST] = np.roll(v[common][:, :, :LAST], by, axis=2)
        return v, truth
    sb.refuse(how != "years" or plant, "no such rearrangement")
    v = change(v)
    while True:
        by = [0] + [int(x) for x in rng.integers(1, LAST, 3)]
        if all(min((a - b) % LAST, (b - a) % LAST) >= sb.APART for i, a in enumerate(by) for b in by[:i]):
            break
    for k, shift in zip(("crops", "exchange rates", "climate"), by[1:]):
        v[sets == k, :, :LAST] = np.roll(v[sets == k][:, :, :LAST], shift, axis=2)
    return v, truth


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "table":
        sb.table()
    elif cmd in SEEDS:
        p, done = sb.panel(), lambda: {(r["step"], r["seed"]) for r in sb.rows()}
        for seed in [int(s) for s in sys.argv[2:]] or SEEDS[cmd]:
            sb.refuse(seed not in SEEDS[cmd], "registered seeds only")
            if (cmd, seed) in done():
                continue
            v, truth = changed(p, "places" if cmd == "planted" else cmd, seed, plant=cmd == "planted")
            r = {"step": cmd, **sb.run(p, v, seed, truth)}
            if (cmd, seed) in done():  # another process ran the same seed meanwhile: the first kept stands
                continue
            sb.keep(r)
            print(f"{cmd} seed {seed}: {r['posted']} posted, {r['board']['sent']} sent, bar {sb.fmt(r['board']['bar'])}, {r['board']['passed']} passed" + (f"; heard {sum(x['heard'] for x in r['links'])} of {len(r['links'])}" if truth else "") + f", {r['seconds']}s", flush=True)
    elif cmd == "real" and sys.argv[2:] == ["once"]:
        rs = sb.rows()
        sb.refuse(any(r["step"] == "real" for r in rs), "the real read has been made")
        sb.refuse(not all(ok for _, _, ok in sb.marks(rs).values()), f"the placebo marks do not all hold: {sb.marks(rs)}")
        sb.refuse({r["seed"] for r in rs if r["step"] == "planted"} != set(SEEDS["planted"]), "the planted runs are not all in: a silence could not be read")
        p = sb.panel()
        sb.keep({"step": "real", **sb.run(p, changed(p)[0], REAL)})
        sb.table()
    elif cmd == "confirm" and sys.argv[2:] == ["once"]:
        rs = sb.rows()
        sb.refuse(any(r["step"] == "confirm" for r in rs), "the last ten years have been read")
        real = [r for r in rs if r["step"] == "real"]
        sb.refuse(len(real) != 1, "no real read to confirm")
        p, out = sb.panel(), []
        v = changed(p)[0]
        for x in real[0]["board"]["rows"]:
            if not x["passes"]:
                continue
            q = x["row"]
            where = q["where"] if isinstance(q["where"], str) else np.isin(np.arange(v.shape[1]), q["where"])
            prop = rf.proposal(q["outcome"], [tuple(i) for i in q["inputs"]], q["form"], where, level=q["level"], groups=None if q["groups"] is None else np.array(q["groups"]), state=None if q["state"] is None else tuple(q["state"]), weights=q["weights"], event=q["event"])
            res = rf.judge(v, p["group"], LAST, [prop], seed=CONFIRM, labels=False)
            g = res["proposals"][0]
            out.append({"outcome": x["outcome"], "names": x["names"], "label": x["label"], "bar": res["bar"], "confirmed": bool(sb.confirmed(g, res["bar"])), **{k: [g[f][k] if k in ("groups", "years") else g[f][k] and round(g[f][k], 4) for f in rf.READS] for k in ("t", "s", "without_best", "groups", "years")}})
        sb.keep({"step": "confirm", "seed": CONFIRM, "rows": out})
        sb.table()
    else:
        sys.exit(__doc__)
