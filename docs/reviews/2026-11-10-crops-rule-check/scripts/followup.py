"""Written by the project session after the reader reported, not by the reader. The reader's hardest world (a curving drift shared by drought and yields at 2.5 times the registered strength, no link in the other crops; its seeds 26010 and 26011, 20 shifts) on more seeds and with all 62 shifts, read as the rule reads: both drivers. Usage: followup.py SEED [SEED ...]; one line a seed to logs/followup.jsonl."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE)]
import rv  # noqa: E402

KW = {"kind": "link", "share": 0.2, "rainfed": 0.0, "crops": 18, "sure": 6, "shape": "drift", "drift_x": 3.0, "drift_y": 0.75}
for seed in map(int, sys.argv[1:]):
    o = rv.go("drift3_62", seed, 62, "year_end", KW)
    with open(HERE.parent / "logs" / "followup.jsonl", "a") as fh:
        fh.write(json.dumps(o) + "\n")
    print(seed, o["passes"], o["model"]["s"], o["model"]["ci"], o["model"]["beats"], o["flat"]["s"], o["flat"]["ci"], o["flat"]["beats"], o["secs"], flush=True)
