"""Question 3: recompute every number in 'Result of step 1' from results/fire-enso.jsonl."""
import json, collections
R = [json.loads(s) for s in open("results/fire-enso.jsonl")]
F = ["africa", "south_america", "australia", "south_southeast_asia", "north_america", "europe"]
fields = sorted({r["field"] for r in R}, key=F.index) if all(r["field"] in F for r in R) else sorted({r["field"] for r in R})
print("fields", fields)
k = lambda kind: [r for r in R if r["kind"] == kind]
for f in fields:
    print(f, "oni named real", sum(0 in r["leads"] for r in k("real") if r["field"] == f),
          "sight", sum(0 in r["leads"] for r in k("sight") if r["field"] == f))
print("F1 decoy lead (real)", sum(any(c > 0 for c in r["leads"]) for r in k("real")))
print("F2 no_oni", sum(bool(r["leads"]) for r in k("no_oni")))
print("F3 mixed", sum(bool(r["leads"]) for r in k("years_mixed")))
for kind in ("real", "no_oni", "years_mixed"):
    off = 1 if kind != "no_oni" else 0
    b = sum(any(c >= off for c in r["broad"]["leads"]) for r in k(kind)) if kind != "no_oni" else sum(bool(r["broad"]["leads"]) for r in k(kind))
    s = sum(any(c >= off for c in r["sharp"]["leads"]) for r in k(kind)) if kind != "no_oni" else sum(bool(r["sharp"]["leads"]) for r in k(kind))
    both_ = sum((bool([c for c in r["broad"]["leads"] if c >= off]) and bool([c for c in r["sharp"]["leads"] if c >= off])) for r in k(kind))
    print(kind, "broad", b, "sharp", s, "both gates", both_)
# kinds 1 and 2 identical alarms?
a = {(r["field"], r["seed"]): sorted(c - 1 for c in r["leads"] if c > 0) for r in k("real")}
b = {(r["field"], r["seed"]): sorted(r["leads"]) for r in k("no_oni")}
print("real alarms == no_oni alarms (decoy index aligned):", sum(a[x] == b[x] for x in a), "of", len(a))
print("same runs alarmed:", sum(bool(a[x]) == bool(b[x]) for x in a))
m = {(r["field"], r["seed"]): bool(r["leads"]) for r in k("years_mixed")}
print("overlap real-alarm & mixed-alarm runs:", sum(bool(a[x]) and m[x] for x in a))
# alarms by field
for kind in ("real", "no_oni", "years_mixed"):
    c = collections.Counter(r["field"] for r in k(kind) if (any(x > 0 for x in r["leads"]) if kind == "real" else bool(r["leads"])))
    print(kind, dict(c))
bars = [r["sharp"]["bar"] for kind in ("real", "no_oni", "years_mixed", "sight") for r in k(kind)]
print("sharp bar range all 480", min(bars), max(bars))
bars = [r["sharp"]["bar"] for kind in ("real", "no_oni", "years_mixed") for r in k(kind)]
print("sharp bar range 360 (kinds 1-3)", min(bars), max(bars))
bars = [r["sharp"]["bar"] for r in k("real")]
print("sharp bar real 120", min(bars), max(bars))
bars = [r["sharp"]["bar"] for r in k("real") if r["field"] == "south_southeast_asia"]
print("sharp bar real SSEA", min(bars), max(bars))
# ruler
ru = k("ruler")
for f in fields:
    row = []
    for s in (0.05, 0.15, 0.40):
        for ar in (0.05, 0.25):
            row.append(sum(r["found"] for r in ru if (r["field"], r["share"], r["area"]) == (f, s, ar)))
    print("ruler", f, row)
big = [r for r in ru if (r["share"], r["area"]) == (0.4, 0.25)]
print("40/25 found", sum(r["found"] for r in big), "of", len(big))
others = {}
for s in (0.05, 0.15, 0.40):
    for ar in (0.05, 0.25):
        if (s, ar) != (0.4, 0.25):
            others[(s, ar)] = sum(r["found"] for r in ru if (r["share"], r["area"]) == (s, ar))
print("others of 60", others)
fb = [r for r in big if r["found"]]
cl = [r["claims"] for r in fb]
print("claims range", min(cl), max(cl), "zero", sum(c == 0 for c in cl))
ins = sorted((r["claims_true_cells"], r["claims"]) for r in fb if r["claims"] > 0)
print("inside lowest", ins[:3], "n<0.9", sum(i < 0.9 for i, _ in ins))
print("decoy named in ruler runs", sum(bool(r["false"]) for r in ru), "sets", len({(r["field"], r["seed"]) for r in ru if r["false"]}))
print("ruler oni named", sum(r["oni"] for r in ru))
# false definition: c > 1 i.e. decoys other than planted; ONI is 0
# where ONI stood
for f in fields:
    for kind in ("real", "sight"):
        rr = [r for r in k(kind) if r["field"] == f]
        print(kind, f, "top5 broad", sum(0 in r["broad"]["top"] for r in rr), "top5 sharp", sum(0 in r["sharp"]["top"] for r in rr),
              "either", sum(0 in r["broad"]["top"] or 0 in r["sharp"]["top"] for r in rr),
              "sharpest", sum(r["sharp"]["top"][0] == 0 for r in rr), "broad first", sum(r["broad"]["top"][0] == 0 for r in rr),
              "named", sum(0 in r["leads"] for r in rr))
for r in k("where"):
    print(r)
ss = [r for r in k("real") if r["field"] == "south_southeast_asia"]
print("SSEA best decoy sharp r (top non-ONI)", sorted(max(v for c, v in zip(r["sharp"]["top"], r["sharp"]["r"]) if c != 0) for r in ss))
print("SSEA bar", sorted(r["sharp"]["bar"] for r in ss))
