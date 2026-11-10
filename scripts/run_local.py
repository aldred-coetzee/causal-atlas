"""Local drought and burned area: does each cell's own drought, four or more months before, improve a forecast of its burned area beyond own history. First on made-up panels with a link, with none, with a link only through the instrument, and with nothing but a shared drift; then on the real fields, fitted on 1982 to 2003 and scored once on 2004 to 2018. Rule: results/fire-drought.md."""
import json
import sys
from pathlib import Path

import numpy as np

from causal_atlas import confirm, field, fire, local
from run_continents import verdict
from run_fire import SCORED, YEARS, pooled

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import local_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "fire-drought.jsonl"
KINDS = ("plain", "adjusted", "sight")  # burned area; burned area less what the share observed that month explains; the share observed itself
MADE_UP = {  # name: (share of variance from moisture, instrument effect, shared drift, seeds)
    "link_20": (0.20, 0.0, 0.0, range(19101, 19111)),
    "link_10": (0.10, 0.0, 0.0, range(19201, 19211)),
    "link_05": (0.05, 0.0, 0.0, range(19301, 19311)),
    "none": (0.0, 0.0, 0.0, range(19401, 19461)),
    "instrument": (0.0, 1.0, 0.0, range(19501, 19525)),
    "both": (0.20, 1.0, 0.0, range(19601, 19611)),
    "trends": (0.0, 0.0, 1.0, range(19701, 19725)),
}
MARKS = {  # panel: (what is counted, "least" or "most", how many seeds)
    "link_20": ("link", "least", 7),
    "both": ("link", "least", 7),
    "none": ("link", "most", 4),
    "trends": ("link", "most", 2),
    "instrument": ("link", "most", 2),
}
SIGHT = ("instrument", "least", 22)  # and the instrument-only panels must show in what the satellite saw
EMPTY = ("none", "instrument", "trends")  # panels with no link, also read six at a time, as the six real fields are read together
SIX = 6
MOST_SIXES = 1  # sixes read as a link, of all the sixes of the empty panels


def row(r):
    with open(OUT, "a") as f:
        f.write(json.dumps(r) + "\n")
    print({k: v for k, v in r.items() if k not in ("shifted", "by_year", "alone", "fold_error", "by_month")}, flush=True)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def drought(which):
    """SPEI-3 on the fire clock for the cells of fire.box(which), clipped, as its departure from the cell's own last five years (local.departure, with the years before 1982 from the drought record), and which of those cells have it."""
    _, lat, lon, _ = fire.box(which)
    if which == "africa":
        (a, o), (s, kept) = field.cells(), field.spei()
        a, o = a[kept], o[kept]
    else:
        s, a, o = field.box(which)
    at = {(round(2 * p), round(2 * q)): i for i, (p, q) in enumerate(zip(a, o))}
    i = np.array([at.get((round(2 * p), round(2 * q)), -1) for p, q in zip(lat, lon)])
    first = 12 * (fire.FIRST_YEAR - field.FIRST_YEAR)
    return local.departure(np.clip(s[np.maximum(i, 0), : first + fire.MONTHS], -fire.CLIP, fire.CLIP), first), i >= 0


def real(which):
    """One real field: burned area, drought, the share observed, the months in use, latitude and longitude, for the cells that have a drought value."""
    y, lat, lon, used = fire.box(which)
    x, has = drought(which)
    return y[has], x[has], fire.sight(which)[has], used[has], lat[has], lon[has]


def made_up(seed, share, instrument, trend=0.0):
    """One made-up field through the same preparation as the real ones, and which of its cells hold a planted link."""
    burned, seen, moisture, lat, lon, planted = local_panel.make(seed, share, instrument, trend)
    y, used = fire.standard(burned, seen)
    kept = used.any(axis=1)
    y = np.clip(y, -fire.CLIP, fire.CLIP).reshape(len(y), -1)
    return (y[kept], local.departure(moisture[kept], 0), fire.share(seen)[kept], used[kept], lat[kept], lon[kept]), planted[kept]


def outcome(data, kind):
    y, x, s, used, lat, lon = data
    group = local.blocks(lat, lon)
    y = {"plain": y, "adjusted": local.adjusted(y, s, used, group, YEARS), "sight": s * used[:, np.arange(y.shape[1]) % 12]}[kind]
    return y, confirm.near_mean(y, confirm.neighbours(lat, lon)), x, used, group


def fitted(data, kind, months=None):
    """The model from the fitting years, and what it claims. With months given, nothing after them is in memory when it is fitted."""
    y, near, x, used, group = outcome(data, kind)
    model = local.fit(y[:, :months], near[:, :months], x[:, :months], used, group, YEARS)
    c = model["claimed"]
    info = {
        "cells": len(y),
        "blocks": int(group.max() + 1),
        "baseline": model["baseline"],
        "fold_error": {k: round(v, 1) for k, v in model["fold_error"].items()},
        "k": round(model["k"], 3),
        "season": model["season"],
        "tau": model["tau"],
        "gain": model["gain"],
        "block_months_claimed": model["blocks"],
        "claimed": int(c.sum()),
        "cells_with_claim": int(c.any(axis=0).sum()),
        "lags": np.bincount(model["lag"][c], minlength=13)[4:].tolist(),
        "by_month": c.sum(axis=1).tolist(),
        "positive": round(float((model["slope"][c] > 0).mean()), 3) if c.any() else None,
    }
    return model, info, (y, near, x, used)


def scored(data, kind):
    """One field and outcome, fitted on the fitting years and scored on the years after."""
    model, info, (y, near, x, used) = fitted(data, kind)
    base, got, shifted = local.score(model, x, SCORED)
    return model, info, [base, got, shifted, local.alone(y, near, used, model["claimed"], YEARS, SCORED)]


def known(names):
    """Rule 3: the made-up panels, each seed fitted and scored as a real field would be."""
    done = {(r["panel"], r["seed"], r["outcome"]) for r in rows() if r["kind"] == "made_up"}
    for name in names:
        *how, seeds = MADE_UP[name]
        for seed in seeds:
            if all((name, seed, kind) in done for kind in KINDS):
                continue
            data, planted = made_up(seed, *how)
            for kind in KINDS:
                if (name, seed, kind) in done:
                    continue
                model, info, parts = scored(data, kind)
                c = model["claimed"]
                inside = round(float(c[:, planted].sum() / max(c.sum(), 1)), 3)
                row({"kind": "made_up", "panel": name, "seed": seed, "outcome": kind, **info, "claims_in_planted_cells": inside, "planted_cells": int(planted.sum()), **verdict(*parts), "by_year": by_year(parts)})


def by_year(parts):
    """The squared errors by scoring year, as kept in a row: the baseline's, the model's, the model's under each shift, each baseline's alone."""
    base, got, shifted, alone = parts
    return {"base": base.tolist(), "model": got.tolist(), "shifted": shifted.tolist(), "alone": {k: v.tolist() for k, v in alone.items()}}


def together(found):
    """Several panels read as one, their squared errors summed year by year as the real fields' are: by outcome, the verdict."""
    out = {}
    for kind in KINDS:
        parts = {r["seed"]: [np.array(r["by_year"][k]) for k in ("base", "model", "shifted")] + [{k: np.array(v) for k, v in r["by_year"]["alone"].items()}] for r in found if r["outcome"] == kind}
        out[kind] = verdict(*pooled(parts, list(parts)))
    return out


def link(passed):
    """The reading of one field or panel: a link from the driver to the outcome is claimed only when it passes on burned area and again on burned area less what the share observed explains."""
    return passed["plain"] and passed["adjusted"]


def marks(done):
    """By made-up panel: seeds run, seeds read as a link, seeds where each outcome passes; and whether each mark holds."""
    out, held = {}, {}
    for name in MADE_UP:
        by_seed = {}
        for r in done:
            if r["kind"] == "made_up" and r["panel"] == name:
                by_seed.setdefault(r["seed"], {})[r["outcome"]] = r["passes"]
        full = [v for v in by_seed.values() if len(v) == len(KINDS)]
        out[name] = {"seeds": len(full), "of": len(MADE_UP[name][-1]), "link": sum(link(v) for v in full), **{k: sum(v[k] for v in full) for k in KINDS}}
    sixes = 0
    for name in EMPTY:
        seeds = list(MADE_UP[name][-1])
        found = [r for r in done if r["kind"] == "made_up" and r["panel"] == name]
        if out[name]["seeds"] < len(seeds):
            continue
        read = [together([r for r in found if r["seed"] in seeds[i : i + SIX]]) for i in range(0, len(seeds), SIX)]
        whole = together(found)
        out[name]["sixes"] = len(read)
        out[name]["sixes_link"] = sum(link({k: v[k]["passes"] for k in KINDS}) for v in read)
        out[name]["sixes_s"] = {k: [round(v[k]["s"], 5) for v in read] for k in KINDS}
        out[name]["all_together"] = {k: {"s": round(whole[k]["s"], 5), "ci": [round(q, 5) for q in whole[k]["ci"]], "beats": whole[k]["beats"], "passes": whole[k]["passes"]} for k in KINDS}
        sixes += out[name]["sixes_link"]
    for name, (what, side, n) in [*MARKS.items(), ("sight", SIGHT)]:
        got = out[SIGHT[0] if name == "sight" else name]
        count = got["sight" if name == "sight" else what]
        held[name] = got["seeds"] == got["of"] and (count >= n if side == "least" else count <= n)
    held["sixes"] = all("sixes" in out[name] for name in EMPTY) and sixes <= MOST_SIXES
    return out, held


def step1(which):
    """The real fields on the fitting years only: what each model claims. Nothing after 2003 is loaded into the fit."""
    if not all(marks(rows())[1].values()):
        sys.exit("The made-up panels are incomplete or a mark missed. The real fields are not set against drought.")
    done = {(r["field"], r["outcome"]) for r in rows() if r["kind"] == "fit"}
    for name in which:
        for kind in KINDS:
            if (name, kind) not in done:
                row({"kind": "fit", "field": name, "outcome": kind, **fitted(real(name), kind, fire.FIT)[1]})


def step2():
    """Once: every field and outcome scored on 2004 to 2018, and the fields together."""
    done = rows()
    if any(r["kind"] in ("score", "pooled") for r in done):
        sys.exit("Already scored. The years after 2003 are spent for this driver and these fields.")
    fits = [r for r in done if r["kind"] == "fit"]
    if len(fits) != len(KINDS) * len(fire.FIELDS):
        sys.exit("Step 1 is incomplete. The years after 2003 stay sealed.")
    if not all(any(r["k"] > 0 for r in fits if r["outcome"] == kind) for kind in KINDS[:2]):
        sys.exit("Nothing held up within the fitting years on burned area, or nothing once the share observed is taken out. There is nothing to score and the years after 2003 stay sealed.")
    passed = {}
    for kind in KINDS:
        parts = {}
        for name in fire.FIELDS:
            model, info, parts[name] = scored(real(name), kind)
            row({"kind": "score", "field": name, "outcome": kind, **info, **verdict(*parts[name]), "by_year": {"base": parts[name][0].round(3).tolist(), "model": parts[name][1].round(3).tolist()}})
        out = verdict(*pooled(parts, list(fire.FIELDS)))
        passed[kind] = out["passes"]
        row({"kind": "pooled", "outcome": kind, "fields": list(fire.FIELDS), **out})
    row({"kind": "reading", "link": link(passed), "also_in_what_the_satellite_saw": passed["sight"]})


if __name__ == "__main__":
    if sys.argv[1] == "known":
        known(sys.argv[2:] or list(MADE_UP))
    elif sys.argv[1] == "marks":
        print(*marks(rows()), sep="\n")
    elif sys.argv[1] == "fit":
        step1(sys.argv[2:] or list(fire.FIELDS))
    elif sys.argv[1:] == ["score", "once"]:
        step2()
    else:
        sys.exit("run_local.py known [panel ...] | marks | fit [field ...] | score once")
