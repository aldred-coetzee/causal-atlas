"""Lagged links from candidate driver series to a gridded field, by calendar month: a gate on each driver as a whole, then where and when. See results/real-enso-drought.md."""
import numpy as np
from scipy import stats

from causal_atlas.screen import gate

LAGS = tuple(range(13))
Q = 0.05


def unit(a):
    """Zero mean and unit length along the last axis."""
    a = a - a.mean(axis=-1, keepdims=True)
    n = np.sqrt((a * a).sum(axis=-1, keepdims=True))
    return np.divide(a, n, out=np.zeros_like(a), where=n > 0)


def lagged(x, years, lags=LAGS):
    """x at month t - lag for target month t = 12 * year + m: lags by 12 by years."""
    return x[12 * years[None, None, :] + np.arange(12)[None, :, None] - np.asarray(lags)[:, None, None]]


def by_month(y, years):
    """The field's target months: 12 by cells by years, each row unit."""
    return unit(np.stack([y[:, 12 * years + m] for m in range(12)]).astype(np.float64))


def strengths(ym, x, years, shifts, lags=LAGS):
    """Mean squared correlation over cells, by shift (unshifted first), lag and calendar month. A shift moves x later by whole years, circularly."""
    d = np.stack([unit(lagged(np.roll(x, 12 * s), years, lags)) for s in (0, *shifts)])
    out = np.zeros(d.shape[:3])
    for m in range(12):
        r = ym[m] @ d[:, :, m].reshape(-1, len(years)).T
        out[:, :, m] = (r * r).mean(axis=0).reshape(d.shape[:2])
    return out


def search(y, drivers, years, shifts, lags=LAGS):
    """T by driver and shift, the sum over lags and months of the mean squared correlation, with the gate's leads and its top five."""
    ym = by_month(y, years)
    f = np.stack([strengths(ym, x, years, shifts, lags) for x in drivers])
    t = f.sum(axis=(2, 3))
    leads, top, z = gate(t)
    return {"leads": leads, "top": top, "z": z, "t": t, "f": f[:, 0]}


def correlations(y, x, years, lags=LAGS):
    """r by lag, calendar month and cell for one driver."""
    ym, d = by_month(y, years), unit(lagged(x, years, lags))
    return np.stack([ym[m] @ d[:, m].T for m in range(12)], axis=1).transpose(2, 1, 0)


def significant(r, n, q=Q):
    """Benjamini-Hochberg over every entry of r, each tested as a correlation on n years."""
    t = r * np.sqrt((n - 2) / np.maximum(1 - r * r, 1e-12))
    p = 2 * stats.t.sf(np.abs(t), n - 2)
    flat = np.sort(p.ravel())
    ok = flat <= q * np.arange(1, flat.size + 1) / flat.size
    return p <= (flat[ok].max() if ok.any() else -1.0)
