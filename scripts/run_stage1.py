"""Framework Stage 1. Steps in order: `toy`, `dev`, then `summary`. Step 3's fresh seeds are not here until step 2 says go on. See results/framework-stage-1.md."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_r2 import JOBS, NULLS, PLANTED, ROOT, THREADS, TIER1, load, spent_jobs, windows, world
from causal_atlas import bench as b, screen as c, twin as w  # noqa: E402

sys.path.insert(0, str(ROOT / "synth"))
import toy  # noqa: E402

OUT = Path(os.environ.get("STAGE1", ROOT / "results" / "framework-stage-1.jsonl"))
REFS = ROOT / "data" / "panel" / "r2-refs"
TABLES = ROOT / "data" / "panel" / "stage1-tables"
SAVED = ROOT / "data" / "panel" / "r2-tables"
MONTHS = np.arange(TIER1[0], TIER1[1] + 1)
METHODS = {"capped": c.COUNT_CAP, "uncapped": None}
TOY_PLANTED, TOY_NULLS = range(7001, 7021), range(7001, 7016)
DECOY_SEEDS = range(8001, 8061)
DECOYS = 15
SIZES = (1280, 320, 80)


def names_of(n):
    return [f"own{i}" for i in range(2)] + [f"decoy{i}" for i in range(n - 2)]


def read_table(t):
    """Each form's claims and reading against the world's own 2 series, at each search size."""
    out = {}
    for size in SIZES:
        cols = size // c.PER_SERIES
        out[str(size)] = {}
        for i, form in enumerate(c.FORMS):
            found = b.claims(t[i, :size], names_of(cols))
            out[str(size)][form] = dict(claims=found, **b.read_world(found, {"own0", "own1"}))
    return out


def append(row):
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")


def toy_baseline(y):
    """Month means and a pooled AR term at three months, fitted before month 195, in plain code."""
    months = np.arange(y.shape[1])
    means = np.stack([y[:, (months % 12 == m) & (months < c.BEFORE)].mean(axis=1) for m in range(12)], axis=1)
    a = y - means[:, months % 12]
    phi = (a[:, 3 : c.BEFORE] * a[:, : c.BEFORE - 3]).sum() / (a[:, : c.BEFORE - 3] ** 2).sum()
    r = means[:, months % 12].copy()
    r[:, 3:] += phi * a[:, :-3]
    return r


def toy_one(linked, seed):
    _, lat, lon = load()
    lat, lon = lat[::5], lon[::5]
    g = toy.generate(lat, lon, seed, linked=linked)
    series = [g["a"], g["b"]]
    for s in np.random.default_rng(seed + 880000).choice(DECOY_SEEDS, DECOYS, replace=False):
        series += list(toy.inputs(len(lat), int(s)))
    block = w.blocks_of(lat, lon)
    residual = g["y"] - toy_baseline(g["y"])
    variance = residual[:, : c.BEFORE].var()
    shifted = residual / np.sqrt(variance) + 1  # the statistic reads e = y - rstar with variance rstar, so rstar = 1
    rstar = np.ones((len(lat), len(MONTHS)))
    t = c.table(series, shifted, rstar, block, MONTHS, cap=None)
    row = dict(step="toy", panel="planted" if linked else "null", seed=seed, method="screen", sizes=read_table(t))
    z = g["exact"]
    row["exact"] = hears(shifted, rstar, z, block, None)
    row["ceiling_S"] = float(1 - ((residual[:, MONTHS] - (z[:, MONTHS] if linked else 0)) ** 2).sum() / (residual[:, MONTHS] ** 2).sum())
    append(row)


def hears(y, rstar, z, block, cap):
    """Does the method's statistic, handed the exact column, beat all 32 shifts, by form. Null worlds get the planted world's column."""
    from causal_atlas import detector as d

    e = (np.minimum(y[:, MONTHS], cap) if cap else y[:, MONTHS]) - rstar
    n = block.max() + 1
    t = np.zeros((len(c.FORMS), len(c.SHIFTS) + 1))
    for j, k in enumerate((0, *c.SHIFTS)):
        zz = (d.circular_shift(z, k) if k else z)[:, MONTHS]
        t[:, j] = c.statistic(np.bincount(block, np.einsum("ij,ij->i", e, zz), n), np.bincount(block, np.einsum("ij,ij,ij->i", rstar, zz, zz), n))
    return {f: bool(t[i, 0] > t[i, 1:].max()) for i, f in enumerate(c.FORMS)}


def dev_one(panel, seed, method):
    if method == "capped":  # the table the check already built, read the same way
        t = np.load(SAVED / f"{panel}_{seed}.npy")
        append(dict(step="dev", panel=panel, seed=seed, method=method, sizes=read_table(t)))
        return
    y, lat, lon, series = world(panel, seed)
    r = np.full(y.shape, np.nan)
    r[:, MONTHS] = np.load(REFS / f"R_{panel}_{seed}.npy")
    block = w.blocks_of(lat, lon)
    sched = windows()[0]
    t = c.table(series, y, w.rescaled(y, r, block, sched), block, MONTHS, cap=METHODS[method])
    TABLES.mkdir(parents=True, exist_ok=True)
    np.save(TABLES / f"{method}_{panel}_{seed}.npy", t.astype(np.float32))
    totals = [float(np.nansum(r[:, s : e + 1]) / max(y[:, s : e + 1].sum(), 1)) for s, e in sched]
    append(dict(step="dev", panel=panel, seed=seed, method=method, sizes=read_table(t), r_over_obs=totals))


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(job):
    step, panel, seed, method = job
    if any(x["step"] == step and x["panel"] == panel and x["seed"] == seed and x["method"] == method for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", step, panel, str(seed), method], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", step, panel, seed, method, flush=True)


def by_form(found, method, size):
    planted = [x for x in found if x["method"] == method and x["panel"] in ("planted", PLANTED)]
    nulls = [x for x in found if x["method"] == method and x["panel"] not in ("planted", PLANTED)]
    return {f: b.tally([x["sizes"][size][f] for x in planted], [x["sizes"][size][f] for x in nulls]) for f in c.FORMS}


def summary():
    found = rows()
    for step, methods in (("toy", ["screen"]), ("dev", list(METHODS))):
        here = [x for x in found if x["step"] == step]
        print(step, len(here), "rows")
        for method in methods:
            for size in map(str, SIZES):
                forms = by_form(here, method, size)
                print(" ", method, size, json.dumps(forms))
                if step == "dev" and size == "1280" and here:
                    form = b.choose_form(forms)
                    print("  chosen", form, "go on" if form and b.step_two(forms[form]) else "stop")
        if step == "toy" and here:
            planted = [x for x in here if x["panel"] == "planted"]
            print("  exact heard", {f: sum(x["exact"][f] for x in planted) for f in c.FORMS}, "null", {f: sum(x["exact"][f] for x in here if x["panel"] == "null") for f in c.FORMS})
            print("  ceiling S median", round(float(np.median([x["ceiling_S"] for x in planted])), 4))
        ratios = [v for x in here for v in x.get("r_over_obs", []) if x["panel"] in NULLS]
        if ratios:
            print("  R over observed on nulls: spans outside 0.2 to 5:", sum(not 0.2 <= v <= 5 for v in ratios), "of", len(ratios))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "one":
        step, panel, seed, method = sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
        if step == "toy":
            toy_one(panel == "planted", seed)
        else:
            dev_one(panel, seed, method)
    elif mode == "toy":
        jobs = [("toy", "planted", s, "screen") for s in TOY_PLANTED] + [("toy", "null", s, "screen") for s in TOY_NULLS]
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, jobs))
        print("FINISHED", flush=True)
    elif mode == "dev":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, [("dev", p, s, m) for m in METHODS for p, s in spent_jobs()]))
        print("FINISHED", flush=True)
    else:
        summary()
