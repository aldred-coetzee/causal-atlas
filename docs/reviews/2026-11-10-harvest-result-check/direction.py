"""Item 5: the direction. With this review's own errors (mean3 baseline) and standardised drought: slopes per cereal x band over 1981-2024 (descriptive), and, for the records with the largest project gains, the correlation of the yield's departure with each of the six values."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np, json
from causal_atlas import yields
import own
p, country, cereal = common.real()
o = own.Own(p, country, cereal, "mean3")
B = o.slopes(p["x"], "B")
lab = ["Sep-1", "Dec-1", "Mar", "Jun", "Sep", "Dec"]
print("slopes (error in scale units per sd of SPEI), cereal x band; + means wetter -> higher yield than baseline")
for c in range(6):
    for band, bn in enumerate(("south", "tropics", "north")):
        n = ((o.groups["B"] == c * 3 + band)).sum()
        if n:
            print(" %-12s %-8s n=%3d" % (yields.CEREALS[c][:12], bn, n), " ".join("%+.3f" % v for v in B[c * 3 + band]))
f = own.drivers(p["x"], o.T)[country]
tg = o.target & np.isfinite(f).all(2); tg[:, :20] = False
rows = [json.loads(s) for s in open(os.path.join(common.ROOT, "results", "harvest-drought.jsonl"))]
real = [r for r in rows if r["kind"] == "real" and r["variant"] == "year_end"][0]
gain = np.array([u[3] for u in real["by_unit"]]); n = np.array([u[2] for u in real["by_unit"]])
order = np.argsort(-np.where(n >= 20, gain, -9))
print("\nlargest project gains, correlation of own error with each value (1981-2024):")
pos = neg = 0
for u in order[:25]:
    z, ff = o.z[u, tg[u]], f[u, tg[u]]
    r = [np.corrcoef(z, ff[:, k])[0, 1] for k in range(6)]
    k = int(np.argmax(np.abs(r)))
    pos += r[k] > 0; neg += r[k] < 0
    print(" %-4s %-13s gain %+.2f  " % (p["code"][u], p["item"][u][:13], gain[u]), " ".join("%+.2f" % v for v in r), " strongest:", lab[k])
print("strongest correlation positive (wet->more) in", pos, "of", pos + neg)
# whole panel: sum over records of correlation sign at the strongest month, weighted by nothing
allr = []
for u in range(len(country)):
    if tg[u].sum() >= 20:
        z, ff = o.z[u, tg[u]], f[u, tg[u]]
        r = np.array([np.corrcoef(z, ff[:, k])[0, 1] for k in range(6)])
        allr.append(r)
allr = np.array(allr)
k = np.argmax(np.abs(allr), 1)
s = allr[np.arange(len(allr)), k]
print("all records with 20+ years:", len(allr), "strongest correlation positive in %d, negative in %d; |r|>0.3: positive %d, negative %d" % ((s > 0).sum(), (s < 0).sum(), ((s > 0.3)).sum(), (s < -0.3).sum()))
print("mean correlation by month over all records:", " ".join("%s %+.3f" % (a, b) for a, b in zip(lab, allr.mean(0))))
