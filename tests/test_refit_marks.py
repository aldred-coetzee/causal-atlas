"""The marks' counting, on made-up rows. See results/refit-marks.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_refit_marks as m  # noqa: E402


def first(panel, seed, inputs="real", skill=0.0, low=-0.001):
    return dict(stage="first", panel=panel, seed=seed, inputs=inputs, skill=skill, ci=[low, 0.05])


def quiet_rows(skill=0.0):
    return [first(p, s, k, skill) for p in m.NULLS for s in m.SEEDS for k in ("real", "noise")]


def shuffles(panel, seed, value=0.0):
    return dict(stage="shuffled", panel=panel, seed=seed, inputs="real", circular=[value] * 32, permutation=[value] * 19)


def test_a_needs_every_panel_and_kind():
    rows = quiet_rows()
    assert m.outcome(rows)["a_pass"]
    assert not m.outcome(rows[:-1])["a_pass"]
    for x in rows:
        if x["panel"] == "combo_null" and x["inputs"] == "noise" and x["seed"] <= 3003:
            x["skill"] = 0.006
    out = m.outcome(rows)
    assert out["quiet"]["combo_null noise"] == 17 and not out["a_pass"]


def test_b_passes_only_with_shuffles_and_few_false_positives():
    rows = quiet_rows() + [first(m.PLANTED, s, skill=0.05, low=0.01) for s in m.SEEDS]
    assert m.outcome(rows)["chosen"] is None
    rows += [shuffles(m.PLANTED, s) for s in m.SEEDS]
    assert m.outcome(rows)["chosen"] == "circular"
    for s in (3001, 3002):
        rows.append(shuffles("shared_null", s))
        x = next(x for x in rows if x["stage"] == "first" and x["panel"] == "shared_null" and x["seed"] == s and x["inputs"] == "real")
        x["skill"], x["ci"] = 0.05, [0.01, 0.06]
    assert m.outcome(rows)["chosen"] is None


def test_shuffles_above_or_median_fail_detection():
    rows = quiet_rows() + [first(m.PLANTED, s, skill=0.05, low=0.01) for s in m.SEEDS]
    rows += [shuffles(m.PLANTED, s, 0.06 if s <= 3005 else 0.0) for s in m.SEEDS]
    assert m.outcome(rows)["schemes"]["circular"]["hears"] == 15


def test_to_shuffle_follows_the_rule():
    rows = quiet_rows() + [first(m.PLANTED, s, skill=0.05 if s <= 3015 else 0.0, low=0.01) for s in m.SEEDS]
    jobs = m.to_shuffle(rows)
    assert len(jobs) == 12 and (m.PLANTED, 3003) in jobs and (m.PLANTED, 3004) not in jobs
    rows = quiet_rows() + [first(m.PLANTED, s, skill=0.05 if s <= 3016 else 0.0, low=0.01) for s in m.SEEDS]
    assert len([j for j in m.to_shuffle(rows) if j[0] == m.PLANTED]) == 16
