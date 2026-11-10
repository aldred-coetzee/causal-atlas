"""Where a driver's term has gone with a record's outcome before, as known each year from the years before it, does it go on helping, and by how much? The forecast of causal_atlas.harvest is taken as it stands, record by record and year by year. One thing is added: where a record claims, its term is used at the slope its own earlier years give, and never at more than it stands (CAP): a record's past may shrink its term, not enlarge it. Each year's claim and slope are made from earlier years alone. Intervals draw countries and years again, both."""
import numpy as np

from causal_atlas import harvest
from causal_atlas.forecast import DRAWS

LEVELS = (1.0, 1.5, 2.0)  # standard errors above zero that a record's slope so far must stand, for the record to claim
MAIN = 1.5  # the level the verdict is read at
LEAST = 10  # scored years behind a year, for a record to be able to claim in it
CAP = 1.0  # the most a record's slope may scale its term
FEW = (30, 15)  # records, and countries, that must claim at some time for the claims to be read at all
USABLE = 0.05  # of squared error: from here a usable aid
SMALL = 0.01  # of squared error: below here too small to forecast with


def level(x):
    """The driver with each country's and calendar month's mean and straight line taken out, as harvest.run makes its flat driver."""
    q = x.reshape(len(x), -1, 12).astype(float)
    t = np.arange(q.shape[1]) - (q.shape[1] - 1) / 2
    q = q - q.mean(axis=1, keepdims=True)
    return (q - t[None, :, None] * np.einsum("ctm,t->cm", q, t)[:, None, :] / (t @ t)).reshape(len(x), -1)


def standing(now, term, pick, least=LEAST):
    """For each record, year and column of `term` (the driver as it fell, then each shift): the slope of the outcome less the baseline on the term, through the origin, over the record's scored years before that year; and how many standard errors above zero that slope stands. Slope 0 and standing -inf with fewer than `least` such years, or where the term has been nothing."""
    z, f = np.where(pick, now, 0)[:, :, None], np.where(pick[:, :, None], term, 0)
    n = np.cumsum(pick, axis=1)[:, :, None]
    ff, fz, zz = np.cumsum(f * f, axis=1), np.cumsum(f * z, axis=1), np.cumsum(z * z, axis=1)
    ok = (n >= least) & (ff > 1e-12)
    slope = np.where(ok, fz / np.maximum(ff, 1e-12), 0)
    left = np.maximum(zz - slope * fz, 1e-12) / np.maximum(n - 1, 1)
    t = np.where(ok, slope * np.sqrt(np.maximum(ff, 1e-12) / left), -np.inf)
    a, b = np.zeros(t.shape), np.full(t.shape, -np.inf)
    a[:, 1:], b[:, 1:] = slope[:, :-1], t[:, :-1]
    return a, b


def by_country(a, country):
    out = np.zeros((int(country.max()) + 1,) + a.shape[1:])
    np.add.at(out, country, a)
    return out


def two_way(num, den, seed=0, draws=DRAWS):
    """1 - sum(num) / sum(den), for sums by country and year, and its 95% interval with countries and years both drawn again."""
    rng = np.random.default_rng(seed)
    c, y = num.shape
    boot = np.zeros(draws)
    for i in range(draws):
        w = np.bincount(rng.integers(c, size=c), minlength=c)[:, None] * np.bincount(rng.integers(y, size=y), minlength=y)[None, :]
        d = (w * den).sum()
        if d > 0:
            boot[i] = 1 - (w * num).sum() / d
    return float(1 - num.sum() / den.sum()) if den.sum() > 0 else 0.0, [float(v) for v in np.percentile(boot, [2.5, 97.5])]


def plain(s):
    """A share of squared error as a share of a typical error."""
    return float(1 - np.sqrt(max(1 - s, 0)))


def only(q, keep):
    """A run's parts, record by record, for the records kept: the others ran beside them and are not scored."""
    out = {k: q[k][keep] for k in ("pick", "unit_base", "unit_model", "unit_now", "unit_term")}
    out["unit_alone"] = {k: v[keep] for k, v in q["unit_alone"].items()}
    return out


def pooled(r, f, country, seed=0):
    """harvest.reading's verdict on every record given, with the intervals over countries and years. r is from harvest.run with the driver as it fell, f with level() of it."""
    out = {}
    for name, q in (("model", r), ("flat", f)):
        m, b = q["unit_model"], q["unit_base"]
        s, ci = two_way(by_country(m[:, :, 0], country), by_country(b, country), seed)
        sh = 1 - m[:, :, 1:].sum(axis=(0, 1)) / b.sum()
        ex, ex_ci = two_way(by_country(m[:, :, 0], country), by_country(m[:, :, 1:].mean(axis=2), country), seed)
        out[name] = {"s": s, "ci": ci, "beats": int((s > sh).sum()), "shifts": int(len(sh)), "shift_mean": float(sh.mean()), "shift_max": float(sh.max()), "excess": ex, "excess_ci": ex_ci,
                     "ok": bool(s >= harvest.SIZE and ci[0] > 0 and (s > sh).all() and ex_ci[0] > 0)}
    by_year = r["unit_base"].sum(axis=0) - r["unit_model"][:, :, 0].sum(axis=0)
    rest = np.arange(len(by_year)) != by_year.argmax()
    out["below"] = {b: bool(r["unit_model"][:, :, 0].sum() < v.sum()) for b, v in r["unit_alone"].items()}
    out["without_best"] = float(1 - r["unit_model"][:, rest, 0].sum() / r["unit_base"][:, rest].sum())
    out["passes"] = bool(out["model"]["ok"] and out["flat"]["ok"] and all(out["below"].values()) and out["without_best"] > 0)
    out["size"] = float(min(out["model"]["s"], out["flat"]["s"]))
    return out


def claimed(q, country, at, seed=0):
    """One driver's claims at one level: S on the record-years that claim, each forecast with its term scaled by its record's slope so far (no more than CAP), with its interval; the same for each shift, which claims and scales by its own past; S on the same record-years with the term as it stands; whether the forecast on the claims is below each baseline alone there; and what the claims are made of."""
    now, term, pick = q["unit_now"], q["unit_term"], q["pick"]
    slope, t = standing(now, term, pick)
    cl = (t >= at) & pick[:, :, None]
    b = np.where(pick, now**2, 0)
    m = np.where(cl, (now[:, :, None] - np.clip(slope, 0, CAP) * term) ** 2, 0)
    num, den = m.sum(axis=(0, 1)), (cl * b[:, :, None]).sum(axis=(0, 1))
    sh = np.where(den[1:] > 0, 1 - num[1:] / np.maximum(den[1:], 1e-12), 0.0)  # a shift that claims nothing counts as no gain
    c0 = cl[:, :, 0]
    nc, dc = by_country(m[:, :, 0], country), by_country(c0 * b, country)
    s, ci = two_way(nc, dc, seed)
    gain = (dc - nc).sum(axis=0)
    rest = np.arange(len(gain)) != gain.argmax()
    able = (np.cumsum(pick, axis=1) - pick >= LEAST) & pick
    left = able & ~c0
    as_it_stands = np.where(pick, (now - term[:, :, 0]) ** 2, 0)
    return {"s": s, "ci": ci, "beats": int((s > sh).sum()), "shifts": int(len(sh)), "shift_mean": float(sh.mean()), "shift_max": float(sh.max()),
            "without_best": float(1 - nc[:, rest].sum() / dc[:, rest].sum()) if dc[:, rest].sum() > 0 else 0.0,
            "unscaled": float(1 - (c0 * as_it_stands).sum() / den[0]) if den[0] > 0 else 0.0, "below": {k: bool(num[0] < (c0 * v).sum()) for k, v in q["unit_alone"].items()},
            "figures": int(c0.sum()), "records": int(c0.any(axis=1).sum()), "countries": int((dc.sum(axis=1) > 0).sum()), "share": float(den[0] / max((able * b).sum(), 1e-12)),
            "rest": float(1 - (left * as_it_stands).sum() / (left * b).sum()) if left.any() else 0.0, "claim": c0, "error": m[:, :, 0]}


def reading(r, f, country, seed=0):
    """The verdict on the claims at each of LEVELS. They pass when enough records in enough countries claim (FEW), S on the claims has an interval above zero and beats S under every shift, S stays above zero without its best year, the forecast on the claims is below every baseline alone there, and all of that holds too with the driver's level and line taken out. The size reported is the smaller of S with the driver as it fell and S with its level and line out. Returns by level: both readings (without their masks), whether it passes, the size, and the word for it."""
    out = {}
    for at in LEVELS:
        a, b = claimed(r, country, at, seed), claimed(f, country, at, seed)
        ok = lambda v: bool(v["records"] >= FEW[0] and v["countries"] >= FEW[1] and v["ci"][0] > 0 and v["beats"] == v["shifts"] and v["without_best"] > 0 and all(v["below"].values()))  # noqa: E731
        passes, size = ok(a) and ok(b), float(min(a["s"], b["s"]))
        low = min(a["ci"][0], b["ci"][0])
        word = "not read" if not passes else "too small to forecast with" if size < SMALL else "a real but small aid" if size < USABLE else "a usable aid" if low >= SMALL else "may be a usable aid; not settled"
        out[at] = {"model": {k: v for k, v in a.items() if k not in ("claim", "error")}, "flat": {k: v for k, v in b.items() if k not in ("claim", "error")}, "passes": passes, "size": size, "plain": plain(size), "word": word}
    return out
