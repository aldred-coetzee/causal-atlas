"""Question 6: the ONI's largest correlation with a 10-degree region average of South and Southeast Asia, from this reader's own rebuild (1982-2003 only) and own tiling; then the same with less processing, to see whether the processing flattens an El Nino signal. All on the fitting years."""
import sys
import warnings
import numpy as np
warnings.simplefilter("ignore")
S = sys.argv[1]
m, raw = np.load(f"{S}/ssea_mine.npz"), np.load(f"{S}/ssea_raw.npz")
y, lat, lon = m["y"], m["lat"], m["lon"]
oni = {int(l.split()[0]): [float(v) for v in l.split()[1:]] for l in open("data/raw/oni.data") if len(l.split()) == 13 and l.split()[0].isdigit()}
x = np.ravel([oni[v] for v in range(1982, 2004)])  # month 0 = 1982-01
years = [v for v in range(1, 22) if v != 12]


def regions(lat, lon):
    out = []
    for a in np.arange(np.floor(lat.min() / 5) * 5, lat.max(), 5):
        for o in np.arange(np.floor(lon.min() / 5) * 5, lon.max(), 5):
            inside = (lat >= a) & (lat < a + 10) & (lon >= o) & (lon < o + 10)
            if inside.sum() >= 40:
                out.append((a, o, inside))
    return out


def best(series_by_region, label):
    """series_by_region: regions x 264. Largest |r| over regions, lags 0-12, calendar months, over the 20 target years."""
    top = (0, None)
    for k, s in enumerate(series_by_region):
        for mth in range(12):
            t = np.array([s[12 * v + mth] for v in years])
            if t.std() == 0:
                continue
            for lag in range(13):
                d = np.array([x[12 * v + mth - lag] for v in years])
                r = np.corrcoef(t, d)[0, 1]
                if abs(r) > abs(top[0]):
                    top = (r, (k, mth + 1, lag))
    return top


R = regions(lat, lon)
avg = np.array([y[ins].mean(0) for _, _, ins in R])
r, (k, mth, lag) = best(avg, "standardised")
a, o, ins = R[k]
print(f"own rebuild, standardised: {len(R)} regions; largest r = {r:+.3f}, month {mth}, lag {lag}, region centred {lat[ins].mean():.1f}N {lon[ins].mean():.1f}E")

# El Nino's own season in equatorial Asia: Indonesia-Borneo regions, September-October, lags 0-3
b = raw["km2"].reshape(22, 12, -1); ob = raw["obs"].reshape(22, 12, -1)
LAT, LON = raw["lat"], raw["lon"]
for nm, box in (("Sumatra-Borneo 5S-5N 95-120E", (-5, 5, 95, 120)), ("Borneo 4S-4N 108-119E", (-4, 4, 108, 119))):
    sel = (LAT >= box[0]) & (LAT <= box[1]) & (LON >= box[2]) & (LON <= box[3])
    kept_here = np.isin(np.round(LAT * 1000 + LON, 3), np.round(lat * 1000 + lon, 3)) & sel
    print(f"\n{nm}: {sel.sum()} cells in box, {kept_here.sum()} kept by the rule")
    for mth in (8, 9, 10):
        tot = np.nansum(b[:, mth - 1][:, sel], axis=1)  # plain km2 summed, no seen filter
        seen_share = np.nanmean((ob[:, mth - 1][:, sel] >= 0.2), axis=1)
        zrule = np.array([y[(lat >= box[0]) & (lat <= box[1]) & (lon >= box[2]) & (lon <= box[3])][:, 12 * v + mth - 1].mean() for v in range(22)])
        rs = []
        for lag in (0, 1, 2, 3):
            d = np.array([x[12 * v + mth - 1 - lag] for v in years])
            rs.append((lag, round(np.corrcoef(np.log1p(tot[years]), d)[0, 1], 2), round(np.corrcoef(zrule[years], d)[0, 1], 2)))
        print(f" month {mth}: r with ONI by lag (lag, log total km2 raw, rule's region mean) {rs}")
        print(f"   share of box cells seen (>=0.2): 1997 {seen_share[15]:.2f}, 1982 {seen_share[0]:.2f}, median other years {np.median(np.delete(seen_share, [0, 12, 15])):.2f}")
        print(f"   rule's region mean in 1997 {zrule[15]:+.2f}, 1982 {zrule[0]:+.2f}; share of kept cells zero in 1997 {(y[(lat >= box[0]) & (lat <= box[1]) & (lon >= box[2]) & (lon <= box[3])][:, 12 * 15 + mth - 1] == 0).mean():.2f}")
# months in use per calendar month in the Borneo/Sumatra box
sel = (lat >= -5) & (lat <= 5) & (lon >= 95) & (lon <= 120)
print("\nkept cells in 5S-5N 95-120E with each calendar month in use:", m["used"][sel].sum(0).tolist(), "of", sel.sum())
