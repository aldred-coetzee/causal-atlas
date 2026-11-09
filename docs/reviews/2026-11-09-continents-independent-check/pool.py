import json, numpy as np
import os; D = os.path.dirname(os.path.abspath(__file__)) + "/"  # was the reader's scratch folder
res=json.load(open(D+"clean.json"))
ent=[r for r in res if r["field"]!="europe"]
for r in res: print(r["field"], r["fold_error"])
b=sum(np.array(r["base"]) for r in ent); m=sum(np.array(r["model"]) for r in ent); sh=sum(np.array(r["shifted"]) for r in ent)
S=1-m.sum()/b.sum(); shs=1-sh.sum(1)/b.sum()
print("pooled S",S,"shifted",shs.min(),shs.max(),"beats",(S>shs).sum())
al={k:sum(r["alone"][k] for r in ent) for k in ("zero","level","linear")}; print("model",m.sum(),al)
def boot(seed):
    d=np.random.default_rng(seed).integers(25,size=(2000,25)); bs=1-m[d].sum(1)/b[d].sum(1); return np.percentile(bs,[2.5,97.5])
print("ci seed0",boot(0),"other seeds",[boot(s).round(3).tolist() for s in (1,2,3)])
for r in ent:
    bb,mm,ss=np.array(r["base"]),np.array(r["model"]),np.array(r["shifted"])
    d=np.random.default_rng(0).integers(25,size=(2000,25)); bs=1-mm[d].sum(1)/bb[d].sum(1)
    s2=1-ss.sum(1)/bb.sum()
    print(r["field"], round(1-mm.sum()/bb.sum(),4), np.percentile(bs,[2.5,97.5]).round(4), s2.min().round(4), s2.max().round(4))
# new analysis: leave-one-ENSO-event-year-out, block-of-years bootstrap
yrs=np.arange(2000,2025)
for drop in ([2015,2016],[2010,2011],[2015,2016,2010,2011,2023,2024]):
    keep=~np.isin(yrs,drop); print("drop",drop, round(1-m[keep].sum()/b[keep].sum(),3))
rng=np.random.default_rng(5); out=[]
for _ in range(2000):
    st=rng.integers(0,23,size=9); idx=np.concatenate([np.arange(s,s+3) for s in st])[:25]; out.append(1-m[idx].sum()/b[idx].sum())
print("3-year block bootstrap",np.percentile(out,[2.5,97.5]).round(3))
