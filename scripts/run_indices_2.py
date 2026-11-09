"""The test of run_indices.py again with one thing changed in the search: the control copies one year either side of the real alignment are left out. Fresh seeds, its own rows. Rule: results/real-indices-2.md."""
import sys
from pathlib import Path

import run_indices as first
from causal_atlas import field

first.OUT = Path(__file__).resolve().parents[1] / "results" / "real-indices-2.jsonl"
first.SHIFTS = range(2, first.DISCOVERY // 12 - 1)  # whole years, 2 to 48: at 1 and 49 the copy's lags meet the real ones
first.SEEDS = {name: range(15101 + 100 * i, 15121 + 100 * i) for i, name in enumerate(field.BOXES)}
first.RULER_SEEDS = {name: range(15601 + 100 * i, 15611 + 100 * i) for i, name in enumerate(field.BOXES)}

if __name__ == "__main__":
    first.main(sys.argv)
