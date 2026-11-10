"""Other crops and drought: in the records where the drought term of the harvest forecast has gone with a crop's yield before, does it go on helping, and by how much? The six cereals, already read, run beside the other crops and are not scored. First on made-up records, by the marks in results/crops-drought.md; then, once, on the real record."""
import json
import os
import sys
from pathlib import Path

import numpy as np

from causal_atlas import claims, harvest, yields

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import harvest_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "crops-drought.jsonl"
FIRST = 20  # the first year forecast, on the record's clock: 1981. Scored from FIRST + harvest.WARM: 1986
VARIANTS = {"year_end": 6, "mid_year": 4}  # how many of harvest.SEASONS are known: to December of the harvest year, or to June
SURE = 6  # the made-up crops that stand for the six cereals: linked wherever their country is, run beside the others, not scored
SMALL = {"crops": 18, "sure": SURE}  # a made-up world of six such crops and twelve others
FULL = {"crops": 53, "sure": SURE}  # and one the size of the real record: six and forty-seven
LEAK = {"kind": "link", "share": 0.20, "rainfed": 0.0}  # the six linked at 20% of variance, as in the cereal test; no other crop linked anywhere
LINK = {"kind": "link", "share": 0.35, "rainfed": 0.5}  # each other crop rain-fed with chance a half, and linked at 35% where its country is
MADE_UP = {  # name: (how the record is made, seeds)
    "leak": ({**LEAK, **SMALL}, range(25001, 25021)),
    "leak_drift": ({**LEAK, **SMALL, "shape": "drift"}, range(25101, 25111)),
    "leak_step": ({**LEAK, **SMALL, "shape": "step"}, range(25201, 25211)),
    "none": ({"kind": "none", **SMALL}, range(25301, 25311)),
    "link": ({**LINK, **SMALL}, range(25401, 25411)),
    "few": ({**LINK, **SMALL, "rainfed": 0.2}, range(25501, 25511)),
    "weak": ({**LINK, **SMALL, "share": 0.20}, range(25801, 25811)),
    "full_leak": ({**LEAK, **FULL}, range(25601, 25606)),
    "full_link": ({**LINK, **FULL}, range(25701, 25706)),
}
MARKS = {"leak": ("most", 1), "leak_drift": ("most", 1), "leak_step": ("most", 1), "none": ("most", 1), "full_leak": ("most", 1), "link": ("least", 8)}  # seeds read at claims.MAIN, for each variant run
MID_YEAR = ("leak", "link")  # the panels the mid-year variant is run on


def row(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r) + "\n").encode())
    os.close(f)
    print({k: v for k, v in r.items() if k not in ("by_unit", "by_crop", "by_country", "weights", "weights_flat", "levels", "pooled")}, flush=True)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def read(y, official, country, crop, x, lat, lon, helper, upto):
    """One record, read once: the forecast with the driver as it fell and with its level and line out, every record together; then the verdict on the records that are scored. Returns what is kept, and the scored records' parts with the claims at claims.MAIN."""
    r = harvest.run(y, official, country, crop, x, lat, lon, FIRST, upto, flat=False)
    f = harvest.run(y, official, country, crop, claims.level(x), lat, lon, FIRST, upto, flat=False)
    a, b = claims.only(r, ~helper), claims.only(f, ~helper)
    v = claims.reading(a, b, country[~helper])
    main = v[claims.MAIN]
    out = {"scored": int(a["pick"].sum()), "passes": main["passes"], "size": main["size"], "plain": main["plain"], "word": main["word"], "levels": {str(at): w for at, w in v.items()},
           "pooled": claims.pooled(a, b, country[~helper]), "weights": np.round(r["weights"], 4).tolist(), "weights_flat": np.round(f["weights"], 4).tolist(), "chosen": sorted(set(r["chosen"]))}
    return out, a, claims.claimed(a, country[~helper], claims.MAIN)


def known(names, part=0, parts=1):
    """Rule 3: the made-up records, each seed read as the real record would be."""
    done = {(r["panel"], r["variant"], r["seed"]) for r in rows() if r["kind"] == "made_up"}
    for name in names:
        how, seeds = MADE_UP[name]
        for seed in list(seeds)[part::parts]:
            w = None
            for variant, upto in VARIANTS.items():
                if (name, variant, seed) in done or (variant == "mid_year" and name not in MID_YEAR):
                    continue
                w = w or harvest_panel.make(seed, **how)
                helper = w["cereal"] < SURE
                out, a, c = read(w["logy"], w["official"], w["country"], w["cereal"], w["x"], w["lat"], w["lon"], helper, upto)
                lk = w["linked"][~helper]
                gain = lambda pick: float(1 - a["unit_model"][pick][:, :, 0].sum() / a["unit_base"][pick].sum()) if pick.any() else None  # noqa: E731
                row({"kind": "made_up", "panel": name, "variant": variant, "seed": seed, "units": int((~helper).sum()), "beside": int(helper.sum()), "linked_units": int(lk.sum()), **out,
                     "gain_linked": gain(lk), "gain_unlinked": gain(~lk), "claims_linked": float(c["claim"][lk].sum() / max(c["claim"].sum(), 1))})


def marks(done):
    """By variant and made-up panel: seeds run and seeds read at claims.MAIN; and whether each mark holds."""
    out, held = {}, {}
    for variant in VARIANTS:
        for name, (_, seeds) in MADE_UP.items():
            if variant == "mid_year" and name not in MID_YEAR:
                continue
            got = [r for r in done if r["kind"] == "made_up" and r["panel"] == name and r["variant"] == variant]
            out[variant, name] = {"seeds": len(got), "of": len(seeds), "read": sum(r["passes"] for r in got)}
            if name in MARKS:
                side, n = MARKS[name]
                held[variant, name] = len(got) == len(seeds) and (out[variant, name]["read"] >= n if side == "least" else out[variant, name]["read"] <= n)
    return out, held


def real():
    """Once: the real record, year-end and then mid-year. Both are read before either is written, so a run that stops part-way leaves nothing behind."""
    done = rows()
    if any(r["kind"] == "real" for r in done):
        sys.exit("Already scored. These crops' records are spent for this driver.")
    held = marks(done)[1]
    if not all(v for (variant, _), v in held.items() if variant == "year_end"):
        sys.exit("The made-up records are incomplete or a year-end mark missed. No yield of these crops is set against drought.")
    crops = yields.CEREALS + yields.others()
    p = yields.panel(crops, "crops")
    country = np.searchsorted(p["codes"], p["code"])
    crop = np.array([crops.index(i) for i in p["item"]])
    helper = crop < len(yields.CEREALS)
    both = []
    for variant, upto in VARIANTS.items():
        out, a, c = read(p["logy"], p["official"], country, crop, p["x"], p["lat"], p["lon"], helper, upto)
        code, item, pick = p["code"][~helper], p["item"][~helper], a["pick"]
        base = np.where(c["claim"], a["unit_base"], 0)
        gain = base - c["error"]  # by record and year: what the claims took off the baseline's squared error
        by = lambda keys: sorted(([str(k), int(c["claim"][keys == k].any(axis=1).sum()), int(c["claim"][keys == k].sum()), round(float(base[keys == k].sum()), 3), round(float(gain[keys == k].sum()), 3)] for k in np.unique(keys)), key=lambda v: -v[4])  # noqa: E731
        both.append({"kind": "real", "variant": variant, "units": int((~helper).sum()), "beside": int(helper.sum()), "countries": int(len(np.unique(code))), "crops": int(len(np.unique(item))), "marked": all(v for (w, _), v in held.items() if w == variant), **out,
                     "by_crop": by(item), "by_country": by(code),  # name, records that claim, record-years claimed, the baseline's squared error there, and what the claims took off it
                     "by_unit": [[str(code[u]), str(item[u]), int(pick[u].sum()), int(c["claim"][u].sum()), round(float(base[u].sum()), 3), round(float(gain[u].sum()), 3)] for u in range(len(code))]})
    for r in both:
        row(r)


if __name__ == "__main__":
    if sys.argv[1] == "known":
        names = [a for a in sys.argv[2:] if a in MADE_UP] or list(MADE_UP)
        split = [int(a) for a in sys.argv[2:] if a.isdigit()] or [0, 1]
        known(names, *split)
    elif sys.argv[1] == "marks":
        print(*marks(rows()), sep="\n")
    elif sys.argv[1:] == ["real", "once"]:
        real()
    else:
        sys.exit("run_claims.py known [panel ...] [part parts] | marks | real once")
