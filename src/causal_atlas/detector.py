"""The machinery step 1b tests and 1d will use: baseline B, model M1, skill, interval, shuffles."""
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.ensemble import HistGradientBoostingRegressor

LEAD = 3
TRAIN = (36, 338)  # target months by index from 1989-01, both ends included
VALID = (339, 386)
HELD = (387, 434)
FIRST_YEARS = 432  # months in whole years; the last 3 months of the series are a partial year
SHIFTS = 32
SETTINGS = dict(learning_rate=0.05, max_leaf_nodes=15, max_iter=100, l2_regularization=100, min_samples_leaf=200)


def _windows(x, ts, widths):
    """Sums of x (cells by months) over each width ending at each month in ts."""
    c = np.concatenate([np.zeros((x.shape[0], 1)), np.cumsum(x, axis=1)], axis=1)
    return [c[:, ts + 1] - c[:, np.maximum(ts + 1 - w, 0)] for w in widths]


def neighbours(lat, lon):
    """Sparse cell-by-cell matrix with a 1 for each of the 8 surrounding cells on the 0.5 degree grid."""
    where = {(int(np.floor(a * 2)), int(np.floor(o * 2))): i for i, (a, o) in enumerate(zip(lat, lon))}
    rows, cols = [], []
    for (a, o), i in where.items():
        for da in (-1, 0, 1):
            for do in (-1, 0, 1):
                j = where.get((a + da, o + do))
                if (da or do) and j is not None:
                    rows.append(i)
                    cols.append(j)
    n = len(lat)
    return csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))


def _targets(lead):
    tau = np.arange(TRAIN[0], HELD[1] + 1)
    return tau, tau - lead


def base_features(y, lat, lon, lead=LEAD):
    """Baseline B's features, one row per cell and target month. Nothing later than t = target - lead."""
    tau, ts = _targets(lead)
    n = y.shape[0]
    y = y.astype(float)
    cols = [y[:, ts], y[:, ts - 1], y[:, ts - 2]]
    cols += _windows(y, ts, (3, 6, 12, 36))
    last = np.full(n, -1)
    since = np.empty_like(y)
    for t in range(y.shape[1]):
        last = np.where(y[:, t] > 0, t, last)
        since[:, t] = t - last
    cols.append(since[:, ts])
    cols.append(_windows(y, ts, (ts.max() + 1,))[0] / (ts + 1))
    cols.append(np.tile(tau % 12, (n, 1)))
    cols.append(np.tile(lat[:, None], (1, len(ts))))
    cols.append(np.tile(lon[:, None], (1, len(ts))))
    cols += _windows(neighbours(lat, lon) @ y, ts, (1, 3, 12))
    return np.stack([c.ravel() for c in cols], axis=1).astype(np.float32)


def input_features(drought, oni, lead=LEAD, train_months=TRAIN):
    """M1's inputs: the cell's drought anomaly over 1, 3, 6, 12 months to t, and ONI at t-1 and its means."""
    _, ts = _targets(lead)
    n = drought.shape[0]
    anom = drought.astype(float).copy()
    train = np.arange(train_months[0], train_months[1] + 1)
    for m in range(12):
        where = train[train % 12 == m]
        anom[:, np.arange(drought.shape[1]) % 12 == m] -= anom[:, where].mean(axis=1, keepdims=True)
    cols = [w / k for w, k in zip(_windows(anom, ts, (1, 3, 6, 12)), (1, 3, 6, 12))]
    o = oni.astype(float)[None, :]
    cols.append(np.tile(o[:, ts - 1], (n, 1)))
    cols += [np.tile(w / k, (n, 1)) for w, k in zip(_windows(o, ts - 1, (3, 6, 12)), (3, 6, 12))]
    return np.stack([c.ravel() for c in cols], axis=1).astype(np.float32)


def naive_b0(y, lead=LEAD):
    """B0: same calendar month over the last 3 years, blended equally with the last-12-month rate."""
    tau, ts = _targets(lead)
    y = y.astype(float)
    same = np.mean([y[:, tau - 12 * k] for k in (1, 2, 3)], axis=0)
    return 0.5 * same + 0.5 * _windows(y, ts, (12,))[0] / 12


def fit_predict(X, target, fit_rows, predict_rows, settings=SETTINGS, threads_seed=0):
    """Poisson gradient boosting with a fixed seed; returns predictions for predict_rows."""
    model = HistGradientBoostingRegressor(
        loss="poisson", early_stopping=False, random_state=threads_seed, **settings
    )
    model.fit(X[fit_rows], target[fit_rows])
    pred = model.predict(X[predict_rows])
    if not np.isfinite(pred).all() or pred.max() > 10 * target[fit_rows].max():
        raise FloatingPointError("boosting diverged: predictions far above any training count")
    return np.maximum(pred, 1e-12)


def deviance_by_month(obs, rate):
    """Summed Poisson deviance per month, for cells-by-months arrays."""
    rate = np.maximum(rate, 1e-12)
    term = np.zeros_like(rate, dtype=float)
    pos = obs > 0
    term[pos] = obs[pos] * np.log(obs[pos] / rate[pos])
    return 2 * (term - (obs - rate)).sum(axis=0)


def skill(obs, model, base):
    return 1 - deviance_by_month(obs, model).sum() / deviance_by_month(obs, base).sum()


def block_interval(obs, model, base, draws=10000, block=6, seed=0, level=0.95):
    """Moving-block bootstrap of skill over months, whole panel per month."""
    dm, db = deviance_by_month(obs, model), deviance_by_month(obs, base)
    months = len(dm)
    rng = np.random.default_rng(seed)
    starts = rng.integers(0, months - block + 1, size=(draws, months // block))
    picks = (starts[:, :, None] + np.arange(block)).reshape(draws, -1)
    boot = 1 - dm[picks].sum(axis=1) / db[picks].sum(axis=1)
    tail = (1 - level) / 2
    return float(np.quantile(boot, tail)), float(np.quantile(boot, 1 - tail))


def circular_shift(x, years):
    """Move a series by whole years along its last axis, keeping calendar month."""
    i = np.arange(x.shape[-1]) - 12 * years
    i[i < 0] += FIRST_YEARS
    return x[..., i]


def year_permutation(x, seed):
    """Reorder whole years along the last axis, keeping calendar month. The partial year follows the last."""
    order = np.random.default_rng(seed).permutation(FIRST_YEARS // 12)
    t = np.arange(x.shape[-1])
    year = np.minimum(t // 12, len(order) - 1)
    return x[..., order[year] * 12 + t % 12]


def verdict(observed, ci_low, shuffled, margin=0.02, allowed_above=0, vanish=0.01):
    """The three criteria for one replicate under one shuffle scheme."""
    shuffled = np.asarray(shuffled)
    first = bool(observed >= margin and ci_low > 0)
    second = bool((shuffled >= observed).sum() <= allowed_above)
    third = bool(abs(np.median(shuffled)) < vanish)
    return dict(first=first, second=second, third=third, all=first and second and third)
