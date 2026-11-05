"""The third design's comparison: reference R = B times g0 (no inputs), test M = R times g1 (inputs). g1 may be no trees."""
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

G_SETTINGS = dict(loss="poisson", learning_rate=0.05, max_leaf_nodes=6, min_samples_leaf=2000, l2_regularization=100,
                  early_stopping=False, random_state=0)
MAX_TREES = 100
TOLERANCE = 0.001  # a share of the stop block's deviance at no trees
LEVEL_MONTHS = 24
LEVEL_SHRINK = 50.0
FLOOR = 1e-3


def deviance(y, mu):
    mu = np.maximum(mu, 1e-12)
    term = np.zeros_like(mu, dtype=float)
    pos = y > 0
    term[pos] = y[pos] * np.log(y[pos] / mu[pos])
    return float(2 * (term - (y - mu)).sum())


def choose_trees(X, y, ref, fit, stop):
    """The smallest tree count, from 0, whose stop-block deviance is within TOLERANCE of the lowest. Ties take the smaller."""
    model = HistGradientBoostingRegressor(max_iter=MAX_TREES, **G_SETTINGS)
    model.fit(X[fit], y[fit] / ref[fit], sample_weight=ref[fit])
    at_zero = deviance(y[stop], ref[stop])
    scores = [at_zero] + [deviance(y[stop], ref[stop] * g) for g in model.staged_predict(X[stop])]
    limit = min(scores) + TOLERANCE * at_zero
    return next(i for i, s in enumerate(scores) if s <= limit)


def apply_trees(X, y, ref, fit, trees, at=None):
    """ref itself at no trees; otherwise ref times a booster of that many trees fitted on the fit rows. at limits the rows returned."""
    at = np.ones(len(y), bool) if at is None else at
    if trees == 0:
        return ref[at].copy()
    model = HistGradientBoostingRegressor(max_iter=trees, **G_SETTINGS)
    model.fit(X[fit], y[fit] / ref[fit], sample_weight=ref[fit])
    return np.maximum(ref[at] * model.predict(X[at]), FLOOR)


def level_factor(y, forecast, lat, lon, first_target, lead=3, months=LEVEL_MONTHS, shrink=LEVEL_SHRINK):
    """Per 5 degree block and target month: (observed + shrink) / (forecast + shrink) over the months ending at target minus lead.

    y and forecast are cells by months; forecast is used from first_target on, as issued at the lead for that month.
    """
    T = y.shape[1]
    _, block = np.unique(np.floor(lat / 5) * 1000 + np.floor(lon / 5), return_inverse=True)
    n_blocks = block.max() + 1
    obs, pred = np.zeros((n_blocks, T + 1)), np.zeros((n_blocks, T + 1))
    for m in range(first_target, T):
        obs[:, m + 1] = np.bincount(block, y[:, m], n_blocks)
        pred[:, m + 1] = np.bincount(block, forecast[:, m], n_blocks)
    obs, pred = np.cumsum(obs, axis=1), np.cumsum(pred, axis=1)
    factor = np.ones((len(block), T))
    for tau in range(first_target, T):
        end = tau - lead
        assert end < tau - lead + 1, "the level ratio must not read past the forecast origin"
        if end < first_target:
            continue
        start = max(first_target, end - months + 1)
        ratio = (obs[:, end + 1] - obs[:, start] + shrink) / (pred[:, end + 1] - pred[:, start] + shrink)
        factor[:, tau] = ratio[block]
    return factor
