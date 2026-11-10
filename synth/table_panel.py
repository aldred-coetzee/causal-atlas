"""Made-up places-by-years-by-series tables with planted lagged links (rule 3).

Shares no code or assumptions with the methods tested on it; numpy only.
Built from docs/specs/2026-11-10-made-up-tables.md.
"""
import numpy as np

BURN = 50
KINDS = ("steady", "threshold", "extremes", "pair", "flip", "many", "hidden", "same_year", "none")
LOAD = {"many": 0.1, "hidden": 0.5}  # share of an input's variance that the hidden mover supplies


def _draw(rng, shape, heavy):
    """Unit-variance shocks: Student t with 4 degrees of freedom if heavy, else normal."""
    if heavy:
        return rng.standard_t(4, size=shape) / np.sqrt(2.0)
    return rng.standard_normal(shape)


def _ar(e, phi0, phi1, spread, switch_at, changed, fac, rows):
    """Run the autoregression for the given series rows, with a change of behaviour in some places."""
    S, P, T = e[rows].shape
    d = np.zeros((S, P))
    out = np.empty((S, P, T))
    for t in range(T):
        sw = changed & (t >= switch_at)
        phi = np.where(sw[None, :], phi1[rows], phi0[rows][:, None])
        scale = spread[rows] * np.sqrt(1 - phi ** 2) * np.where(sw[None, :], fac[rows], 1.0)
        d = phi * d + scale * e[rows][:, :, t]
        out[:, :, t] = d
    return out


def _std(sig, linked):
    """Centre and scale a signal to mean zero, variance one over the linked place-years."""
    part = sig[linked]
    return (sig - part.mean()) / part.std()


def _zscore(x, years):
    """Departure from the place's own kept-years mean in its own spreads; also returns centre and spread."""
    kept = x[:, BURN:BURN + years]
    c, s = kept.mean(axis=1), kept.std(axis=1)
    return (x - c[:, None]) / s[:, None], c, s


def make(seed, kind, share=0.35, places=120, years=60, outcomes=8, local=24, shared=8,
         links=3, frac=0.25, source="local", flip="place", rough=1.0, nuisance=1.0, gaps=0.0):
    """Return a made-up table and its planted links as a dict (see the brief for the keys).

    Keys beginning with an underscore are for tests only: `_shocks` (series, places, years)
    is each series' year-to-year shock in units of its own spread, after any link is
    applied; `_signals` is one (places, years) array per planted link.
    """
    if kind not in KINDS:
        raise ValueError(kind)
    ss = dict(zip(("base", "layout", "nuis", "links", "rough", "gaps", "hidden"),
                  np.random.SeedSequence(seed).spawn(7)))
    rng = {k: np.random.default_rng(v) for k, v in ss.items()}
    S, P, T = outcomes + local + shared, places, years + BURN
    O = np.arange(outcomes)
    L = np.arange(outcomes, outcomes + local)
    H = np.arange(outcomes + local, S)
    role = np.array(["outcome"] * outcomes + ["local"] * local + ["shared"] * shared)
    group = np.arange(P) // 5
    G = group.max() + 1
    nz = nuisance > 0
    heavy = rough > 0

    # layout: which series carry nuisances; planted links only use the rest
    r = rng["layout"]
    drift_out = r.permutation(O)[:2]
    out_free = np.array([o for o in r.permutation(O) if o not in drift_out])
    lperm = r.permutation(L)
    drift_in, copies, free = lperm[:2], lperm[2:4], lperm[4:]
    sources = r.choice(free, 2, replace=False)

    # base world
    b = rng["base"]
    phi0 = b.uniform(0.2, 0.7, S)
    phi0[b.choice(H, 2, replace=False)] = b.uniform(0.85, 0.95, 2)
    sd = b.uniform(0.5, 3.0, S)
    m_s = b.normal(10, 5, S)
    sp_noise, mu_noise = b.standard_normal((S, P)), b.standard_normal((S, P))
    idio = _draw(b, (S, P, T), heavy)
    grp = _draw(b, (S, G, T), heavy)
    allp = _draw(b, (S, T), heavy)
    e_sh = _draw(b, (shared, T), heavy)
    spread = sd[:, None] * np.exp(0.55 * rough * sp_noise)
    mu = m_s[:, None] + 0.5 * sd[:, None] * mu_noise
    spread[H] = sd[H, None]
    mu[H] = m_s[H, None]
    w_all = np.zeros(S)
    w_all[O] = 0.05
    e = (np.sqrt(0.30) * grp[:, group] + np.sqrt(w_all)[:, None, None] * allp[:, None, :]
         + np.sqrt(0.70 - w_all)[:, None, None] * idio)
    e[H] = e_sh[:, None, :]

    # change of behaviour in a fifth of the places (not in shared series)
    n = rng["nuis"]
    changed = (n.random(P) < 0.2) & nz
    switch_at = BURN + n.integers(25, 46, P)
    fac = np.where(n.random(P) < 0.5, n.uniform(0.4, 0.7, P), n.uniform(1.5, 2.5, P))
    fac = np.broadcast_to(fac, (S, P)).copy()
    fac[H] = 1.0
    dphi = np.where(n.random(P) < 0.5, -0.25, 0.25)
    phi1 = np.clip(phi0[:, None] + dphi[None, :], 0.05, 0.95)
    phi1[H] = phi0[H, None]
    chg = changed.copy()

    # planted links
    lk = rng["links"]
    n_link = max(1, int(round(frac * G)))
    linked_groups = lk.choice(G, n_link, replace=False)
    pmask = np.isin(group, linked_groups)
    plan, used = [], set(drift_out) | set(drift_in)
    pool = H if (source == "shared" and kind not in ("many", "hidden")) else free
    if kind != "none":
        if links > len(out_free):
            raise ValueError("too many links for the outcomes available")
        pool_perm = lk.permutation(pool)
        need = {"pair": 2, "many": 0, "hidden": 1}.get(kind, 1)
        for i in range(links):
            ins = list(pool_perm[i * need:(i + 1) * need]) if kind != "many" else list(lk.permutation(free)[:20])
            if len(ins) < need:
                raise ValueError("not enough input series")
            item = dict(outcome=int(out_free[i]), inputs=ins)
            if kind == "flip":
                if flip == "state":
                    item["state"] = int(lk.permutation([h for h in H if h not in ins])[0])
                else:
                    sg = lk.choice([-1.0, 1.0], P)  # unlinked places get a sign too, unused
                    lp = np.flatnonzero(pmask)
                    half = lk.permutation(lp)[:len(lp) // 2]
                    sg[lp] = 1.0
                    sg[half] = -1.0
                    item["sign"] = sg
            plan.append(item)
            used |= {item["outcome"], *ins} | ({item["state"]} if "state" in item else set())
    # hidden movers: loaded onto inputs in every place
    hr = rng["hidden"]
    hid, load = [], {}
    if kind in LOAD:
        for item in plan:
            h = np.empty((P, T))
            prev = hr.standard_normal(P)
            for t in range(T):
                prev = 0.3 * prev + np.sqrt(1 - 0.09) * hr.standard_normal(P)
                h[:, t] = prev
            hid.append(h)
            for s in item["inputs"]:
                load.setdefault(int(s), []).append(len(hid) - 1)
        for s, ks in load.items():
            tot = LOAD[kind] * len(ks)
            if tot >= 1:
                raise ValueError("too many hidden movers on one series")
            e[s] = np.sqrt(1 - tot) * e[s] + sum(np.sqrt(LOAD[kind]) * hid[k] for k in ks)

    # series first (all but outcomes), then the links onto outcomes, then outcomes
    nonout = np.arange(outcomes, S)
    dev = np.zeros((S, P, T))
    dev[nonout] = _ar(e, phi0, phi1, spread, switch_at, chg, fac, nonout)
    kslice = slice(BURN, BURN + years)
    prev = slice(BURN - 1, BURN + years - 1)
    sigs, truth = [], []
    for k, item in enumerate(plan):
        o, ins = item["outcome"], item["inputs"]
        z = {s: _zscore(dev[s], years) for s in ins + ([item["state"]] if "state" in item else [])}
        extra = {}
        if kind == "steady":
            sig = z[ins[0]][0][:, prev]
        elif kind == "threshold":
            zz = z[ins[0]][0][:, prev]
            q = np.quantile(zz, 0.8, axis=1)
            sig = np.maximum(zz - q[:, None], 0)
            extra = dict(quantile=0.8, level=q)
        elif kind == "extremes":
            zz = z[ins[0]][0][:, prev]
            q = np.quantile(zz, 0.9, axis=1)
            sig = (zz > q[:, None]).astype(float)
            extra = dict(quantile=0.9, level=q)
        elif kind == "pair":
            sig = z[ins[0]][0][:, prev] * z[ins[1]][0][:, prev]
        elif kind == "flip":
            zz = z[ins[0]][0][:, prev]
            if "state" in item:
                sg = np.where(z[item["state"]][0][:, prev] >= 0, 1.0, -1.0)
                extra = dict(state=item["state"])
            else:
                sg = item["sign"][:, None]
                extra = dict(sign=item["sign"])
            sig = zz * sg
        elif kind in LOAD:
            sig = hid[k][:, prev]
        else:  # same_year: the input's own shock at t
            sig = e[ins[0]][:, kslice]
        sig = _std(sig, pmask)
        e[o, :, BURN:] = np.where(pmask[:, None], np.sqrt(1 - share) * e[o, :, BURN:]
                                  + np.sqrt(share) * sig, e[o, :, BURN:])
        sigs.append(sig)
        lag = 0 if kind == "same_year" else 1
        t = dict(outcome=o, inputs=[(int(s), lag) for s in ins], places=pmask.copy(), kind=kind,
                 share=share, predicts=kind != "same_year", changes=kind in
                 ("steady", "threshold", "extremes", "pair", "flip"), **extra)
        if kind in ("steady", "threshold", "extremes", "pair", "flip"):
            t["weights"] = [1.0] * len(ins)
            t["input_centre"] = [mu[s] + z[s][1] for s in ins]
            t["input_spread"] = [z[s][2] for s in ins]
        if kind == "many":
            t["weights"] = [1.0 / len(ins)] * len(ins)
        truth.append(t)
    dev[O] = _ar(e, phi0, phi1, spread, switch_at, chg, fac, O)

    # nuisances act on local and outcome values only
    x = mu[:, :, None] + dev
    x = x[:, :, kslice].copy()
    tau = (np.arange(years) / years)[None, None, :]
    a = n.standard_normal((S, P, 2)) * 2.0
    drift_flag = n.random(S) < 1 / 3
    pair_groups = np.isin(group, n.choice(G, max(1, G // 2), replace=False))
    pair_ab = n.standard_normal((2, P, 2)) * 2.0 * pair_groups[None, :, None]
    step_mask = n.random((S, P)) < 0.1
    step_at = n.integers(15, 46, (S, P))
    step_sz = (1 + n.random((S, P))) * np.where(n.random((S, P)) < 0.5, -1, 1)
    copy_noise = n.standard_normal((2, P, years))
    movable = np.concatenate([O, L])
    if nz:
        planted = used
        for s in movable:
            if drift_flag[s] and s not in planted and s not in drift_out and s not in drift_in:
                x[s] += nuisance * spread[s][:, None] * (a[s, :, :1] * tau[0] + a[s, :, 1:] * tau[0] ** 2)
        for k in range(2):
            for s in (drift_out[k], drift_in[k]):
                x[s] += nuisance * spread[s][:, None] * (pair_ab[k, :, :1] * tau[0] + pair_ab[k, :, 1:] * tau[0] ** 2)
        yrs = np.arange(years)[None, None, :]
        x[movable] += nuisance * (step_mask[movable][:, :, None] * (yrs >= step_at[movable][:, :, None])
                                  * (step_sz[movable] * spread[movable])[:, :, None])
        for c, src, nn in zip(copies, sources, copy_noise):
            x[c] = x[src] + 0.1 * spread[src][:, None] * nn

    # roughness: one-year spikes of several spreads, on local and outcome values
    rr = rng["rough"]
    spike = rr.random((S, P, years)) < 0.01 * rough
    mag = (4 + 4 * rr.random((S, P, years))) * np.where(rr.random((S, P, years)) < 0.5, -1, 1)
    spike[H] = False
    x += spike * mag * spread[:, :, None]

    gp = rng["gaps"]
    if gaps > 0:
        miss = gp.random((S, P, years)) < gaps
        miss[H] = False
        x[miss] = np.nan

    return dict(values=x, role=role, group=group, truth=truth,
                _shocks=e[:, :, BURN:].copy(), _signals=sigs)
