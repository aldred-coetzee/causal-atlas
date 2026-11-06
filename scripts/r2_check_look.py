"""Post hoc look at the saved R2 check tables: spent seeds, after the verdict, no setting comes from it. See results/r2-check.md. Run from the repo root."""
import numpy as np, glob, os
d='data/panel/r2-tables/'
def L(p,s): return np.load(f'{d}{p}_{s}.npy')
pl=[('planted_3.50',s) for s in range(3001,3021)]; nu=[(p,s) for p in ('pure_null','shared_null','combo_null') for s in range(3001,3006)]
F={'all':0,'largest':1,'pooled':2}
for name,i in F.items():
  for size in (1280,320,80):
    out=[]
    for W in (pl,nu):
      raw=0;best=[];rk=[]
      for w in W:
        t=L(*w)[i,:size]
        raw+= t[:,0].max()>t[:,1:].max()
        own=t[:80]
        z=(own-own.mean(1,keepdims=True))/own.std(1,ddof=1,keepdims=True)
        # is the whole of the world's own inputs raised, unshifted vs each shift: the mean of T over the 80 columns
        m=own.mean(0); rk.append((m[0]>m[1:]).sum())
        best.append((own[:,0]/own[:,1:].mean(1)).max())
      out.append((raw,round(float(np.median(best)),2),int(sum(r==32 for r in rk))))
    print(name,size,'raw max beats all shifts: planted',out[0][0],'null',out[1][0],'| median best true/shift-mean ratio planted',out[0][1],'null',out[1][1],'| own-input mean T beats all 32: planted',out[0][2],'null',out[1][2])
