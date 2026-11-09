"""The frozen two-gate search, then the forecast check, on five fields never read before. Rule: results/real-enso-continents.md."""
import json
import sys
from pathlib import Path

import numpy as np

from causal_atlas import confirm, decoy, field, forecast, links
from run_enso import CLIP, DISCOVERY, SHIFTS, YEARS

OUT = Path(__file__).resolve().parents[1] / "results" / "real-enso-continents.jsonl"
SEEDS = {name: range(12101 + 100 * i, 12121 + 100 * i) for i, name in enumerate(field.BOXES)}
PUBLISHED = ("south_america", "australia", "south_southeast_asia")
NAMED = 18  # of 20, for a field to enter the pooled forecast check
ALARMS = 8  # of 100, pooled over the five fields, for each kind of false alarm
SCORED = np.arange(DISCOVERY // 12, field.MONTHS // 12)


def data(name):
    y, lat, lon = field.box(name)
    return np.clip(y, -CLIP, CLIP), field.oni(), lat, lon


def row(r):
    with open(OUT, "a") as f:
        f.write(json.dumps(r) + "\n")
    print({k: v for k, v in r.items() if k not in ("shifted", "by_year")}, flush=True)


def rows():
    return [json.loads(line) for line in open(OUT)] if OUT.exists() else []


def name(which):
    """Blind naming on the discovery years of one field, and where the ONI's strongest regional correlation is."""
    y, x, lat, lon = data(which)
    y, x = y[:, :DISCOVERY], x[:DISCOVERY]
    for seed in SEEDS[which]:
        d = decoy.make(seed, field.MONTHS, field.oni())[:, :DISCOVERY]
        order = np.random.default_rng(seed).permutation(DISCOVERY // 12)
        mixed = y.reshape(len(y), -1, 12)[:, order].reshape(len(y), -1)
        for kind, field_y, drivers in (("real", y, [x, *d]), ("no_oni", y, list(d)), ("years_mixed", mixed, [x, *d])):
            row({"kind": kind, "field": which, "seed": seed, **links.both(field_y, drivers, YEARS, SHIFTS, lat, lon)})
    t = links.tiles(lat, lon)
    r = links.correlations(t @ y, x, YEARS)
    lag, month, tile = [int(v) for v in np.unravel_index(np.abs(r).argmax(), r.shape)]
    row({"kind": "where", "field": which, "cells": len(y), "regions": len(t), "lat": round(float(t[tile] @ lat), 1), "lon": round(float(t[tile] @ lon), 1), "lag": lag, "month": month + 1, "r": round(float(r[lag, month, tile]), 3)})


def marks(done):
    """Counts for the naming marks: by field, sets with the ONI a lead; pooled, runs with a false alarm of each kind."""
    named = {f: sum(0 in r["leads"] for r in done if r["kind"] == "real" and r["field"] == f) for f in field.BOXES}
    alarms = {
        "decoy": sum(any(c > 0 for c in r["leads"]) for r in done if r["kind"] == "real"),
        "no_oni": sum(bool(r["leads"]) for r in done if r["kind"] == "no_oni"),
        "years_mixed": sum(bool(r["leads"]) for r in done if r["kind"] == "years_mixed"),
    }
    runs = sum(r["kind"] == "real" for r in done)
    return named, alarms, runs


def units(which, scale):
    y, x, lat, lon = data(which)
    if scale == "cell":
        return y, confirm.near_mean(y, confirm.neighbours(lat, lon)), x
    y = links.tiles(lat, lon) @ y
    return y, np.repeat(y.mean(axis=0, keepdims=True), len(y), axis=0), x


def check(which, scale):
    """One field at one scale: everything fitted on the discovery years, scored on the years after."""
    y, near, x = units(which, scale)
    model = forecast.fit(y, near, x, DISCOVERY)
    base, got, shifted = forecast.score(model, x, SCORED)
    alone = forecast.errors(y, near, model["claimed"], DISCOVERY, SCORED)
    late = np.arange(DISCOVERY, y.shape[1])
    info = {
        "units": len(y),
        "baseline": model["baseline"],
        "fold_error": {k: round(v, 1) for k, v in model["fold_error"].items()},
        "baseline_vs_zero_all": round(float(1 - (model["e"][:, late] ** 2).sum() / (y[:, late].astype(np.float64) ** 2).sum()), 4),
        "k": round(model["k"], 3),
        "claimed": int(model["claimed"].sum()),
        "units_with_claim": int(model["claimed"].any(axis=0).sum()),
        "lags": np.bincount(model["lag"][model["claimed"]], minlength=13)[4:].tolist(),
    }
    return info, base, got, shifted, alone


def verdict(base, got, shifted, alone):
    out = forecast.skill(base, got, shifted)
    out["model_error"] = round(float(got.sum()), 2)
    out["alone"] = {k: round(float(v.sum()), 2) for k, v in alone.items()}
    out["below_every_baseline"] = bool(all(got.sum() < v.sum() for v in alone.values()))
    out["passes"] = bool(out["ci"][0] > 0 and out["beats"] == len(out["shifted"]) and out["below_every_baseline"])
    return out


def confirmation():
    done = rows()
    if any(r["kind"] in ("confirmation", "pooled") for r in done):
        sys.exit("Already scored. The years after 1999 are spent for this driver and these fields.")
    named, alarms, runs = marks(done)
    if runs != 20 * len(field.BOXES) or any(v > ALARMS for v in alarms.values()):
        sys.exit(f"Naming is incomplete or its false-alarm marks missed ({runs} runs, {alarms}). The years after 1999 stay sealed.")
    entered = [f for f in field.BOXES if named[f] >= NAMED]
    if not entered:
        sys.exit("The ONI was not named in any field. The years after 1999 stay sealed.")
    for scale in ("region", "cell"):
        pool = None
        for which in field.BOXES:
            info, *parts = check(which, scale)
            row({"kind": "confirmation", "scale": scale, "field": which, "entered": which in entered, **info, **verdict(*parts), "by_year": {"base": parts[0].round(3).tolist(), "model": parts[1].round(3).tolist()}})
            if which in entered:
                pool = parts if pool is None else [p + q if not isinstance(p, dict) else {k: p[k] + q[k] for k in p} for p, q in zip(pool, parts)]
        row({"kind": "pooled", "scale": scale, "fields": entered, **verdict(*pool)})


if __name__ == "__main__":
    if sys.argv[1] == "name":
        for which in sys.argv[2:] or field.BOXES:
            name(which)
    elif sys.argv[1] == "marks":
        print(marks(rows()))
    elif sys.argv[1:] == ["confirm", "once"]:
        confirmation()
    else:
        sys.exit("run_continents.py name [field ...] | marks | confirm once")
