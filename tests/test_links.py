import numpy as np

from causal_atlas import decoy, links


def world(seed, cells=300, years=40, share=0.0, lag=5, months=(0, 1, 2), where=slice(0, 100)):
    rng = np.random.default_rng(seed)
    n = 12 * years
    x = decoy.make(seed, n, decoy.ar1(n, 0.9, rng), count=8)
    y = rng.standard_normal((cells, n))
    if share:
        t = np.arange(12, n)
        t = t[np.isin(t % 12, months)]
        y[where, t] += np.sqrt(share / (1 - share)) * x[0][t - lag]
    return y, x, np.arange(1, years)


def test_planted_link_is_named_with_where_and_when():
    y, x, years = world(1, share=0.3)
    out = links.search(y, x, years, range(1, len(years)))
    assert out["leads"] == [0]
    r = links.correlations(y, x[0], years)
    sig = links.significant(r, len(years))
    assert sig[5, :3, :100].mean() > 0.7
    assert sig[:, :, 100:].mean() < 0.01
    assert (r[5, :3, :100] > 0).mean() > 0.95


def test_no_link_names_nothing_at_about_the_stated_rate():
    named = sum(bool(links.search(*world(s)[:2], world(s)[2], range(1, 39))["leads"]) for s in range(100, 130))
    assert named <= 3


def test_lagged_reads_the_right_months():
    x = np.arange(120.0)
    d = links.lagged(x, np.arange(1, 10))
    assert d[3, 4, 0] == 12 + 4 - 3 and d[0, 11, 8] == 119


def test_both_names_a_small_planted_link_and_nothing_without_one():
    lat, lon = [v.ravel() for v in np.meshgrid(np.arange(-20, 20, 1.0), np.arange(0, 30, 1.0), indexing="ij")]
    years, shifts = np.arange(1, 40), range(1, 40)
    named = 0
    for seed in range(7921, 7931):
        rng = np.random.default_rng(seed)
        d = decoy.make(seed, 480, rng.normal(size=480), 8)
        y = rng.normal(size=(len(lat), 480))
        named += bool(links.both(y, list(d), years, shifts, lat, lon)["leads"])
        t = np.arange(12, 480)
        t = t[t % 12 == 4]
        small = (lat < -10) & (lon < 10)
        y[np.ix_(np.where(small)[0], t)] += 0.7 * d[3][t - 2]
        out = links.both(y, list(d), years, shifts, lat, lon)
        assert 3 in out["sharp"]["leads"] and out["sharp"]["at"][0][1:] == [2, 4], (seed, out)
    assert named <= 2


def test_step_down_names_only_what_beats_every_shift_left():
    c = np.array([[9.0, 1, 2], [5.0, 1, 6], [7.0, 3, 1]])
    assert links.step_down(c) == ([0, 2], [0, 2, 1])
    assert links.step_down(np.array([[9.0, 1, 2], [5.0, 1, 8], [7.0, 3, 1]])) == ([0], [0, 2, 1])


def test_a_copy_one_year_off_is_the_series_itself_at_the_far_lag():
    y, x, years = world(3, share=0.3, lag=0)
    s = links.strengths(links.by_month(y, years), x[0], years, (1, len(years)))  # one year later, one year earlier
    assert np.allclose(s[1, 0], s[0, 12]) and np.allclose(s[2, 12], s[0, 0])
