"""The real yields alone (no drought value is loaded): official figures that repeat the year before exactly, figures per scored year, and the year-to-year memory of the departures from each record's own past."""
import numpy as np

z = np.load("data/panel/real/yields.npz")
logy, off, item, code = z["logy"], z["official"], z["item"], z["code"]
units, years = logy.shape
print("units", units, "countries", len(np.unique(code)), "years", years, "first official year index min", np.argmax(off, axis=1).min())
same = np.zeros_like(off)
same[:, 1:] = off[:, 1:] & np.isfinite(logy[:, :-1]) & (np.abs(logy[:, 1:] - logy[:, :-1]) < 1e-9)
print("official figures equal to the year before exactly:", int(same.sum()), "of", int(off.sum()), f"({same.sum() / off.sum():.2%});", "in scored years 1986-2024:", int(same[:, 25:].sum()), "of", int(off[:, 25:].sum()))
runs = (same.sum(axis=1))
print("records with 3 or more such repeats:", int((runs >= 3).sum()), "most:", int(runs.max()))
print("official figures by year (1961, 1981, 1986, 2000, 2020, 2024):", [int(off[:, t].sum()) for t in (0, 20, 25, 39, 59, 63)])
print("by cereal:", {c: int((item == c).sum()) for c in np.unique(item)})
# year-to-year memory of changes and of departures from a ten-year mean
d = np.diff(logy, axis=1)
a = d[:, 1:], d[:, :-1]
ok = np.isfinite(a[0]) & np.isfinite(a[1])
print("lag-1 correlation of year-on-year changes, pooled:", round(float(np.corrcoef(a[0][ok], a[1][ok])[0, 1]), 3))
# smoothing: share of records whose official stretch has very small year-on-year change relative to the panel
sd = np.array([np.nanstd(d[u][off[u, 1:] & off[u, :-1]]) if (off[u, 1:] & off[u, :-1]).sum() > 5 else np.nan for u in range(units)])
print("rms-like spread of official year-on-year changes, quantiles 5/25/50/75/95:", np.round(np.nanpercentile(sd, [5, 25, 50, 75, 95]), 3))
print("records with spread below 0.03:", int((sd < 0.03).sum()))
