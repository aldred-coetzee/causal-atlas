"""The revision's forecaster and score. See docs/plan-phase-1-revision.md, sections 1 and 2.

R and M are twins: the same learner, rows and tree count on the same bounded L, and only M sees the inputs. S is skill after each forecast is rescaled to the observed total per span and 5 degree block.
"""
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor

from causal_atlas import detector as d, nested as n
from causal_atlas.refit import FIRST, spans

TREES = (25, 50, 100)
FACTOR_LOW, FACTOR_HIGH = 0.25, 4.0
CAP_TIMES, CAP_LEAST = 2.0, 1.0
BLOWN_TIMES, BLOWN_MONTHS = 5.0, 24
FEW_EVENTS = 5


def blocks_of(lat, lon):
    """Each cell's 5 degree block, numbered from 0."""
    return np.unique(np.floor(lat / 5) * 1000 + np.floor(lon / 5), return_inverse=True)[1]


def cell_cap(y, block, last):
    """Per cell: twice the largest count its block has seen up to month last, and never below 1."""
    largest = np.zeros(block.max() + 1)
    np.maximum.at(largest, block, y[:, : last + 1].max(axis=1))
    return np.maximum(CAP_TIMES * largest, CAP_LEAST)[block]


def bounded(rate, cap):
    """The floor comes after the cap, so no forecast is zero when an event arrives. A diverged prediction becomes the cap."""
    return np.maximum(np.minimum(np.nan_to_num(rate, nan=np.inf), cap), n.FLOOR)


def blown(forecast, y, s, e):
    """A span whose forecast total is over 5 times the larger of what came before it (24 months) and what it observed (decision 0034)."""
    last = s - d.LEAD
    past = y[:, last - BLOWN_MONTHS + 1 : last + 1].sum()
    return bool(forecast[:, s : e + 1].sum() > BLOWN_TIMES * max(past, y[:, s : e + 1].sum()))


def stages(X, y, ref, fit, at, cap, trees=TREES):
    """ref times the booster at each tree count, on the rows at, bounded. One fit, read at each count."""
    model = HistGradientBoostingRegressor(max_iter=max(trees), **n.G_SETTINGS)
    model.fit(X[fit], y[fit] / ref[fit], sample_weight=ref[fit])
    out = {}
    for i, g in enumerate(model.staged_predict(X[at]), start=1):
        if i in trees:
            out[i] = bounded(ref[at] * g, cap[at])
    return out


def references(y, lat, lon, schedule=None, trees=TREES):
    """L and R for each span. L's level correction reads B's forecasts as issued for scored months already passed."""
    cells, T = y.shape
    tau = np.arange(FIRST, T)
    target = y[:, tau].ravel().astype(float)
    month = np.tile(tau, cells)
    base = d.base_features(y, lat, lon)
    where = np.repeat(np.stack([lat, lon], axis=1), len(tau), axis=0).astype(np.float32)
    block = blocks_of(lat, lon)
    issued = np.zeros((cells, T))
    schedule = schedule or spans()
    first = schedule[0][0]
    R = {t: np.full((cells, T), np.nan) for t in trees}
    out = []
    for s, e in schedule:
        last = s - d.LEAD
        fit, at = month <= last, (month >= s) & (month <= e)
        cap = np.repeat(cell_cap(y, block, last), len(tau))
        model = HistGradientBoostingRegressor(loss="poisson", early_stopping=False, random_state=0, **d.SETTINGS)
        model.fit(base[fit], target[fit].astype(np.float32))
        raw = bounded(model.predict(base).astype(float), cap)
        full = np.zeros((cells, T))
        full[:, FIRST:] = raw.reshape(cells, len(tau))
        full[:, first : s] = issued[:, first : s]
        factor = n.level_factor(y, full, lat, lon, FIRST)[:, FIRST:].ravel()
        clipped = np.clip(factor, FACTOR_LOW, FACTOR_HIGH)
        ref = bounded(raw * clipped, cap)
        issued[:, s : e + 1] = raw[at].reshape(cells, -1)
        X = np.hstack([where, np.log(ref)[:, None].astype(np.float32)])
        for t, f in stages(X, target, ref, fit, at, cap, trees).items():
            R[t][:, s : e + 1] = f.reshape(cells, -1)
        out.append(dict(span=(s, e), last=last, ref=ref, X=X, cap=cap, factor_share=float((clipped[at] != factor[at]).mean()),
                        cap_share=float((raw[at] * clipped[at] >= cap[at]).mean())))
    return dict(target=target, month=month, cells=cells, T=T, trees=trees, blocks=out, R=R)


def test_panel(refs, drought, oni):
    """M at each tree count, filled only in the scored spans. Shifts call this alone."""
    target, month, cells = refs["target"], refs["month"], refs["cells"]
    M = {t: np.full((cells, refs["T"]), np.nan) for t in refs["trees"]}
    for b in refs["blocks"]:
        s, e = b["span"]
        fit, at = month <= b["last"], (month >= s) & (month <= e)
        inputs = d.input_features(drought, oni, train_months=(FIRST, b["last"]))
        X = np.hstack([b["X"], inputs])
        for t, f in stages(X, target, b["ref"], fit, at, b["cap"], refs["trees"]).items():
            M[t][:, s : e + 1] = f.reshape(cells, -1)
    return M


def rescaled(y, forecast, block, schedule):
    """Each forecast scaled to the observed total in each span and block. The months scored, joined, as cells by months."""
    out = []
    for s, e in schedule:
        obs = np.bincount(block, y[:, s : e + 1].sum(axis=1), block.max() + 1)
        total = np.bincount(block, forecast[:, s : e + 1].sum(axis=1), block.max() + 1)
        ratio = np.divide(obs, total, out=np.zeros_like(obs, dtype=float), where=total > 0)
        out.append(forecast[:, s : e + 1] * ratio[block][:, None])
    return np.concatenate(out, axis=1)


def level_free(y, m, r, block, schedule, interval=True):
    """S with its interval, and raw skill, S per span, and the share of R's deviance from span-blocks with few events. Factors stay fixed in the interval."""
    months = np.concatenate([np.arange(s, e + 1) for s, e in schedule])
    obs = y[:, months].astype(float)
    ms, rs = rescaled(y, m, block, schedule), rescaled(y, r, block, schedule)
    by_span = [float(1 - d.deviance_by_month(y[:, s : e + 1].astype(float), rescaled(y, m, block, [(s, e)])).sum()
                     / d.deviance_by_month(y[:, s : e + 1].astype(float), rescaled(y, r, block, [(s, e)])).sum()) for s, e in schedule]
    few = 0.0
    i = 0
    for s, e in schedule:
        width = e - s + 1
        counts = np.bincount(block, obs[:, i : i + width].sum(axis=1), block.max() + 1)
        small = counts[block] < FEW_EVENTS
        few += d.deviance_by_month(obs[small][:, i : i + width], rs[small][:, i : i + width]).sum()
        i += width
    total = d.deviance_by_month(obs, rs).sum()
    return dict(S=float(1 - d.deviance_by_month(obs, ms).sum() / total), ci=list(d.block_interval(obs, ms, rs)) if interval else None,
                raw=float(d.skill(obs, m[:, months], r[:, months])), by_span=by_span, few_share=float(few / total))
