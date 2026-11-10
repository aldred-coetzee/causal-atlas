"""Question 1: rebuild South and Southeast Asia's standardised burned area on 1982-2003 from the raw files, without causal_atlas.fire, and compare with the cache.
Reads only files dated 1982-01 to 2003-12. Writes a scratch npz (not kept in the repo) for the other checks."""
import sys
from pathlib import Path
import netCDF4
import numpy as np

RAW = Path("data/raw/firecci")
OUT = Path(sys.argv[1])
S, N, W, E = -10, 35, 65, 155
years = range(1982, 2004)
nc0 = netCDF4.Dataset(next(RAW.glob("19820101*.nc")))
la, lo = np.asarray(nc0["lat"][:]), np.asarray(nc0["lon"][:])
# quarter-degree rows/cols whose half-degree parent centre lies in the box (edges inclusive, as the rule's boxes)
pla = np.floor(la * 2) / 2 + 0.25  # parent centre of each quarter cell
plo = np.floor(lo * 2) / 2 + 0.25
ri = np.flatnonzero((pla >= S) & (pla <= N)); ci = np.flatnonzero((plo >= W) & (plo <= E))
assert len(ri) % 2 == 0 and len(ci) % 2 == 0
nr, nc_ = len(ri) // 2, len(ci) // 2
km2 = np.full((22, 12, nr, nc_), np.nan); obs = np.full((22, 12, nr, nc_), np.nan)
checked = []
for k, yr in enumerate(years):
    if yr == 1994:
        assert not list(RAW.glob("1994*.nc"))
        continue
    for m in range(12):
        f = netCDF4.Dataset(RAW / f"{yr}{m+1:02d}01-ESACCI-L4_FIRE-BA-AVHRR-LTDR-fv1.1.nc")
        d = netCDF4.num2date(f["time"][0], f["time"].units)
        assert (d.year, d.month) == (yr, m + 1)
        g = lambda v: np.ma.filled(f[v][0, ri[0]:ri[-1] + 1, ci[0]:ci[-1] + 1], 0).astype(float)
        ba, fb, fo = g("burned_area"), g("fraction_of_burnable_area"), g("fraction_of_observed_area")
        if m == 0:
            checked.append((yr, fb.max(), fo.max()))
        fb, fo = fb / 100, fo / 100
        q = lambda a: a.reshape(nr, 2, nc_, 2).sum(axis=(1, 3))
        km2[k, m] = q(ba) / 1e6
        land = q(fb)
        obs[k, m] = np.where(land > 0, q(fb * fo) / np.where(land > 0, land, 1), 0)
print("max of the two fractions in each January file (per cent if ~100):", [(y, round(a, 1), round(b, 1)) for y, a, b in checked])
latc, lonc = pla[ri][::2], plo[ci][::2]
LAT, LON = np.meshgrid(latc, lonc, indexing="ij")
np.savez_compressed(OUT, km2=km2, obs=obs, lat=LAT.ravel(), lon=LON.ravel())
