"""Synthetic monthly count panels with optional planted lagged links.

generate(panel, lat, lon, seed) -> dict   (see synth/SPEC.md for the contract)

Only numpy and the standard library are used.  Every spatial field is a
function of (lat, lon) and the seed alone (random Fourier features), so any
subset of cells sees the same underlying world.
"""
import numpy as np

T = 435            # Jan 1989 .. Mar 2025
BURN = 36          # months simulated before index 0 (multiple of 12), discarded
PANELS = ("planted_1.05", "planted_1.15", "planted_1.40", "pure_null", "shared_null")

# ---- tunable parameters (calibrated on pure_null, see README) ---------------
P = dict(
    # latent base rate: log mu0 = b0 + s_a*f_a + s_b*f_b + s_h*max(f_h-1, 0)
    b0=-14.4, s_a=1.8, L_a=4.0, s_b=2.6, L_b=1.0, s_h=3.0, L_h=2.5,
    # seasonality of the count rate (log amplitude; phase varies smoothly in space)
    seas_amp=0.5, seas_amp_shared=0.8,
    # self-excitation: rate = exp(link) * (mu + min(A_f*Sf + A_s*Ss + A_n*Sn, exc_cap))
    # where S are decaying sums of y**zpow (own cell; Sn from the 8 neighbours)
    A_f=0.6, d_f=0.5, A_s=0.006, d_s=0.97, A_n=0.05, d_n=0.5, zpow=0.6, exc_cap=80.0,
    # negative binomial dispersion: var = m + phi*m^2; hard cap on the rate
    phi=4.0, rate_cap=300.0,
    # long regional episodes, then short intense bursts (log-rate amplitude ~ |N(m, sd)|)
    n_ep=130, ep_rad=(2.0, 8.0), ep_dur_med=30.0, ep_dur_sig=1.2, ep_amp=(1.8, 0.6),
    n_mega=20, mega_dur_med=70.0, mega_amp=(2.0, 0.3),
    n_burst=300, burst_rad=(0.7, 2.5), burst_dur_med=3.0, burst_amp=(3.0, 2.0),
    # slow regional component: smooth spatial field, AR(1) over months, unrelated to inputs
    s_slow=2.2, slow_L=6.0, slow_phi_f=0.98, slow_w=0.85,
    # inputs
    drought_L=6.5, drought_slow=0.18, drought_phi_fast=0.68, drought_phi_slow=0.97,
    drought_sd=0.94,
    oni_r=0.93, oni_period=42.0, oni_noise=0.12, oni_sd=0.85,
    # link design
    link_share_thr=1.0, link_L=6.0, link_threshold=1.0, link_cap=3.0,
    # shared_null extras
    shared_trend_counts=0.9, shared_trend_drought=0.8, shared_seas_drought=0.7,
)

# irregular distributed lags (index = lag in months); little at 0-2, mass at 3-9,
# a long tail to 12.  Normalised below.
W_DROUGHT = np.array([0.00, 0.02, 0.04, 0.14, 0.05, 0.22, 0.18, 0.04, 0.12, 0.10, 0.02, 0.07, 0.00])
W_ONI = np.array([0.00, 0.00, 0.03, 0.02, 0.10, 0.06, 0.20, 0.08, 0.24, 0.05, 0.14, 0.00, 0.08])
W_DROUGHT = W_DROUGHT / np.sqrt((W_DROUGHT ** 2).sum())   # L2 normalised, re-standardised empirically
W_ONI = W_ONI / np.sqrt((W_ONI ** 2).sum())


def _rng(seed, key):
    return np.random.default_rng([int(seed), int(key)])


class _Field:
    """Spatial Gaussian field, approx unit variance, kernel ~ exp(-d/L) (Matern 1/2),
    as random Fourier features.  Pure function of (lat, lon, seed, key)."""

    def __init__(self, seed, key, L, M=400, kernel="exp"):
        r = _rng(seed, key)
        z = r.standard_normal((M, 2))
        if kernel == "exp":       # multivariate t, 1 dof  <->  exp(-d/L) in 2-D
            z = z / np.sqrt(r.chisquare(1, size=(M, 1)))
        self.w = z / L
        self.ph = r.uniform(0, 2 * np.pi, M)
        self.M = M

    def phi(self, lat, lon):
        x = np.stack([lat, lon], 1)
        return np.sqrt(2.0 / self.M) * np.cos(x @ self.w.T + self.ph)

    def __call__(self, lat, lon):
        return self.phi(lat, lon).sum(1)


def _smooth_field_series(seed, key, lat, lon, L, TT, phi_f, phi_s, w_slow, M=400):
    """C x TT field, spatially ~exp(-d/L), temporally fast+slow AR(1), unit variance."""
    r = _rng(seed, key)
    z = r.standard_normal((M, 2))
    z = z / np.sqrt(r.chisquare(1, size=(M, 1)))
    w = z / L
    ph = r.uniform(0, 2 * np.pi, M)
    Phi = np.sqrt(2.0 / M) * np.cos(np.stack([lat, lon], 1) @ w.T + ph)    # C x M
    e1 = r.standard_normal((TT + 100, M))
    e2 = r.standard_normal((TT + 100, M))
    a = np.zeros((TT + 100, M)); b = np.zeros((TT + 100, M))
    sf = np.sqrt(1 - phi_f ** 2); ss = np.sqrt(1 - phi_s ** 2)
    for t in range(1, TT + 100):
        a[t] = phi_f * a[t - 1] + sf * e1[t]
        b[t] = phi_s * b[t - 1] + ss * e2[t]
    A = (np.sqrt(1 - w_slow) * a + np.sqrt(w_slow) * b)[100:]               # TT x M
    return Phi @ A.T                                                       # C x TT


def _oni_series(seed, TT):
    """Stochastic oscillator (period ~ 4+ years) plus a little persistent noise."""
    r = _rng(seed, 20)
    n = TT + 300
    rr, th = P["oni_r"], 2 * np.pi / P["oni_period"]
    p1, p2 = 2 * rr * np.cos(th), -rr ** 2
    x = np.zeros(n); e = r.standard_normal(n)
    for t in range(2, n):
        x[t] = p1 * x[t - 1] + p2 * x[t - 2] + e[t]
    x = x[300:]
    x = x / x.std()
    u = np.zeros(n - 300); e2 = r.standard_normal(n)[300:]
    for t in range(1, n - 300):
        u[t] = 0.9 * u[t - 1] + np.sqrt(1 - 0.81) * e2[t]
    s = np.sqrt(1 - P["oni_noise"]) * x + np.sqrt(P["oni_noise"]) * u
    return s / s.std() * P["oni_sd"]


def _episodes(seed, lat, lon, TT):
    """C x TT additive log-rate: long regional episodes plus short intense bursts.
    Independent of every input."""
    out = np.zeros((len(lat), TT))
    specs = [
        # (key, n, radius range, median duration, duration log-sd, amp mean, amp sd, amp dist)
        (30, P["n_ep"], P["ep_rad"], P["ep_dur_med"], P["ep_dur_sig"], P["ep_amp"][0], P["ep_amp"][1]),
        (32, P["n_mega"], (4.0, 8.0), P["mega_dur_med"], 0.4, P["mega_amp"][0], P["mega_amp"][1]),
        (31, P["n_burst"], P["burst_rad"], P["burst_dur_med"], 0.5, P["burst_amp"][0], P["burst_amp"][1]),
    ]
    for key, n, rr, dmed, dsig, am, asd in specs:
        r = _rng(seed, key)
        cl = r.uniform(-36, 39, n); co = r.uniform(-19, 53, n)
        rad = r.uniform(*rr, n)
        t0 = r.uniform(0, TT, n) - 20
        dur = np.clip(np.exp(np.log(dmed) + dsig * r.standard_normal(n)), 2, 120)
        amp = np.abs(am + asd * r.standard_normal(n))
        for k in range(n):
            d2 = (lat - cl[k]) ** 2 + ((lon - co[k]) * np.cos(np.deg2rad(cl[k]))) ** 2
            wsp = np.exp(-0.5 * d2 / (rad[k] / 1.5) ** 2)
            idx = np.where(wsp > 0.03)[0]
            ts = np.arange(max(0, int(np.ceil(t0[k]))), min(TT, int(t0[k] + dur[k]) + 1))
            if idx.size == 0 or ts.size == 0:
                continue
            tw = np.sin(np.pi * np.clip((ts - t0[k]) / dur[k], 0, 1)) ** 0.5
            out[np.ix_(idx, ts)] += amp[k] * np.outer(wsp[idx], tw)
    return out


def _nb8(z, iy, ix, shape):
    """Mean of the 8 neighbours' values on the 0.5-degree raster, evaluated at the cells."""
    g = np.zeros(shape)
    g[iy, ix] = z
    s = np.zeros(shape)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy or dx:
                s += np.roll(np.roll(g, dy, 0), dx, 1)
    return s[iy, ix] / 8.0


def generate(panel, lat, lon, seed):
    if panel not in PANELS:
        try:
            ok = panel.startswith("planted_") and float(panel[8:]) > 0
        except ValueError:
            ok = False
        if not ok:
            raise ValueError(panel)
    lat = np.asarray(lat, float); lon = np.asarray(lon, float)
    C = len(lat); TT = T + BURN
    shared = panel == "shared_null"
    month = np.arange(TT) % 12                       # BURN % 12 == 0, so aligned

    # ---- inputs (identical in every panel for a given seed, except shared extras)
    drought = _smooth_field_series(seed, 10, lat, lon, P["drought_L"], TT,
                                   P["drought_phi_fast"], P["drought_phi_slow"], P["drought_slow"])
    drought *= P["drought_sd"]
    oni = _oni_series(seed, TT)

    # shared drivers (only shared_null): seasonal cycle and slow regional trend
    f_ph = _Field(seed, 40, 15.0)
    ph_c = 6.0 + 4.0 * np.tanh(f_ph(lat, lon))        # smooth phase in months
    seas_shape = np.cos(2 * np.pi * (month[None, :] - ph_c[:, None]) / 12.0)
    f_tr = _Field(seed, 41, 12.0)
    g_c = f_tr(lat, lon)
    trend = np.linspace(-1, 1, TT)[None, :]
    if shared:
        drought = drought + P["shared_seas_drought"] * seas_shape + P["shared_trend_drought"] * g_c[:, None] * trend

    # ---- latent log rate
    fa = _Field(seed, 50, P["L_a"])(lat, lon)
    fb = _Field(seed, 51, P["L_b"])(lat, lon)
    fh = _Field(seed, 52, P["L_h"])(lat, lon)
    logmu0 = P["b0"] + P["s_a"] * fa + P["s_b"] * fb + P["s_h"] * np.maximum(fh - 1.0, 0.0)
    amp = P["seas_amp_shared"] if shared else P["seas_amp"]
    slow = _smooth_field_series(seed, 53, lat, lon, P["slow_L"], TT, P["slow_phi_f"], 0.99, P["slow_w"], M=250)
    logm = logmu0[:, None] + amp * seas_shape + _episodes(seed, lat, lon, TT) + P["s_slow"] * slow
    del slow
    if shared:
        logm = logm + P["shared_trend_counts"] * g_c[:, None] * trend
    mu = np.exp(logm)
    del logm

    # ---- planted link
    linked = np.zeros(C, bool)
    link = None
    if panel.startswith("planted_"):
        R = float(panel.split("_")[1])
        f_l = _Field(seed, 60, P["link_L"])(lat, lon)
        linked = f_l > P["link_share_thr"]
        idx = np.where(linked)[0]
        if idx.size:
            f_a = _Field(seed, 61, 10.0)(lat[idx], lon[idx])
            alpha = 1 / (1 + np.exp(-1.5 * f_a))           # drought share of the link
            Ud = np.zeros((idx.size, TT))
            for L, w in enumerate(W_DROUGHT):
                if w:
                    Ud[:, L:] += w * (-drought[idx][:, :TT - L])    # dry = negative index
            Uo = np.zeros(TT)
            for L, w in enumerate(W_ONI):
                if w:
                    Uo[L:] += w * oni[:TT - L]
            Ud /= Ud[:, BURN:].std(); Uo = (Uo - Uo[BURN:].mean()) / Uo[BURN:].std()
            Ud = Ud - Ud[:, BURN:].mean()
            u = np.sqrt(alpha)[:, None] * Ud + np.sqrt(1 - alpha)[:, None] * Uo[None, :]
            u[:, :12] = 0.0                                  # lags not fully observed in burn-in
            link = np.zeros((C, TT))
            link[idx] = np.log(R) * np.clip(u - P["link_threshold"], 0, P["link_cap"])

    # ---- count process
    rng = _rng(seed, 70)
    iy = np.round((lat - lat.min()) / 0.5).astype(int) + 1
    ix = np.round((lon - lon.min()) / 0.5).astype(int) + 1
    shape = (iy.max() + 2, ix.max() + 2)
    y = np.zeros((C, TT), np.int64)
    rate = np.zeros((C, TT)); rate_nl = np.zeros((C, TT))
    Sf = np.zeros(C); Ss = np.zeros(C); Sn = np.zeros(C)
    ig = 1.0 / P["phi"]
    for t in range(TT):
        exc = P["A_f"] * Sf + P["A_s"] * Ss + P["A_n"] * Sn
        base = mu[:, t] + np.minimum(exc, P["exc_cap"])
        r_t = base if link is None else base * np.exp(link[:, t])
        r_t = np.minimum(r_t, P["rate_cap"])            # the mean actually used for the draw
        rate_nl[:, t] = np.minimum(base, P["rate_cap"]); rate[:, t] = r_t
        lam = r_t * rng.gamma(ig, P["phi"], C)
        y[:, t] = rng.poisson(lam)
        z = y[:, t].astype(float) ** P["zpow"]
        Sf = P["d_f"] * Sf + z
        Ss = P["d_s"] * Ss + z
        Sn = P["d_n"] * Sn + _nb8(z, iy, ix, shape)

    out = dict(y=y[:, BURN:], drought=drought[:, BURN:], oni=oni[BURN:],
               rate=rate[:, BURN:], rate_no_link=rate_nl[:, BURN:], linked=linked)
    return out
