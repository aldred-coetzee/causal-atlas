"""A reviewer's modified copy of synth/harvest_panel.py, kept apart from it. Added: drift shapes a straight line cannot take out (shape "u", "hockey"), a strength multiplier, heavy-tailed yield shocks, and a shared year-to-year swing in both moisture and yield with no seasonal link.

Made-up national harvests: yield by country, cereal and year, with a monthly moisture series for each country, for a known-answer check of causal_atlas.harvest. Nothing here is imported from, or shares a line with, the detector."""
import numpy as np

CEREALS = 6
WANDER = (0.15, 0.7)  # how far a record's level wanders each year, as a share of its year-to-year spread: lowest and highest
EARTH = 6371.0


def apart(lat, lon):
    """Great-circle distance in km between every pair of points."""
    a, o = np.radians(lat), np.radians(lon)
    c = np.sin(a)[:, None] * np.sin(a) + np.cos(a)[:, None] * np.cos(a) * np.cos(o[:, None] - o)
    return EARTH * np.arccos(np.clip(c, -1, 1))


def near(rng, dist, reach, shape):
    """Noise that neighbours share: correlation falls off with distance over the reach given, in km."""
    vals, vecs = np.linalg.eigh(np.exp(-dist / reach))
    root = (vecs * np.sqrt(np.maximum(vals, 0))) @ vecs.T
    return np.einsum("ij,j...->i...", root, rng.standard_normal((len(dist),) + shape))


def make(seed, kind="link", share=0.2, countries=141, years=64, linked=0.5, shape="square", mult=1.0, tails=None, common=0.0, blur=0.0):
    """One world. kind: "link" (moisture in a growing season moves the yield, in about the fraction `linked` of countries, taking `share` of the variance of a linked series' year-to-year departures), "none" (no link), "drift" (no link; a slow drying or wetting that speeds up, and a yield path bending the same way in the same places), "step" (no link from year to year; in patches of countries the climate turns drier for good in one year, and yields there fall to a lower path in the same year). In every kind most countries dry a little over the record, as the real drought file's country means do.

    Returns log yield (units by years, NaN where no figure), which figures are official, each unit's country and cereal, the monthly moisture by country starting twelve months before the first year, each country's latitude and longitude, and the truth: which units are linked and each unit's season as (first month, length), months counted from January of the harvest year, negative for the year before."""
    rng = np.random.default_rng(seed)
    months = 12 * (years + 1)

    # Where: clusters of countries, so that neighbours exist.
    hubs = np.column_stack([rng.uniform(-35, 55, 9), rng.uniform(-180, 180, 9)])
    hub = rng.integers(9, size=countries)
    lat = np.clip(hubs[hub, 0] + rng.normal(0, 9, countries), -50, 65)
    lon = (hubs[hub, 1] + rng.normal(0, 14, countries) + 180) % 360 - 180
    dist = apart(lat, lon)

    # Moisture by month: weather neighbours share, a slow swing the whole world feels with a sign that depends on place, and a memory of a few months.
    raw = near(rng, dist, 1200.0, (months,))
    swing = np.zeros(months)
    for m in range(1, months):
        swing[m] = 0.93 * swing[m - 1] + rng.standard_normal()
    swing /= swing.std()
    raw += near(rng, dist, 4000.0, ())[:, None] * 0.5 * swing
    wet = raw.copy()
    wet[:, 1:] += 0.5 * raw[:, :-1]
    wet[:, 2:] += 0.25 * raw[:, :-2]
    bend = near(rng, dist, 3000.0, ())  # where the drift goes, if there is one
    clock = np.linspace(0, 1, months)
    wet += rng.normal(-0.5, 0.45, countries)[:, None] * clock * wet.std()
    def bendy(c):
        if shape == "square":
            return c**2
        if shape == "u":
            return 4 * ((c - 0.5) ** 2 - 1 / 12)
        if shape == "hockey":
            return np.maximum(c - 0.6, 0) * 2.5
    if kind == "drift":
        wet += mult * 1.2 * bend[:, None] * bendy(clock) * wet.std()
    yearly = np.zeros((countries, years))
    if common:
        g = near(rng, dist, 2500.0, (years,))
        for yy in range(1, years):
            g[:, yy] = 0.6 * g[:, yy - 1] + 0.8 * g[:, yy]
        yearly = g / g.std()
        wet += common * np.repeat(np.column_stack([yearly[:, :1], yearly]), 12, axis=1) * wet.std()
    stepped = bend > np.quantile(bend, 0.65)  # where the step falls, if there is one
    peak = np.argmax(np.where(stepped[None, :] & (dist < 2000.0), bend[None, :], -np.inf), axis=1)  # the strongest stepped country within reach: a patch takes its year from it
    when = np.where(stepped, (15 + (np.abs(bend) * 1000).astype(int) % 30)[peak], 0)
    if kind == "step":
        wet -= 1.2 * wet.std() * stepped[:, None] * (np.arange(months)[None, :] >= 12 * (when[:, None] + 1))
    wet = (wet - wet.mean(axis=1, keepdims=True)) / wet.std(axis=1, keepdims=True)
    width = rng.uniform(0.6, 1.05, countries)  # a wide country's mean moves less
    moisture = wet * width[:, None]

    # Which cereals a country grows.
    grows = rng.random((countries, CEREALS)) < np.array([0.70, 0.83, 0.67, 0.56, 0.49, 0.32])
    grows[~grows.any(axis=1), 1] = True
    country, cereal = np.nonzero(grows)
    units = len(country)

    # Each unit's season: where the months are counted from January of the harvest year.
    late = np.array([5, 7, 8, 5, 8, 8])[cereal] + rng.integers(-1, 2, units)  # the season's last month, in the north
    south = lat[country] < -15
    tropic = np.abs(lat[country]) <= 15
    late = np.where(south, late - 6, late)
    late = np.where(tropic, rng.integers(-2, 11, countries)[country] + rng.integers(-1, 2, units), late)
    length = rng.integers(2, 5, units)
    start = late - length + 1

    # Who is linked: rain-fed places, in patches.
    patch = near(rng, dist, 2500.0, ()) + 0.5 * rng.standard_normal(countries)
    is_linked = (patch > np.quantile(patch, 1 - linked))[country] if kind == "link" else np.zeros(units, dtype=bool)

    # The yield's own path: a level, growth that changes once or twice, a memory, shocks neighbours share, a level that wanders and does not come back, and noise in the figure.
    t = np.arange(years)
    growth = rng.uniform(0.0, 0.025, units)
    path = np.zeros((units, years))
    for u in range(units):
        rate = np.full(years, growth[u])
        for b in rng.integers(8, years - 5, rng.integers(0, 3)):
            rate[b:] = rng.uniform(-0.01, 0.03)
        path[u] = np.cumsum(rate)
    if kind == "drift":
        path -= mult * 0.25 * bend[country][:, None] * bendy(t / years)[None, :]
    if kind == "step":
        path -= rng.uniform(0.15, 0.3, units)[:, None] * stepped[country][:, None] * (t[None, :] >= when[country][:, None])
    spread = rng.lognormal(np.log(0.14), 0.55, units)  # how much a unit's yield moves from year to year
    own = np.zeros((units, years))
    phi = rng.uniform(0.1, 0.6, units)
    for y in range(years):
        own[:, y] = (phi * own[:, y - 1] if y else 0) + np.sqrt(1 - phi**2) * rng.standard_normal(units)
    shared = near(rng, dist, 1500.0, (years,))[country] * 0.6 + rng.standard_normal((countries, years))[country] * 0.5
    rough = np.ones((units, years))  # a stretch in which a record behaves differently
    for u in np.flatnonzero(rng.random(units) < 0.3):
        a = rng.integers(5, years - 8)
        rough[u, a : a + rng.integers(4, 15)] = rng.uniform(1.8, 3.0)
    if tails:
        own = own * np.sqrt(tails / rng.chisquare(tails, (units, years)))
    depart = (0.8 * own + 0.55 * shared) * rough
    if common:
        depart = depart / depart.std(axis=1, keepdims=True) + common * yearly[country]
    depart /= depart.std(axis=1, keepdims=True)
    wander = np.cumsum(rng.standard_normal((units, years)), axis=1) * rng.uniform(*WANDER, units)[:, None]  # a level that does not come back

    # The season's moisture: a dry season costs more than a wet one gives.
    season = np.zeros((units, years))
    for u in range(units):
        cols = 12 * (t[:, None] + 1) + start[u] + np.arange(length[u])[None, :]
        v = moisture[country[u]][cols].mean(axis=1)
        season[u] = np.where(v < 0, v, 0.35 * v)
    season = (season - season.mean(axis=1, keepdims=True)) / season.std(axis=1, keepdims=True)
    effect = np.sqrt(share / (1 - share)) * season * is_linked[:, None] if share else np.zeros((units, years))
    logy = rng.normal(7.5, 0.6, units)[:, None] + path + spread[:, None] * (wander + depart + effect)

    # The record as kept: late starters, gaps, and stretches of figures that are not official, some of them last year's carried forward.
    official = np.ones((units, years), dtype=bool)
    begins = np.where(rng.random(countries) < 0.12, 31, 0)[country]
    for u in range(units):
        for _ in range(rng.integers(0, 4) if rng.random() < 0.55 else 0):
            a = rng.integers(1, years - 2)
            b = min(years, a + rng.integers(1, 9))
            official[u, a:b] = False
            if rng.random() < 0.15:
                logy[u, a:b] = logy[u, a - 1]
            else:
                logy[u, a:b] += spread[u] * 0.5 * rng.standard_normal(b - a)
        official[u, -3:] &= rng.random(3) < 0.7
        logy[u, : begins[u]] = np.nan
        gone = rng.random(years) < 0.01
        logy[u, gone] = np.nan
    official &= np.isfinite(logy)
    seen = moisture
    if blur:  # the detector sees the country's mean, not the cropland's: the moisture that acts plus weather of its own, with the same memory
        extra = near(np.random.default_rng(seed + 10**6), dist, 1200.0, (months,))
        extra[:, 1:] += 0.5 * extra[:, :-1].copy()
        extra[:, 2:] += 0.25 * extra[:, :-2].copy()
        extra /= extra.std(axis=1, keepdims=True)
        seen = (moisture / moisture.std(axis=1, keepdims=True) + blur * extra) / np.sqrt(1 + blur**2)
    return {"logy": logy, "official": official, "country": country, "cereal": cereal, "x": seen, "lat": lat, "lon": lon, "linked": is_linked, "season": np.column_stack([start, length])}
