"""Does a country's weather in the months up to a harvest improve the forecast of that harvest beyond the yield's own past? Each year is forecast from the years before it only: the baseline is chosen again, the slopes fitted again and their weights set again. The years are the unit of evidence, and the same forecast made with the weather of other years is the control."""
import numpy as np

from causal_atlas.forecast import DRAWS

SEASONS = ((-1, 9), (-1, 12), (0, 3), (0, 6), (0, 9), (0, 12))  # (year, month): six three-month values of the driver that do not overlap, the eighteen months to the year's end
BASELINES = ("last", "mean3", "mean5", "trend10", "trend20", "linear", "blend")
SCALES = ("own", "country", 1500.0, 4000.0, "all")  # whose past a unit's slopes are fitted on: its own; every cereal in its country; the same cereal within so many km, nearer ones counting for more; the same cereal everywhere
REACH = 1500.0  # km: a unit's neighbours in the baseline
RIDGE = 10.0
CLIP = 4.0
FLOOR = 0.02  # the least scale of a unit, in log yield
LEAST_PAST = 10  # known years before a year, for a unit to be forecast in it
WARM = 5  # years of forecasts behind a year before the scales are weighed and the term is used
SIZE = 0.002  # the least S that is read as a link
KEPT = 1 / 3  # the share of units followed into the later years
LEAST_EARLY = 10  # scored years in the earlier half, for a unit to be ranked
EARTH = 6371.0


def apart(lat, lon):
    a, o = np.radians(lat), np.radians(lon)
    return EARTH * np.arccos(np.clip(np.sin(a)[:, None] * np.sin(a) + np.cos(a)[:, None] * np.cos(a) * np.cos(o[:, None] - o), -1, 1))


def seasons(x, years, upto=len(SEASONS)):
    """Countries by years by season: the driver's value at each of the first `upto` SEASONS. x is monthly and starts in January of the year before the first."""
    t = np.arange(years)
    return np.stack([x[:, 12 * (t + 1 + dy) + m - 1] for dy, m in SEASONS[:upto]], axis=2)


def line(y, span, least):
    """For each unit and year, the straight line through its known values in the `span` years before, read at that year and at the year before; NaN with fewer than `least` of them."""
    units, years = y.shape
    at, before = np.full((units, years), np.nan), np.full((units, years), np.nan)
    for t in range(1, years):
        w = y[:, max(0, t - span) : t]
        ok = np.isfinite(w)
        n = ok.sum(axis=1)
        k = np.arange(w.shape[1]) - w.shape[1]  # -1 is the year before
        km = np.where(ok, k, 0).sum(axis=1) / np.maximum(n, 1)
        ym = np.where(ok, w, 0).sum(axis=1) / np.maximum(n, 1)
        dk = np.where(ok, k - km[:, None], 0)
        den = (dk**2).sum(axis=1)
        slope = (dk * np.where(ok, w - ym[:, None], 0)).sum(axis=1) / np.where(den > 0, den, 1)
        good = (n >= least) & (den > 0)
        at[good, t] = (ym + slope * (0 - km))[good]
        before[good, t] = (ym + slope * (-1 - km))[good]
    return at, before


def recent(y, n):
    """For each unit and year, the mean of its known values in the n years before; NaN if none."""
    out = np.full(y.shape, np.nan)
    for t in range(1, y.shape[1]):
        w = y[:, max(0, t - n) : t]
        ok = np.isfinite(w)
        out[:, t] = np.where(ok.any(axis=1), np.where(ok, w, 0).sum(axis=1) / np.maximum(ok.sum(axis=1), 1), np.nan)
    return out


def scale(y):
    """For each unit and year, the root mean square of its year-on-year changes before that year, floored; NaN with fewer than LEAST_PAST - 1 changes."""
    d = np.diff(y, axis=1)
    ok = np.isfinite(d)
    sq, n = np.cumsum(np.where(ok, d**2, 0), axis=1), np.cumsum(ok, axis=1)
    out = np.full(y.shape, np.nan)
    out[:, 2:] = np.where(n[:, :-1] >= LEAST_PAST - 1, np.sqrt(sq[:, :-1] / np.maximum(n[:, :-1], 1)), np.nan)
    return np.maximum(out, FLOOR)


def neighbours(country, cereal, lat, lon):
    """Units by units: 1 for another unit in the same country, or of the same cereal within REACH."""
    d = apart(lat, lon)[country][:, country]
    nb = ((country[:, None] == country) | ((cereal[:, None] == cereal) & (d <= REACH))).astype(float)
    np.fill_diagonal(nb, 0)
    return nb


def baselines(y, official, nb):
    """Every baseline's forecast of every unit and year, from the years before it. "linear" adds to the twenty-year line what the unit and its neighbours stood above their lines by the year before, with two slopes shared by all units and fitted on official figures of earlier years."""
    units, years = y.shape
    out = {"mean3": recent(y, 3), "mean5": recent(y, 5), "last": recent(y, 1)}
    out["last"] = np.where(np.isfinite(out["last"]), out["last"], out["mean3"])
    out["trend10"], _ = line(y, 10, 6)
    out["trend20"], before = line(y, 20, 8)
    above = np.full((units, years), np.nan)  # how far the year before stood above the line through the years to it
    above[:, 1:] = y[:, :-1] - before[:, 1:]
    ok = np.isfinite(above)
    near = (nb @ np.where(ok, above, 0)) / np.maximum(nb @ ok, 1)
    own = np.where(ok, above, 0)
    lin = np.full((units, years), np.nan)
    target = y - out["trend20"]
    use = official & np.isfinite(target)
    cols = np.stack([own, near], axis=2)
    for t in range(years):
        past = use[:, :t]
        if past.sum() < 50:
            lin[:, t] = out["trend20"][:, t]
            continue
        a = cols[:, :t][past]
        coef = np.linalg.solve(a.T @ a + 1e-6 * np.eye(2), a.T @ target[:, :t][past])
        lin[:, t] = out["trend20"][:, t] + cols[:, t] @ coef
    out["linear"] = lin
    out["blend"] = blend(y, official, out)
    return out


def blend(y, official, made):
    """The mean of the last three years, moved towards each other baseline by a share fitted on official figures of earlier years, one share per baseline for all units."""
    s = scale(y)
    others = [b for b in made if b != "mean3"]
    cols = np.stack([(made[b] - made["mean3"]) / s for b in others], axis=2)
    target = (y - made["mean3"]) / s
    use = official & np.isfinite(target) & np.isfinite(cols).all(axis=2)
    cols, target = np.where(use[:, :, None], np.clip(cols, -CLIP, CLIP), 0), np.where(use, np.clip(target, -CLIP, CLIP), 0)
    g, c = np.cumsum(np.einsum("uti,utj->tij", cols, cols), axis=0), np.cumsum(np.einsum("uti,ut->ti", cols, target), axis=0)
    n = np.cumsum(use.sum(axis=0))
    out = made["mean3"].copy()
    for t in range(1, y.shape[1]):
        if n[t - 1] >= 200:
            coef = np.linalg.solve(g[t - 1] + 1e-6 * np.eye(len(others)), c[t - 1])
            out[:, t] = made["mean3"][:, t] + s[:, t] * (np.clip(np.stack([(made[b][:, t] - made["mean3"][:, t]) / s[:, t] for b in others], axis=1), -CLIP, CLIP) @ coef)
    return np.where(np.isfinite(out), out, made["mean3"])


def pooling(country, cereal, lat, lon):
    """For each of SCALES, units by units: how much each unit's past counts towards another's slopes."""
    d = apart(lat, lon)[country][:, country]
    same = (cereal[:, None] == cereal).astype(float)
    out = []
    for s in SCALES:
        if s == "own":
            out.append(np.eye(len(country)))
        elif s == "country":
            out.append((country[:, None] == country).astype(float))
        elif s == "all":
            out.append(same)
        else:
            out.append(same * np.exp(-((d / s) ** 2)))
    return out


def nonneg(a, b):
    """Weights, none below zero, that bring a @ w nearest b: by coordinate descent on the normal equations."""
    g, c = a.T @ a, a.T @ b
    w = np.zeros(len(c))
    for _ in range(200):
        for j in range(len(c)):
            if g[j, j] > 0:
                w[j] = max(0.0, (c[j] - g[j] @ w + g[j, j] * w[j]) / g[j, j])
    return w


def terms(zb, target, chosen, fc, country, pools, first):
    """For each year from `first` on, the driver's part of the forecast, in units of each unit's scale: slopes at each of SCALES fitted on the years before, and each scale's forecast weighed by how the scales' earlier forecasts did (weights none below zero, shared by all units). zb holds, for each baseline, the outcome less that baseline over the unit's scale (zero where not a target); chosen names the baseline in force each year; fc is countries by years by season, and is brought to mean zero and spread one with each country's years before the year being forecast. Returns the term (units by years, zero before the weights exist) and the weights by year."""
    units, years = target.shape
    k = fc.shape[2]
    f = fc[country]
    m = target[:, :, None]
    c1, c2 = np.cumsum(fc, axis=1), np.cumsum(fc**2, axis=1)
    f1, n = np.cumsum(np.where(m, f, 0), axis=1), np.cumsum(target, axis=1)
    f2 = np.cumsum(np.where(m[:, :, :, None], f[:, :, :, None] * f[:, :, None, :], 0), axis=1)
    fz = {b: np.cumsum(f * v[:, :, None], axis=1) for b, v in zb.items()}
    z1 = {b: np.cumsum(v, axis=1) for b, v in zb.items()}
    per = np.zeros((len(pools), units, years))
    term, weights = np.zeros((units, years)), np.zeros((years, len(pools)))
    for t in range(first, years):
        mu = (c1[:, t - 1] / t)[country]
        sd = np.sqrt(np.maximum(c2[:, t - 1] / t - (c1[:, t - 1] / t) ** 2, 1e-12))[country]
        b = chosen[t]
        gram = f2[:, t - 1] - mu[:, :, None] * f1[:, t - 1][:, None, :] - f1[:, t - 1][:, :, None] * mu[:, None, :] + n[:, t - 1][:, None, None] * mu[:, :, None] * mu[:, None, :]
        gram = gram / (sd[:, :, None] * sd[:, None, :])
        cross = (fz[b][:, t - 1] - mu * z1[b][:, t - 1][:, None]) / sd
        a = (pools @ gram.reshape(units, k * k)).reshape(len(pools), units, k, k) + RIDGE * np.eye(k)
        slope = np.linalg.solve(a, (pools @ cross)[:, :, :, None])[:, :, :, 0]
        per[:, :, t] = np.clip((slope * ((f[:, t] - mu) / sd)[None]).sum(axis=2), -CLIP, CLIP)
        if t - first >= WARM:
            back = target[:, first:t]
            weights[t] = nonneg(per[:, :, first:t][:, back].T, zb[b][:, first:t][back])
            term[:, t] = weights[t] @ per[:, :, t]
    return term, weights


def run(y, official, country, cereal, x, lat, lon, first, upto=len(SEASONS), shifts=None):
    """Forecast every year from `first` on from the years before it. Scored on official figures from year first + WARM. Returns sums by scored year of squared error (in units of each unit's past scale, clipped): the baseline chosen that year, each baseline alone, the model with the driver as it fell, with the driver moved by each of `shifts` whole years (round the record), and the same with each country's and calendar month's mean and straight line taken out of the driver; and by cereal, the weights by year, the baseline chosen by year, and, unit by unit and year by year, which are scored, the baseline's squared error and the model's under the driver as it fell and under each shift."""
    units, years = y.shape
    shifts = list(range(2, years)) if shifts is None else list(shifts)
    s = scale(y)
    base = baselines(y, official, neighbours(country, cereal, lat, lon))
    err = {b: np.clip((y - v) / s, -CLIP, CLIP) for b, v in base.items()}
    target = official & np.all([np.isfinite(e) for e in err.values()], axis=0)
    zb = {b: np.where(target, e, 0) for b, e in err.items()}
    sq = {b: np.cumsum((v**2).sum(axis=0)) for b, v in zb.items()}
    chosen = [min(BASELINES, key=lambda b: sq[b][t - 1]) if t else BASELINES[0] for t in range(years)]
    pools = np.stack(pooling(country, cereal, lat, lon))
    scored = np.arange(first + WARM, years)
    pick = target[:, scored]
    now = np.stack([zb[chosen[t]][:, t] for t in scored], axis=1)

    def errors(drv):
        term, w = terms(zb, target, chosen, seasons(drv, years, upto), country, pools, first)
        return np.where(pick, (now - term[:, scored]) ** 2, 0), w

    def level(drv):
        q = drv.reshape(len(drv), -1, 12).astype(float)
        t = np.arange(q.shape[1]) - (q.shape[1] - 1) / 2
        q = q - q.mean(axis=1, keepdims=True)
        return (q - t[None, :, None] * np.einsum("ctm,t->cm", q, t)[:, None, :] / (t @ t)).reshape(len(drv), -1)

    e, w = errors(x)
    flat = level(x)
    each = np.stack([e] + [errors(np.roll(x, 12 * k, axis=1))[0] for k in shifts], axis=2)
    model = each.sum(axis=0)
    level_model = np.stack([errors(flat)[0].sum(axis=0)] + [errors(np.roll(flat, 12 * k, axis=1))[0].sum(axis=0) for k in shifts], axis=1)
    b = np.where(pick, now**2, 0)
    return {
        "years": scored, "base": b.sum(axis=0), "model": model, "flat": level_model,
        "alone": {k: np.where(pick, zb[k][:, scored] ** 2, 0).sum(axis=0) for k in BASELINES},
        "by_cereal": {int(c): [float(b[cereal == c].sum()), float(e[cereal == c].sum())] for c in np.unique(cereal)},
        "weights": w[scored], "chosen": [chosen[t] for t in scored], "scored": int(pick.sum()),
        "pick": pick, "unit_base": b, "unit_model": each,
    }


def interval(num, den, seed=0, draws=DRAWS):
    """1 - sum(num) / sum(den) and its 95% interval from draws of years."""
    picks = np.random.default_rng(seed).integers(len(den), size=(draws, len(den)))
    boot = 1 - num[picks].sum(axis=1) / den[picks].sum(axis=1)
    return float(1 - num.sum() / den.sum()), [float(v) for v in np.percentile(boot, [2.5, 97.5])]


def reading(r, seed=0):
    """The verdict on one run. S is the share of the baseline's squared error the driver's term removes, with its interval over years. It passes when S is at least SIZE, the interval is above zero, S beats S under every shift, the model's error is also below the mean of its error under the shifts with an interval above zero, all three hold again with the driver's level and line taken out, the model's error is below each baseline's alone, and S is above zero without its best year."""
    out = {}
    for name in ("model", "flat"):
        m = r[name]
        s, ci = interval(m[:, 0], r["base"], seed)
        sh = 1 - m[:, 1:].sum(axis=0) / r["base"].sum()
        ex, ex_ci = interval(m[:, 0], m[:, 1:].mean(axis=1), seed)
        out[name] = {"s": s, "ci": ci, "beats": int((s > sh).sum()), "shifts": int(len(sh)), "shift_mean": float(sh.mean()), "shift_max": float(sh.max()), "excess": ex, "excess_ci": ex_ci,
                     "ok": bool(s >= SIZE and ci[0] > 0 and (s > sh).all() and ex_ci[0] > 0)}
    gain = r["base"] - r["model"][:, 0]
    rest = np.arange(len(gain)) != gain.argmax()
    out["below"] = {b: bool(r["model"][:, 0].sum() < v.sum()) for b, v in r["alone"].items()}
    out["without_best"] = float(1 - r["model"][rest, 0].sum() / r["base"][rest].sum())
    out["passes"] = bool(out["model"]["ok"] and out["flat"]["ok"] and all(out["below"].values()) and out["without_best"] > 0)
    return out


def kept(r, seed=0):
    """Where the driver helped before, does it go on helping? The scored years are halved. Units with LEAST_EARLY scored years in the earlier half are ranked by the share of their baseline error the term removed there, and the top KEPT of them are scored in the later half: S there with its interval over those years, and how many of the shifts, each ranked and scored the same way on its own errors, it beats. Returns also which units were kept."""
    half = len(r["years"]) // 2
    b, m, pick = r["unit_base"], r["unit_model"], r["pick"]
    able = pick[:, :half].sum(axis=1) >= LEAST_EARLY
    late = []
    for j in range(m.shape[2]):
        gain = np.where(able, 1 - m[:, :half, j].sum(axis=1) / np.maximum(b[:, :half].sum(axis=1), 1e-12), -np.inf)
        top = np.argsort(-gain)[: int(round(KEPT * able.sum()))]
        late.append((top, m[top, half:, j].sum(axis=0), b[top, half:].sum(axis=0)))
    s, ci = interval(late[0][1], late[0][2], seed)
    sh = np.array([1 - num.sum() / den.sum() for _, num, den in late[1:]])
    return {"s": s, "ci": ci, "beats": int((s > sh).sum()), "shifts": int(len(sh)), "shift_mean": float(sh.mean()), "units": [int(u) for u in late[0][0]], "ranked": int(able.sum()), "years": [int(r["years"][half]), int(r["years"][-1])]}
