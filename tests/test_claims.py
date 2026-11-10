import numpy as np

from causal_atlas import claims, harvest
from test_harvest import world


def parts(seed, units=40, years=30, shifts=5, helped=(), by=2.0, size=0.3):
    """Made-up records: the outcome less a baseline, and a driver's term as it fell and under each shift. The terms are noise of spread `size`, except as it fell in the records named, where the outcome carries `by` times the term."""
    rng = np.random.default_rng(seed)
    term = size * rng.normal(size=(units, years, 1 + shifts))
    now = rng.normal(size=(units, years))
    now[list(helped)] += by * term[list(helped), :, 0]
    pick = rng.random((units, years)) < 0.9
    return {"unit_now": np.where(pick, now, 0), "unit_term": np.where(pick[:, :, None], term, 0), "pick": pick, "unit_alone": {"one": np.where(pick, 1.1 * now**2, 0)},
            "unit_base": np.where(pick, now**2, 0), "unit_model": np.where(pick[:, :, None], (now[:, :, None] - term) ** 2, 0)}


def test_the_flat_driver_is_the_one_the_forecast_makes():
    y, official, country, cereal, x, lat, lon = world(3, countries=25, years=40, link=0.05)
    r = harvest.run(y, official, country, cereal, x, lat, lon, 15, shifts=[2, 3])
    f = harvest.run(y, official, country, cereal, claims.level(x), lat, lon, 15, shifts=[2, 3], flat=False)
    assert f["flat"] is None and np.allclose(f["model"], r["flat"]) and np.allclose(f["unit_model"].sum(axis=0), r["flat"])
    assert np.allclose(np.where(r["pick"][:, :, None], (r["unit_now"][:, :, None] - r["unit_term"]) ** 2, 0), r["unit_model"])  # the parts make the errors
    assert all(np.allclose(r["unit_alone"][k].sum(axis=0), v) for k, v in r["alone"].items())
    half = np.arange(len(country)) % 2 == 0
    a = claims.only(r, half)
    assert np.array_equal(a["unit_term"], r["unit_term"][half]) and np.array_equal(a["unit_alone"]["last"], r["unit_alone"]["last"][half])


def test_a_record_stands_on_earlier_years_only():
    q = parts(1)
    a, ta = claims.standing(q["unit_now"], q["unit_term"], q["pick"])
    later = q["unit_now"].copy()
    later[:, 20:] += 5
    b, tb = claims.standing(later, q["unit_term"], q["pick"])
    assert np.array_equal(a[:, :21], b[:, :21]) and np.array_equal(ta[:, :21], tb[:, :21]) and not np.array_equal(a[:, 21:], b[:, 21:])
    assert np.isinf(ta[:, : claims.LEAST]).all() and not a[:, : claims.LEAST].any()  # no record has ten scored years behind it before the eleventh
    n = np.cumsum(q["pick"], axis=1)
    assert np.array_equal(np.isfinite(ta[:, 1:, 0]), n[:, :-1] >= claims.LEAST)


def test_standing_is_the_usual_slope_through_the_origin():
    q = parts(2, units=3, years=25, helped=[0])
    a, t = claims.standing(q["unit_now"], q["unit_term"], q["pick"])
    for u in range(3):
        keep = q["pick"][u, :24]
        z, f = q["unit_now"][u, :24][keep], q["unit_term"][u, :24, 0][keep]
        slope = (f @ z) / (f @ f)
        se = np.sqrt(((z - slope * f) ** 2).sum() / (len(z) - 1) / (f @ f))
        assert np.isclose(a[u, 24, 0], slope) and np.isclose(t[u, 24, 0], slope / se)


def test_a_term_that_has_been_nothing_claims_nothing():
    q = parts(3, helped=range(40))
    q["unit_term"][:5] = 0
    a, t = claims.standing(q["unit_now"], q["unit_term"], q["pick"])
    assert np.isinf(t[:5]).all() and not a[:5].any()
    assert not claims.claimed(q, np.arange(40), 1.0)["claim"][:5].any()


def test_the_interval_draws_countries_and_years():
    rng = np.random.default_rng(4)
    den = rng.uniform(1, 2, (30, 20))
    s, ci = claims.two_way(0.9 * den, den, seed=1)
    assert np.isclose(s, 0.1) and np.allclose(ci, 0.1)
    num = den * (1 - 0.1 - 0.3 * rng.normal(size=(30, 1)))  # the gain differs by country: years alone would not show how unsure it is
    s, ci = claims.two_way(num, den, seed=1)
    years_only = harvest.interval(num.sum(axis=0), den.sum(axis=0), 1)[1]
    assert ci[1] - ci[0] > 3 * (years_only[1] - years_only[0])


def test_claims_find_the_records_that_were_helped_and_shifts_find_none():
    helped = range(0, 80, 2)
    q = parts(5, units=80, years=40, shifts=20, helped=helped)
    country = np.arange(80) // 2
    c = claims.claimed(q, country, 2.0)
    others = [u for u in range(80) if u not in helped]
    assert c["claim"][list(helped)].any(axis=1).mean() > 0.9 and c["claim"][list(helped)][:, 20:].mean() > 0.6
    assert c["claim"][others].mean() < 0.1  # a record with no help claims now and then by chance, over many years of looking
    assert c["s"] > 0.15 and c["ci"][0] > 0.1 and c["beats"] == 20 and c["without_best"] > 0.1
    assert np.isclose(c["s"], c["unscaled"], atol=0.01)  # the outcome carries twice the term, and no slope may enlarge it
    assert not c["claim"][:, : claims.LEAST].any() and not (c["claim"] & ~q["pick"]).any()
    assert c["shift_mean"] < 0  # a shift claims by chance alone, and a term that is noise does harm where it is used


def test_the_slope_scales_the_term_no_further_than_the_cap():
    q = parts(8, units=60, years=40, shifts=3, helped=range(60), by=6.0)
    c = claims.claimed(q, np.arange(60) // 2, 2.0)
    capped = np.where(c["claim"], (q["unit_now"] - claims.CAP * q["unit_term"][:, :, 0]) ** 2, 0)
    assert np.allclose(c["error"], capped)  # every slope is near six, so every claim is scaled by the cap


def test_a_record_that_carries_half_its_term_is_forecast_with_half():
    q = parts(9, units=60, years=40, shifts=3, helped=range(60), by=0.5, size=2.0)
    c = claims.claimed(q, np.arange(60) // 2, 2.0)
    assert c["s"] > 0.4 and abs(c["unscaled"]) < 0.1  # the whole term overshoots as much as it helps; the record's own slope so far shrinks it


def test_no_help_anywhere_is_not_read():
    q = parts(6, units=80, years=40, shifts=20)
    out = claims.reading(q, q, np.arange(80) // 2)
    assert not any(v["passes"] for v in out.values()) and all(v["word"] == "not read" for v in out.values())


def test_the_words_follow_the_size_and_the_interval():
    q = parts(7, units=120, years=40, shifts=20, helped=range(0, 120, 2))
    out = claims.reading(q, q, np.arange(120) // 2)[claims.MAIN]
    assert out["passes"] and out["word"] == "a usable aid" and np.isclose(out["plain"], 1 - np.sqrt(1 - out["size"]))
    q["unit_alone"]["one"] = 0.5 * q["unit_base"]  # a baseline that by itself does better on the claims than the forecast does
    assert not claims.reading(q, q, np.arange(120) // 2)[claims.MAIN]["passes"]
    assert np.isclose(claims.plain(0.0167), 0.0084, atol=1e-4)
