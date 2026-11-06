import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from causal_atlas import detector as d, twin as w
from run_r1 import CALIBRATED, FALSE_GAIN_COUNT, FALSE_GAIN_SEEDS, PLANTED, choose_trees, false_gain_years, gate, jobs

FRESH = [range(5001, 5021), range(5101, 5121), range(5201, 5221), range(5301, 5321), range(6001, 7000)]


def world(cells=60, seed=0):
    rng = np.random.default_rng(seed)
    lat = np.repeat(np.arange(cells // 6) * 5.25, 6)[:cells]
    lon = np.tile(np.arange(6) * 5.25, cells // 6 + 1)[:cells]
    y = rng.poisson(0.3 * rng.gamma(1, 1, (cells, 1)), (cells, 435))
    return y, lat, lon, w.blocks_of(lat, lon)


def test_level_cannot_inflate():
    y, _, _, block = world()
    sched = [(195, 218), (219, 242)]
    rng = np.random.default_rng(1)
    r = rng.gamma(2, 0.2, y.shape) + 0.01
    m = rng.gamma(2, 0.2, y.shape) + 0.01
    plain = w.level_free(y, m, r, block, sched, interval=False)["S"]
    worse = r.copy()
    k = rng.uniform(0.01, 143, block.max() + 1)
    worse[:, 195:219] *= k[block][:, None]
    worse[:, 219:243] *= 37.0
    assert abs(w.level_free(y, m, worse, block, sched, interval=False)["S"] - plain) < 1e-10


def test_block_with_no_events_scores_nothing_and_a_near_zero_forecast_is_finite():
    y, _, _, block = world()
    y = y.copy()
    y[block == 0] = 0
    r = np.full(y.shape, 0.2)
    assert np.allclose(w.rescaled(y, r, block, [(195, 218)])[block == 0], 0)
    y[block == 1, 200] = 3
    tiny = np.where(block[:, None] == 1, 1e-3, 0.2) * np.ones(y.shape)
    assert np.isfinite(w.level_free(y, tiny, r, block, [(195, 218)], interval=False)["S"])


def test_cap_is_never_zero_and_uses_the_past_only():
    y = np.zeros((4, 20), int)
    block = np.array([0, 0, 1, 1])
    y[0, 5], y[2, 15] = 7, 9
    cap = w.cell_cap(y, block, 10)
    assert cap.tolist() == [14, 14, 1, 1]
    assert (w.bounded(np.array([np.nan, 1e9, 0.0]), np.array([2.0, 2.0, 2.0])) == [2.0, 2.0, 1e-3]).all()


def test_blown_flags_a_total_over_five_times_the_trailing_months():
    y = np.zeros((2, 100))
    y[:, 40:50] = 1  # 20 events in the 24 months to 58
    f = np.zeros((2, 100))
    f[:, 61:85] = 3.0
    assert w.blown(f, y, 61, 84)
    f[:, 61:85] = 1.0
    assert not w.blown(f, y, 61, 84)


def test_a_forecast_of_a_real_surge_is_not_blown():
    y = np.zeros((2, 100))
    y[:, 40:50] = 1
    y[:, 61:85] = 3  # 144 events, more than 5 times the 20 before
    f = np.zeros((2, 100))
    f[:, 61:85] = 3.0
    assert not w.blown(f, y, 61, 84)
    f[:, 61:85] = 3.0 * 143
    assert w.blown(f, y, 61, 84)


def test_twins_are_the_same_when_the_inputs_carry_nothing():
    y, lat, lon, _ = world()
    refs = w.references(y, lat, lon, schedule=[(195, 218)], trees=(5, 10))
    m = w.test_panel(refs, np.zeros(y.shape), np.zeros(435))
    for t in (5, 10):
        assert np.array_equal(m[t][:, 195:219], refs["R"][t][:, 195:219])


def test_the_booster_at_a_stage_is_the_booster_of_that_size():
    y, lat, lon, _ = world()
    a = w.references(y, lat, lon, schedule=[(195, 218)], trees=(5, 10))["R"][5]
    b = w.references(y, lat, lon, schedule=[(195, 218)], trees=(5,))["R"][5]
    assert np.allclose(a[:, 195:219], b[:, 195:219])


def test_a_shift_keeps_calendar_month_in_every_value():
    t = np.arange(435)
    for k in range(1, 33):
        moved = d.circular_shift(t, k)
        assert (moved % 12 == t % 12).all()
        assert moved.max() < 432


def test_the_false_gain_shifts_are_the_eight_named():
    assert sum(len(false_gain_years(s)) for s in FALSE_GAIN_SEEDS) == FALSE_GAIN_COUNT


def test_fresh_seeds_are_unspent():
    spent = set()
    for f in (ROOT / "results").glob("*.jsonl"):
        spent |= {json.loads(x).get("seed") for x in f.read_text().splitlines()}
    assert not any(s in spent for r in FRESH for s in r)
    assert not any(s in r for r in FRESH for _, s in jobs())


def fake(panel, seed, S, ratio=1.0, shifts=()):
    return dict(panel=panel, seed=seed, inputs="real", shifts=[dict(S={"25": v, "50": v, "100": v}) for v in shifts],
                by_trees={str(t): dict(S=S, ratio_r=ratio) for t in (25, 50, 100)})


def full(ratio=1.0, shift=0.0, s=0.05):
    rows = [fake(p, n, s, ratio, [shift] * (6 if n == 3007 else 2 if n == 3010 else 0) if p == PLANTED else ()) for p, n in jobs()]
    return rows


def test_gate():
    assert gate(full()[:-1])["verdict"] == "incomplete"
    assert gate(full())["verdict"] == "go on"
    assert gate(full(ratio=3.0))["verdict"] == "stop"
    assert gate(full(shift=0.03))["verdict"] == "stop"
    assert gate(full(s=-0.01))["verdict"] == "stop"


def test_choose_trees():
    rows = full()
    assert choose_trees(rows) == 25
    for x in rows:
        if x["panel"] == PLANTED and x["seed"] in CALIBRATED:
            x["by_trees"]["25"]["S"] = 0.01
    assert choose_trees(rows) == 50
