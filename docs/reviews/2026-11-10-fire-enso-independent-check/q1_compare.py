"""Question 1, second half: standardise the rebuild as the rule text says and compare with the cache's columns 0-263 (fitting years only)."""
import sys
import numpy as np

z = np.load(sys.argv[1])
km2, obs, lat, lon = z["km2"], z["obs"], z["lat"], z["lon"]  # years x months x rows x cols
Y = km2.shape[0]
b = km2.reshape(Y, 12, -1).transpose(2, 0, 1)  # cells, years, months
o = obs.reshape(Y, 12, -1).transpose(2, 0, 1)
seen = np.isfinite(b) & (np.nan_to_num(o) >= 0.2)
v = np.where(seen, np.log1p(np.where(seen, b, 0) / np.where(seen, o, 1)), np.nan)
n = seen.sum(axis=1)
mu = np.nanmean(v, axis=1)
sd = np.nanstd(v, axis=1)
burned = (seen & (np.nan_to_num(b) > 0)).sum(axis=1)
use = (n >= 15) & (burned >= 5) & (sd > 0)
zz = np.where(seen & use[:, None, :], (v - mu[:, None, :]) / np.where(sd > 0, sd, 1)[:, None, :], 0)
zz = np.clip(np.nan_to_num(zz), -3, 3).reshape(len(b), -1)
kept = use.any(axis=1)
mine, mlat, mlon, mused = zz[kept], lat[kept], lon[kept], use[kept]
c = np.load("data/panel/real/fire_south_southeast_asia.npz")
print("cells mine", kept.sum(), "cache", len(c["y"]), "of", len(b))
same = np.array_equal(np.round(mlat, 3), np.round(c["lat"], 3)) and np.array_equal(np.round(mlon, 3), np.round(c["lon"], 3))
print("same cells, same order:", same, " used months equal:", np.array_equal(mused, c["used"]))
d = np.abs(mine - c["y"][:, :264])
print("max abs difference over fitting columns:", d.max(), " entries > 1e-4:", int((d > 1e-4).sum()), "of", d.size)
print("share zero (mine):", round(float((mine == 0).mean()), 3), " share clipped:", round(float((np.abs(mine) == 3).mean()), 4))
print("used cell-months on fitting:", int(mused.sum()), " per cell:", round(float(mused.sum(1).mean()), 2))
np.savez_compressed(sys.argv[2], y=mine, lat=mlat, lon=mlon, used=mused)
