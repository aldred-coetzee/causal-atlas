"""Reading by month (causal_atlas.months) and what it changed in the finders and the referee: the season step uses earlier dates alone; the whole-year draw takes a year's months together; the month settings hold for a read and are put back after it; and every yearly read is as counted.

The last is shown twice. Quickly, on worlds made in the test: the finders' board and the referee's judgement from the code as it stands are set beside those from the code as it was counted (COUNTED, read from git), field for field. Slowly, when CA_COUNTED is set (a number of worlds, or "all"): the registered worlds of the finders' count (results/finders-stage-a2.jsonl) are read again and must give the stored rows exactly. Neither writes anything."""
import importlib
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from causal_atlas import finders as fd
from causal_atlas import months as mo
from causal_atlas import referee as rf

ROOT = Path(__file__).resolve().parents[1]
COUNTED = "269b5d8"  # the last commit that changed finders.py or referee.py before the monthly read: the code the yearly counts ran on
PLACES, YEARS, FIRST = 60, 45, 28
GROUP = np.repeat(np.arange(PLACES // 5), 5)


def yearly(seed, share=0.4):
    """A small yearly world: series 0 and 1 outcomes; series 2 a year before moves series 0 in a third of the places; series 7 the same everywhere."""
    rng = np.random.default_rng(seed)
    v = rng.standard_normal((8, PLACES, YEARS))
    v[7] = v[7][:1]
    before = np.concatenate([np.zeros((8, PLACES, 1)), v[:, :, :-1]], axis=2)
    where = (GROUP < 4)[:, None]
    v[0] = np.where(where, np.sqrt(1 - share) * v[0] + np.sqrt(share) * before[2], v[0])
    return v


def plain(x):
    """A board row or a judgement as plain values, so that two can be compared exactly; nan equal to nan."""
    if isinstance(x, dict):
        return {k: plain(y) for k, y in x.items()}
    if isinstance(x, (list, tuple)):
        return [plain(y) for y in x]
    if isinstance(x, (frozenset, set)):
        return sorted(x)
    if isinstance(x, np.ndarray):
        return plain(x.tolist())
    if isinstance(x, (float, np.floating)):
        return "nan" if math.isnan(x) else float(x)
    if isinstance(x, np.integer):
        return int(x)
    return x


@pytest.fixture(scope="module")
def counted(tmp_path_factory):
    """The finders and the referee as counted, read from git into a package of their own, the finders importing that referee."""
    d = tmp_path_factory.mktemp("counted") / "counted_atlas"
    d.mkdir()
    try:
        for name in ("referee", "finders"):
            src = subprocess.run(["git", "-C", str(ROOT), "show", f"{COUNTED}:src/causal_atlas/{name}.py"], capture_output=True, text=True, check=True).stdout
            (d / f"{name}.py").write_text(src.replace("from causal_atlas import referee as rf", "from counted_atlas import referee as rf"))
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("the counted code cannot be read from git here")
    (d / "__init__.py").write_text("")
    sys.path.insert(0, str(d.parent))
    try:
        yield importlib.import_module("counted_atlas.finders"), importlib.import_module("counted_atlas.referee")
    finally:
        sys.path.remove(str(d.parent))
        for k in [k for k in sys.modules if k.startswith("counted_atlas")]:
            del sys.modules[k]


def read_with(f, r, v, seed):
    board = f.swarm(f.view(v, GROUP, FIRST, [0, 1]))
    rows = f.steward(board)
    floorless = f.steward(board, sent=20, share=4, floor=-np.inf)
    return board, rows, r.judge(v, GROUP, FIRST, [f.proposal(x) for x in rows], seed=seed), r.judge(v, GROUP, FIRST, [f.proposal(x) for x in floorless], seed=seed, shifts=(3,))


@pytest.mark.parametrize("seed", [11, 12, 13])
def test_a_yearly_board_and_judgement_are_as_counted(counted, seed):
    v = yearly(seed)
    now, then = read_with(fd, rf, v, seed), read_with(*counted, v, seed)
    for a, b in zip(now, then):
        assert plain(a) == plain(b)
    assert now[2]["passed"] > 0  # the link is heard, so a pass and its label were compared too


@pytest.mark.parametrize("seed", [11, 12])
def test_errors_made_again_when_asked_give_the_same_judgement_as_errors_kept(seed):
    """LAZY changes only where an outcome's errors live, not what they are: the past step by step, and the whole judgement with its labels, are the same to the last bit."""
    v = yearly(seed)
    rows = fd.steward(fd.swarm(fd.view(v, GROUP, FIRST, [0, 1])))
    kept = rf.judge(v, GROUP, FIRST, [fd.proposal(x) for x in rows], seed=seed, shifts=(3,))
    made = rf.judge(v, GROUP, FIRST, [fd.proposal(x) for x in rows], seed=seed, shifts=(3,), settings={"LAZY": True})
    assert plain(kept) == plain(made) and kept["passed"] > 0
    for event in (None, 0.8):
        a = rf.outcome(v[0], GROUP, FIRST, event)
        with rf.using({"LAZY": True}):
            z = rf.outcome(v[0], GROUP, FIRST, event)
        assert isinstance(a["past"], list) and not isinstance(z["past"], list)
        assert len(a["past"]) == len(z["past"]) == YEARS - FIRST
        for x, y in zip(a["past"], z["past"]):
            for p, q in zip(x, y):
                assert np.array_equal(p, q, equal_nan=True)

def test_the_settings_are_put_back_after_a_read_and_after_a_failure():
    before = {k: getattr(rf, k) for k in rf.SETTINGS} | {"_level": rf._level}
    with rf.using(mo.MONTHLY, level=fd.level):
        assert rf.WARM == mo.MONTHLY["WARM"] and rf._level is fd.level
    with pytest.raises(ZeroDivisionError), rf.using(mo.MONTHLY):
        1 / 0
    assert {k: getattr(rf, k) for k in rf.SETTINGS} | {"_level": rf._level} == before
    with pytest.raises(ValueError):
        with rf.using({"DRAWS": 3}):
            pass


def test_the_season_step_uses_earlier_years_only_and_removes_a_fixed_season():
    rng = np.random.default_rng(3)
    season = 5 * np.cos(2 * np.pi * np.arange(120) / 12)
    v = season + rng.standard_normal((4, 120))
    d = mo.season_out(v)
    assert np.isnan(d[:, :24]).all() and np.isfinite(d[:, 24:]).all()
    changed = v.copy()
    changed[:, 60:] += 100
    assert np.array_equal(mo.season_out(changed)[:, :60], d[:, :60], equal_nan=True)
    assert abs(np.corrcoef(d[0, 24:], season[24:])[0, 1]) < 0.2


def test_the_whole_year_draw_takes_a_years_months_together():
    cg, cy = mo.whole_years(36)(10, 48, 50, 1)
    assert cg.shape == (50, 10) and (cg.sum(axis=1) == 10).all()
    assert cy.shape == (50, 48) and (cy.reshape(50, 4, 12) == cy[:, ::12, None]).all() and (cy[:, ::12].sum(axis=1) == 4).all()


def test_a_monthly_read_hears_a_link_at_four_months_and_passes_nothing_where_nothing_predicts():
    rng = np.random.default_rng(5)
    S, P, T = 6, 60, 480
    group = np.repeat(np.arange(P // 5), 5)
    season = 2 * np.cos(2 * np.pi * (np.arange(T) - rng.uniform(0, 12, (S, 1, 1))) / 12)
    e = rng.standard_normal((S, P, T))
    x = np.zeros_like(e)
    for t in range(1, T):
        x[..., t] = 0.6 * x[..., t - 1] + 0.8 * e[..., t]
    null = x + season
    _, _, res = mo.read(null, group, 288, [0], seed=1, labels=False)
    assert res["passed"] == 0
    linked = null.copy()
    linked[0, :30, 4:] += 0.8 * x[3, :30, :-4]
    _, rows, res = mo.read(linked, group, 288, [0], seed=1, labels=False)
    heard = [r for r, q in zip(rows, res["proposals"]) if q["passes"]]
    assert heard and all(r["names"] == {3} for r in heard)


def counted_rows():
    n = os.environ.get("CA_COUNTED")
    if not n:
        return []
    rows = [json.loads(s) for s in open(ROOT / "results" / "finders-stage-a2.jsonl")]
    return rows if n == "all" else rows[:: max(1, len(rows) // int(n))][: int(n)]


@pytest.mark.parametrize("row", counted_rows(), ids=lambda r: f"{r['panel']}-{r['seed']}")
def test_a_counted_world_read_again_gives_its_stored_rows(row):
    """Slow, and only when CA_COUNTED is set: a registered world of the finders' count read again with the code as it stands."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import run_finders as rfi

    _, _, how, path, _ = rfi.PANELS[row["panel"]]
    again = json.loads(json.dumps(rfi.world(how, path, row["seed"])))
    for part in ("board", "first", "told", "ranks", "posted"):
        assert again.get(part) == row.get(part), part
