"""Tests for the shared slow paths (synth/shared_paths.py)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import shared_paths as sp  # noqa: E402
import table_panel as tp  # noqa: E402


@pytest.fixture(scope="module")
def world():
    return tp.make(3, "steady", places=60)


def added(world, w, p):
    """What was added to a pair's outcome and to its series, (places, years) each."""
    v0, v1 = world["values"], w["values"]
    return v1[p["outcome"]] - v0[p["outcome"]], v1[p["series"]] - v0[p["series"]]


def slow(x):
    """Year-to-year change (spread of first differences) against range over the record, median over places."""
    return np.median(np.diff(x, axis=1).std(axis=1) / np.ptp(x, axis=1))


def one_step_miss(x):
    """Fit a 3-lag linear rule to the first 40 years; its one-step error over the rest, in spreads of yearly change."""
    def design(a):
        return np.column_stack([np.ones(len(a) - 3), a[2:-1], a[1:-2], a[:-3]])
    miss = []
    for p in x:
        coef = np.linalg.lstsq(design(p[:40]), p[3:40], rcond=None)[0]
        miss.append(np.sqrt(np.mean((p[3:] - design(p) @ coef)[37:] ** 2)) / np.diff(p).std())
    return np.median(miss)


def test_kinds_declared():
    assert len(sp.KINDS) >= 6 and set(sp.FORESEEABLE) == set(sp.KINDS)
    assert sum(sp.FORESEEABLE.values()) >= 2 and not all(sp.FORESEEABLE.values())


def test_deterministic_and_unchanged_input(world):
    before = world["values"].copy()
    a, b, c = (sp.add(world, s, "mixed") for s in (5, 5, 6))
    assert a["values"].tobytes() == b["values"].tobytes()
    assert not np.array_equal(a["values"], c["values"])
    assert np.array_equal(world["values"], before) and a["values"] is not world["values"]
    assert [p["outcome"] for p in a["paths"]] == [p["outcome"] for p in b["paths"]]


def test_only_named_series_and_whole_groups(world):
    w = sp.add(world, 1, "cycle", pairs=3, frac=0.25)
    v0, v1 = world["values"], w["values"]
    named = {x for p in w["paths"] for x in (p["outcome"], p["series"])}
    assert len(named) == 6 and set(w) == set(world) | {"paths", "_paths"}
    for s in range(v0.shape[0]):
        if s not in named:
            assert np.array_equal(v0[s], v1[s])
    for p in w["paths"]:
        m = p["places"]
        assert m.sum() == 15 and all(len(set(m[world["group"] == g])) == 1 for g in np.unique(world["group"]))
        for s in (p["outcome"], p["series"]):
            assert np.array_equal(v0[s][~m], v1[s][~m])
            assert (v0[s][m] != v1[s][m]).any(axis=1).all()


def test_no_truth_series_used(world):
    taken = {t["outcome"] for t in world["truth"]} | {s for t in world["truth"] for s, _ in t["inputs"]}
    for seed in range(8):
        w = sp.add(world, seed, "mixed", pairs=4)
        used = [x for p in w["paths"] for x in (p["outcome"], p["series"])]
        assert not taken & set(used) and len(set(used)) == 8
        assert all(world["role"][p["outcome"]] == "outcome" and world["role"][p["series"]] == "local"
                   for p in w["paths"])
    with pytest.raises(ValueError):
        sp.add(world, 0, "cycle", pairs=6)


@pytest.mark.parametrize("kind", sp.KINDS)
def test_outcome_and_series_carry_one_path(world, kind):
    w = sp.add(world, 2, kind, pairs=3)
    signs = set()
    for p, path in zip(w["paths"], w["_paths"]):
        a, b = added(world, w, p)
        assert np.allclose(a[p["places"]], path[p["places"]], atol=1e-9) and not path[~p["places"]].any()
        for x, y in zip(a[p["places"]], b[p["places"]]):
            assert np.corrcoef(x, y)[0, 1] == pytest.approx(p["sign"], abs=1e-6)
        signs.add(p["sign"])
    assert signs <= {-1, 1}


def test_signs_vary(world):
    signs = {p["sign"] for s in range(6) for p in sp.add(world, s, "cycle")["paths"]}
    assert signs == {-1, 1}


@pytest.mark.parametrize("kind", sp.KINDS)
def test_slow_and_sized(kind):
    big = tp.make(4, "steady", places=120)
    w = sp.add(big, 3, kind, pairs=2, frac=1.0)
    for strength in (1.0, 0.5):
        w2 = w if strength == 1.0 else sp.add(big, 3, kind, strength=0.5, pairs=2, frac=1.0)
        for p in w2["paths"]:
            a, b = added(big, w2, p)
            assert slow(a) < 0.15  # a path moves by under 15% of its range a year, typically
            for add_, s in ((a, p["outcome"]), (b, p["series"])):
                ratio = add_.std(axis=1) / big["values"][s].std(axis=1)
                assert np.median(ratio) == pytest.approx(1.5 * strength, abs=0.01)
                assert ratio.max() > 2 * np.median(ratio) * 0.99 and ratio.min() < 0.7 * np.median(ratio)


@pytest.mark.parametrize("kind", sp.KINDS)
def test_foreseeable_is_true_to_the_path(world, kind):
    w = sp.add(world, 7, kind, pairs=3, frac=1.0)
    miss = np.median([one_step_miss(path[p["places"]]) for p, path in zip(w["paths"], w["_paths"])])
    if sp.FORESEEABLE[kind]:
        assert miss < 0.1
    else:
        assert miss > 0.4


def test_mixed_uses_several_kinds(world):
    w = sp.add(world, 1, "mixed", pairs=2, frac=1.0)
    for p in w["paths"]:
        names = set(p["kinds"][p["places"]])
        assert len(names) >= 4 and names <= set(sp.KINDS) and not p["kinds"][~p["places"]].any()


def test_strength_zero_changes_nothing_and_nan_kept():
    gappy = tp.make(5, "steady", places=60, gaps=0.05)
    assert np.isnan(gappy["values"]).any()
    z = sp.add(gappy, 1, "mixed", strength=0.0)
    assert np.array_equal(z["values"], gappy["values"], equal_nan=True)
    w = sp.add(gappy, 1, "mixed")
    assert np.array_equal(np.isnan(w["values"]), np.isnan(gappy["values"]))
    assert not np.isnan(w["_paths"][0]).any()


def test_bad_kind(world):
    with pytest.raises(ValueError):
        sp.add(world, 1, "line")
