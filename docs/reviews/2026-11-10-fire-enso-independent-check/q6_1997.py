"""Question 6, follow-up: does the product record the 1997 fires of equatorial Asia (a fitting year)? Plain km2 burned, summed over boxes, ranked among the 21 years 1982-2003 (1994 absent). No driver is involved."""
import sys
import numpy as np
S = sys.argv[1]
raw = np.load(f"{S}/ssea_raw.npz")
b = raw["km2"].reshape(22, 12, -1); LAT, LON = raw["lat"], raw["lon"]
yrs = [v for v in range(22) if v != 12]
for nm, box in (("Borneo 4S-4N 108-119E", (-4, 4, 108, 119)), ("Sumatra 6S-3N 95-106E", (-6, 3, 95, 106)), ("Kalimantan+Sumatra 6S-5N 95-120E", (-6, 5, 95, 120))):
    sel = (LAT >= box[0]) & (LAT <= box[1]) & (LON >= box[2]) & (LON <= box[3])
    tot = np.nansum(b[:, :, sel], axis=2)  # years x months
    aso = tot[:, 7:10].sum(1)
    order = sorted(yrs, key=lambda v: -aso[v])
    print(f"{nm}: Aug-Oct km2 burned, years ranked: " + ", ".join(f"{1982 + v}:{aso[v]:.0f}" for v in order[:6]) + f" ... 1997 is rank {order.index(15) + 1} of 21, 1998 Feb-Apr rank among Feb-Apr: {sorted(yrs, key=lambda v: -tot[v, 1:4].sum()).index(16) + 1}")
