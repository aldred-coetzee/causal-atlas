"""Item 1: an independent forecast, written from the words of the Method section, sharing no forecast code with harvest.py.
Baselines: mean of the last three known values (mean3), and a ten-year straight line (trend10, 6 of 10 needed), each own code.
Errors over each record's past scale (rms of earlier year-on-year changes, at least 9 of them, floor 0.02), clipped at 4.
Driver: each country's SPEI-3 at the same six months; each value standardised with the country's earlier years only.
Slopes of the error on the six values, fitted by ridge on all earlier years' official targets:
  A: one slope set per cereal (pooled over all countries), ridge 10
  B: one slope set per cereal x latitude band (south of 23.5S..., tropics, north), ridge 10
  C: one slope set per record, ridge 10
Scored on official figures 1986 to 2024, same as the project."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
import common

MONTHS = ((-1, 9), (-1, 12), (0, 3), (0, 6), (0, 9), (0, 12))
SCORE0 = 25  # 1986
PRED0 = 20   # first year forecast: 1981; slopes fitted on every earlier year with an error
RIDGE = 10.0


def own_baselines(y):
    U, T = y.shape
    m3 = np.full((U, T), np.nan); tr = np.full((U, T), np.nan)
    for t in range(1, T):
        w = y[:, max(0, t - 3):t]; ok = np.isfinite(w)
        m3[:, t] = np.where(ok.any(1), np.nansum(w, 1) / np.maximum(ok.sum(1), 1), np.nan)
        w = y[:, max(0, t - 10):t]; ok = np.isfinite(w); n = ok.sum(1)
        k = np.arange(w.shape[1]) - w.shape[1]
        for u in np.flatnonzero(n >= 6):
            kk, yy = k[ok[u]], w[u, ok[u]]
            b = np.polyfit(kk, yy, 1)
            tr[u, t] = b[1]  # value at k=0, the year being forecast
    return {"mean3": m3, "trend10": tr}


def own_scale(y):
    U, T = y.shape
    out = np.full((U, T), np.nan)
    d = np.diff(y, axis=1)
    for t in range(2, T):
        dd = d[:, :t - 1]; ok = np.isfinite(dd)
        out[:, t] = np.where(ok.sum(1) >= 9, np.sqrt(np.nansum(dd ** 2, 1) / np.maximum(ok.sum(1), 1)), np.nan)
    return np.maximum(out, 0.02)


def drivers(x, T):
    """countries x years x 6, each value standardised by the country's earlier years' values of the same month slot."""
    raw = np.stack([x[:, 12 * (np.arange(T) + 1 + dy) + m - 1] for dy, m in MONTHS], axis=2)
    out = np.full(raw.shape, np.nan)
    for t in range(3, T):
        mu = raw[:, :t].mean(1); sd = raw[:, :t].std(1)
        out[:, t] = (raw[:, t] - mu) / np.maximum(sd, 1e-6)
    return out


class Own:
    def __init__(self, p, country, cereal, base="mean3"):
        self.y, self.off, self.country, self.cereal = p["logy"], p["official"], country, cereal
        U, T = self.y.shape
        self.T = T
        s = own_scale(self.y)
        b = own_baselines(self.y)[base]
        self.z = np.clip((self.y - b) / s, -4, 4)
        self.target = self.off & np.isfinite(self.z)
        lat = p["lat"][country]
        band = np.where(lat < -23.5, 0, np.where(lat <= 23.5, 1, 2))
        self.groups = {"A": cereal, "B": cereal * 3 + band, "C": np.arange(U)}

    def run(self, x, models=("A", "B", "C")):
        """Returns per unit x scored-year squared errors: base, and each model."""
        f = drivers(x, self.T)[self.country]  # units x years x 6
        U, T = self.z.shape
        tg = self.target & np.isfinite(f).all(2)
        z = np.where(tg, self.z, 0); fz = np.where(tg[:, :, None], f, 0)
        xx = np.einsum("uti,utj->utij", fz, fz); xz = fz * z[:, :, None]
        cxx, cxz = np.cumsum(xx, 1), np.cumsum(xz, 1)
        out = {"base": np.where(tg, z ** 2, 0)[:, SCORE0:]}
        preds = {}
        for mname in models:
            g = self.groups[mname]; G = g.max() + 1
            pred = np.zeros((U, T))
            for t in range(PRED0, T):
                A = cxx[:, t - 1]; c = cxz[:, t - 1]
                GA = np.zeros((G, 6, 6)); Gc = np.zeros((G, 6))
                np.add.at(GA, g, A); np.add.at(Gc, g, c)
                beta = np.linalg.solve(GA + RIDGE * np.eye(6), Gc[:, :, None])[:, :, 0]
                pred[:, t] = np.where(tg[:, t], np.clip((beta[g] * np.nan_to_num(f[:, t])).sum(1), -4, 4), 0)
            out[mname] = np.where(tg, (z - pred) ** 2, 0)[:, SCORE0:]
            preds[mname] = pred
        # D: the three combined with weights none below zero, shared by all records, fitted on earlier years' out-of-time forecasts
        from scipy.optimize import nnls
        P = np.stack([preds[m] for m in models], 2)
        comb = np.zeros((U, T))
        for t in range(SCORE0, T):
            back = tg[:, PRED0:t]
            w, _ = nnls(P[:, PRED0:t][back], z[:, PRED0:t][back])
            comb[:, t] = P[:, t] @ w
            self.w = w
        out["D"] = np.where(tg, (z - comb) ** 2, 0)[:, SCORE0:]
        return out

    def slopes(self, x, mname="B"):
        f = drivers(x, self.T)[self.country]
        tg = self.target & np.isfinite(f).all(2)
        z = np.where(tg, self.z, 0); fz = np.where(tg[:, :, None], f, 0)
        g = self.groups[mname]; G = g.max() + 1
        A = np.einsum("uti,utj->uij", fz, fz); c = np.einsum("uti,ut->ui", fz, z)
        GA = np.zeros((G, 6, 6)); Gc = np.zeros((G, 6)); np.add.at(GA, g, A); np.add.at(Gc, g, c)
        return np.linalg.solve(GA + RIDGE * np.eye(6), Gc[:, :, None])[:, :, 0]


def S(o, m, units=None):
    b, e = o["base"], o[m]
    if units is not None:
        b, e = b[units], e[units]
    return float(1 - e.sum() / b.sum())


if __name__ == "__main__":
    p, country, cereal = common.real()
    x = p["x"]
    for base in ("mean3", "trend10"):
        own = Own(p, country, cereal, base)
        o = own.run(x)
        print(base, "scored", int((o["base"] > 0).sum()), {m: round(100 * S(o, m), 2) for m in "ABCD"}, flush=True)
        for m in "ABCD":
            print("  ", m, "interval over years", [round(100 * v, 2) for v in common.boot(o[m].sum(0), o["base"].sum(0), 24002)])
        sh = {m: [] for m in "ABCD"}
        for k in range(2, 64):
            os_ = own.run(np.roll(x, 12 * k, axis=1))
            for m in "ABCD":
                sh[m].append(S(os_, m))
        for m in "ABCD":
            a = np.array(sh[m])
            print("  ", m, "S %.2f%%" % (100 * S(o, m)), "shifts mean %.2f%% max %.2f%% beaten %d of 62" % (100 * a.mean(), 100 * a.max(), (S(o, m) > a).sum()), flush=True)
