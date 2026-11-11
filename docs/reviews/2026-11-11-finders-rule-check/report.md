# The finders' rule before its count: an independent reading

*Returned as text by the independent reader on 2026-11-11 and saved here, unedited, by the project session: the reader could not write the file itself. Its scripts and their outputs are beside it. What the project session did about it is in `results/finders-stage-a2.md`, under "Changed after the independent reading".*

**Summary in ten lines**
1. Q1, leaks: **holds.** Members see only years 0 to 34, and the harness hands the referee rows with no truth in them; a test checks this.
2. Q2, bar coverage: **holds as measured at 120 places, not by the bar's own construction.** 0 of 40 worlds where nothing predicts had a pass. But the floor drops the bar to a median of about 1.8 (0.83 to 2.82, 15 of 40 below 1.645), not decision 0062's "2.3 to 2.7".
3. With so few rows sent, chance is kept out by the recent check (t > 2), the rule of at least 10 scored years and the drop-the-best read, not by the bar. On seed 47925 a chance row stood at t 4.69 and failed only on the years rule.
4. Rows chosen on the early years still stand higher on the scored years: mean scored t 0.18 against 0.01 where nothing predicts, and 0.79 against 0.24 with a shared path (path_regimes, 240 places). The floor raised path passes from 1 to 2 of 10 worlds. I did not run worlds where nothing predicts at 240 or 480 places.
5. Q2 change: strike the 0062 bar range. Report beside the count: the bar by size, the rows that stood above the bar and failed only on the check, years or drop-the-best, and mean scored t by lift band.
6. Q3, marks against `table()`: **wording, denominators and limits all match the code.**
7. Mark 4 can barely fail, because path passes are rare (2 of 84 smoke worlds, 2 of my 10). Register its real denominator (path worlds with any path pass) and say "not tested" when that is below about 11. Today it is a condition for going to Stage B.
8. A pass that should count as false can be classed "part". Components rows name all 31 series that differ by place, and gathered rows or pairs containing one planted series are also "part", so they never count against mark 2. Register "part" passes reported by family, with the weight share on planted series.
9. In 4 of 20 "shared" worlds, an unrelated common series went with the planted input at 0.5 or more by chance, so a pass on it is classed "copy". Report copy passes in shared worlds apart. `full` ignores where the row applies: report `inside` beside heard links. Mark 1's limit of 15 of 180 holds about half the time even at a true rate near 8%.
10. Must change before the count: (a) correct the bar range; (b) give mark 4 a stated effective denominator and a "not tested" rule; (c) report part and copy passes by family. Seeds used: 47900 to 47946, 47960 to 47989; 47947 to 47959 and 47990 to 47999 are untouched.

---

Brief: `brief.md` in this folder. The registration I read is `results/finders-stage-a2.md` at 70c426a, with decision 0062, `src/causal_atlas/finders.py`, `scripts/run_finders.py` and `src/causal_atlas/referee.py`. Nothing was counted. No seed from 48001 on was made, and nothing under `data/` was read. The scripts I ran and their outputs are in this folder:

- `carry.py` produced `a`, `b` and `c.jsonl`;
- `linked.py` produced `d.jsonl`;
- `copies.py` and `dig.py` are also here.

## 1. Can the scored years or the planted truth reach a sent row? **Holds.**

- `view` cuts the values to years 0 to 34 before any member sees them.
- Everything a member uses is computed on that cut alone: the comparable forms, the residual (the referee's baselines run with `first - 1`), the twenty other alignments behind the lift (rolls of 3 to 22 within the 25 early residual years), the scan for where, the components and the gathered terms.
- The second round reads only first-round rows and early values.
- Members are given only values, groups and which series are outcomes.
- The harness hands the referee `fd.proposal(r)` for the steward's rows. The truth (`stands`, `ranks`, the answers) is used only to class rows afterwards and in the two side readings, which enter no mark.
- `tests/test_finders.py` replaces the scored years with noise and checks that the board is identical.

I found no path from the scored years or the truth into a sent row.

## 2. Does the bar still cover what is sent? **Holds as measured at 120 places; not by the bar's own construction.**

**The floor pulls the bar well below the figure decision 0062 gives.** I ran 40 worlds where nothing predicts, at 120 places (seeds 47901 to 47940: 20 none_strong and 20 none). With the floor:

- rows sent were 0 to 11, mostly 1 to 5;
- the median bar was about 1.8, with a range of 0.83 to 2.82;
- 15 of the 40 bars were below 1.645.

Decision 0062, point 6, says "about 2.3 to 2.7". With so few rows sent, what keeps chance out is the uncharged recent check (t > 2), the rule of at least 10 scored years, and the drop-the-best read. The bar does little of that work. 0 of 40 worlds passed, so the result holds empirically.

**Two chance rows show how close it came:**

- Seed 47925 (none): a tail row on a common series stood at t 4.69 in both reads, with a check of 4.76. It failed only because it applied in 2 scored years.
- Seed 47924: a row stood above a bar of 1.46 (t 2.06 and 2.31) and failed only on the check (0.58).

**Choosing on the early years carries across year 35:**

- In the null worlds, rows the floor sent stood at a mean scored t of 0.18 (se 0.08), against about 0.01 for rows with a lift of 0 to 1.5. That is modest.
- With a shared slow path it is larger. I ran path_regimes at 240 places (seeds 47980 to 47989), and with the floor 2 of 10 worlds had a path pass (t 4.0 and 8.6). Both carried the label.
- With no floor (forty rows), only 1 of 10 had one. The floor raises path passes.
- Mean scored t of floor-sent rows was 0.79, against 0.24 for all rows sent with no floor.
- By lift band (all rows): 0.11, 0.31, 0.69. With path rows removed: 0.10, 0.22, 0.27.
- The bar's bootstrap does not model this carry-over.

I did not run null worlds at 240 or 480 places.

**What must change in the registration:**

- Strike or correct the bar range taken from 0062, and say that the bar can sit below the check's 2.
- Beside the count, report:
  - the bar by size;
  - the share of failed rows that stood above the bar and failed only on the check, the years rule or the drop-the-best read;
  - the mean scored t of sent rows by lift band, in null and in path worlds.

## 3. Do the marks match `table()`, and can each fail? **Wording and code agree; mark 4 can barely fail, and "part" can hide a false pass.**

**All four marks match their code.** Each mark's denominator matches, and every limit equals `at_most` (180→15, 285→22, 146→13, 105→10, 56→6, 90→9). In the code:

- Mark 1 is `passed > 0`.
- Mark 2 is a pass classed `other`, over link and path worlds.
- Mark 3 counts a link as heard when a row naming it in full passes.
- Mark 4 is any path pass without the label.

**Problems:**

- **Mark 4 is near-vacuous.**
  - It can fail only if more than 10 of 105 path worlds have an unlabelled path pass. But only about 2 in 84 smoke worlds, and 2 of my 10, had any path pass at all, and all of them were labelled.
  - Yet mark 4 holding is a condition for going to Stage B.
  - Register the effective denominator (path worlds with any path pass). Say the mark is uninformative when that number is below about 11, and that "holds" then means "not tested".
- **"Part" absorbs rows that cannot be false by construction:**
  - A components row names all 31 series that differ by place. On any linked outcome it is always `part` (or `full` for many weak).
  - A gathered row of 5, 10 or 20 series is `part` whenever one planted series is among them.
  - A pair with one planted series is `part`.
  - Such passes never count against mark 2.
  - In my linked worlds (seeds 47941 to 47946, steady at 120 places), the part passes looked real: a component passed where the planted input had a near copy. But the class cannot tell.
  - Register that part passes are reported by family, with the weight share on planted series.
- **Chance "copies":**
  - In 4 of 20 generator-only "shared" worlds (seeds 47960 to 47979), an unrelated common series went with the planted common input at 0.5 or more by chance. A pass on it is classed `copy`, not false.
  - Report the copy passes in shared worlds apart from the others.
- **Where a row applies plays no part in `full`.** In smoke, the share of a heard row's places that lay where the link acts (`inside`) ran 0.4 to 1.0. Report `inside` beside heard links.
- **Mark 1's limit is lenient:** 15 of 180 would hold about half the time at a true rate near 8%. This is minor, and says how little "holds" means.
- **Conservative, and no change needed:** drift pairs and path rows that are not exactly the path pair are classed `other`.

## Seeds used

All are within 47900 to 47999:

- 47900 to 47940: null worlds at 120 places;
- 47941 to 47946: steady at 120 places, share 0.35;
- 47960 to 47979: generator only;
- 47980 to 47989: path_regimes at 240 places.

Unused: 47947 to 47959 and 47990 to 47999.
