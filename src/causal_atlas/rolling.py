"""Does a driver that differs from place to place improve a forecast some months ahead of a record with gaps, when each year is forecast from the years before it only. The baseline is chosen again and fitted again at every year; slopes are shared first by every unit, then by the units of wide squares, then of five-degree squares, each kind of square placed twice; the years are the unit of evidence. Built for staple prices at markets and tried on made-up panels only: no rule is registered for it and it has been run on no real record (decision 0050)."""
import numpy as np

from causal_atlas import local
from causal_atlas.forecast import all_months, folds, skill

BASELINES = ("zero", "level", "linear")
CARRY = 3  # months a collected value stands in for the months after it, as a predictor only
CLIP = 4.0
LEAST_PAST = 24  # months of the outcome before a year, for a unit to be scaled and used in forecasting it
LEAST = 8  # units in use in a square, for one of its calendar months to be tested
LEAST_YEARS = 3  # fitting years in which a unit's calendar month can be scored, for it to count
SCALES = (None, 20.0, local.BLOCK)  # degrees: the squares whose units share a slope. None: every unit shares one
REACH = 1.5  # degrees each way: a unit's neighbours
LONGEST = 12  # months: the longest lag of the driver


def carried(v, n=CARRY):
    """v with each gap filled by the last value before it, for up to n months."""
    out = v.copy()
    for _ in range(n):
        gap = np.isnan(out[:, 1:]) & np.isfinite(out[:, :-1])
        out[:, 1:][gap] = out[:, :-1][gap]
    return out


def over_a_year(v):
    """The change in v over twelve months; nought in the first year, where there is none."""
    out = np.zeros(v.shape)
    out[:, 12:] = v[:, 12:] - v[:, :-12]
    return out


def change(logp):
    """The change in log price over twelve months, from carried values (NaN where either end is unknown), and where a price was collected."""
    f = carried(logp)
    y = np.full(f.shape, np.nan)
    y[:, 12:] = f[:, 12:] - f[:, :-12]
    return y, np.isfinite(logp)


def neighbours(lat, lon, reach=REACH):
    """Units by units: 1 where another unit lies within reach degrees both ways."""
    nb = (np.abs(lat[:, None] - lat[None, :]) <= reach) & (np.abs(lon[:, None] - lon[None, :]) <= reach)
    np.fill_diagonal(nb, False)
    return nb.astype(np.float64)


def near_mean(y, nb):
    """The mean of each unit's neighbours with a value that month; its own value where none has."""
    ok = np.isfinite(y)
    total, count = nb @ np.where(ok, y, 0), nb @ ok
    return np.where(count > 0, total / np.maximum(count, 1), y)


def back(v, lag):
    """v as it stood lag months earlier."""
    out = np.full(v.shape, np.nan)
    out[:, lag:] = v[:, :-lag]
    return out


def trail(v, ahead):
    """The mean of the twelve months ending ahead months back, where at least six of them have a value."""
    ok = np.isfinite(v)
    c = np.concatenate([np.zeros((len(v), 1)), np.cumsum(np.where(ok, v, 0), axis=1)], axis=1)
    n = np.concatenate([np.zeros((len(v), 1)), np.cumsum(ok, axis=1)], axis=1)
    hi = np.maximum(np.arange(v.shape[1]) - ahead + 1, 0)
    lo = np.maximum(hi - 12, 0)
    count = n[:, hi] - n[:, lo]
    return np.where(count >= 6, (c[:, hi] - c[:, lo]) / np.maximum(count, 1), np.nan)


def own_lags(ahead):
    return tuple(range(ahead, ahead + 4)) + (12,) * (ahead + 3 < 12)


def known(y, seen, nb, origin, ahead):
    """What is in hand when year origin is forecast ahead months ahead, on the months up to its end: the outcome over each unit's own spread before that year, clipped; the baseline's predictors, none nearer than ahead months back; and which unit-months can be forecast and scored (a value collected that month, and every predictor present)."""
    y = y[:, : 12 * (origin + 1)]
    past = np.isfinite(y[:, : 12 * origin])
    n = past.sum(axis=1)
    mean = np.where(past, y[:, : 12 * origin], 0).sum(axis=1) / np.maximum(n, 1)
    s = np.sqrt((np.where(past, y[:, : 12 * origin] - mean[:, None], 0) ** 2).sum(axis=1) / np.maximum(n, 1))
    ys = np.clip(y / np.where((n >= LEAST_PAST) & (s > 0), s, np.nan)[:, None], -CLIP, CLIP)
    cols = [back(ys, lag) for lag in own_lags(ahead)] + [back(near_mean(ys, nb), ahead), trail(ys, ahead)]
    ok = seen[:, : y.shape[1]] & np.isfinite(ys) & np.all([np.isfinite(c) for c in cols], axis=0)
    return ys, cols, ok


def predict(name, ys, cols, ok, fit):
    """A baseline's forecast of every unit-month. zero: no change on a year before. level: the unit's mean change over the last twelve months known. linear: one least-squares fit over all units on the months given."""
    if name == "zero":
        return np.zeros(ys.shape)
    if name == "level":
        return cols[-1]
    a = np.stack(cols + [np.ones(ys.shape)])
    rows = ok[:, fit]
    coef = np.linalg.lstsq(a[:, :, fit][:, rows].T, ys[:, fit][rows], rcond=None)[0]
    return np.tensordot(coef, a, axes=1)


def choose(ys, cols, ok, years):
    """The baseline with the least squared error on the years given, each block of years predicted from a fit on the others."""
    err = dict.fromkeys(BASELINES, 0.0)
    for f in folds(years):
        held = all_months(f)
        for name in BASELINES:
            p = predict(name, ys, cols, ok, all_months(np.setdiff1d(years, f)))
            err[name] += float(((ys[:, held] - p[:, held])[ok[:, held]] ** 2).sum())
    return min(BASELINES, key=err.get), err


def left(name, ys, cols, ok, years):
    """What a baseline fitted on the years given leaves, zero where a unit-month cannot be scored."""
    return np.where(ok, ys - predict(name, ys, cols, ok, all_months(years)), 0)


def sums(e, t, claimed, ok, years):
    """By year, over claimed unit-months that can be scored: the residual's squares, its products with the term, and the term's squares."""
    at = all_months(years)
    res = e[:, at].reshape(len(e), len(years), 12)
    w = claimed.T[:, None, :] & ok[:, at].reshape(res.shape)
    return np.array([np.where(w, v, 0).sum(axis=(0, 2)) for v in (res * res, res * t, t * t)])


def evidence(e, x, ok, group, years, season, lags):
    """local.evidence for a record with gaps: a unit's calendar month counts when it can be scored in at least LEAST_YEARS of the years, and a square's when at least LEAST units count. Returns the lag, how sure, the slope, which square-months are tested (each 12 by squares) and which unit-months count (units by 12)."""
    n = group.max() + 1
    to = np.zeros((n, len(group)))
    to[group, np.arange(len(group))] = 1
    a = np.zeros((len(lags), 12, n, len(years)))
    b = np.zeros(a.shape[:3])
    used = np.zeros((len(group), 12), bool)
    for m in range(12):
        at = 12 * years + m
        used[:, m] = ok[:, at].sum(axis=1) >= LEAST_YEARS
        w = ok[:, at] & used[:, m, None]
        for i, lag in enumerate(lags):
            d = x[:, at - lag] * w
            a[i, m] = to @ (d * e[:, at])
            b[i, m] = to @ (d * d).sum(axis=1)
    tested = (to @ used).T >= LEAST
    if season:
        a = np.broadcast_to((a * tested[None, :, :, None]).sum(axis=1, keepdims=True), a.shape)
        b = np.broadcast_to((b * tested[None]).sum(axis=1, keepdims=True), b.shape)
    sd = a.std(axis=-1, ddof=1)
    t = np.where(tested[None], np.divide(a.mean(axis=-1) * np.sqrt(len(years)), sd, out=np.zeros(sd.shape), where=sd > 0), 0)
    best = np.abs(t).argmax(axis=0)
    pick = lambda v: np.take_along_axis(v, best[None], axis=0)[0]
    slope = np.divide(pick(a.sum(axis=-1)), pick(b), out=np.zeros(best.shape), where=pick(b) > 0)
    return lags[best], pick(t), slope, tested, used


def tune(e, x, ok, group, years, lags):
    """local.tune for a record with gaps: by calendar month or one slope a season, how sure a slope must be, and the one number in 0 to 1 that sizes every kept slope, chosen together on each block of years with the evidence from the others."""
    b, c = np.zeros((2, len(local.TAUS))), np.zeros((2, len(local.TAUS)))
    for f in folds(years):
        if not len(f):
            continue
        for j in (0, 1):
            *found, used = evidence(e, x, ok, group, np.setdiff1d(years, f), bool(j), lags)
            for i, tau in enumerate(local.TAUS):
                lag, claimed, slope = local.spread(*found, tau, used, group)
                _, bf, cf = sums(e, local.term(x, f, lag, slope), claimed, ok, f)
                b[j, i], c[j, i] = b[j, i] + bf.sum(), c[j, i] + cf.sum()
    k = np.clip(np.divide(b, c, out=np.zeros(b.shape), where=c > 0), 0, 1)
    gain = 2 * k * b - k * k * c
    j, i = np.unravel_index(gain.argmax(), gain.shape)
    return bool(j), local.TAUS[i], float(k[j, i])


def claims(e, x, ok, group, years, lags):
    """One placing of the squares: the lag, the claim and the sized slope of every unit's calendar month, from the years given."""
    season, tau, k = tune(e, x, ok, group, years, lags)
    *found, used = evidence(e, x, ok, group, years, season, lags)
    lag, claimed, slope = local.spread(*found, tau, used, group)
    return lag, claimed & (k > 0), k * slope


def placings(lat, lon, size):
    """Each unit's square at each placing of the squares: twice, half a square apart. With no size, one placing with every unit in it."""
    if size is None:
        return [np.zeros(len(lat), int)]
    return [local.blocks(lat + o, lon + o, size) for o in (0.0, size / 2)]


def term(found, x, years):
    """What the placings of one scale add to the forecast of the years given, units by years by 12: each placing's slope times the unit's own driver at its lag, averaged over the placings that claim the unit's month; nought where none does."""
    n = np.maximum(sum(c.astype(int) for _, c, _ in found), 1).T[:, None, :]
    return sum(np.where(c.T[:, None, :], local.term(x, years, lag, slope), 0) for lag, c, slope in found) / n


def flat(x, years):
    """The driver with, for each unit and calendar month, its mean and its straight line across the years given (and the year before them, which the lags reach into) taken out: a level or a rise shared with the outcome over those years then earns nothing."""
    out = x.astype(np.float64).copy()
    span = np.arange(years[0] - 1, years[-1] + 1)
    t = span - span.mean()
    for m in range(12):
        v = out[:, 12 * span + m]
        v = v - v.mean(axis=1, keepdims=True)
        out[:, 12 * span + m] = v - t[None, :] * (v @ t)[:, None] / (t @ t)
    return out


def run(y, seen, x, lat, lon, years, ahead=3, first=2):
    """Each of years forecast from the years before it, ahead months ahead or more. y: units by months, NaN where unknown (change() of a price record); seen: where a value was collected; x: the driver, units by months on the same clock; years: the years to forecast, in order; first: the first year that can be a target.

    At each year: the baseline is chosen and fitted on the years before; then, scale by scale, slopes on the driver are fitted to what is left on those years and their term taken out before the next scale is fitted. Returns, by year: the baseline's squared error on the unit-months claimed, the model's with the driver as it was and under each whole-year shift of the driver field among years, the same with the driver made flat, each baseline's error alone, and what was claimed."""
    lags = np.arange(ahead + 1, LONGEST + 1)
    nb, groups, xf = neighbours(lat, lon), [placings(lat, lon, size) for size in SCALES], flat(x, years)
    out = {"base": [], "model": [], "flat": [], "alone": {b: [] for b in BASELINES}, "claimed": [], "units": [], "baseline": [], "by_scale": []}
    for i, origin in enumerate(years):
        ys, cols, ok = known(y, seen, nb, origin, ahead)
        fit, now = np.arange(first, origin), np.array([origin])
        name, _ = choose(ys, cols, ok, fit)
        e = left(name, ys, cols, ok, fit)
        rest, stages = e.copy(), []
        for placed in groups:
            found = [claims(rest, x[:, : e.shape[1]], ok, g, fit, lags) for g in placed]
            rest[:, all_months(fit)] -= np.where(ok[:, all_months(fit)], term(found, x, fit).reshape(len(e), -1), 0)
            stages.append(found)
        w = np.any([c for found in stages for _, c, _ in found], axis=0)
        res = []
        for drv in (x, xf):
            rows = []
            for s in range(len(years)):
                d = sum(term(found, drv, np.array([years[(i + s) % len(years)]])) for found in stages)
                a, b, c = sums(e, d, w, ok, now)
                rows.append(float(a[0] - 2 * b[0] + c[0]))
            res.append(rows)
        out["base"].append(float(a[0]))
        out["model"].append(res[0])
        out["flat"].append(res[1])
        for b in BASELINES:
            out["alone"][b].append(float(sums(left(b, ys, cols, ok, fit), np.zeros((len(ys), 1, 12)), w, ok, now)[0][0]))
        scored = w.T & ok[:, 12 * origin :]
        out["claimed"].append(int(scored.sum()))
        out["units"].append(int(scored.any(axis=1).sum()))
        out["baseline"].append(name)
        out["by_scale"].append([int(np.any([c for _, c, _ in found], axis=0).sum()) for found in stages])
    return {k: (np.array(v) if k in ("base", "model", "flat") else v) for k, v in out.items()}


def reading(r, seed=0):
    """The verdict on one run or several pooled (their by-year sums added): S with its interval over years, how many of the shifts it beats, the same with the driver made flat, whether the model's error is below each baseline's alone, and S without its best year."""
    base, model, flt = r["base"], r["model"], r["flat"]
    out = skill(base, model[:, 0], model[:, 1:].T, seed)
    f = skill(base, flt[:, 0], flt[:, 1:].T, seed)
    gain = base - model[:, 0]
    rest = np.arange(len(base)) != gain.argmax()
    out.update(
        flat_s=f["s"], flat_ci=f["ci"], flat_beats=f["beats"], shifts=int(model.shape[1] - 1),
        below={b: bool(model[:, 0].sum() < np.sum(r["alone"][b])) for b in BASELINES},
        without_best=float(1 - model[rest, 0].sum() / base[rest].sum()) if base[rest].sum() else float("nan"),
        by_year=[round(float(v), 4) for v in np.divide(gain, base, out=np.zeros(len(base)), where=base > 0)],
    )
    n = out["shifts"]
    ok = lambda ci, beats: bool(base.sum() > 0 and ci[0] > 0 and beats == n)
    out["passes"] = ok(out["ci"], out["beats"]) and ok(f["ci"], f["beats"]) and all(out["below"].values()) and out["without_best"] > 0
    return out
