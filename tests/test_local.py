import numpy as np

from causal_atlas import forecast, local

FIT = np.array([y for y in range(1, 22) if y != 12])
SCORED = np.arange(22, 37)
PER = 40  # cells in a block


def world(seed, link, blocks=6):
    """Blocks of cells five degrees apart. The driver is partly shared within a block; the outcome has a shock each year shared by all. In the first block, in three calendar months, the outcome follows the cell's own driver of seven months before."""
    rng = np.random.default_rng(seed)
    cells, months = PER * blocks, 12 * 37
    group = np.repeat(np.arange(blocks), PER)
    x = np.sqrt(0.5) * rng.normal(size=(blocks, months))[group] + np.sqrt(0.5) * rng.normal(size=(cells, months))
    y = np.sqrt(0.7) * rng.normal(size=(cells, months)) + np.sqrt(0.3) * rng.normal(size=months // 12).repeat(12)[None, :]
    t = np.arange(12, months)
    t = t[np.isin(t % 12, (5, 6, 7))]
    y[np.ix_(np.arange(PER), t)] += link * x[np.ix_(np.arange(PER), t - 7)]
    lat, lon = rng.uniform(0, 5, cells), 5.0 * group + rng.uniform(0, 5, cells)
    return y, np.repeat(y.mean(axis=0, keepdims=True), cells, axis=0), x, np.ones((cells, 12), bool), local.blocks(lat, lon)


def run(y, near, x, used, group):
    model = local.fit(y, near, x, used, group, FIT)
    return model, forecast.skill(*local.score(model, x, SCORED))


def test_cells_of_one_square_share_a_block():
    g = local.blocks(np.array([1.0, 4.9, 5.1, 1.0]), np.array([1.0, 4.9, 1.0, 11.0]))
    assert g[0] == g[1] and len({g[0], g[2], g[3]}) == 3


def test_the_evidence_finds_the_planted_lag_and_sign_and_skips_a_thin_block():
    y, near, x, used, group = world(7931, 0.6)
    used[group == 5, 0] = np.arange(PER) < local.LEAST - 1
    lag, t, slope, tested = local.evidence(y, x, used, group, FIT, False)
    assert (lag[5:8, 0] == 7).all() and (t[5:8, 0] > 4).all() and (np.abs(slope[5:8, 0] - 0.6) < 0.2).all()
    assert not tested[0, 5] and tested[1, 5] and t[0, 5] == 0
    assert np.abs(t[:, 1:]).max() < np.abs(t[5:8, 0]).min()


def test_with_one_slope_for_the_season_a_block_has_one_lag_and_the_planted_one_is_found():
    y, near, x, used, group = world(7937, 0.6)
    used[group == 5, 0] = np.arange(PER) < local.LEAST - 1
    lag, t, slope, tested = local.evidence(y, x, used, group, FIT, True)
    assert (lag[:, 0] == 7).all() and (t[:, 0] > 4).all() and (slope[:, 0] > 0).all()
    assert all(len(set(lag[tested[:, b], b])) == 1 for b in range(6))
    assert not tested[0, 5] and t[0, 5] == 0 and np.abs(t[:, 1:]).max() < t[0, 0]


def test_less_of_a_slope_is_kept_the_less_sure_it_is():
    assert local.weight(np.array([1.0, 2.0, 4.0]), 2.0).tolist() == [0, 0, 0.75] and local.weight(np.array([0.1]), 0.0)[0] == 1


def test_a_planted_link_beats_the_baseline_out_of_time_where_it_was_planted():
    model, out = run(*world(7932, 0.6))
    kept = np.abs(model["slope"])
    assert 0 < model["k"] <= 1 and model["claimed"][5:8, :PER].all()
    assert kept[5:8, :PER].min() > 3 * kept[:, PER:].max()
    assert out["ci"][0] > 0 and out["beats"] == len(out["shifted"]) == len(SCORED) - 1


def test_no_link_does_not_pass():
    model, out = run(*world(7933, 0.0))
    assert not (out["ci"][0] > 0 and out["beats"] == len(out["shifted"]))


def test_nothing_after_the_fitting_years_reaches_the_model():
    y, near, x, used, group = world(7934, 0.6)
    late, drv = y.copy(), x.copy()
    late[:, 264:] = np.random.default_rng(1).normal(size=late[:, 264:].shape)
    drv[:, 264:] = np.random.default_rng(2).normal(size=drv[:, 264:].shape)
    a = local.fit(y, near, x, used, group, FIT)
    b = local.fit(late, np.repeat(late.mean(axis=0, keepdims=True), len(late), axis=0), drv, used, group, FIT)
    c = local.fit(y[:, :264], near[:, :264], x[:, :264], used, group, FIT)
    for other in (b, c):
        assert np.allclose(a["slope"], other["slope"]) and (a["claimed"] == other["claimed"]).all() and (a["lag"] == other["lag"]).all()
        assert a["k"] == other["k"] and a["tau"] == other["tau"] and a["season"] == other["season"] and a["baseline"] == other["baseline"]


def test_a_model_sized_to_nothing_claims_nothing(monkeypatch):
    monkeypatch.setattr(local, "tune", lambda *a: (False, 0.0, 0.0, []))
    model, out = run(*world(7938, 0.6))
    assert model["k"] == 0 and not model["claimed"].any() and model["blocks"] == 0


def test_a_shift_gives_each_year_another_years_driver():
    y, near, x, used, group = world(7935, 0.6)
    model = local.fit(y, near, x, used, group, FIT)
    moved = local.term(x, SCORED, model["lag"], model["slope"], 3)
    assert np.allclose(moved, local.term(x, np.roll(SCORED, -3), model["lag"], model["slope"]))
    assert not np.allclose(moved, local.term(x, SCORED, model["lag"], model["slope"]))


def test_what_the_share_observed_explains_is_taken_out_from_the_fitting_years_only():
    rng = np.random.default_rng(7936)
    y, near, x, used, group = world(7936, 0.0)
    s = rng.normal(size=y.shape)
    step = rng.normal(0, 2, (6, 5))[group[:, None], np.digitize(s, local.CUTS)]  # by block and band of the share observed: no straight line
    out = local.adjusted(y + step, s, used, group, FIT)
    assert (out - y).std() < 0.25 and step.std() > 1.5
    late = y + step
    late[:, 264:] = 0
    assert np.allclose(local.adjusted(late, s, used, group, FIT)[:, :264], out[:, :264])


def test_a_departure_drops_a_steady_drift_and_reads_nothing_later():
    rng = np.random.default_rng(7939)
    x = rng.normal(size=(3, 12 * 20))
    drift = 0.01 * np.arange(x.shape[1])[None, :] * np.array([[1.0], [-2.0], [0.5]])
    first = 12 * local.BACK
    d = local.departure(x, first)
    assert d.shape == (3, x.shape[1] - first)
    assert np.allclose(local.departure(x + drift, first) - d, 0.36 * np.array([[1.0], [-2.0], [0.5]]))  # a line leaves a constant: three years of it
    assert np.allclose(d[:, 0], x[:, first] - x[:, first - 12 * np.arange(1, local.BACK + 1)].mean(axis=1))
    later = x.copy()
    later[:, first + 30 :] = 9.0
    assert np.allclose(local.departure(later, first)[:, :30], d[:, :30])
    assert np.allclose(local.departure(x, 0)[:, :12], x[:, :12])  # with no year before it, a value stands as it is


def test_a_term_less_its_line_keeps_only_what_differs_from_year_to_year():
    rng = np.random.default_rng(7940)
    d, t = rng.normal(size=(4, 15, 12)), np.arange(15)[None, :, None]
    line = rng.normal(size=(4, 1, 12)) + t * rng.normal(size=(4, 1, 12))
    flat = local.level(d)
    assert np.allclose(local.level(d + line), flat) and np.allclose(local.level(line), 0)
    assert np.allclose(flat.mean(axis=1), 0) and np.allclose((flat * t).sum(axis=1), 0)


def test_a_planted_link_still_passes_with_every_term_less_its_line():
    y, near, x, used, group = world(7932, 0.6)
    out = forecast.skill(*local.score(local.fit(y, near, x, used, group, FIT), x, SCORED, flat=True))
    assert out["ci"][0] > 0 and out["beats"] == len(SCORED) - 1


def test_a_rise_shared_over_the_scoring_years_passes_as_first_scored_and_not_once_terms_are_less_their_line():
    rng = np.random.default_rng(7941)
    cells, months = 60, 12 * 37
    rise = ((np.arange(months) / 12 - 29) / 7)[None, :]
    x, e = rise + rng.normal(size=(cells, months)), 1.5 * rise + rng.normal(size=(cells, months))
    model = {"e": e, "lag": np.full((12, cells), 6), "slope": np.full((12, cells), 0.3), "claimed": np.ones((12, cells), bool), "k": 1.0}
    first, then = forecast.skill(*local.score(model, x, SCORED)), forecast.skill(*local.score(model, x, SCORED, flat=True))
    assert first["ci"][0] > 0 and first["beats"] == len(SCORED) - 1
    assert then["s"] < 0 and then["ci"][1] < 0
