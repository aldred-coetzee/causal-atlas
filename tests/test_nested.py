import numpy as np

from causal_atlas import nested as n


def panel(seed=0, cells=40, T=120):
    rng = np.random.default_rng(seed)
    lat = np.repeat(np.arange(8) * 5 + 2.5, 5)[:cells]
    lon = np.tile(np.arange(5) * 5 + 2.5, 8)[:cells]
    return rng.poisson(2.0, (cells, T)).astype(float), rng.uniform(1, 3, (cells, T)), lat, lon


def test_level_reads_nothing_past_target_minus_lead():
    y, f, lat, lon = panel()
    tau = 80
    a = n.level_factor(y, f, lat, lon, 36)
    later_y, later_f = y.copy(), f.copy()
    later_y[:, tau - 3 + 1 :] += 50
    later_f[:, tau - 3 + 1 :] += 50
    b = n.level_factor(later_y, later_f, lat, lon, 36)
    assert np.array_equal(a[:, : tau + 1], b[:, : tau + 1])
    assert not np.array_equal(a[:, tau + 1], b[:, tau + 1])


def test_level_uses_the_stated_window():
    y, f, lat, lon = panel()
    tau = 80
    earlier = y.copy()
    earlier[:, : tau - 3 - n.LEVEL_MONTHS + 1] += 50
    assert np.array_equal(n.level_factor(y, f, lat, lon, 36)[:, tau], n.level_factor(earlier, f, lat, lon, 36)[:, tau])


def test_no_trees_on_noise_gives_the_reference_itself():
    rng = np.random.default_rng(1)
    rows = 60000
    ref = rng.uniform(0.2, 2.0, rows)
    y = rng.poisson(ref).astype(float)
    X = rng.normal(size=(rows, 3))
    fit = np.arange(rows) < 40000
    trees = n.choose_trees(X, y, ref, fit, ~fit)
    assert trees == 0
    assert np.array_equal(n.apply_trees(X, y, ref, fit, trees), ref)


def test_a_real_signal_gets_trees():
    rng = np.random.default_rng(2)
    rows = 60000
    ref = rng.uniform(0.2, 2.0, rows)
    X = rng.normal(size=(rows, 3))
    y = rng.poisson(ref * np.exp(0.8 * (X[:, 0] > 0))).astype(float)
    fit = np.arange(rows) < 40000
    assert n.choose_trees(X, y, ref, fit, ~fit) > 0
