# Status

Last updated 2026-11-05.

**Phase 1, step 1b: first run in progress, second run's rule awaiting next-pattern's check.** Current order is decisions 0016
and 0017 (1b ceiling 1M fresh tokens). `scripts/run_1b_all.py` appends to `results/1b-replicates.jsonl`, uncommitted until it ends, and
resumes if restarted; started 2026-11-05 about 13:30 UTC, 24 hour ceiling.

Next, in order:
1. First run ends: `scripts/close_1b.py`, then fill `## Result` in `results/1b-known-answer.md` as its "How 1b closes" says (name rule
   commit b94c22b; the 16 of 20 mark is reported missed, not rewritten). Commit the jsonl and summary.
2. Second run, only after next-pattern approves the rule (section "Second run", commit 671f8f1): last 240 months, mark panel 3.50,
   seeds 3001 to 3020, 159 training months. `detector.py` and `run_1b.py` need the window parameterised first; nothing is fitted yet.
3. At most five sources (300k), then the multi-input test as a plan revision, checked by next-pattern. It must settle whether
   real scoring uses the 240 month window as its one scoring or keeps 2021-04 on held out.

1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
