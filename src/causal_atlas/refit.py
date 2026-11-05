"""The third design's comparison, refitted as scored months pass. See results/refit-dev.md.

Each span of scored target months has its own fit of B, g0 and g1, using only what is known when the span's first forecast is issued.
"""
import time

import numpy as np

from causal_atlas import detector as d, nested as n

FIRST = 36
SCORED = (195, 434)
EVERY = 24
STOP = 48


def spans(first=SCORED[0], last=SCORED[1], every=EVERY):
    """Scored target months as (start, end) pairs, both ends included."""
    return [(s, min(s + every - 1, last)) for s in range(first, last + 1, every)]


def references(y, lat, lon, schedule=None):
    """B and g0 for each span. The level correction's predicted side uses B's forecasts as issued for scored months already passed."""
    cells, T = y.shape
    tau = np.arange(FIRST, T)
    target = y[:, tau].ravel().astype(float)
    month = np.tile(tau, cells)
    base = d.base_features(y, lat, lon)
    where = np.repeat(np.stack([lat, lon], axis=1), len(tau), axis=0).astype(np.float32)
    everything = np.ones(len(target), bool)
    issued = np.zeros((cells, T))

    def plain(ref):
        return np.hstack([where, np.log(ref)[:, None].astype(np.float32)])

    def baseline(rows, passed=None):
        raw = d.fit_predict(base, target.astype(np.float32), rows, everything).astype(float)
        full = np.zeros((cells, T))
        full[:, FIRST:] = raw.reshape(cells, len(tau))
        if passed is not None:
            full[:, SCORED[0] : passed] = issued[:, SCORED[0] : passed]
        return raw, np.maximum(raw * n.level_factor(y, full, lat, lon, FIRST)[:, FIRST:].ravel(), n.FLOOR)

    blocks = []
    for s, e in schedule or spans():
        started = time.time()
        last = s - d.LEAD
        mid = last - STOP
        fit1, stop, fit2 = month <= mid, (month > mid) & (month <= last), month <= last
        _, b1 = baseline(fit1)
        raw2, b2 = baseline(fit2, s)
        trees0 = n.choose_trees(plain(b1), target, b1, fit1, stop)
        r1 = n.apply_trees(plain(b1), target, b1, fit1, trees0)
        r2 = n.apply_trees(plain(b2), target, b2, fit2, trees0)
        at = (month >= s) & (month <= e)
        issued[:, s : e + 1] = raw2[at].reshape(cells, -1)
        blocks.append(dict(span=(s, e), mid=mid, last=last, trees0=trees0, r1=r1, r2=r2, x1=plain(r1), x2=plain(r2),
                           seconds=round(time.time() - started, 1)))
    return dict(target=target, month=month, cells=cells, T=T, blocks=blocks)


def reference_panel(refs):
    """R over all months, filled only in the scored spans."""
    out = np.full((refs["cells"], refs["T"]), np.nan)
    for b in refs["blocks"]:
        s, e = b["span"]
        at = (refs["month"] >= s) & (refs["month"] <= e)
        out[:, s : e + 1] = b["r2"][at].reshape(refs["cells"], -1)
    return out


def test_panel(refs, drought, oni):
    """M over all months, filled only in the scored spans, with each span's tree count and seconds. Shuffles call this alone."""
    target, month, cells = refs["target"], refs["month"], refs["cells"]
    out = np.full((cells, refs["T"]), np.nan)
    trees, seconds = [], []
    for b in refs["blocks"]:
        started = time.time()
        s, e = b["span"]
        fit1, stop, fit2 = month <= b["mid"], (month > b["mid"]) & (month <= b["last"]), month <= b["last"]
        at = (month >= s) & (month <= e)
        x1 = np.hstack([b["x1"], d.input_features(drought, oni, train_months=(FIRST, b["mid"]))])
        used = n.choose_trees(x1, target, b["r1"], fit1, stop)
        x2 = np.hstack([b["x2"], d.input_features(drought, oni, train_months=(FIRST, b["last"]))])
        out[:, s : e + 1] = n.apply_trees(x2, target, b["r2"], fit2, used, at=at).reshape(cells, -1)
        trees.append(used)
        seconds.append(round(time.time() - started, 1))
    return out, trees, seconds
