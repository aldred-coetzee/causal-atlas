"""R1: twin forecasts, limits and level-free score on spent seeds. `run` does every row, `summary` prints the gate. See results/r1-twin.md."""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_refit_marks import ROOT, d, load, noise_inputs, synth
from causal_atlas import twin as w  # noqa: E402
from causal_atlas.refit import spans

OUT = Path(os.environ.get("R1_OUT", ROOT / "results" / "r1-twin.jsonl"))
SHIFTS = ROOT / "results" / "refit-shifts.jsonl"
PLANTED = "planted_3.50"
PLANTED_SEEDS = range(3001, 3021)
NULLS = ["pure_null", "shared_null", "combo_null"]
NULL_SEEDS = range(3001, 3006)
CALIBRATED = (3011, 3002, 3008)
FALSE_GAIN_SEEDS = (3007, 3010)
FALSE_GAIN = 0.08  # takes 3007's six and 3010's two, one of them just under 0.085
FALSE_GAIN_COUNT = 8
LATER = (291, 386)
RATIO = (0.5, 2.0)
RATIO_NEEDED = 18
SHIFT_LIMIT = 0.02
JOBS = 2
THREADS = 3


def false_gain_years(seed):
    rows = (json.loads(x) for x in SHIFTS.read_text().splitlines())
    row = next(x for x in rows if x["seed"] == seed)
    return [s["years"] for s in row["shifts"] if s["skill"] >= FALSE_GAIN]


def jobs():
    """Every row of the rule, as (panel, seed). A seed's noise row goes with its real row."""
    return [(PLANTED, s) for s in PLANTED_SEEDS] + [(p, s) for p in NULLS for s in NULL_SEEDS] + [("pure_null", 3007)]


def row_of(y, r, m, block, sched, refs, inputs, panel, seed):
    out = dict(panel=panel, seed=seed, inputs=inputs, by_trees={})
    later = [x for x in sched if x[0] >= LATER[0] and x[1] <= LATER[1]]
    i = np.concatenate([np.arange(s, e + 1) for s, e in sched])
    obs = y[:, i].sum()
    for t in refs["trees"]:
        full = w.level_free(y, m[t], r[t], block, sched)
        full["ratio_r"] = float(r[t][:, i].sum() / obs)
        full["ratio_m"] = float(m[t][:, i].sum() / obs)
        full["blown"] = [s for s, e in sched if w.blown(r[t], y, s, e) or w.blown(m[t], y, s, e)]
        if later:
            part = w.level_free(y, m[t], r[t], block, later)
            full["later"] = dict(S=part["S"], ci=part["ci"], raw=part["raw"])
        out["by_trees"][str(t)] = full
    out["factor_share"] = [round(b["factor_share"], 5) for b in refs["blocks"]]
    out["cap_share"] = [round(b["cap_share"], 6) for b in refs["blocks"]]
    return out


def one(panel, seed, schedule=None, years=None):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    sched = schedule or spans()
    block = w.blocks_of(lat, lon)
    started = time.time()
    refs = w.references(y, lat, lon, schedule=sched)
    r = refs["R"]
    rows = [row_of(y, r, w.test_panel(refs, drought, oni), block, sched, refs, "real", panel, seed)]
    if panel == "pure_null" and seed == 3007:
        rows.append(row_of(y, r, w.test_panel(refs, *noise_inputs(seed, *y.shape)), block, sched, refs, "noise", panel, seed))
    years = (false_gain_years(seed) if panel == PLANTED and seed in FALSE_GAIN_SEEDS else []) if years is None else years
    shifted = []
    for k in years:
        m = w.test_panel(refs, d.circular_shift(drought, k), d.circular_shift(oni, k))
        shifted.append(dict(years=k, S={str(t): w.level_free(y, m[t], r[t], block, sched, interval=False)["S"] for t in refs["trees"]}))
    rows[0]["shifts"] = shifted
    for row in rows:
        row["seconds"] = round(time.time() - started, 1)
    return rows


def choose_trees(rows):
    """The smallest count at which each calibrated row keeps at least half its S at 100. Pure."""
    found = {x["seed"]: x["by_trees"] for x in rows if x["panel"] == PLANTED and x["seed"] in CALIBRATED}
    for t in w.TREES[:-1]:
        if all(found[s][str(t)]["S"] >= 0.5 * found[s][str(w.TREES[-1])]["S"] for s in CALIBRATED):
            return t
    return w.TREES[-1]


def gate(rows):
    """R1's four conditions for going on to R2, at the chosen tree count. Pure, so a cold session can rerun it."""
    done = {(x["panel"], x["seed"]) for x in rows}
    if any(j not in done for j in jobs()):
        return dict(verdict="incomplete", missing=[j for j in jobs() if j not in done])
    t = str(choose_trees(rows))
    planted = [x for x in rows if x["panel"] == PLANTED]
    in_range = sum(RATIO[0] <= x["by_trees"][t]["ratio_r"] <= RATIO[1] for x in planted)
    shifts = [s["S"][t] for x in planted for s in x["shifts"]]
    calibrated = [x["by_trees"][t]["S"] for x in planted if x["seed"] in CALIBRATED]
    checks = dict(ratio=in_range >= RATIO_NEEDED, shifts=len(shifts) == FALSE_GAIN_COUNT and all(v < SHIFT_LIMIT for v in shifts), calibrated=all(v > 0 for v in calibrated))
    return dict(verdict="go on" if all(checks.values()) else "stop", trees=int(t), in_range=in_range, shifts=shifts, calibrated=calibrated, checks=checks)


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(job):
    """One failed row is reported, and leaves the gate incomplete."""
    panel, seed = job
    if any(x["panel"] == panel and x["seed"] == seed for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", panel, str(seed)], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", panel, seed, flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["run", "one", "summary", "smoke"])
    ap.add_argument("panel", nargs="?")
    ap.add_argument("seed", type=int, nargs="?")
    args = ap.parse_args()
    if args.mode == "run":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, jobs()))
        print("FINISHED", json.dumps(gate(rows())), flush=True)
    elif args.mode == "one":
        found = one(args.panel, args.seed)
        with OUT.open("a") as f:
            f.write("".join(json.dumps(x) + "\n" for x in found))
    elif args.mode == "summary":
        for x in rows():
            t = x["by_trees"][str(w.TREES[-1])]
            print(x["panel"], x["seed"], x["inputs"], "S", round(t["S"], 4), "raw", round(t["raw"], 4), "R/obs", round(t["ratio_r"], 3), "blown", t["blown"], x["seconds"])
        print(json.dumps(gate(rows())))
    else:  # one span of a seed outside the rule, written nowhere, to show the code runs and time it
        started = time.time()
        found = one("pure_null", 9001, schedule=[(195, 218)], years=[2])
        print(json.dumps(found[0]["by_trees"]["25"])[:400], found[0]["shifts"], "seconds", round(time.time() - started, 1))
