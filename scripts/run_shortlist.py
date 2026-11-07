"""Framework Stage 1, third method: shortlist on earlier months, test on later months. Steps: `toy`, `dev`, then `summary`. Step 3 is not here until step 2 says go on. See results/framework-shortlist.md."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_r2 import JOBS, NULLS, PLANTED, ROOT, THREADS, load, spent_jobs, windows, world
from run_r2_ceiling import heard, signal
from run_stage1 import DECOY_SEEDS, DECOYS, TOY_NULLS, TOY_PLANTED, names_of, toy_baseline, toy
from causal_atlas import bench as b, screen as c, twin as w  # noqa: E402

OUT = Path(os.environ.get("SHORTLIST", ROOT / "results" / "framework-shortlist.jsonl"))
REFS = ROOT / "data" / "panel" / "r2-refs"
TABLES = ROOT / "data" / "panel" / "shortlist-tables"
EARLY, LATE = np.arange(195, 243), np.arange(243, 291)
N = 5
SERIES = 32
TRUE = {"own0", "own1"}
METHODS = ("shortlist", "oracle", "floor")


def chosen_by(method, early, seed, form):
    if method == "shortlist":
        return b.shortlist(early, N)
    if method == "oracle":
        return b.shortlist(early[: 2 * c.PER_SERIES], 2)
    rng = np.random.default_rng([seed, form])
    return [int(s) * c.PER_SERIES + int(rng.integers(c.PER_SERIES)) for s in rng.choice(SERIES, N, replace=False)]


def read(early, late, seed):
    names = names_of(SERIES)
    out = {}
    for i, form in enumerate(c.FORMS):
        out[form] = {}
        for method in METHODS:
            held = chosen_by(method, early[i], seed, i)
            found = b.claims(late[i], names, chosen=held)
            out[form][method] = dict(held=[names[x // c.PER_SERIES] for x in held], held_true=any(x // c.PER_SERIES < 2 for x in held), claims=found, **b.read_world(found, TRUE))
    return out


def append(row):
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")


def toy_one(linked, seed):
    _, lat, lon = load()
    lat, lon = lat[::5], lon[::5]
    g = toy.generate(lat, lon, seed, linked=linked)
    series = [g["a"], g["b"]]
    for s in np.random.default_rng(seed + 880000).choice(DECOY_SEEDS, DECOYS, replace=False):
        series += list(toy.inputs(len(lat), int(s)))
    block = w.blocks_of(lat, lon)
    residual = g["y"] - toy_baseline(g["y"])
    y = residual / residual[:, : c.BEFORE].std() + 1
    one = np.ones((len(lat), len(EARLY)))
    early, late = c.table(series, y, one, block, EARLY, cap=None), c.table(series, y, one, block, LATE, cap=None)
    row = dict(step="toy", panel="planted" if linked else "null", seed=seed, forms=read(early, late, seed))
    row["exact"] = {f: v["beats"] for f, v in heard(y, one, g["exact"], block, LATE, cap=None).items()}
    append(row)


def dev_one(panel, seed):
    y, lat, lon, series = world(panel, seed)
    r = np.full(y.shape, np.nan)
    r[:, np.arange(195, 291)] = np.load(REFS / f"R_{panel}_{seed}.npy")
    block = w.blocks_of(lat, lon)
    rstar = w.rescaled(y, r, block, windows()[0])
    a, z = rstar[:, : len(EARLY)], rstar[:, len(EARLY) :]
    early, late = c.table(series, y, a, block, EARLY, cap=None), c.table(series, y, z, block, LATE, cap=None)
    TABLES.mkdir(parents=True, exist_ok=True)
    np.savez(TABLES / f"{panel}_{seed}.npz", early=early.astype(np.float32), late=late.astype(np.float32))
    row = dict(step="dev", panel=panel, seed=seed, forms=read(early, late, seed))
    row["exact"] = {f: v["beats"] for f, v in heard(y, z, signal(seed, lat, lon), block, LATE, cap=None).items()}
    append(row)


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(job):
    step, panel, seed = job
    if any(x["step"] == step and x["panel"] == panel and x["seed"] == seed for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", step, panel, str(seed)], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", step, panel, seed, flush=True)


def summary():
    found = rows()
    for step in ("toy", "dev"):
        here = [x for x in found if x["step"] == step]
        planted = [x for x in here if x["panel"] in ("planted", PLANTED)]
        nulls = [x for x in here if x["panel"] not in ("planted", PLANTED)]
        print(step, len(planted), "planted", len(nulls), "null")
        if not here:
            continue
        print("  truth plug-in", sum(b.read_world([dict(input="own0", lead=True)], TRUE)["first_true"] for _ in here), "of", len(here))
        for method in METHODS:
            forms = {f: b.tally([x["forms"][f][method] for x in planted], [x["forms"][f][method] for x in nulls]) for f in c.FORMS}
            for f, v in forms.items():
                held = sum(x["forms"][f][method]["held_true"] for x in planted), sum(x["forms"][f][method]["held_true"] for x in nulls)
                print(f"  {method} {f}: first true {v['first_true']}/{v['planted']}, any {v['any_true']}, held true {held[0]} (nulls {held[1]}), named on nulls {v['null_named']}/{v['nulls']}")
            if method == "shortlist":
                form = b.choose_form(forms)
                print("  chosen", form, "line met" if form and b.step_two(forms[form]) else "line missed")
        print("  exact, later months", {f: (sum(x["exact"][f] for x in planted), sum(x["exact"][f] for x in nulls)) for f in c.FORMS})
        if step == "toy":
            print("  global input claimed", {f: sum(k["input"] == "own1" for x in planted for k in x["forms"][f]["shortlist"]["claims"]) for f in c.FORMS})


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "one":
        step, panel, seed = sys.argv[2], sys.argv[3], int(sys.argv[4])
        toy_one(panel == "planted", seed) if step == "toy" else dev_one(panel, seed)
    elif mode == "toy":
        jobs = [("toy", "planted", s) for s in TOY_PLANTED] + [("toy", "null", s) for s in TOY_NULLS]
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, jobs))
        print("FINISHED", flush=True)
    elif mode == "dev":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, [("dev", p, s) for p, s in spent_jobs()]))
        print("FINISHED", flush=True)
    else:
        summary()
