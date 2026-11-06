"""After-the-fact diagnostic: does the planted gain vanish when the inputs are shifted? `run` does the six rows, `summary` prints the reading. See results/refit-shifts.md."""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_refit_marks import PLANTED, ROOT, THREADS, d, load, r, scored, synth

MARKS = ROOT / "results" / "refit-marks.jsonl"
OUT = Path(os.environ.get("REFIT_SHIFTS_OUT", ROOT / "results" / "refit-shifts.jsonl"))
OVERSHOT, CALIBRATED = (3010, 3014, 3007), (3011, 3002, 3008)
YEARS = range(2, 33, 2)  # 16 of the 32 shifts, spread across the same range
KEEPS, LOSES = 0.5, 0.25
JOBS = 2


def marks_row(panel, seed):
    rows = (json.loads(x) for x in MARKS.read_text().splitlines())
    return next(x for x in rows if x["stage"] == "first" and x["panel"] == panel and x["seed"] == seed)


def shifted(panel, seed, years=YEARS):
    first = marks_row(panel, seed)
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    started = time.time()
    refs = r.references(y, lat, lon)
    ref = r.reference_panel(refs)
    obs, _, ri = scored(y, ref, ref)
    assert abs(ri.sum() - first["total_ref"]) < 1e-6 * first["total_ref"], "R differs from the first pass"
    out = []
    for i in years:
        m, trees1, _ = r.test_panel(refs, d.circular_shift(drought, i), d.circular_shift(oni, i))
        mi = m[:, r.SCORED[0] : r.SCORED[1] + 1]
        out.append(dict(years=i, skill=float(d.skill(obs, mi, ri)), total_m=float(mi.sum()), trees1=trees1))
    return dict(panel=panel, seed=seed, skill=first["skill"], total_obs=first["total_obs"], total_ref=first["total_ref"], shifts=out, seconds=round(time.time() - started, 1))


def state(skill, values):
    """One row: does it keep its skill with the inputs shifted? Pure."""
    median = float(np.median(values))
    return "keeps" if median >= KEEPS * skill else "loses" if median <= LOSES * skill else "between"


def reading(rows):
    """The rule's reading of the two groups. Pure, so it can be tested and rerun by a cold session."""
    found = {x["seed"]: state(x["skill"], [s["skill"] for s in x["shifts"]]) for x in rows}
    count = lambda group, what: sum(found.get(s) == what for s in group)
    if len(found) < len(OVERSHOT) + len(CALIBRATED):
        verdict = "incomplete"
    elif count(CALIBRATED, "keeps") >= 2:
        verdict = "not hearing the link"
    elif count(CALIBRATED, "loses") >= 2 and count(OVERSHOT, "keeps") >= 2:
        verdict = "baseline"
    elif count(CALIBRATED, "loses") >= 2 and count(OVERSHOT, "loses") >= 2:
        verdict = "margin"
    else:
        verdict = "mixed"
    return dict(rows=found, verdict=verdict)


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(seed):
    """One failed replicate is reported and does not end the others."""
    if any(x["seed"] == seed for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", str(seed)], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", seed, flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["run", "one", "summary", "smoke"])
    ap.add_argument("seed", type=int, nargs="?")
    args = ap.parse_args()
    if args.mode == "run":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, OVERSHOT + CALIBRATED))
        print("FINISHED", json.dumps(reading(rows())), flush=True)
    elif args.mode == "one":
        row = shifted(PLANTED, args.seed)
        with OUT.open("a") as f:
            f.write(json.dumps(row) + "\n")
    elif args.mode == "summary":
        for x in rows():
            values = [s["skill"] for s in x["shifts"]]
            print(x["seed"], round(x["skill"], 4), "shifted median", round(float(np.median(values)), 4), "max", round(max(values), 4), state(x["skill"], values))
        print(json.dumps(reading(rows())))
    else:  # one shift of a row, written nowhere, to show the code runs and R repeats the first pass
        print(shifted(PLANTED, 3011, years=[2]))
