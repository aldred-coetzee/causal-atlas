"""The changed table of the second real read: the change itself, and that no rearrangement lets the last ten years into the years that are read. Made-up numbers only; the real panel is not opened."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import run_stage_b as sb  # noqa: E402

KEPT = (sb.OUT, sb.SEEDS, sb.MOST)
import run_stage_c as sc  # noqa: E402

FILE = (sb.OUT, sb.SEEDS, sb.MOST)
sb.OUT, sb.SEEDS, sb.MOST = KEPT  # importing the second read's runner must not leave the first read's names changed for other tests


def made(seed=0):
    rng = np.random.default_rng(seed)
    sets = np.array(["world bank"] * 5 + ["crops"] * 4 + ["exchange rates"] * 2 + ["climate"] * 3)
    common = np.array([False] * 12 + [True] * 2)
    v = rng.normal(size=(14, 40, 64)).cumsum(axis=2)
    v[common] = v[common][:, :1]
    v[rng.random(v.shape) < 0.1] = np.nan
    p = {"values": v, "sets": sets, "common": common, "group": np.repeat(np.arange(8), 5), "groups": np.array([f"g{i}" for i in range(8)]), "ids": np.array([f"s{i}" for i in range(14)])}
    p["allowed"] = sets[:, None] != sets[None, :]
    return p


def test_the_runner_keeps_its_own_file_and_seeds():
    assert FILE[0].name == "stage-c-second-read.jsonl" and KEPT[0].name == "stage-b-first-read.jsonl"
    spent = set(range(58001, 59000)) | set(range(59001, 64000))
    assert not spent & ({sc.REAL, sc.CONFIRM} | {s for r in sc.SEEDS.values() for s in r})


def test_change_is_the_value_less_the_year_before():
    v = np.array([[[1.0, 4.0, np.nan, 6.0, 9.0]]])
    np.testing.assert_array_equal(sc.change(v), [[[np.nan, 3.0, np.nan, np.nan, 3.0]]])


def test_unmoved_is_the_change_of_the_panel():
    p = made()
    v, truth = sc.changed(p)
    assert truth is None
    np.testing.assert_array_equal(v, sc.change(p["values"]))


@pytest.mark.parametrize("how,plant", [("places", False), ("places", True), ("years", False)])
def test_the_last_ten_years_do_not_enter(how, plant):
    p = made(1)
    q = {**p, "values": p["values"].copy()}
    q["values"][:, :, sc.LAST:] += 100 * np.random.default_rng(2).normal(size=q["values"][:, :, sc.LAST:].shape)
    a, b = sc.changed(p, how, 7, plant)[0], sc.changed(q, how, 7, plant)[0]
    np.testing.assert_array_equal(a[:, :, : sc.LAST], b[:, :, : sc.LAST])
    assert not np.array_equal(np.nan_to_num(a[:, :, sc.LAST:]), np.nan_to_num(b[:, :, sc.LAST:]))


def test_places_moved_keeps_each_series_and_breaks_the_places():
    p = made(3)
    v, _ = sc.changed(p, "places", 11)
    c = sc.change(p["values"])
    bank, crops = p["sets"] == "world bank", p["sets"] == "crops"
    np.testing.assert_array_equal(v[bank], c[bank])
    assert not np.array_equal(np.nan_to_num(v[crops]), np.nan_to_num(c[crops]))
    key = lambda x: np.sort(np.nan_to_num(x, nan=-1e9).reshape(len(x), -1), axis=1)
    np.testing.assert_array_equal(key(v[crops]), key(c[crops]))  # the same changes, in other places: no change is taken across two places


def test_years_moved_takes_no_change_across_a_seam():
    p = made(4)
    v, _ = sc.changed(p, "years", 13)
    c = sc.change(p["values"])
    key = lambda x: np.sort(np.nan_to_num(x[:, :, : sc.LAST], nan=-1e9), axis=2)
    np.testing.assert_array_equal(key(v), key(c))  # each place keeps its own changes of the years before LAST, in another order
    np.testing.assert_array_equal(v[:, :, sc.LAST:], c[:, :, sc.LAST:])


def test_planted_links_are_put_in_before_the_change():
    p = made(5)
    plain, _ = sc.changed(p, "places", 17)
    v, truth = sc.changed(p, "places", 17, plant=True)
    assert len(truth) == 9
    outs = {t["outcome"] for t in truth}
    for s in range(len(v)):
        same = np.array_equal(np.nan_to_num(v[s]), np.nan_to_num(plain[s]))
        assert same == (s not in outs)
