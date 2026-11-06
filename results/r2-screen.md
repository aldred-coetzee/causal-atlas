# R2: the screen, its gate, the decoys, and the mark

Rule first, committed before any number (rule 9). The design is `docs/plan-phase-1-revision.md`, sections 3 to 7, with the corrections in decision 0034. Code: `src/causal_atlas/screen.py`, `scripts/run_r2.py`. Trees 25, frozen by R1.

## Questions

1. Without being told which input matters, does the quick screen name a truly linked input among 1,280 columns, and stay quiet when nothing is linked?
2. Do the leads it names carry skill to the later window, beyond the place's own history?
3. If so, how big must S be before a fake world with no link would not reach it? That is the mark m.

## Part A: spent seeds, first

Worlds: `planted_3.50`, seeds 3001 to 3020; `pure_null`, `shared_null`, `combo_null`, seeds 3001 to 3005 each. 35 worlds. All these seeds have been seen in R1, so nothing here is a clean estimate. It is a check of whether going on is worth it.

Each world has its own 2 input series and 30 decoys, the inputs of 15 worlds drawn without replacement from seeds 6001 to 6060, chosen by the world's seed. A column named from the world's own 2 series counts as true on a planted world. Decoys are noise, so sharing them between worlds is allowed.

Screen on months 195 to 290, 40 columns per series, and the gate as section 4 states: 32 shifts, step down, K = 5, p = 1/33 per lead.

**Choosing the form.** Among `all`, `largest` and `pooled`, drop any that names a lead in more than 2 of the 15 null worlds. Of the rest take the one naming a true column in most planted worlds; ties go to fewer named on nulls, then to that order. If all are dropped, stop. The other forms' counts are reported beside it.

**Tier 2.** With the chosen form, each world's leads go into M, on spans 291 to 386: the top 5 forced on every world, and the gated leads where the gate named any. R is the twin without them.

**The early stop.** An addition to the plan at the owner's request (decision 0034). It can only stop work. Go on to part B only if all three hold:

| Check | Bar | Source |
|---|---|---|
| Screen hears | a true column among the leads in at least 16 of 20 planted worlds | R3's mark |
| Screen is quiet | a lead named in at most 2 of 15 null worlds | R3's mark, scaled down, stricter |
| Pipeline hears | a true column among the leads, with S ≥ 0.005 and lower end > 0, raw > 0, S positive in at least 3 of 4 spans, in at least 16 of 20 planted worlds | R3's mark, at the lowest m can be, shift conditions unapplied |

Going on therefore means only "not ruled out". Shifts and a higher m can only remove rows. A failed check stops and is reported, with no setting changed. Forced runs on planted and null worlds and any blown spans are reported beside the checks.

**What R1 says in advance.** R1 gave M all 8 input columns on this window at 25 trees, and 9 of 20 planted worlds met these conditions apart from the spans. So this stop may well fire unless the screen's leads do better than those columns.

## Part B: the mark, only if part A goes on

`pure_null`, `shared_null`, `combo_null`, seeds 5001 to 5020, 60 worlds, the chosen form, top 5 forced through tier 2. Everything else is frozen by then.

m = the larger of 0.005 and the second-largest S. **Stop here for the owner to confirm m or set it higher**; a lower m needs a new decision. Reported beside it: the largest S, how many of the 60 would reach the old 0.02, and how many worlds the gate named a lead in. No mark seed (5101 onward) is touched in R2.

## What is held back

The hearing test (planted 1.15, 1.4, 2.4) is not part of R2 and is not built without the owner's yes. Nothing here touches real data or the held-out months 387 to 434.

## Limits, fixed before the run

Estimate 175k fresh tokens, stop at 220k. Machine time 8 hours, ceiling 10 hours; a projection past the ceiling stops and is reported. Two processes of 3 threads, nice 19. Timed once on spent seed 9001, `pure_null`, which is in neither part, on an idle box: 379 seconds for one whole world, 232 of them the screen. Only the times were read, and that no form named a lead. That projects to about 2.2 hours for part A, which screens each world and then fits it again for tier 2, and about 3.2 hours for part B.

## Result

Not yet run.
