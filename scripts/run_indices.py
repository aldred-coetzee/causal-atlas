"""Every series the candidate rule lets in, and the ONI, among decoys: which are named for each field, what the search can hear with that many candidates, then whether a named one adds to the forecast beyond own history and El Niño. Rule: results/real-indices.md."""
import json
import sys
from pathlib import Path

import numpy as np

import index_candidates
from causal_atlas import decoy, field, forecast, links
from index_names import NAMES
from run_continents import ALARMS, NAMED, SCORED, data, units
from run_continents import rows as scored_rows
from run_enso import AREAS, DISCOVERY, RULER_LAG, SHIFTS, YEARS, planted

OUT = Path(__file__).resolve().parents[1] / "results" / "real-indices.jsonl"
REAL = ("oni", *NAMES)
DECOYS = 18
SEEDS = {name: range(13101 + 100 * i, 13121 + 100 * i) for i, name in enumerate(field.BOXES)}
RULER_SEEDS = {name: range(13601 + 100 * i, 13611 + 100 * i) for i, name in enumerate(field.BOXES)}
SHARES = (0.05, 0.15, 0.40)
CHECK = (0.40, 0.25)  # the planted link the instrument check is marked on: share of variance, share of cells
FOUND, FOUND_EACH, INSIDE = 45, 8, 0.8  # of 50 pooled, of 10 in each field, share of claims in the planted cells
EXPECTED = ("south_america", "australia", "south_southeast_asia", "north_america")  # where the ONI was named before
ALL_YEARS = np.arange(1, field.MONTHS // 12)
DRAWS = 20000


def index(name):
    """One index as its departure from its own calendar-month means over the discovery years, in units of its spread there. Nothing after the discovery years sets the scale."""
    x = field.series(f"{index_candidates.DIR}/{name}").reshape(-1, 12)
    x = (x - x[: DISCOVERY // 12].mean(axis=0)).ravel()
    return x / x[:DISCOVERY].std()


def real():
    return np.array([field.oni(), *(index(n) for n in NAMES)])


def line():
    """A straight line in time, on the indices' scale: the control for a trend."""
    t = np.arange(field.MONTHS, dtype=float)
    return (t - t[:DISCOVERY].mean()) / t[:DISCOVERY].std()


def row(r):
    with open(OUT, "a") as f:
        f.write(json.dumps(r) + "\n")
    print({k: v for k, v in r.items() if k not in ("shifted", "by_year", "broad", "sharp")}, flush=True)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def have(kind, *keys):
    """The runs of one kind already in the rows, so a run that was stopped picks up where it left off. Every run draws only on its own seed, so its row is the same whenever it is made."""
    return {tuple(r[k] for k in keys) for r in rows() if r["kind"] == kind}


def name(which):
    """Naming on the discovery years of one field: the real series first, then the decoys."""
    y, _, lat, lon = data(which)
    y, x = y[:, :DISCOVERY], real()[:, :DISCOVERY]
    for seed in SEEDS[which]:
        d = decoy.make(seed, field.MONTHS, field.oni(), DECOYS)[:, :DISCOVERY]
        order = np.random.default_rng(seed).permutation(DISCOVERY // 12)
        mixed = y.reshape(len(y), -1, 12)[:, order].reshape(len(y), -1)
        for kind, field_y in (("real", y), ("years_mixed", mixed)):
            if (which, seed) in have(kind, "field", "seed"):
                continue
            row({"kind": kind, "field": which, "seed": seed, **links.both(field_y, [*x, *d], YEARS, SHIFTS, lat, lon, most=len(x))})


def ruler(which):
    """What the search hears on one field with these candidates: a link planted from the first decoy, at each size and extent."""
    y, _, lat, lon = data(which)
    y, x = y[:, :DISCOVERY], real()[:, :DISCOVERY]
    for seed in RULER_SEEDS[which]:
        d = decoy.make(seed, field.MONTHS, field.oni(), DECOYS)[:, :DISCOVERY]
        for share in SHARES:
            for area in AREAS:
                if (which, seed, share, area) in have("ruler", "field", "seed", "share", "area"):
                    continue
                yp, cells, months = planted(y, lat, lon, d[0], seed, share, area)
                out = links.both(yp, [*x, *d], YEARS, SHIFTS, lat, lon, most=len(x) + 1)
                more = {"share": share, "area": area, "found": len(x) in out["leads"], "false": [c for c in out["leads"] if c > len(x)]}
                if more["found"]:
                    sig = links.significant(links.correlations(yp, d[0], YEARS), len(YEARS))
                    inside = np.zeros(len(y), bool)
                    inside[cells] = True
                    more["claims"] = int(sig.sum())
                    more["claims_true_cells"] = round(float(sig[:, :, inside].sum() / max(sig.sum(), 1)), 3)
                    more["true_cell_months_claimed"] = round(float(sig[RULER_LAG][months][:, inside].mean()), 3)
                row({"kind": "ruler", "field": which, "seed": seed, **out, **more})


def marks(done):
    """By field and real series: sets in which it is a lead. Pooled: runs with a decoy a lead, and years-mixed runs with any lead."""
    run = [r for r in done if r["kind"] == "real"]
    named = {f: {n: sum(i in r["leads"] for r in run if r["field"] == f) for i, n in enumerate(REAL)} for f in field.BOXES}
    alarms = {
        "decoy": sum(any(c >= len(REAL) for c in r["leads"]) for r in run),
        "years_mixed": sum(bool(r["leads"]) for r in done if r["kind"] == "years_mixed"),
    }
    return named, alarms, len(run)


def instrument(done):
    """The ruler's table by field, and whether the instrument check holds: the marked link found often enough, pooled and in each field, with its claims in the planted cells."""
    run = [r for r in done if r["kind"] == "ruler"]
    table = {f: {f"{s:.2f} over {a:.2f}": sum(r["found"] for r in run if (r["field"], r["share"], r["area"]) == (f, s, a)) for s in SHARES for a in AREAS} for f in field.BOXES}
    marked = [r for r in run if (r["share"], r["area"]) == CHECK]
    found = {f: sum(r["found"] for r in marked if r["field"] == f) for f in field.BOXES}
    inside = min((r["claims_true_cells"] for r in marked if r["found"]), default=0.0)
    holds = len(marked) == 10 * len(field.BOXES) and sum(found.values()) >= FOUND and min(found.values()) >= FOUND_EACH and inside >= INSIDE
    return table, {"found": found, "least_inside": inside, "decoy_named": sum(bool(r["false"]) for r in run), "runs": len(run)}, holds


def first(which, scale):
    """The model as tested for one field, checked against its scored row, and what it leaves on every month."""
    y, near, x = units(which, scale)
    model = forecast.fit(y, near, x, DISCOVERY)
    was = next(r for r in scored_rows() if r["kind"] == "confirmation" and r["field"] == which and r["scale"] == scale)
    assert (model["baseline"], int(model["claimed"].sum()), round(model["k"], 3)) == (was["baseline"], was["claimed"], was["k"])
    return y, near, forecast.residual(model, x, ALL_YEARS)


def check(y, near, left, z, level):
    """One further driver on one field: fitted on the discovery years to what the tested model left, scored on the years after."""
    more = forecast.after(left, z, DISCOVERY)
    base, got, shifted = forecast.score(more, z, SCORED)
    alone = forecast.errors(y, near, more["claimed"], DISCOVERY, SCORED)
    out = forecast.skill(base, got, shifted, level=level, draws=DRAWS)
    out.update(
        k=round(more["k"], 3),
        claimed=int(more["claimed"].sum()),
        units_with_claim=int(more["claimed"].any(axis=0).sum()),
        lags=np.bincount(more["lag"][more["claimed"]], minlength=13)[4:].tolist(),
        model_error=round(float(got.sum()), 2),
        alone={k: round(float(v.sum()), 2) for k, v in alone.items()},
        by_year={"base": base.round(3).tolist(), "model": got.round(3).tolist()},
    )
    out["below_every_baseline"] = bool(all(got.sum() < v.sum() for v in alone.values()))
    out["passes"] = bool(out["ci"][0] > 0 and out["beats"] == len(out["shifted"]) and out["below_every_baseline"])
    return out


def confirmation():
    done = rows()
    if any(r["kind"] in ("confirmation", "line") for r in done):
        sys.exit("Already scored. The years after 1999 are spent for these indices and these fields.")
    named, alarms, runs = marks(done)
    kept = all(named[f]["oni"] >= NAMED for f in EXPECTED)
    if runs != 20 * len(field.BOXES) or any(v > ALARMS for v in alarms.values()) or not kept:
        sys.exit(f"Naming is incomplete or a naming mark missed ({runs} runs, {alarms}, ONI kept: {kept}). The years after 1999 stay sealed.")
    if not instrument(done)[2]:
        sys.exit(f"The instrument check is incomplete or missed ({instrument(done)[1]}). The years after 1999 stay sealed.")
    pairs = [(f, n) for f in field.BOXES for n in NAMES if named[f][n] >= NAMED]
    if not pairs:
        sys.exit("No index beyond the ONI was named in any field. Nothing to score; the years after 1999 stay sealed for them.")
    level = 1 - 0.05 / len(pairs)
    for scale in ("region", "cell"):
        for which in dict.fromkeys(f for f, _ in pairs):
            y, near, left = first(which, scale)
            for n in (n for f, n in pairs if f == which):
                row({"kind": "confirmation", "scale": scale, "field": which, "index": n, "pairs": len(pairs), "level": level, **check(y, near, left, index(n), level)})
            row({"kind": "line", "scale": scale, "field": which, **check(y, near, left, line(), 0.95)})


if __name__ == "__main__":
    assert NAMES == index_candidates.kept(), "the frozen names are not what the candidate rule lets in"
    if sys.argv[1] in ("name", "ruler"):
        for which in sys.argv[2:] or field.BOXES:
            {"name": name, "ruler": ruler}[sys.argv[1]](which)
    elif sys.argv[1] == "marks":
        print(marks(rows()), instrument(rows()), sep="\n")
    elif sys.argv[1:] == ["confirm", "once"]:
        confirmation()
    else:
        sys.exit("run_indices.py name [field ...] | ruler [field ...] | marks | confirm once")
