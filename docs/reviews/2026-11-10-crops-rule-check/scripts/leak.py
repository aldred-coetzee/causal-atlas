"""Item 2: replace every yield and drought value from a cut year onward with noise; nothing for an earlier year may change. Seeds 26002 (world), 26003 (noise)."""
import sys
from pathlib import Path
import numpy as np
sys.path[:0] = [str(Path(__file__).resolve().parent)]
import panel_x
from causal_atlas import claims, harvest
FIRST, SURE = 20, 6
w = panel_x.make(26002, kind="link", share=0.35, rainfed=0.5, crops=18, sure=6)
helper = w["cereal"] < SURE
rng = np.random.default_rng(26003)
for cut in (40, 55):  # year index: the cut year and all after are replaced
    y2, x2 = w["logy"].copy(), w["x"].copy()
    fin = np.isfinite(y2[:, cut:])
    y2[:, cut:] = np.where(fin, 7 + 3 * rng.standard_normal(fin.shape), np.nan)
    x2[:, 12 * (cut + 1):] = 5 * rng.standard_normal(x2[:, 12 * (cut + 1):].shape)  # x starts in January of the year before year 0
    sc = cut - (FIRST + harvest.WARM)  # scored column of the cut year
    for variant, up in (("year_end", 6), ("mid_year", 4)):
        res = []
        for drv in ("asfell", "flat"):
            X1, X2 = (w["x"], x2) if drv == "asfell" else (claims.level(w["x"]), claims.level(x2))
            r1 = harvest.run(w["logy"], w["official"], w["country"], w["cereal"], X1, w["lat"], w["lon"], FIRST, up, shifts=[2, 3], flat=False)
            r2 = harvest.run(y2, w["official"], w["country"], w["cereal"], X2, w["lat"], w["lon"], FIRST, up, shifts=[2, 3], flat=False)
            for name, keep in (("scored", ~helper), ("beside", helper)):
                a1, a2 = claims.only(r1, keep), claims.only(r2, keep)
                s1, t1 = claims.standing(a1["unit_now"], a1["unit_term"], a1["pick"])
                s2, t2 = claims.standing(a2["unit_now"], a2["unit_term"], a2["pick"])
                c1 = claims.claimed(a1, w["country"][keep], 1.5); c2 = claims.claimed(a2, w["country"][keep], 1.5)
                same = lambda p, q: bool(np.array_equal(p[:, :sc], q[:, :sc]))
                d = {"now": same(a1["unit_now"], a2["unit_now"]), "term_true": same(a1["unit_term"][..., 0], a2["unit_term"][..., 0]), "term_shifts": same(a1["unit_term"][..., 1:], a2["unit_term"][..., 1:]),
                     "pick": same(a1["pick"], a2["pick"]), "base": same(a1["unit_base"], a2["unit_base"]), "alone": all(same(a1["unit_alone"][k], a2["unit_alone"][k]) for k in a1["unit_alone"]),
                     "model_true": same(a1["unit_model"][..., 0], a2["unit_model"][..., 0]),
                     "slope_true_upto_cut": bool(np.array_equal(s1[:, :sc + 1, 0], s2[:, :sc + 1, 0])), "stand_true_upto_cut": bool(np.array_equal(t1[:, :sc + 1, 0], t2[:, :sc + 1, 0])),
                     "claim_true": same(c1["claim"], c2["claim"]), "error_on_claims": same(c1["error"], c2["error"]),
                     "weights": bool(np.array_equal(r1["weights"][:sc], r2["weights"][:sc])), "chosen": r1["chosen"][:sc] == r2["chosen"][:sc],
                     "max_abs_term_true_diff_before": float(np.abs(a1["unit_term"][:, :sc, 0] - a2["unit_term"][:, :sc, 0]).max())}
                print(cut, variant, drv, name, d, flush=True)
