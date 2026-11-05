# Status

Last updated 2026-11-05.

**Phase 1, step 1b: in progress. Current order is decision 0016, replacing the sources step of 0015.** Generator
committed; detector written (`src/causal_atlas/detector.py`, `scripts/run_1b.py`); multi-input panel being added
by the generator's author; then the full run at full size, then at most five sources (300k), then a pre-registered
multi-input test as a plan revision. 1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
