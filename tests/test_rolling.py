import numpy as np

from causal_atlas import rolling


def world(seed, units=120, years=11):
    """Units scattered over thirty degrees, a record with gaps, a driver of its own for each unit, and nothing between them."""
    rng = np.random.default_rng(seed)
    logp = np.cumsum(rng.normal(0.005, 0.05, (units, 12 * years)), axis=1)
    logp[rng.random(logp.shape) < 0.1] = np.nan
    x = rng.normal(size=logp.shape)
    return logp, x, rng.uniform(0, 30, units), rng.uniform(0, 30, units)


def test_a_gap_is_filled_for_three_months_and_no_longer():
    v = np.array([[1.0, np.nan, np.nan, np.nan, np.nan, 2.0]])
    assert np.array_equal(rolling.carried(v), np.array([[1.0, 1.0, 1.0, 1.0, np.nan, 2.0]]), equal_nan=True)


def test_the_change_is_unknown_where_either_end_is():
    logp = np.arange(30.0)[None, :].copy()
    logp[0, 2:8] = np.nan
    y, seen = rolling.change(logp)
    assert np.isnan(y[0, :12]).all() and np.isnan(y[0, 18:20]).all() and (y[0, 20:] == 12).all()
    assert seen.sum() == 24


def test_the_trailing_mean_knows_nothing_nearer_than_the_lead():
    rng = np.random.default_rng(1)
    v = rng.normal(size=(3, 60))
    w = v.copy()
    w[:, 38:] = 99.0
    assert np.array_equal(rolling.trail(v, 3)[:, :41], rolling.trail(w, 3)[:, :41], equal_nan=True)
    assert not np.array_equal(rolling.trail(v, 3)[:, 41], rolling.trail(w, 3)[:, 41])


def test_a_flat_driver_has_no_mean_and_no_line_left_over_the_years():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(4, 120)) + np.linspace(0, 3, 120)[None, :]
    years = np.arange(5, 10)
    f = rolling.flat(x, years)
    span = np.arange(4, 10)
    for m in range(12):
        v = f[:, 12 * span + m]
        assert np.allclose(v.mean(axis=1), 0) and np.allclose(v @ (span - span.mean()), 0)
    assert np.array_equal(f[:, :48], x[:, :48])


def test_a_year_is_forecast_from_nothing_after_it():
    logp, x, lat, lon = world(3)
    y, seen = rolling.change(logp)
    years = np.arange(7, 9)
    a = rolling.run(y, seen, x, lat, lon, years)
    later = np.random.default_rng(4)
    y2, x2, seen2 = y.copy(), x.copy(), seen.copy()
    y2[:, 108:], x2[:, 108:], seen2[:, 108:] = later.normal(size=(len(y), 24)), later.normal(size=(len(y), 24)), True
    b = rolling.run(y2, seen2, x2, lat, lon, years)
    assert a["base"][0] == b["base"][0] and a["model"][0, 0] == b["model"][0, 0] and a["baseline"][0] == b["baseline"][0]


def test_squares_are_placed_twice_and_one_scale_holds_every_unit():
    lat, lon = np.array([1.0, 4.0, 6.0]), np.array([1.0, 4.0, 6.0])
    first, second = rolling.placings(lat, lon, 5.0)
    assert first[0] == first[1] != first[2] and second[1] == second[2] != second[0]
    assert (rolling.placings(lat, lon, None)[0] == 0).all()
