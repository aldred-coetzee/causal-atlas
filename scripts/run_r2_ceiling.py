"""R2 ceiling: the real baseline told the link's exact effect, and the screen's statistic given the exact column. See results/r2-ceiling.md."""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from run_r2 import JOBS, LEAST_S, NULLS, OLD_MARK, PLANTED, ROOT, SPANS_LEAST, THREADS, TIER1, TREES, load, spent_jobs, synth, windows
from causal_atlas import detector as d, screen as c, twin as w  # noqa: E402

OUT = Path(os.environ.get("R2_CEILING", ROOT / "results" / "r2-ceiling-exact.jsonl"))  # the first pass, r2-ceiling.jsonl, used the invalid ratio
KEEP = ROOT / "data" / "panel" / "r2-refs"


def signal(seed, lat, lon):
    """The exact link effect, log(rate / rate_no_link), for a planted seed."""
    g = synth.generate(PLANTED, lat, lon, seed)
    out = np.zeros_like(g["rate"])
    ok = (g["rate"] > 0) & (g["rate_no_link"] > 0)
    out[ok] = np.log(g["rate"][ok] / g["rate_no_link"][ok])
    return out


def heard(y, rstar, z, block, months, cap=c.COUNT_CAP):
    """Does the unshifted T beat all 32 shifts, by form, and the unshifted T over the shifts' mean."""
    counts = np.minimum(y[:, months], cap) if cap else y[:, months]
    e = counts.astype(float) - rstar
    n = block.max() + 1
    t = np.zeros((len(c.FORMS), len(c.SHIFTS) + 1))
    for j, k in enumerate((0, *c.SHIFTS)):
        zz = (d.circular_shift(z, k) if k else z)[:, months]
        u = np.bincount(block, np.einsum("ij,ij->i", e, zz), n)
        v = np.bincount(block, np.einsum("ij,ij,ij->i", rstar, zz, zz), n)
        t[:, j] = c.statistic(u, v)
    return {f: dict(beats=bool(t[i, 0] > t[i, 1:].max()), ratio=float(t[i, 0] / t[i, 1:].mean())) for i, f in enumerate(c.FORMS)}


def one(panel, seed):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y = g["y"]
    block = w.blocks_of(lat, lon)
    sched = windows()[0]
    months = np.arange(TIER1[0], TIER1[1] + 1)
    r = w.references(y, lat, lon, schedule=sched, trees=(TREES,))["R"][TREES]
    KEEP.mkdir(parents=True, exist_ok=True)
    np.save(KEEP / f"R_{panel}_{seed}.npy", r[:, months].astype(np.float32))
    z = signal(seed, lat, lon)
    rstar = w.rescaled(y, r, block, sched)
    row = dict(panel=panel, seed=seed)
    row["C"] = heard(y, rstar, z, block, months)
    row["C_uncapped"] = heard(y, rstar, z, block, months, cap=None)
    row["C_oracle"] = heard(y, w.rescaled(y, g["rate_no_link"], block, sched), z, block, months)
    row["B"] = w.level_free(y, r * np.exp(z), r, block, sched)
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def launch(job):
    panel, seed = job
    if any(x["panel"] == panel and x["seed"] == seed for x in rows()):
        return
    env = dict(os.environ, OMP_NUM_THREADS=str(THREADS))
    code = subprocess.run(["nice", "-n", "19", sys.executable, __file__, "one", panel, str(seed)], env=env).returncode
    print("done" if code == 0 else f"FAILED ({code})", panel, seed, flush=True)


def clears(b):
    return b["S"] >= LEAST_S and b["ci"][0] > 0 and b["raw"] > 0 and sum(s > 0 for s in b["by_span"]) >= SPANS_LEAST


def summary():
    found = rows()
    planted = [x for x in found if x["panel"] == PLANTED]
    nulls = [x for x in found if x["panel"] in NULLS]
    print(len(planted), "planted", len(nulls), "null")
    for x in sorted(planted, key=lambda x: x["seed"]):
        b = x["B"]
        print(x["seed"], f"B {b['S']:.4f} [{b['ci'][0]:.4f}, {b['ci'][1]:.4f}] raw {b['raw']:.4f} spans+ {sum(s > 0 for s in b['by_span'])}", "clears" if clears(b) else "-")
    print("B clears", sum(clears(x["B"]) for x in planted), "S>=0.02", sum(x["B"]["S"] >= OLD_MARK for x in planted), "median S", round(float(np.median([x["B"]["S"] for x in planted])), 4))
    print("B on nulls: clears", sum(clears(x["B"]) for x in nulls), "median S", round(float(np.median([x["B"]["S"] for x in nulls])), 4))
    for name in ("C", "C_uncapped", "C_oracle"):
        for f in c.FORMS:
            print(name, f, "planted", sum(x[name][f]["beats"] for x in planted), "null", sum(x[name][f]["beats"] for x in nulls),
                  "median ratio planted", round(float(np.median([x[name][f]["ratio"] for x in planted])), 2), "null", round(float(np.median([x[name][f]["ratio"] for x in nulls])), 2))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "one":
        one(sys.argv[2], int(sys.argv[3]))
    elif mode == "run":
        jobs = spent_jobs()
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, jobs[:20]))
        with ThreadPoolExecutor(JOBS) as pool:
            list(pool.map(launch, jobs[20:]))
        print("FINISHED", flush=True)
    else:
        summary()
