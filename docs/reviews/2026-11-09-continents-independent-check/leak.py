import json, numpy as np
from causal_atlas import field, links, forecast
import os; D = os.path.dirname(os.path.abspath(__file__)) + "/"  # was the reader's scratch folder
a,b=json.load(open(D+"clean.json")),json.load(open(D+"noise.json"))
for r,s in zip(a,b):
    print("mine", r["field"], r["fold_error"]==s["fold_error"], r["coef"]==s["coef"], r["k"]==s["k"], r["slope_sum"]==s["slope_sum"], r["lag_hist"]==s["lag_hist"])
# their forecast.fit, regions
for name in ["south_america","australia","south_southeast_asia","north_america"]:
    yc,lat,lon=field.box(name); yc=np.clip(yc,-3,3); x=field.oni()
    T=links.tiles(lat,lon)
    out=[]
    for noisy in (False,True):
        y2,x2=yc.copy(),x.copy()
        if noisy:
            g=np.random.default_rng(7); y2[:,600:]=g.normal(0,1,y2[:,600:].shape); x2[600:]=g.normal(0,1,x2[600:].shape)
        y=T@y2; near=np.repeat(y.mean(0,keepdims=True),len(y),0)
        m=forecast.fit(y,near,x2,600); out.append(m)
    p,q=out
    print("theirs",name,p["baseline"]==q["baseline"],p["fold_error"]==q["fold_error"],p["k"]==q["k"],np.array_equal(p["lag"],q["lag"]),np.array_equal(p["claimed"],q["claimed"]),np.array_equal(p["slope"],q["slope"]),np.array_equal(p["e"][:,:600],q["e"][:,:600]))
