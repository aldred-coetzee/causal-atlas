"""Item 4/8: how much a country's crops share their year-to-year changes, yields only (cereal with other crop, other with other), real vs made-up. Run with python -I."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]  # the repo root; put in by the project session in place of an absolute path, before this file was committed
import sys
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "docs/reviews/2026-11-10-crops-rule-check/scripts")]
import numpy as np
CEREALS = ("Wheat", "Maize (corn)", "Rice", "Barley", "Sorghum", "Millet")
def pairs(logy, cer, code):
    d = np.diff(logy, axis=1)[:, 24:]
    co, oo = [], []
    for c in np.unique(code):
        u = np.flatnonzero(code == c)
        for i in range(len(u)):
            for j in range(i + 1, len(u)):
                a, b = d[u[i]], d[u[j]]; k = np.isfinite(a) & np.isfinite(b)
                if k.sum() < 20: continue
                r = np.corrcoef(a[k], b[k])[0, 1]
                if cer[u[i]] != cer[u[j]]: co.append(r)
                elif not cer[u[i]]: oo.append(r)
    return np.median(co), np.mean(co), np.median(oo), np.mean(oo), len(co), len(oo)
z = np.load(str(ROOT / "data/panel/real/crops.npz"), allow_pickle=False)
print("real: cereal-other median %.3f mean %.3f | other-other median %.3f mean %.3f | pairs %d %d" % pairs(z["logy"], np.isin(z["item"], CEREALS), z["code"]))
import panel_x
for kw, lab in ((dict(), "registered leak"), (dict(shared_k=1.5, own_k=0.5), "shared_k 1.5 own_k 0.5")):
    w = panel_x.make(26050, kind="link", share=0.2, rainfed=0.0, crops=18, sure=6, **kw)
    print(lab, ": cereal-other median %.3f mean %.3f | other-other median %.3f mean %.3f | pairs %d %d" % pairs(w["logy"], w["cereal"] < 6, w["country"]))
