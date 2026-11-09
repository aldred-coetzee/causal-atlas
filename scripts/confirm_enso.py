"""The one-time confirmation of the ONI against the baseline on 2000 to 2024. Rule: results/real-enso-drought.md. Run once, after discovery is frozen and committed."""
import json
import sys

import numpy as np

from causal_atlas import confirm
from run_enso import DISCOVERY, OUT, SAVE, data

if __name__ == "__main__":
    if sys.argv[1:] != ["once"]:
        sys.exit("This scores the sealed years. Run it as: confirm_enso.py once")
    done = [json.loads(line) for line in open(OUT)] if OUT.exists() else []
    if any(r["kind"] == "confirmation" for r in done):
        sys.exit("Already scored. The confirmation period is spent for this driver and field.")
    y, x, lat, lon = data()
    out, parts = confirm.run(y, x, lat, lon, DISCOVERY)
    np.savez(SAVE / "oni_confirmation.npz", lat=lat, lon=lon, **parts)
    with open(OUT, "a") as f:
        f.write(json.dumps({"kind": "confirmation", **out}) + "\n")
    print(out)
