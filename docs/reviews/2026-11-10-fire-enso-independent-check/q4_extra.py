"""Question 4: in runs where the broad gate alarms with controls 2..20 but not with 1..21, where was the overall largest value among all 22 alignments?"""
import glob, json, sys
from collections import Counter
rows = [json.loads(s) for f in sorted(glob.glob(sys.argv[1] + "/*.jsonl*")) for s in open(f)]
for gate in ("broad", "sharp"):
    extra = [r for r in rows if r["cut"][gate] and not r["full"][gate]]
    lost = [r for r in rows if r["full"][gate] and not r["cut"][gate]]
    print(gate, f"runs alarmed only with 2..20: {len(extra)}, only with 1..21: {len(lost)}, of {len(rows)};",
          "where the overall max sat in the first group:", dict(Counter(r[f'argmax_{gate}_rot'] for r in extra)))
