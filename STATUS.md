# Status

Last updated 2026-11-05.

**Phase 1, step 1b: the full run is in progress, and its pass mark is in question.** Current order is decision 0016.
`scripts/run_1b_all.py` appends to `results/1b-replicates.jsonl` and resumes if restarted; it was started 2026-11-05 about
13:30 UTC with a 24 hour ceiling. The 16 of 20 mark cannot be met in the scored window (see `results/1b-known-answer.md`), and
next-pattern has been asked about restating it. Then at most five sources (300k), then a pre-registered multi-input test as a plan
revision. 1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
