"""The growing refit's marks on fresh seeds. `marks` runs everything in order, `summary` prints the outcome so far. See results/refit-marks.md."""
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
from run_1b_third import noise_inputs  # noqa: E402

OUT = Path(os.environ.get("REFIT_MARKS_OUT", ROOT / "results" / "refit-marks.jsonl"))
NULLS = ["pure_null", "shared_null", "combo_null"]
PLANTED = "planted_3.50"
SEEDS = range(3001, 3021)
BAND, MARGIN, QUIET_NEEDED, HEARS_NEEDED, FALSE_ALLOWED, SHUFFLE_ALWAYS = 0.005, 0.02, 18, 16, 1, 3
PERMS = 19
SECONDARY_END = 386
JOBS, THREADS = 2, 3
CEILING = 36 * 3600


def scored(y, m, ref, last=r.SCORED[1]):
    i = np.arange(r.SCORED[0], last + 1)
    obs, mi, ri = y[:, i].astype(float), m[:, i], ref[:, i]
    return obs, mi, ri


def score(y, m, ref, trees1):
    obs, mi, ri = scored(y, m, ref)
    low, high = (0.0, 0.0) if not any(trees1) else d.block_interval(obs, mi, ri)
    o2, m2, r2 = scored(y, m, ref, SECONDARY_END)
    low2, high2 = (0.0, 0.0) if not any(trees1) else d.block_interval(o2, m2, r2)
    return dict(skill=float(d.skill(obs, mi, ri)), ci=[low, high], second_skill=float(d.skill(o2, m2, r2)), second_ci=[low2, high2],
                trees1=trees1, by_span=[round(float(d.skill(y[:, s : e + 1].astype(float), m[:, s : e + 1], ref[:, s : e + 1])), 4) for s, e in r.spans()],
                total_obs=float(obs.sum()), total_ref=float(ri.sum()), total_m=float(mi.sum()))


def first_pass(panel, seed):
    """One row per kind of input. R does not depend on the inputs, so a null's two kinds share it."""
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    started = time.time()
    refs = r.references(y, lat, lon)
    ref = r.reference_panel(refs)
    out = []
    for kind in ("real", "noise") if panel != PLANTED else ("real",):
        dr, on = (drought, oni) if kind == "real" else noise_inputs(seed, *y.shape)
        m, trees1, _ = r.test_panel(refs, dr, on)
        out.append(dict(stage="first", panel=panel, seed=seed, inputs=kind, trees0=[b["trees0"] for b in refs["blocks"]], **score(y, m, ref, trees1)))
    for row in out:
        row["seconds"] = round(time.time() - started, 1)
    return out


def shuffled(panel, seed, total_ref, limit=None):
    """Shuffled skills on real-shaped inputs. R is refitted; its total must match the first pass."""
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    started = time.time()
    refs = r.references(y, lat, lon)
    ref = r.reference_panel(refs)
    obs, _, ri = scored(y, ref, ref)
    assert abs(ri.sum() - total_ref) < 1e-6 * total_ref, "R differs from the first pass"
    schemes = dict(circular=[(d.circular_shift(drought, i), d.circular_shift(oni, i)) for i in range(1, d.SHIFTS + 1)],
                   permutation=[(d.year_permutation(drought, 5000 + i), d.year_permutation(oni, 5000 + i)) for i in range(PERMS)])
    out = dict(stage="shuffled", panel=panel, seed=seed, inputs="real")
    for scheme, pairs in schemes.items():
        values, counts = [], []
        for dr, on in pairs[:limit]:
            m, trees1, _ = r.test_panel(refs, dr, on)
            values.append(float(d.skill(obs, m[:, r.SCORED[0] : r.SCORED[1] + 1], ri)))
            counts.append(sum(trees1))
        out[scheme], out[scheme + "_total_trees_median"] = values, float(np.median(counts))
    out["seconds"] = round(time.time() - started, 1)
    return out


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def met_first(x):
    return x["skill"] >= MARGIN and x["ci"][0] > 0


def outcome(all_rows):
    """The marks, from the rows so far. Pure, so it can be tested and rerun by a cold session."""
    first = {(x["panel"], x["seed"], x["inputs"]): x for x in all_rows if x["stage"] == "first"}
    shuf = {(x["panel"], x["seed"]): x for x in all_rows if x["stage"] == "shuffled"}
    quiet = {(p, k): sum(abs(first[(p, s, k)]["skill"]) <= BAND for s in SEEDS if (p, s, k) in first) for p in NULLS for k in ("real", "noise")}
    a_done = all((p, s, k) in first for p in NULLS for s in SEEDS for k in ("real", "noise"))
    a_pass = a_done and all(v >= QUIET_NEEDED for v in quiet.values())
    planted = [first[(PLANTED, s, "real")] for s in SEEDS if (PLANTED, s, "real") in first]
    crit1 = sum(met_first(x) for x in planted)

    def detected(panel, scheme):
        n = 0
        for s in SEEDS:
            x, y = first.get((panel, s, "real")), shuf.get((panel, s))
            if x and y and d.verdict(x["skill"], x["ci"][0], y[scheme])["all"]:
                n += 1
        return n

    schemes = {}
    for scheme in ("circular", "permutation"):
        hears, false = detected(PLANTED, scheme), {p: detected(p, scheme) for p in NULLS}
        schemes[scheme] = dict(hears=hears, false=false, qualifies=hears >= HEARS_NEEDED and all(v <= FALSE_ALLOWED for v in false.values()))
    chosen = "circular" if schemes["circular"]["qualifies"] else "permutation" if schemes["permutation"]["qualifies"] else None
    return dict(quiet={f"{p} {k}": v for (p, k), v in quiet.items()}, a_done=a_done, a_pass=a_pass, planted_run=len(planted), planted_meeting_first=crit1, schemes=schemes, chosen=chosen)


def to_shuffle(all_rows):
    """Which replicates need shuffles, as the rule says."""
    first = [x for x in all_rows if x["stage"] == "first" and x["inputs"] == "real"]
    always = list(SEEDS)[:SHUFFLE_ALWAYS]
    jobs = [(p, s) for p in NULLS for s in always] + [(PLANTED, s) for s in always]
    jobs += [(x["panel"], x["seed"]) for x in first if x["panel"] != PLANTED and met_first(x)]
    planted = [x for x in first if x["panel"] == PLANTED and met_first(x)]
    if len(planted) >= HEARS_NEEDED:
        jobs += [(x["panel"], x["seed"]) for x in planted]
    return sorted(set(jobs))


def launch(args):
    mode, panel, seed = args
    have = rows()
    if mode == "first" and any(x["stage"] == "first" and x["panel"] == panel and x["seed"] == seed for x in have):
        return
    if mode == "shuffled" and any(x["stage"] == "shuffled" and x["panel"] == panel and x["seed"] == seed for x in have):
        return
    if time.time() - STARTED > CEILING:
        print("over the ceiling, not starting", mode, panel, seed, flush=True)
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    subprocess.run(["nice", "-n", "19", sys.executable, __file__, mode, panel, str(seed)], check=True, env=env)
    print("done", mode, panel, seed, flush=True)


STARTED = time.time()


def marks():
    with ThreadPoolExecutor(JOBS) as pool:
        list(pool.map(launch, [("first", p, s) for p in NULLS for s in SEEDS]))
        result = outcome(rows())
        print(json.dumps(result), flush=True)
        if not result["a_pass"]:
            print("A MISSED: stopping, no planted panel runs" if result["a_done"] else "A INCOMPLETE", flush=True)
            return
        list(pool.map(launch, [("first", PLANTED, s) for s in SEEDS]))
        list(pool.map(launch, [("shuffled", p, s) for p, s in to_shuffle(rows())]))
    result = outcome(rows())
    print(json.dumps(result), flush=True)
    print("FINISHED: A and B PASSED under " + result["chosen"] if result["chosen"] else "FINISHED: B MISSED", flush=True)


def append(row):
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["marks", "summary", "first", "shuffled", "smoke"])
    ap.add_argument("panel", nargs="?")
    ap.add_argument("seed", type=int, nargs="?")
    args = ap.parse_args()
    if args.mode == "marks":
        marks()
    elif args.mode == "summary":
        print(json.dumps(outcome(rows()), indent=1))
    elif args.mode == "first":
        for row in first_pass(args.panel, args.seed):
            append(row)
    elif args.mode == "shuffled":
        x = next(x for x in rows() if x["stage"] == "first" and x["panel"] == args.panel and x["seed"] == args.seed)
        append(shuffled(args.panel, args.seed, x["total_ref"]))
    else:  # a spent seed through both paths, one draw per scheme, to show the code runs and repeats refit-dev
        for row in first_pass("pure_null", 2001):
            append(row)
        x = rows()[0]
        append(shuffled("pure_null", 2001, x["total_ref"], limit=1))
