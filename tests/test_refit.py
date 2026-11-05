import numpy as np

from causal_atlas import nested as n, refit as r

T = 435
SCHEDULE = [(195, 218), (219, 242)]


def panel(seed=0):
    rng = np.random.default_rng(seed)
    lat = np.repeat(np.arange(15) * 0.5 + 0.25, 10)
    lon = np.tile(np.arange(10) * 0.5 + 0.25, 15)
    drought = rng.normal(size=(150, T))
    oni = rng.normal(size=T)
    rate = np.ones((150, T))
    rate[:, 3:] = np.exp(0.8 * (drought[:, :-3] > 0.5))
    return rng.poisson(rate).astype(float), drought, oni, lat, lon


def run(y, drought, oni, lat, lon):
    refs = r.references(y, lat, lon, SCHEDULE)
    m, trees, _ = r.test_panel(refs, drought, oni)
    return m, r.reference_panel(refs), trees


def test_spans_cover_the_scored_months_once():
    got = r.spans()
    assert len(got) == 10 and got[0] == (195, 218) and got[-1] == (411, 434)
    months = [m for s, e in got for m in range(s, e + 1)]
    assert months == list(range(195, 435))


def test_a_forecast_reads_nothing_past_its_origin(monkeypatch):
    # tau 219 opens a span, so this also holds the fit to target months up to 216; tau 225 is inside the span
    monkeypatch.setattr(n, "TOLERANCE", 0.0)
    y, drought, oni, lat, lon = panel()
    m, ref, trees = run(y, drought, oni, lat, lon)
    assert all(t > 0 for t in trees), "g1 must be in the path being tested"
    for tau in (219, 225):
        later = tau - 2
        y2, d2, o2 = y.copy(), drought.copy(), oni.copy()
        y2[:, later:] += 5
        d2[:, later:] += 5
        o2[later:] += 5
        m2, ref2, _ = run(y2, d2, o2, lat, lon)
        assert np.array_equal(m[:, 195 : tau + 1], m2[:, 195 : tau + 1])
        assert np.array_equal(ref[:, 195 : tau + 1], ref2[:, 195 : tau + 1])
        assert not np.array_equal(m[:, tau + 3], m2[:, tau + 3])


def test_apply_trees_at_returns_the_same_rows():
    rng = np.random.default_rng(3)
    rows = 20000
    ref = rng.uniform(0.2, 2.0, rows)
    X = rng.normal(size=(rows, 3))
    y = rng.poisson(ref * np.exp(0.8 * (X[:, 0] > 0))).astype(float)
    fit, at = np.arange(rows) < 15000, np.arange(rows) >= 15000
    assert np.array_equal(n.apply_trees(X, y, ref, fit, 10, at=at), n.apply_trees(X, y, ref, fit, 10)[at])
    assert np.array_equal(n.apply_trees(X, y, ref, fit, 0, at=at), ref[at])
