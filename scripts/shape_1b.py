"""Shape statistics for the synthetic generator's spec. Training months only, inputs not joined."""
import json
import sys
from pathlib import Path

import netCDF4
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from causal_atlas.panel import FIRST_MONTH, RAW, TRAIN_FIRST, VALID_FIRST, load


def autocorr(a, lag):
    x, z = a[:, :-lag].ravel().astype(float), a[:, lag:].ravel().astype(float)
    return float(np.corrcoef(x, z)[0, 1])


y, lat, lon = load()
tr = y[:, TRAIN_FIRST - FIRST_MONTH : VALID_FIRST - FIRST_MONTH]
out = {"cells": tr.shape[0], "train_months": tr.shape[1], "mean_events_per_cell_month": float(tr.mean())}
out["share_zero"] = float((tr == 0).mean())
out["variance_over_mean"] = float(tr.var() / tr.mean())
out["share_cells_ever_event"] = float((tr.sum(1) > 0).mean())
out["max_cell_month"] = int(tr.max())
out["lag1_autocorr"] = autocorr(tr, 1)
out["lag12_autocorr"] = autocorr(tr, 12)
s = np.sort(tr.ravel())[::-1]
out["share_events_in_top_1pct_cell_months"] = float(s[: len(s) // 100].sum() / s.sum())
out["share_events_in_top_0.1pct_cell_months"] = float(s[: len(s) // 1000].sum() / s.sum())
out["share_events_in_top_0.01pct_cell_months"] = float(s[: len(s) // 10000].sum() / s.sum())
cell_tot = np.sort(tr.sum(1))[::-1]
out["share_events_in_top_1pct_cells"] = float(cell_tot[: len(cell_tot) // 100].sum() / cell_tot.sum())

cal = (np.arange(tr.shape[1]) + TRAIN_FIRST) % 12
by_cal = np.array([tr[:, cal == c].sum() / (cal == c).sum() for c in range(12)])
out["seasonal_amplitude_peak_over_trough"] = float(by_cal.max() / by_cal.min())

# Spatial clustering: Moran's I of log cell totals over the 8-neighbour graph.
idx = {(a, o): i for i, (a, o) in enumerate(zip(lat, lon))}
z = np.log1p(tr.sum(1).astype(float))
z -= z.mean()
num = n_links = 0
for (a, o), i in idx.items():
    for da in (-0.5, 0, 0.5):
        for do in (-0.5, 0, 0.5):
            j = idx.get((a + da, o + do))
            if j is not None and j != i:
                num += z[i] * z[j]
                n_links += 1
out["morans_i_log_cell_totals"] = float(len(z) / n_links * num / (z @ z))

# Regional episodes: runs of months over twice a 5-degree block's own mean, in blocks with events.
block = (np.floor(lat / 5).astype(int) * 100 + np.floor(lon / 5).astype(int))
runs = []
for b in np.unique(block):
    series = tr[block == b].sum(0).astype(float)
    if series.sum() < 12:
        continue
    run = 0
    for hot in series > 2 * series.mean():
        if hot:
            run += 1
        elif run:
            runs.append(run)
            run = 0
    if run:
        runs.append(run)
runs = np.array(runs)
out["regional_blocks_5deg_with_events"] = int(np.sum([tr[block == b].sum() >= 12 for b in np.unique(block)]))
out["episode_months_median_p90_max"] = [float(np.median(runs)), float(np.percentile(runs, 90)), int(runs.max())]

# Inputs: SPEI anomalies and the ONI, on training months, no outcome involved.
nc = netCDF4.Dataset(str(RAW / "spei03.nc"))
t0 = 1901 * 12
ilat = np.searchsorted(nc["lat"][:], lat)
ilon = np.searchsorted(nc["lon"][:], lon)
sp = np.empty((len(lat), tr.shape[1]), dtype=float)
for k in range(tr.shape[1]):
    grid = nc["spei"][TRAIN_FIRST - t0 + k]
    sp[:, k] = np.ma.filled(grid[ilat, ilon].astype(float), np.nan)
for c in range(12):
    col = cal == c
    sp[:, col] -= np.nanmean(sp[:, col], axis=1, keepdims=True)
ok = ~np.isnan(sp).any(1)
q = sp[ok]
out["spei_anom_sd"] = float(q.std())
out["spei_lag1_autocorr"] = autocorr(q, 1)
out["spei_lag12_autocorr"] = autocorr(q, 12)
rng = np.random.default_rng(0)
pairs = rng.integers(0, len(q), (6000, 2))
ql, qo = lat[ok], lon[ok]
dist = np.hypot(ql[pairs[:, 0]] - ql[pairs[:, 1]], qo[pairs[:, 0]] - qo[pairs[:, 1]])
corr = np.array([np.corrcoef(q[i], q[j])[0, 1] for i, j in pairs])
out["spei_corr_by_distance_deg"] = {f"{lo}-{hi}": float(corr[(dist >= lo) & (dist < hi)].mean())
                                    for lo, hi in [(0, 2), (2, 5), (5, 10), (10, 20), (20, 40)]}
oni = {}
for line in (RAW / "oni.data").read_text().splitlines():
    parts = line.split()
    if len(parts) == 13 and parts[0].isdigit():
        for m, v in enumerate(parts[1:]):
            oni[int(parts[0]) * 12 + m] = float(v)
o = np.array([oni[m] for m in range(TRAIN_FIRST, VALID_FIRST)])
out["oni_sd"] = float(o.std())
out["oni_lag1_autocorr"] = float(np.corrcoef(o[:-1], o[1:])[0, 1])
out["oni_lag12_autocorr"] = float(np.corrcoef(o[:-12], o[12:])[0, 1])
print(json.dumps(out, indent=1))
