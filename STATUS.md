# Status

Last updated 2026-11-05.

**Phase 1: the growing refit passed its development test on spent seeds (`results/refit-dev.md`). Waiting for the owner before sources start.** Nothing is running.

The refit: quiet 8 of 8, hears 2 of 3 (1011 at 0.0215, interval 0.008 to 0.034; 1016 at 0.0226, 0.011 to 0.034; 1017 at 0.011, missing). A thin pass on spent seeds, with no shuffle run, so it does not show the gain comes from the inputs. Not detection and not a mark; seeds 3001 to 3020 are unspent. Nothing here is about real data. A 51-shuffle replicate is about 1.7 hours. The earlier close of 1b: `results/1b-known-answer.md`, last two sections.

**Why it is waiting.** This session's transcripts stand at about 1.97M fresh, Phase 0 included and next-pattern's share not, against the 3M cap, with most of the plan to run. The owner's refined aim (decision 0021) may also change what sources are worth fetching, and his wider reading request is being put to him with this result. Recommendation sent: settle the aim's effect and the budget first, then sources.

**Next steps, in order, once he has answered:**
2. At most five sources, 300k, each named with its mechanism before fetching and entered in `data/manifest.toml` and `docs/data-sources.md`.
3. The plan revision, on the list in `docs/plan-phase-1.md` (Amendments after step 1b), checked by next-pattern before anything runs. The margin is the owner's call.

**The aim was refined by the owner on 2026-11-05 evening, in his words: `docs/decisions/0021-owner-refines-the-aim.md`.** `CLAUDE.md` and `README.md` carry it. It starts no work.

1c and 1d are not run on real data, and the held-out set stays unscored.
Step 1a is done. Sources are in `docs/data-sources.md`, data in the ignored `data/raw/`, checksums in
`data/manifest.toml`. Decision 0013 has his answers after 1a and the plan's amendments section their effect.

**Gates that pass no longer stop** (decision 0014): send the report and carry on. Stop only if it
really needs his guidance. The end of 1d always stops.

He can reverse the PCMCI and CCM deferral at any gate.

**Worth knowing.** GitHub refused deploy keys intermittently on 2026-11-05, on several repos, with the key fine: retry a few times, seconds apart, before treating "Permission denied (publickey)" as a key problem. Git's global email on this box is a personal address. This repo overrides
it locally (decision 0009), and a fresh clone must set it again before committing.

Token figures are reported at each gate, not kept here.
