"""Item 6: how often claims.two_way's lower end is above zero when the true S on the claims is zero. Claimed record-years with error e and term f, built so that E[S] = 0 exactly (e = f/2 + noise gives 2E[ef] = E[f^2]); countries differ in size and in how strongly their term goes with their error (a country effect that averages to the null), years share a shock, tails heavy. Seeds 26060 onward, one per setting."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]  # the repo root; put in by the project session in place of an absolute path, before this file was committed
import sys
import numpy as np
sys.path[:0] = [str(ROOT / "src")]
from causal_atlas import claims
def one(rng, nc, years=29, recs_per=(1, 6), cfx=1.0, yfx=0.5, tail=3, fill=0.35):
    cn = rng.integers(*recs_per, size=nc)
    num, den = np.zeros((nc, years)), np.zeros((nc, years))
    yshock = rng.standard_normal(years) * yfx
    for c in range(nc):
        k = rng.normal(0, cfx)  # country's own departure of the e-f relation from the null, mean zero
        for _ in range(cn[c]):
            claim = rng.random(years) < fill
            f = 0.3 * (rng.standard_t(tail, years) + yshock)
            e = (0.5 + k) * f + rng.standard_t(tail, years)
            num[c] += np.where(claim, (e - f) ** 2, 0)
            den[c] += np.where(claim, e ** 2, 0)
    # recentre so the population S is exactly zero is not possible draw by draw; E[S]~0 by construction of k mean zero
    return num, den
for seed, nc, rp, cfx in ((26060, 15, (1, 4), 1.0), (26061, 15, (2, 3), 0.0), (26062, 40, (1, 6), 1.0), (26063, 100, (1, 6), 1.0), (26064, 15, (1, 4), 2.0)):
    rng = np.random.default_rng(seed)
    hits, S = 0, []
    reps = 300
    for i in range(reps):
        num, den = one(rng, nc, recs_per=rp, cfx=cfx)
        s, ci = claims.two_way(num, den, seed=0, draws=1000)
        S.append(s); hits += ci[0] > 0
    print(f"seed {seed} countries {nc} records/country {rp} country spread {cfx}: lower end above zero in {hits}/{reps} ({hits/reps:.3f}); mean S {np.mean(S):+.4f}, median {np.median(S):+.4f}", flush=True)
