"""The real driver alone (no burned-area value read): its field-mean departure by year on 2004-2018, and how monotone it is."""
import sys
import numpy as np
sys.path.insert(0, "scripts")
from causal_atlas import fire
import run_local
from run_fire import SCORED, YEARS
for name in fire.FIELDS:
    x, has = run_local.drought(name)
    x = x[has]
    yr = x.reshape(len(x), -1, 12).mean(axis=(0, 2))
    sc, ft = yr[SCORED], yr[YEARS]
    r_sc = np.corrcoef(np.arange(len(sc)), sc)[0, 1]
    r_ft = np.corrcoef(np.arange(len(ft)), ft)[0, 1]
    # share of cells whose own yearly departure correlates with year over 2004-2018
    cy = x.reshape(len(x), -1, 12).mean(axis=2)[:, SCORED]
    c = ((cy - cy.mean(1, keepdims=True)) * (np.arange(15) - 7)).sum(1) / (cy.std(1) * np.arange(15).std() * 15 + 1e-12)
    print(f"{name:12s} fit-mean {ft.mean():+.3f} r(year) fit {r_ft:+.2f} | scored mean {sc.mean():+.3f} r(year) {r_sc:+.2f} | cells |r|>0.5: {np.mean(np.abs(c) > 0.5):.2f}  yearly scored: {np.round(sc, 2).tolist()}")
