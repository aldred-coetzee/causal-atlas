"""Tests for the made-up tables generator (synth/table_panel.py)."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import table_panel as tp  # noqa: E402

SEEDS = (1, 2, 3)
LINKED = ("steady", "threshold", "extremes", "pair", "flip", "many", "hidden")


def r2(shock, sig):
    """Squared correlation of an outcome's shocks with a signal over the given place-years."""
    return np.corrcoef(shock.ravel(), sig.ravel())[0, 1] ** 2


def shares(w):
    """Per link: share of shock variance the signal accounts for, in linked and in unlinked places."""
    inside, outside = [], []
    for t, sig in zip(w["truth"], w["_signals"]):
        sh, pm = w["_shocks"][t["outcome"]], t["places"]
        inside.append(r2(sh[pm], sig[pm]))
        outside.append(r2(sh[~pm], sig[~pm]))
    return inside, outside


def test_deterministic():
    a, b, c = (tp.make(s, "steady") for s in (5, 5, 6))
    assert a["values"].tobytes() == b["values"].tobytes()
    assert not np.array_equal(a["values"], c["values"])


def test_shapes_and_roles():
    w = tp.make(1, "steady")
    assert w["values"].shape == (40, 120, 60)
    assert list(w["role"][:8]) == ["outcome"] * 8 and list(w["role"][-8:]) == ["shared"] * 8
    assert len(w["truth"]) == 3 and len({t["outcome"] for t in w["truth"]}) == 3
    assert all(t["places"].sum() == 30 for t in w["truth"])


@pytest.mark.parametrize("kind", LINKED)
@pytest.mark.parametrize("share", (0.2, 0.35))
def test_link_share(kind, share):
    ins, outs = [], []
    for s in SEEDS:
        i, o = shares(tp.make(s, kind, share=share))
        ins += i
        outs += o
    assert abs(np.mean(ins) - share) < 0.06
    assert np.mean(outs) < 0.02


def test_unlinked_outcomes_show_no_signal():
    w = tp.make(2, "steady")
    linked = {t["outcome"] for t in w["truth"]}
    free = [o for o in range(8) if o not in linked]
    for o in free:
        assert r2(w["_shocks"][o], w["_signals"][0]) < 0.01


def test_shock_variance_unchanged():
    w = tp.make(3, "steady", rough=0, nuisance=0)
    t = w["truth"][0]
    assert abs(w["_shocks"][t["outcome"]][t["places"]].var() - 1) < 0.1


def test_same_year():
    ins, lag = [], []
    for s in SEEDS:
        w = tp.make(s, "same_year")
        for t, sig in zip(w["truth"], w["_signals"]):
            assert not t["predicts"] and not t["changes"]
            pm, sh = t["places"], w["_shocks"][t["outcome"]]
            ins.append(r2(sh[pm], sig[pm]))
            x = w["_shocks"][t["inputs"][0][0]]  # the input's own shock, one year earlier
            lag.append(r2(sh[pm][:, 1:], x[pm][:, :-1]))
    assert abs(np.mean(ins) - 0.35) < 0.06
    assert np.mean(lag) < 0.01


def test_none():
    w = tp.make(4, "none")
    assert w["truth"] == []
    sh = w["values"][w["role"] == "shared"]
    assert (sh == sh[:, :1, :]).all()
    assert np.bincount(w["group"]).tolist() == [5] * 24


def test_flags_and_truth():
    for kind in LINKED:
        t = tp.make(1, kind)["truth"][0]
        assert t["predicts"] and t["changes"] == (kind in ("steady", "threshold", "extremes", "pair", "flip"))
    assert len(tp.make(1, "many")["truth"][0]["inputs"]) == 20
    w = tp.make(1, "flip")
    sg = w["truth"][0]["sign"][w["truth"][0]["places"]]
    assert (sg == 1).sum() == (sg == -1).sum()
    assert tp.make(1, "flip", flip="state")["truth"][0]["state"] >= 32


def test_shared_source():
    w = tp.make(1, "pair", source="shared")
    assert all(w["role"][s] == "shared" for t in w["truth"] for s, _ in t["inputs"])


@pytest.mark.parametrize("kind", ("steady", "threshold", "extremes", "pair", "flip"))
def test_truth_states_the_signal(kind):
    """With roughness and nuisances off, the signal rebuilt from the stored inputs and truth matches."""
    w = tp.make(1, kind, rough=0, nuisance=0, flip="state" if kind == "flip" else "place")
    t = w["truth"][0]
    zs = [(w["values"][s] - c[:, None]) / sp[:, None]
          for (s, _), c, sp in zip(t["inputs"], t["input_centre"], t["input_spread"])]
    z = zs[0][:, :-1]
    if kind == "steady":
        mine = z
    elif kind == "threshold":
        mine = np.maximum(z - t["level"][:, None], 0)
    elif kind == "extremes":
        mine = (z > t["level"][:, None]).astype(float)
    elif kind == "pair":
        mine = z * zs[1][:, :-1]
    else:
        st = w["values"][t["state"]]
        mine = z * np.where(st >= st.mean(axis=1, keepdims=True), 1, -1)[:, :-1]
    sig = w["_signals"][0][:, 1:]
    pm = t["places"]
    assert np.corrcoef(mine[pm].ravel(), sig[pm].ravel())[0, 1] > 0.95


def test_no_heavy_tail_no_drift_when_off():
    w = tp.make(1, "none", rough=0, nuisance=0)
    sh = w["_shocks"][8:32].ravel()
    k = ((sh - sh.mean()) ** 4).mean() / sh.var() ** 2
    assert abs(k - 3) < 0.2
    rough = tp.make(1, "none", rough=1, nuisance=0)["_shocks"][8:32].ravel()
    assert ((rough - rough.mean()) ** 4).mean() / rough.var() ** 2 > 3.5

    def drift(v):
        x = v[:32]
        a = x[:, :, :10].mean(axis=2) - x[:, :, -10:].mean(axis=2)
        return np.mean(np.abs(a) / x.std(axis=2))
    assert drift(w["values"]) < 0.8 * drift(tp.make(1, "none", rough=0, nuisance=1)["values"])


def test_gaps():
    w = tp.make(1, "steady", gaps=0.05)
    v, role = w["values"], w["role"]
    assert abs(np.isnan(v[role != "shared"]).mean() - 0.05) < 0.005
    assert not np.isnan(v[role == "shared"]).any()
    assert not np.isnan(tp.make(1, "steady")["values"]).any()
