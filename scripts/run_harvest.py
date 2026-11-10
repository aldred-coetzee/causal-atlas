"""National cereal harvests and drought: does the weather of the months to a harvest, as each country's own drought index, improve an estimate of that year's official yield beyond the yield's own past? First on made-up records with a link, with none, with a drift and with a step in both, by the marks in results/harvest-drought.md; then, once, on the real record."""
import json
import os
import sys
from pathlib import Path

import numpy as np

from causal_atlas import harvest, yields

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "synth"))
import harvest_panel  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "harvest-drought.jsonl"
FIRST = 20  # the first year forecast, on the record's clock: 1981. Scored from FIRST + harvest.WARM: 1986
VARIANTS = {"year_end": 6, "mid_year": 4}  # how many of harvest.SEASONS are known: to December of the harvest year, or to June
MADE_UP = {  # name: (how the record is made, seeds)
    "link_20": ({"kind": "link", "share": 0.20}, range(22001, 22011)),
    "link_10": ({"kind": "link", "share": 0.10}, range(22101, 22111)),
    "link_05": ({"kind": "link", "share": 0.05}, range(22201, 22211)),
    "none": ({"kind": "none"}, range(22301, 22331)),
    "drift": ({"kind": "drift"}, range(22401, 22421)),
    "step": ({"kind": "step"}, range(22501, 22521)),
    "few_20": ({"kind": "link", "share": 0.20, "linked": 0.2}, range(22601, 22611)),  # the link in a fifth of the countries, not half
}
MARKS = {"link_20": ("least", 8), "none": ("most", 1), "drift": ("most", 1), "step": ("most", 1)}  # seeds read as a link, for each variant
MID_YEAR = ("link_20", "none", "drift", "step")  # the panels the mid-year variant is run on


def row(r):
    f = os.open(OUT, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)  # one write a row, so several processes may share the file
    os.write(f, (json.dumps(r) + "\n").encode())
    os.close(f)
    print({k: v for k, v in r.items() if k not in ("by_year", "kept_units", "weights")}, flush=True)


def rows():
    return [json.loads(s) for s in open(OUT)] if OUT.exists() else []


def read(r):
    """What is kept of one run: the verdict, the units followed into the later years, and the sums by year."""
    v, k = harvest.reading(r), harvest.kept(r)
    out = {"scored": r["scored"], "passes": v["passes"], "size": v["size"], "s": v["model"]["s"], "ci": v["model"]["ci"], "model": v["model"], "flat": v["flat"], "below": v["below"], "without_best": v["without_best"],
           "kept": {a: b for a, b in k.items() if a != "units"}, "kept_units": k["units"],
           "by_cereal": {c: 1 - m / b for c, (b, m) in r["by_cereal"].items()}, "weights": np.round(r["weights"], 4).tolist(), "chosen": sorted(set(r["chosen"])),
           "by_year": {"years": r["years"].tolist(), "base": r["base"].tolist(), "model": r["model"][:, 0].tolist(), "shift_mean": r["model"][:, 1:].mean(axis=1).tolist(), "flat": r["flat"][:, 0].tolist()}}
    return out, k


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
                r = harvest.run(w["logy"], w["official"], w["country"], w["cereal"], w["x"], w["lat"], w["lon"], FIRST, upto)
                out, k = read(r)
                lk = w["linked"]
                gain = lambda pick: float(1 - r["unit_model"][pick][:, :, 0].sum() / r["unit_base"][pick].sum()) if pick.any() else None  # noqa: E731
                row({"kind": "made_up", "panel": name, "variant": variant, "seed": seed, "units": len(lk), "linked_units": int(lk.sum()), **out,
                     "gain_linked": gain(lk), "gain_unlinked": gain(~lk), "kept_linked": float(lk[k["units"]].mean())})


def marks(done):
    """By variant and made-up panel: seeds run and seeds read as a link; and whether each mark holds."""
    out, held = {}, {}
    for variant in VARIANTS:
        for name, (_, seeds) in MADE_UP.items():
            if variant == "mid_year" and name not in MID_YEAR:
                continue
            got = [r for r in done if r["kind"] == "made_up" and r["panel"] == name and r["variant"] == variant]
            out[variant, name] = {"seeds": len(got), "of": len(seeds), "link": sum(r["passes"] for r in got)}
            if name in MARKS:
                side, n = MARKS[name]
                held[variant, name] = len(got) == len(seeds) and (out[variant, name]["link"] >= n if side == "least" else out[variant, name]["link"] <= n)
    return out, held


def real():
    """Once: the real record, year-end and then mid-year. Both are read before either is written, so a run that stops part-way leaves nothing behind."""
    done = rows()
    if any(r["kind"] == "real" for r in done):
        sys.exit("Already scored. The harvest record is spent for this driver.")
    held = marks(done)[1]
    if not all(v for (variant, _), v in held.items() if variant == "year_end"):
        sys.exit("The made-up records are incomplete or a mark missed. No real harvest is set against drought.")
    p = yields.panel()
    country = np.searchsorted(p["codes"], p["code"])
    cereal = np.array([yields.CEREALS.index(i) for i in p["item"]])
    both = []
    for variant, upto in VARIANTS.items():
        r = harvest.run(p["logy"], p["official"], country, cereal, p["x"], p["lat"], p["lon"], FIRST, upto)
        out, k = read(r)
        gain = 1 - r["unit_model"][:, :, 0].sum(axis=1) / np.maximum(r["unit_base"].sum(axis=1), 1e-12)
        both.append({"kind": "real", "variant": variant, "units": len(country), "countries": len(p["codes"]), "marks_held": all(v for (a, _), v in held.items() if a == variant), **out,
             "by_unit": [[str(p["code"][u]), str(p["item"][u]), int(r["pick"][u].sum()), round(float(gain[u]), 4)] for u in range(len(country))],
             "kept_named": [[str(p["code"][u]), str(p["item"][u])] for u in k["units"]]})
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
        sys.exit("run_harvest.py known [panel ...] [part parts] | marks | real once")
