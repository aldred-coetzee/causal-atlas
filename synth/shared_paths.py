"""Slow unrecorded paths shared by two series of a place, planted on made-up tables (rule 3).

Shares no code or assumptions with the methods tested on it; numpy only.
Built from docs/specs/2026-11-10-shared-paths.md, after `table_panel.make`.
"""
import warnings

import numpy as np

KINDS = ("waves", "cycle", "boom", "wander", "regimes", "quasi_cycle")
FORESEEABLE = {"waves": True, "cycle": True, "boom": True,
               "wander": False, "regimes": False, "quasi_cycle": False}
SALT = 7919  # own number, so no stream is shared with table_panel (which spawns from the bare seed)
SIZE_MEDIAN, SIZE_SPREAD, SIZE_RANGE = 1.5, 0.6, (0.3, 4.5)


def _waves(r, T):
    """Two adoption waves (S-curves) a few decades apart: a technology, then its successor. Foreseeable."""
    t = np.arange(T)
    out = np.zeros(T)
    for (lo, hi), amp in (((0.1, 0.4), 1.0), ((0.3, 0.6), r.uniform(0.5, 1.5) * r.choice([-1.0, 1.0]))):
        mid, width = r.uniform(lo, hi) * T, r.uniform(0.03, 0.08) * T
        out += amp / (1 + np.exp(-(t - mid) / width))
    return out


def _cycle(r, T):
    """A decadal climate mode of fixed period whose strength swells or fades steadily. Foreseeable."""
    t = np.arange(T)
    env = 1 + r.uniform(-0.5, 0.8) * t / T
    return env * np.sin(2 * np.pi * t / r.uniform(18, 45) + r.uniform(0, 2 * np.pi))


def _boom(r, T):
    """A boom and bust, such as a resource or a bubble: one smooth hump of random width. Foreseeable."""
    t = np.arange(T)
    return np.exp(-0.5 * ((t - r.uniform(0.2, 0.6) * T) / (r.uniform(0.1, 0.25) * T)) ** 2)


def _wander(r, T):
    """Slowly drifting institutions or attitudes: a random walk, lightly smoothed. Fresh movement every year."""
    walk = np.cumsum(r.standard_normal(T))
    return np.convolve(np.pad(walk, 1, mode="edge"), np.ones(3) / 3, mode="valid")


def _regimes(r, T):
    """Policy or climate regimes: levels that shift at random times, about every dozen years, over four-year ramps."""
    n = max(2, r.poisson(T / 12))
    at = np.sort(r.choice(np.arange(3, max(T - 3, 4)), size=min(n, max(T - 6, 1)), replace=False))
    jumps = r.standard_normal(len(at))
    t = np.arange(T)[:, None]
    return (jumps * np.clip((t - at[None, :]) / 4 + 0.5, 0, 1)).sum(axis=1)


def _quasi_cycle(r, T):
    """An oscillation like ENSO or an ocean mode: a slow cycle whose phase wanders. Fresh movement every year."""
    phase = 2 * np.pi * np.arange(T) / r.uniform(18, 45) + r.uniform(0, 2 * np.pi)
    return np.sin(phase + np.cumsum(r.normal(0, 0.12, T)))


_MAKERS = {"waves": _waves, "cycle": _cycle, "boom": _boom, "wander": _wander,
           "regimes": _regimes, "quasi_cycle": _quasi_cycle}


def _unit(x):
    """Centre a path and scale it to unit spread over the record."""
    x = x - x.mean()
    return x / max(x.std(), 1e-9)


def _paths(rng, places, kind, T):
    """Unit-spread paths (places, years) for the given place indices, and the kind each place drew."""
    out = np.zeros((len(places), T))
    names = np.full(len(places), "", dtype="<U11")
    for i in range(len(places)):
        k = KINDS[rng.integers(len(KINDS))] if kind == "mixed" else kind
        out[i], names[i] = _unit(_MAKERS[k](rng, T)), k
    return out, names


def _sizes(rng, n):
    """Size by place: lognormal around SIZE_MEDIAN (the middle place sits exactly on it), clipped."""
    z = rng.standard_normal(n)
    return np.clip(SIZE_MEDIAN * np.exp(SIZE_SPREAD * (z - np.median(z))), *SIZE_RANGE)


def _spread(x):
    """Each place's spread of a series over the record, ignoring gaps (zero where it has no values)."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        s = np.nanstd(x, axis=1)
    return np.nan_to_num(s)


def add(world, seed, kind, strength=1.0, pairs=2, frac=0.5):
    """Return a copy of `world` with `pairs` shared slow paths added, and a list `paths` describing them.

    Each pair is an outcome and a local series, neither in `truth`; in `frac` of the groups
    (whole groups) both get the same year's path value times their own spread there times
    `strength` times a size by place (middle place 1.5; the series' sign is `sign`).
    `_paths` is for tests only: the path added to each pair's outcome, (places, years).
    """
    if kind != "mixed" and kind not in KINDS:
        raise ValueError(kind)
    values, role, group = world["values"], world["role"], world["group"]
    S, P, T = values.shape
    taken = set()
    for t in world["truth"]:
        taken |= {t["outcome"], *(s for s, _ in t["inputs"])} | ({t["state"]} if "state" in t else set())
    outs = [s for s in range(S) if role[s] == "outcome" and s not in taken]
    locs = [s for s in range(S) if role[s] == "local" and s not in taken]
    if pairs > min(len(outs), len(locs)):
        raise ValueError("not enough free series for that many pairs")
    ss_pairs, ss_places, ss_paths = np.random.SeedSequence([seed, SALT]).spawn(3)
    r = np.random.default_rng(ss_pairs)
    po = r.permutation(outs)[:pairs]
    pl = r.permutation(locs)[:pairs]
    signs = r.choice([-1, 1], size=pairs)
    groups = np.unique(group)
    k = max(1, int(round(frac * len(groups))))
    new = values.copy()
    info, shown = [], []
    for o, s, sg, cp, cs in zip(po, pl, signs, ss_places.spawn(pairs), ss_paths.spawn(pairs)):
        mask = np.isin(group, np.random.default_rng(cp).choice(groups, k, replace=False))
        where = np.flatnonzero(mask)
        rr = np.random.default_rng(cs)
        unit, names = _paths(rr, where, kind, T)
        size = _sizes(rr, len(where))[:, None] * strength * unit
        so, ss = _spread(values[o, where]), _spread(values[s, where])
        new[o, where] += so[:, None] * size
        new[s, where] += sg * ss[:, None] * size
        path = np.zeros((P, T))
        path[where] = so[:, None] * size
        kinds = np.full(P, "", dtype="<U11")
        kinds[where] = names
        info.append(dict(outcome=int(o), series=int(s), places=mask, kind=kind, sign=int(sg), kinds=kinds))
        shown.append(path)
    return {**world, "values": new, "paths": info, "_paths": shown}
