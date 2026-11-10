"""Staple cereal prices by market (World Bank Real Time Food Prices, release 2026-11-02) on their own clock: month 0 is January of FIRST_YEAR. Only prices as collected, never the file's model estimates (decision 0049)."""
import duckdb
import numpy as np

from causal_atlas.panel import PANEL, RAW

FIRST_YEAR = 2007
LAST_YEAR = 2024  # the last year the drought file holds
MONTHS = 12 * (LAST_YEAR - FIRST_YEAR + 1)
ITEMS = ("maize", "millet", "sorghum", "rice", "wheat", "wheat_flour")  # the plain columns: prices as collected
LEAST = 120  # observed months, for a market's series of one item to be kept
FILE = RAW / "rtfp" / "WLD_RTFP_mkt_2026-11-02.csv"


def table():
    """Every observed price of ITEMS at a market with coordinates, FIRST_YEAR-01 to LAST_YEAR-12: market, country, latitude, longitude, month on this clock, item, price."""
    cols = ", ".join(f'try_cast("{c}" as double) as "{c}"' for c in ITEMS)
    con = duckdb.connect()
    con.execute(f"""create table t as select geo_id, ISO3, try_cast(lat as double) as lat, try_cast(lon as double) as lon,
        12 * (year(price_date::date) - {FIRST_YEAR}) + month(price_date::date) - 1 as m, {cols}
        from read_csv('{FILE}', header=true, all_varchar=true)""")
    return con.execute(f"""select geo_id, ISO3, lat, lon, m, item, price from (unpivot t on {", ".join(ITEMS)} into name item value price)
        where price > 0 and lat is not null and lon is not null and m between 0 and {MONTHS - 1} order by ISO3, geo_id, item, m""").fetchnumpy()


def panel():
    """Units by months of log price, NaN where no price was collected, for each market and item with at least LEAST observed months; and each unit's latitude, longitude, country and item."""
    cache = PANEL / "real" / "prices.npz"
    if not cache.exists():
        t = table()
        key = np.char.add(np.char.add(t["geo_id"].astype(str), "|"), t["item"].astype(str))
        names, unit, n = np.unique(key, return_inverse=True, return_counts=True)
        logp = np.full((len(names), MONTHS), np.nan)
        logp[unit, t["m"]] = np.log(t["price"])
        first = np.unique(unit, return_index=True)[1]
        kept = n >= LEAST
        np.savez(cache, logp=logp[kept], lat=t["lat"][first][kept], lon=t["lon"][first][kept], country=t["ISO3"][first][kept].astype(str), item=t["item"][first][kept].astype(str))
    z = np.load(cache)
    return z["logp"], z["lat"], z["lon"], z["country"], z["item"]
