"""The second count's harness (scripts/run_referee_b.py): what it sends is what it says it sends, and it reads the early years only where it chooses places."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_referee_b as rb  # noqa: E402

tp, sp = rb.table_panel, rb.shared_paths


def test_the_drift_pairs_are_the_ones_the_generator_plants():
    """With and without nuisances the same seed differs, in half the groups of places, by a smooth curve in exactly four series, and the same curve within each pair."""
    t = np.arange(60.0)
    x = np.stack([np.ones(60), t, t * t], axis=1)
    for seed, kind in ((32801, "none"), (32802, "same_year"), (32803, "steady")):
        d = tp.make(seed, kind, nuisance=3.0)["values"] - tp.make(seed, kind, nuisance=0.0)["values"]
        smooth = np.zeros(d.shape[:2], bool)
        for s in range(len(d)):
            left = d[s].T - x @ np.linalg.lstsq(x, d[s].T, rcond=None)[0]
            smooth[s] = (left.var(axis=0) < 0.02 * d[s].var(axis=1)) & (d[s].var(axis=1) > 1e-6)
        share = smooth.mean(axis=1)
        pairs = rb.drift_pairs(seed)
        assert {s for s in range(len(d)) if 0.25 < share[s] < 0.6} == {s for p in pairs for s in p}

        def together(a, b):
            """How closely two series' curves go together over the years, in the middle place of those where both have one."""
            both = smooth[a] & smooth[b]
            return np.median([abs(np.corrcoef(d[a, p], d[b, p])[0, 1]) for p in np.flatnonzero(both)])

        (o1, s1), (o2, s2) = pairs
        assert min(together(o1, s1), together(o2, s2)) > 0.9999 > max(together(o1, s2), together(o2, s1))  # one curve a pair; the two pairs are in the same places with curves of their own


def test_the_places_named_for_a_pair_come_from_the_early_years_alone():
    w = tp.make(32804, "none")
    v = w["values"]
    later = v.copy()
    later[:, :, rb.FIRST:] = np.random.default_rng(1).standard_normal(later[:, :, rb.FIRST:].shape)
    for a, b in zip(rb.sets(v, w["group"], 0, 9), rb.sets(later, w["group"], 0, 9)):
        assert np.array_equal(a, b)
    quarter, half = rb.sets(v, w["group"], 0, 9)
    assert quarter.sum() == 30 and half.sum() == 60 and (quarter & ~half).sum() == 0
    assert all(len(set(x[w["group"] == g])) == 1 for x in (quarter, half) for g in np.unique(w["group"]))


def test_a_world_is_forty_proposals_and_says_what_each_was(monkeypatch):
    monkeypatch.setattr(rb.rf, "DRAWS", 60)  # the shape of a row, not its numbers
    r = rb.world("none", 32805)
    assert r["sent"] == rb.SENT and [(a["of"], a["way"]) for a in r["direct"]] == [(i, w) for i in (0, 1) for w in ("all", "claim", "quarter", "half")] and not r["answers"]
    assert sum(k["sent"] for k in r["keen"].values()) == rb.SENT - 8
    r = rb.world("path_mixed", 32806)
    assert [a["way"] for a in r["direct"]].count("true") == 2 and [a["way"] for a in r["direct"]].count("back") == 2 and len(r["direct"]) == 12
    r = rb.world("steady_35", 32807)
    assert [a["way"] for a in r["answers"]] == ["true", "all", "claim", "back"] * 3 and not r["direct"]
    json_safe = __import__("json").dumps(r)
    assert json_safe


def test_the_limit_a_rate_of_one_in_twenty_rarely_passes():
    assert [rb.at_most(n) for n in (20, 40, 50, 60, 100, 120)] == [3, 5, 6, 6, 9, 11]


def test_seeds_are_fresh_and_no_panel_shares_one():
    seeds = [s for _, _, r in rb.PANELS.values() for s in r]
    assert len(seeds) == len(set(seeds)) and min(seeds) >= 33001 and not set(seeds) & set(rb.SMOKE)
    assert len(rb.FORESEEN) == 6 and all(rb.PANELS[n][1] for n in rb.FORESEEN)
