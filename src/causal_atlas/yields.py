"""Crop yield by country and year (FAOSTAT; the six cereals of decision 0051, and every other crop with enough long records, decision 0054) on its own clock: year 0 is FIRST_YEAR. With it, each country's drought by month, the mean of the drought file over the country's cells, starting a year earlier."""
import duckdb
import netCDF4
import numpy as np
import shapefile
from shapely import contains_xy
from shapely.geometry import shape

from causal_atlas.panel import PANEL, RAW

FIRST_YEAR = 1961
LAST_YEAR = 2024
YEARS = LAST_YEAR - FIRST_YEAR + 1
CEREALS = ("Wheat", "Maize (corn)", "Rice", "Barley", "Sorghum", "Millet")
YIELD = 5412  # FAOSTAT's element code for yield, kg/ha
LEAST = 30  # official years, for a country's series of one cereal to be kept
SUMS = 1700  # FAOSTAT's item codes from here up are sums of crops
OTHER_SERIES = 30  # country series of LEAST official years, for a crop outside CEREALS to be read
TOTALS = ("159",)  # M49 codes that are sums of other rows kept: China, which holds the mainland and Taiwan
BY_NAME = {"NOR": "578", "TWN": "158"}  # Natural Earth gives these two no UN code
FILE = RAW / "faostat" / "Production_Crops_Livestock_E_All_Data_(Normalized).csv"


def others():
    """Every single crop outside CEREALS with at least OTHER_SERIES country series of LEAST official years of yield, most series first. Chosen by that count alone, from the yields alone."""
    items = ", ".join(f"'{c}'" for c in CEREALS)
    totals = ", ".join(f"'{c}'" for c in TOTALS)
    return tuple(r[0] for r in duckdb.connect().execute(f"""with u as (select "Area Code (M49)" as m49, Item as item, sum((Flag = 'A')::int) as n
        from read_csv('{FILE}', header=true, all_varchar=true, encoding='latin-1')
        where "Element Code" = '{YIELD}' and cast("Area Code" as int) < 5000 and cast("Item Code" as int) < {SUMS} and Item not in ({items}) and try_cast("Value" as double) > 0
        and cast("Year" as int) between {FIRST_YEAR} and {LAST_YEAR} and replace("Area Code (M49)", '''', '') not in ({totals}) group by all)
        select item, count(*) as series from u where n >= {LEAST} group by item having count(*) >= {OTHER_SERIES} order by series desc, item""").fetchall())


def table(crops=CEREALS):
    """Every yield above zero of the crops named for a country: M49 code, crop, year on this clock, kg/ha, and whether the figure is official."""
    items = ", ".join("'" + c.replace("'", "''") + "'" for c in crops)
    return duckdb.connect().execute(f"""select replace("Area Code (M49)", '''', '') as m49, Item as item, cast("Year" as int) - {FIRST_YEAR} as yr,
        cast("Value" as double) as kg, Flag = 'A' as official
        from read_csv('{FILE}', header=true, all_varchar=true, encoding='latin-1')
        where "Element Code" = '{YIELD}' and cast("Area Code" as int) < 5000 and Item in ({items}) and try_cast("Value" as double) > 0
        and cast("Year" as int) between {FIRST_YEAR} and {LAST_YEAR} order by m49, item, yr""").fetchnumpy()


def borders():
    """Natural Earth's country shapes by M49 code."""
    reader = shapefile.Reader(str(RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    fields = [f[0] for f in reader.fields[1:]]
    out = {}
    for r in reader.iterShapeRecords():
        rec = dict(zip(fields, r.record))
        code = BY_NAME.get(rec["ADM0_A3"], str(rec["UN_A3"]).zfill(3))
        if code not in ("-99", "-099"):
            out[code] = shape(r.shape.__geo_interface__)
    return out


def drought(codes):
    """For each country code, its drought by month from January of the year before FIRST_YEAR to December of LAST_YEAR (the mean of SPEI-3 over the half-degree cells whose centres lie inside it and that have a value every month), its number of such cells, and its middle as latitude and longitude. A country with no such cell has NaN."""
    nc = netCDF4.Dataset(RAW / "spei03.nc")
    time = nc["time"]
    dates = netCDF4.num2date(time[:], time.units, getattr(time, "calendar", "standard"))
    first = next(i for i, d in enumerate(dates) if d.year == FIRST_YEAR - 1 and d.month == 1)
    months = 12 * (YEARS + 1)
    assert dates[first + months - 1].year == LAST_YEAR and dates[first + months - 1].month == 12
    lat, lon = np.asarray(nc["lat"][:], dtype=float), np.asarray(nc["lon"][:], dtype=float)
    glon, glat = np.meshgrid(lon, lat)
    shapes = borders()
    x, cells, mid = np.full((len(codes), months), np.nan), np.zeros(len(codes), dtype=int), np.full((len(codes), 2), np.nan)
    for i, code in enumerate(codes):
        if code not in shapes:
            continue
        south, north = shapes[code].bounds[1], shapes[code].bounds[3]
        rows = np.flatnonzero((lat >= south - 0.5) & (lat <= north + 0.5))
        if not len(rows):
            continue
        a = slice(rows[0], rows[-1] + 1)
        inside = contains_xy(shapes[code], glon[a], glat[a])
        if not inside.any():
            continue
        cube = np.ma.filled(nc["spei"][first : first + months, a, :], np.nan)[:, inside]
        whole = np.isfinite(cube).all(axis=0)
        if not whole.any():
            continue
        x[i], cells[i] = cube[:, whole].mean(axis=1), whole.sum()
        la, lo = np.radians(glat[a][inside][whole]), np.radians(glon[a][inside][whole])
        v = np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)]).mean(axis=1)
        mid[i] = np.degrees(np.arcsin(v[2] / np.linalg.norm(v))), np.degrees(np.arctan2(v[1], v[0]))
    return x, cells, mid


def panel(crops=CEREALS, name="yields"):
    """Units by years of log yield (NaN where no figure), which of them are official, each unit's country code and crop, and by country: code, drought by month (see drought), latitude and longitude. A unit is a country's series of one crop with at least LEAST official years, in a country the drought file covers. Kept under `name`, so a set of crops is built once."""
    cache = PANEL / "real" / f"{name}.npz"
    if not cache.exists():
        t = table(crops)
        keep = ~np.isin(t["m49"].astype(str), TOTALS)
        t = {k: v[keep] for k, v in t.items()}
        key = np.char.add(np.char.add(t["m49"].astype(str), "|"), t["item"].astype(str))
        names, unit = np.unique(key, return_inverse=True)
        logy, official = np.full((len(names), YEARS), np.nan), np.zeros((len(names), YEARS), dtype=bool)
        logy[unit, t["yr"]] = np.log(t["kg"])
        official[unit, t["yr"]] = t["official"]
        code = np.array([n.split("|")[0] for n in names])
        item = np.array([n.split("|")[1] for n in names])
        codes = np.unique(code)
        x, cells, mid = drought(codes)
        kept = (official.sum(axis=1) >= LEAST) & (cells[np.searchsorted(codes, code)] > 0)
        used = np.isin(codes, code[kept])
        np.savez(cache, logy=logy[kept], official=official[kept], code=code[kept], item=item[kept], codes=codes[used], x=x[used], lat=mid[used, 0], lon=mid[used, 1], cells=cells[used])
    z = np.load(cache)
    return {k: z[k] for k in z.files}
