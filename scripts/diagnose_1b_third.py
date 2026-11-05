"""Development only, spent seeds: why g1 falls short of what the planted effect is worth. The linked column is the generator's truth, for diagnosis; it never enters the detector."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "synth"))
import generate as synth  # noqa: E402

from causal_atlas import detector as d, nested as n  # noqa: E402
from causal_atlas.panel import load  # noqa: E402

FIRST, LAST_TRAIN, SCORED = 36, 194, 195


def one(panel, seed):
    _, lat, lon = load()
    g = synth.generate(panel, lat, lon, seed)
    y, drought, oni = g["y"], g["drought"], g["oni"]
    cells, T = y.shape
    tau = np.arange(FIRST, T)
    target = y[:, tau].ravel().astype(float)
    month = np.tile(tau, cells)
    fit = month <= LAST_TRAIN
    raw = d.fit_predict(d.base_features(y, lat, lon), target.astype(np.float32), fit, np.ones(len(target), bool)).astype(float)
    full = np.zeros((cells, T))
    full[:, FIRST:] = raw.reshape(cells, len(tau))
    b = np.maximum(raw * n.level_factor(y, full, lat, lon, FIRST)[:, FIRST:].ravel(), n.FLOOR)
    where = np.repeat(np.stack([lat, lon], axis=1), len(tau), axis=0).astype(np.float32)
    plain = lambda r: np.hstack([where, np.log(r)[:, None].astype(np.float32)])
    r = n.apply_trees(plain(b), target, b, fit, 40)
    inputs = d.input_features(drought, oni, train_months=(FIRST, LAST_TRAIN))
    x = np.hstack([plain(r), inputs])
    linked = g["linked"].any(axis=1) if g["linked"].ndim > 1 else g["linked"]
    oracle = np.hstack([x, np.repeat(linked.astype(np.float32), len(tau))[:, None]])
    score = month >= SCORED
    obs, ref = target[score].reshape(cells, -1), r[score].reshape(cells, -1)
    a, c = synth.lead_rates(panel, lat, lon, seed, lead=3)
    i = np.arange(SCORED, T)
    out = dict(seed=seed, worth=float(d.skill(y[:, i], a[:, i], c[:, i])))
    truth, none = a[:, i], c[:, i]
    q = truth / none
    def cell_dev(mu):
        t = np.zeros_like(mu)
        pos = obs > 0
        t[pos] = obs[pos] * np.log(obs[pos] / mu[pos])
        return 2 * (t - (obs - mu))
    gain = cell_dev(none) - cell_dev(truth)
    order = np.sort(gain.ravel())[::-1]
    total = gain.sum()
    by_month, by_cell = np.sort(gain.sum(axis=0))[::-1], np.sort(gain.sum(axis=1))[::-1]
    big = q > 1.5
    train_i = np.arange(FIRST, LAST_TRAIN + 1)
    out.update(
        ratio_quantiles=[round(float(v), 2) for v in np.quantile(q, [.5, .9, .95, .99, .999, 1])],
        gain_share_top_1000_cell_months=round(float(order[:1000].sum() / total), 3),
        gain_share_top_12_months=round(float(by_month[:12].sum() / total), 3),
        gain_share_top_50_cells=round(float(by_cell[:50].sum() / total), 3),
        where_big_median=dict(truth=round(float(np.median(truth[big])), 3), none=round(float(np.median(none[big])), 3), ref=round(float(np.median(ref[big])), 3)),
        months_with_big=[int((a[:, train_i] / c[:, train_i] > 1.5).any(axis=0).sum()), int(big.any(axis=0).sum())],
        excess_events=[round(float((a - c)[:, train_i].sum())), round(float((truth - none).sum()))],
        events=[round(float(y[:, train_i].sum())), round(float(obs.sum()))],
        in_sample_inputs_t100=round(float(d.skill(obs, n.apply_trees(x, target, r, score, 100)[score].reshape(cells, -1), ref)), 4),
        in_sample_big_t300=None,
    )
    base = dict(n.G_SETTINGS)
    n.G_SETTINGS.update(max_leaf_nodes=31, min_samples_leaf=50, l2_regularization=1)
    out["in_sample_big_t300"] = round(float(d.skill(obs, n.apply_trees(x, target, r, score, 300)[score].reshape(cells, -1), ref)), 4)
    n.G_SETTINGS.clear()
    n.G_SETTINGS.update(base)
    return out


if __name__ == "__main__":
    with (ROOT / "results" / "1b-third-dev-diagnostic-3.jsonl").open("a") as f:
        for s in (1011, 1016, 1017):
            line = json.dumps(one("planted_3.00", s))
            print(line, flush=True)
            f.write(line + "\n")
