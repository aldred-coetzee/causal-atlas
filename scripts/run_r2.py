"""R2: screen, gate, decoys. `spent` chooses the form and runs the early stop; `calibrate` measures the mark, only after it. `summary` prints the gate. See results/r2-screen.md."""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_refit_marks import ROOT, load, synth
from causal_atlas import screen as c, twin as w  # noqa: E402
from causal_atlas.refit import spans

SPENT = Path(os.environ.get("R2_SPENT", ROOT / "results" / "r2-screen.jsonl"))
CALIBRATION = Path(os.environ.get("R2_CALIBRATION", ROOT / "results" / "r2-calibration.jsonl"))
FIRST_PASS = SPENT.with_name("r2-screen-first.jsonl")
CACHE = ROOT / "data" / "panel" / "decoys"
TREES = 25  # frozen by R1
PLANTED = "planted_3.50"
NULLS = ["pure_null", "shared_null", "combo_null"]
DECOY_POOL = range(6001, 6061)
DECOY_WORLDS = 15
TIER1 = (195, 290)
TIER2 = (291, 386)
OWN = 2  # the world's own series come first
QUIET_MOST = 2
HEARS_LEAST = 16
LEAST_S = 0.005  # the lowest m can be
SPANS_LEAST = 3
MARK_FLOOR = 0.005
OLD_MARK = 0.02
JOBS = 2
THREADS = 3


def spent_jobs():
    return [(PLANTED, s) for s in range(3001, 3021)] + [(p, s) for p in NULLS for s in range(3001, 3006)]


def calibration_jobs():
    return [(p, s) for p in NULLS for s in range(5001, 5021)]


def decoy(seed, lat, lon):
    """One decoy world's two inputs. Cached, written by rename; two processes doing it at once is harmless."""
    path = CACHE / f"{seed}.npz"
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        g = synth.generate("pure_null", lat, lon, seed)
        tmp = CACHE / f"{seed}.{os.getpid()}.tmp.npz"
        np.savez(tmp, drought=g["drought"].astype(np.float32), oni=g["oni"].astype(np.float32))
        tmp.replace(path)
    with np.load(path) as f:
        return [f["drought"], f["oni"]]


def world(panel, seed):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    series = [g["drought"], g["oni"]]
    for s in np.random.default_rng(seed + 880000).choice(DECOY_POOL, DECOY_WORLDS, replace=False):
        series += decoy(int(s), lat, lon)
    return g["y"], lat, lon, series


def windows():
    sched = spans()
    return [x for x in sched if x[1] <= TIER1[1]], [x for x in sched if TIER2[0] <= x[0] and x[1] <= TIER2[1]]


def names_true(cols):
    return any(x // c.PER_SERIES < OWN for x in cols)


def prepared(panel, seed, schedule):
    y, lat, lon, series = world(panel, seed)
    return y, series, w.references(y, lat, lon, schedule=schedule, trees=(TREES,)), w.blocks_of(lat, lon)


def screened(panel, seed, parts):
    started = time.time()
    y, series, refs, block = parts
    months = np.arange(TIER1[0], TIER1[1] + 1)
    t = c.table(series, y, w.rescaled(y, refs["R"][TREES], block, windows()[0]), block, months)
    row = dict(panel=panel, seed=seed, cols=t.shape[1], forms={})
    for i, form in enumerate(c.FORMS):
        leads, top, z = c.gate(t[i])
        row["forms"][form] = dict(leads=leads, top=top, z=z, named=bool(leads), true=names_true(leads), top_true=names_true(top[:1]))
    row["seconds_screen"] = round(time.time() - started, 1)
    return row


def score(y, m, refs, block, sched):
    r = refs["R"][TREES]
    out = w.level_free(y, m, r, block, sched)
    out["blown"] = [s for s, e in sched if w.blown(r, y, s, e) or w.blown(m, y, s, e)]
    return out


def tier2(row, form, parts):
    y, series, refs, block = parts
    second = windows()[1]
    found = row["forms"][form]
    row["form"] = form
    row["forced"] = score(y, c.lead_panel(refs, series, found["top"], TIER2)[TREES], refs, block, second)
    row["gated"] = None
    if found["leads"]:
        same = len(found["leads"]) == len(found["top"])
        row["gated"] = row["forced"] if same else score(y, c.lead_panel(refs, series, found["leads"], TIER2)[TREES], refs, block, second)
    return row


def rows(path=SPENT):
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


def choose_form(found):
    """Most planted worlds naming a true column, among forms naming a lead in at most 2 null worlds; ties to fewer named on nulls, then the order of FORMS. Pure."""
    table = []
    for i, form in enumerate(c.FORMS):
        true = sum(x["forms"][form]["true"] for x in found if x["panel"] == PLANTED)
        named = sum(x["forms"][form]["named"] for x in found if x["panel"] != PLANTED)
        if named <= QUIET_MOST:
            table.append((-true, named, i, form))
    return min(table)[3] if table else None


def passes(x):
    """Tier 2's conditions 1 to 3, at the lowest m can be. Shifts can only take rows away."""
    return bool(x) and x["S"] >= LEAST_S and x["ci"][0] > 0 and x["raw"] > 0 and sum(v > 0 for v in x["by_span"]) >= SPANS_LEAST


def early_stop(found):
    """Stop before calibrating unless the screen and the pipeline reach R3's own counts on spent seeds. Pure."""
    done = {(x["panel"], x["seed"]) for x in found if "forced" in x}
    if any(j not in done for j in spent_jobs()):
        return dict(verdict="incomplete", missing=len([j for j in spent_jobs() if j not in done]))
    form = found[0]["form"]
    planted = [x for x in found if x["panel"] == PLANTED]
    nulls = [x for x in found if x["panel"] != PLANTED]
    true = sum(x["forms"][form]["true"] for x in planted)
    named = sum(x["forms"][form]["named"] for x in nulls)
    pipeline = sum(passes(x["gated"]) and x["forms"][form]["true"] for x in planted)
    forced = sum(passes(x["forced"]) for x in planted)
    blown = sum(bool(x["forced"]["blown"]) for x in found)
    checks = dict(hears_screen=true >= HEARS_LEAST, quiet_screen=named <= QUIET_MOST, hears_pipeline=pipeline >= HEARS_LEAST)
    return dict(verdict="go on" if all(checks.values()) else "stop", form=form, true=true, named=named, pipeline=pipeline, forced=forced, blown=blown, checks=checks,
                forced_null=sum(passes(x["forced"]) for x in nulls), by_form={f: [sum(x["forms"][f]["true"] for x in planted), sum(x["forms"][f]["named"] for x in nulls)] for f in c.FORMS})


def mark(found):
    """m from the 60 calibration worlds, forced top 5. Pure."""
    values = sorted((x["forced"]["S"] for x in found), reverse=True)
    return dict(m=max(MARK_FLOOR, values[1]), second=values[1], largest=values[0], worlds=len(values), at_old_mark=sum(v >= OLD_MARK for v in values), named=sum(x["forms"][x["form"]]["named"] for x in found))


def launch(args):
    stage, panel, seed, out, form = args
    if any(x["panel"] == panel and x["seed"] == seed and (stage == "screen" or "forced" in x) for x in rows(out)):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", stage, panel, str(seed), str(out), form], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", stage, panel, seed, flush=True)


def append(row, out):
    with out.open("a") as f:
        f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["spent", "calibrate", "one", "summary", "smoke"])
    ap.add_argument("rest", nargs="*")
    args = ap.parse_args()
    if args.mode == "one":
        stage, panel, seed, out, form = args.rest
        first, second = windows()
        parts = prepared(panel, int(seed), first if stage == "screen" else first + second)
        earlier = [x for x in rows(FIRST_PASS) if x["panel"] == panel and x["seed"] == int(seed)]
        row = earlier[0] if earlier else screened(panel, int(seed), parts)
        append(row if stage == "screen" else tier2(row, form, parts), Path(out))
    elif args.mode == "spent":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, [("screen", p, s, FIRST_PASS, "") for p, s in spent_jobs()]))
        form = choose_form(rows(FIRST_PASS))
        print("FORM", form, flush=True)
        if form:
            with ThreadPoolExecutor(JOBS) as pool:
                list(pool.map(launch, [("tier2", p, s, SPENT, form) for p, s in spent_jobs()]))
            print("FINISHED", json.dumps(early_stop(rows())), flush=True)
    elif args.mode == "calibrate":
        gate = early_stop(rows())
        if gate["verdict"] != "go on":
            sys.exit(f"the early stop says {gate['verdict']}: {gate}")
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, [("tier2", p, s, CALIBRATION, gate["form"]) for p, s in calibration_jobs()]))
        print("FINISHED", json.dumps(mark(rows(CALIBRATION))), flush=True)
    elif args.mode == "summary":
        for x in rows():
            f = x["forms"][x["form"]]
            print(x["panel"], x["seed"], "leads", [(v // c.PER_SERIES, v % c.PER_SERIES) for v in f["leads"]], "true", f["true"], "z", round(f["z"][0], 2),
                  "forced S", round(x["forced"]["S"], 4), "gated S", x["gated"] and round(x["gated"]["S"], 4), "blown", x["forced"]["blown"], x["seconds_screen"])
        print(json.dumps(early_stop(rows())))
        if CALIBRATION.exists():
            print(json.dumps(mark(rows(CALIBRATION))))
    else:  # a seed outside the rule, written nowhere, to time the screen
        started = time.time()
        first, second = windows()
        parts = prepared("pure_null", 9001, first + second)
        print("references", round(time.time() - started, 1), flush=True)
        row = screened("pure_null", 9001, parts)
        print("screen", row["seconds_screen"], flush=True)
        tier2(row, "all", parts)
        print("all", round(time.time() - started, 1), {k: row["forms"][k]["named"] for k in c.FORMS})
