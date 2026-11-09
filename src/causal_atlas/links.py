"""Lagged links from candidate driver series to a gridded field, by calendar month: a gate on each driver as a whole, then where and when. See results/real-enso-drought.md."""
import numpy as np
from scipy import stats

from causal_atlas.screen import gate

LAGS = tuple(range(13))
Q = 0.05
TILE = 10.0
STEP = 5.0
MIN_CELLS = 40
K = 5


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


def search(y, drivers, years, shifts, lags=LAGS, most=K):
    """T by driver and shift, the sum over lags and months of the mean squared correlation, with the gate's leads and its top five."""
    ym = by_month(y, years)
    f = np.stack([strengths(ym, x, years, shifts, lags) for x in drivers])
    t = f.sum(axis=(2, 3))
    leads, top, z = gate(t, most)
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



def tiles(lat, lon, size=TILE, step=STEP, least=MIN_CELLS):
    """Overlapping square tiles as rows of an averaging matrix, tiles by cells."""
    rows = []
    for a in np.arange(np.floor(lat.min() / step) * step, lat.max(), step):
        for o in np.arange(np.floor(lon.min() / step) * step, lon.max(), step):
            inside = (lat >= a) & (lat < a + size) & (lon >= o) & (lon < o + size)
            if inside.sum() >= least:
                rows.append(inside / inside.sum())
    return np.array(rows)


def sharpest(tm, x, years, shifts, lags=LAGS):
    """By shift (unshifted first): the largest absolute correlation between x and any tile's mean series, over tiles, lags and calendar months. For the unshifted, also where it is: tile, lag, month."""
    d = np.stack([unit(lagged(np.roll(x, 12 * s), years, lags)) for s in (0, *shifts)])
    r = np.stack([np.abs(tm[m] @ d[:, :, m].reshape(-1, len(years)).T).reshape(tm.shape[1], len(d), len(lags)) for m in range(12)])
    tile, lag, month = [int(v) for v in np.unravel_index(r[:, :, 0].transpose(1, 2, 0).argmax(), (tm.shape[1], len(lags), 12))]
    return r.max(axis=(0, 1, 3)), [tile, lag, month]


def step_down(c, most=K):
    """c: candidates by shifts, unshifted first, all on one scale. A candidate is named when its unshifted value beats every shifted value of every candidate left."""
    order = np.argsort(-c[:, 0], kind="stable")
    left = np.ones(len(c), bool)
    leads = []
    for i in order[:most]:
        if c[i, 0] <= c[left, 1:].max():
            break
        leads.append(int(i))
        left[i] = False
    return leads, [int(i) for i in order[:most]]


def both(y, drivers, years, shifts, lat, lon, lags=LAGS, most=K):
    """Two gates, a driver named by either. Broad: search(), the continent's total over all lags and months. Sharp: the largest correlation with any one tile's mean series at one lag and month."""
    broad = search(y, drivers, years, shifts, lags, most)
    tm = by_month(tiles(lat, lon) @ y, years)
    found = [sharpest(tm, x, years, shifts, lags) for x in drivers]
    e = np.array([f[0] for f in found])
    leads, top = step_down(e, most)
    return {
        "leads": broad["leads"] + [i for i in leads if i not in broad["leads"]],
        "broad": {"leads": broad["leads"], "top": broad["top"], "z": [round(float(v), 3) for v in broad["z"]]},
        "sharp": {"leads": leads, "top": top, "r": [round(float(e[i, 0]), 3) for i in top], "at": [found[i][1] for i in top], "bar": round(float(e[:, 1:].max()), 3)},
    }
