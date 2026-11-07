import sys
from pathlib import Path

import numpy as np

from causal_atlas import bench as b, screen as c

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import toy  # noqa: E402


def noise(rng, cols=200):
    return rng.standard_normal((cols, 33)) ** 2


def test_gate_on_pure_noise_names_a_lead_at_about_one_in_33():
    rng = np.random.default_rng(1)
    named = sum(bool(c.gate(noise(rng))[0]) for _ in range(1000))
    assert 10 <= named <= 60


def test_ceiling_plugin_scores_every_world_and_floor_stays_near_chance():
    rng = np.random.default_rng(2)
    names = [f"s{i}" for i in range(32)]
    true = {"s0", "s1"}
    hits = 0
    for _ in range(2000):
        pick = names[rng.integers(32)]
        hits += b.read_world([dict(input=pick, lead=True)], true)["first_true"]
        assert b.read_world([dict(input="s0", lead=True)], true)["first_true"]
    assert 0.04 < hits / 2000 < 0.09


def test_first_lead_must_be_true_and_any_lead_is_beside():
    found = [dict(input="decoy", lead=True), dict(input="a", lead=True), dict(input="b", lead=False)]
    r = b.read_world(found, {"a"})
    assert r["named"] and not r["first_true"] and r["any_true"]
    r = b.read_world([dict(input="a", lead=False)], {"a"})
    assert not r["named"] and not r["first_true"] and r["top_true"]


def test_claims_decode_input_gap_and_width():
    t = np.random.default_rng(3).standard_normal((c.PER_SERIES * 2, 33)) ** 2
    col = c.PER_SERIES + 2 * len(c.WIDTHS) + 1  # second series, third gap, second width
    t[col, 0] = 1e6
    first = b.claims(t, ["x", "y"])[0]
    assert (first["input"], first["gap"], first["width"], first["lead"]) == ("y", c.GAPS[2], c.WIDTHS[1], True)


def test_marks_use_only_worlds_with_something_to_find():
    planted = [dict(ceiling=True, heard=True, first_true=i < 5) for i in range(10)] + [dict(ceiling=False, heard=False, first_true=False) for _ in range(5)]
    nulls = [dict(named=i < 3) for i in range(30)]
    m = b.marks(dict(planted=planted, nulls=nulls))
    assert (m["E"], m["outside"], m["found"]) == (10, 5, 5) and m["instrument"] and m["recovery"] and m["quiet"]
    assert not b.marks(dict(planted=planted, nulls=[dict(named=i < 4) for i in range(30)]))["quiet"]
    assert not b.marks(dict(planted=[], nulls=nulls))["recovery"]


def test_choose_form_needs_quiet_then_most_found_then_fewer_named():
    forms = dict(all=dict(first_true=9, null_named=3), largest=dict(first_true=7, null_named=2), pooled=dict(first_true=7, null_named=1))
    assert b.choose_form(forms) == "pooled"
    assert b.choose_form(dict(all=dict(first_true=9, null_named=3))) is None
    assert b.step_two(dict(first_true=8, null_named=2)) and not b.step_two(dict(first_true=7, null_named=0))


def test_wilson_brackets_the_share():
    lo, hi = b.wilson(10, 20)
    assert lo < 0.5 < hi and b.wilson(0, 0) == (0.0, 1.0)


def test_toy_null_differs_from_planted_only_by_the_link():
    lat, lon = np.linspace(-30, 30, 40), np.linspace(-20, 40, 40)
    p, n = toy.generate(lat, lon, 7), toy.generate(lat, lon, 7, linked=False)
    assert np.allclose(p["y"] - n["y"], p["exact"]) and np.array_equal(p["a"], n["a"])
    assert p["exact"][lat < np.median(lat)].std() < p["exact"][lat >= np.median(lat)].std()


def test_shortlist_keeps_one_column_per_input():
    t = np.random.default_rng(4).standard_normal((c.PER_SERIES * 8, 33)) ** 2
    t[[0, 1, c.PER_SERIES + 3], 0] = [1e6, 1e5, 1e4]
    held = b.shortlist(t, n=3)
    assert held[:2] == [0, c.PER_SERIES + 3] and len({x // c.PER_SERIES for x in held}) == 3


def test_gate_on_five_noise_columns_names_a_lead_at_about_one_in_33():
    rng = np.random.default_rng(5)
    named = sum(bool(c.gate(noise(rng, 5))[0]) for _ in range(2000))
    assert 30 <= named <= 100


def test_claims_on_chosen_columns_map_back():
    t = np.random.default_rng(6).standard_normal((c.PER_SERIES * 4, 33)) ** 2
    col = c.PER_SERIES * 3 + 1
    t[col, 0] = 1e6
    first = b.claims(t, list("abcd"), chosen=[0, col])[0]
    assert first["input"] == "d" and first["lead"] and first["width"] == c.WIDTHS[1]
