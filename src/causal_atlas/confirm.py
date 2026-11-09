"""Out-of-time check of a named driver against the baseline of own history, season and neighbours. Rule: results/real-enso-drought.md, "Confirmation"."""
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

from causal_atlas import links

OWN_LAGS = (3, 4, 5, 6, 12)
CLAIM_LAGS = tuple(range(4, 13))
DRAWS = 2000


def neighbours(lat, lon, step=0.5):
    """For each cell, the indices of its up to 8 neighbours on the grid, -1 where there is none."""
    at = {(round(a / step), round(o / step)): i for i, (a, o) in enumerate(zip(lat, lon))}
    out = np.full((len(lat), 8), -1)
    for (a, o), i in at.items():
        around = [(a + da, o + do) for da in (-1, 0, 1) for do in (-1, 0, 1) if da or do]
        out[i] = [at.get(k, -1) for k in around]
    return out


def near_mean(y, nb):
    """The mean of each cell's neighbours, by month; the cell's own value where it has none."""
    has = nb >= 0
    total = np.where(has[:, :, None], y[np.maximum(nb, 0)], 0).sum(axis=1)
    count = has.sum(axis=1)[:, None]
    return np.where(count > 0, total / np.maximum(count, 1), y)


def features(y, near, lat, lon, months):
    """One row per cell and target month, cells varying fastest within a month."""
    cols = [y[:, months - lag].T.ravel() for lag in OWN_LAGS]
    cols.append(near[:, months - 3].T.ravel())
    cols.append(np.repeat(months % 12, len(lat)))
    cols.append(np.tile(lat, len(months)))
    cols.append(np.tile(lon, len(months)))
    return np.stack(cols, axis=1).astype(np.float32)


def baseline(y, lat, lon, fit, score, seed=0):
    """Predictions on the fit and score months, cells by months, from a model fitted on the fit months only."""
    near = near_mean(y, neighbours(lat, lon))
    model = HistGradientBoostingRegressor(max_iter=200, random_state=seed)
    model.fit(features(y, near, lat, lon, fit), y[:, fit].T.ravel())
    return [model.predict(features(y, near, lat, lon, m)).reshape(len(m), len(lat)).T for m in (fit, score)]


def claims(y, x, years):
    """Per cell and calendar month: the lag from CLAIM_LAGS with the largest absolute correlation, and whether it is significant."""
    r = links.correlations(y, x, years, CLAIM_LAGS)
    sig = links.significant(r, len(years))
    best = np.abs(r).argmax(axis=0)
    lag = np.asarray(CLAIM_LAGS)[best]
    return lag.T, np.take_along_axis(sig, best[None], axis=0)[0].T


def slopes(res, x, months, lag, claimed):
    """Through the origin, per claimed cell and calendar month, shrunk by 1 - 1/t², floored at 0. Cells by 12."""
    out = np.zeros(lag.shape)
    for m in range(12):
        cols = np.where(months % 12 == m)[0]
        for c in np.where(claimed[:, m])[0]:
            d, e = x[months[cols] - lag[c, m]], res[c, cols]
            b = (d @ e) / (d @ d)
            se = np.sqrt(((e - b * d) ** 2).sum() / (len(d) - 1) / (d @ d))
            t = b / se if se > 0 else 0.0
            out[c, m] = b * max(0.0, 1 - 1 / (t * t)) if t else 0.0
    return out


def added(x, months, lag, slope, year_shift=0):
    """The driver's term on the score months, cells by months. A shift gives each target year the driver values of another, circularly."""
    n = len(months) // 12
    year = (np.arange(len(months)) // 12 + year_shift) % n
    moved = months[0] + 12 * year + months % 12 - months[0] % 12
    m = months % 12
    return slope[:, m] * x[moved[None, :] - lag[:, m]]


def skill(err_model, err_base, pick, years):
    """S = 1 - SSE(model) / SSE(baseline) over the picked cell-months, with a bootstrap over years."""
    a = np.where(pick, err_model, 0).reshape(len(pick), years, 12).sum(axis=(0, 2))
    b = np.where(pick, err_base, 0).reshape(len(pick), years, 12).sum(axis=(0, 2))
    if not b.sum():
        return float("nan"), [float("nan")] * 2
    rng = np.random.default_rng(0)
    draws = rng.integers(years, size=(DRAWS, years))
    boot = 1 - a[draws].sum(axis=1) / b[draws].sum(axis=1)
    return 1 - a.sum() / b.sum(), [float(v) for v in np.percentile(boot, [2.5, 97.5])]


def run(y, x, lat, lon, split):
    """Everything fitted on months before split; scored on whole years from split to the end."""
    fit, score = np.arange(12, split), np.arange(split, y.shape[1])
    years = np.arange(1, split // 12)
    base_fit, base = baseline(y, lat, lon, fit, score)
    lag, claimed = claims(y[:, :split], x[:split], years)
    slope = slopes(y[:, fit] - base_fit, x, fit, lag, claimed)
    truth, n = y[:, score], len(score) // 12
    pick = np.repeat(claimed[:, None, :], n, axis=1).reshape(len(y), -1)
    err_base = (truth - base) ** 2
    out = {"claimed_cell_months": int(claimed.sum()), "cells_with_claim": int(claimed.any(axis=1).sum()), "of_cells": len(y)}
    for shift in range(n):
        err = (truth - base - added(x, score, lag, slope, shift)) ** 2
        s, ci = skill(err, err_base, pick, n)
        if shift == 0:
            out["s_claimed"], out["ci_claimed"] = float(s), ci
            s_all, out["ci_all"] = skill(err, err_base, np.ones_like(pick), n)
            out["s_all"] = float(s_all)
            out["baseline_r2_all"] = float(1 - err_base.sum() / ((truth - truth.mean()) ** 2).sum())
        else:
            out.setdefault("shifted", []).append(round(float(s), 5))
    out["beats_shifted"] = int(sum(out["s_claimed"] > v for v in out["shifted"]))
    return out, {"lag": lag, "claimed": claimed, "slope": slope}
