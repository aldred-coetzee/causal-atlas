# Status

Last updated 2026-11-06.

**Phase 1: the plan revision is written and passed next-pattern's plan audit, with its eight text conditions made (`docs/plan-phase-1-revision.md`, the owner's yes in decision 0030). He agreed to R1 and to the fixed formula for the mark (decision 0031). R1 ran and its gate passes, on spent seeds, at 25 trees (`results/r1-twin.md`, Result): no row crashed, R within 0.68 to 1.12 of observed on all 20 planted rows, all eight false-gain shifts under 0.02, three calibrated rows above zero. Two things the gate does not check: the `blown` flag fires on 4 of 20 planted rows because it marks real surges, against 1 in 20 allowed at R3, and on R3's window only 9 of 20 planted rows clear the easiest conditions against 16 needed. **R2 part A stopped at its early stop, on spent seeds (`results/r2-screen.md`, Result): every form named a lead on 9 to 11 of 15 no-link worlds against 2 allowed, and a true column in 4 or 5 of 20 planted worlds against 16 needed. Tier 2 and part B did not run; no fresh seed used. Two causes: the plan's gate is wrong (it scales the unshifted value differently from the shifts; `scripts/r2_gate_null.py` shows 33% to 92% false alarms on pure noise, 2% or less when fixed), and the screen does not hear (a true column in the top 5 in only 8 or 9 of 20). He said go on the last check, raised the cap to 20M, asked not to be asked about spending on subsections, and asked for a proper test framework because he doubts we are testing the right things and fears going in circles (decision 0035). The check is `results/r2-check.md`, `scripts/run_r2_check.py`: gate corrected, same 35 spent worlds, 1,280, 320 and 80 columns. **After it: report, then write the framework proposal for him.** His yes and the new flag: decision 0034. Hearing test still waits. R1 about 200k; next-pattern's shared overhead is beside the count (his word, 2026-11-06 12:11 UTC). Phase 1 about 5.55M of 7M plus next-pattern's share of R2.** About 4.85M of 7M by next-pattern's count at the start of R1, low by roughly 180k for 9 compactions not in any transcript (about 20k each, measured once). Beside the count, not in the cap: at least 3,053,170 Haiku tokens from web reading in the four research runs (decision 0033).**

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
