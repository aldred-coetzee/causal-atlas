# Status

Last updated 2026-11-05.

**Phase 1, step 1b: stopped for a ruling.** Current order is decisions 0016 to 0019 (1b ceiling 1M of this session's own fresh tokens, nearly spent).
The third design was built and tried on spent seeds. It is quiet (8 of 8 nulls within 0.005) but missed its test to proceed: 0 of 3 test seeds reached 0.02, with skills .0088, .0165, .0078. So marks A and B did not run and seeds 3001 to 3020 are unspent. Full account: `results/1b-known-answer.md`, last section. Waiting on the owner through next-pattern: how to close 1b. `scripts/run_1b_third.py marks` is the ready command if the marks ever run; `scripts/run_1b_second.py` is unused.

Then: at most five sources (300k) and the multi-input test as a plan revision, checked by next-pattern, settling whether real scoring uses the 240 month window as its one scoring or keeps 2021-04 on held out.

1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
