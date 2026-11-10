"""A second domain's known answer: is the ONI named, among decoys, as a driver of burned area, what the search can hear on so short a record, and whether the ONI then improves a forecast four or more months ahead. Rule: results/fire-enso.md."""
import json
import sys
from pathlib import Path

import numpy as np

from causal_atlas import confirm, decoy, fire, forecast, links
from run_continents import verdict

OUT = Path(__file__).resolve().parents[1] / "results" / "fire-enso.jsonl"
SEEDS = {name: range(17101 + 100 * i, 17121 + 100 * i) for i, name in enumerate(fire.FIELDS)}
RULER_SEEDS = {name: range(17701 + 100 * i, 17711 + 100 * i) for i, name in enumerate(fire.FIELDS)}
YEARS = np.array([y for y in range(1, fire.FIT // 12) if y != fire.ABSENT - fire.FIRST_YEAR])  # targets: 1983 to 2003 without 1994
SHIFTS = range(2, fire.FIT // 12 - 1)  # whole years, circular on the fitting record; the copies a year either side are the series itself (decision 0044)
SCORED = np.arange(fire.FIT // 12, fire.MONTHS // 12)  # 2004 to 2018
SHARES = (0.05, 0.15, 0.40)
AREAS = (0.05, 0.25)
RULER_LAG = 5
CHECK = (0.40, 0.25)  # the planted link a field must hear: share of variance, share of cells
HEARD = 8  # of 10
NAMED = 18  # of 20, for a field to enter the forecast check
ALARMS = 0.08  # of the runs, pooled over the fields, for each kind of false alarm


def fields():
    """The fields with at least one region of enough cells to average; the others are too sparse to test."""
    return [f for f in fire.FIELDS if len(links.tiles(*fire.box(f)[1:3]))]


def row(r):
    with open(OUT, "a") as f:
        f.write(json.dumps(r) + "\n")
    print({k: v for k, v in r.items() if k not in ("shifted", "by_year", "broad", "sharp")}, flush=True)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def have(kind, *keys):
    """The runs of one kind already in the rows, so a stopped run picks up where it left off."""
    return {tuple(r[k] for k in keys) for r in rows() if r["kind"] == kind}


def shapes():
    """Cells, regions and used cell-months by field: what the fitting years' observation and burning leave to test. No correlation with anything."""
    for which in fire.FIELDS:
        y, lat, lon, used = fire.box(which)
        print(which, {"cells": len(y), "regions": len(links.tiles(lat, lon)), "used_by_month": used.sum(axis=0).tolist(), "season": season(used)}, flush=True)


def season(used):
    """The three consecutive calendar months with the most used cell-months in the field, 0 for January."""
    n = used.sum(axis=0)
    m0 = int(np.argmax([n[[(m + k) % 12 for k in range(3)]].sum() for m in range(12)]))
    return [(m0 + k) % 12 for k in range(3)]


def planted(y, used, lat, lon, z, seed, share, area):
    """y with a link from z added in the nearest cells to a seeded centre, in the field's three busiest calendar months, at RULER_LAG, on the cell-months in use."""
    rng = np.random.default_rng(seed)
    c = rng.integers(len(y))
    dist = (lat - lat[c]) ** 2 + ((lon - lon[c]) * np.cos(np.radians(lat[c]))) ** 2
    cells = np.argsort(dist)[: int(area * len(y))]
    months = season(used)
    t = np.arange(12, y.shape[1])
    t = t[np.isin(t % 12, months)]
    out = y.astype(np.float64)
    out[np.ix_(cells, t)] += np.sqrt(share / (1 - share)) * z[t - RULER_LAG] * used[np.ix_(cells, t % 12)]
    return out, cells, months


def ruler(which):
    """What the search hears on one field: a link planted from the first decoy, at each size and extent."""
    y, lat, lon, used = fire.box(which)
    y, x = y[:, : fire.FIT], fire.oni()[: fire.FIT]
    for seed in RULER_SEEDS[which]:
        d = decoy.make(seed, fire.MONTHS, fire.oni())[:, : fire.FIT]
        for share in SHARES:
            for area in AREAS:
                if (which, seed, share, area) in have("ruler", "field", "seed", "share", "area"):
                    continue
                yp, cells, months = planted(y, used, lat, lon, d[0], seed, share, area)
                out = links.both(yp, [x, *d], YEARS, SHIFTS, lat, lon)
                more = {"share": share, "area": area, "found": 1 in out["leads"], "false": [c for c in out["leads"] if c > 1], "oni": 0 in out["leads"]}
                if more["found"]:
                    sig = links.significant(links.correlations(yp, d[0], YEARS), len(YEARS))
                    inside = np.zeros(len(y), bool)
                    inside[cells] = True
                    more["claims"] = int(sig.sum())
                    more["claims_true_cells"] = round(float(sig[:, :, inside].sum() / max(sig.sum(), 1)), 3)
                row({"kind": "ruler", "field": which, "seed": seed, **out, **more})


def name(which):
    """Blind naming on the fitting years of one field: the ONI among decoys, the ONI left out, the field's years in a seeded random order, and the ONI among decoys with what the satellite saw in place of what burned."""
    y, lat, lon, _ = fire.box(which)
    y, x, seen = y[:, : fire.FIT], fire.oni()[: fire.FIT], fire.sight(which)[:, : fire.FIT]
    for seed in SEEDS[which]:
        d = decoy.make(seed, fire.MONTHS, fire.oni())[:, : fire.FIT]
        order = np.arange(fire.FIT // 12)
        order[np.r_[0, YEARS]] = np.random.default_rng(seed).permutation(np.r_[0, YEARS])  # the absent year stays where it is
        mixed = y.reshape(len(y), -1, 12)[:, order].reshape(len(y), -1)
        for kind, field_y, drivers in (("real", y, [x, *d]), ("no_oni", y, list(d)), ("years_mixed", mixed, [x, *d]), ("sight", seen, [x, *d])):
            if (which, seed) in have(kind, "field", "seed"):
                continue
            row({"kind": kind, "field": which, "seed": seed, **links.both(field_y, drivers, YEARS, SHIFTS, lat, lon)})
    if (which,) not in have("where", "field"):
        t = links.tiles(lat, lon)
        r = links.correlations(t @ y, x, YEARS)
        lag, month, tile = [int(v) for v in np.unravel_index(np.abs(r).argmax(), r.shape)]
        row({"kind": "where", "field": which, "cells": len(y), "regions": len(t), "lat": round(float(t[tile] @ lat), 1), "lon": round(float(t[tile] @ lon), 1), "lag": lag, "month": month + 1, "r": round(float(r[lag, month, tile]), 3)})


def marks(done):
    """By field: sets with the ONI a lead (of burning, and of what the satellite saw), and ruler runs that found the marked link. Pooled: runs with a false alarm of each kind, and the most allowed."""
    named = {f: sum(0 in r["leads"] for r in done if r["kind"] == "real" and r["field"] == f) for f in fields()}
    sight = {f: sum(0 in r["leads"] for r in done if r["kind"] == "sight" and r["field"] == f) for f in fields()}
    heard = {f: sum(r["found"] for r in done if r["kind"] == "ruler" and r["field"] == f and (r["share"], r["area"]) == CHECK) for f in fields()}
    alarms = {
        "decoy": sum(any(c > 0 for c in r["leads"]) for r in done if r["kind"] == "real"),
        "no_oni": sum(bool(r["leads"]) for r in done if r["kind"] == "no_oni"),
        "years_mixed": sum(bool(r["leads"]) for r in done if r["kind"] == "years_mixed"),
    }
    runs = sum(r["kind"] == "real" for r in done)
    return named, heard, alarms, runs, int(ALARMS * runs), sight


def table(done):
    """The ruler by field: runs that found the planted link at each size and extent, and runs that named some other decoy."""
    run = [r for r in done if r["kind"] == "ruler"]
    found = {f: {f"{s:.2f} over {a:.2f}": sum(r["found"] for r in run if (r["field"], r["share"], r["area"]) == (f, s, a)) for s in SHARES for a in AREAS} for f in fields()}
    inside = min((r["claims_true_cells"] for r in run if r["found"] and (r["share"], r["area"]) == CHECK), default=None)
    return found, {"decoy_named": sum(bool(r["false"]) for r in run), "runs": len(run), "least_inside": inside}


def units(which, scale):
    y, lat, lon, _ = fire.box(which)
    if scale == "cell":
        return y, confirm.near_mean(y, confirm.neighbours(lat, lon)), fire.oni()
    y = links.tiles(lat, lon) @ y
    return y, np.repeat(y.mean(axis=0, keepdims=True), len(y), axis=0), fire.oni()


def check(which, scale):
    """One field at one scale: everything fitted on the fitting years, scored on the years after."""
    y, near, x = units(which, scale)
    model = forecast.fit(y, near, x, fire.FIT, YEARS)
    base, got, shifted = forecast.score(model, x, SCORED)
    alone = forecast.errors(y, near, model["claimed"], fire.FIT, SCORED, YEARS)
    late = np.arange(fire.FIT, y.shape[1])
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


def pooled(parts, which):
    """Squared errors summed over fields, year by year: the baseline's, the model's, the shifted models' and each baseline's alone."""
    return [sum(parts[f][i] for f in which) for i in range(3)] + [{k: sum(parts[f][3][k] for f in which) for k in parts[which[0]][3]}]


def confirmation():
    done = rows()
    if any(r["kind"] in ("confirmation", "pooled") for r in done):
        sys.exit("Already scored. The years after 2003 are spent for this driver and these fields.")
    named, heard, alarms, runs, most, sight = marks(done)
    measured = sum(r["kind"] == "ruler" for r in done)
    if measured != 10 * len(SHARES) * len(AREAS) * len(fields()) or runs != 20 * len(fields()) or any(v > most for v in alarms.values()):
        sys.exit(f"The ruler or the naming is incomplete, or a false-alarm mark missed ({measured} ruler runs, {runs} naming runs, {alarms}, at most {most}). The years after 2003 stay sealed.")
    entered = [f for f in fields() if named[f] >= NAMED]
    if not entered:
        sys.exit("The ONI was not named in any field. The years after 2003 stay sealed.")
    clear = [f for f in entered if sight[f] < NAMED]  # fields where the ONI was not also named as a driver of what the satellite saw
    for scale in ("region", "cell"):
        parts = {}
        for which in fields():
            info, *parts[which] = check(which, scale)
            row({"kind": "confirmation", "scale": scale, "field": which, "entered": which in entered, **info, **verdict(*parts[which]), "by_year": {"base": parts[which][0].round(3).tolist(), "model": parts[which][1].round(3).tolist()}})
        row({"kind": "pooled", "scale": scale, "fields": entered, **verdict(*pooled(parts, entered))})
        if clear and clear != entered:
            row({"kind": "pooled_clear", "scale": scale, "fields": clear, **verdict(*pooled(parts, clear))})


if __name__ == "__main__":
    if sys.argv[1] in ("name", "ruler"):
        for which in sys.argv[2:] or fields():
            {"name": name, "ruler": ruler}[sys.argv[1]](which)
    elif sys.argv[1] == "shapes":
        shapes()
    elif sys.argv[1] == "marks":
        print(*marks(rows()), *table(rows()), sep="\n")
    elif sys.argv[1:] == ["confirm", "once"]:
        confirmation()
    else:
        sys.exit("run_fire.py shapes | ruler [field ...] | name [field ...] | marks | confirm once")
