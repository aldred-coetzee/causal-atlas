"""Made-up tables shaped like the yearly panel of the first read across the real table: places in groups of uneven size, 64 years, series that keep their level from one year to the next, some drifting, some wandering, gaps and late starts, a few series common to all places, series in sets. Development only (docs/specs/2026-11-11-parallel-helpers-fourth-wave.md, helper G).

What knows a truth is here: the links, the shared paths, and where they are. Shares no code or assumptions with anything that proposes or scores (rule 3): numpy only, nothing imported from causal_atlas or from scripts/lab_levels.py. Only the harness imports this file.

Two ways a link is put in:
  added:  as `plant` in scripts/run_stage_b.py does it (copied here so that its settings can be varied; with the defaults it gives the same table, which the harness checks): after the table is made, the outcome gains a multiple of the input the year before, sized so that the year-to-year changes of what is added are the stated share of the outcome's year-to-year movement.
  shock:  as synth/table_panel.py states a size: the link is put into what the outcome's own history leaves, the stated share of each year's new movement, before the outcome's memory carries it on.
"""
import warnings

import numpy as np

BURN = 60
NEED = ((0, 35, 25), (35, 54, 15), (54, 64, 8))  # values a place needs in each stretch of years to count for a series, as the real panel's rule
MIDDLE = 30  # places a year needs for the year's middle to be taken off
SETS = ("a", "b", "c", "d")
KINDS = ("wander", "cycle", "boom", "regimes", "bend")


def _groups(rng, places, n):
    size = 5 + rng.multinomial(places - 5 * n, rng.dirichlet(np.full(n, 2.0)))
    return np.repeat(np.arange(n), size)


def _where(rng, group, n_groups, frac, least=5):
    """Whole groups, at least `least`, holding at least `frac` of the places."""
    where, order, took = np.zeros(len(group), bool), list(rng.permutation(n_groups)), 0
    while where.sum() < frac * len(group) or took < least:
        where, took = where | (group == order.pop()), took + 1
    return where


def _run(e, phi, start):
    """Each place's path from its shocks: one year carried into the next by phi (1: a walk)."""
    d, out = start.copy(), np.empty(e.shape)
    scale = np.sqrt(1 - phi ** 2) if phi < 1 else 0.25
    for t in range(e.shape[1]):
        d = phi * d + scale * e[:, t]
        out[:, t] = d
    return out


def _path(rng, kind, years):
    """One slow path over the years, mean zero, spread one."""
    t = np.arange(years, dtype=float)
    if kind == "wander":
        h = np.cumsum(rng.standard_normal(years))
    elif kind == "cycle":
        h = np.sin(2 * np.pi * t / rng.uniform(12, 30) + rng.uniform(0, 2 * np.pi))
    elif kind == "boom":
        h = np.exp(-0.5 * ((t - rng.uniform(12, years - 12)) / rng.uniform(4, 10)) ** 2)
    elif kind == "regimes":
        cuts = np.sort(rng.choice(np.arange(6, years - 6), rng.integers(2, 5), replace=False))
        h = rng.standard_normal(len(cuts) + 1)[np.searchsorted(cuts, t, side="right")]
    else:  # bend: a line and a curve
        h = rng.standard_normal() * t / years + rng.standard_normal() * (t / years) ** 2
    return (h - h.mean()) / (h.std() if h.std() > 0 else 1.0)


def make(seed, places=166, years=64, series=120, common=3, groups=18, sets=(0.40, 0.35, 0.05, 0.20), memory=(0.85, 0.999), fixed=None, drift=0.35, walk=0.25, noise=0.1,
         gaps=True, need=NEED, shock=None, paths=0, path_kind="mixed", path_size=1.0):
    """A made-up table.
    memory: a series' one year is carried into the next by a number drawn so that its distance below 1 is spread evenly on a log scale between these two.
    fixed: {set name: memory} gives every series of that set that memory exactly, with no drift, walk or reading error; how the knobs of question 2 are turned.
    drift, walk: the share of series with a line of its own in each place, and the share that wander with no level to return to. noise: the most reading error, as a share of the series' spread.
    shock: None, or {"sizes": (...), "links": n, "frac": share of places, "from": set name or None}: links put into the outcome's new movement each year.
    paths: pairs of series from different sets given a shared slow path in half the groups, with no link between them; path_kind one of KINDS or "mixed"; path_size: the path's spread in units of each series' own.
    Returns values (series, places, years), group, groups, common, sets, ids, allowed (a row for an outcome may name a series only from another set), outcomes, truth (shock links), paths, phi."""
    ss = dict(zip(("layout", "base", "gaps", "links", "paths"), np.random.SeedSequence(seed).spawn(5)))
    rng = {k: np.random.default_rng(v) for k, v in ss.items()}
    S, P, T, G = series, places, years + BURN, groups
    r = rng["layout"]
    group = _groups(r, P, G)
    is_common = np.arange(S) >= S - common
    share = np.asarray(sets, float) / np.sum(sets)
    set_of = np.where(is_common, len(SETS) - 1, r.choice(len(SETS), S, p=share))
    for k in range(len(SETS)):  # every set has at least two series that differ by place
        while ((set_of == k) & ~is_common).sum() < 2:
            set_of[r.choice(np.flatnonzero(~is_common & (np.bincount(set_of, minlength=len(SETS))[set_of] > 3)))] = k
    lo, hi = memory
    phi = 1 - np.exp(r.uniform(np.log(1 - hi), np.log(1 - lo), S))
    kind = r.random(S)
    walks, drifts = kind < walk, (kind >= walk) & (kind < walk + drift)
    err = r.uniform(0, noise, S)
    phi[is_common] = r.uniform(0.2, 0.9, common)
    walks[is_common], drifts[is_common] = False, False
    for name, value in (fixed or {}).items():
        mine = (set_of == SETS.index(name)) & ~is_common
        phi[mine], walks[mine], drifts[mine], err[mine] = value, False, False, 0.0
    phi[walks] = 1.0

    b = rng["base"]
    sd = b.uniform(0.5, 3.0, S)
    spread = sd[:, None] * np.exp(0.4 * b.standard_normal((S, P)))
    mu = b.normal(10, 5, S)[:, None] + sd[:, None] * b.standard_normal((S, P))
    heavy = lambda shape: b.standard_t(5, size=shape) / np.sqrt(5 / 3)
    idio, grp, allp = heavy((S, P, T)), heavy((S, G, T)), heavy((S, T))
    e = np.sqrt(0.65) * idio + np.sqrt(0.25) * grp[:, group] + np.sqrt(0.10) * allp[:, None, :]
    e[is_common] = allp[is_common][:, None, :]
    start = b.standard_normal((S, P))
    start[is_common] = start[is_common, :1]
    slope = b.standard_normal((S, P)) * 4.0  # a drifting series crosses about four of its own spreads over the years
    read = b.standard_normal((S, P, T))
    dev = np.array([_run(e[s], phi[s], start[s]) for s in range(S)])

    vary = np.flatnonzero(~is_common)
    allowed = set_of[:, None] != set_of[None, :]
    truth = []
    if shock:
        k = rng["links"]
        sizes, links, frac = shock.get("sizes", (0.35, 0.20, 0.10)), shock.get("links", 3), shock.get("frac", 0.25)
        cand = vary if shock.get("from") is None else vary[set_of[vary] == SETS.index(shock["from"])]
        outs = k.choice(cand, links * len(sizes), replace=False)
        for n, o in enumerate(outs):
            x = int(k.choice([s for s in vary if allowed[o, s] and s not in outs]))
            where = _where(k, group, G, frac)
            sig = dev[x][:, :-1]
            sig = (sig - sig.mean(axis=1, keepdims=True)) / sig.std(axis=1, keepdims=True)
            size = sizes[n // links]
            e[o][where, 1:] = np.sqrt(1 - size) * e[o][where, 1:] + np.sqrt(size) * sig[where]
            dev[o] = _run(e[o], phi[o], start[o])
            truth.append({"outcome": int(o), "input": x, "share": size, "where": where})

    tau = np.arange(T) / T
    x = mu[:, :, None] + spread[:, :, None] * (dev + drifts[:, None, None] * slope[:, :, None] * tau + err[:, None, None] * read)
    x = x[:, :, BURN:].copy()

    made = []
    if paths:
        k = rng["paths"]
        free = [s for s in vary if not any(s in (t["outcome"], t["input"]) for t in truth)]
        for _ in range(paths):
            a = int(k.choice(free))
            c = int(k.choice([s for s in free if allowed[a, s]]))
            free = [s for s in free if s not in (a, c)]
            where = _where(k, group, G, 0.5)
            what = path_kind if path_kind != "mixed" else KINDS[k.integers(len(KINDS))]
            h = np.zeros((P, years))
            for g in np.unique(group[where]):
                h[group == g] = _path(k, what, years)
            own = np.array([_path(k, what, years) for _ in range(P)])
            h = np.where(where[:, None], (h + 0.5 * own) / np.sqrt(1.25), 0.0)
            for s in (a, c):
                x[s] += path_size * k.choice([-1.0, 1.0]) * k.uniform(0.7, 1.4, P)[:, None] * spread[s][:, None] * h
            made.append({"pair": (a, c), "kind": what, "where": where})

    if gaps:
        g = rng["gaps"]
        out = g.random((S, P)) < g.uniform(0.0, 0.6, S)[:, None]  # places a series does not have at all
        late = np.where(g.random((S, P)) < 0.3, g.integers(1, 10, (S, P)), 0)
        miss = (np.arange(years)[None, None, :] < late[:, :, None]) | (g.random((S, P, years)) < g.uniform(0.0, 0.06, S)[:, None, None]) | out[:, :, None]
        miss[is_common] = False
        x[miss] = np.nan
        have = np.isfinite(x)
        counts = np.all([have[:, :, a:c].sum(axis=2) >= n for a, c, n in need if c <= years], axis=0)
        x = np.where(counts[:, :, None], x, np.nan)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        mid = np.where(np.isfinite(x).sum(axis=1) >= MIDDLE, np.nanmedian(x, axis=1), np.nan)
    x = np.where(is_common[:, None, None], x, x - mid[:, None, :])  # each series that differs by place as its departure from the year's middle, as the real panel is made
    return {"values": x, "group": group, "groups": np.array([f"g{i:02d}" for i in range(G)]), "common": is_common, "sets": np.array([SETS[i] for i in set_of]), "ids": np.array([f"s{i:03d}" for i in range(S)]),
            "allowed": allowed, "outcomes": vary, "truth": truth, "paths": made, "phi": phi}


def memory(a):
    """How one year goes with the next in each place of a series: the middle place's."""
    out = []
    for row in a:
        ok = np.isfinite(row[1:] + row[:-1])
        if ok.sum() > 10:
            out.append(np.corrcoef(row[1:][ok], row[:-1][ok])[0, 1])
    return float(np.nanmedian(out)) if out else float("nan")


def plant(p, v, seed, sizes=(0.35, 0.20, 0.10), links=3, frac=0.25, last=54, least=5, outcomes_from=None):
    """A copy of `plant` in scripts/run_stage_b.py with its settings as arguments; with the defaults the same draws in the same order, so the same table. outcomes_from: a set name the outcomes are taken from, where a knob needs outcomes and inputs to differ."""
    rng = np.random.default_rng(seed)
    v, vary = v.copy(), np.flatnonzero(~p["common"])
    cand = vary if outcomes_from is None else vary[p["sets"][vary] == outcomes_from]
    outs, truth = rng.choice(cand, links * len(sizes), replace=False), []
    for n, o in enumerate(outs):
        x = int(rng.choice([s for s in vary if p["allowed"][o, s] and s not in outs]))
        where, groups, took = np.zeros(v.shape[1], bool), list(rng.permutation(len(p["groups"]))), 0
        while where.sum() < frac * v.shape[1] or took < least:
            where, took = where | (p["group"] == groups.pop()), took + 1
        share = sizes[n // links]
        with np.errstate(invalid="ignore", divide="ignore"), warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            early = v[x][:, :last]
            moves = np.nanstd(np.diff(early, axis=1), axis=1)
            z = np.nan_to_num((v[x] - np.nanmean(early, axis=1, keepdims=True)) / np.where(moves > 0, moves, np.nan)[:, None])
            step = np.nan_to_num(np.nanstd(np.diff(v[o][:, :last], axis=1), axis=1))
        v[o][where, 1:] += np.sqrt(share / (1 - share)) * step[where, None] * z[where, :-1]
        truth.append({"outcome": int(o), "input": x, "share": share, "where": where})
    return v, truth
