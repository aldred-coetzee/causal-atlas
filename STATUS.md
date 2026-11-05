# Status

Last updated 2026-11-05.

**Phase 1: the marks for the refit design are written and await next-pattern's check (`results/refit-marks.md`). Nothing is running; seeds 3001 to 3020 are untouched.** After its check: `PYTHONPATH=src uv run python scripts/run_refit_marks.py marks`, detached (`nohup`, log to the scratchpad), about 17 to 30 hours; `summary` reads the outcome at any time, including from a cold session. Do not sit awake watching it.

The refit's development test: quiet 8 of 8, hears 2 of 3 (1011 at 0.0215, interval 0.008 to 0.034; 1016 at 0.0226, 0.011 to 0.034; 1017 at 0.011, missing). A thin pass on spent seeds, with no shuffle run, so it does not show the gain comes from the inputs. Not detection; nothing here is about real data (`results/refit-dev.md`).

**The cap is 4M for both sessions, and the order is decision 0023's.** About 2.44M was spent at 18:22 (1.84M here, 606k next-pattern). `CLAUDE.md`'s caps line still says 3M until the owner says to change it. A step at its line stops and says so; every agent's cost is stated before it spawns, checks included.

**Next steps, in order:**
1. Marks on fresh seeds, as above: estimate 65k, line 80k. If A or B misses, report and stop: whether anything goes ahead is put to the owner.
2. One reading check: does anything similar already exist? One question, one page, 150k all in, cost stated first. The owner's wider reading is not approved.
3. At most five sources, 300k, chosen in the light of decision 0021, each named with its reason before fetching and entered in `data/manifest.toml` and `docs/data-sources.md`.
4. The plan revision, on the list in `docs/plan-phase-1.md` (Amendments after step 1b), checked by next-pattern before anything runs, then the real test, the stop at the end of 1d and next-pattern's result audit. The margin is the owner's call. The revision must set a null with many input columns before anything runs on many real inputs.

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
