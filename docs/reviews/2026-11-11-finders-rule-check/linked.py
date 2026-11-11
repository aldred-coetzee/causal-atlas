"""Reader's check, question 3: in worlds with planted links, how each sent row is classed by the harness (run_finders.stands), by family, and for rows naming a link in full, the share of their places the link is in. One JSON line a world. Seeds 47941 to 47959 only.

    linked.py <kind> <places> <share> <seeds...>
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import run_finders as rf2  # noqa: E402

kind, places, share = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
seeds = [int(s) for s in sys.argv[4:]]
assert all(47941 <= s <= 47959 for s in seeds)
how = {"kind": kind, **rf2.rr.HOW.get(kind, {}), "share": share, "places": places}
for seed in seeds:
    r = rf2.world(how, None, seed, first=False, told=False)
    b = r["board"]
    print(json.dumps({"kind": kind, "seed": seed, "bar": b["bar"], "sent": b["sent"], "passed": b["passed"],
                      "rows": [{k: x[k] for k in ("family", "member", "rel", "link", "inside", "places", "lift", "passes", "label")} for x in b["rows"]]}), flush=True)
