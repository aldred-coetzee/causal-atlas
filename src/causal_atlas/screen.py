"""Tier 1, the quick screen and its search-wide gate, and tier 2 on the screen's leads. See docs/plan-phase-1-revision.md, sections 4 and 5."""
import numpy as np

from causal_atlas import detector as d, twin as w
from causal_atlas.refit import FIRST

GAPS = (0, 1, 2, 3, 4, 6, 9, 12, 18, 24)
WIDTHS = (1, 3, 6, 12)
PER_SERIES = len(GAPS) * len(WIDTHS)
BEFORE = 195
COUNT_CAP = 20
K = 5
SHIFTS = tuple(range(1, 33))
LARGEST = 10
FORMS = ("all", "largest", "pooled")


def anomaly(x):
    """Each calendar month less its mean over months before 195, per row."""
    months = np.arange(x.shape[1])
    out = x.astype(float).copy()
    for m in range(12):
        same = months % 12 == m
        out[:, same] -= x[:, same & (months < BEFORE)].astype(float).mean(axis=1, keepdims=True)
    return out


def columns(x, months):
    """Every gap and width of a 2-D input for the target months. A column stops at the forecast origin, months - LEAD - gap. The earliest training months average what exists."""
    c = np.concatenate([np.zeros((x.shape[0], 1)), np.cumsum(anomaly(x), axis=1)], axis=1)
    origin = months - d.LEAD
    for g in GAPS:
        hi = origin - g + 1
        for width in WIDTHS:
            lo = np.maximum(hi - width, 0)
            yield ((c[:, hi] - c[:, lo]) / (hi - lo)).astype(np.float32)


def statistic(u, v):
    """The three forms of T from one column's U and V per block."""
    q = np.divide(u * u, v, out=np.zeros_like(u), where=v > 0)
    total = v.sum()
    return q.sum(), np.partition(q, -LARGEST)[-LARGEST:].sum() if q.size > LARGEST else q.sum(), u.sum() ** 2 / total if total > 0 else 0.0


def table(series, y, rstar, block, months, shifts=SHIFTS):
    """T by form, column and shift, the unshifted first. All inputs move together. A global input is a plain vector."""
    e = (np.minimum(y[:, months], COUNT_CAP) - rstar).astype(np.float32)
    rstar = rstar.astype(np.float32)
    n = block.max() + 1
    by_e = np.stack([np.bincount(block, e[:, j], n) for j in range(e.shape[1])], axis=1)
    by_r = np.stack([np.bincount(block, rstar[:, j], n) for j in range(e.shape[1])], axis=1)
    out = np.zeros((len(FORMS), len(series) * PER_SERIES, len(shifts) + 1))
    for j, k in enumerate((0, *shifts)):
        c = 0
        for x in series:
            x = np.atleast_2d(x)
            for z in columns(d.circular_shift(x, k) if k else x, months):
                if x.shape[0] == 1:
                    u, v = by_e @ z[0], by_r @ (z[0] * z[0])
                else:
                    u = np.bincount(block, np.einsum("ij,ij->i", e, z), n)
                    v = np.bincount(block, np.einsum("ij,ij,ij->i", rstar, z, z), n)
                out[:, c, j] = statistic(u, v)
                c += 1
    return out


def gate(t):
    """The search-wide gate on one form's T, columns by shifts, unshifted first. Returns the leads, stepping down to K, and the top K forced. Each lead's p is 1/33. All 33 values share one scale, or the unshifted one wins on noise (results/r2-screen.md)."""
    sd = t.std(axis=1, ddof=1)
    z = np.divide(t - t.mean(axis=1, keepdims=True), sd[:, None], out=np.zeros_like(t), where=sd[:, None] > 0)
    order = np.argsort(-z[:, 0], kind="stable")
    leads = []
    left = np.ones(len(z), bool)
    for c in order[:K]:
        if z[c, 0] <= z[left, 1:].max():
            break
        leads.append(int(c))
        left[c] = False
    return leads, [int(c) for c in order[:K]], [float(z[c, 0]) for c in order[:K]]


def lead_columns(series, chosen, months):
    """The chosen columns as rows of cells by months, stacked. Global inputs are repeated over cells."""
    out = []
    for c in chosen:
        x = np.atleast_2d(series[c // PER_SERIES])
        z = list(columns(x, months))[c % PER_SERIES]
        out.append(np.tile(z, (series[0].shape[0], 1)).ravel() if x.shape[0] == 1 else z.ravel())
    return np.stack(out, axis=1)


def lead_panel(refs, series, chosen, window):
    """M on the leads, at each tree count, in the spans of the window."""
    tau = np.arange(FIRST, refs["T"])
    extra = lead_columns(series, chosen, tau)
    target, month, cells = refs["target"], refs["month"], refs["cells"]
    m = {t: np.full((cells, refs["T"]), np.nan) for t in refs["trees"]}
    for b in refs["blocks"]:
        s, e = b["span"]
        if s < window[0] or e > window[1]:
            continue
        fit, at = month <= b["last"], (month >= s) & (month <= e)
        for t, f in w.stages(np.hstack([b["X"], extra]), target, b["ref"], fit, at, b["cap"], refs["trees"]).items():
            m[t][:, s : e + 1] = f.reshape(cells, -1)
    return m
