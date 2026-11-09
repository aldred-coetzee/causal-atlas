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
