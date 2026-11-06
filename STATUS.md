# Status

Last updated 2026-11-05.

**Phase 1: the marks on fresh seeds are running (`results/refit-marks.md`), started 2026-11-05 19:18 by next-pattern from 92065c3 after its check, no edits. About 17 to 30 hours, ceiling 36. Do nothing in this repo's results until it ends, and do not sit awake watching it.**

- **Is it running:** `systemctl is-active causal-atlas-refit-marks`. Clean end: "inactive"; crash: "failed". It is its own system unit, not inside this session, because the nightly restart would kill a job started here.
- **Outcome at any time:** `PYTHONPATH=src uv run python scripts/run_refit_marks.py summary`. Rows `results/refit-marks.jsonl`, log `results/refit-marks.log`; both untracked until it ends. The last log line says FINISHED or A MISSED.
- **If it stops early:** ask next-pattern; do not start it from a session. Restart skips what is done, but a replicate killed between its real and noise rows would be skipped and leave A incomplete, so check first for a null seed with one row.
- **When it ends:** fill the Result section of `results/refit-marks.md` (A by panel and input; B by scheme; shuffled medians on the three planted seeds; the caveats in its limits), commit the jsonl, send the gate report to the owner and next-pattern. A miss stops: whether anything goes ahead is put to the owner. A pass carries on to step 2. Tokens for this step: 52.9k of its 80k line were spent before launch, so read with DuckDB or `summary`, not the whole file, and stop at the line.
- **Must go in the write-up, seen 2026-11-06 01:24 with the run still going, no setting changed:** pure_null 3007 with noise inputs scored 0.1032 (0.0102 to 0.222), meeting criterion 1 with nothing planted, nearly all from one span (0.3661). Mark A allows it as one miss, and noise rows get no shuffles under the rule. Planted skill also swings by span and window (3014: 0.29 on the full window, 0.03 on the second). The question for the revision: does one burst dominate pooled deviance, so that 0.02 is not a fixed effect size?

The refit's development test: quiet 8 of 8, hears 2 of 3 (1011 at 0.0215, interval 0.008 to 0.034; 1016 at 0.0226, 0.011 to 0.034; 1017 at 0.011, missing). A thin pass on spent seeds, with no shuffle run, so it does not show the gain comes from the inputs. Not detection; nothing here is about real data (`results/refit-dev.md`).

**The cap is 4M for both sessions, and the order is decision 0023's.** About 2.44M was spent at 18:22 (1.84M here, 606k next-pattern). A step at its line stops and says so; every agent's cost is stated before it spawns, checks included.

**Next steps, in order:**
1. Marks on fresh seeds, running, as above.
2. One reading check, done: `docs/reading/anything-similar.md`. Not found as a single system in a bounded search. About 115k fresh against the stated 135k and the 150k line. The owner's wider reading is not approved.
   Also done, outside this order and outside the Phase 1 cap (decision 0024): `docs/reading/maths-for-combinations.md` and `docs/reading/other-fields.md`, 404k. Both rank a search-wide gate first (is the best of many tries luck?), the search-wide false discovery gap next-pattern's plan check already listed. Input to the revision, not acted on; what else is tested on synthetic worlds is the owner's call, with next-pattern putting it to him.
   Also `docs/reading/further-maths.md`, 152k, same terms (decision 0025): ranks random matrix theory, transfer entropy and persistent homology as fake-world tests, nothing run yet. Reading is at about 556k of its 600k before that page's spot-check. With the fourth page below, about 687k before its helpers, past the 600k last recorded here; next-pattern holds that budget.
   For the revision (decision 0026): target-free methods may be candidates. Their reports count only after planted structure, quiet nulls and the search-wide gate, and are leads, not findings, until they beat the baseline out of time. Fourth reading page: `docs/reading/multi-block-integration.md`, 131k: two-step angles first, no test found on data like ours and no evidence opened that shared dimensions predict out of time. Next-pattern recommended to the owner no more pages until one candidate has been tried on fake worlds.
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
