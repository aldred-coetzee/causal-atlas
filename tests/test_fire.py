import sys
from pathlib import Path

import numpy as np

from causal_atlas import fire, forecast

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))


def record(seed=0, cells=30):
    rng = np.random.default_rng(seed)
    b = rng.gamma(1.0, 50.0, size=(cells, fire.MONTHS // 12, 12))
    o = rng.uniform(0.3, 1.0, size=b.shape)
    gap = fire.ABSENT - fire.FIRST_YEAR
    b[:, gap], o[:, gap] = np.nan, np.nan
    return b, o


def test_the_absent_year_and_unseen_months_are_the_average_not_no_fire():
    b, o = record()
    o[0, 3, 5] = fire.SEEN / 2
    y, used = fire.standard(b, o)
    assert used.all() and np.isfinite(y).all()
    assert (y[:, fire.ABSENT - fire.FIRST_YEAR] == 0).all() and y[0, 3, 5] == 0
    years = np.delete(np.arange(fire.FIT // 12), fire.ABSENT - fire.FIRST_YEAR)
    assert abs(y[1:, years].mean(axis=1)).max() < 1e-9 and np.allclose(y[1:, years].std(axis=1), 1)


def test_burning_is_scaled_by_the_share_observed():
    b, o = record()
    y, _ = fire.standard(b, o)
    half, _ = fire.standard(b / 2, o / 2 + (o / 2 < fire.SEEN) * 0)
    seen_both = np.nan_to_num(o) / 2 >= fire.SEEN
    assert np.allclose(y[:, : fire.FIT // 12][seen_both[:, : fire.FIT // 12].all(axis=(1, 2))], half[:, : fire.FIT // 12][seen_both[:, : fire.FIT // 12].all(axis=(1, 2))])


def test_nothing_after_the_fitting_years_reaches_the_fitting_years():
    b, o = record()
    y, used = fire.standard(b, o)
    b[:, fire.FIT // 12 :] *= 7
    o[:, fire.FIT // 12 :] = 0.25
    later, used_later = fire.standard(b, o)
    assert np.array_equal(y[:, : fire.FIT // 12], later[:, : fire.FIT // 12]) and np.array_equal(used, used_later)


def test_a_calendar_month_that_rarely_burns_or_is_rarely_seen_is_not_used():
    b, o = record()
    b[0, :, 2] = 0
    b[0, :4, 2] = 5
    o[1, :10, 7] = 0
    y, used = fire.standard(b, o)
    assert not used[0, 2] and not used[1, 7] and used.sum() == used.size - 2
    assert (y[0, :, 2] == 0).all() and (y[1, :, 7] == 0).all()


def test_a_planted_link_lands_only_on_used_months_of_the_busiest_season():
    import run_fire

    rng = np.random.default_rng(1)
    used = np.zeros((40, 12), bool)
    used[:, [11, 0, 1]] = True
    used[:20, 6] = True
    assert run_fire.season(used) == [11, 0, 1]
    y = np.zeros((40, fire.FIT), np.float32)
    z = rng.normal(size=fire.FIT)
    out, cells, months = run_fire.planted(y, used, rng.uniform(0, 10, 40), rng.uniform(0, 10, 40), z, 3, 0.4, 0.25)
    touched = np.flatnonzero(np.abs(out).sum(axis=0))
    assert months == [11, 0, 1] and len(cells) == 10
    assert set(touched % 12) == {11, 0, 1} and touched.min() >= 12
    assert not np.delete(out, cells, axis=0).any()


def test_fitting_on_named_years_leaves_the_default_as_it_was():
    rng = np.random.default_rng(2)
    y = rng.normal(size=(20, 360))
    x = rng.normal(size=360)
    near = np.repeat(y.mean(axis=0, keepdims=True), 20, axis=0)
    a, b = forecast.fit(y, near, x, 240), forecast.fit(y, near, x, 240, np.arange(1, 20))
    assert a["baseline"] == b["baseline"] and a["k"] == b["k"] and np.array_equal(a["e"], b["e"]) and np.array_equal(a["slope"], b["slope"])
    c = forecast.fit(y, near, x, 240, np.delete(np.arange(1, 20), 11))
    assert not np.array_equal(a["slope"], c["slope"])


def test_pooling_sums_each_part_over_the_fields_named():
    import run_fire

    rng = np.random.default_rng(3)
    parts = {f: [rng.random(15), rng.random(15), rng.random((14, 15)), {"zero": rng.random(15), "level": rng.random(15)}] for f in "abc"}
    base, got, shifted, alone = run_fire.pooled(parts, ["a", "c"])
    assert np.allclose(base, parts["a"][0] + parts["c"][0]) and np.allclose(got, parts["a"][1] + parts["c"][1])
    assert shifted.shape == (14, 15) and np.allclose(alone["level"], parts["a"][3]["level"] + parts["c"][3]["level"])
