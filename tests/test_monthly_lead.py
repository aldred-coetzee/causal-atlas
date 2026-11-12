"""The second monthly count's two new pieces: gaps in a made-up table, and a pass kept as a lead only where its label does not say the two move together. Made-up numbers only."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import run_monthly as rm  # noqa: E402
import run_monthly_lead as ml  # noqa: E402


def test_its_own_file_and_unused_seeds():
    assert ml.OUT.name == "monthly-lead-count.jsonl" and rm.OUT.name == "monthly-count.jsonl"
    seeds = {s for _, _, first, _ in ml.PANELS.values() for s in range(first, first + 99)}
    assert min(seeds) >= 65001 and max(seeds) <= 65999
    assert len(seeds) == 99 * len(ml.PANELS)


def test_gaps_only_take_values_away_and_are_the_same_each_time():
    v = np.random.default_rng(0).normal(size=(6, 30, 600))
    a, b = ml.gaps(v, 5), ml.gaps(v, 5)
    np.testing.assert_array_equal(a, b)
    there = np.isfinite(a)
    np.testing.assert_array_equal(a[there], v[there])
    assert 0.04 < 1 - there.mean() < 0.15
    assert np.isfinite(v).all()
    late = ~there[:, :, 0] & there[:, :, 130:].any(axis=2)
    assert 0.2 < late.mean() < 0.5


def test_a_lead_is_a_pass_not_labelled_together():
    res = {"passed": 4, "proposals": [{"passes": True, "label": {"together": False}}, {"passes": True, "label": {"together": True}}, {"passes": True, "label": None}, {"passes": False, "label": None}, {"passes": True}]}
    out = ml.leads(res)
    assert [p["passes"] for p in out["proposals"]] == [True, False, False, False, False] and out["passed"] == 1
    assert res["proposals"][1]["passes"] and res["passed"] == 4
