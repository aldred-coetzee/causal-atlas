"""Independent re-implementation of Step 2 (region scale) of results/real-enso-continents.md.
Uses only field.box, field.oni, links.tiles, links.correlations, links.significant (the last two only for a cross-check).
Usage: reimpl.py [noise]   -- 'noise' replaces every SPEI and ONI value from 2000-01 on with noise and prints the fitted objects."""
import json, sys
import numpy as np
from scipy import stats
from causal_atlas import field, links

import os; OUT = os.path.dirname(os.path.abspath(__file__)) + "/"  # was the reader's scratch folder
SPLIT = 600                      # 2000-01
FIT_YEARS = list(range(1, 50))   # targets 1951..1999
SCORE_YEARS = list(range(50, 75))
LAGS = list(range(4, 13))
NOISE = len(sys.argv) > 1 and sys.argv[1] == "noise"


def trailing(series, t, n):
    lo, hi = max(t - 2 - n, 0), t - 2          # months lo..t-3
    return float(np.mean(series[lo:hi])) if hi > lo else 0.0


def feats(R, near, u, t):
    s = R[u]
    return [s[t - 3], s[t - 4], s[t - 5], s[t - 6], s[t - 12], near[t - 3], trailing(s, t, 12), trailing(s, t, 60), 1.0]


def months_of(years):
    return [12 * yr + m for yr in years for m in range(12)]


def predict(name, R, near, coef, u, t):
    if name == "zero":
        return 0.0
    if name == "level":
        return trailing(R[u], t, 60)
    return float(np.dot(feats(R, near, u, t), coef))


def fit_linear(R, near, fit_months):
    X, Y = [], []
    for t in fit_months:
        for u in range(len(R)):
            X.append(feats(R, near, u, t)); Y.append(R[u, t])
    return np.linalg.lstsq(np.array(X), np.array(Y), rcond=None)[0]


def blocks(years):
    n = len(years); sizes = [n // 5 + (1 if i < n % 5 else 0) for i in range(5)]
    out, i = [], 0
    for s in sizes:
        out.append(years[i:i + s]); i += s
    return out


def corr_claims(R, x, years):
    """r[u][m][L], p-values, BH over all, best lag per (u,m), claimed flag."""
    U = len(R); n = len(years)
    r = np.zeros((U, 12, len(LAGS)))
    for u in range(U):
        for m in range(12):
            a = np.array([R[u, 12 * yr + m] for yr in years], float)
            for j, L in enumerate(LAGS):
                b = np.array([x[12 * yr + m - L] for yr in years], float)
                r[u, m, j] = np.corrcoef(a, b)[0, 1]
    tt = r * np.sqrt((n - 2) / (1 - r * r)); p = 2 * stats.t.sf(np.abs(tt), n - 2)
    ps = np.sort(p.ravel()); k = np.arange(1, ps.size + 1)
    ok = ps <= 0.05 * k / ps.size
    thr = ps[ok].max() if ok.any() else -1
    best = np.abs(r).argmax(axis=2)
    claimed = np.zeros((U, 12), bool); lag = np.zeros((U, 12), int)
    for u in range(U):
        for m in range(12):
            lag[u, m] = LAGS[best[u, m]]
            claimed[u, m] = p[u, m, best[u, m]] <= thr
    return r, lag, claimed


def slopes(e, x, lag, years):
    U = len(e); sl = np.zeros((U, 12))
    for u in range(U):
        for m in range(12):
            num = sum(e[u, 12 * yr + m] * x[12 * yr + m - lag[u, m]] for yr in years)
            den = sum(x[12 * yr + m - lag[u, m]] ** 2 for yr in years)
            sl[u, m] = num / den
    return sl


def run(name):
    yc, lat, lon = field.box(name)
    yc = np.clip(yc, -3, 3).astype(np.float64)
    x = field.oni().astype(np.float64).copy()
    if NOISE:
        rng = np.random.default_rng(99)
        yc[:, SPLIT:] = rng.normal(0, 1, yc[:, SPLIT:].shape); x[SPLIT:] = rng.normal(0, 1, x[SPLIT:].shape)
    T = links.tiles(lat, lon)
    R = T @ yc
    U, M = R.shape
    near = R.mean(axis=0)
    # baseline choice by 5 blocks
    ferr = {}
    for bname in ("zero", "level", "linear"):
        tot = 0.0
        for blk in blocks(FIT_YEARS):
            rest = [yr for yr in FIT_YEARS if yr not in blk]
            coef = fit_linear(R, near, months_of(rest)) if bname == "linear" else None
            for t in months_of(blk):
                for u in range(U):
                    tot += (R[u, t] - predict(bname, R, near, coef, u, t)) ** 2
        ferr[bname] = tot
    chosen = min(ferr, key=ferr.get)
    coef = fit_linear(R, near, months_of(FIT_YEARS))
    E = {}
    for bname in ("zero", "level", "linear"):
        e = np.zeros((U, M))
        for t in range(12, M):
            for u in range(U):
                e[u, t] = R[u, t] - predict(bname, R, near, coef, u, t)
        E[bname] = e
    e = E[chosen]
    r, lag, claimed = corr_claims(R, x, FIT_YEARS)
    sl = slopes(e, x, lag, FIT_YEARS)
    # k
    bb = cc = 0.0
    for blk in blocks(FIT_YEARS):
        rest = [yr for yr in FIT_YEARS if yr not in blk]
        _, lg, cl = corr_claims(R, x, rest)
        s2 = slopes(e, x, lg, rest)
        for yr in blk:
            for u in range(U):
                for m in range(12):
                    if cl[u, m]:
                        t = 12 * yr + m; term = s2[u, m] * x[t - lg[u, m]]
                        bb += e[u, t] * term; cc += term * term
    k = min(max(bb / cc, 0.0), 1.0) if cc > 0 else 0.0
    # score, by year
    def by_year(shift):
        base, mod = np.zeros(25), np.zeros(25)
        for i, yr in enumerate(SCORE_YEARS):
            dyr = SCORE_YEARS[(i + shift) % 25]
            for u in range(U):
                for m in range(12):
                    if claimed[u, m]:
                        t = 12 * yr + m
                        pred = k * sl[u, m] * x[12 * dyr + m - lag[u, m]]
                        base[i] += e[u, t] ** 2; mod[i] += (e[u, t] - pred) ** 2
        return base, mod
    base, mod = by_year(0)
    shifted = np.array([by_year(s)[1] for s in range(1, 25)])
    alone = {b: float(sum(E[b][u, 12 * yr + m] ** 2 for yr in SCORE_YEARS for u in range(U) for m in range(12) if claimed[u, m])) for b in E}
    # cross-check links.correlations against my numpy loop
    rl = links.correlations(R, x, np.array(FIT_YEARS), np.array(LAGS))  # lags x 12 x units
    corr_diff = float(np.abs(rl.transpose(2, 1, 0) - r).max())
    return dict(field=name, baseline=chosen, fold_error={k_: round(v, 1) for k_, v in ferr.items()}, coef=coef.round(6).tolist(), k=k,
                claimed=int(claimed.sum()), lag_hist=np.bincount(lag[claimed], minlength=13)[4:].tolist(),
                slope_sum=float(sl[claimed].sum()), corr_diff=corr_diff,
                base=base.tolist(), model=mod.tolist(), shifted=shifted.tolist(), alone=alone)


if __name__ == "__main__":
    names = ["south_america", "australia", "south_southeast_asia", "north_america", "europe"]
    res = [run(n) for n in names]
    json.dump(res, open(OUT + ("noise.json" if NOISE else "clean.json"), "w"))
    for r in res:
        b, m = np.array(r["base"]), np.array(r["model"])
        s = 1 - m.sum() / b.sum() if b.sum() else float("nan")
        print(r["field"], r["baseline"], "k=%.3f" % r["k"], "claims", r["claimed"], r["lag_hist"], "S=%.4f" % s, "model=%.2f" % m.sum(), {k: round(v, 2) for k, v in r["alone"].items()}, "corrdiff=%.1e" % r["corr_diff"])
