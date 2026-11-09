import numpy as np

from causal_atlas import confirm, decoy


def world(seed, link):
    rng = np.random.default_rng(seed)
    lat, lon = [v.ravel() for v in np.meshgrid(np.arange(0, 6, 0.5), np.arange(10, 16, 0.5), indexing="ij")]
    months = 600
    x = decoy.cycle(months, 4, 0.9, rng)
    y = rng.normal(size=(len(lat), months))
    for t in range(1, months):
        y[:, t] += 0.5 * y[:, t - 1]
    t = np.arange(12, months)
    t = t[np.isin(t % 12, (0, 1, 2))]
    y[np.ix_(np.where(lat < 3)[0], t)] += link * x[t - 6]
    return y.astype(np.float32), x, lat, lon


def test_neighbours_are_the_eight_around():
    _, _, lat, lon = world(7911, 0)
    nb = confirm.neighbours(lat, lon)
    inner = (lat == 2.5) & (lon == 12.5)
    got = nb[inner][0]
    assert (got >= 0).all() and np.abs(lat[got] - 2.5).max() == 0.5 and np.abs(lon[got] - 12.5).max() == 0.5
    assert (nb[(lat == 0) & (lon == 10)][0] >= 0).sum() == 3


def test_a_planted_link_beats_the_baseline_out_of_time():
    y, x, lat, lon = world(7912, 0.8)
    out, parts = confirm.run(y, x, lat, lon, 360)
    assert parts["claimed"][lat < 3][:, :3].mean() > 0.7
    assert parts["claimed"][lat >= 3].mean() < 0.02
    assert out["ci_claimed"][0] > 0 and out["beats_shifted"] == len(out["shifted"]) == 19


def test_no_link_does_not_pass():
    y, x, lat, lon = world(7913, 0.0)
    out, _ = confirm.run(y, x, lat, lon, 360)
    assert out["claimed_cell_months"] == 0 or not (out["ci_claimed"][0] > 0 and out["beats_shifted"] == len(out["shifted"]))
