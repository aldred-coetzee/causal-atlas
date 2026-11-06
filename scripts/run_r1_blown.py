"""R1, post hoc: totals per span for the four rows flagged blown. Nothing changed, spent seeds, not a mark. See results/r1-twin.md."""
import json,sys
import numpy as np
from run_refit_marks import load,synth
from causal_atlas import twin as w
from causal_atlas.refit import spans
seed=int(sys.argv[1])
_,lat,lon=load()
g=synth.generate('planted_3.50',lat,lon,seed); y=g['y']
refs=w.references(y,lat,lon,trees=(25,))
m=w.test_panel(refs,g['drought'],g['oni'])
r=refs['R']
for s,e in spans():
    l=s-3; tr=y[:,l-23:l+1].sum(); o=y[:,s:e+1].sum()
    print(seed,s,'trail',int(tr),'obs',int(o),'R',round(r[25][:,s:e+1].sum()),'M',round(m[25][:,s:e+1].sum()),'limit',int(5*tr),'BLOWN' if w.blown(r[25],y,s,e) or w.blown(m[25],y,s,e) else '',flush=True)
