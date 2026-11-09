"""Does a named driver improve a forecast three or more months ahead, beyond the best baseline the fitting years can choose. Units are rows: cells or region averages. Rule: results/real-enso-continents.md."""
import numpy as np

from causal_atlas import links

OWN_LAGS = (3, 4, 5, 6, 12)
CLAIM_LAGS = np.arange(4, 13)
FOLDS = 5
DRAWS = 2000
BASELINES = ("zero", "level", "linear")


def trail(y, n):
    """The mean of the n months ending at t - 3, on as many as exist."""
    c = np.concatenate([np.zeros((len(y), 1)), np.cumsum(y, axis=1, dtype=np.float64)], axis=1)
    hi = np.maximum(np.arange(y.shape[1]) - 2, 0)
    lo = np.maximum(hi - n, 0)
    return (c[:, hi] - c[:, lo]) / np.maximum(hi - lo, 1)


def design(y, near, months):
    """Own values at OWN_LAGS, the neighbours at t - 3, own trailing means of 12 and 60 months, and a constant. Rows: units fastest within a month."""
    cols = [y[:, months - lag] for lag in OWN_LAGS] + [near[:, months - 3], trail(y, 12)[:, months], trail(y, 60)[:, months]]
    return np.stack([c.T.ravel() for c in cols] + [np.ones(len(y) * len(months))], axis=1)


def baseline(name, y, near, fit, months):
    """Predictions on months, units by months. zero: the index's long-run average. level: the unit's last 60 months. linear: one least-squares fit over all units on the fit months."""
    if name == "zero":
        return np.zeros((len(y), len(months)))
    if name == "level":
        return trail(y, 60)[:, months]
    coef = np.linalg.lstsq(design(y, near, fit), y[:, fit].T.ravel().astype(np.float64), rcond=None)[0]
    return (design(y, near, months) @ coef).reshape(len(months), len(y)).T


def errors(y, near, claimed, split, years):
    """By baseline: its squared error by year on the claimed unit-months of the years given, fitted on months before split."""
    out = {}
    for name in BASELINES:
        e = np.zeros(y.shape)
        e[:, 12:] = y[:, 12:] - baseline(name, y, near, np.arange(12, split), np.arange(12, y.shape[1]))
        out[name] = sums(e, np.zeros((len(y), len(years), 12)), claimed, years)[0]
    return out


def folds(years):
    return np.array_split(years, FOLDS)


def all_months(years):
    return (12 * years[:, None] + np.arange(12)[None, :]).ravel()


def choose(y, near, years):
    """The baseline with the least squared error on the fitting years, each block of years predicted from a fit on the others."""
    err = dict.fromkeys(BASELINES, 0.0)
    for f in folds(years):
        fit, held = all_months(np.setdiff1d(years, f)), all_months(f)
        for name in BASELINES:
            err[name] += float(((y[:, held] - baseline(name, y, near, fit, held)) ** 2).sum())
    return min(BASELINES, key=err.get), err


def claims(y, e, x, years):
    """Per calendar month and unit: the lag in CLAIM_LAGS with the largest absolute correlation between x and y, whether it is significant, and the slope of the residual e on x at that lag, through the origin. Each 12 by units."""
    r = links.correlations(y, x, years, CLAIM_LAGS)
    best = np.abs(r).argmax(axis=0)
    claimed = np.take_along_axis(links.significant(r, len(years)), best[None], axis=0)[0]
    slope = np.zeros(best.shape)
    for m in range(12):
        res = e[:, 12 * years + m]
        for i, lag in enumerate(CLAIM_LAGS):
            d = x[12 * years + m - lag]
            slope[m, best[m] == i] = res[best[m] == i] @ d / (d @ d)
    return CLAIM_LAGS[best], claimed, slope


def term(x, years, lag, slope, shift=0):
    """slope times x at the claimed lag: units by years by 12. A shift gives each year the driver values of another of the years, circularly."""
    moved = years[(np.arange(len(years)) + shift) % len(years)]
    at = 12 * moved[None, :, None] + np.arange(12)[None, None, :] - lag.T[:, None, :]
    return slope.T[:, None, :] * x[at]


def sums(e, t, claimed, years):
    """By year, over claimed unit-months: the residual's squares, its products with the term, and the term's squares."""
    res = e[:, all_months(years)].reshape(len(e), len(years), 12)
    w = claimed.T[:, None, :]
    return np.array([np.where(w, v, 0).sum(axis=(0, 2)) for v in (res * res, res * t, t * t)])


def multiplier(y, e, x, years):
    """The one number in 0 to 1 that sizes every slope: least squared error on each block of years, with the claims picked and fitted on the others."""
    b = c = 0.0
    for f in folds(years):
        lag, claimed, slope = claims(y, e, x, np.setdiff1d(years, f))
        _, bf, cf = sums(e, term(x, f, lag, slope), claimed, f)
        b, c = b + bf.sum(), c + cf.sum()
    return float(np.clip(b / c, 0, 1)) if c > 0 else 0.0


def fit(y, near, x, split):
    """Everything from months before split: the baseline chosen, its residual on every month, the claims and the multiplier."""
    years = np.arange(1, split // 12)
    name, err = choose(y, near, years)
    months = np.arange(12, y.shape[1])
    e = np.zeros(y.shape)
    e[:, 12:] = y[:, 12:] - baseline(name, y, near, all_months(years), months)
    lag, claimed, slope = claims(y, e, x, years)
    k = multiplier(y, e, x, years)
    return {"baseline": name, "fold_error": err, "e": e, "lag": lag, "claimed": claimed, "slope": slope, "k": k}


def score(model, x, years):
    """By year on the scoring years, over claimed unit-months: the baseline's squared error, the model's, and the model's under each whole-year shift of the driver."""
    out = []
    for shift in range(len(years)):
        a, b, c = sums(model["e"], term(x, years, model["lag"], model["slope"], shift), model["claimed"], years)
        out.append(a - 2 * model["k"] * b + model["k"] ** 2 * c)
    return a, out[0], np.array(out[1:])


def skill(base, model, shifted, seed=0):
    """S = 1 - model / baseline over the years given, its 95% interval from draws of years, and S under each shift."""
    if not base.sum():
        return {"s": float("nan"), "ci": [float("nan")] * 2, "shifted": [], "beats": 0}
    draws = np.random.default_rng(seed).integers(len(base), size=(DRAWS, len(base)))
    boot = 1 - model[draws].sum(axis=1) / base[draws].sum(axis=1)
    s = 1 - model.sum() / base.sum()
    sh = 1 - shifted.sum(axis=1) / base.sum()
    return {"s": float(s), "ci": [float(v) for v in np.percentile(boot, [2.5, 97.5])], "shifted": [round(float(v), 4) for v in sh], "beats": int((s > sh).sum())}
