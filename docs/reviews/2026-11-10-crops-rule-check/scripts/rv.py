"""Reviewer's runner: one made-up world (from panel_x, a copy of synth/harvest_panel.py with knobs), read as run_claims.read reads it, with a chosen number of shifts, and diagnostics. Usage: rv.py TAG SEED NSHIFTS VARIANT JSON_KWARGS"""
import json, sys, time
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import panel_x
from causal_atlas import claims, harvest

FIRST, SURE = 20, 6
VAR = {"year_end": 6, "mid_year": 4}

def go(tag, seed, nshift, variant, kw):
    t0 = time.time()
    w = panel_x.make(seed, **kw)
    helper = w["cereal"] < SURE
    years = w["logy"].shape[1]
    allsh = list(range(2, years))
    sh = allsh if nshift >= len(allsh) else [allsh[i] for i in np.linspace(0, len(allsh) - 1, nshift).round().astype(int)]
    up = VAR[variant]
    r = harvest.run(w["logy"], w["official"], w["country"], w["cereal"], w["x"], w["lat"], w["lon"], FIRST, up, shifts=sh, flat=False)
    f = harvest.run(w["logy"], w["official"], w["country"], w["cereal"], claims.level(w["x"]), w["lat"], w["lon"], FIRST, up, shifts=sh, flat=False)
    a, b = claims.only(r, ~helper), claims.only(f, ~helper)
    ctry = w["country"][~helper]
    v = claims.reading(a, b, ctry)
    L = v[claims.MAIN]
    c = claims.claimed(a, ctry, claims.MAIN)
    # diagnostics: size of the term as fell vs under shifts, in the scored records and in the cereal-like
    rms = lambda q, keep: np.sqrt((q["unit_term"][keep] ** 2).sum(axis=(0, 1)) / max(q["pick"][keep].sum(), 1))
    tr = rms(r, ~helper); tc = rms(r, helper)
    # S of every shift on its own claims, to place the true one
    now, term, pick = a["unit_now"], a["unit_term"], a["pick"]
    slope, t = claims.standing(now, term, pick)
    cl = (t >= claims.MAIN) & pick[:, :, None]
    bb = np.where(pick, now ** 2, 0)
    m = np.where(cl, (now[:, :, None] - np.clip(slope, 0, claims.CAP) * term) ** 2, 0)
    num, den = m.sum(axis=(0, 1)), (cl * bb[:, :, None]).sum(axis=(0, 1))
    S = np.where(den > 0, 1 - num / np.maximum(den, 1e-12), 0.0)
    scaled = float((np.clip(slope[..., 0], 0, 1)[c["claim"]] < 1).mean()) if c["claim"].any() else None
    lk = w["linked"][~helper]
    out = {"tag": tag, "seed": seed, "variant": variant, "nshift": len(sh), "kw": kw, "units": int((~helper).sum()), "beside": int(helper.sum()), "linked_units": int(lk.sum()),
           "passes": L["passes"], "word": L["word"], "size": L["size"],
           "model": {k: L["model"][k] for k in ("s", "ci", "beats", "shifts", "shift_max", "shift_mean", "without_best", "records", "countries", "below")},
           "flat": {k: L["flat"][k] for k in ("s", "ci", "beats", "shifts", "shift_max", "without_best", "records", "countries", "below")},
           "levels": {str(k): [vv["passes"], vv["model"]["s"], vv["model"]["ci"][0], vv["model"]["beats"]] for k, vv in v.items()},
           "term_rms_scored_true": float(tr[0]), "term_rms_scored_shift_mean": float(tr[1:].mean()), "term_rms_cereal_true": float(tc[0]), "term_rms_cereal_shift_mean": float(tc[1:].mean()),
           "S_all_cols": [round(float(s), 6) for s in S], "frac_claims_slope_below_cap": scaled,
           "claims_linked": float(c["claim"][lk].sum() / max(c["claim"].sum(), 1)), "secs": round(time.time() - t0)}
    return out

if __name__ == "__main__":
    tag, seed, nshift, variant = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    kw = json.loads(sys.argv[5])
    o = go(tag, seed, nshift, variant, kw)
    with open(HERE.parent / "logs" / "runs.jsonl", "a") as fh:
        fh.write(json.dumps(o) + "\n")
    print(json.dumps({k: v for k, v in o.items() if k != "S_all_cols"}))
