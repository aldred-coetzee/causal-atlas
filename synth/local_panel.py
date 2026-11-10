"""A made-up burned-area record with a made-up local moisture field beside it, for the known-answer check of results/fire-drought.md.

Written from what such records look like, not from how the detector works, and it imports nothing from src (rule 3; tests/test_synth_isolated.py). Three kinds of panel:

- a link: in round patches, burning in the fire season follows the moisture of some months earlier, with a sign of the patch's own. In some patches the lag is the same through the season; in the others the moisture that matters is that of one time of year, so the lag grows as the season goes on;
- none: burning owes nothing to moisture;
- instrument only: burning owes nothing to moisture, but how much the satellite sees does, and what it records is biased by how much it sees;
- trends: burning owes nothing to moisture, but both drift over the record, in the same places and the same direction.

Two more, added after the independent check of 2026-11-10 (docs/reviews/2026-11-10-fire-drought-rule-check/), each from the reader's own panel:

- before: instrument only, but what is recorded depends on how well the month before was seen, not only on this month's share;
- curve: burning owes nothing to moisture, but both drift at a quickening pace.
"""
import numpy as np
from scipy.ndimage import gaussian_filter

ROWS, COLS = 60, 100  # half-degree cells: 30 by 50 degrees
YEARS = 37
ABSENT = 12  # the year with no data, as in the real record
PATCHES = 6
LAGS = (4, 5, 6, 8, 10, 12)  # where the lag is the same through the season
FIRST = (4, 5, 6, 8)  # where it grows through the season: the lag in the season's first month


def smooth(rng, n, scale):
    """n maps of noise, each smooth over about scale cells, unit variance."""
    w = gaussian_filter(rng.standard_normal((n, ROWS, COLS)), sigma=(0, scale, scale), mode="nearest")
    return w / w.std()


def make(seed, share=0.0, instrument=0.0, trend=0.0, cover=0.25, before=0.0, curve=0.0):
    """Returns burned km2 and share observed (cells by years by 12, the absent year NaN), moisture (cells by months), latitude, longitude, and which cells hold a planted link.

    share: the part of the variance of burning's underlying strength, in the patches' fire seasons, that comes from moisture. instrument: how strongly the share observed follows moisture five months before. trend: the size of a slow drift, one wide map of places times a straight line through the record, added alike to moisture and to burning's strength. before: with an instrument effect, what is recorded goes as this month's share times the month before's share to this power, in place of the cube of this month's. curve: the size of a drift that quickens, one wide map of places times the square of the time gone, added alike to moisture and to burning's strength."""
    rng = np.random.default_rng(seed)
    months = 12 * YEARS
    weather = smooth(rng, months + 2, 6)
    moisture = (weather[2:] + weather[1:-1] + weather[:-2]) / np.sqrt(3)  # a three-month index, so neighbouring months overlap
    moisture = moisture.reshape(months, -1).T

    row, col = [g.ravel() for g in np.meshgrid(np.arange(ROWS), np.arange(COLS), indexing="ij")]
    cells = ROWS * COLS
    start = (row * 12 // ROWS + rng.integers(12)) % 12  # the fire season moves with latitude
    month = np.arange(months) % 12
    season = ((month[None, :] - start[:, None]) % 12) < 4

    # What burning owes to itself: fine-grained noise, a shock each year shared over wide areas, and some carry-over from the year before.
    fine = smooth(rng, months, 1).reshape(months, -1).T
    yearly = np.repeat(smooth(rng, YEARS, 10).reshape(YEARS, -1).T, 12, axis=1)
    own = np.sqrt(0.6) * fine + np.sqrt(0.4) * yearly
    own[:, 12:] = np.sqrt(0.85) * own[:, 12:] + np.sqrt(0.15) * own[:, :-12]

    strength = own.copy()
    planted = np.zeros(cells, bool)
    radius = np.sqrt(cover * cells / PATCHES / np.pi)
    for _ in range(PATCHES if share > 0 else 0):
        c = rng.integers(cells)
        inside = (row - row[c]) ** 2 + (col - col[c]) ** 2 <= radius**2
        sign, t, new = rng.choice([-1, 1]), np.arange(12, months), inside & ~planted
        if rng.random() < 0.5:
            lag = np.full((new.sum(), len(t)), rng.choice(LAGS))
        else:
            lag = rng.choice(FIRST) + np.minimum((month[None, t] - start[new, None]) % 12, 3)
        strength[np.ix_(new, t)] = np.sqrt(1 - share) * own[np.ix_(new, t)] + sign * np.sqrt(share) * np.take_along_axis(moisture[new], t[None, :] - lag, axis=1)
        planted |= inside

    if trend:
        slow = trend * smooth(np.random.default_rng([seed, 1]), 1, 12).reshape(-1, 1) * np.linspace(-1, 1, months)[None, :]
        moisture, strength = moisture + slow, strength + slow
    if curve:
        slow = curve * smooth(np.random.default_rng([seed, 2]), 1, 12).reshape(-1, 1) * np.linspace(0, 1, months)[None, :] ** 2
        moisture, strength = moisture + slow, strength + slow

    size = np.exp(rng.normal(3, 1, cells))[:, None]  # km2 in a typical burning month, cell by cell
    drift = 1 + 0.4 * rng.random(cells)[:, None] * (np.arange(months)[None, :] >= 240)  # a later satellite records more, by a cell's own factor
    burned = np.where(season & (strength > -0.5), size * drift * np.exp(1.2 * strength), 0)
    stray = (~season) & (rng.random((cells, months)) < 0.03)
    burned = np.where(stray, size * 0.2 * np.exp(rng.standard_normal((cells, months))), burned)

    cloud = smooth(rng, months, 4).reshape(months, -1).T
    seen = 0.75 + 0.15 * cloud
    seen[:, 5:] -= 0.2 * instrument * moisture[:, :-5]
    seen = np.clip(np.where(rng.random((cells, months)) < 0.08, 0.1 * rng.random((cells, months)), seen), 0.0, 1.0)
    if before:  # a clear view the month before is needed to record a burn
        recorded = burned * seen * (np.concatenate([seen[:, :1], seen[:, :-1]], axis=1) / 0.75) ** before
    else:
        recorded = burned * seen ** (1 + 2 * (instrument > 0))  # with an instrument effect, what is recorded falls faster than the share observed

    out = [a.reshape(cells, YEARS, 12).copy() for a in (recorded, seen)]
    for a in out:
        a[:, ABSENT] = np.nan
    lat, lon = -15 + 0.25 + 0.5 * row, 10 + 0.25 + 0.5 * col
    return out[0], out[1], moisture, lat.astype(float), lon.astype(float), planted
