"""Print each SPEC target beside the value from one replicate (training months 36..338).

usage: ~/.local/bin/uv run python synth/check_shape.py [panel] [seed] [ncells]
"""
import sys, time, resource
from pathlib import Path
import numpy as np
import duckdb

sys.path.insert(0, str(Path(__file__).parent))
import generate as G

LO, HI = 36, 339


def moran8(lat, lon, z):
    iy = np.round((lat - lat.min()) / 0.5).astype(int) + 1
    ix = np.round((lon - lon.min()) / 0.5).astype(int) + 1
    sh = (iy.max() + 2, ix.max() + 2)
    zc = z - z.mean()
    g = np.zeros(sh); m = np.zeros(sh)
    g[iy, ix] = zc; m[iy, ix] = 1
    num = np.zeros(sh); W = 0.0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy or dx:
                num += np.roll(np.roll(g, dy, 0), dx, 1) * g
                W += (np.roll(np.roll(m, dy, 0), dx, 1) * m).sum()
    return len(z) / W * num.sum() / (zc ** 2).sum()


def episodes(lat, lon, y):
    by = np.floor(lat / 5).astype(int); bx = np.floor(lon / 5).astype(int)
    key = by * 1000 + bx
    lens = []
    for k in np.unique(key):
        s = y[key == k].sum(0)
        if s.sum() < 12:
            continue
        run = 0
        for v in s > 2 * s.mean():
            if v:
                run += 1
            else:
                if run: lens.append(run)
                run = 0
        if run: lens.append(run)
    if not lens:
        return (0, 0, 0)
    return (np.median(lens), np.percentile(lens, 90), max(lens))


def pooled_ac(a, lag):
    x = a[:, :-lag].ravel(); z = a[:, lag:].ravel()
    return np.corrcoef(x, z)[0, 1]


def main():
    panel = sys.argv[1] if len(sys.argv) > 1 else "pure_null"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    nc = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    cells = duckdb.sql("select lat, lon from 'data/panel/cells.parquet' order by cell").fetchnumpy()
    lat, lon = cells["lat"], cells["lon"]
    if nc:
        sel = np.random.default_rng(0).choice(len(lat), nc, replace=False)
        lat, lon = lat[sel], lon[sel]
    import os
    for kv in filter(None, os.environ.get('SYNTH_P', '').split(';')):
        k, v = kv.split('='); G.P[k] = eval(v)
    t0 = time.time()
    d = G.generate(panel, lat, lon, seed)
    rt = time.time() - t0
    y = d["y"][:, LO:HI].astype(float)
    C = len(lat)
    flat = np.sort(y.ravel())[::-1]; tot = y.sum()
    ct = np.sort(y.sum(1))[::-1]
    mean = y.mean()
    rows = []
    def add(name, real, val): rows.append((name, real, val))
    add("mean count", 0.0097, mean)
    add("share zero", 0.9953, (y == 0).mean())
    add("var/mean", 24.8, y.var() / mean)
    add("share cells any event", 0.210, (y.sum(1) > 0).mean())
    add("lag-1 ac", 0.372, pooled_ac(y, 1))
    add("lag-12 ac", 0.061, pooled_ac(y, 12))
    add("top 0.1% cell-months share", 0.559, flat[:int(round(0.001 * flat.size))].sum() / tot)
    add("top 1% cells share", 0.550, ct[:int(round(0.01 * C))].sum() / tot)
    add("max cell-month", 609, y.max())
    add("top 0.01% cell-months share", 0.214, flat[:int(round(0.0001 * flat.size))].sum() / tot)
    cm = y.mean(0).reshape(-1, 12).mean(0) if False else np.array([y[:, (np.arange(LO, HI) % 12) == m].mean() for m in range(12)])
    add("peak/trough calendar month", 1.99, cm.max() / cm.min())
    add("Moran I log1p total", 0.555, moran8(lat, lon, np.log1p(y.sum(1))))
    e = episodes(lat, lon, y)
    add("episode length median", 1, e[0]); add("episode length p90", 4, e[1]); add("episode length max", 46, e[2])
    by = np.floor(lat / 5).astype(int); bx = np.floor(lon / 5).astype(int); key = by * 1000 + bx
    ann = []
    for k in np.unique(key):
        m = key == k
        if y[m].sum() >= 12:
            a = np.log1p(y[m].sum(0)[:300].reshape(25, 12).sum(1)); ann.append(a - a.mean())
    ann = np.array(ann)
    for lg, real in zip([1, 2, 3, 5], [0.63, 0.43, 0.30, 0.16]):
        add(f"block annual log ac lag {lg}y", real, np.corrcoef(ann[:, :-lg].ravel(), ann[:, lg:].ravel())[0, 1])
    dr = d["drought"][:, LO:HI]
    mon = np.arange(LO, HI) % 12
    an = dr.copy()
    for m in range(12):
        an[:, mon == m] -= an[:, mon == m].mean(1, keepdims=True)
    add("drought anomaly SD", 0.94, an.std())
    add("drought lag-1 ac", 0.71, pooled_ac(an, 1)); add("drought lag-12 ac", 0.04, pooled_ac(an, 12))
    r = np.random.default_rng(5)
    i = r.integers(0, C, 60000); j = r.integers(0, C, 60000)
    dist = np.hypot(lat[i] - lat[j], (lon[i] - lon[j]) * np.cos(np.deg2rad(lat[i])))
    az = (an - an.mean(1, keepdims=True)); az /= az.std(1, keepdims=True) + 1e-12
    cc = (az[i] * az[j]).mean(1)
    for (a, b), real in zip([(0, 2), (2, 5), (5, 10), (10, 20), (20, 40)], [0.91, 0.64, 0.34, 0.13, 0.02]):
        s = (dist >= a) & (dist < b)
        add(f"drought corr {a}-{b} deg", real, cc[s].mean() if s.any() else float("nan"))
    o = d["oni"][LO:HI]
    add("oni SD", 0.85, o.std())
    add("oni lag-1 ac", 0.97, np.corrcoef(o[:-1], o[1:])[0, 1]); add("oni lag-12 ac", -0.03, np.corrcoef(o[:-12], o[12:])[0, 1])
    print(f"panel={panel} seed={seed} cells={C} runtime={rt:.1f}s maxrss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.2f}GB")
    for n, a, b in rows:
        print(f"{n:32s} real {a:>9.4g}   synth {b:>9.4g}")
    if panel == "planted_1.40":
        lk = d["linked"]
        print(f"linked share of cells {lk.mean():.3f}; share of training events in linked cells {y[lk].sum()/tot:.3f}")
    if panel.startswith("planted"):
        m = (d["rate"] != d["rate_no_link"]).mean()
        print(f"share of cell-months where link active {m:.4f}")


main()
