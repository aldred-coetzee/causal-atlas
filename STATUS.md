# Status

Last updated 2026-11-05.

**Phase 1: step 1b is closed (decision 0020). Next, from a fresh context: the growing refit on spent seeds.** Nothing is running.

1b's result: the third design is quiet (8 of 8 spent nulls within 0.005) and with a single fit does not reach 0.02 on effects worth 0.10 to 0.14 (0 of 3; skills 0.008 to 0.017). Marks A and B did not run; seeds 3001 to 3020 are unspent. Nothing here is about real data. Full account: `results/1b-known-answer.md`, last two sections.

**Next steps, in order:**
1. Refit that grows as scored months pass, in the model of `scripts/run_1b_third.py` and `src/causal_atlas/nested.py`, with spent seeds and the same development test: all 8 nulls (pure_null 2001 to 2003, 9001 to 9005) within 0.005, and at least 2 of planted_3.00 seeds 1011, 1016, 1017 at skill 0.02 or more with lower bound above 0. Write the rule into the results file first, and check it with next-pattern before it runs. Estimate 60k fresh, line 75k, under the Phase 1 cap. State the cost per shuffle replicate under refits, so we know before any marks whether the full test is affordable on this box. Keep to what the development test needs. If it misses, report it: whether sources go ahead is then put to the owner.
2. At most five sources, 300k, each named with its mechanism before fetching and entered in `data/manifest.toml` and `docs/data-sources.md`.
3. The plan revision, on the list in `docs/plan-phase-1.md` (Amendments after step 1b), checked by next-pattern before anything runs. The margin is the owner's call.

**The aim was refined by the owner on 2026-11-05 evening, in his words: `docs/decisions/0021-owner-refines-the-aim.md`.** It supersedes the working statement in `CLAUDE.md`, which awaits his direct word to change. It starts no work.

1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** GitHub refused deploy keys intermittently on 2026-11-05, on several repos, with the key fine: retry a few times, seconds apart, before treating "Permission denied (publickey)" as a key problem. Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
