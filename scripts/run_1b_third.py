"""The 1b third design. One replicate, or `marks` to run mark A and, only if it passes, mark B. See results/1b-known-answer.md."""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d, nested as n  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

FIRST, MID, LAST_TRAIN = 36, 146, 194
SCORED = (195, 434)
SECONDARY_END = 386
PERMS = 19
OUT = ROOT / "results" / "1b-third-replicates.jsonl"
NULLS = ["pure_null", "shared_null", "combo_null"]
DESCRIBED = ["planted_3.00", "planted_2.40", "planted_combo_6"]
SEEDS = range(3001, 3021)
SHUFFLE_ALWAYS = 3
BAND, QUIET_NEEDED = 0.005, 18
CEILING = 14 * 3600


def noise_inputs(seed, cells, T):
    rng = np.random.default_rng(seed + 770000)
    return rng.normal(size=(cells, T)).astype(np.float32), rng.normal(size=T).astype(np.float32)


def replicate(panel, seed, inputs="real", level=True, always_shuffle=False):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    if inputs == "noise":
        drought, oni = noise_inputs(seed, *y.shape)
    cells, T = y.shape
    tau = np.arange(FIRST, T)
    target = y[:, tau].ravel().astype(float)
    month = np.tile(tau, cells)
    fit1, stop, fit2 = month <= MID, (month > MID) & (month <= LAST_TRAIN), month <= LAST_TRAIN
    everything = np.ones(len(target), bool)
    base = d.base_features(y, lat, lon)
    started = time.time()

    def baseline(rows):
        raw = d.fit_predict(base, target.astype(np.float32), rows, everything).astype(float)
        full = np.zeros((cells, T))
        full[:, FIRST:] = raw.reshape(cells, len(tau))
        adjusted = raw
        if level:
            adjusted = raw * n.level_factor(y, full, lat, lon, FIRST)[:, FIRST:].ravel()
        return raw, np.maximum(adjusted, n.FLOOR)

    raw1, b1 = baseline(fit1)
    raw2, b2 = baseline(fit2)
    where = np.repeat(np.stack([lat, lon], axis=1), len(tau), axis=0).astype(np.float32)

    def plain(ref):
        return np.hstack([where, np.log(ref)[:, None].astype(np.float32)])

    trees0 = n.choose_trees(plain(b1), target, b1, fit1, stop)
    r1 = n.apply_trees(plain(b1), target, b1, fit1, trees0)
    r2 = n.apply_trees(plain(b2), target, b2, fit2, trees0)
    x1, x2 = plain(r1), plain(r2)

    def test_model(dr, on):
        a = np.hstack([x1, d.input_features(dr, on, train_months=(FIRST, MID))])
        b = np.hstack([x2, d.input_features(dr, on, train_months=(FIRST, LAST_TRAIN))])
        trees = n.choose_trees(a, target, r1, fit1, stop)
        return n.apply_trees(b, target, r2, fit2, trees), trees

    score = month >= SCORED[0]
    obs = target[score].reshape(cells, -1)
    ref = r2[score].reshape(cells, -1)
    cut = dict(main=obs.shape[1], secondary=SECONDARY_END - SCORED[0] + 1)

    def skills(m):
        return {k: float(d.skill(obs[:, :c], m[:, :c], ref[:, :c])) for k, c in cut.items()}

    m_full, trees1 = test_model(drought, oni)
    m = m_full[score].reshape(cells, -1)
    out = dict(panel=panel, seed=seed, inputs=inputs, level=level, trees0=trees0, trees1=trees1,
               dev_b_raw=n.deviance(obs, raw2[score].reshape(cells, -1)), dev_b_level=n.deviance(obs, b2[score].reshape(cells, -1)),
               total_obs=float(obs.sum()), total_ref=float(ref.sum()), total_m=float(m.sum()), shuffled=False)
    first = {}
    for k, c in cut.items():
        low, high = (0.0, 0.0) if trees1 == 0 else d.block_interval(obs[:, :c], m[:, :c], ref[:, :c])
        s = float(d.skill(obs[:, :c], m[:, :c], ref[:, :c]))
        no = dict(first=False, second=None, third=None, all=False)
        out[k] = dict(skill=s, ci=[low, high], circular=no, permutation=no)
        first[k] = s >= 0.02 and low > 0
    if inputs == "real" and (always_shuffle or any(first.values())):
        schemes = dict(circular=[(d.circular_shift(drought, i), d.circular_shift(oni, i)) for i in range(1, d.SHIFTS + 1)],
                       permutation=[(d.year_permutation(drought, 5000 + i), d.year_permutation(oni, 5000 + i)) for i in range(PERMS)])
        out.update(shuffled=True, shuffled_for_secondary_only=not always_shuffle and not first["main"])
        for scheme, pairs in schemes.items():
            values, counts = [], []
            for dr, on in pairs:
                full, used = test_model(dr, on)
                values.append(skills(full[score].reshape(cells, -1)))
                counts.append(used)
            for k in cut:
                v = [x[k] for x in values]
                out[k][scheme] = d.verdict(out[k]["skill"], out[k]["ci"][0], v)
                out[k][scheme + "_median"], out[k][scheme + "_max"] = float(np.median(v)), max(v)
            out[scheme + "_trees_median"] = float(np.median(counts))
    out["seconds"] = round(time.time() - started, 1)
    if panel.startswith("planted"):
        a, c = synth.lead_rates(panel, lat, lon, seed, lead=3)
        for k, end in (("main", SCORED[1]), ("secondary", SECONDARY_END)):
            i = np.arange(SCORED[0], end + 1)
            out[k]["worth"] = float(d.skill(y[:, i], a[:, i], c[:, i]))
        linked = g["linked"].any(axis=1) if g["linked"].ndim > 1 else g["linked"]
        out.update(linked_share=float(linked.mean()),
                   linked_rate_share=float(g["rate_no_link"][linked][:, 36:].sum() / g["rate_no_link"][:, 36:].sum()))
    return out


def rows():
    return [json.loads(x) for x in OUT.read_text().splitlines()] if OUT.exists() else []


def run(panel, seed, inputs, level):
    if any(r["panel"] == panel and r["seed"] == seed and r["inputs"] == inputs for r in rows()):
        return
    cmd = [sys.executable, __file__, panel, str(seed), "--inputs", inputs, "--level", level]
    if inputs == "real" and panel in NULLS and seed < SEEDS[0] + SHUFFLE_ALWAYS:
        cmd.append("--always-shuffle")
    subprocess.run(cmd, check=True)


def marks(level, start=None):
    start = time.time()
    for panel in NULLS:
        for inputs in ("real", "noise"):
            for seed in SEEDS:
                run(panel, seed, inputs, level)
    quiet = {}
    for panel in NULLS:
        for inputs in ("real", "noise"):
            got = [abs(r["main"]["skill"]) <= BAND for r in rows() if r["panel"] == panel and r["inputs"] == inputs]
            quiet[f"{panel}/{inputs}"] = sum(got)
    print("mark A", quiet, flush=True)
    if min(quiet.values()) < QUIET_NEEDED:
        sys.exit("mark A failed: no planted panel runs")
    for panel in ["planted_3.50", *DESCRIBED]:
        for seed in SEEDS:
            if time.time() - start > CEILING:
                sys.exit("ceiling reached")
            run(panel, seed, "real", level)
    print("all replicates done", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("panel")
    ap.add_argument("seed", type=int, nargs="?")
    ap.add_argument("--inputs", choices=["real", "noise"], default="real")
    ap.add_argument("--level", choices=["on", "off"], default="on")
    ap.add_argument("--always-shuffle", action="store_true")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    if args.panel == "marks":
        marks(args.level)
    else:
        line = json.dumps(replicate(args.panel, args.seed, args.inputs, args.level == "on", args.always_shuffle))
        with args.out.open("a") as f:
            f.write(line + "\n")
