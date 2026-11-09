"""The El Niño term by region for months after the drought file ends, from the model as tested and from a refit. Rule: results/outlook-2026-27.md."""
import json
from pathlib import Path

import numpy as np
import shapefile
from shapely import contains_xy
from shapely.geometry import shape

from causal_atlas import field, forecast, links
from causal_atlas.panel import RAW
from run_continents import SCORED, data, rows, units
from run_enso import DISCOVERY

OUT = Path(__file__).resolve().parents[1] / "results" / "outlook-2026-27.jsonl"
FIELDS = ("south_america", "australia", "south_southeast_asia", "north_america")
FIRST, LAST = 12 * (2025 - field.FIRST_YEAR), 12 * (2027 - field.FIRST_YEAR) + 8  # 2025-01 to 2027-09
BANDS = (0.0, 0.1, 0.25, 0.5, np.inf)


def index():
    """The ONI from field.FIRST_YEAR to the last year in the file; months not yet published are NaN."""
    table = {}
    for line in open(RAW / "oni.data"):
        p = line.split()
        if len(p) == 13 and p[0].isdigit():
            table[int(p[0])] = [float(v) for v in p[1:]]
    x = np.array([table[y] for y in range(field.FIRST_YEAR, max(table) + 1)]).ravel()
    return np.where(x > -90, x, np.nan)


def countries(lat, lon):
    """The Natural Earth country each point falls in, empty where none."""
    reader = shapefile.Reader(str(RAW / "ne" / "ne_10m_admin_0_countries.shp"))
    names = [f[0] for f in reader.fields[1:]]
    out = np.full(len(lat), "", dtype=object)
    for r in reader.iterShapeRecords():
        out[contains_xy(shape(r.shape.__geo_interface__), lon, lat)] = dict(zip(names, r.record))["ADMIN"]
    return out


def terms(model, x, years):
    """The multiplier times the term on the years given: units by years by 12, NaN where there is no claim or no index value."""
    pad = np.concatenate([x, np.full(max(0, 12 * (years.max() + 1) - len(x)), np.nan)])
    return np.where(model["claimed"].T[:, None, :], model["k"] * forecast.term(pad, years, model["lag"], model["slope"]), np.nan)


def coefficients(y, near):
    """The linear baseline's coefficients as fitted on the discovery years: own values at t - 3, 4, 5, 6 and 12, the neighbours at t - 3, own means of 12 and 60 months, a constant."""
    fit = forecast.all_months(np.arange(1, DISCOVERY // 12))
    return np.linalg.lstsq(forecast.design(y, near, fit), y[:, fit].T.ravel().astype(np.float64), rcond=None)[0]


def label(month):
    return f"{field.FIRST_YEAR + month // 12}-{month % 12 + 1:02d}"


def main():
    x = index()
    scored = {r["field"]: r for r in rows() if r["kind"] == "confirmation" and r["scale"] == "region"}
    last = int(np.flatnonzero(np.isfinite(x)).max())
    out = [{"kind": "driver", "last": label(last), "since_2024": {label(m): float(x[m]) for m in range(12 * 74, last + 1)}, "largest_1950_1999": float(x[:DISCOVERY].max()), "smallest_1950_1999": float(x[:DISCOVERY].min()), "largest_2000_2024": float(x[DISCOVERY : field.MONTHS].max())}]
    years = np.arange(FIRST // 12, LAST // 12 + 1)
    past = []
    for which in FIELDS:
        y, near, held = units(which, "region")
        _, _, lat, lon = data(which)
        tile = links.tiles(lat, lon)
        at = np.stack([tile @ lat, tile @ lon], axis=1)
        place = countries(at[:, 0], at[:, 1])
        tested, refit = forecast.fit(y, near, held, DISCOVERY), forecast.fit(y, near, held, field.MONTHS)
        assert tested["baseline"] == scored[which]["baseline"] == "linear" and int(tested["claimed"].sum()) == scored[which]["claimed"] and round(tested["k"], 3) == scored[which]["k"]
        out.append({"kind": "model", "field": which, "regions": len(y), "baseline": tested["baseline"], "coefficients": [round(float(c), 6) for c in coefficients(y, near)], "k": round(tested["k"], 4), "claims": int(tested["claimed"].sum()), "refit_baseline": refit["baseline"], "refit_k": round(refit["k"], 4), "refit_claims": int(refit["claimed"].sum()), "claims_in_both": int((tested["claimed"] & refit["claimed"]).sum())})
        a, b = terms(tested, x, years), terms(refit, x, years)
        for u, j, m in zip(*np.nonzero(np.isfinite(a) | np.isfinite(b))):
            month = 12 * int(years[j]) + int(m)
            if FIRST <= month <= LAST:
                r = {"kind": "term", "field": which, "region": int(u), "lat": round(float(at[u, 0]), 1), "lon": round(float(at[u, 1]), 1), "country": place[u], "target": label(month)}
                for key, model, t in (("tested", tested, a), ("refit", refit, b)):
                    if np.isfinite(t[u, j, m]):
                        lag = int(model["lag"][m, u])
                        r[key] = {"term": round(float(t[u, j, m]), 4), "lag": lag, "oni": float(x[month - lag])}
                out.append(r)
        t = terms(tested, held, SCORED)
        months = forecast.all_months(SCORED)
        res, got = [v[:, months].reshape(len(y), len(SCORED), 12) for v in (tested["e"], y)]
        said = np.isfinite(t)
        past.append(np.stack([t[said], res[said], got[said]]))
    t, res, got = np.concatenate(past, axis=1)
    for lo, hi in zip(BANDS, BANDS[1:]):
        b = (np.abs(t) >= lo) & (np.abs(t) < hi)
        way = np.sign(t[b])
        out.append({"kind": "band", "from": lo, "to": None if np.isinf(hi) else hi, "n": int(b.sum()), "right_side_of_baseline": round(float((res[b] * way > 0).mean()), 3), "right_side_of_zero": round(float((got[b] * way > 0).mean()), 3), "mean_beyond_baseline": round(float((res[b] * way).mean()), 3), "mean_term": round(float(np.abs(t[b]).mean()), 3)})
    with open(OUT, "w") as f:
        for r in out:
            f.write(json.dumps(r) + "\n")
    for r in out:
        if r["kind"] != "term":
            print(r, flush=True)
    print(sum(r["kind"] == "term" for r in out), "terms")


if __name__ == "__main__":
    main()
