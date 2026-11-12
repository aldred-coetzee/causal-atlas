"""Independent reader's checks on made-up arrays only (stage D rule check, 2026-11-12). No real panel is opened.
Seeds used: 59001 to 59006. Run under ulimit -v 4000000 with PYTHONPATH=src:scripts.
1. run() end to end on a small made-up table with planted links: the kept row is JSON-safe, and nothing of 2020 to 2024 changes it.
2. `real once` then `confirm once`, executed from the script's own text against a made-up panel in a scratch folder, with the two
   registered seeds replaced by smoke seeds: does the confirm path run and confirm a strong planted link?
3. A mostly-nought outcome with a planted link at share 0.04: how much of the outcome's movement in its quiet months is the plant."""
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

import run_stage_d as sd

S = sd.Path(sd.__file__).read_text()


def made(seed, places=60, ngroups=10):
    rng = np.random.default_rng(seed)
    sets = np.array([sd.STILL] * 4 + ["climate"] * 4 + ["conflict and protest"] * 3 + ["earthquakes"] * 2)
    common = np.array([False, False, True, True, False, False, True, True, False, False, False, False, True])
    n = len(sets)
    v = 0.3 * rng.normal(size=(n, places, sd.MONTHS)).cumsum(axis=2) + rng.normal(size=(n, places, sd.MONTHS))
    v[common] = v[common][:, :1]
    v[8, :, :108] = np.nan  # a late start
    group = np.repeat(np.arange(ngroups), places // ngroups)
    p = {"values": v, "common": common, "group": group, "groups": np.array([f"g{i}" for i in range(ngroups)]), "ids": np.array([f"s{i}" for i in range(n)]), "sets": sets}
    p["allowed"] = sets[:, None] != sets[None, :]
    p["outcomes"] = np.flatnonzero(~common)
    return p


def check1():
    p = made(59001)
    v = sd.moved(p, "places", 59002)
    v, truth = sd.plant(p, v, 59002)
    t0 = time.time()
    r = sd.run(p, v, 59002, truth)
    s = json.dumps({"step": "planted", **r}, default=lambda x: x.tolist())
    print(f"1. run with truth: {r['posted']} posted, {r['board']['sent']} sent, {r['board']['passed']} passed, heard {[x['heard'] for x in r['links']]}, answers {[x['answer'] for x in r['links']]}, json {len(s)} chars, {time.time() - t0:.0f}s")
    w = v.copy()
    w[:, :, sd.LAST:] += 50 * np.random.default_rng(59003).normal(size=w[:, :, sd.LAST:].shape)
    r2 = sd.run(p, w, 59002, truth)
    same = json.dumps(r2["board"], default=lambda x: x.tolist()) == json.dumps(r["board"], default=lambda x: x.tolist()) and json.dumps(r2["told"], default=lambda x: x.tolist()) == json.dumps(r["told"], default=lambda x: x.tolist())
    print(f"   2020 to 2024 changed by noise: board and handed-over reading identical: {same}")


def check2():
    p = made(59004)
    rng = np.random.default_rng(59004)
    o, x, lag = 4, 9, 2  # climate outcome, conflict input
    where = np.isin(p["group"], [0, 1, 2, 3, 4, 5])
    z = (p["values"][x] - np.nanmean(p["values"][x][:, : sd.LAST], axis=1)[:, None])
    z = np.nan_to_num(z / np.nanstd(np.diff(p["values"][x][:, : sd.LAST], axis=1), axis=1)[:, None])
    mv = np.nanstd(np.diff(p["values"][o][:, : sd.LAST], axis=1), axis=1)
    p["values"][o][where, lag:] += 2.0 * mv[where, None] * z[where, :-lag]
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts").mkdir()
        (root / "results").mkdir()
        hold = root / "data" / "panel" / "stage-d"
        hold.mkdir(parents=True)
        np.savez_compressed(hold / "panel.npz", **{k: p[k] for k in ("values", "common", "group", "ids", "sets", "groups")}, places=np.arange(60).astype(str))
        out = root / "results" / "stage-d-monthly-read.jsonl"
        with open(out, "w") as f:
            for step, seeds in sd.SEEDS.items():
                for s in seeds:  # made-up placebo rows so the guards let the read through: no read of anything
                    f.write(json.dumps({"step": step, "seed": s, "board": {"leads": 0, "passed": 0, "sent": 0, "bar": None, "rows": []}, "posted": 0, "seconds": 0, "links": []}) + "\n")
        src = S.replace("REAL, CONFIRM = 66900, 66901", "REAL, CONFIRM = 59005, 59006")
        assert src != S
        for argv in (["x", "real", "once"], ["x", "confirm", "once"], ["x", "real", "once"]):
            sys.argv = argv
            g = {"__name__": "__main__", "__file__": str(root / "scripts" / "run_stage_d.py")}
            try:
                exec(compile(src, "run_stage_d_copy", "exec"), g)
            except SystemExit as e:
                print(f"   {' '.join(argv[1:])}: exit {e.code}")
        rows = [json.loads(s) for s in open(out)]
        real = [r for r in rows if r["step"] == "real"][0]["board"]
        conf = [r for r in rows if r["step"] == "confirm"]
        hit = [x for x in real["rows"] if x["passes"] and x["outcome"] == "s4"]
        print(f"2. real: {real['passed']} passed, {real['leads']} leads; passes on s4: {[(x['names'], x['lead']) for x in hit]}")
        print(f"   confirm: {[(x['names'], x['outcome'], x['confirmed'], x['t'], x['groups'], x['months']) for x in conf[0]['rows']] if conf else 'none'}")


def check3():
    rng = np.random.default_rng(59006)
    T = sd.LAST
    y = np.where(rng.random(T) < 0.06, np.log1p(rng.poisson(5, T)), 0.0)  # an outcome mostly nought
    xs = 0.3 * rng.normal(size=T).cumsum() + rng.normal(size=T)
    mo, mx = np.std(np.diff(y)), np.std(np.diff(xs))
    share, lag = 0.04, 1
    add = np.zeros(T)
    add[lag:] = np.sqrt(share / (1 - share)) * mo * ((xs - xs.mean()) / mx)[:-lag]
    yy = y + add
    quiet = (y == 0)
    q2 = quiet[1:] & quiet[:-1]
    print(f"3. mostly nought outcome, share {share}: share of month-to-month variance from the plant overall {np.var(np.diff(add)) / np.var(np.diff(yy)):.3f}; in months quiet before and after {np.var(np.diff(add)[q2]) / np.var(np.diff(yy)[q2]):.3f}; level of plant against outcome's own level spread {np.std(add) / np.std(y):.2f}")


if __name__ == "__main__":
    which = sys.argv[1:] or ["1", "2", "3"]
    for k in which:
        {"1": check1, "2": check2, "3": check3}[k]()
