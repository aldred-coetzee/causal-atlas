"""Exploration on spent years, marking nothing: a link of known size planted in the real fields' burned area and scored as the real fields were, to measure what the null in results/fire-drought.md can and cannot rule out. Registered there before it was run.

Usage: explore_planted.py [aligned] [share ...]
"""
import json
import os
import sys
from pathlib import Path

import numpy as np

from causal_atlas import field, fire, local
from run_local import pooled, real, scored, verdict

OUT = Path(__file__).resolve().parents[1] / "results" / "explore-planted.jsonl"
SIZES = {0.20: range(21001, 21005), 0.10: range(21101, 21105), 0.05: range(21201, 21205), 0.02: range(21301, 21305)}  # share of the outcome's variance where planted: seeds
ALIGNED = {0.20: range(21401, 21405), 0.10: range(21501, 21505), 0.05: range(21601, 21605), 0.02: range(21701, 21705)}  # the same, with the planted squares on the detector's own blocks
COVER = 0.2  # share of a field's cells that hold the planted link
LAGS = np.arange(4, 13)
KINDS = ("plain", "adjusted")  # the share observed is not touched by the planting


def spei(which):
    """SPEI-3 as run_local.drought reads it, clipped, before the departure is taken: the cells of real(which), every month to the end of the fire clock, and the index of 1982-01."""
    _, lat, lon, _ = fire.box(which)
    if which == "africa":
        (a, o), (s, kept) = field.cells(), field.spei()
        a, o = a[kept], o[kept]
    else:
        s, a, o = field.box(which)
    at = {(round(2 * p), round(2 * q)): i for i, (p, q) in enumerate(zip(a, o))}
    i = np.array([at.get((round(2 * p), round(2 * q)), -1) for p, q in zip(lat, lon)])
    first = 12 * (fire.FIRST_YEAR - field.FIRST_YEAR)
    return np.clip(s[i[i >= 0], : first + fire.MONTHS], -fire.CLIP, fire.CLIP), first


def plant(data, s, first, share, rng, aligned=False):
    """Burned area with a link planted in it, and which cells hold it. Five-degree squares, set half a square off the detector's own unless aligned, taken in random order until they hold COVER of the cells; in each, one sign and one lead; on the months in use, the outcome becomes sqrt(1 - share) of itself plus sqrt(share) of the cell's drought that many months earlier, at the outcome's own spread in that cell."""
    y, _, _, used, lat, lon = data
    off = 0 if aligned else local.BLOCK / 2
    patch = local.blocks(lat + off, lon + off)
    out, planted = y.astype(np.float64).copy(), np.zeros(len(y), bool)
    months = np.arange(12, y.shape[1])
    fit = months < fire.FIT
    for b in rng.permutation(patch.max() + 1):
        if planted.mean() >= COVER:
            break
        cells = np.flatnonzero(patch == b)
        sign, lag = rng.choice([-1, 1]), rng.choice(LAGS)
        was = s[cells, first : first + fire.FIT]
        z = (s[np.ix_(cells, first + months - lag)] - was.mean(axis=1, keepdims=True)) / np.maximum(was.std(axis=1, keepdims=True), 1e-6)
        on = used[cells][:, months % 12]
        own = out[np.ix_(cells, months)]
        n = np.maximum((on & fit).sum(axis=1, keepdims=True), 1)
        mean = (own * (on & fit)).sum(axis=1, keepdims=True) / n
        spread = np.sqrt((((own - mean) ** 2) * (on & fit)).sum(axis=1, keepdims=True) / n)
        new = np.clip(np.sqrt(1 - share) * own + sign * np.sqrt(share) * spread * z, -fire.CLIP, fire.CLIP)
        out[np.ix_(cells, months)] = np.where(on, new, own)
        planted[cells] = True
    return out.astype(y.dtype), planted


def main(shares, aligned=False):
    done = {(r["share"], r["seed"]) for r in map(json.loads, open(OUT))} if OUT.exists() else set()
    fields = {}
    for name in fire.FIELDS:
        data, (s, first) = real(name), spei(name)
        assert np.allclose(local.departure(s, first), data[1], equal_nan=True), name  # the same drought the scoring read
        fields[name] = data, s, first
    for share in shares:
        for seed in (ALIGNED if aligned else SIZES)[share]:
            if (share, seed) in done:
                continue
            parts, by_field = {k: {} for k in KINDS}, {k: {} for k in KINDS}
            for i, name in enumerate(fire.FIELDS):
                data, s, first = fields[name]
                y, planted = plant(data, s, first, share, np.random.default_rng([seed, i]), aligned)
                for kind in KINDS:
                    model, info, p = scored((y, *data[1:]), kind)
                    c, v = model["claimed"], verdict(*p)
                    parts[kind][name] = p
                    by_field[kind][name] = {"k": info["k"], "claimed": info["claimed"], "planted_cells": round(float(planted.mean()), 3), "claims_in_planted_cells": round(float(c[:, planted].sum() / max(c.sum(), 1)), 3), "s": v["s"], "beats": v["beats"]}
            out = {"kind": "planted", "placement": "aligned" if aligned else "offset", "share": share, "seed": seed}
            for kind in KINDS:
                v = verdict(*pooled(parts[kind], list(fire.FIELDS)))
                v["without_baseline_condition"] = bool(v["ci"][0] > 0 and v["beats"] == 14 and v["flat"]["ci"][0] > 0 and v["flat"]["beats"] == 14)
                out[kind] = {**v, "fields": by_field[kind]}
            f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
            os.write(f, (json.dumps(out) + "\n").encode())
            os.close(f)
            print(share, seed, {k: (round(out[k]["s"], 4), out[k]["beats"], out[k]["passes"], out[k]["without_baseline_condition"]) for k in KINDS}, flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "aligned"]
    main([float(a) for a in args] or list(SIZES), "aligned" in sys.argv[1:])
