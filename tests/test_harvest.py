import numpy as np

from causal_atlas import harvest


def world(seed, countries=40, years=50, link=0.0):
    """Countries scattered over sixty degrees, two cereals in each, a yield that grows and wanders, a monthly driver of its own for each country, and, if asked, a link from the driver in June to that year's yield."""
    rng = np.random.default_rng(seed)
    lat, lon = rng.uniform(0, 60, countries), rng.uniform(0, 60, countries)
    country, cereal = np.repeat(np.arange(countries), 2), np.tile(np.arange(2), countries)
    x = rng.normal(size=(countries, 12 * (years + 1)))
    june = x[:, 12 * (np.arange(years) + 1) + 5]
    y = 7 + 0.02 * np.arange(years)[None, :] + 0.1 * rng.normal(size=(2 * countries, years)) + link * june[country]
    official = rng.random(y.shape) < 0.9
    y[rng.random(y.shape) < 0.02] = np.nan
    return y, official & np.isfinite(y), country, cereal, x, lat, lon


def test_the_seasons_are_the_months_named():
    x = np.arange(2 * 12 * 6, dtype=float).reshape(2, -1)
    s = harvest.seasons(x, 5)
    assert s.shape == (2, 5, 6)
    assert s[0, 0].tolist() == [8, 11, 14, 17, 20, 23] and s[0, 4, 5] == 71
    assert harvest.seasons(x, 5, 4).shape == (2, 5, 4)


def test_the_line_reads_a_straight_record_exactly_and_needs_enough_years():
    y = (3 + 0.5 * np.arange(30))[None, :].copy()
    y[0, 12] = np.nan
    at, before = harvest.line(y, 20, 8)
    assert np.allclose(at[0, 20:], 3 + 0.5 * np.arange(20, 30)) and np.allclose(before[0, 20:], 3 + 0.5 * np.arange(19, 29))
    assert np.isnan(at[0, 7]) and np.isfinite(at[0, 8])


def test_the_scale_is_made_of_earlier_changes_only():
    rng = np.random.default_rng(1)
    y = np.cumsum(rng.normal(0, 0.1, (3, 40)), axis=1)
    z = y.copy()
    z[:, 25:] += rng.normal(0, 5, (3, 15))
    a, b = harvest.scale(y), harvest.scale(z)
    assert np.isnan(a[:, :10]).all() and np.isfinite(a[:, 10:]).all()
    assert np.array_equal(a[:, :26], b[:, :26], equal_nan=True) and not np.array_equal(a[:, 26:], b[:, 26:])
    assert (harvest.scale(np.ones((1, 30)))[0, 10:] == harvest.FLOOR).all()


def test_weights_are_never_below_zero():
    rng = np.random.default_rng(2)
    a = rng.normal(size=(500, 3))
    assert np.allclose(harvest.nonneg(a, a @ np.array([0.5, 0.0, 2.0])), [0.5, 0.0, 2.0], atol=1e-6)
    w = harvest.nonneg(a, a @ np.array([1.0, -1.0, 0.0]))
    assert (w >= 0).all() and w[1] == 0


def test_a_year_is_forecast_from_nothing_after_it():
    y, official, country, cereal, x, lat, lon = world(3, link=0.05)
    a = harvest.run(y, official, country, cereal, x, lat, lon, first=20, shifts=[2])
    later = np.random.default_rng(4)
    cut = 40
    y2, o2, x2 = y.copy(), official.copy(), x.copy()
    y2[:, cut:] = 7 + later.normal(size=y2[:, cut:].shape)
    o2[:, cut:] = True
    x2[:, 12 * (cut + 1) :] = later.normal(size=x2[:, 12 * (cut + 1) :].shape)
    b = harvest.run(y2, o2, country, cereal, x2, lat, lon, first=20, shifts=[2])
    before = a["years"] < cut
    assert before.sum() == 15
    for k in ("base", "weights"):
        assert np.array_equal(a[k][before], b[k][before])
    assert np.array_equal(a["model"][before, 0], b["model"][before, 0])
    assert all(np.array_equal(a["alone"][k][before], b["alone"][k][before]) for k in harvest.BASELINES)
    assert a["chosen"][: before.sum()] == b["chosen"][: before.sum()]
    assert not np.array_equal(a["model"][~before, 0], b["model"][~before, 0])


def test_a_planted_link_is_read_and_nothing_is_not():
    shifts = list(range(2, 50, 4))
    v = harvest.reading(harvest.run(*world(5, link=0.06), first=20, shifts=shifts))
    assert v["passes"] and v["model"]["s"] > 0.05 and v["model"]["beats"] == len(shifts)
    assert v["size"] == min(v["model"]["s"], v["flat"]["s"])
    for seed in (6, 7):
        v = harvest.reading(harvest.run(*world(seed), first=20, shifts=shifts))
        assert not v["passes"] and abs(v["model"]["s"]) < 0.01


def test_the_shifted_driver_is_the_same_weather_in_other_years():
    y, official, country, cereal, x, lat, lon = world(8, link=0.06)
    r = harvest.run(y, official, country, cereal, x, lat, lon, first=20, shifts=[3])
    again = harvest.run(y, official, country, cereal, np.roll(x, 36, axis=1), lat, lon, first=20, shifts=[2])
    assert np.allclose(r["model"][:, 1], again["model"][:, 0])
    assert r["model"][:, 0].sum() < r["model"][:, 1].sum()


def test_units_helped_before_are_followed_into_the_later_years():
    y, official, country, cereal, x, lat, lon = world(9, countries=60)
    linked = country < 20
    june = x[:, 12 * (np.arange(y.shape[1]) + 1) + 5]
    y = y + 0.08 * june[country] * linked[:, None]
    r = harvest.run(y, official, country, cereal, x, lat, lon, first=20, shifts=list(range(2, 50, 6)))
    k = harvest.kept(r)
    assert len(k["units"]) == round(k["ranked"] / 3) and k["years"] == [int(r["years"][len(r["years"]) // 2]), 49]
    assert linked[k["units"]].mean() > 0.8 and k["ci"][0] > 0 and k["beats"] == k["shifts"]


def test_a_gain_too_small_is_not_read_as_a_link():
    r = harvest.run(*world(5, link=0.06), first=20, shifts=[2, 9, 17])
    r["model"] = r["base"][:, None] * np.array([1 - harvest.SIZE / 2, 1.0, 1.0, 1.0])[None, :]
    r["flat"] = r["model"]
    v = harvest.reading(r)
    assert v["model"]["ci"][0] > 0 and v["model"]["beats"] == 3 and not v["passes"]
