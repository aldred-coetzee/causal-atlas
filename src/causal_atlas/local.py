"""Does a driver that differs from cell to cell improve a forecast four or more months ahead, beyond own history. Slopes are shared by the cells of a block; the years are the unit of evidence. Rule: results/fire-drought.md."""
import numpy as np

from causal_atlas import forecast
from causal_atlas.forecast import BASELINES, CLAIM_LAGS, all_months, folds, sums

BLOCK = 5.0  # degrees
LEAST = 20  # cells in use in a block, for one of its calendar months to be tested
BACK = 5  # years: a driver is read as its departure from its own mean for that calendar month over this many years before
CUTS = (-1.5, -0.5, 0.5, 1.5)  # bands of the standardised share observed
TAUS = (0.0, 1.0, 1.5, 2.0, 2.5, 3.0)  # how sure a block's slope must be before any of it is kept: chosen from these within the fitting years


def blocks(lat, lon, size=BLOCK):
    """Each cell's block: an index into the squares of size degrees that hold any cell."""
    key = np.stack([np.floor(lat / size), np.floor(lon / size)], axis=1)
    return np.unique(key, axis=0, return_inverse=True)[1].ravel()


def baseline(name, y, near, used, fit, months):
    """forecast.baseline, with the linear one fitted on the cell-months in use only."""
    if name != "linear":
        return forecast.baseline(name, y, near, fit, months)
    rows = used[:, fit % 12].T.ravel()
    coef = np.linalg.lstsq(forecast.design(y, near, fit)[rows], y[:, fit].T.ravel().astype(np.float64)[rows], rcond=None)[0]
    return (forecast.design(y, near, months) @ coef).reshape(len(months), len(y)).T


def choose(y, near, used, years):
    """The baseline with the least squared error on the cell-months in use of the fitting years, each block of years predicted from a fit on the others."""
    err = dict.fromkeys(BASELINES, 0.0)
    for f in folds(years):
        fit, held = all_months(np.setdiff1d(years, f)), all_months(f)
        for name in BASELINES:
            err[name] += float((((y[:, held] - baseline(name, y, near, used, fit, held)) ** 2) * used[:, held % 12]).sum())
    return min(BASELINES, key=err.get), err


def residual(name, y, near, used, years):
    """What a baseline fitted on the years given leaves, on every month after the first year."""
    e = np.zeros(y.shape)
    e[:, 12:] = y[:, 12:] - baseline(name, y, near, used, all_months(years), np.arange(12, y.shape[1]))
    return e


def departure(x, first, back=BACK):
    """x from month first on, each value less the cell's own mean for the same calendar month over the back years before it, on as many of those as the record holds. A slow drift in the driver is then not in what is tested, and nothing later than a value is used to make it."""
    months = np.arange(first, x.shape[1])
    total, n = np.zeros((len(x), len(months))), np.zeros(len(months))
    for k in range(1, back + 1):
        ok = months - 12 * k >= 0
        total[:, ok] += x[:, months[ok] - 12 * k]
        n += ok
    return x[:, first:] - total / np.maximum(n, 1)


def evidence(e, x, used, group, years, season):
    """Per calendar month and block: the lag in CLAIM_LAGS at which the driver and the residual move together most surely, how surely (a t on the years), the slope of residual on driver at that lag through the origin, and whether the block has enough cells in use that month to be tested. Each 12 by blocks.

    The evidence at one lag, month and block is one number a year: the sum over the block's cells in use of driver times residual. Its mean over the years is set against its spread over the years, so cells that move together within a year count once. With season, a block has one lag and one slope, from all its tested months together."""
    n = group.max() + 1
    to = np.zeros((n, len(group)))
    to[group, np.arange(len(group))] = 1
    a = np.zeros((len(CLAIM_LAGS), 12, n, len(years)))
    b = np.zeros(a.shape[:3])
    for m in range(12):
        at = 12 * years + m
        for i, lag in enumerate(CLAIM_LAGS):
            d = x[:, at - lag] * used[:, m, None]
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
    return CLAIM_LAGS[best], pick(t), slope, tested


def weight(t, tau):
    """How much of a slope is kept, from how sure it is: nothing below tau, nearly all well above it."""
    return np.maximum(0, 1 - (tau / np.maximum(np.abs(t), 1e-12)) ** 2)


def spread(lag, t, slope, tested, tau, used, group):
    """A block's lag, claim and kept slope given to each of its cells, a claim only on the cell's months in use. Each 12 by cells."""
    w = np.where(tested, weight(t, tau), 0)
    return lag[:, group], (w > 0)[:, group] & used.T, (slope * w)[:, group]


def term(x, years, lag, slope, shift=0):
    """slope times each cell's own driver at the claimed lag: cells by years by 12. A shift gives each year the driver values of another of the years, circularly, the whole field together."""
    moved = years[(np.arange(len(years)) + shift) % len(years)]
    at = 12 * moved[None, :, None] + np.arange(12)[None, None, :] - lag.T[:, None, :]
    return slope.T[:, None, :] * np.take_along_axis(x, at.reshape(len(x), -1), axis=1).reshape(at.shape)


def tune(e, x, used, group, years):
    """Three things chosen together within the fitting years: whether a block's slope is by calendar month or one for its season, tau, and the one number in 0 to 1 that sizes every kept slope. The choice with the least squared error on each block of years, with the evidence taken from the others. A multiplier of 0 means nothing held up within the fitting years, and the model then claims nothing."""
    b, c = np.zeros((2, len(TAUS))), np.zeros((2, len(TAUS)))
    for f in folds(years):
        for j in (0, 1):
            found = evidence(e, x, used, group, np.setdiff1d(years, f), bool(j))
            for i, tau in enumerate(TAUS):
                lag, claimed, slope = spread(*found, tau, used, group)
                _, bf, cf = sums(e, term(x, f, lag, slope), claimed, f)
                b[j, i], c[j, i] = b[j, i] + bf.sum(), c[j, i] + cf.sum()
    k = np.clip(np.divide(b, c, out=np.zeros(b.shape), where=c > 0), 0, 1)
    gain = 2 * k * b - k * k * c
    j, i = np.unravel_index(gain.argmax(), gain.shape)
    return bool(j), TAUS[i], float(k[j, i]), gain.round(1).tolist()


def fit(y, near, x, used, group, years):
    """Everything from the fitting years: the baseline chosen, its residual on every month, what is claimed, and the two numbers tuned."""
    name, err = choose(y, near, used, years)
    e = residual(name, y, near, used, years)
    season, tau, k, gain = tune(e, x, used, group, years)
    found = evidence(e, x, used, group, years, season)
    lag, claimed, slope = spread(*found, tau, used, group)
    if k == 0:
        claimed = np.zeros_like(claimed)
    kept = int((found[3] & (weight(found[1], tau) > 0)).sum()) if k else 0  # calendar months of blocks with a slope kept
    return {"baseline": name, "fold_error": err, "e": e, "lag": lag, "claimed": claimed, "slope": slope, "k": k, "season": season, "tau": tau, "gain": gain, "blocks": kept}


def level(d):
    """A term less its own straight line across its years, cell and calendar month by cell and calendar month: what is left differs from year to year and neither rises nor falls over them."""
    t = (np.arange(d.shape[1]) - (d.shape[1] - 1) / 2)[None, :, None]
    return d - d.mean(axis=1, keepdims=True) - t * (d * t).sum(axis=1, keepdims=True) / (t * t).sum()


def score(model, x, years, flat=False):
    """By year on the scoring years, over claimed cell-months: the baseline's squared error, the model's, and the model's under each whole-year shift of the driver field. With flat, every term, shifted or not, is first taken less its own straight line across the scoring years (level), so a rise or fall shared by driver and outcome over those years earns nothing."""
    out = []
    for shift in range(len(years)):
        d = term(x, years, model["lag"], model["slope"], shift)
        a, b, c = sums(model["e"], level(d) if flat else d, model["claimed"], years)
        out.append(a - 2 * model["k"] * b + model["k"] ** 2 * c)
    return a, out[0], np.array(out[1:])


def alone(y, near, used, claimed, fit_years, years):
    """By baseline: its squared error by year on the claimed cell-months of the years given."""
    return {name: sums(residual(name, y, near, used, fit_years), np.zeros((len(y), len(years), 12)), claimed, years)[0] for name in BASELINES}


def adjusted(y, s, used, group, years):
    """y less what the share observed in the same month explains of it, whatever the shape: the mean of y, in the fitting years, over the block's cell-months in use of that calendar month that fall in the same band of the standardised share observed. A band's mean is pulled toward zero when few cell-months are in it."""
    n = 5 * (group.max() + 1)
    key = 5 * group[:, None] + np.digitize(s, CUTS)
    out = y.astype(np.float64).copy()
    for m in range(12):
        t, w = 12 * years + m, used[:, m]
        at = key[:, t][w].ravel()
        mean = np.bincount(at, y[:, t][w].ravel(), n) / (np.bincount(at, minlength=n) + 5)
        out[:, m::12] -= mean[key[:, m::12]] * w[:, None]
    return out
