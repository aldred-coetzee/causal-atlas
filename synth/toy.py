"""The toy rung: smooth numbers and a simple lagged link. Shares nothing with the detector (rule 3)."""
import numpy as np

T = 435
BETA = 0.25
LAG_CELL, LAG_GLOBAL = 6, 8
PHI_INPUT, PHI_OUTCOME = 0.6, 0.3


def _ar(rng, shape, phi):
    out = rng.standard_normal(shape)
    for t in range(1, shape[-1]):
        out[..., t] = phi * out[..., t - 1] + np.sqrt(1 - phi * phi) * out[..., t]
    return out


def inputs(cells, seed):
    """A cell input and a global input, each unit variance."""
    rng = np.random.default_rng([seed, 1])
    return _ar(rng, (cells, T), PHI_INPUT), _ar(rng, (1, T), PHI_INPUT)


def generate(lat, lon, seed, linked=True):
    """Outcome y, inputs, and the link's exact effect in each cell and month. A null world has the same inputs and noise, and no link."""
    cells = len(lat)
    rng = np.random.default_rng([seed, 2])
    a, b = inputs(cells, seed)
    north = lat >= np.median(lat)
    effect = np.zeros((cells, T))
    effect[:, LAG_GLOBAL:] += BETA * b[:, :-LAG_GLOBAL]
    effect[north, LAG_CELL:] += BETA * a[north, :-LAG_CELL]
    season = rng.uniform(0, 1, cells)[:, None] * np.sin(2 * np.pi * (np.arange(T) / 12 + rng.uniform(0, 1, cells)[:, None]))
    noise = rng.standard_normal((cells, T))
    wander = np.zeros((cells, T))
    for t in range(1, T):
        wander[:, t] = PHI_OUTCOME * wander[:, t - 1] + noise[:, t]
    y = season + wander + (effect if linked else 0)
    return dict(y=y, a=a, b=b, exact=effect)
