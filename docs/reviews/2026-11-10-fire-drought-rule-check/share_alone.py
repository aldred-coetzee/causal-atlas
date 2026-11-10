"""The real share observed alone (no burned-area value, no drought): how many used cell-months fall below the 0.2 seen threshold, by period, and the field-mean share by year."""
import numpy as np
from causal_atlas import fire
_, observed, _ = fire.grid()
for name in fire.FIELDS:
    _, _, _, used = fire.box(name)
    at = np.load(fire.PANEL / "real" / f"fire_{name}.npz")["at"]
    i, j, _, _ = fire.where(name)
    o = observed[:, i[at], j[at]].T.reshape(len(at), -1, 12)
    u = np.broadcast_to(used[:, None, :], o.shape)
    def low(a, b):
        sl = o[:, a:b][u[:, a:b]]
        sl = sl[np.isfinite(sl)]
        return (sl < fire.SEEN).mean()
    yearly = np.nanmean(np.where(u, o, np.nan), axis=(0, 2))
    print(f"{name:20s} unseen among used: 1982-2003 {low(0, 22):.3f}  2004-2018 {low(22, 37):.3f} | mean share by year: {np.round(yearly, 2).tolist()}")
