"""How strong must a link be for blind search to find it. Steps: `check`, `smoke`, `run`, then `summary`. See results/framework-curve.md."""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_r2 import JOBS, NULLS, ROOT, THREADS, TREES, load, world, synth
from run_r2_ceiling import heard, signal
from run_shortlist import METHODS, REFS, TRUE, chosen_by
from run_stage1 import TABLES as STAGE1, names_of
from causal_atlas import bench as b, screen as c, twin as w  # noqa: E402
from causal_atlas.refit import spans

OUT = Path(os.environ.get("CURVE", ROOT / "results" / "framework-curve.jsonl"))
KEEP = ROOT / "data" / "panel" / "curve"
STRENGTHS = ("1.40", "2.00", "3.50", "6.00", "10.00")
LENGTHS = (96, 240)
FIRST = 195
SEEDS, NULL_SEEDS = range(9001, 9016), range(9001, 9006)
SMOKE = 9901
SERIES = 32
PANELS = [f"planted_{s}" for s in STRENGTHS] + NULLS


def schedule(n):
    return spans(FIRST, FIRST + n - 1, 24)


def read_length(y, series, r, block, z, panel, seed, n, g):
    """Every reading at one length. r holds all 240 months as cells by T; a length uses its first spans."""
    sched = schedule(n)
    months = np.arange(FIRST, FIRST + n)
    half = n // 2
    rstar = w.rescaled(y, r, block, sched)
    whole = c.table(series, y, rstar, block, months, cap=None)
    early = c.table(series, y, rstar[:, :half], block, months[:half], cap=None)
    late = c.table(series, y, rstar[:, half:], block, months[half:], cap=None)
    KEEP.mkdir(parents=True, exist_ok=True)
    np.savez(KEEP / f"tables_{panel}_{seed}_{n}.npz", whole=whole.astype(np.float32), early=early.astype(np.float32), late=late.astype(np.float32))
    names = names_of(SERIES)
    key = seed * 10 + PANELS.index(panel) if panel in PANELS else seed * 10
    out = dict(exact={f: v["beats"] for f, v in heard(y, rstar, z, block, months, cap=None).items()}, size=b.link_share(g["rate"][:, months], g["rate_no_link"][:, months]), forms={})
    for i, form in enumerate(c.FORMS):
        here = dict(search=b.read_world(b.claims(whole[i], names), TRUE), true_only=b.read_world(b.claims(whole[i, : 2 * c.PER_SERIES], names), TRUE))
        for method in METHODS:
            held = chosen_by(method, early[i], key, i)
            here[method] = dict(held_true=any(x // c.PER_SERIES < 2 for x in held), **b.read_world(b.claims(late[i], names, chosen=held), TRUE))
        out["forms"][form] = here
    return out


def baseline(y, lat, lon):
    return w.references(y, lat, lon, schedule=schedule(max(LENGTHS)), trees=(TREES,))["R"][TREES]


def link_of(panel, seed, g, lat, lon):
    """The exact effect. A null has none, so it is read against the 3.50 link of the same seed, a false alarm rate."""
    if not panel.startswith("planted_"):
        return signal(seed, lat, lon)
    ok = (g["rate"] > 0) & (g["rate_no_link"] > 0)
    z = np.zeros_like(g["rate"])
    z[ok] = np.log(g["rate"][ok] / g["rate_no_link"][ok])
    return z


def one(panel, seed):
    t0 = time.time()
    y, lat, lon, series = world(panel, seed)
    g = synth.generate(panel, lat, lon, seed)
    block = w.blocks_of(lat, lon)
    r = baseline(y, lat, lon)
    KEEP.mkdir(parents=True, exist_ok=True)
    np.save(KEEP / f"R_{panel}_{seed}.npy", r[:, FIRST : FIRST + max(LENGTHS)].astype(np.float32))
    t1 = time.time()
    z = link_of(panel, seed, g, lat, lon)
    row = dict(panel=panel, seed=seed, lengths={str(n): read_length(y, series, r, block, z, panel, seed, n, g) for n in LENGTHS}, baseline_s=round(t1 - t0), total_s=round(time.time() - t0))
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")


def check():
    """Seed 3001 at 3.50, a spent seed: R and the 96-month table must match what is saved."""
    panel, seed = "planted_3.50", 3001
    y, lat, lon, series = world(panel, seed)
    block = w.blocks_of(lat, lon)
    r = baseline(y, lat, lon)
    saved = np.load(REFS / f"R_{panel}_{seed}.npy")
    print("R largest relative difference", np.max(np.abs(r[:, FIRST : FIRST + 96] - saved) / np.maximum(saved, 1e-6)), flush=True)
    months = np.arange(FIRST, FIRST + 96)
    t = c.table(series, y, w.rescaled(y, r, block, schedule(96)), block, months, cap=None)
    old = np.load(STAGE1 / f"uncapped_{panel}_{seed}.npy")
    print("table largest relative difference", np.max(np.abs(t - old) / np.maximum(np.abs(old), 1e-6)))


def jobs():
    return [(p, s) for p in NULLS for s in NULL_SEEDS] + [(f"planted_{x}", s) for x in ("3.50", "6.00", "2.00", "10.00", "1.40") for s in SEEDS]


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(job):
    panel, seed = job
    if any(x["panel"] == panel and x["seed"] == seed for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", panel, str(seed)], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", panel, seed, flush=True)


def counted(found, want, n, form, method, key):
    return sum(x["lengths"][str(n)]["forms"][form][method][key] for x in found if x["panel"] in want)


def summary():
    found = rows()
    print(len(found), "of", len(jobs()), "worlds")
    missing = [j for j in jobs() if not any(x["panel"] == j[0] and x["seed"] == j[1] for x in found)]
    if missing:
        print("not finished", missing)
    print("truth plug-in", sum(b.read_world([dict(input="own0", lead=True)], TRUE)["first_true"] for _ in found), "of", len(found))
    print("baseline seconds, median", np.median([x["baseline_s"] for x in found]), "total", np.median([x["total_s"] for x in found]))
    nulls = len([x for x in found if x["panel"] in NULLS])
    for n in LENGTHS:
        print("length", n, "nulls", nulls)
        for form in c.FORMS:
            print(" ", form, "named on nulls", {m: counted(found, NULLS, n, form, m, "named") for m in ("search", "true_only", *METHODS)}, "exact on nulls", sum(x["lengths"][str(n)]["exact"][form] for x in found if x["panel"] in NULLS))
        for s in STRENGTHS:
            p = [f"planted_{s}"]
            here = [x for x in found if x["panel"] in p]
            size = np.median([x["lengths"][str(n)]["size"] for x in here]) if here else float("nan")
            print(f"  strength {s}, {len(here)} worlds, link share of events, median {size:.3f}")
            for form in c.FORMS:
                print("   ", form, {m: counted(found, p, n, form, m, "first_true") for m in ("search", "true_only", *METHODS)}, "exact", sum(x["lengths"][str(n)]["exact"][form] for x in here))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "one":
        one(sys.argv[2], int(sys.argv[3]))
    elif mode == "check":
        check()
    elif mode == "smoke":
        for panel in ("planted_3.50", "planted_10.00"):
            launch((panel, SMOKE))
        print("FINISHED", flush=True)
    elif mode == "run":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, jobs()))
        print("FINISHED", flush=True)
    else:
        summary()
