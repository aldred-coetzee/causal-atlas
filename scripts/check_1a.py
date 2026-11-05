"""Step 1a coverage queries. Reports data shape only: never outcomes by place or period."""
import glob

import duckdb
import netCDF4
import numpy as np
import shapefile
from shapely import contains_xy
from shapely.geometry import shape
from shapely.ops import unary_union

ged = glob.glob("data/raw/ged/*.csv")[0]
db = duckdb.connect()
db.execute(f"CREATE VIEW g AS SELECT * FROM read_csv_auto('{ged}', sample_size=-1)")
print("columns", [r[0] for r in db.execute("DESCRIBE g").fetchall()])
print("regions", db.execute("SELECT region, count(*) FROM g GROUP BY 1 ORDER BY 2 DESC").fetchall())
print("africa rows, years", db.execute("SELECT count(*), min(year), max(year), min(date_start), max(date_end) FROM g WHERE region='Africa'").fetchall())
total = db.execute("SELECT count(*) FROM g WHERE region='Africa'").fetchone()[0]
for col in ("where_prec", "date_prec", "type_of_violence"):
    rows = db.execute(f"SELECT {col}, count(*) FROM g WHERE region='Africa' GROUP BY 1 ORDER BY 1").fetchall()
    print(col, [(k, round(100 * n / total, 1)) for k, n in rows])
print("spans a month boundary %", db.execute(f"SELECT round(100.0*count(*)/{total},1) FROM g WHERE region='Africa' AND date_trunc('month',date_start::DATE)<>date_trunc('month',date_end::DATE)").fetchone())

reader = shapefile.Reader("data/raw/ne/ne_10m_admin_0_countries.shp")
fields = [f[0] for f in reader.fields[1:]]
africa = [shape(r.shape.__geo_interface__) for r in reader.iterShapeRecords() if dict(zip(fields, r.record))["CONTINENT"] == "Africa"]
print("NE african countries", len(africa))
land = unary_union(africa)
lats = np.arange(-40, 40, 0.5) + 0.25
lons = np.arange(-20, 55, 0.5) + 0.25
glon, glat = np.meshgrid(lons, lats)
mask = contains_xy(land, glon, glat)
print("cells, centre in NE Africa", int(mask.sum()))

nc = netCDF4.Dataset("data/raw/spei03.nc")
time = nc["time"]
dates = netCDF4.num2date(time[:], time.units, getattr(time, "calendar", "standard"))
print("SPEI", dates[0], dates[-1], len(dates), "res", float(np.diff(nc["lat"][:2])[0]), {k: str(getattr(nc, k))[:100] for k in nc.ncattrs()})
ilat = np.searchsorted(nc["lat"][:], lats)
ilon = np.searchsorted(nc["lon"][:], lons)
grid_ok = np.allclose(nc["lat"][ilat], lats) and np.allclose(nc["lon"][ilon], lons)
print("SPEI on our cell centres", grid_ok)
for label, idx in (("1992-01", (1992 - 1901) * 12), ("last", len(dates) - 1)):
    frame = np.ma.filled(nc["spei"][idx, ilat, ilon], np.nan)
    print("SPEI missing share of our cells", label, round(float(np.isnan(frame[mask]).mean()), 4))
