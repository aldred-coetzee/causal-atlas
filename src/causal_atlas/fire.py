"""Burned area (ESA Fire_cci FireCCILT11) on the 0.5 degree grid, on its own clock: month 0 is January of FIRST_YEAR. The makers left 1994 out. Rule: results/fire-enso.md."""
import netCDF4
import numpy as np

from causal_atlas import field
from causal_atlas.panel import PANEL, RAW

FIRST_YEAR = 1982
LAST_YEAR = 2018
ABSENT = 1994
MONTHS = 12 * (LAST_YEAR - FIRST_YEAR + 1)
FIT = 12 * (2003 - FIRST_YEAR + 1)  # months: 1982-01 to 2003-12
SEEN = 0.2  # a cell-month counts as seen when at least this share of its burnable land was observed
LEAST_SEEN = 15  # fitting years seen, for a cell's calendar month to be used
LEAST_BURNED = 5  # of those, years with any burned area
CLIP = 3.0
FIELDS = ("africa", *field.BOXES)


def grid():
    """Burned area in km2 and the share of burnable land observed, each months by 360 by 720 with north first, and each cell's burnable share. 1994 is NaN in the first two."""
    cache = PANEL / "real" / "fire_grid.npz"
    if not cache.exists():
        burned = np.full((MONTHS, 360, 720), np.nan, np.float32)
        observed = np.full((MONTHS, 360, 720), np.nan, np.float32)
        burnable = np.zeros((360, 720))
        files = 0
        for t in range(MONTHS):
            year, month = FIRST_YEAR + t // 12, t % 12 + 1
            if year == ABSENT:
                continue
            nc = netCDF4.Dataset(RAW / "firecci" / f"{year}{month:02d}01-ESACCI-L4_FIRE-BA-AVHRR-LTDR-fv1.1.nc")
            assert nc["lat"][0] > nc["lat"][-1] and nc["lat"].shape == (720,) and nc["lon"].shape == (1440,)
            four = lambda name: np.ma.filled(nc[name][0], 0).astype(np.float64).reshape(360, 2, 720, 2)
            land, seen = four("fraction_of_burnable_area") / 100, four("fraction_of_observed_area") / 100  # both are stored as per cent, whatever their units attribute says
            burned[t] = four("burned_area").sum(axis=(1, 3)) / 1e6
            total = land.sum(axis=(1, 3))
            observed[t] = np.divide((land * seen).sum(axis=(1, 3)), total, out=np.zeros_like(total), where=total > 0)
            burnable += total / 4
            files += 1
        np.savez_compressed(cache, burned=burned, observed=observed, burnable=(burnable / files).astype(np.float32))
    z = np.load(cache)
    return z["burned"], z["observed"], z["burnable"]


def where(name):
    """Rows and columns of grid() for one field: Africa's cells are the panel's, the others are the plain boxes of field.BOXES."""
    lat, lon = 89.75 - 0.5 * np.arange(360), -179.75 + 0.5 * np.arange(720)
    if name == "africa":
        a, o = field.cells()
        i, j = np.rint((89.75 - a) / 0.5).astype(int), np.rint((o + 179.75) / 0.5).astype(int)
        assert np.allclose(lat[i], a) and np.allclose(lon[j], o)
    else:
        south, north, west, east = field.BOXES[name]
        i, j = [g.ravel() for g in np.meshgrid(np.flatnonzero((lat >= south) & (lat <= north)), np.flatnonzero((lon >= west) & (lon <= east)), indexing="ij")]
    return i, j, lat[i], lon[j]


def standard(b, o):
    """b: km2 burned, o: share of burnable land observed, each cells by years by 12, NaN where the makers give no data. Returns the standardised value in the same shape and which calendar months of each cell are used (cells by 12).

    The value is log(1 + km2 burned / share observed), less the cell's mean for that calendar month and over its spread, both from the seen months of the fitting years only. A cell-month is seen when at least SEEN of its burnable land was observed. A calendar month of a cell is used when it was seen in at least LEAST_SEEN fitting years and burned in at least LEAST_BURNED of them. Every other cell-month, every month not seen, and every month with no data are zero: the calendar-month average."""
    seen = np.isfinite(b) & (np.nan_to_num(o) >= SEEN)
    b = np.where(seen, b, 0)
    v = np.log1p(np.divide(b, o, out=np.zeros_like(b), where=seen))
    years = FIT // 12
    early = seen[:, :years]
    n = early.sum(axis=1)
    mean = np.divide((v[:, :years] * early).sum(axis=1), n, out=np.zeros(n.shape), where=n > 0)
    spread = np.sqrt(np.divide((((v[:, :years] - mean[:, None]) ** 2) * early).sum(axis=1), n, out=np.zeros(n.shape), where=n > 0))
    used = (n >= LEAST_SEEN) & (((b[:, :years] > 0) & early).sum(axis=1) >= LEAST_BURNED) & (spread > 0)
    y = np.where(seen & used[:, None], np.divide(v - mean[:, None], spread[:, None], out=np.zeros_like(v), where=spread[:, None] > 0), 0)
    return y, used


def box(name):
    """One field: cells by months of standardised burned area (see standard()), clipped, with latitude, longitude, and which of each cell's calendar months are used (cells by 12). A cell with no used month is dropped."""
    cache = PANEL / "real" / f"fire_{name}.npz"
    if not cache.exists():
        burned, observed, _ = grid()
        i, j, lat, lon = where(name)
        y, used = standard(*[a[:, i, j].T.astype(np.float64).reshape(len(i), -1, 12) for a in (burned, observed)])
        kept = used.any(axis=1)
        np.savez(cache, y=np.clip(y, -CLIP, CLIP).reshape(len(i), -1)[kept].astype(np.float32), lat=lat[kept], lon=lon[kept], used=used[kept], at=np.flatnonzero(kept))
    z = np.load(cache)
    return z["y"], z["lat"], z["lon"], z["used"]


def share(o):
    """The share of burnable land observed (cells by years by 12, NaN where there is no data), less the cell's mean for that calendar month and over its spread on the fitting years, clipped; months with no data zero. Cells by months."""
    known = np.isfinite(o)
    o = np.nan_to_num(o)
    early = known[:, : FIT // 12]
    n = early.sum(axis=1)
    mean = (o[:, : FIT // 12] * early).sum(axis=1) / n
    spread = np.sqrt((((o[:, : FIT // 12] - mean[:, None]) ** 2) * early).sum(axis=1) / n)
    y = np.where(known, np.divide(o - mean[:, None], spread[:, None], out=np.zeros_like(o), where=spread[:, None] > 0), 0)
    return np.clip(y, -CLIP, CLIP).reshape(len(o), -1).astype(np.float32)


def sight(name):
    """What the satellite saw, for the cells of box(name): share() of the observed share. A check on the instrument, not an outcome."""
    box(name)
    at = np.load(PANEL / "real" / f"fire_{name}.npz")["at"]
    i, j, _, _ = where(name)
    return share(grid()[1][:, i[at], j[at]].T.astype(np.float64).reshape(len(at), -1, 12))


def oni():
    """The ONI on this clock."""
    return field.oni()[12 * (FIRST_YEAR - field.FIRST_YEAR) : 12 * (LAST_YEAR + 1 - field.FIRST_YEAR)]
