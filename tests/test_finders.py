"""The finders and the steward: nothing from the years the referee scores reaches the board; the same table gives the same board; each family puts what was planted for it first, and roughly where; a member that tries or chooses more is not ranked higher for it; the steward keeps to its rule. The worlds here are made in the test, small and plain."""
import inspect

import numpy as np

from causal_atlas import finders as fd
from causal_atlas import referee as rf

PLACES, YEARS, FIRST = 120, 50, 30
GROUP = np.repeat(np.arange(PLACES // 5), 5)
QUARTER = GROUP < 6


def world(seed, kind=None, share=0.4, series=8, where=QUARTER):
    """Series 0 and 1 are outcomes. Series 2 a year before moves series 0 in `where`: steadily; only in its top tenth; times series 3; or each place its own way. Series 7 is the same in every place."""
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((series, PLACES, YEARS))
    v[7] = v[7][:1]
    before = np.concatenate([np.zeros((series, PLACES, 1)), v[:, :, :-1]], axis=2)
    signal = {None: 0.0, "steady": before[2], "tail": (before[2] > 1.28) * 3.0, "pair": before[2] * before[3], "flip": before[2] * np.where(np.arange(PLACES) % 2, 1.0, -1.0)[:, None]}[kind]
    v[0] = np.where(where[:, None], np.sqrt(1 - share) * v[0] + np.sqrt(share) * signal, v[0])
    return v


def see(v):
    return fd.view(v, GROUP, FIRST, [0, 1])


def same(a, b):
    """Two boards, row for row."""
    def flat(r):
        return {k: (x.tolist() if isinstance(x, np.ndarray) else x) for k, x in r.items()}
    return len(a) == len(b) and all(flat(x) == flat(y) for x, y in zip(a, b))


def top(rows):
    return max(rows, key=lambda r: r["lift"])


def inside(row, where=QUARTER):
    """The share of a row's places that are in `where`, and the share of `where` the row took."""
    return (row["where"] & where).sum() / row["where"].sum(), (row["where"] & where).sum() / where.sum()


def test_level_is_the_referees():
    c = np.random.default_rng(1).standard_normal((3, 20, 40))
    c[0, 3, 5:9] = np.nan
    c[1, :, :12] = np.nan
    c[2, 7] = np.nan
    for q in (0.9, 0.8, 0.2, 0.1):
        assert np.allclose(fd.level(c, q), rf._level(c, q), equal_nan=True)


def test_nothing_from_the_scored_years_reaches_the_board():
    v = world(2, "steady")
    changed = v.copy()
    changed[:, :, FIRST:] = np.random.default_rng(3).standard_normal(changed[:, :, FIRST:].shape) * 5
    assert same(fd.swarm(see(v)), fd.swarm(see(changed)))


def test_same_table_same_board():
    v = world(4, "pair")
    a, b = fd.swarm(see(v)), fd.swarm(see(v.copy()))
    assert same(a, b) and len(a) > fd.SENT
    assert same(fd.steward(a), fd.steward(b))


def test_the_finders_never_look_at_the_generator():
    assert "synth" not in inspect.getsource(fd).replace("synthetic", "")
    assert "table_panel" not in inspect.getsource(fd)


def test_a_view_knows_which_series_are_the_same_everywhere():
    v = see(world(5))
    assert v["common"].tolist() == [False] * 7 + [True]
    assert v["values"].shape[2] == FIRST and v["shifts"][0] == fd.QUIET and len(v["shifts"]) >= 3


def test_a_steady_link_in_a_quarter_tops_the_slopes_and_is_placed():
    v = see(world(6, "steady"))
    row = top(fd.slope(v, 0, []))
    assert row["names"] == {2} and row["form"] == "slope" and row["inputs"] == [(2, 1)]
    mine, found = inside(row)
    assert mine >= 0.6 and found >= 0.6
    assert row["lift"] > 8 and top(fd.slope(v, 1, []))["lift"] < row["lift"] - 5  # the other outcome has nothing


def test_a_link_everywhere_is_sent_for_most_places():
    v = see(world(7, "steady", share=0.3, where=np.ones(PLACES, bool)))
    row = top(fd.slope(v, 0, []))
    assert row["names"] == {2}
    assert isinstance(row["where"], str) or row["where"].sum() >= 0.7 * PLACES


def test_a_scan_takes_enough_groups_and_all_when_it_is_all():
    rng = np.random.default_rng(8)
    size = np.full(24, 5.0)
    c, b = np.ones((1, 24)), np.ones(24)
    one = np.zeros((1, 6, 24))
    one[0, 0, 3] = 5.0  # one group alone goes with the outcome
    one[0, 1:] = rng.standard_normal((5, 24)) * 0.1
    stand, order, k, way = fd.scan(one, c, b, size)
    assert k[0] + 1 >= rf.GROUPS and order[0][0] == 3 and way[0] == 1
    every = np.full((1, 6, 24), 0.5)
    every[0, 1:] = rng.standard_normal((5, 24)) * 0.1
    stand, order, k, way = fd.scan(every, c, b, size)
    assert k[0] + 1 == 24
    stand, order, k, way = fd.scan(-every, c, b, size)
    assert k[0] + 1 == 24 and way[0] == -1


def test_a_tail_link_tops_the_extremes():
    v = see(world(9, "tail", share=0.5))
    row = top(fd.tail(v, 0, [], 0.9))
    assert row["names"] == {2} and row["form"] == "tail" and row["level"] == 0.9
    assert inside(row)[0] >= 0.6


def test_two_together_top_the_pairs_and_neither_alone_stands():
    v = see(world(10, "pair", share=0.5))
    row = top(fd.pairs(v, 0, []))
    assert row["names"] == {2, 3} and row["form"] == "product" and inside(row)[0] >= 0.6
    assert row["lift"] > 6 and top(fd.slope(v, 0, []))["lift"] < row["lift"] - 3


def test_a_pair_does_not_ride_on_one_strong_series():
    v = see(world(11, "steady", share=0.5))
    alone, together = top(fd.slope(v, 0, [])), top(fd.pairs(v, 0, []))
    assert alone["names"] == {2} and alone["lift"] > 3
    assert together["lift"] < alone["lift"] - 2


def test_beyond_leaves_nothing_of_the_parts():
    rng = np.random.default_rng(12)
    z, x, y = rng.standard_normal((3, 4, 10, 18))
    one, two = fd.beyond(z, [x]), fd.beyond(z, [x, y])
    assert np.allclose((one * x).sum(axis=2), 0)
    assert np.allclose((two * x).sum(axis=2), 0) and np.allclose((two * y).sum(axis=2), 0)
    assert np.allclose(fd.beyond(x * 2.0, [x]), 0)
    assert np.isfinite(fd.beyond(z, [np.zeros_like(x), np.zeros_like(y)])).all()  # a part that says nothing takes nothing


def test_a_sign_that_differs_by_place_is_found_with_its_signs():
    v = see(world(13, "flip", share=0.5))
    row = top(fd.by_place(v, 0, []))
    assert row["names"] == {2} and row["form"] == "by_group" and inside(row)[0] >= 0.6
    took = row["where"] & QUARTER
    assert (row["groups"][took] == (np.arange(PLACES) % 2)[took]).mean() >= 0.8
    assert top(fd.slope(v, 0, []))["lift"] < row["lift"]  # a pooled slope sees little of it


def test_a_lift_is_in_each_terms_own_units_and_trying_more_does_not_raise_it():
    rng = np.random.default_rng(14)
    stand = rng.standard_normal((30, 14))
    stand[0, 0] = 9.0
    up = fd.lift(stand)
    assert np.argmax(up) == 0
    assert np.allclose(fd.lift(stand * rng.uniform(0.5, 20, (30, 1))), up)  # a series with long memory does not set the scale
    more = np.concatenate([stand, rng.standard_normal((300, 14))])
    assert fd.lift(more)[0] < up[0]  # the same term among ten times as many stands lower
    assert np.isneginf(fd.lift(stand[:, :3])).all()  # too few other alignments to say


def test_noise_has_no_lift_to_speak_of():
    v = see(world(15))
    board = fd.swarm(v)
    assert len(board) > fd.SENT
    assert np.median([r["lift"] for r in board]) < 0
    assert max(r["lift"] for r in board) < 6  # with so few other alignments a lift of four is chance; a planted link here stands at ten or more
    assert all(r["outcome"] not in r["names"] for r in board)


def row(outcome, names, family, lift, tag=None, rnd=1):
    return {"outcome": outcome, "names": frozenset(names), "family": family, "member": "m", "round": rnd, "lift": lift, "tag": tag, "where": "all", "event": None, "inputs": [(s, 1) for s in names], "form": "slope"}


def test_the_steward_counts_a_familys_rows_for_one_link_once_and_takes_turns():
    board = [row(0, [2], "slope", 5.0), row(0, [2], "slope", 7.0), row(0, [3], "slope", 4.0), row(0, [2], "shape", 3.0), row(1, [4, 5], "pairs", 2.0), row(0, [6], "extremes", 1.0), row(0, [3], "shape", 0.5)]
    sent = fd.steward(board, sent=6, share=1, floor=-np.inf)
    assert [(r["family"], sorted(r["names"]), r["lift"], r["chosen"]) for r in sent[:4]] == [("slope", [2], 7.0, "slope"), ("shape", [2], 3.0, "shape"), ("extremes", [6], 1.0, "extremes"), ("pairs", [4, 5], 2.0, "pairs")]
    assert [(r["family"], sorted(r["names"]), r["chosen"]) for r in sent[4:]] == [("slope", [3], "agreement"), ("shape", [3], "agreement")]  # two families arrived at series 3
    assert sent[0]["families"] == ["shape", "slope"] and len(sent) == 6
    assert len(fd.steward(board, sent=3, share=1, floor=-np.inf)) == 3


def test_the_steward_keeps_to_the_floor_the_rounds_and_the_tags():
    board = [row(0, [2], "slope", 5.0), row(0, [3], "slope", -1.0), row(0, [2, 3], "pairs", 4.0, rnd=2), row(0, [4, 5, 6], "modes", 1.0, tag="component 1"), row(0, [4, 5, 6], "modes", 0.5, tag="component 2")]
    assert len(fd.steward(board, floor=-np.inf)) == 5  # two components of one block are two rows
    assert [sorted(r["names"]) for r in fd.steward(board, floor=0.0)] == [[2], [2, 3], [4, 5, 6], [4, 5, 6]]
    assert [sorted(r["names"]) for r in fd.steward(board, floor=-np.inf, rounds=1)] == [[2], [4, 5, 6], [3], [4, 5, 6]]
    assert fd.FLOOR == 3.0 and [sorted(r["names"]) for r in fd.steward(board)] == [[2], [2, 3]]  # by default a row three spreads above chance or nothing


def test_a_row_goes_to_the_referee_as_posted():
    v = see(world(16, "tail", share=0.5))
    r = top(fd.tail(v, 0, [], 0.9))
    p = fd.proposal(r)
    assert p["outcome"] == 0 and p["form"] == "tail" and p["level"] == 0.9 and p["by"] == "extremes: tail 0.9"
    assert np.array_equal(p["where"], r["where"])


def test_the_swarm_the_steward_and_the_referee_hear_a_planted_link():
    v = world(17, "steady", share=0.5)
    rows = fd.steward(fd.swarm(see(v)))
    assert 0 < len(rows) < fd.SENT and all(r["lift"] >= fd.FLOOR for r in rows)
    res = rf.judge(v, GROUP, FIRST, [fd.proposal(r) for r in rows], seed=1)
    heard = [r for r, q in zip(rows, res["proposals"]) if q["passes"]]
    assert heard and all(r["outcome"] == 0 and 2 in r["names"] for r in heard)


def test_allowing_everything_changes_nothing():
    v = world(6, "pair")
    assert same(fd.swarm(see(v)), fd.swarm(fd.view(v, GROUP, FIRST, [0, 1], allowed=np.ones((8, 8), bool))))


def test_a_row_names_only_what_its_outcome_may():
    v = world(7, "steady")
    ok = np.ones((8, 8), bool)
    ok[0, [2, 4]] = ok[1, 5] = False  # outcome 0 may not name series 2 or 4, nor outcome 1 series 5
    cut = fd.swarm(fd.view(v, GROUP, FIRST, [0, 1], allowed=ok))
    assert cut and all(ok[r["outcome"], s] for r in cut for s in r["names"])
    assert any(2 in r["names"] for r in cut if r["outcome"] == 1) and any(5 in r["names"] for r in cut if r["outcome"] == 0)
    assert {r["family"] for r in cut} == set(fd.ORDER)
    free = top([r for r in fd.swarm(see(v)) if r["outcome"] == 0 and r["member"] == "lag 1"])
    assert free["names"] == {2} and top([r for r in cut if r["outcome"] == 0 and r["member"] == "lag 1"])["lift"] < free["lift"]  # the planted series is out of reach, and nothing stands in for it


def test_what_may_not_be_named_is_not_counted_among_a_members_terms():
    v = world(8)
    v[0] = np.where(QUARTER[:, None], np.sqrt(0.6) * v[0] + np.sqrt(0.4) * np.concatenate([np.zeros((PLACES, 1)), v[3][:, :-1]], axis=1), v[0])  # series 3 a year before moves outcome 0
    ok = np.zeros((8, 8), bool)
    ok[0, 3] = True  # outcome 0 may name series 3 alone
    alone = fd.swarm(fd.view(v[[0, 3]], GROUP, FIRST, [0]), [fd.slope])  # a table that holds nothing else
    cut = fd.swarm(fd.view(v, GROUP, FIRST, [0], allowed=ok), [fd.slope])
    assert len(cut) == len(alone) == 1 and cut[0]["names"] == {3} and alone[0]["names"] == {1}
    assert np.isclose(cut[0]["lift"], alone[0]["lift"]) and (cut[0]["where"] == alone[0]["where"]).all()


def test_the_swarm_runs_without_the_every_pair_member():
    v = world(10, "pair")
    full, less = fd.swarm(see(v)), fd.swarm(see(v), [m for m in fd.MEMBERS if m is not fd.pairs])
    gone = {r["member"] for r in full} - {r["member"] for r in less}
    assert gone == {"every pair"}
    assert same([r for r in full if r["round"] == 1 and r["member"] not in gone], [r for r in less if r["round"] == 1])
    assert any(r["member"] == "pairs from the board" for r in less)


def test_a_gathered_row_never_names_what_it_may_not_when_a_series_has_no_standing():
    v = world(11, "steady")
    ok = np.zeros((8, 8), bool)
    ok[0, 2:7] = True  # outcome 0 may name series 2 to 6
    v[6] = np.nan  # and one of them has no values at all: it must not let the outcome or a barred series into its place
    rows = fd.gathered(fd.view(v, GROUP, FIRST, [0], allowed=ok), 0, [])
    assert rows and all(r["names"] <= {2, 3, 4, 5} for r in rows)
