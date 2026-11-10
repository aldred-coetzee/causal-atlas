"""Item 4 follow-up: this review's own forecast D gave 1.09% with every country given the world mean drought. Is that a year effect or a drift? Shifts and a whole-record line taken out."""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import numpy as np
import own
p, country, cereal = common.real()
x = p["x"]; C, M = x.shape
o = own.Own(p, country, cereal, "mean3")
def flat(v):
    q = v.reshape(len(v), -1, 12); t = np.arange(q.shape[1]) - (q.shape[1] - 1) / 2
    q = q - q.mean(1, keepdims=True); q = q - t[None, :, None] * np.einsum("ctm,t->cm", q, t)[:, None, :] / (t @ t)
    return q.reshape(len(v), -1)
wm = np.repeat(np.nanmean(x, 0, keepdims=True), C, 0)
for name, v in (("world mean", wm), ("world mean, line taken out", flat(wm)), ("own country, line taken out", flat(x))):
    s = own.S(o.run(v), "D")
    sh = np.array([own.S(o.run(np.roll(v, 12 * k, 1)), "D") for k in range(2, 64, 3)])
    print("%-30s own D S %.2f%%; 21 shifts mean %.2f%% max %.2f%% beaten %d/21" % (name, 100 * s, 100 * sh.mean(), 100 * sh.max(), (s > sh).sum()), flush=True)
