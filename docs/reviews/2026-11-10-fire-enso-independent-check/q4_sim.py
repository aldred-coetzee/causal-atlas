"""Question 4: how often does the search name something when nothing is linked?

Each run computes the two gates' statistics once for shifts 1..21 and then applies the gates twice:
  'cut'  - controls 2..20 (as in the result: decision 0044),
  'full' - controls 1..21 (every whole-year rotation of the 22-year record).
Modes:
  noise  - a field of pure noise on a real field's geometry (cells, months in use), smooth in space and persistent in time,
           standardised and zeroed as the rule does, 1994 zero; candidates: the ONI and 31 decoys from decoy.make.
  white  - the same noise field, but the 32 candidates are independent white noise (no persistence).
  real   - the real fitting-year field (1982-2003 only) with 32 fresh decoys from decoy.make and no ONI (kind 2 on fresh seeds).
  trend  - noise mode plus a common linear trend in the raw noise before standardising.
  no94   - noise mode with 1994 left as noise instead of zero.
  realdt - real mode, with each cell's calendar month detrended over the 21 years with data (a straight line in the year removed where the month is in use).
Usage: q4_sim.py MODE FIELD FIRST_SEED N OUT.jsonl"""
import json, sys
import numpy as np
sys.path.insert(0, "src")
from causal_atlas import links, decoy, fire
from causal_atlas.screen import gate

FIT = 264
YEARS = np.array([v for v in range(1, 22) if v != 12])
ALL = list(range(1, 22))
CUT = [s for s in ALL if s not in (1, 21)]


def noise_field(rng, lat, lon, used, trend=0.0, zero94=True, scale=2.0, phi=0.6, yearly=0.3):
    """Smooth in space (Gaussian random features, length scale about `scale` degrees), AR(1) month to month plus an AR(1) year-to-year part."""
    k = 300
    w = rng.normal(0, 1 / scale, (k, 2))
    ph = rng.uniform(0, 2 * np.pi, k)
    basis = np.sqrt(2 / k) * np.cos(np.c_[lat, lon * np.cos(np.radians(lat))] @ w.T + ph)  # cells x k
    e = rng.standard_normal((FIT, k))
    a = np.zeros((FIT, k))
    for t in range(FIT):
        a[t] = (phi * a[t - 1] if t else 0) + e[t]
    yr = np.zeros((22, k)); ey = rng.standard_normal((22, k))
    for j in range(22):
        yr[j] = (yearly * yr[j - 1] if j else 0) + ey[j]
    a = a / a.std() + np.repeat(yr, 12, axis=0) / yr.std() * 0.5
    v = (basis @ a.T) + 0.5 * rng.standard_normal((len(lat), FIT))  # plus cell-level noise
    v += trend * np.linspace(-1, 1, FIT)[None, :] * v.std()
    v = v.reshape(len(lat), 22, 12)
    mu, sd = v.mean(1, keepdims=True), v.std(1, keepdims=True)
    z = (v - mu) / sd
    z = np.where(used[:, None, :], z, 0)
    if zero94:
        z[:, 12] = 0
    return np.clip(z, -3, 3).reshape(len(lat), -1)


def detrend(y, used):
    v = y.reshape(len(y), 22, 12).copy()
    yrs = np.array([j for j in range(22) if j != 12])
    t = yrs - yrs.mean()
    slope = (v[:, yrs] * t[None, :, None]).sum(1) / (t * t).sum()
    v[:, yrs] -= slope[:, None, :] * t[None, :, None] * used[:, None, :]
    return v.reshape(len(y), -1)


def stats(y, drivers, lat, lon):
    ym = links.by_month(y, YEARS)
    t = np.stack([links.strengths(ym, x, YEARS, ALL).sum(axis=(1, 2)) for x in drivers])  # drivers x 22
    tm = links.by_month(links.tiles(lat, lon) @ y, YEARS)
    e = np.stack([links.sharpest(tm, x, YEARS, ALL)[0] for x in drivers])
    return t, e


def gates(t, e, controls):
    cols = [0] + controls
    b, _, _ = gate(t[:, cols])
    s, _ = links.step_down(e[:, cols])
    return b, s


if __name__ == "__main__":
    mode, name, first, n, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    yreal, lat, lon, used = fire.box(name)
    yreal = yreal[:, :FIT].astype(np.float64)
    oni = fire.oni()
    for seed in range(first, first + n):
        rng = np.random.default_rng(seed)
        if mode in ("real", "realdt"):
            y = detrend(yreal, used) if mode == "realdt" else yreal
            drivers = list(decoy.make(seed, fire.MONTHS, oni, count=32)[:, :FIT])
        else:
            y = noise_field(rng, lat, lon, used, trend=1.0 if mode == "trend" else 0.0, zero94=mode != "no94")
            if mode == "white":
                drivers = list(rng.standard_normal((32, FIT)))
            else:
                drivers = [oni[:FIT], *decoy.make(seed, fire.MONTHS, oni)[:, :FIT]]
        t, e = stats(y, drivers, lat, lon)
        r = {"mode": mode, "field": name, "seed": seed}
        for label, c in (("cut", CUT), ("full", ALL)):
            b, s = gates(t, e, c)
            r[label] = {"broad": b, "sharp": s}
        # where in the 22 rotations the largest value of each gate sits (0 = unshifted): for the exchangeability check
        r["argmax_broad_rot"] = int(np.argmax(((t - t.mean(1, keepdims=True)) / t.std(1, ddof=1, keepdims=True)).max(0)))
        r["argmax_sharp_rot"] = int(np.argmax(e.max(0)))
        with open(out, "a") as f:
            f.write(json.dumps(r) + "\n")
