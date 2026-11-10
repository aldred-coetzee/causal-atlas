"""Shared loading for this review's scripts. Reads the project's cached real panel (yields.panel) and nothing else from the project except where a script says so."""
import os, sys
os.environ.setdefault("OMP_NUM_THREADS", "3"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "3"); os.environ.setdefault("MKL_NUM_THREADS", "3")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src")); sys.path.insert(0, os.path.join(ROOT, "synth"))
import numpy as np
from causal_atlas import yields

FIRST = 20


def real():
    p = yields.panel()
    country = np.searchsorted(p["codes"], p["code"])
    cereal = np.array([yields.CEREALS.index(i) for i in p["item"]])
    return p, country, cereal


def S(r, col=0, which="model"):
    return float(1 - r[which][:, col].sum() / r["base"].sum())


def boot(num, den, seed, draws=2000):
    picks = np.random.default_rng(seed).integers(len(den), size=(draws, len(den)))
    b = 1 - num[picks].sum(axis=1) / den[picks].sum(axis=1)
    return [float(v) for v in np.percentile(b, [2.5, 97.5])]
