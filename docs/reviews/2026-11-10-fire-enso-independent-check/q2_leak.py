"""Question 2: does anything after 2003 reach what is fitted? The burned-area and observed-share values after 2003 are replaced by noise in memory (two different draws), never read out, and the field, the cells kept, the months in use, what the satellite saw, and one real and one sight row of step 1 are rebuilt and compared."""
import json, sys, tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0, "src"); sys.path.insert(0, "scripts")
from causal_atlas import fire, links, decoy

FIT = fire.FIT
x = fire.oni()
oni_rows = {int(l.split()[0]): [float(v) for v in l.split()[1:]] for l in open("data/raw/oni.data") if len(l.split()) == 13 and l.split()[0].isdigit()}
print("ONI on the fire clock: month 0 =", x[0], "(1982 Jan in file:", oni_rows[1982][0], ") month 263 =", x[263], "(2003 Dec:", oni_rows[2003][11], ") length", len(x), "=", fire.MONTHS)
assert np.allclose(x, np.ravel([oni_rows[y] for y in range(1982, 2019)]))

burned0, observed0, burnable0 = fire.grid()
orig = {}
for name in ("south_southeast_asia", "europe"):
    y, lat, lon, used = fire.box(name)
    orig[name] = (y[:, :FIT].copy(), lat.copy(), lon.copy(), used.copy(), fire.sight(name)[:, :FIT].copy())

results = {}
for draw in (1, 2):
    rng = np.random.default_rng(draw)
    b, o = burned0.copy(), observed0.copy()
    late = slice(FIT, None)
    b[late] = rng.gamma(0.3, 50.0, b[late].shape).astype(np.float32) * (rng.random(b[late].shape) < 0.5)
    o[late] = rng.random(o[late].shape).astype(np.float32)
    tmp = Path(tempfile.mkdtemp()); (tmp / "real").mkdir()
    fire.PANEL = tmp
    fire.grid = lambda b=b, o=o: (b, o, burnable0)
    for name in orig:
        y, lat, lon, used = fire.box(name)
        s = fire.sight(name)
        Y0, la0, lo0, u0, s0 = orig[name]
        ok = (y.shape[0] == Y0.shape[0] and np.array_equal(y[:, :FIT], Y0) and np.array_equal(lat, la0) and np.array_equal(lon, lo0) and np.array_equal(used, u0) and np.array_equal(s[:, :FIT], s0))
        print(f"draw {draw} {name}: fitting values, cells, months in use and sight identical: {ok}")
    # one real and one sight row of step 1, rebuilt on the noised record
    name, seed = "south_southeast_asia", 17401
    y, lat, lon, _ = fire.box(name)
    y, seen = y[:, :FIT], fire.sight(name)[:, :FIT]
    d = decoy.make(seed, fire.MONTHS, fire.oni())[:, :FIT]
    YEARS = np.array([v for v in range(1, FIT // 12) if v != 12]); SHIFTS = range(2, FIT // 12 - 1)
    results[draw] = {k: links.both(f, [x[:FIT], *d], YEARS, SHIFTS, lat, lon) for k, f in (("real", y), ("sight", seen))}
rows = {r["kind"]: r for r in map(json.loads, open("results/fire-enso.jsonl")) if r.get("field") == "south_southeast_asia" and r.get("seed") == 17401 and r["kind"] in ("real", "sight")}
for k in ("real", "sight"):
    same = all(results[d][k]["leads"] == rows[k]["leads"] and results[d][k]["sharp"] == rows[k]["sharp"] and results[d][k]["broad"] == rows[k]["broad"] for d in (1, 2))
    print(f"step 1 row {k}, seed 17401, rebuilt on both noised records equals the committed row: {same}")
