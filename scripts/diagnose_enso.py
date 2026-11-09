"""After the confirmation missed: why. Exploration on a spent period, marking nothing. Reported in results/real-enso-drought.md, "After the miss"."""
import numpy as np

from causal_atlas import confirm
from run_enso import DISCOVERY, REGIONS, SAVE, data

if __name__ == "__main__":
    y, x, lat, lon = data()
    p = np.load(SAVE / "oni_confirmation.npz")
    lag, claimed, slope = p["lag"], p["claimed"], p["slope"]
    fit, score = np.arange(12, DISCOVERY), np.arange(DISCOVERY, y.shape[1])
    n = len(score) // 12
    base_fit, base = confirm.baseline(y, lat, lon, fit, score)
    truth = y[:, score]
    pick = np.repeat(claimed[:, None, :], n, axis=1).reshape(len(y), -1)
    term = confirm.added(x, score, lag, slope)
    sse = lambda pred, w=pick: float(((truth - pred) ** 2)[w].sum())
    everything = np.ones_like(pick)
    print("field mean, 1951-1999 and 2000-2024:", round(float(y[:, fit].mean()), 3), round(float(truth.mean()), 3))
    cell_mean = y[:, fit].mean(axis=1, keepdims=True)
    for name, w in (("claimed", pick), ("all", everything)):
        b = sse(base, w)
        print(name, "| squared error relative to the baseline's: flat zero", round(sse(0 * base, w) / b, 3), "| each cell's 1951-1999 mean", round(sse(cell_mean + 0 * base, w) / b, 3))
    print("S on claimed by slope multiplier:", {k: round(1 - sse(base + k * term) / sse(base), 3) for k in (0.0, 0.25, 0.5, 0.75, 1.0)})
    print("S on claimed, El Niño term on a flat-zero forecast instead of the baseline:", round(1 - sse(term) / sse(0 * base), 3))
    res = (truth - base).reshape(len(y), n, 12)
    same, ratio = [], []
    for c, m in zip(*np.where(claimed)):
        d = x[score[m::12] - lag[c, m]]
        b = (d @ res[c, :, m]) / (d @ d)
        same.append(b * slope[c, m] > 0)
        ratio.append(b / slope[c, m] if slope[c, m] else np.nan)
    print("claimed cell-months whose 2000-2024 slope has the 1951-1999 sign:", round(float(np.mean(same)), 3), "| median ratio of new slope to old:", round(float(np.nanmedian(ratio)), 3))
    print("claims by lag:", {int(k): int((lag[claimed] == k).sum()) for k in np.unique(lag[claimed])})
    print("claims by target month (0 = January):", claimed.sum(axis=0).tolist())
    for name, ((s, nth, w, e), _, _) in REGIONS.items():
        box = (lat >= s) & (lat <= nth) & (lon >= w) & (lon <= e)
        wb = pick & box[:, None]
        if wb.any():
            print(name, "claimed cell-months", int((claimed & box[:, None]).sum()), "S", round(1 - sse(base + term, wb) / sse(base, wb), 3))
    en = np.abs(x[score - 4]).reshape(n, 12).mean(axis=1)
    print("mean |ONI| by confirmation year (lag 4):", np.round(en, 2).tolist())
    a = np.where(pick, (truth - base - term) ** 2, 0).reshape(len(y), n, 12).sum(axis=(0, 2))
    b = np.where(pick, (truth - base) ** 2, 0).reshape(len(y), n, 12).sum(axis=(0, 2))
    print("S on claimed by year, 2000 on:", np.round(1 - a / b, 2).tolist())
