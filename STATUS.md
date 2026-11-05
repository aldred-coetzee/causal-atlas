# Status

Last updated 2026-11-05.

**Phase 1, step 1a: done, at its gate** (`results/1a-data-check.md`). Data is in the ignored
`data/raw/`, with checksums in `data/manifest.toml`. Rerun with `scripts/fetch_*.py`, from `scripts/`.
No food price data is held, and there is no fetch script for it (HDX's `robots.txt` disallows it).

**Waiting for the owner, two answers:** which events count as precise enough (level 1-2 at 75.3%,
or 1-3 at 85.6%), and what to do about food prices. Then his yes to 1b. Do not begin 1b without that.
The plan is not yet changed for findings 3 and 4 (the split's end, and ONI at t-1); record these with
his answers in one new decision, and amend the plan.

Later he can refuse the 1b generator subagent at the 1b gate, and reverse the PCMCI and CCM deferral
at any gate.

**Worth knowing.** Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
