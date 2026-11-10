"""Question 4: tally the q4_sim runs, and the binomial arithmetic."""
import glob, json, sys
from collections import defaultdict
import numpy as np
from scipy import stats

rows = [json.loads(s) for f in sorted(glob.glob(sys.argv[1] + "/*.jsonl*")) for s in open(f)]
g = defaultdict(list)
for r in rows:
    g[(r["mode"], r["field"])].append(r)
def ci(k, n):
    lo, hi = stats.beta.ppf(0.025, k, n - k + 1) if k else 0, stats.beta.ppf(0.975, k + 1, n - k) if k < n else 1
    return f"{k}/{n} = {k / n:.3f} [{lo:.3f}, {hi:.3f}]"
for key, rr in sorted(g.items()):
    n = len(rr)
    print(key)
    for c in ("cut", "full"):
        b = sum(bool(r[c]["broad"]) for r in rr); s = sum(bool(r[c]["sharp"]) for r in rr)
        a = sum(bool(r[c]["broad"]) or bool(r[c]["sharp"]) for r in rr); bb = sum(bool(r[c]["broad"]) and bool(r[c]["sharp"]) for r in rr)
        print(f"  controls {c:4s}: any lead {ci(a, n)}; broad {ci(b, n)}; sharp {ci(s, n)}; both gates {bb}")
    # exchangeability: where the overall maximum of 22 rotations sits
    for gname in ("broad", "sharp"):
        h = np.bincount([r[f"argmax_{gname}_rot"] for r in rr], minlength=22)
        print(f"  {gname}: overall max at rotation 0 in {h[0]}/{n} (1/22 = {n / 22:.1f} expected); at rotations 1 or 21: {h[1] + h[21]}; mean per other rotation {h[2:21].mean():.1f}")
print("\nBinomial, 120 runs: P(X >= 18) at p:")
for p in (0.05, 0.0975, 0.10, 0.12, 0.15):
    print(f"  p={p}: {stats.binom.sf(17, 120, p):.4f}   (expected {120 * p:.1f})")
print("P(X <= 9 | 120, p=0.0975):", round(stats.binom.cdf(9, 120, 0.0975), 3), "  p=0.10:", round(stats.binom.cdf(9, 120, 0.10), 3))
print("Per gate 1/20 two gates independent:", 1 - (19 / 20) ** 2, " with 49 controls:", 1 - (49 / 50) ** 2, " 47:", 1 - (47 / 48) ** 2)
print("P(X<=5 | 100, 0.0396)", round(stats.binom.cdf(5, 100, 0.0396), 3))
