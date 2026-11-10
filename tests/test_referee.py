"""The referee: nothing from a later year reaches an earlier score; a planted link passes and noise does not; sending more costs more. The worlds here are made in the test, small and plain."""
import numpy as np
import pytest

from causal_atlas import referee as rf

PLACES, YEARS, FIRST = 60, 50, 28
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
    for flat in (False, True):
        a, b = rf.comparable(v, flat), rf.comparable(changed, flat)
        assert np.array_equal(a[:, :, :cut], b[:, :, :cut], equal_nan=True)
        assert np.isnan(a[:, :, : rf.MIN_PAST]).all() and np.isfinite(a[:, :, rf.MIN_PAST + 2 :]).all()
        assert np.abs(a[np.isfinite(a)]).max() <= rf.CLIP


def test_a_value_in_the_past_moves_only_what_follows_it():
    v = world(3)
    moved = v.copy()
    moved[2, 7, 20] += 4.0
    a, b = rf.comparable(v), rf.comparable(moved)
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
        for flat in (False, True):
            a, claims = rf.score(out, rf.terms(p, rf.comparable(values, flat)), p["where"], FIRST)
            got.append(({k: x[:, : cut - FIRST] for k, x in a.items()}, claims[: cut - FIRST], out["chosen"][:cut]))
    for (a, ca, cha), (b, cb, chb) in zip(got[:2], got[2:]):
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
