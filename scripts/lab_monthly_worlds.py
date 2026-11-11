"""Made-up places-by-months-by-series tables, with a season in every series, each month close to the one before, and links planted at a lag of months (rule 3). For the design of reading by month (docs/specs/2026-11-11-parallel-helpers-second-wave.md, brief E).

Shares no code or assumptions with anything that proposes or scores; numpy only. Imported by the harness part of scripts/lab_monthly.py and by nothing else. synth/table_panel.py makes yearly tables and is not edited; this maker follows its shape (series by places by steps, places in groups of five, outcomes first, then series that differ by place, then series common to all places) so that the same finders and referee can be driven on it.

Kinds of world:
    none        nothing predicts: every series runs by itself
    same_month  an input's own shock of the month enters an outcome the same month: nothing predicts a month ahead beyond the outcome's own months before
    steady      the outcome's shock follows the input as it stood `lag` months before, in every month of the year
    burst       the outcome's shock follows a tail event (beyond the 90th percentile of the place's own) in the input `lag` months before
    window      as steady, in three calendar months of the year only
"""
import numpy as np

BURN = 120  # months run and thrown away before the table begins; a whole number of years
KINDS = ("none", "same_month", "steady", "burst", "window")
MEMORY = {"near": (0.5, 0.9), "loose": (0.2, 0.7), "none": (0.0, 0.0)}  # how much of a month's departure carries to the next


def _draw(rng, shape, heavy):
    """Unit-variance shocks: Student t with 4 degrees of freedom if heavy, else normal."""
    return rng.standard_t(4, size=shape) / np.sqrt(2.0) if heavy else rng.standard_normal(shape)


def _run(e, phi):
    """Each series' departure from its own level, month by month: unit variance, a share phi carried from the month before."""
    d = np.zeros(e.shape[:-1])
    out = np.empty(e.shape)
    for t in range(e.shape[-1]):
        d = phi * d + np.sqrt(1 - phi ** 2) * e[..., t]
        out[..., t] = d
    return out


def make(seed, kind="none", places=120, months=480, outcomes=4, local=12, shared=4, links=2, share=0.35, frac=0.25, lag=3,
         season=1.0, memory="near", wander=0.0, rough=1.0, nuisance=1.0):
    """A made-up monthly table and what was planted in it.

    values: series by places by months, month 0 a January. role: outcome, local or shared for each series. group: each place's group of five. truth: one entry a planted link.
    season: the size of the yearly cycle in every series, in units of the series' own month-to-month spread (0: none). memory: near (each month close to the one before), loose (as a yearly table), none.
    wander: how much the size of a series' season changes from year to year (0: the same every year). lag: months, or several (the outcome follows their mean).
    """
    if kind not in KINDS:
        raise ValueError(kind)
    rng = {k: np.random.default_rng(v) for k, v in zip(("base", "layout", "season", "links", "nuis", "rough"), np.random.SeedSequence(seed).spawn(6))}
    S, P, T = outcomes + local + shared, places, months + BURN
    O, L, H = np.arange(outcomes), np.arange(outcomes, outcomes + local), np.arange(outcomes + local, S)
    role = np.array(["outcome"] * outcomes + ["local"] * local + ["shared"] * shared)
    group = np.arange(P) // 5
    G = int(group.max()) + 1
    heavy = rough > 0

    # the base world: every series by itself
    b = rng["base"]
    lo, hi = MEMORY[memory]
    phi = b.uniform(lo, hi, S)
    slow = b.choice(H, min(2, shared), replace=False)
    if memory == "near":
        phi[slow] = b.uniform(0.93, 0.98, len(slow))  # an index of the kind that holds for many months
    sd = b.uniform(0.5, 3.0, S)
    centre = b.normal(10, 5, S)
    spread = sd[:, None] * np.exp(0.55 * rough * b.standard_normal((S, P)))
    mu = centre[:, None] + 0.5 * sd[:, None] * b.standard_normal((S, P))
    spread[H], mu[H] = sd[H, None], centre[H, None]
    w_all = np.zeros(S)
    w_all[O] = 0.05
    e = (np.sqrt(0.30) * _draw(b, (S, G, T), heavy)[:, group] + np.sqrt(w_all)[:, None, None] * _draw(b, (S, T), heavy)[:, None, :]
         + np.sqrt(0.70 - w_all)[:, None, None] * _draw(b, (S, P, T), heavy))
    e[H] = _draw(b, (shared, T), heavy)[:, None, :]

    # which series carry a slow drift; planted links use the rest
    r = rng["layout"]
    drifting = set(int(s) for s in r.permutation(np.concatenate([O, L]))[: (outcomes + local) // 3])
    out_free = [int(o) for o in r.permutation(O) if int(o) not in drifting]
    in_free = [int(s) for s in r.permutation(L) if int(s) not in drifting]

    # the inputs run first, then the links onto the outcomes' shocks, then the outcomes
    dev = np.zeros((S, P, T))
    rest = np.concatenate([L, H])
    dev[rest] = _run(e[rest], phi[rest, None])
    lk = rng["links"]
    pmask = np.isin(group, lk.choice(G, max(1, int(round(frac * G))), replace=False))
    lags = (lag,) if np.isscalar(lag) else tuple(lag)
    truth = []
    if kind != "none":
        if links > min(len(out_free), len(in_free)):
            raise ValueError("too many links for the series free of drift")
        for i in range(links):
            o, s = out_free[i], in_free[i]
            z = (dev[s] - dev[s, :, BURN:].mean(axis=1, keepdims=True)) / dev[s, :, BURN:].std(axis=1, keepdims=True)
            back = lambda a, k: np.concatenate([np.zeros((P, k)), a[:, : T - k]], axis=1)  # as it stood k months before
            when = np.ones(T, bool)
            extra = {}
            if kind == "same_month":
                sig = e[s].copy()
            elif kind == "burst":
                hit = (z > np.quantile(z[:, BURN:], 0.9, axis=1, keepdims=True)) * 1.0
                sig = sum(back(hit, k) for k in lags) / len(lags)
                extra = {"quantile": 0.9}
            else:
                sig = sum(back(z, k) for k in lags) / len(lags)
                if kind == "window":
                    start = int(lk.integers(0, 12))
                    cal = [(start + j) % 12 for j in range(3)]
                    when = np.isin(np.arange(T) % 12, cal)  # BURN is whole years, so the calendar month of a kept month is its index mod 12
                    extra = {"calendar": cal}
            on = pmask[:, None] & when[None, :] & (np.arange(T) >= BURN - 12)[None, :]
            part = sig[on]
            sig = (sig - part.mean()) / part.std()
            e[o] = np.where(on, np.sqrt(1 - share) * e[o] + np.sqrt(share) * sig, e[o])
            truth.append(dict(outcome=o, inputs=[(s, 0 if kind == "same_month" else k) for k in lags], places=pmask.copy(), kind=kind, share=share, predicts=kind != "same_month", **extra))
    dev[O] = _run(e[O], phi[O, None])

    # the season: a yearly cycle and a smaller half-yearly one, its size and timing a little different in each group of places
    sn = rng["season"]
    amp = season * sn.uniform(0.5, 2.0, S)[:, None] * np.exp(0.25 * sn.standard_normal((S, G)))
    peak = sn.uniform(0, 12, S)[:, None] + 0.7 * sn.standard_normal((S, G))
    half = sn.uniform(0, 6, S)[:, None] + 0.4 * sn.standard_normal((S, G))
    amp[H], peak[H], half[H] = amp[H, :1], peak[H, :1], half[H, :1]
    m = np.arange(T)[None, None, :]
    cycle = np.cos(2 * np.pi * (m - peak[:, :, None]) / 12) + 0.3 * np.cos(4 * np.pi * (m - half[:, :, None]) / 12)
    years = T // 12 + 1
    size = np.zeros((S, G, years))
    step = sn.standard_normal((S, G, years))
    for y in range(1, years):
        size[:, :, y] = 0.6 * size[:, :, y - 1] + 0.8 * step[:, :, y]
    size[H] = size[H, :1]
    grow = np.maximum(1 + wander * size[:, :, np.arange(T) // 12], 0.0)
    x = mu[:, :, None] + spread[:, :, None] * (dev + (amp[:, :, None] * grow * cycle)[:, group])

    # nuisances on outcomes and series that differ by place: a slow drift in a third of the series, a step in a tenth of place-series
    x = x[:, :, BURN:].copy()
    n = rng["nuis"]
    movable = np.concatenate([O, L])
    tau = (np.arange(months) / months)[None, :]
    a = 2.0 * n.standard_normal((S, P, 2))
    step_mask = n.random((S, P)) < 0.1
    step_at = n.integers(months // 4, 3 * months // 4, (S, P))
    step_sz = (1 + n.random((S, P))) * np.where(n.random((S, P)) < 0.5, -1, 1)
    if nuisance > 0:
        for s in movable:
            if int(s) in drifting:
                x[s] += nuisance * spread[s][:, None] * (a[s, :, :1] * tau + a[s, :, 1:] * tau ** 2)
        x[movable] += nuisance * (step_mask[movable][:, :, None] * (np.arange(months)[None, None, :] >= step_at[movable][:, :, None]) * (step_sz[movable] * spread[movable])[:, :, None])

    # roughness: one-month spikes of several spreads
    rr = rng["rough"]
    spike = rr.random((S, P, months)) < 0.003 * rough
    mag = (4 + 4 * rr.random((S, P, months))) * np.where(rr.random((S, P, months)) < 0.5, -1, 1)
    spike[H] = False
    x += spike * mag * spread[:, :, None]

    return dict(values=x, role=role, group=group, truth=truth, memory=phi)
