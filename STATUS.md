# Status

Last updated 2026-11-06.

**Phase 1: the plan revision is written and passed next-pattern's plan audit, with its eight text conditions made (`docs/plan-phase-1-revision.md`, the owner's yes in decision 0030). Waiting for his go-ahead to R1, in his words. Each step, R1 to R3 and the real-data outline, needs its own. About 4.85M of 7M by next-pattern's count.**

The shift diagnostic read "margin": all six planted rows lose their gain when inputs are shifted, so on those rows the gain came through the inputs (`results/refit-shifts.md`, Result). But shifted inputs still gave large false gains on two overshooting rows (3007 six of 16 shifts at 0.085 or more, 3010 two), so the baseline's blow-ups still need fixing. The revision covers that.

Below, the marks run that led here. It crashed at 01:31 CET and B missed (`results/refit-marks.md`, Result).

- **A passed by count:** real 19, 19, 20 and noise 18, 18, 20 of 20. One null false alarm with noise inputs, pure_null 3007 at 0.1032 (0.0102 to 0.222).
- **B missed:** 10 of 16 finished planted seeds meet criterion 1, at most 14 of 20 even if the four missing all met it, against 16 needed. 3015 crashed in the baseline fit, 3018 to 3020 did not run. **No shuffle ran, so whether the gain vanishes with the inputs broken is unanswered.**
- **The doubt, checked on the rows, post hoc:** skill rewarding a broken baseline holds for three rows (3017 at 143 times observed, 3010, 3014), not generally: 0.57 falls to 0.21 without them, 0.06 on nulls. With the baseline calibrated, all 8 planted rows beat all 49 real-input nulls by size. **Shuffles are still the open question**: nothing shows the gain comes through the inputs.
- **Recommended to him, after the review:** a post hoc shuffle diagnostic on six rows, 3010, 3014, 3007 (baseline overshooting) and 3011, 3002, 3008 (calibrated), 16 circular shifts each, about 3.5 machine hours or fewer, about 60k tokens, launched by next-pattern, labelled not a mark. If the calibrated rows keep their skill under shifts, stop this forecaster. If only the overshooting rows keep it, fix the baseline. If all lose it, the margin was the problem. **He said yes (decision 0029), also to reshaping around discovery. Rule and code: `results/refit-shifts.md`, `scripts/run_refit_shifts.py`. Next-pattern started it as a unit at 2026-11-06 02:05 CET from a16a9a8, ceiling 08:05, and the 04:01 restart leaves it alone. Check with `systemctl is-active causal-atlas-refit-shifts` and `systemctl show causal-atlas-refit-shifts -p Result -p ExecMainStatus`; rows and `results/refit-shifts.log` are untracked until it ends; read with `scripts/run_refit_shifts.py summary`, fill its Result, commit its jsonl, report to him and stop whatever it reads.**
- **If the unit is ever run again:** ask next-pattern; do not start it from a session, since the nightly restart would kill it. Restart skips finished rows.
- **Cap:** raised by the owner on 2026-11-06, "Raise the cap by a few more million", read as 7M (decision 0028; the figure is a working reading, his to change). About 3.64M spent at 01:41 by next-pattern's count: about 2.49M here, about 1.15M there, with about 823k of reading outside it.
- **Independent Fable review, at the owner's request:** done, about 106k, its numbers recomputed here and held.

The refit's development test: quiet 8 of 8, hears 2 of 3 (1011 at 0.0215, interval 0.008 to 0.034; 1016 at 0.0226, 0.011 to 0.034; 1017 at 0.011, missing). A thin pass on spent seeds, with no shuffle run, so it does not show the gain comes from the inputs. Not detection; nothing here is about real data (`results/refit-dev.md`).

**The cap covers both sessions, and the order is decision 0023's.** A step at its line stops and says so; every agent's cost is stated before it spawns, checks included.

**Next steps, in order:**
1. Marks on fresh seeds: ran, crashed, B missed, as above. Stopped for the owner; the steps below wait for his answer.
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
