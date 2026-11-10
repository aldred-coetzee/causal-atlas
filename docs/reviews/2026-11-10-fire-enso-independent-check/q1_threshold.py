"""Question 1, the residue: the few cell-calendar-months that differ are those where the observed share sits on the 0.2 threshold and float32 storage in the cache's grid tips it. Recompute with the shares rounded to float32 and compare again."""
import sys
import numpy as np
z = np.load(sys.argv[1])
o64 = z["obs"].reshape(22, 12, -1).transpose(2, 0, 1)
o32 = o64.astype(np.float32).astype(np.float64)
b32 = z["km2"].reshape(22, 12, -1).transpose(2, 0, 1).astype(np.float32).astype(np.float64)
flip = (np.nan_to_num(o64) >= 0.2) != (np.nan_to_num(o32) >= 0.2)
print("cell-months whose 'seen' flips between float64 and float32 shares:", int(flip.sum()), " shares there:", np.unique(o64[flip]).round(9)[:6])
def std(b, o):
    seen = np.isfinite(b) & (np.nan_to_num(o) >= 0.2)
    v = np.where(seen, np.log1p(np.where(seen, b, 0) / np.where(seen, o, 1)), np.nan)
    n = seen.sum(1); mu = np.nanmean(v, 1); sd = np.nanstd(v, 1)
    use = (n >= 15) & ((seen & (np.nan_to_num(b) > 0)).sum(1) >= 5) & (sd > 0)
    y = np.where(seen & use[:, None], (v - mu[:, None]) / np.where(sd > 0, sd, 1)[:, None], 0)
    return np.clip(np.nan_to_num(y), -3, 3).reshape(len(b), -1), use
import warnings; warnings.simplefilter("ignore")
y, use = std(b32, o32)
c = np.load("data/panel/real/fire_south_southeast_asia.npz")
y = y[use.any(1)]
d = np.abs(y - c["y"][:, :264])
print("with float32 inputs: max abs difference", d.max(), " entries > 1e-4:", int((d > 1e-4).sum()))
