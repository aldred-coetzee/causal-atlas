"""The referee: every proposal, whatever kind of mathematics found it, is fitted and scored the same way on years no finder saw, and all proposals of a run share one interval, so sending more costs more. docs/plan-finders-and-referee.md, "The referee"; the rule is the other-crops rule (claims.py) made general.
Since decision 0060 each place's baseline is chosen for that place, a place's recent line carried forward is among the baselines, and a proposal must also stand, by a lower mark, on what was new in its inputs against their recent path: a slow path shared by a series and an outcome is the place's own history, not a link. OWN = None, PATH = False and CHECKS = () give the referee as Stage A1 counted it.
Since decision 0061 each pass carries a label: whether it also stands turned round, the outcome a year before for the series, or is as strong read in the same year. Either way it may be two series moving together and not one leading the other. The label is not charged in the bar and neither makes nor unmakes a pass."""
import warnings

import numpy as np

MIN_PAST = 8  # years of its own past before a value has a comparable form
WARM = 10  # years before a baseline's error is used in a fit, and earlier years a place needs before it may claim
RIDGE = 20.0  # added to a slope's sum of squares, in place-years of a unit term: shrinks most where little stands behind the slope
CLAIM = 1.5  # standard errors above zero, in the direction of the pooled slope, for a place to claim in a year
DRAWS = 500  # groups of places and years drawn again, the same draws for every proposal
RATE = 0.05  # in a world where nothing predicts, any pass at all in at most this share of runs
CLIP = 3.0  # a departure of more than this many of a place's usual errors so far, or of a series' own past spreads, counts as this many
FLOOR = 0.25  # no place's usual error is taken as less than this share of the middle place's
GROUPS = 5  # a proposal must apply in at least this many groups of places
YEARS = 10  # and in this many of the scored years
SPAN = 15  # years behind a recent line: shorter follows a bend sooner and costs more of what can be heard
OWN = 10.0  # years of every place's error that stand beside a place's own when its baseline is chosen; None: one baseline for all places
PATH = True  # whether a place's recent line carried forward is among the baselines
READS = ("mean", "line")  # the forms of its inputs a proposal is read in and held to the bar in
CHECKS = ("recent",)  # forms it is read in beside, not charged in the bar: it must still stand LEAST of its own spreads above zero there, and take something off the baseline's error
LEAST = 2.0  # of its own spreads above zero, for a read that is a check
BACK = 2.0  # of its own spreads above zero, in every read held to the bar, for a passed proposal turned round to count as standing too
FORMS = ("slope", "hinge", "tail", "product", "by_group", "by_state", "mode")


def proposal(outcome, inputs, form="slope", where="all", level=None, groups=None, state=None, weights=None, when=None, event=None, by=None):
    """A link as a description: which outcome, which series how many years before, in what form, where and when. Nothing fitted to the outcome travels with it.
    where: "all", "claim", or a yes or no for each place. level: the share of an input's own past below the line, for hinge, tail and when. groups: a label a place for by_group (below zero: not in).
    state: (series, years before) whose side of its own past mean splits the slope in two. when: (series, years before, level). event: the outcome scored as the chance of standing beyond this level of its own past. by: who posted it."""
    assert form in FORMS, form
    return {"outcome": outcome, "inputs": [tuple(i) for i in inputs], "form": form, "where": where, "level": level, "groups": groups, "state": state, "weights": weights, "when": when, "event": event, "by": by}


def _before(a):
    """The sum over the years before each year."""
    c = np.cumsum(a, axis=-1)
    return np.concatenate([np.zeros_like(c[..., :1]), c[..., :-1]], axis=-1)


def _line(v):
    """For each year, the line through the years before it carried forward to that year, and the spread about that line; and how many years stood behind it."""
    ok = np.isfinite(v)
    x, t = np.where(ok, v, 0.0), np.arange(v.shape[-1], dtype=float)
    n, st, stt, sx, sxt, sxx = (_before(a) for a in (ok * 1.0, ok * t, ok * t * t, x, x * t, x * x))
    with np.errstate(divide="ignore", invalid="ignore"):
        slope = (n * sxt - st * sx) / (n * stt - st * st)
        level = (sx - slope * st) / n
        spread = np.sqrt(np.maximum(sxx - level * sx - slope * sxt, 0) / (n - 2))
    return level + slope * t, spread, n


def _recent(v, span=None):
    """For each year, the line through the last SPAN years before it carried forward to that year; the spread is how far the series has stood from that line in the years before (root mean square), so it carries what carrying a line forward costs; and how many such years there were."""
    span = SPAN if span is None else span
    ok = np.isfinite(v)
    x, t = np.where(ok, v, 0.0), np.arange(v.shape[-1], dtype=float)

    def last(a):
        c = _before(a)
        c[..., span:] = c[..., span:] - c[..., :-span]
        return c

    n, st, stt, sx, sxt = (last(a) for a in (ok * 1.0, ok * t, ok * t * t, x, x * t))
    with np.errstate(divide="ignore", invalid="ignore"):
        slope = (n * sxt - st * sx) / (n * stt - st * st)
        centre = (sx - slope * st) / n + slope * t
    centre[(n < MIN_PAST) | ~np.isfinite(centre)] = np.nan
    d = np.where(ok & np.isfinite(centre), v - centre, np.nan)
    have = np.isfinite(d)
    m = _before(have * 1.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        spread = np.sqrt(_before(np.where(have, d * d, 0.0)) / m)
    return centre, spread, m


def _mean(v):
    """For each year, the mean and spread of the years before it; and how many there were."""
    ok = np.isfinite(v)
    x = np.where(ok, v, 0.0)
    n, sx, sxx = _before(ok * 1.0), _before(x), _before(x * x)
    with np.errstate(divide="ignore", invalid="ignore"):
        mean = sx / n
        spread = np.sqrt(np.maximum(sxx - n * mean * mean, 0) / (n - 1))
    return mean, spread, n


def comparable(v, form="mean"):
    """Each value as its departure from its own past, in units of its own past spread, from earlier years only: from its past mean; from its past line carried forward; or from the line through its last SPAN years carried forward, which follows a slow path of any smooth shape. No departure counted as more than CLIP spreads, so that one wild figure cannot speak for a series. The one form in which series of different kinds are set beside each other."""
    centre, spread, n = {"mean": _mean, "line": _line, "recent": _recent}[form](v)
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (v - centre) / spread
    out[(n < MIN_PAST) | ~np.isfinite(out)] = np.nan
    return np.clip(out, -CLIP, CLIP)


def _level(c, q):
    """For each year, the level that the share q of the series' own earlier values lie below."""
    out = np.full(c.shape, np.nan)
    for t in range(2 * MIN_PAST, c.shape[-1]):
        out[..., t] = np.nanquantile(c[..., :t], q, axis=-1)
    return out


def _lag(c, years):
    """The series as it stood that many years before."""
    out = np.full(c.shape, np.nan)
    out[..., years:] = c[..., : c.shape[-1] - years] if years else c
    return out


def _beyond(c, q):
    """Whether a value stands beyond the level q of its own past: above it for the upper half, below for the lower."""
    lv = _level(c, q)
    return np.where(np.isfinite(c) & np.isfinite(lv), (c > lv) if q >= 0.5 else (c < lv), False), lv


def terms(p, comp):
    """The proposal's terms, one number a place and year each, known before the year; several only where the form gives each group or state a slope of its own, and then no two speak in the same place-year. Zero where a term has nothing to say."""
    ins = [_lag(comp[s], k) for s, k in p["inputs"]]
    form = p["form"]
    if form == "product":
        z = ins[0] * ins[1]
    elif form == "mode":
        w = np.ones(len(ins)) if p["weights"] is None else np.asarray(p["weights"], float)
        z = sum(wi * np.nan_to_num(c) for wi, c in zip(w, ins)) / np.sqrt((w * w).sum())
        z[~np.all([np.isfinite(c) for c in ins], axis=0)] = np.nan
    elif form in ("hinge", "tail"):
        s, k = p["inputs"][0]
        hit, lv = _beyond(comp[s], p["level"])
        side = 1.0 if p["level"] >= 0.5 else -1.0
        z = _lag(np.where(hit, side * (comp[s] - lv) if form == "hinge" else 1.0, np.where(np.isfinite(lv) & np.isfinite(comp[s]), 0.0, np.nan)), k)
    else:
        z = ins[0]
    if p["when"] is not None:
        s, k, q = p["when"]
        z = np.where(_lag(_beyond(comp[s], q)[0], k) > 0, z, 0.0 * z)
    if form == "by_group":
        g = np.asarray(p["groups"])
        out = [np.where((g == i)[:, None], z, 0.0) for i in np.unique(g[g >= 0])]
    elif form == "by_state":
        s, k = p["state"]
        side = _lag(comp[s], k)
        out = [np.where(side > 0, z, 0.0 * side), np.where(side <= 0, z, 0.0 * side)]
    else:
        out = [z]
    return np.nan_to_num(np.array(out))


def _share(u, v):
    """For each year, the slope of u on v over all places and earlier years: how much of a departure carries over."""
    ok = np.isfinite(u) & np.isfinite(v)
    num, den = _before(np.where(ok, u * v, 0).sum(axis=0)), _before(np.where(ok, v * v, 0).sum(axis=0))
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.nan_to_num(num / den)


def _group_before(y, group):
    """Each place's group mean the year before."""
    out = np.full(y.shape, np.nan)
    for g in np.unique(group):
        ok = np.isfinite(y[group == g])
        with np.errstate(invalid="ignore"):
            m = np.where(ok, y[group == g], 0.0).sum(axis=0) / ok.sum(axis=0)  # nan in a year the group has nothing
        out[group == g, 1:] = m[:-1]
    return out


def baselines(y, group):
    """What a place's own history and its group say about next year, six ways: its past mean; its last value; its mean with a share of its last departure; its own line; its group's mean the year before; and, with PATH, the line through its last SPAN years. And for each place and year, which had the least squared error over the years before: the baseline is chosen again every year, from the past alone."""
    mean, _, n = _mean(y)
    last = _lag(y, 1)
    b = np.array([mean, last, mean + _share(y - mean, last - mean) * (last - mean), _line(y)[0], _group_before(y, group), _recent(y)[0]][: 6 if PATH else 5])
    b[:, n < 3] = np.nan
    return b, _choose(y, b)


def chances(e, group, rate):
    """The same for an event: the rate by construction; the place's own past rate; that with a share of last year's departure; its group's rate the year before."""
    mean, _, n = _mean(e)
    last = _lag(e, 1)
    b = np.array([np.full(e.shape, rate), mean, mean + _share(e - mean, last - mean) * (last - mean), _group_before(e, group)])
    b[1:, n < 3] = np.nan
    return np.clip(b, 0, 1), _choose(e, np.clip(b, 0, 1))


def _choose(y, b):
    """For each place and year, the baseline with the least squared error in the years before it, from WARM on: the place's own, with OWN years of every place's usual beside it, so that a place with a path of its own gets the baseline that follows it and a place with little to go on gets what serves all places best."""
    usable = np.isfinite(b).any(axis=(1, 2))
    both = np.isfinite(y) & np.isfinite(b[usable]).all(axis=0)  # compared only where every baseline in use has something to say
    err = np.where(both, (y - b) ** 2, 0.0)
    err[:, :, :WARM] = 0.0
    own = _before(err)
    every = own.sum(axis=1)
    count = np.maximum(_before(both * 1.0 * (np.arange(y.shape[1]) >= WARM)).sum(axis=0), 1.0)
    total = every[:, None, :] + 0 * own if OWN is None else own + OWN * (every / count)[:, None, :]
    return np.argmin(np.where(usable[:, None, None], total, np.inf), axis=0)


def _usual(e):
    """Each place's usual error so far: the middle of its absolute errors, on the scale of a spread; the middle place's where a place has too few years, and never less than FLOOR of the middle place's."""
    with np.errstate(invalid="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)  # a place with no error yet has no middle
        s = 1.4826 * np.nanmedian(np.abs(e), axis=1)
        s[np.isfinite(e).sum(axis=1) < MIN_PAST] = np.nan
        mid = np.nanmedian(s) if np.isfinite(s).any() else 1.0
    return np.where(np.isfinite(s), np.maximum(s, FLOOR * mid), mid)


def outcome(v, group, first, event=None):
    """The outcome as it is scored, with its baselines, which is used each year, and for each scored year the baseline's errors up to then.
    A quantity: in units of its own spread over the years the finders saw; its errors then in units of the place's usual error so far, a departure beyond CLIP of them counted as CLIP, so that places count alike and one wild year does not decide a score.
    An event: a yes or no for standing beyond a level of its own past; its errors as they are."""
    if event is not None:
        hit, lv = _beyond(v, event)
        y = np.where(np.isfinite(v) & np.isfinite(lv), hit * 1.0, np.nan)
        b, chosen = chances(y, group, 1 - event if event >= 0.5 else event)
    else:
        early = v[:, :first]
        with np.errstate(invalid="ignore", divide="ignore"):
            y = (v - np.nanmean(early, axis=1, keepdims=True)) / np.nanstd(early, axis=1, keepdims=True)
        y[~np.isfinite(y)] = np.nan
        b, chosen = baselines(y, group)
    past = []
    for t in range(first, y.shape[1]):
        mine = b[chosen[:, t], np.arange(len(y))]
        e = y - mine
        unit = np.ones(len(y)) if event is not None else _usual(e[:, WARM:t])
        u = e[:, WARM : t + 1] / unit[:, None]
        past.append((u if event is not None else np.clip(u, -CLIP, CLIP), unit, mine[:, t]))
    return {"y": y, "past": past, "chosen": chosen, "chance": event is not None}


def score(out, z, where, first, fit="claimed"):
    """One proposal, one form of its inputs: each scored year forecast from the years before it. By place and scored year, where the proposal applies:
    base, the baseline's squared error; gain, what the proposal took off it; agree, the baseline's error times what the proposal added to the forecast (above zero on average only if the term knows something: the sharper statistic, and the one tested);
    plain, the gain and base against the outcome as it fell, nothing counted as less than it was; and how many places claimed each year."""
    y, chance = out["y"], out["chance"]
    places, years = y.shape
    a = {k: np.zeros((places, years - first)) for k in ("gain", "base", "agree", "plain_gain", "plain_base")}
    claims = np.zeros(years - first, int)
    by_claim = isinstance(where, str) and where == "claim"
    inside = np.ones(places, bool) if isinstance(where, str) else np.asarray(where, bool)
    assert not (by_claim and len(z) > 1), "by claim is for a single term"
    for t in range(first, years):
        u, unit, b = out["past"][t - first]
        r, e = u[:, :-1], u[:, -1]
        ok = np.isfinite(r)
        r = np.where(ok, r, 0.0)
        zp = z[:, :, WARM:t] * ok
        szr, szz = (zp * r).sum(axis=2), (zp * zp).sum(axis=2)  # by term and place
        if by_claim:
            n, srr = (ok & (zp[0] != 0)).sum(axis=1), (r * r * (zp[0] != 0)).sum(axis=1)
            with np.errstate(divide="ignore", invalid="ignore"):
                own = szr[0] / szz[0]
                se = np.sqrt(np.maximum(srr - szr[0] ** 2 / szz[0], 0) / (n - 1) / szz[0])
            way = np.sign(szr[0].sum())
            inside = (n >= WARM) & np.isfinite(own) & np.isfinite(se) & (way * own >= CLAIM * se) & (way != 0)
            claims[t - first] = inside.sum()
            fitted = inside if fit == "claimed" else np.ones(places, bool)
        else:
            fitted = inside
        slope = szr[:, fitted].sum(axis=1) / (szz[:, fitted].sum(axis=1) + RIDGE)
        now = z[:, :, t]
        f = (slope[:, None] * now).sum(axis=0)
        if chance:
            f = np.clip(b + f, 0, 1) - b
        on = inside & np.isfinite(e) & (now != 0).any(axis=0)
        k = t - first
        a["gain"][on, k], a["base"][on, k], a["agree"][on, k] = (2 * e * f - f * f)[on], (e * e)[on], (e * f)[on]
        raw, add = y[:, t] - b, unit * f
        a["plain_gain"][on, k], a["plain_base"][on, k] = (2 * raw * add - add * add)[on], (raw * raw)[on]
    return a, claims


def _pool(a, group):
    """Summed within each group of places."""
    return np.array([a[group == g].sum(axis=0) for g in np.unique(group)])


def _draws(groups, years, draws, seed):
    """How many times each group and each year is taken, in each draw: both drawn again, with replacement."""
    rng = np.random.default_rng(seed)
    return rng.multinomial(groups, np.full(groups, 1 / groups), draws).astype(float), rng.multinomial(years, np.full(years, 1 / years), draws).astype(float)


def read(a, group, cg, cy):
    """One form of one proposal, with what the bar needs. s: the share of the baseline's squared error removed, with the middle nine tenths of it over the draws and its value without its best year. k: the tested statistic, the baseline's error times the proposal's addition as a share of the same squared error, with its value in every draw. And how widely the proposal applies."""
    g, b, c = (_pool(a[k], group) for k in ("gain", "base", "agree"))
    total = b.sum()
    with np.errstate(divide="ignore", invalid="ignore"):
        s, k = (g.sum() / total, c.sum() / total) if total > 0 else (np.nan, np.nan)
        den = np.einsum("dg,gy,dy->d", cg, b, cy)
        s_again, k_again = np.einsum("dg,gy,dy->d", cg, g, cy) / den, np.einsum("dg,gy,dy->d", cg, c, cy) / den
    best = np.argmax(g.sum(axis=0))
    rest = np.delete(g, best, axis=1).sum() / max(np.delete(b, best, axis=1).sum(), 1e-12)
    span = [float(v) for v in np.nanquantile(s_again, [0.05, 0.95])] if np.isfinite(s_again).any() else [np.nan, np.nan]
    pg, pb = a["plain_gain"].sum(), a["plain_base"].sum()
    return {"s": float(s), "span": span, "without_best": float(rest), "k": float(k), "again": k_again, "plain": float(pg / pb) if pb > 0 else None,
            "place_years": int((a["base"] > 0).sum()), "places": int((a["base"] > 0).any(axis=1).sum()), "groups": int((b > 0).any(axis=1).sum()), "years": int((b > 0).any(axis=0).sum())}


def bar(reads, rate=RATE):
    """The charge for how many were sent: in each draw, the largest departure of any proposal's tested statistic from its own value, in its own spreads; the bar is the level that all but `rate` of the draws stay under. Near copies depart together and are charged about as one. Returns the bar and each statistic's spread."""
    spread = np.array([np.nanstd(r["again"]) if np.isfinite(r["k"]) else np.nan for r in reads])
    use = np.isfinite(spread) & (spread > 0)
    if not use.any():
        return np.inf, spread
    depart = np.array([(reads[i]["again"] - reads[i]["k"]) / spread[i] for i in np.flatnonzero(use)])
    return float(np.quantile(np.nanmax(np.where(np.isfinite(depart), depart, -np.inf), axis=0), 1 - rate)), spread


def turned(p, values):
    """A proposal turned round: each of its inputs that differs by place as the outcome, with the outcome that many years before, in the same places; the form kept where there is one input, a plain slope otherwise. Empty when every input is one series common to all places."""
    single = len(p["inputs"]) == 1
    out = []
    for s, k in p["inputs"]:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            if not np.nanmax(np.nanstd(values[s], axis=0)) > 1e-9 * np.nanstd(values[s]):
                continue
        kw = {"form": p["form"], "level": p["level"], "groups": p["groups"], "state": p["state"]} if single else {}
        out.append(proposal(s, [(p["outcome"], max(k, 1))], where=p["where"], by=p["by"], **kw))
    return out


def label(values, group, first, p, r, seed=0, draws=DRAWS, fit="claimed"):
    """What a pass may be read as. A pass says the inputs, known beforehand, improve the forecast; it does not say they lead. Two readings beside it, neither charged in the bar and neither able to make or unmake a pass:
    back: the proposal turned round stands too, more than BACK of its own spreads above zero with something off the baseline's error, in every read held to the bar; None when it cannot be turned round.
    same: read with each input as it stood in the outcome's own year, it stands at least as far above zero as with the inputs beforehand.
    together: either. Then the two may only be moving together, and a lead is not shown."""
    def least(x):
        ts = [x[f]["t"] for f in READS]
        return -np.inf if any(t is None for t in ts) else min(ts)

    back = turned(p, values)
    more = judge(values, group, first, back + [{**p, "inputs": [(s, 0) for s, _ in p["inputs"]]}], seed=seed, draws=draws, fit=fit, labels=False)["proposals"]
    stands = [bool(least(x) > BACK and all(x[f]["s"] > 0 for f in READS)) for x in more[:-1]]
    out = {"back": any(stands) if back else None, "same": bool(least(more[-1]) >= least(r)), "back_t": [least(x) for x in more[:-1]], "same_t": least(more[-1]), "t": least(r)}
    return {**out, "together": bool(out["back"] or out["same"])}


def judge(values, group, first, proposals, seed=0, draws=DRAWS, rate=RATE, fit="claimed", shifts=(), labels=True):
    """Every proposal read both ways, with its inputs as they fell and with their past level and line removed, and all of them held to one bar; and read once more as a check, with its inputs against their recent line, which the bar is not charged for.
    A proposal passes when, both ways: its tested statistic stands more than the bar of its own spreads above zero; it took something off the baseline's squared error, and still did without its best year; and it applies widely enough. And when, in the check, the statistic stands more than LEAST of its own spreads above zero and something came off the baseline's error. Its size is the smaller of the two shares removed.
    values: series by places by years. first: the first year scored; finders saw only the years before it. shifts: years to move the inputs by, for the scores reported beside (a weak control alone, decision 0058).
    Each pass carries a label (see `label`): whether it also stands turned round or in the same year, and so may be two things moving together."""
    forms = READS + CHECKS
    comp = {f: comparable(values, f) for f in forms}
    group = np.asarray(group)
    cg, cy = _draws(len(np.unique(group)), values.shape[2] - first, draws, seed)
    outs, reads, beside = {}, [], []
    for p in proposals:
        key = (p["outcome"], p["event"])
        if key not in outs:
            outs[key] = outcome(values[p["outcome"]], group, first, p["event"])
        for f in forms:
            a, claims = score(outs[key], terms(p, comp[f]), p["where"], first, fit)
            reads.append({**read(a, group, cg, cy), "claims": int(claims.sum())})
        beside.append([_shifted(p, comp[READS[0]], k, outs[key], first, fit) for k in shifts])
    held = [j for j in range(len(reads)) if j % len(forms) < len(READS)]
    level, _ = bar([reads[j] for j in held], rate)
    spread = np.array([np.nanstd(r["again"]) if np.isfinite(r["k"]) else np.nan for r in reads])
    out = []
    for i in range(len(proposals)):
        both = []
        for n, j in enumerate(range(len(forms) * i, len(forms) * (i + 1))):
            r = {k: v for k, v in reads[j].items() if k != "again"}
            r["t"] = float(r["k"] / spread[j]) if np.isfinite(spread[j]) and spread[j] > 0 else None
            wide = r["groups"] >= GROUPS and r["years"] >= YEARS and r["t"] is not None
            r["ok"] = bool(wide and r["t"] > (level if n < len(READS) else LEAST) and r["s"] > 0 and (r["without_best"] > 0 or n >= len(READS)))
            both.append(r)
        sizes = [r["s"] for r in both[: len(READS)]]
        out.append({"passes": all(r["ok"] for r in both), "size": float(min(sizes)) if np.all(np.isfinite(sizes)) else None, "fell": both[0], "flat": both[1], **dict(zip(forms, both)), "shifts": beside[i]})
    for p, r in zip(proposals, out):
        r["label"] = label(values, group, first, p, r, seed, draws, fit) if labels and r["passes"] else None
    chosen = {f"{int(k[0])}" + ("" if k[1] is None else f" beyond {k[1]}"): [int(c) for c in np.bincount(o["chosen"][:, first:].ravel(), minlength=5)] for k, o in outs.items()}
    return {"bar": level, "sent": len(proposals), "passed": int(sum(v["passes"] for v in out)), "proposals": out, "chosen": chosen}


def _shifted(p, comp, k, out, first, fit):
    """The proposal's share removed with every input moved k years round its own record."""
    a, _ = score(out, terms(p, np.roll(comp, k, axis=2)), p["where"], first, fit)
    return float(a["gain"].sum() / a["base"].sum()) if a["base"].sum() > 0 else None
