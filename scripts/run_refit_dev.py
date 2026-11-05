"""The growing refit's development test, spent seeds only. One replicate, or `dev` for all of them and the outcome. See results/refit-dev.md."""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d, refit as r  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

OUT = ROOT / "results" / "refit-dev.jsonl"
NULLS = [("pure_null", s) for s in (2001, 2002, 2003, 9001, 9002, 9003, 9004, 9005)]
PLANTED = [("planted_3.00", s) for s in (1011, 1016, 1017)]
TIMED = {("pure_null", 2001), ("planted_3.00", 1016)}
BAND, MARGIN, NEEDED = 0.005, 0.02, 2
SHUFFLES = d.SHIFTS + 19
JOBS, THREADS = 2, 3


def replicate(panel, seed, timed):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    started = time.time()
    refs = r.references(y, lat, lon)
    reference_seconds = round(time.time() - started, 1)
    m, trees1, g1_seconds = r.test_panel(refs, drought, oni)
    ref = r.reference_panel(refs)
    i = np.arange(r.SCORED[0], r.SCORED[1] + 1)
    obs, mi, ri = y[:, i].astype(float), m[:, i], ref[:, i]
    low, high = (0.0, 0.0) if not any(trees1) else d.block_interval(obs, mi, ri)
    out = dict(panel=panel, seed=seed, skill=float(d.skill(obs, mi, ri)), ci=[low, high],
               trees0=[b["trees0"] for b in refs["blocks"]], trees1=trees1,
               by_span=[round(float(d.skill(y[:, s : e + 1].astype(float), m[:, s : e + 1], ref[:, s : e + 1])), 4) for s, e in r.spans()],
               total_obs=float(obs.sum()), total_ref=float(ri.sum()), total_m=float(mi.sum()),
               reference_seconds=reference_seconds, reference_span_seconds=[b["seconds"] for b in refs["blocks"]],
               g1_span_seconds=g1_seconds, threads=os.environ.get("OMP_NUM_THREADS"))
    if timed:
        started = time.time()
        r.test_panel(refs, d.circular_shift(drought, 1), d.circular_shift(oni, 1))
        out["one_shuffle_seconds"] = round(time.time() - started, 1)
        out["projected_shuffled_replicate_hours"] = round((reference_seconds + sum(g1_seconds) + SHUFFLES * out["one_shuffle_seconds"]) / 3600, 2)
    return out


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(job):
    panel, seed = job
    if any(x["panel"] == panel and x["seed"] == seed for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    subprocess.run(["nice", "-n", "19", sys.executable, __file__, panel, str(seed)] + (["--timed"] if job in TIMED else []), check=True, env=env)
    print("done", panel, seed, flush=True)


def dev():
    with ThreadPoolExecutor(JOBS) as pool:
        list(pool.map(launch, NULLS + PLANTED))
    got = {(x["panel"], x["seed"]): x for x in rows()}
    quiet = sum(abs(got[j]["skill"]) <= BAND for j in NULLS)
    hears = sum(got[j]["skill"] >= MARGIN and got[j]["ci"][0] > 0 for j in PLANTED)
    print(f"quiet {quiet} of {len(NULLS)} (all needed); hears {hears} of {len(PLANTED)} ({NEEDED} needed)")
    print("PASSED" if quiet == len(NULLS) and hears >= NEEDED else "MISSED")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("panel")
    ap.add_argument("seed", type=int, nargs="?")
    ap.add_argument("--timed", action="store_true")
    args = ap.parse_args()
    if args.panel == "dev":
        dev()
    else:
        line = json.dumps(replicate(args.panel, args.seed, args.timed))
        with OUT.open("a") as f:
            f.write(line + "\n")
