"""All 1b replicates, pass-mark panels first. Resumes from the output file; stops at the 24 hour ceiling."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "1b-replicates.jsonl"
NULLS = ["pure_null", "shared_null", "combo_null"]
PANELS = ["planted_3.00", *NULLS, "planted_2.40", "planted_combo_6", "planted_2.00"]
SEEDS = range(1001, 1021)
SHUFFLE_ALWAYS = 3  # the first seeds of each null, to show the shuffled distribution
CEILING = 24 * 3600

done = set()
if OUT.exists():
    done = {(r["panel"], r["seed"]) for r in map(json.loads, OUT.read_text().splitlines())}
start = time.time()
for panel in PANELS:
    for seed in SEEDS:
        if (panel, seed) in done:
            continue
        if time.time() - start > CEILING:
            sys.exit("ceiling reached: 24 hours")
        cmd = [sys.executable, str(ROOT / "scripts" / "run_1b.py"), panel, str(seed), "full"]
        if panel in NULLS and seed < SEEDS[0] + SHUFFLE_ALWAYS:
            cmd.append("--always-shuffle")
        subprocess.run(cmd, check=True)
print("all replicates done")
