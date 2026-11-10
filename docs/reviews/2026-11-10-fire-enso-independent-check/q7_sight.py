"""Question 7: what the satellite saw (share of burnable land observed), South and Southeast Asia, 1982-2003, from this reader's rebuild. Is it near-constant with a few months dominating; does it carry year-to-year drift; where does its tie to the ONI come from?"""
import sys, warnings
import numpy as np
warnings.simplefilter("ignore")
S = sys.argv[1]
m, raw = np.load(f"{S}/ssea_mine.npz"), np.load(f"{S}/ssea_raw.npz")
LAT, LON = raw["lat"], raw["lon"]
keep = np.isin(np.round(LAT * 1000 + LON, 3), np.round(m["lat"] * 1000 + m["lon"], 3))
o = raw["obs"].reshape(22, 12, -1)[:, :, keep].transpose(2, 0, 1)  # cells x years x months; 1994 NaN
lat, lon = m["lat"], m["lon"]
known = np.isfinite(o)
mu, sd = np.nanmean(o, 1), np.nanstd(o, 1)
z = np.where(known, (o - mu[:, None]) / np.where(sd > 0, sd, 1)[:, None], 0)
z = np.clip(np.nan_to_num(z), -3, 3)
print("raw observed share, per cell-calendar-month: median spread over years", round(float(np.median(sd)), 3), " median mean", round(float(np.median(mu)), 3),
      " share of cell-months with spread < 0.02:", round(float((sd < 0.02).mean()), 3))
flat = z[:, [v for v in range(22) if v != 12]].reshape(-1)
print("standardised: kurtosis", round(float(((flat - flat.mean()) ** 4).mean() / flat.var() ** 2), 2), "(3 for a normal); share at the clip", round(float((np.abs(flat) == 3).mean()), 4))
# year-to-year: field-mean standardised sight by year
ym = z.mean(axis=(0, 2))
print("field mean of standardised sight by year:", " ".join(f"{1982 + v}:{ym[v]:+.2f}" for v in range(22)))
yrs = np.array([v for v in range(22) if v != 12])
print("lag-1-year autocorrelation of the field mean (21 years):", round(float(np.corrcoef(ym[yrs][:-1], ym[yrs][1:])[0, 1]), 2))
yb = np.load(f"{S}/ssea_mine.npz")["y"].reshape(len(lat), 22, 12)
bm = yb.mean(axis=(0, 2))
print("same for standardised burned area:", round(float(np.corrcoef(bm[yrs][:-1], bm[yrs][1:])[0, 1]), 2))
# tie to the ONI in the region where the result's sight run puts it: best |r| over regions, months, lags 0-12, then leave one year out
oni = {int(l.split()[0]): [float(v) for v in l.split()[1:]] for l in open("data/raw/oni.data") if len(l.split()) == 13 and l.split()[0].isdigit()}
x = np.ravel([oni[v] for v in range(1982, 2004)])
years = [v for v in range(1, 22) if v != 12]
zz = z.reshape(len(lat), -1)
regs = []
for a in np.arange(np.floor(lat.min() / 5) * 5, lat.max(), 5):
    for b in np.arange(np.floor(lon.min() / 5) * 5, lon.max(), 5):
        ins = (lat >= a) & (lat < a + 10) & (lon >= b) & (lon < b + 10)
        if ins.sum() >= 40:
            regs.append(ins)
avg = np.array([zz[i].mean(0) for i in regs]); avgb = np.array([yb.reshape(len(lat), -1)[i].mean(0) for i in regs])
def table(series):
    out = np.zeros((len(regs), 12, 13))
    for k in range(len(regs)):
        for mth in range(12):
            t = np.array([series[k, 12 * v + mth] for v in years])
            for lag in range(13):
                out[k, mth, lag] = np.corrcoef(t, [x[12 * v + mth - lag] for v in years])[0, 1]
    return np.nan_to_num(out)
rs, rb = table(avg), table(avgb)
for nm, r, ser in (("sight", rs, avg), ("burned", rb, avgb)):
    k, mth, lag = np.unravel_index(np.abs(r).argmax(), r.shape)
    t = np.array([ser[k, 12 * v + mth] for v in years]); d = np.array([x[12 * v + mth - lag] for v in years])
    loo = [np.corrcoef(np.delete(t, i), np.delete(d, i))[0, 1] for i in range(20)]
    print(f"{nm}: largest r {r[k, mth, lag]:+.3f} (region at {lat[regs[k]].mean():.1f}N {lon[regs[k]].mean():.1f}E, month {mth + 1}, lag {lag}); leaving out each year in turn: {min(loo, key=abs):+.2f} to {max(loo, key=abs):+.2f}; "
          f"mean of r^2 over all regions, months, lags {float((r ** 2).mean()):.3f}; share of region-month-lags with |r| > 0.5: {float((np.abs(r) > 0.5).mean()):.3f}")
# how much of the ONI-sight tie is the field mean (one common instrument signal): correlate field-mean sight by calendar month with the ONI
fm = zz.mean(0)
rr = [max((abs(np.corrcoef([fm[12 * v + mth] for v in years], [x[12 * v + mth - lag] for v in years])[0, 1]), lag) for lag in range(13)) for mth in range(12)]
print("field-wide mean sight vs ONI, best |r| over lags by calendar month:", [round(a, 2) for a, _ in rr])
print("correlation of the 12-month-mean ONI with the field-mean sight by year:", round(float(np.corrcoef(ym[yrs], x.reshape(22, 12).mean(1)[yrs])[0, 1]), 2))
