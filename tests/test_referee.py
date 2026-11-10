"""The referee: nothing from a later year reaches an earlier score; a planted link passes and noise does not; sending more costs more. The worlds here are made in the test, small and plain."""
import numpy as np
import pytest

from causal_atlas import referee as rf

PLACES, YEARS, FIRST = 60, 50, 28
FORMS = rf.READS + rf.CHECKS
GROUP = np.repeat(np.arange(PLACES // 5), 5)


def world(seed, share=0.0, series=6, where=None, kind="slope"):
    """Series 0 is the outcome. With a share, series 1 a year before moves it (in `where`, or everywhere): steadily, or only when series 1 stood in its top tenth."""
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((series, PLACES, YEARS))
    before = np.concatenate([np.zeros((PLACES, 1)), v[1][:, :-1]], axis=1)
    signal = before if kind == "slope" else (before > 1.28) * 3.0
    inside = np.ones(PLACES, bool) if where is None else where
    v[0] = np.where(inside[:, None], np.sqrt(1 - share) * v[0] + np.sqrt(share) * signal, v[0])
    return v


def test_comparable_reads_earlier_years_only():
    v = world(1)
    cut = 30
    changed = v.copy()
    changed[:, :, cut:] = np.random.default_rng(2).standard_normal(changed[:, :, cut:].shape) * 5
    for form in FORMS:
        a, b = rf.comparable(v, form), rf.comparable(changed, form)
        assert np.array_equal(a[:, :, :cut], b[:, :, :cut], equal_nan=True)
        start = 2 * rf.MIN_PAST if form == "recent" else rf.MIN_PAST  # a recent line needs its years, and then years of its own departures
        assert np.isnan(a[:, :, : rf.MIN_PAST]).all() and np.isfinite(a[:, :, start + 2 :]).all()
        assert np.abs(a[np.isfinite(a)]).max() <= rf.CLIP


def test_a_value_in_the_past_moves_only_what_follows_it():
    v = world(3)
    moved = v.copy()
    moved[2, 7, 20] += 4.0
    for form in FORMS:
        a, b = rf.comparable(v, form), rf.comparable(moved, form)
        differ = ~np.isclose(a, b, equal_nan=True)
        assert differ[2, 7, 20:].any() and not differ[2, 7, :20].any()
        differ[2, 7] = False
        assert not differ.any()


PROPOSALS = [
    rf.proposal(0, [(1, 1)]),
    rf.proposal(0, [(1, 1)], where="claim"),
    rf.proposal(0, [(1, 1)], where=GROUP < 6),
    rf.proposal(0, [(1, 1)], "hinge", level=0.8),
    rf.proposal(0, [(1, 1)], "tail", level=0.9),
    rf.proposal(0, [(1, 1), (2, 1)], "product"),
    rf.proposal(0, [(1, 1)], "by_group", groups=GROUP % 2),
    rf.proposal(0, [(1, 1)], "by_state", state=(3, 1)),
    rf.proposal(0, [(1, 1), (2, 1), (3, 2)], "mode"),
    rf.proposal(0, [(1, 1)], when=(2, 1, 0.5)),
    rf.proposal(0, [(1, 1)], "tail", level=0.9, event=0.9),
    rf.proposal(0, [(1, 1)], event=0.1, where="claim"),
]


@pytest.mark.parametrize("p", PROPOSALS, ids=lambda p: f"{p['form']}-{p['where'] if isinstance(p['where'], str) else 'set'}-{p['event']}")
def test_no_later_year_reaches_an_earlier_score(p):
    v = world(4, share=0.3)
    cut = 40
    changed = v.copy()
    changed[:, :, cut:] = np.random.default_rng(5).standard_normal(changed[:, :, cut:].shape) * 5
    got = []
    for values in (v, changed):
        out = rf.outcome(values[0], GROUP, FIRST, p["event"])
        for form in FORMS:
            a, claims = rf.score(out, rf.terms(p, rf.comparable(values, form)), p["where"], FIRST)
            got.append(({k: x[:, : cut - FIRST] for k, x in a.items()}, claims[: cut - FIRST], out["chosen"][:, :cut]))
    for (a, ca, cha), (b, cb, chb) in zip(got[: len(FORMS)], got[len(FORMS) :]):
        assert all(np.array_equal(a[k], b[k]) for k in a) and np.array_equal(ca, cb) and np.array_equal(cha, chb)
        assert np.abs(a["base"]).sum() > 0


def test_no_two_terms_speak_in_one_place_year_and_a_hinge_is_silent_below_its_level():
    comp = rf.comparable(world(6))
    for p in (PROPOSALS[6], PROPOSALS[7]):
        z = rf.terms(p, comp)
        assert len(z) == 2 and ((z != 0).sum(axis=0) <= 1).all()
    hinge, tail = rf.terms(PROPOSALS[3], comp)[0], rf.terms(PROPOSALS[4], comp)[0]
    assert (hinge >= 0).all() and 0.1 < (hinge > 0).mean() < 0.3
    assert set(np.unique(tail)) == {0.0, 1.0} and 0.03 < tail.mean() < 0.2


def test_a_planted_link_passes_and_noise_does_not():
    noise = [rf.proposal(0, [(s, 1)]) for s in range(2, 6)]
    r = rf.judge(world(7, share=0.3), GROUP, FIRST, [rf.proposal(0, [(1, 1)])] + noise, seed=1)
    assert r["proposals"][0]["passes"] and r["passed"] == 1
    assert 0.15 < r["proposals"][0]["size"] < 0.45  # of the baseline's squared error, where 30% was planted
    lo, hi = r["proposals"][0]["fell"]["span"]
    assert lo < r["proposals"][0]["fell"]["s"] < hi
    r = rf.judge(world(8), GROUP, FIRST, [rf.proposal(0, [(1, 1)])] + noise, seed=1)
    assert r["passed"] == 0


def test_a_link_in_some_places_is_heard_there():
    inside = GROUP < 6
    r = rf.judge(world(9, share=0.35, where=inside), GROUP, FIRST, [rf.proposal(0, [(1, 1)], where=inside), rf.proposal(0, [(1, 1)], where=~inside)], seed=1)
    assert r["proposals"][0]["passes"] and not r["proposals"][1]["passes"]
    assert r["proposals"][0]["fell"]["places"] == inside.sum()


def test_an_event_is_scored_as_a_chance():
    v = world(10, share=0.5, kind="tail")
    r = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(1, 1)], "tail", level=0.9, event=0.9), rf.proposal(0, [(2, 1)], "tail", level=0.9, event=0.9)], seed=1)
    a, b = r["proposals"]
    assert a["fell"]["s"] > 0.05 and a["fell"]["t"] > 3 and a["passes"]
    assert not b["passes"] and abs(b["fell"]["s"]) < 0.05
    out = rf.outcome(v[0], GROUP, FIRST, 0.9)
    assert set(np.unique(out["y"][np.isfinite(out["y"])])) == {0.0, 1.0}
    assert all(((0 <= b) & (b <= 1))[np.isfinite(b)].all() for _, _, b in out["past"])


def test_sending_more_raises_the_bar():
    v = world(11, series=41)
    one = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(1, 1)])], seed=1)["bar"]
    forty = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(s, 1)]) for s in range(1, 41)], seed=1)["bar"]
    copies = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(1, 1)])] * 40, seed=1)["bar"]
    assert forty > one + 0.5
    assert copies < one + 0.3  # near copies are charged about as one; one proposal is still two reads


def test_the_check_is_not_charged_in_the_bar(monkeypatch):
    v = world(11, series=41)
    sent = [rf.proposal(0, [(s, 1)]) for s in range(1, 41)]
    with_check = rf.judge(v, GROUP, FIRST, sent, seed=1)
    monkeypatch.setattr(rf, "CHECKS", ())
    assert rf.judge(v, GROUP, FIRST, sent, seed=1)["bar"] == with_check["bar"]


def path(seed, shape):
    """A slow path of its own for each place, in units of a series' spread: a line, or a long wave."""
    rng = np.random.default_rng(seed)
    t = np.arange(YEARS)[None, :]
    if shape == "line":
        return rng.choice([-1, 1], (PLACES, 1)) * 0.15 * (t - YEARS / 2)
    return 2.5 * np.sin(2 * np.pi * (t / rng.uniform(40, 80, (PLACES, 1)) + rng.random((PLACES, 1))))


def test_a_place_with_a_path_of_its_own_gets_a_baseline_that_follows_it(monkeypatch):
    """A few places on a slow wave of their own: chosen place by place, they get a line that follows it; chosen once for all places, as the referee first stood, they get what serves the many, and their path stays in the baseline's error."""
    v = world(16)
    inside = GROUP < 2
    v[0] += np.where(inside[:, None], path(17, "wave"), 0.0)

    def chosen():
        out = rf.outcome(v[0], GROUP, FIRST)
        mine = np.take_along_axis(rf.baselines(out["y"], GROUP)[0], out["chosen"][None], 0)[0]
        return np.isin(out["chosen"][inside, FIRST:], (3, 5)).mean(), np.nanmean((out["y"] - mine)[inside, FIRST:] ** 2)  # its own line, or its recent line

    follows, error = chosen()
    monkeypatch.setattr(rf, "OWN", None)
    for_all, error_for_all = chosen()
    assert follows > 0.7 and for_all < 0.2 and error < 0.5 * error_for_all


def test_a_shared_slow_path_is_not_a_link(monkeypatch):
    """A series and an outcome that ride one slow path in the same places: the series tells nothing the place's own path did not. The referee as it first stood passed this."""
    inside = GROUP < 6
    sent = [rf.proposal(0, [(1, 1)], where=inside), rf.proposal(0, [(1, 1)]), rf.proposal(0, [(1, 1)], where="claim")] + [rf.proposal(0, [(s, 1)]) for s in range(2, 6)]
    passed = 0
    for seed in range(20, 26):
        v = world(seed)
        p = np.where(inside[:, None], path(seed + 100, "wave"), 0.0)
        v[0], v[1] = v[0] + p, v[1] + p
        r = rf.judge(v, GROUP, FIRST, sent, seed=1)
        assert r["passed"] == 0
        with monkeypatch.context() as m:
            m.setattr(rf, "OWN", None), m.setattr(rf, "PATH", False), m.setattr(rf, "CHECKS", ())
            passed += rf.judge(v, GROUP, FIRST, sent, seed=1)["passed"] > 0
    assert passed >= 4


def test_a_link_still_passes_beside_a_slow_path():
    inside = GROUP < 6
    v = world(30, share=0.3)
    v[0] += np.where(inside[:, None], path(31, "wave"), 0.0)
    v[2] += np.where(inside[:, None], path(31, "wave"), 0.0)
    r = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(1, 1)]), rf.proposal(0, [(2, 1)], where=inside)], seed=1)
    assert r["proposals"][0]["passes"] and not r["proposals"][1]["passes"]


def test_too_narrow_a_proposal_cannot_pass():
    inside = GROUP < rf.GROUPS - 1
    r = rf.judge(world(12, share=0.6, where=inside), GROUP, FIRST, [rf.proposal(0, [(1, 1)], where=inside)], seed=1)
    assert r["proposals"][0]["fell"]["t"] > r["bar"] and not r["proposals"][0]["passes"]


def test_the_same_seed_gives_the_same_reading():
    v = world(13, share=0.2)
    a, b = (rf.judge(v, GROUP, FIRST, PROPOSALS[:4], seed=3, shifts=(5,)) for _ in range(2))
    assert a == b
    assert a["bar"] != rf.judge(v, GROUP, FIRST, PROPOSALS[:4], seed=4)["bar"]


def test_gaps_are_carried():
    v = world(14, share=0.3)
    v[np.random.default_rng(15).random(v.shape) < 0.1] = np.nan
    r = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(1, 1)]), rf.proposal(0, [(2, 1)])], seed=1)
    assert r["proposals"][0]["passes"] and not r["proposals"][1]["passes"]
    assert np.isfinite(r["bar"])


def wander(seed, size=2.5, smooth=5):
    """A slow path a place: a random walk smoothed over a few years."""
    r = np.random.default_rng(seed)
    w = np.cumsum(r.standard_normal((PLACES, YEARS + smooth)), axis=1)
    w = np.stack([np.convolve(x, np.ones(smooth) / smooth, mode="valid")[:YEARS] for x in w])
    return size * (w - w.mean(axis=1, keepdims=True)) / w.std()


def test_a_planted_lead_passes_and_is_not_labelled_as_moving_together():
    for seed in range(40, 46):
        r = rf.judge(world(seed, share=0.3), GROUP, FIRST, [rf.proposal(0, [(1, 1)])] + [rf.proposal(0, [(s, 1)]) for s in range(2, 6)], seed=1)
        first = r["proposals"][0]
        assert first["passes"] and first["label"]["back"] is False and not first["label"]["together"]
        assert all(q["label"] is None for q in r["proposals"] if not q["passes"])


def test_a_shared_wandering_path_is_labelled_as_moving_together():
    """The label is asked for directly, so the test does not rest on which of these small worlds pass."""
    together = 0
    for seed in range(50, 58):
        v = world(seed)
        p = wander(seed + 100)
        v[0], v[1] = v[0] + p, v[1] + p
        ps = [rf.proposal(0, [(1, 1)])] + [rf.proposal(0, [(s, 1)]) for s in range(2, 6)]
        r = rf.judge(v, GROUP, FIRST, ps, seed=1, labels=False)
        assert all("label" not in q or q["label"] is None for q in r["proposals"])
        together += rf.label(v, GROUP, FIRST, ps[0], r["proposals"][0], seed=1)["together"]
    assert together >= 7


def test_a_link_within_the_year_through_a_lasting_series_is_labelled_by_the_same_year():
    """Series 1 lasts from year to year and moves the outcome in the same year: last year's value helps, this year's helps more, and the outcome a year before says nothing of the series."""
    for seed in range(60, 66):
        rng = np.random.default_rng(seed)
        v = rng.standard_normal((6, PLACES, YEARS))
        for t in range(1, YEARS):
            v[1][:, t] = 0.8 * v[1][:, t - 1] + 0.6 * v[1][:, t]
        v[0] = np.sqrt(0.5) * v[0] + np.sqrt(0.5) * v[1]
        first = rf.judge(v, GROUP, FIRST, [rf.proposal(0, [(1, 1)])] + [rf.proposal(0, [(s, 1)]) for s in range(2, 6)], seed=1)["proposals"][0]
        assert first["passes"] and first["label"]["back"] is False and first["label"]["same"] and first["label"]["together"]


def test_a_series_common_to_all_places_cannot_be_turned_round():
    v = world(70)
    v[1] = v[1][:1]
    before = np.concatenate([np.zeros((PLACES, 1)), v[1][:, :-1]], axis=1)
    v[0] = np.sqrt(0.5) * v[0] + np.sqrt(0.5) * before
    p = rf.proposal(0, [(1, 1)])
    assert rf.turned(p, v) == []
    first = rf.judge(v, GROUP, FIRST, [p], seed=1)["proposals"][0]
    assert first["passes"] and first["label"]["back"] is None and not first["label"]["together"]


def test_the_label_neither_makes_nor_unmakes_a_pass():
    v = world(41, share=0.3)
    p = wander(141)
    v[2], v[3] = v[2] + p, v[3] + p
    ps = [rf.proposal(0, [(1, 1)]), rf.proposal(2, [(3, 1)])] + [rf.proposal(0, [(s, 1)]) for s in range(4, 6)]
    a, b = rf.judge(v, GROUP, FIRST, ps, seed=1), rf.judge(v, GROUP, FIRST, ps, seed=1, labels=False)
    assert a["bar"] == b["bar"] and [q["passes"] for q in a["proposals"]] == [q["passes"] for q in b["proposals"]]
    for q, w in zip(a["proposals"], b["proposals"]):
        assert all(q[f]["t"] == w[f]["t"] for f in rf.READS)
