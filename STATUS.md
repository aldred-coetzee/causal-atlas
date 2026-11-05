# Status

Last updated 2026-11-05.

**Phase 1, step 1b: stopped on a committed stop, talking to next-pattern.** Current order is decisions 0016, 0017, 0018 (1b ceiling 1M fresh tokens).
The first run ended at ratio 3.00's 20 replicates. It detected 1 or 2 of the 8 replicates worth at least 0.05, and in some replicates shuffled inputs alone
beat the baseline by 0.10 to 0.14, cause unknown (`results/1b-known-answer.md`, Result). The null check came in at -0.0134, below its -0.01 line,
so the settings re-fix in that file is next by rule, once this is talked through.

Then: second run, `nice -n 19` with `OMP_NUM_THREADS=6`, `scripts/run_1b_second.py all`, `results/1b-second-replicates.jsonl` (no closing script yet). Then at most
five sources (300k) and the multi-input test as a plan revision, checked by next-pattern, settling whether real scoring uses the 240 month window as
its one scoring or keeps 2021-04 on held out.

1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
