import numpy as np

from causal_atlas import decoy, forecast


def world(seed, link, level=0.0):
    rng = np.random.default_rng(seed)
    units, months = 60, 720
    x = decoy.cycle(months, 4, 0.9, rng)
    y = rng.normal(size=(units, months))
    for t in range(1, months):
        y[:, t] += 0.5 * y[:, t - 1]
    y += level * np.cumsum(rng.normal(size=(units, months // 60)), axis=1).repeat(60, axis=1)
    t = np.arange(12, months)
    t = t[np.isin(t % 12, (0, 1, 2))]
    y[np.ix_(np.arange(30), t)] += link * x[t - 6]
    return y, np.repeat(y.mean(axis=0, keepdims=True), units, axis=0), x


def run(y, near, x, split=480):
    model = forecast.fit(y, near, x, split)
    years = np.arange(split // 12, y.shape[1] // 12)
    return model, forecast.skill(*forecast.score(model, x, years))


def test_trail_is_the_mean_of_the_months_ending_three_back():
    y = np.arange(20.0)[None, :]
    assert forecast.trail(y, 4)[0, 10] == np.mean([4, 5, 6, 7])
    assert forecast.trail(y, 60)[0, 5] == np.mean([0, 1, 2])
    assert forecast.trail(y, 60)[0, 0] == 0


def test_a_planted_link_beats_the_baseline_out_of_time():
    model, out = run(*world(7921, 0.8))
    assert model["claimed"][:3, :30].mean() > 0.7 and model["claimed"][:, 30:].sum() < 0.15 * model["claimed"].sum()
    assert (model["lag"][:3, :30][model["claimed"][:3, :30]] == 6).mean() > 0.9
    assert 0 < model["k"] <= 1
    assert out["ci"][0] > 0 and out["beats"] == len(out["shifted"]) == 19


def test_no_link_does_not_pass():
    model, out = run(*world(7922, 0.0))
    assert not model["claimed"].any() or not (out["ci"][0] > 0 and out["beats"] == len(out["shifted"]))


def test_a_unit_whose_level_wanders_is_not_given_the_zero_baseline():
    y, near, x = world(7923, 0.0, level=1.0)
    name, err = forecast.choose(y, near, np.arange(1, 40))
    assert name != "zero" and err["level"] < err["zero"]


def test_the_multiplier_is_fitted_only_on_the_years_before_the_split():
    y, near, x = world(7924, 0.8)
    late = y.copy()
    late[:, 480:] = np.random.default_rng(1).normal(size=late[:, 480:].shape)
    a, b = forecast.fit(y, near, x, 480), forecast.fit(late, np.repeat(late.mean(axis=0, keepdims=True), len(late), axis=0), x, 480)
    near_same = np.allclose(a["slope"], b["slope"]) and (a["claimed"] == b["claimed"]).all()
    assert near_same and a["k"] == b["k"] and a["baseline"] == b["baseline"]


def test_the_model_error_with_no_shift_is_the_direct_sum():
    y, near, x = world(7925, 0.8)
    model = forecast.fit(y, near, x, 480)
    years = np.arange(40, 60)
    base, got, _ = forecast.score(model, x, years)
    t = model["k"] * forecast.term(x, years, model["lag"], model["slope"])
    res = model["e"][:, forecast.all_months(years)].reshape(len(y), len(years), 12)
    want = np.where(model["claimed"].T[:, None, :], (res - t) ** 2, 0).sum(axis=(0, 2))
    assert np.allclose(got, want) and np.allclose(base, np.where(model["claimed"].T[:, None, :], res**2, 0).sum(axis=(0, 2)))


def second(seed, link):
    """world() with a second driver planted in the other half of the units, in other months, at lag 5."""
    y, _, x = world(seed, 0.8)
    z = decoy.cycle(y.shape[1], 3, 0.9, np.random.default_rng(seed + 1))
    t = np.arange(12, y.shape[1])
    t = t[np.isin(t % 12, (6, 7, 8))]
    y[np.ix_(np.arange(30, 60), t)] += link * z[t - 5]
    return y, np.repeat(y.mean(axis=0, keepdims=True), len(y), axis=0), x, z


def beyond(y, near, x, z, split=480):
    first = forecast.fit(y, near, x, split)
    years = np.arange(split // 12, y.shape[1] // 12)
    more = forecast.after(forecast.residual(first, x, np.arange(1, y.shape[1] // 12)), z, split)
    return first, more, forecast.skill(*forecast.score(more, z, years))


def test_the_residual_is_the_baseline_residual_less_the_sized_term_where_claimed():
    y, near, x = world(7926, 0.8)
    model = forecast.fit(y, near, x, 480)
    years = np.arange(40, 60)
    left = forecast.residual(model, x, np.arange(1, 60))
    _, got, _ = forecast.score(model, x, years)
    res = left[:, forecast.all_months(years)].reshape(len(y), len(years), 12)
    assert np.allclose(np.where(model["claimed"].T[:, None, :], res**2, 0).sum(axis=(0, 2)), got)
    assert np.array_equal(left[:, :12], model["e"][:, :12]) and np.array_equal(np.where(model["claimed"].T[:, None, :], 0, res), np.where(model["claimed"].T[:, None, :], 0, model["e"][:, forecast.all_months(years)].reshape(res.shape)))


def test_a_second_planted_driver_adds_beyond_the_first_and_is_claimed_where_it_was_planted():
    first, more, out = beyond(*second(7927, 0.8))
    assert more["claimed"][6:9, 30:].mean() > 0.7 and more["claimed"][:, :30].sum() < 0.15 * more["claimed"].sum()
    assert (more["lag"][6:9, 30:][more["claimed"][6:9, 30:]] == 5).mean() > 0.9
    assert out["ci"][0] > 0 and out["beats"] == len(out["shifted"]) == 19


def test_the_first_driver_again_adds_nothing_beyond_itself():
    y, near, x, _ = second(7928, 0.0)
    _, more, out = beyond(y, near, x, x)
    assert not more["claimed"].any() or not (out["ci"][0] > 0 and out["beats"] == len(out["shifted"]))


def test_a_wider_level_gives_a_wider_interval():
    base, got, shifted = forecast.score(forecast.fit(*world(7929, 0.8), 480), world(7929, 0.8)[2], np.arange(40, 60))
    a, b = forecast.skill(base, got, shifted), forecast.skill(base, got, shifted, level=0.995, draws=20000)
    assert b["ci"][0] <= a["ci"][0] and b["ci"][1] >= a["ci"][1] and a["s"] == b["s"]
