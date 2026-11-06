import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from causal_atlas import detector as d, screen as c
from run_r2 import HEARS_LEAST, NULLS, PLANTED, choose_form, early_stop, mark, names_true, spent_jobs


def test_a_column_ends_at_the_forecast_origin_and_never_later():
    x = np.zeros((1, 435))
    x[0, 100] = 1.0  # one value away from its calendar mean is enough to trace
    months = np.arange(36, 435)
    found = np.stack(list(c.columns(x, months)))[:, 0]
    i = 0
    for g in c.GAPS:
        for width in c.WIDTHS:
            lit = months[np.abs(found[i]) > 0.5 / width]
            assert lit.min() == 100 + d.LEAD + g
            assert lit.max() == 100 + d.LEAD + g + width - 1
            i += 1


def test_the_anomaly_uses_months_before_195_only():
    x = np.ones((2, 435))
    x[:, 195:] = 50
    a = c.anomaly(x)
    assert np.allclose(a[:, :195], 0)
    assert np.allclose(a[:, 195:], 49)


def test_gridded_and_global_give_the_same_statistic_for_the_same_values():
    rng = np.random.default_rng(0)
    months = np.arange(195, 291)
    block = np.repeat(np.arange(4), 3)
    y = rng.poisson(1.0, (12, 435))
    rstar = rng.gamma(2, 0.5, (12, 96))
    v = rng.normal(size=435)
    a = c.table([v], y, rstar, block, months, shifts=(1, 2))
    b = c.table([np.tile(v, (12, 1))], y, rstar, block, months, shifts=(1, 2))
    assert np.allclose(a, b, rtol=1e-4)


def test_count_cap_limits_one_huge_month():
    months = np.arange(195, 291)
    block = np.zeros(4, int)
    y = np.zeros((4, 435), int)
    y[0, 200] = 609
    capped = y.copy()
    capped[0, 200] = 20
    rstar = np.full((4, 96), 0.1)
    v = np.random.default_rng(0).normal(size=435)
    assert np.allclose(c.table([v], y, rstar, block, months, shifts=(1,)), c.table([v], capped, rstar, block, months, shifts=(1,)))


def test_gate_names_a_clear_column_steps_down_and_stays_quiet_otherwise():
    rng = np.random.default_rng(1)
    t = rng.normal(100, 5, (80, 33))
    leads, top, _ = c.gate(t)
    assert len(top) == c.K
    t[7, 0] = 500
    leads, top, _ = c.gate(t)
    assert leads[0] == 7 and top[0] == 7
    t = rng.normal(100, 5, (80, 33))
    t[:, 1] = t[:, 1] + 500  # one shift beats everything, so nothing can pass
    assert c.gate(t)[0] == []


def test_the_gate_fires_about_one_time_in_33_on_noise_of_any_shape():
    rng = np.random.default_rng(3)
    for draw in (lambda s: rng.normal(size=s), lambda s: rng.chisquare(1, s)):
        fired = sum(bool(c.gate(draw((320, 33)))[0]) for _ in range(300))
        assert fired <= 300 * 3 / 33


def test_a_planted_column_is_found_among_decoys():
    rng = np.random.default_rng(2)
    months = np.arange(195, 291)
    block = np.repeat(np.arange(4), 10)
    v, decoy = rng.normal(size=435), rng.normal(size=435)
    rate = np.exp(0.8 * v[months - d.LEAD])
    y = np.zeros((40, 435), int)
    y[:, months] = rng.poisson(rate, (40, 96))
    t = c.table([decoy, v], y, np.ones((40, 96)) * rate.mean(), block, months)
    leads, top, _ = c.gate(t[0])
    assert top[0] // c.PER_SERIES == 1
    assert leads and leads[0] == c.PER_SERIES  # gap 0, width 1 of the second series


def test_a_lead_is_true_only_in_the_worlds_own_series():
    assert names_true([0, 79])
    assert not names_true([80, 1279])
    assert not names_true([])


def fake(panel, seed, true=True, named=True, s=0.05, form="all"):
    leads = [0] if true else [80] if named else []
    score = dict(S=s, ci=[0.01, 0.1], raw=0.01, by_span=[0.1] * 4, blown=[])
    f = dict(leads=leads, top=leads, z=[3.0], named=named, true=true)
    return dict(panel=panel, seed=seed, form=form, forms={x: f for x in c.FORMS}, forced=score, gated=score if named else None)


def spent(planted_true=20):
    out = []
    for i, (p, s) in enumerate(spent_jobs()):
        out.append(fake(p, s, true=i < planted_true) if p == PLANTED else fake(p, s, true=False, named=False))
    return out


def test_early_stop():
    assert early_stop(spent()[:-1])["verdict"] == "incomplete"
    assert early_stop(spent())["verdict"] == "go on"
    assert early_stop(spent(HEARS_LEAST))["verdict"] == "go on"
    assert early_stop(spent(HEARS_LEAST - 1))["verdict"] == "stop"
    weak = spent()
    for x in weak:
        if x["panel"] == PLANTED:
            x["gated"] = dict(x["gated"], S=0.004)
    assert early_stop(weak)["verdict"] == "stop"
    noisy = spent()
    for x in [r for r in noisy if r["panel"] in NULLS][:3]:
        x["forms"] = {f: dict(leads=[80], top=[80], z=[3.0], named=True, true=False) for f in c.FORMS}
    assert early_stop(noisy)["verdict"] == "stop"


def test_choose_form_drops_a_noisy_form():
    rows = spent()
    assert choose_form(rows) == "all"
    for x in [r for r in rows if r["panel"] in NULLS][:3]:
        x["forms"] = dict(x["forms"], all=dict(leads=[80], top=[80], z=[3.0], named=True, true=False))
    assert choose_form(rows) == "largest"


def test_mark_is_the_second_largest_and_never_under_the_floor():
    rows = [fake("pure_null", 5001 + i, s=v) for i, v in enumerate([0.03, 0.01, 0.001])]
    assert mark(rows)["m"] == 0.01
    rows = [fake("pure_null", 5001 + i, s=v) for i, v in enumerate([0.03, 0.001, 0.001])]
    assert mark(rows)["m"] == 0.005
