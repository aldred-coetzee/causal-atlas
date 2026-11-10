"""Item 1, data: 20 random yield figures from the panel against the raw FAOSTAT csv (own query), and three countries' drought series rebuilt from the netCDF with an independent cell test (matplotlib-free ray casting via shapely only for the shape's coordinates)."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common, numpy as np, duckdb, netCDF4, shapefile
p, country, cereal = common.real()
raw = os.path.join(common.ROOT, "data", "raw")
rng = np.random.default_rng(24001)
u, t = np.nonzero(np.isfinite(p["logy"]))
pick = rng.choice(len(u), 20, replace=False)
csv = os.path.join(raw, "faostat", "Production_Crops_Livestock_E_All_Data_(Normalized).csv")
db = duckdb.connect()
bad = 0
for i in pick:
    code, item, yr = p["code"][u[i]], p["item"][u[i]], 1961 + t[i]
    q = db.execute(f"""select "Value", "Flag", "Area", "Unit" from read_csv('{csv}', header=true, all_varchar=true, encoding='latin-1')
      where "Area Code (M49)" = '''{code}' and "Item" = '{item}' and "Year" = '{yr}' and "Element" = 'Yield'""").fetchall()
    v = float(q[0][0]); ok = abs(np.log(v) - p["logy"][u[i], t[i]]) < 1e-9 and (q[0][1] == 'A') == bool(p["official"][u[i], t[i]])
    bad += not ok
    print(q[0][2][:20], item[:6], yr, q[0][0], q[0][3], q[0][1], "panel", round(float(np.exp(p['logy'][u[i], t[i]])), 1), bool(p['official'][u[i], t[i]]), "OK" if ok else "MISMATCH")
print("yield mismatches", bad, "of 20")
# drought: own cell test for three countries via point-in-polygon on Natural Earth rings (even-odd), own mean
nc = netCDF4.Dataset(os.path.join(raw, "spei03.nc"))
tm = nc["time"]; dates = netCDF4.num2date(tm[:], tm.units)
i0 = [k for k, d in enumerate(dates) if d.year == 1960 and d.month == 1][0]
lat = np.asarray(nc["lat"][:]); lon = np.asarray(nc["lon"][:])
rd = shapefile.Reader(os.path.join(raw, "ne", "ne_10m_admin_0_countries.shp"))
names = [f[0] for f in rd.fields[1:]]
def inside(px, py, ring):
    ring = np.asarray(ring); x1, y1 = ring[:-1, 0], ring[:-1, 1]; x2, y2 = ring[1:, 0], ring[1:, 1]
    c = ((y1[None] > py[:, None]) != (y2[None] > py[:, None])) & (px[:, None] < (x2 - x1)[None] * (py[:, None] - y1[None]) / np.where(y2 - y1 == 0, 1e-12, y2 - y1)[None] + x1[None])
    return c.sum(axis=1) % 2 == 1
for a3, m49 in (("AUS", "036"), ("HUN", "348"), ("ZWE", "716")):
    sr = [s for s in rd.iterShapeRecords() if dict(zip(names, s.record))["ADM0_A3"] == a3][0]
    pts = sr.shape.points; parts = list(sr.shape.parts) + [len(pts)]
    bb = sr.shape.bbox
    la = lat[(lat >= bb[1]) & (lat <= bb[3])]; lo = lon[(lon >= bb[0]) & (lon <= bb[2])]
    gx, gy = np.meshgrid(lo, la); px, py = gx.ravel(), gy.ravel()
    flag = np.zeros(len(px), dtype=int)
    for a, b in zip(parts[:-1], parts[1:]):
        flag += inside(px, py, pts[a:b])
    inn = flag % 2 == 1
    li = np.searchsorted(lat, py[inn]); oi = np.searchsorted(lon, px[inn])
    cube = np.ma.filled(nc["spei"][i0:i0 + 780], np.nan)[:, li, oi]
    whole = np.isfinite(cube).all(axis=0)
    mine = cube[:, whole].mean(axis=1)
    k = list(p["codes"]).index(m49)
    d = p["x"][k]
    print(a3, "cells mine", whole.sum(), "panel", p["cells"][k], "corr", round(np.corrcoef(mine, d)[0, 1], 6), "max abs diff", round(float(np.nanmax(abs(mine - d))), 6))
