"""The real outcome panel: 0.5 degree African land cells by calendar month. No names kept."""
import glob
from pathlib import Path

import duckdb
import numpy as np
import shapefile
from shapely import contains_xy
from shapely.geometry import shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
PANEL = ROOT / "data" / "panel"

FIRST_MONTH = 1989 * 12  # 1989-01, the start of the outcome and of the warm-up
LAST_MONTH = 2025 * 12 + 2  # 2025-03, E from decision 0013
TRAIN_FIRST = 1992 * 12
VALID_FIRST = 2017 * 12 + 3
HELD_FIRST = 2021 * 12 + 3
MAX_WHERE_PREC = 3


def month_index(year, month):
    return year * 12 + month - 1


def land_cells():
    """Cell centres inside Natural Earth's African countries, with each cell's country."""
    reader = shapefile.Reader(str(RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    fields = [f[0] for f in reader.fields[1:]]
    countries = []
    for r in reader.iterShapeRecords():
        rec = dict(zip(fields, r.record))
        if rec["CONTINENT"] == "Africa":
            countries.append((rec["ADM0_A3"], shape(r.shape.__geo_interface__)))
    land = unary_union([g for _, g in countries])
    lats = np.arange(-40, 40, 0.5) + 0.25
    lons = np.arange(-20, 55, 0.5) + 0.25
    glon, glat = np.meshgrid(lons, lats)
    inside = contains_xy(land, glon, glat)
    lat, lon = glat[inside], glon[inside]
    country = np.full(lat.shape, "", dtype="U3")
    for code, geom in countries:
        country[contains_xy(geom, lon, lat)] = code
    return lat, lon, country


def build():
    """Write cells.parquet and counts.parquet. Returns counts that describe the build only."""
    PANEL.mkdir(parents=True, exist_ok=True)
    lat, lon, country = land_cells()
    db = duckdb.connect()
    db.execute("SET threads=4")
    db.execute("CREATE TABLE cells(cell INT, lat DOUBLE, lon DOUBLE, country VARCHAR)")
    db.executemany(
        "INSERT INTO cells VALUES (?,?,?,?)",
        [(i, float(a), float(o), str(c)) for i, (a, o, c) in enumerate(zip(lat, lon, country))],
    )
    db.execute(f"COPY cells TO '{PANEL / 'cells.parquet'}' (FORMAT parquet)")
    csv = glob.glob(str(RAW / "ged" / "*.csv"))[0]
    # Only the columns needed: actor names and source text never leave the raw file.
    db.execute(f"""
        CREATE TABLE ev AS
        SELECT latitude AS lat, longitude AS lon, where_prec,
               year(date_start)*12 + month(date_start) - 1 AS m
        FROM read_csv_auto('{csv}', sample_size=-1) WHERE region = 'Africa'
    """)
    db.execute(f"""
        CREATE TABLE placed AS
        SELECT e.m, c.cell, e.where_prec FROM ev e LEFT JOIN cells c
        ON c.lat = floor(e.lat*2)/2 + 0.25 AND c.lon = floor(e.lon*2)/2 + 0.25
    """)
    db.execute(f"""
        COPY (SELECT cell, m, count(*)::INT AS y FROM placed
              WHERE cell IS NOT NULL AND where_prec <= {MAX_WHERE_PREC}
                AND m BETWEEN {FIRST_MONTH} AND {LAST_MONTH}
              GROUP BY 1, 2 ORDER BY 1, 2)
        TO '{PANEL / 'counts.parquet'}' (FORMAT parquet)
    """)
    total, used, off_mask = db.execute(f"""
        SELECT count(*), count(*) FILTER (where_prec <= {MAX_WHERE_PREC}),
               count(*) FILTER (where_prec <= {MAX_WHERE_PREC} AND cell IS NULL) FROM placed
    """).fetchone()
    return {"cells": len(lat), "events": total, "precise": used, "precise_off_mask": off_mask,
            "no_country": int((country == "").sum())}


def load():
    """Dense outcome, cells by months from FIRST_MONTH, plus the cell coordinates."""
    db = duckdb.connect()
    db.execute("SET threads=4")
    cells = db.execute(f"SELECT lat, lon FROM '{PANEL / 'cells.parquet'}' ORDER BY cell").fetchnumpy()
    n_months = LAST_MONTH - FIRST_MONTH + 1
    y = np.zeros((len(cells["lat"]), n_months), dtype=np.int32)
    rows = db.execute(f"SELECT cell, m, y FROM '{PANEL / 'counts.parquet'}'").fetchnumpy()
    y[rows["cell"], rows["m"] - FIRST_MONTH] = rows["y"]
    return y, cells["lat"], cells["lon"]


if __name__ == "__main__":
    print(build())
