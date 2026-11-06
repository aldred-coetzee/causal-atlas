"""R2 check: the screen with the gate corrected, at three search sizes. Saves T tables. See results/r2-check.md."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_r2 import HEARS_LEAST, JOBS, PLANTED, QUIET_MOST, ROOT, THREADS, TIER1, TREES, names_true, prepared, rows, spent_jobs, windows
from causal_atlas import screen as c, twin as w  # noqa: E402

OUT = Path(os.environ.get("R2_CHECK", ROOT / "results" / "r2-check.jsonl"))
TABLES = ROOT / "data" / "panel" / "r2-tables"
SIZES = (1280, 320, 80)


def row_of(panel, seed, t):
    row = dict(panel=panel, seed=seed, sizes={})
    for size in SIZES:
        row["sizes"][str(size)] = {}
        for i, form in enumerate(c.FORMS):
            leads, top, z = c.gate(t[i, :size])
            row["sizes"][str(size)][form] = dict(leads=leads, top=top, z=z, named=bool(leads), true=names_true(leads), top_true=names_true(top))
    return row


def one(panel, seed):
    y, series, refs, block = prepared(panel, seed, windows()[0])
    months = np.arange(TIER1[0], TIER1[1] + 1)
    t = c.table(series, y, w.rescaled(y, refs["R"][TREES], block, windows()[0]), block, months)
    TABLES.mkdir(parents=True, exist_ok=True)
    np.save(TABLES / f"{panel}_{seed}.npy", t.astype(np.float32))
    with OUT.open("a") as f:
        f.write(json.dumps(row_of(panel, seed, t)) + "\n")


def launch(job):
    panel, seed = job
    if any(x["panel"] == panel and x["seed"] == seed for x in rows(OUT)):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", panel, str(seed)], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", panel, seed, flush=True)


def reading(found):
    """Counts and verdict per size and form. Pure."""
    planted = [x for x in found if x["panel"] == PLANTED]
    nulls = [x for x in found if x["panel"] != PLANTED]
    out = {}
    for size in SIZES:
        for form in c.FORMS:
            get = lambda x: x["sizes"][str(size)][form]  # noqa: E731
            named, true = sum(get(x)["named"] for x in nulls), sum(get(x)["true"] for x in planted)
            out[f"{size} {form}"] = dict(null_named=named, planted_true=true, top5=sum(get(x)["top_true"] for x in planted), top5_null=sum(get(x)["top_true"] for x in nulls),
                                         quiet=named <= QUIET_MOST, hears=true >= HEARS_LEAST)
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "one":
        one(sys.argv[2], int(sys.argv[3]))
    elif mode == "run":
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, spent_jobs()))
        print("FINISHED", flush=True)
    else:
        found = rows(OUT)
        print(len(found), "worlds")
        for k, v in reading(found).items():
            print(k, json.dumps(v))
