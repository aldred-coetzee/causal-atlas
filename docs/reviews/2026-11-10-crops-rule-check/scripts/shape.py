"""Item 8: the real panel's shape, yields only. The drought array in the cache is never read. Compared with one full-size made-up world (seed 26050). Run with python -I."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]  # the repo root; put in by the project session in place of an absolute path, before this file was committed
import sys, zipfile
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "docs/reviews/2026-11-10-crops-rule-check/scripts")]
import numpy as np
CEREALS = ("Wheat", "Maize (corn)", "Rice", "Barley", "Sorghum", "Millet")
path = str(ROOT / "data/panel/real/crops.npz")
z = np.load(path, allow_pickle=False)
logy, off, code, item = z["logy"], z["official"], z["code"], z["item"]  # 'x' is not touched
cer = np.isin(item, CEREALS)
FIRST, SC = 20, 25  # scored from year index 25 = 1986
def stats(logy, off, cer, code, label):
    o = ~cer
    print(f"== {label}: scored records {o.sum()}, beside {cer.sum()}, countries {len(np.unique(code[o]))}")
    ctry_no_cer = set(np.unique(code[o])) - set(np.unique(code[cer]))
    print("  countries with no cereal-like record:", len(ctry_no_cer), "; their scored records:", int(np.isin(code[o], list(ctry_no_cer)).sum()))
    per = np.array([np.sum(code[o] == c) for c in np.unique(code[o])]); print("  scored records per country: median", np.median(per), "max", per.max(), "min", per.min())
    so = off[o][:, SC:]; print("  official scored years per record: median", np.median(so.sum(1)), "p10", np.percentile(so.sum(1), 10), "share of records with <20:", round(float((so.sum(1) < 20).mean()), 3))
    fin = np.isfinite(logy[o][:, SC:]); print("  share of present figures 1986-2024 that are not official:", round(float(1 - so.sum() / fin.sum()), 3))
    d = np.diff(logy[o], axis=1); dd = d[:, SC - 1:]
    rep = np.sum(np.isfinite(dd) & (dd == 0)) / np.isfinite(dd).sum(); print("  share of year-on-year changes exactly zero (repeated figures):", round(float(rep), 3))
    sd = np.nanstd(dd, axis=1); print("  per-record SD of log change: median %.3f p90 %.3f p99 %.3f max %.3f" % tuple(np.nanpercentile(sd, [50, 90, 99, 100])))
    z_ = (dd - np.nanmean(dd, 1, keepdims=True)) / sd[:, None]; zz = z_[np.isfinite(z_)]
    print("  pooled standardised change: kurtosis %.1f, share beyond 4 SD %.4f" % (float(np.mean(zz**4)), float(np.mean(np.abs(zz) > 4))))
    # persistence of changes: lag-1 autocorrelation of log change by record
    ac = [np.corrcoef(r[np.isfinite(r[:-1]) & np.isfinite(r[1:])][:-0 or None][:-1], r[1:][np.isfinite(r[:-1]) & np.isfinite(r[1:])])[0, 1] if False else None for r in []]
    acs = []
    for r in dd:
        a, b = r[:-1], r[1:]; k = np.isfinite(a) & np.isfinite(b)
        if k.sum() > 15 and np.std(a[k]) > 0 and np.std(b[k]) > 0: acs.append(np.corrcoef(a[k], b[k])[0, 1])
    print("  lag-1 autocorrelation of log change: median %.2f, share above 0: %.2f" % (np.median(acs), np.mean(np.array(acs) > 0)))
    ends = np.array([np.flatnonzero(np.isfinite(r))[-1] for r in logy[o]]); print("  records whose last figure is before 2020:", int((ends < 59).sum()))
    if isinstance(item[0], str) or True:
        pass
stats(logy, off, cer, code, "real")
names, cnt = np.unique(item[~cer], return_counts=True); print("  records by crop: min", cnt.min(), "max", cnt.max(), "crops", len(names))
# rough crops: by crop, median per-record SD of change
d = np.diff(logy, axis=1)[:, SC - 1:]; sd = np.nanstd(d, axis=1)
bycrop = sorted(((float(np.median(sd[item == n])), n) for n in np.unique(item)), reverse=True)
print("  roughest crops (median SD of log change):", [(n, round(v, 3)) for v, n in bycrop[:6]], "smoothest:", [(n, round(v, 3)) for v, n in bycrop[-4:]])
print("  cereals median SD", round(float(np.median(sd[cer])), 3), "others", round(float(np.median(sd[~cer])), 3))
import panel_x
w = panel_x.make(26050, kind="link", share=0.2, rainfed=0.0, crops=53, sure=6)
c2 = w["cereal"] < 6
stats(w["logy"], w["official"], c2, w["country"], "made-up full size (leak, seed 26050)")
