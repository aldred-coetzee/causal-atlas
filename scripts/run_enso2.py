"""The two-gate search on the real field: the same marks and ruler as run_enso.py, with links.both. Rule: results/real-enso-drought-2.md."""
import json
import sys
from pathlib import Path

import numpy as np

from causal_atlas import decoy, field, links
from run_enso import AREAS, DISCOVERY, RULER_LAG, SHARES, SHIFTS, YEARS, data, planted

OUT = Path(__file__).resolve().parents[1] / "results" / "real-enso-drought-2.jsonl"
SEEDS = range(11201, 11221)
RULER_SEEDS = range(11301, 11311)
DEV_SEEDS = range(11901, 11906)  # development only, never in a count


def row(out_file, kind, seed, out, **more):
    r = {"kind": kind, "seed": seed, **out, **more}
    with open(out_file, "a") as f:
        f.write(json.dumps(r) + "\n")
    print(r, flush=True)


def discover(seeds, out_file):
    y, x, lat, lon = data()
    y, x = y[:, :DISCOVERY], x[:DISCOVERY]
    for seed in seeds:
        d = decoy.make(seed, field.MONTHS, field.oni())[:, :DISCOVERY]
        row(out_file, "real", seed, links.both(y, [x, *d], YEARS, SHIFTS, lat, lon))
        row(out_file, "no_oni", seed, links.both(y, list(d), YEARS, SHIFTS, lat, lon))
        order = np.random.default_rng(seed).permutation(DISCOVERY // 12)
        mixed = y.reshape(len(y), -1, 12)[:, order].reshape(len(y), -1)
        row(out_file, "years_mixed", seed, links.both(mixed, [x, *d], YEARS, SHIFTS, lat, lon))


def ruler(seeds, out_file):
    y, x, lat, lon = data()
    y, x = y[:, :DISCOVERY], x[:DISCOVERY]
    for seed in seeds:
        d = decoy.make(seed, field.MONTHS, field.oni())[:, :DISCOVERY]
        for share in SHARES:
            for area in AREAS:
                yp, cells, months = planted(y, lat, lon, d[0], seed, share, area)
                out = links.both(yp, [x, *d], YEARS, SHIFTS, lat, lon)
                more = {"share": share, "area": area, "found": 1 in out["leads"], "false": [c for c in out["leads"] if c > 1]}
                if more["found"]:
                    sig = links.significant(links.correlations(yp, d[0], YEARS), len(YEARS))
                    inside = np.zeros(len(y), bool)
                    inside[cells] = True
                    more["claims"] = int(sig.sum())
                    more["claims_true_cells"] = round(float(sig[:, :, inside].sum() / max(sig.sum(), 1)), 3)
                    more["true_cell_months_claimed"] = round(float(sig[RULER_LAG][months][:, inside].mean()), 3)
                row(out_file, "ruler", seed, out, **more)


if __name__ == "__main__":
    step, dev = sys.argv[1], sys.argv[2:3] == ["dev"]
    out_file = Path(sys.argv[3]) if dev else OUT
    {"discover": discover, "ruler": ruler}[step](DEV_SEEDS if dev else (SEEDS if step == "discover" else RULER_SEEDS), out_file)
