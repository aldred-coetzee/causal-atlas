"""Written by the project session after the reader reported, not by the reader. The drought series alone: how large is the slow curve in each country's series, on the real panel and on made-up worlds with no drift, the registered drift and the reader's 2.5 times drift? No yield is read. Run from the repo root with python -I."""
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "src"), str(Path(__file__).resolve().parent)]
import panel_x  # noqa: E402


def curve(x):
    """By country: the coefficient of clock squared (clock from 0 to 1 over the record) beside a level and a straight line, in units of the spread left over; and the share of the series' variance, level and line out, that the curve takes."""
    x = x[np.isfinite(x).all(axis=1)]
    clock = np.linspace(0, 1, x.shape[1])
    A = np.column_stack([np.ones_like(clock), clock, clock**2])
    coef, *_ = np.linalg.lstsq(A, x.T, rcond=None)
    rest = x.T - A @ coef
    line = x.T - A[:, :2] @ np.linalg.lstsq(A[:, :2], x.T, rcond=None)[0]
    return coef[2] / rest.std(axis=0), 1 - rest.var(axis=0) / line.var(axis=0)


def say(label, x):
    c, share = curve(x)
    print(f"{label}: countries {len(c)}; curve in units of spread: spread across countries {c.std():.2f}, median size {np.median(abs(c)):.2f}, 90th {np.percentile(abs(c), 90):.2f}, largest {abs(c).max():.2f}; share of variance the curve takes: median {np.median(share):.4f}, 90th {np.percentile(share, 90):.4f}, largest {share.max():.4f}")


z = np.load(ROOT / "data" / "panel" / "real" / "crops.npz", allow_pickle=False)
x = z["x"]
print("real drought panel", x.shape, "countries with a gap:", int((~np.isfinite(x).all(axis=1)).sum()))
say("real", x)
half = x.shape[1] // 2
say("real, second half of the record only", x[:, half:])
small = {"kind": "link", "share": 0.2, "rainfed": 0.0, "crops": 18, "sure": 6}
kinds = (("made-up, no drift", small), ("made-up, registered drift", {**small, "shape": "drift"}), ("made-up, 2.5 times drift", {**small, "shape": "drift", "drift_x": 3.0, "drift_y": 0.75}))
for seed in range(26080, 26095):  # five worlds of each kind, because the slow swing every made-up world carries curves too, differently in each
    label, kw = kinds[(seed - 26080) % 3]
    say(f"{label} (seed {seed})", panel_x.make(seed, **kw)["x"])
