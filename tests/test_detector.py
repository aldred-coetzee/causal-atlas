import numpy as np

from causal_atlas import detector as d


def small(seed=0, cells=30, T=435):
    rng = np.random.default_rng(seed)
    lat = np.repeat(np.arange(6) * 0.5 + 0.25, 5)[:cells]
    lon = np.tile(np.arange(5) * 0.5 + 0.25, 6)[:cells]
    return rng.poisson(0.2, (cells, T)), rng.normal(size=(cells, T)), rng.normal(size=T), lat, lon


def row(cells, tau_index, cell):
    return cell * (d.HELD[1] - d.TRAIN[0] + 1) + tau_index


def test_features_ignore_everything_after_t():
    y, dr, oni, lat, lon = small()
    tau = 200
    t = tau - d.LEAD
    r = row(len(lat), tau - d.TRAIN[0], 7)
    a, a2 = d.base_features(y, lat, lon)[r], d.input_features(dr, oni)[r]
    y2, dr2, oni2 = y.copy(), dr.copy(), oni.copy()
    y2[:, t + 1 :] = 99
    dr2[:, t + 1 :] = 99
    dr2[:, d.TRAIN[0] :] = dr[:, d.TRAIN[0] :]  # anomaly means use training months, by design
    dr2[:, t + 1 :] = dr[:, t + 1 :]
    oni2[t:] = 99
    assert np.array_equal(d.base_features(y2, lat, lon)[r], a)
    assert np.array_equal(d.input_features(dr2, oni2)[r], a2)


def test_lag_columns_and_since():
    y = np.zeros((30, 435), dtype=int)
    y[7, 197] = 5
    _, _, _, lat, lon = small()
    x = d.base_features(y, lat, lon)[row(30, 200 - d.TRAIN[0], 7)]
    assert x[0] == 5 and x[1] == 0 and x[3] == 5 and x[7] == 0
    x = d.base_features(y, lat, lon)[row(30, 203 - d.TRAIN[0], 7)]
    assert x[0] == 0 and x[1] == 0 and x[7] == 3


def test_neighbours_count():
    _, _, _, lat, lon = small()
    a = d.neighbours(lat, lon)
    assert a.shape == (30, 30)
    assert a[12].sum() == 8  # an interior cell
    assert a[0].sum() == 3  # a corner


def test_shuffles_keep_calendar_month():
    x = np.arange(435) % 12
    for k in (1, 7, 32):
        assert np.array_equal(d.circular_shift(x, k), x)
    assert np.array_equal(d.year_permutation(x, 3), x)


def test_shift_moves_values_and_is_a_permutation_on_whole_years():
    x = np.arange(435)
    s = d.circular_shift(x, 2)
    assert s[24] == 0 and s[0] == 408
    assert sorted(s[:432]) == list(range(432))


def test_skill_and_interval():
    rng = np.random.default_rng(0)
    rate = rng.gamma(0.5, 0.4, (200, 48))
    obs = rng.poisson(rate)
    assert abs(d.skill(obs, rate, rate)) < 1e-12
    flat = np.full_like(rate, rate.mean())
    s = d.skill(obs, rate, flat)
    lo, hi = d.block_interval(obs, rate, flat, draws=2000)
    assert s > 0.1 and lo < s < hi and lo > 0


def test_verdict():
    assert d.verdict(0.05, 0.01, [0.0, 0.001, 0.002])["all"]
    assert not d.verdict(0.05, -0.01, [0.0])["all"]
    assert not d.verdict(0.05, 0.01, [0.0, 0.06])["all"]
    assert not d.verdict(0.05, 0.01, [0.02, 0.03, 0.04])["all"]
    assert not d.verdict(0.019, 0.01, [0.0])["all"]


def test_fit_stays_stable_on_a_rare_huge_count():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(50000, 3)).astype(np.float32)
    y = np.zeros(50000, dtype=np.float32)
    y[np.argsort(X[:, 0])[-20:]] = 500
    rows = np.ones(50000, dtype=bool)
    p = d.fit_predict(X, y, rows, rows)
    assert p.max() < 5000


def test_anomaly_months_can_stop_before_the_scored_window():
    y, drought, oni = small()[:3]
    later = drought.astype(float).copy()
    later[:, 195:] += 5.0
    rows = d.input_features(drought, oni, train_months=(36, 194)).reshape(drought.shape[0], 434 - 36 + 1, 8)
    moved = d.input_features(later, oni, train_months=(36, 194)).reshape(drought.shape[0], 434 - 36 + 1, 8)
    assert np.array_equal(rows[:, : 194 - 36 + 1], moved[:, : 194 - 36 + 1])
    usual = d.input_features(later, oni).reshape(drought.shape[0], 434 - 36 + 1, 8)
    assert not np.array_equal(rows[:, : 194 - 36 + 1], usual[:, : 194 - 36 + 1])
