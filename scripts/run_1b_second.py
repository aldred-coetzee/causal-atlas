"""The 1b second run: last 240 months scored, trained on 36 to 194. One replicate, or `all` to drive them."""
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

from causal_atlas import detector as d  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

TRAIN = (36, 194)
SCORED = (195, 434)
SECONDARY_END = 386  # the scored window without today's held-out block
PERMS = 19
OUT = ROOT / "results" / "1b-second-replicates.jsonl"
NULLS = ["pure_null", "shared_null", "combo_null"]
PANELS = ["planted_3.50", *NULLS, "planted_3.00", "planted_2.40", "planted_combo_6"]
SEEDS = range(3001, 3021)
SHUFFLE_ALWAYS = 3
CEILING = 24 * 3600


def spans(obs, m, b):
    """Skill and interval on all scored months and on the secondary span, from the same predictions."""
    k = SECONDARY_END - SCORED[0] + 1
    out = {}
    for name, cut in (("main", obs.shape[1]), ("secondary", k)):
        out[name] = dict(skill=float(d.skill(obs[:, :cut], m[:, :cut], b[:, :cut])))
        out[name]["ci"] = list(d.block_interval(obs[:, :cut], m[:, :cut], b[:, :cut]))
    return out


def shuffle_skills(cut, obs, b, predict, drought, oni):
    shifts = [(d.circular_shift(drought, k), d.circular_shift(oni, k)) for k in range(1, d.SHIFTS + 1)]
    perms = [(d.year_permutation(drought, 5000 + i), d.year_permutation(oni, 5000 + i)) for i in range(PERMS)]
    out = {"circular": [], "permutation": []}
    for key, pairs in (("circular", shifts), ("permutation", perms)):
        for dr, on in pairs:
            m = predict(dr, on)
            out[key].append({n: float(d.skill(obs[:, :c], m[:, :c], b[:, :c])) for n, c in cut.items()})
    return out


def replicate(panel, seed, always_shuffle=False):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    n = len(lat)
    tau = np.arange(d.TRAIN[0], d.HELD[1] + 1)
    target = y[:, tau].ravel().astype(np.float32)
    in_month = np.tile(tau, n)
    fit_rows = in_month <= TRAIN[1]
    score_rows = in_month >= SCORED[0]
    base = d.base_features(y, lat, lon)
    obs = y[:, SCORED[0] : SCORED[1] + 1]
    shape = obs.shape

    def predict(dr, on):
        X = np.hstack([base, d.input_features(dr, on, train_months=TRAIN)])
        return d.fit_predict(X, target, fit_rows, score_rows).reshape(shape)

    started = time.time()
    b = d.fit_predict(base, target, fit_rows, score_rows).reshape(shape)
    m = predict(drought, oni)
    result = spans(obs, m, b)
    cut = dict(main=shape[1], secondary=SECONDARY_END - SCORED[0] + 1)
    first = {k: result[k]["skill"] >= 0.02 and result[k]["ci"][0] > 0 for k in cut}
    out = dict(panel=panel, seed=seed, cells=n, events_scored=int(obs.sum()),
               nonzero_scored=int((obs > 0).sum()), main=result["main"], secondary=result["secondary"],
               b0_skill_of_b=float(d.skill(obs, b, np.maximum(d.naive_b0(y)[:, -shape[1]:], 1e-3))),
               shuffled=False, shuffled_for_secondary_only=False)
    no = dict(first=False, second=None, third=None, all=False)
    for name in cut:
        out[name].update(circular=no, permutation=no)
    if always_shuffle or any(first.values()):
        sk = shuffle_skills(cut, obs, b, predict, drought, oni)
        out.update(shuffled=True, shuffled_for_secondary_only=not always_shuffle and not first["main"])
        for name in cut:
            for scheme in sk:
                values = [s[name] for s in sk[scheme]]
                out[name][scheme] = d.verdict(result[name]["skill"], result[name]["ci"][0], values)
                out[name][scheme + "_max"] = max(values)
                out[name][scheme + "_median"] = float(np.median(values))
    out["seconds"] = round(time.time() - started, 1)
    if panel.startswith("planted"):
        a, c = synth.lead_rates(panel, lat, lon, seed, lead=3)
        for name, end in (("main", SCORED[1]), ("secondary", SECONDARY_END)):
            i = np.arange(SCORED[0], end + 1)
            out[name]["worth"] = float(d.skill(y[:, i], a[:, i], c[:, i]))
        linked = g["linked"].any(axis=1) if g["linked"].ndim > 1 else g["linked"]
        out.update(linked_share=float(linked.mean()),
                   linked_rate_share=float(g["rate_no_link"][linked][:, 36:].sum() / g["rate_no_link"][:, 36:].sum()))
    return out


def run_all():
    done = set()
    if OUT.exists():
        done = {(r["panel"], r["seed"]) for r in map(json.loads, OUT.read_text().splitlines())}
    start = time.time()
    for panel in PANELS:
        for seed in SEEDS:
            if (panel, seed) in done:
                continue
            if time.time() - start > CEILING:
                sys.exit("ceiling reached: 24 hours")
            cmd = [sys.executable, __file__, panel, str(seed)]
            if panel in NULLS and seed < SEEDS[0] + SHUFFLE_ALWAYS:
                cmd.append("--always-shuffle")
            subprocess.run(cmd, check=True)
    print("all replicates done")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("panel")
    ap.add_argument("seed", type=int, nargs="?")
    ap.add_argument("--always-shuffle", action="store_true")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()
    if args.panel == "all":
        run_all()
    else:
        line = json.dumps(replicate(args.panel, args.seed, args.always_shuffle))
        with args.out.open("a") as f:
            f.write(line + "\n")
