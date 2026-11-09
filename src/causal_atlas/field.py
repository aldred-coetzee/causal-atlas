"""Real monthly fields and series on one clock: month 0 is January of FIRST_YEAR. Drought (SPEI-3) on the African cells and the ONI. See results/real-enso-drought.md."""
import netCDF4
import numpy as np
import pyarrow.parquet as pq

from causal_atlas.panel import PANEL, RAW

FIRST_YEAR = 1950
LAST_YEAR = 2024
MONTHS = 12 * (LAST_YEAR - FIRST_YEAR + 1)


def cells():
    t = pq.read_table(PANEL / "cells.parquet").to_pydict()
    return np.array(t["lat"]), np.array(t["lon"])


def spei():
    """Cells by months, FIRST_YEAR-01 to LAST_YEAR-12, and the rows of cells.parquet kept: a cell with any missing month is dropped."""
    cache = PANEL / "real" / "spei.npz"
    if cache.exists():
        z = np.load(cache)
        return z["y"], z["kept"]
    lat, lon = cells()
    nc = netCDF4.Dataset(RAW / "spei03.nc")
    time = nc["time"]
    dates = netCDF4.num2date(time[:], time.units, getattr(time, "calendar", "standard"))
    first = next(i for i, d in enumerate(dates) if d.year == FIRST_YEAR and d.month == 1)
    assert dates[first + MONTHS - 1].year == LAST_YEAR and dates[first + MONTHS - 1].month == 12
    ilat = np.rint((lat - float(nc["lat"][0])) / 0.5).astype(int)
    ilon = np.rint((lon - float(nc["lon"][0])) / 0.5).astype(int)
    assert np.allclose(nc["lat"][ilat], lat) and np.allclose(nc["lon"][ilon], lon)
    box = np.ma.filled(nc["spei"][first : first + MONTHS, ilat.min() : ilat.max() + 1, ilon.min() : ilon.max() + 1], np.nan)
    y = box[:, ilat - ilat.min(), ilon - ilon.min()].T.astype(np.float32)
    kept = np.flatnonzero(np.isfinite(y).all(axis=1))
    y = y[kept]
    np.savez(cache, y=y, kept=kept)
    return y, kept


# Other fields from the same file, as plain boxes: south, north, west, east, in degrees. Fixed in results/real-enso-continents.md before any number on them.
BOXES = {
    "south_america": (-56, 13, -82, -34),
    "australia": (-44, -10.25, 112, 154),
    "south_southeast_asia": (-10, 35, 65, 155),
    "north_america": (15, 60, -130, -60),
    "europe": (35, 70, -10, 40),
}


def box(name):
    """Cells by months for one box of BOXES, with each cell's latitude and longitude. A cell with any missing month is dropped."""
    cache = PANEL / "real" / f"spei_{name}.npz"
    if not cache.exists():
        south, north, west, east = BOXES[name]
        nc = netCDF4.Dataset(RAW / "spei03.nc")
        time = nc["time"]
        dates = netCDF4.num2date(time[:], time.units, getattr(time, "calendar", "standard"))
        first = next(i for i, d in enumerate(dates) if d.year == FIRST_YEAR and d.month == 1)
        assert dates[first + MONTHS - 1].year == LAST_YEAR and dates[first + MONTHS - 1].month == 12
        lat, lon = np.asarray(nc["lat"][:]), np.asarray(nc["lon"][:])
        a, o = np.flatnonzero((lat >= south) & (lat <= north)), np.flatnonzero((lon >= west) & (lon <= east))
        cube = np.ma.filled(nc["spei"][first : first + MONTHS, a[0] : a[-1] + 1, o[0] : o[-1] + 1], np.nan)
        y = cube.reshape(MONTHS, -1).T.astype(np.float32)
        kept = np.isfinite(y).all(axis=1)
        np.savez(cache, y=y[kept], lat=np.repeat(lat[a], len(o))[kept], lon=np.tile(lon[o], len(a))[kept], of=kept.size)
    z = np.load(cache)
    return z["y"], z["lat"], z["lon"]


def series(name):
    """A monthly index in NOAA PSL's layout (a year, then twelve values) on the same clock. Every month must be present."""
    rows = {}
    for line in open(RAW / name):
        p = line.split()
        if len(p) == 13 and p[0].isdigit():
            rows[int(p[0])] = [float(v) for v in p[1:]]
    x = np.array([rows[y] for y in range(FIRST_YEAR, LAST_YEAR + 1)]).ravel()
    assert x.size == MONTHS and (x > -90).all()
    return x


def oni():
    """The ONI by month on the same clock. The value at month t is a 3-month mean centred on t, so it uses month t + 1."""
    return series("oni.data")
