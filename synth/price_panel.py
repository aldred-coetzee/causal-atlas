"""A made-up record of staple prices collected at markets, with a made-up moisture index at each market, for a known-answer check of causal_atlas.rolling. Used in smoke runs only (decision 0050).

Written from what such records look like, not from how the detector works, and it imports nothing from src (rule 3; tests/test_synth_isolated.py). What every panel has, link or no link:

- markets clustered in countries, each selling one to three staples, some grown nearby and some imported;
- a national price level that rises month by month at the country's own pace, and in some countries changes pace part-way through the record, sometimes violently;
- a world price with a few sharp rises, reaching every market at once, imported staples most;
- a yearly cycle tied to the harvest, which comes at a time of year that moves with latitude;
- swings shared by a country's markets, and swings shared by markets near each other;
- prices not collected: series that start late or stop early, single months missed, longer breaks, and months when a whole country was not surveyed.

The kinds of panel:

- a link: in round patches, a dry growing season raises the price of staples grown nearby, building over some months after the season ends and lasting until the next one;
- none: prices owe nothing to moisture;
- coincide: prices owe nothing to moisture, but the driest season of the record, everywhere at once, falls in the year of the world price's sharpest rise;
- trend: prices owe nothing to moisture, but in the same places moisture falls steadily over the record while price rises gather pace.
"""
import numpy as np

YEARS = 18
MONTHS = 12 * YEARS
COUNTRIES = 16
ITEMS = 4  # staples: the first two grown nearby wherever they are sold, the third nearby in half the countries, the fourth imported
SOUTH, NORTH, WEST, EAST = -15.0, 20.0, -15.0, 45.0
PATCHES = 5


def ar(rng, shape, keep, spread):
    """Series along the last axis that keep that share of last month's value, with the long-run spread given."""
    e = rng.standard_normal(shape) * spread * np.sqrt(1 - keep**2)
    out = np.empty(shape)
    out[..., 0] = rng.standard_normal(shape[:-1]) * spread
    for t in range(1, shape[-1]):
        out[..., t] = keep * out[..., t - 1] + e[..., t]
    return out


def near(rng, lat, lon, reach, months):
    """Noise by month at each point, alike at points within about reach degrees of each other, unit variance."""
    d2 = (lat[:, None] - lat[None, :]) ** 2 + (lon[:, None] - lon[None, :]) ** 2
    vals, vecs = np.linalg.eigh(np.exp(-d2 / (2 * reach**2)) + 1e-6 * np.eye(len(lat)))
    return (vecs * np.sqrt(np.maximum(vals, 0))) @ (vecs.T @ rng.standard_normal((len(lat), months)))  # the symmetric root: the same whichever way the eigenvectors come out


def make(seed, rise=0.0, cover=0.3, build=4, coincide=False, trend=0.0):
    """Returns log price (series by months, NaN where no price was collected), moisture (series by months), each series' latitude, longitude, country and staple, whether the staple is grown near it, and whether it holds a planted link.

    rise: how far the log price of a staple grown nearby rises, at full effect, for each unit the growing season's moisture index fell short of normal. cover: the share of markets inside the patches where that happens. build: the months over which the effect builds after the growing season ends. coincide: the driest growing season, everywhere at once, is put in the year of the world price's sharpest rise. trend: the size of a drift, one wide map of places, down in moisture along a straight line and up in prices along its square."""
    rng = np.random.default_rng(seed)

    # Places: country capitals, towns around them, markets around the towns.
    centre = np.stack([rng.uniform(SOUTH, NORTH, COUNTRIES), rng.uniform(WEST, EAST, COUNTRIES)], axis=1)
    count = np.maximum(4, (rng.lognormal(3.0, 0.8, COUNTRIES)).astype(int))  # a few countries hold most of the markets
    country = np.repeat(np.arange(COUNTRIES), count)
    town = centre[country] + rng.normal(0, 1, (len(country), 2)) * rng.uniform(1.0, 4.5, COUNTRIES)[country][:, None]  # some countries are small, some span many degrees
    lat, lon = np.clip(town[:, 0], SOUTH, NORTH), np.clip(town[:, 1], WEST, EAST)
    markets = len(lat)

    # Moisture: a three-month index, alike at nearby markets, with a part shared by the whole region that carries over from year to year.
    wide = ar(rng, (YEARS + 1,), 0.3, 1.0).repeat(12)[: MONTHS + 2] + 0.5 * rng.standard_normal(MONTHS + 2)
    wide = wide / wide.std()
    raw = np.sqrt(0.75) * near(rng, lat, lon, 4.0, MONTHS + 2) + np.sqrt(0.25) * wide[None, :]
    moisture = raw[:, 2:] + raw[:, 1:-1] + raw[:, :-2]
    moisture = (moisture - moisture.mean(axis=1, keepdims=True)) / moisture.std(axis=1, keepdims=True)  # an index: each market's own record has mean nought and unit spread

    # The growing season ends at a time of year that moves with latitude, a little differently in each country.
    ends = (np.rint(8 - 6 * (NORTH - lat) / (NORTH - SOUTH)).astype(int) + rng.integers(-1, 2, COUNTRIES)[country]) % 12

    # The world price: a slow swing and three sharp rises that fade over a year or two.
    world = ar(rng, (MONTHS,), 0.97, 0.12)
    spikes = np.sort(rng.choice(np.arange(1, YEARS - 1), 3, replace=False))
    sizes = rng.uniform(0.2, 0.45, 3)
    for y, s in zip(spikes, sizes):
        t = np.arange(MONTHS) - (12 * y + rng.integers(12))
        world += s * np.where(t < 0, 0, np.minimum(t / 5, 1) * np.exp(-np.maximum(t - 5, 0) / 14))
    if coincide:
        y = spikes[sizes.argmax()]
        for m in range(markets):
            season = 12 * y + ends[m] - np.arange(3)
            moisture[m, season] = moisture[m, season] * 0.4 - 2.0

    if trend:
        place = trend * near(np.random.default_rng([seed, 1]), lat, lon, 8.0, 1)[:, 0]
        moisture = moisture - place[:, None] * np.linspace(-1, 1, MONTHS)[None, :]
    else:
        place = np.zeros(markets)

    # The national price level: the country's own pace, and in some a change of pace part-way.
    pace = rng.uniform(0.02, 0.10, COUNTRIES)[:, None] / 12 * np.ones((1, MONTHS))
    for c in np.flatnonzero(rng.random(COUNTRIES) < 0.4):
        start = rng.integers(36, MONTHS - 24)
        pace[c, start : start + rng.integers(18, 72)] = rng.uniform(0.15, 0.7) / 12
    level = np.cumsum(pace + 0.008 * rng.standard_normal((COUNTRIES, MONTHS)), axis=1)

    # Which staples each market sells, and whether each is grown nearby.
    third_local = rng.random(COUNTRIES) < 0.5
    sold = rng.random((markets, ITEMS)) < np.array([0.6, 0.5, 0.4, 0.6])[None, :]
    sold[np.arange(markets), rng.integers(ITEMS, size=markets)] |= ~sold.any(axis=1)
    m, item = np.nonzero(sold)
    local = (item < 2) | ((item == 2) & third_local[country[m]])
    series = len(m)

    reach = np.where(local, rng.uniform(0.2, 0.6, series), rng.uniform(0.6, 1.0, series))  # how much of the world price arrives
    shared = ar(rng, (COUNTRIES, ITEMS, MONTHS), 0.9, 0.10)[country[m], item]
    nearby = 0.08 * 0.6 * np.stack([near(rng, lat, lon, 1.5, MONTHS) for _ in range(ITEMS)])  # by staple: markets near each other move together
    for t in range(1, MONTHS):  # and their swings carry over from month to month
        nearby[:, :, t] += 0.8 * nearby[:, :, t - 1]
    since = (np.arange(MONTHS)[None, :] - ends[m][:, None]) % 12  # months since the growing season ended
    cycle = np.where(local, rng.uniform(0.05, 0.25, series), rng.uniform(0.0, 0.05, series))[:, None] * -np.cos(2 * np.pi * (since - 2) / 12)

    logp = rng.normal(5, 1, series)[:, None] + level[country[m]] + reach[:, None] * world[None, :] + shared + nearby[item, m] + cycle
    logp += (place[m][:, None] * 0.15 * np.linspace(0, 1, MONTHS)[None, :] ** 2) * YEARS / 2  # with a trend: the yearly rise itself rises over the record
    logp += 0.03 * rng.standard_normal((series, MONTHS))

    planted = np.zeros(series, bool)
    if rise:
        inside = np.zeros(markets, bool)
        radius = np.sqrt(cover * (NORTH - SOUTH) * (EAST - WEST) / PATCHES / np.pi)
        order = rng.permutation(markets)
        for c in order[:PATCHES]:
            inside |= (lat - lat[c]) ** 2 + (lon - lon[c]) ** 2 <= radius**2
        for c in order[PATCHES:]:  # more patches, until the share of markets asked for is inside
            if inside.mean() >= cover:
                break
            inside |= (lat - lat[c]) ** 2 + (lon - lon[c]) ** 2 <= (radius / 2) ** 2
        planted = inside[m] & local
        t = np.arange(12, MONTHS)
        j = since[:, t]  # the season that matters is the last one ended; a month in which one ends still feels the one before
        j = np.where(j == 0, 12, j)
        last = np.take_along_axis(moisture[m], t[None, :] - j, axis=1)
        logp[:, 12:] -= np.where(planted[:, None], rise * np.minimum(j / build, 1) * last, 0)

    # What was not collected.
    seen = np.ones((series, MONTHS), bool)
    t = np.arange(MONTHS)[None, :]
    seen &= t >= np.where(rng.random(series) < 0.45, 0, rng.integers(0, 84, series))[:, None]
    seen &= t < np.where(rng.random(series) < 0.12, rng.integers(120, MONTHS, series), MONTHS)[:, None]
    seen &= rng.random((series, MONTHS)) >= rng.uniform(0.02, 0.15, series)[:, None]
    for s in np.flatnonzero(rng.random(series) < 0.6):
        for _ in range(rng.integers(1, 4)):
            a = rng.integers(MONTHS)
            seen[s, a : a + rng.integers(2, 13)] = False
    for c in np.flatnonzero(rng.random(COUNTRIES) < 0.4):
        a = rng.integers(MONTHS)
        seen[country[m] == c, a : a + rng.integers(2, 9)] = False

    return np.where(seen, logp, np.nan), moisture[m], lat[m], lon[m], country[m], item, local, planted
