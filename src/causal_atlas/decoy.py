"""Decoy driver series: nothing here is linked to any outcome. Shares no code with the search (rule 3)."""
import numpy as np


def surrogate(x, rng):
    """Same spectrum as x, random phases."""
    f = np.fft.rfft(x - x.mean())
    phase = rng.uniform(0, 2 * np.pi, f.size)
    phase[0] = 0
    if x.size % 2 == 0:
        phase[-1] = 0
    return np.fft.irfft(np.abs(f) * np.exp(1j * phase), x.size)


def ar1(n, phi, rng):
    e = rng.standard_normal(n + 200)
    out = np.zeros(n + 200)
    for t in range(1, n + 200):
        out[t] = phi * out[t - 1] + e[t]
    return out[200:]


def cycle(n, years, damping, rng):
    """A noisy cycle of about the given period: an AR(2) with complex roots."""
    w = 2 * np.pi / (12 * years)
    a, b = 2 * damping * np.cos(w), -damping * damping
    e = rng.standard_normal(n + 400)
    out = np.zeros(n + 400)
    for t in range(2, n + 400):
        out[t] = a * out[t - 1] + b * out[t - 2] + e[t]
    return out[400:]


def make(seed, n, like, count=31):
    """A set of decoys: surrogates of a reference spectrum, AR(1) at mixed persistence, noisy cycles of 2 to 7 years. Each has unit variance."""
    rng = np.random.default_rng(seed)
    out = []
    for i in range(count):
        if i % 3 == 0:
            z = surrogate(like, rng)
        elif i % 3 == 1:
            z = ar1(n, rng.uniform(0.5, 0.98), rng)
        else:
            z = cycle(n, rng.uniform(2, 7), rng.uniform(0.9, 0.98), rng)
        out.append((z - z.mean()) / z.std())
    return np.array(out)
