"""The first real monthly read's runner: that no rearrangement or planted link lets 2020 to 2024 into the months that are read, that a table is moved by whole years, and the guards. Made-up numbers only; the real panel is not opened."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import run_stage_d as sd  # noqa: E402
from causal_atlas import finders as fd  # noqa: E402
from causal_atlas import referee as rf  # noqa: E402


def made(seed=0):
    rng = np.random.default_rng(seed)
    sets = np.array([sd.STILL] * 5 + ["climate"] * 5 + ["conflict and protest"] * 2 + ["earthquakes"] * 2)
    common = np.array([False] * 3 + [True] * 2 + [False] * 2 + [True] * 3 + [False] * 4)
    v = rng.normal(size=(14, 40, sd.MONTHS)).cumsum(axis=2)
    v[common] = v[common][:, :1]
    v[:, :, :60][rng.random((14, 40, 60)) < 0.5] = np.nan
    p = {"values": v, "sets": sets, "common": common, "group": np.repeat(np.arange(8), 5), "groups": np.array([f"g{i}" for i in range(8)]), "ids": np.array([f"s{i}" for i in range(14)])}
    p["allowed"] = sets[:, None] != sets[None, :]
    return p


def test_the_split_and_the_seeds():
    assert sd.FIRST % 12 == 0 and sd.LAST % 12 == 0 and sd.MONTHS % 12 == 0
    assert (sd.START + sd.FIRST // 12, sd.START + sd.LAST // 12) == (2009, 2020)
    seeds = {sd.REAL, sd.CONFIRM} | {s for r in sd.SEEDS.values() for s in r}
    assert min(seeds) >= 66001 and max(seeds) <= 66999 and len(seeds) == 42
    assert fd.pairs not in sd.members() and fd.by_state not in sd.members() and len(sd.members()) >= 10


def test_every_source_has_one_set():
    assert sd.set_of("candidates.sunspot.long.data") == "climate" and sd.set_of("ucdp_ged") == "conflict and protest"
    flat = [s for v in sd.SETS.values() for s in v]
    assert len(flat) == len(set(flat))


def test_months_count_from_january_of_the_first_year():
    assert sd.month("1980-01") == 0 and sd.month("2009-01") == sd.FIRST and sd.month("2024-12") == sd.MONTHS - 1


@pytest.mark.parametrize("how,plant", [("places", False), ("places", True), ("years", False)])
def test_the_unopened_months_do_not_enter(how, plant):
    p = made(1)
    q = {**p, "values": p["values"].copy()}
    q["values"][:, :, sd.LAST:] += 100 * np.random.default_rng(2).normal(size=q["values"][:, :, sd.LAST:].shape)
    a, b = sd.moved(p, how, 7), sd.moved(q, how, 7)
    if plant:
        a, b = sd.plant(p, a, 7)[0], sd.plant(q, b, 7)[0]
    np.testing.assert_array_equal(a[:, :, : sd.LAST], b[:, :, : sd.LAST])


def test_places_moved_keeps_each_series_and_breaks_the_places():
    p = made(3)
    v = sd.moved(p, "places", 11)
    still, vary = p["sets"] == sd.STILL, ~p["common"]
    np.testing.assert_array_equal(v[still & vary], p["values"][still & vary])
    k = (p["sets"] == "conflict and protest") & vary
    assert not np.array_equal(np.nan_to_num(v[k]), np.nan_to_num(p["values"][k]))
    key = lambda x: np.sort(np.nan_to_num(x, nan=-1e9).sum(axis=2), axis=1)
    np.testing.assert_allclose(key(v[k]), key(p["values"][k]))  # the same places' series, in another order
    order = [int(np.flatnonzero([np.array_equal(np.nan_to_num(v[k][0][j]), np.nan_to_num(row)) for row in p["values"][k][0]])[0]) for j in range(40)]
    np.testing.assert_array_equal(np.nan_to_num(v[k][1]), np.nan_to_num(p["values"][k][1][order]))  # one reordering for the whole set


@pytest.mark.parametrize("how", ["places", "years"])
def test_time_is_moved_by_whole_years_and_sets_stand_apart(how):
    p = made(4)
    v = sd.moved(p, how, 13)
    by = {}
    for k in sorted(set(p["sets"])):
        for s in np.flatnonzero((p["sets"] == k) & (p["common"] if how == "places" else True)):
            a, b = np.nan_to_num(p["values"][s, 0, : sd.LAST], nan=-1e9), np.nan_to_num(v[s, 0 if how == "years" or p["common"][s] else 0, : sd.LAST], nan=-1e9)
            if how == "places" and not p["common"][s]:
                continue
            shift = [n for n in range(0, sd.LAST, 12) if np.array_equal(np.roll(a, n), b)]
            assert len(shift) == 1
            assert by.setdefault(k, shift[0]) == shift[0]  # a set moves as one
    assert how == "places" or by[sd.STILL] == 0  # with places moved, each set's common series move against every other set's places, the still set's too
    years = sd.LAST // 12
    gaps = [min((a - b) % years, (b - a) % years) for i, a in enumerate(x // 12 for x in by.values()) for b in [y // 12 for y in by.values()][:i]]
    assert all(g >= sd.APART for g in gaps)
    if how == "years":
        np.testing.assert_array_equal(v[:, :, sd.LAST:], p["values"][:, :, sd.LAST:])


def test_planted_links_cross_sets_and_change_only_their_outcomes():
    p = made(5)
    base = sd.moved(p, "places", 17)
    v, truth = sd.plant(p, base, 17)
    assert len(truth) == sd.LINKS * len(sd.SIZES) and sorted({t["share"] for t in truth}) == sorted(sd.SIZES)
    outs = {t["outcome"] for t in truth}
    assert len(outs) == len(truth)
    for t in truth:
        assert p["sets"][t["outcome"]] != p["sets"][t["input"]] and not p["common"][t["outcome"]] and not p["common"][t["input"]]
        assert 1 <= t["lag"] <= 6 and t["input"] not in outs
        assert t["where"].sum() >= sd.QUARTER * 40 and len(set(p["group"][t["where"]])) >= rf.GROUPS
        changed = ~np.isclose(np.nan_to_num(v[t["outcome"]]), np.nan_to_num(base[t["outcome"]])).all(axis=1)
        assert not changed[~t["where"]].any() and changed[t["where"]].all()
    for s in range(len(v)):
        assert np.array_equal(np.nan_to_num(v[s]), np.nan_to_num(base[s])) == (s not in outs)


def test_a_planted_link_has_its_stated_share():
    p = made(6)
    base = sd.moved(p, "places", 19)
    v, truth = sd.plant(p, base, 19)
    t = truth[0]
    added = np.diff((v[t["outcome"]] - base[t["outcome"]])[t["where"]][:, 120: sd.LAST], axis=1)
    whole = np.diff(v[t["outcome"]][t["where"]][:, 120: sd.LAST], axis=1)
    share = np.median(added.var(axis=1) / whole.var(axis=1))
    assert 0.5 * t["share"] < share < 1.6 * t["share"]


def test_the_rule_for_2020_to_2024():
    good = {f: {"t": 3.0, "s": 0.01, "groups": 6, "years": 40} for f in rf.READS}
    assert sd.confirmed(good, 2.0)
    for k, bad in (("t", 1.5), ("t", None), ("s", -0.1), ("groups", 4), ("years", 30)):
        assert not sd.confirmed({**good, rf.READS[0]: {**good[rf.READS[0]], k: bad}}, 2.0)


def test_a_step_run_once_cannot_be_started_twice(tmp_path, monkeypatch):
    monkeypatch.setattr(sd, "HOLD", tmp_path)
    sd.only_once("real")
    with pytest.raises(SystemExit):
        sd.only_once("real")
    sd.only_once("confirm")


def test_marks_refuse_unregistered_or_repeated_seeds():
    row = lambda step, seed, leads: {"step": step, "seed": seed, "board": {"leads": leads, "passed": leads}}
    with pytest.raises(SystemExit):
        sd.marks([row("places", 1, 0)])
    with pytest.raises(SystemExit):
        sd.marks([row("places", 66001, 0), row("places", 66001, 0)])
    rs = [row("places", s, int(s < 66003)) for s in sd.SEEDS["places"]] + [row("years", s, 0) for s in list(sd.SEEDS["years"])[:-1]]
    m = sd.marks(rs)
    assert m["places"] == (20, 2, True) and m["years"] == (7, 0, None)
    assert sd.marks(rs + [row("places", 66001, 1)][:0] + [row("years", 66108, 1)])["years"] == (8, 1, True)
