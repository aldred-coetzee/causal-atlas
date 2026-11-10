import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time, common, numpy as np
from causal_atlas import harvest
p, country, cereal = common.real()
t=time.time()
r = harvest.run(p["logy"], p["official"], country, cereal, p["x"], p["lat"], p["lon"], common.FIRST, 6, shifts=[])
from common import S
print("secs", round(time.time()-t,1), "S", S(r), "flat", S(r,0,"flat"), "scored", r["scored"])
