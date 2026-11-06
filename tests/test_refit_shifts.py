import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_refit_shifts import CALIBRATED, OVERSHOT, reading, state


def row(seed, median):
    return dict(seed=seed, skill=0.1, shifts=[dict(skill=median)])


def test_state_edges():
    assert state(0.1, [0.05]) == "keeps"
    assert state(0.1, [0.025]) == "loses"
    assert state(0.1, [0.04]) == "between"
    assert state(0.1, [-0.01]) == "loses"


def test_reading():
    assert reading([row(s, 0.0) for s in OVERSHOT])["verdict"] == "incomplete"
    assert reading([row(s, 0.0) for s in OVERSHOT + CALIBRATED])["verdict"] == "margin"
    assert reading([row(s, 0.09) for s in OVERSHOT] + [row(s, 0.0) for s in CALIBRATED])["verdict"] == "baseline"
    assert reading([row(s, 0.0) for s in OVERSHOT] + [row(s, 0.09) for s in CALIBRATED])["verdict"] == "not hearing the link"
    assert reading([row(s, 0.04) for s in OVERSHOT + CALIBRATED])["verdict"] == "mixed"
