"""Re-run a counted seed from scratch with the repo's own generator, year-end, all 62 shifts, and set it beside its row (nothing is written to the results file)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path("synth").resolve()))
import harvest_panel  # noqa: E402

from causal_atlas import harvest  # noqa: E402

KW = {"none": {"kind": "none"}, "link_20": {"kind": "link", "share": 0.2}, "drift": {"kind": "drift"}}
panel, seed, variant = sys.argv[1], int(sys.argv[2]), sys.argv[3]
w = harvest_panel.make(seed, **KW[panel])
r = harvest.run(w["logy"], w["official"], w["country"], w["cereal"], w["x"], w["lat"], w["lon"], 20, {"year_end": 6, "mid_year": 4}[variant])
v = harvest.reading(r)
row = next(json.loads(s) for s in open("results/harvest-drought.jsonl") if (lambda q: q["panel"] == panel and q["seed"] == seed and q["variant"] == variant)(json.loads(s)))
print(panel, seed, variant, "again:", v["passes"], v["model"]["s"], v["model"]["ci"], v["model"]["beats"], v["flat"]["s"], "| row:", row["passes"], row["s"], row["ci"], row["model"]["beats"], row["flat"]["s"],
      "| same:", v["passes"] == row["passes"] and abs(v["model"]["s"] - row["s"]) < 1e-12 and v["model"]["beats"] == row["model"]["beats"] and abs(v["flat"]["s"] - row["flat"]["s"]) < 1e-12)
