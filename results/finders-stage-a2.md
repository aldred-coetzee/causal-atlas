# The finders and the board counted: told nothing of where, what does the swarm get the referee to hear, and what does it pass falsely?

**Outcome (2026-11-11, counted once): every mark holds at every size of table. Where nothing predicts, 2 of 450 worlds had any pass (0.1% to 1.6%), none at 120 or 240 places. Told nothing of where, the board gets the referee to hear nearly every planted link of seven kinds at 240 places and more (52 to 60 of 60), and a third to all of them at 120. Mark 4 is not tested: the swarm rarely sends a shared path that passes. The condition for the first read across the real table is met.**

Rule first, committed before any counted seed (rule 9). Stage A2 of `docs/plan-finders-and-referee.md`. Authority: decisions 0040, 0055 to 0057, 0059 to 0062. Code: `src/causal_atlas/finders.py` (the swarm and the steward), `src/causal_atlas/referee.py` (unchanged since the label's count), `scripts/run_finders.py` (which uses `scripts/run_referee.py` and `scripts/run_referee_b.py`), `synth/table_panel.py`, `synth/shared_paths.py`; tests in `tests/test_finders.py`. Seeds: `results/seed-ledger.md`. Rows: `results/finders-stage-a2.jsonl`, one a world.

Made-up tables only. No real series is read.

## Why

The referee alone, told nothing of where a link is, heard 4 of 1,620 links (`results/finders-stage-a1.md`); told where, it hears most kinds. So what stands between the referee and a real table is a finder of where and of what, working on the early years only. Decision 0062 is that finder: sixteen small plain-code members in five families posting to one board, and a steward that sends at most forty rows, and only rows whose lift is at least three. Fewer rows sent lower the referee's bar, so the same count must say what is heard and what is passed falsely.

Four questions, each with a mark:

1. Where nothing predicts, how often does anything pass?
2. Where links or shared paths are planted, how often does a pass name nothing that was planted?
3. How many planted links are heard from the board alone, with no answer handed over?
4. When the swarm itself proposes a shared slow path and it passes, does the pass carry the label?

## What has been looked at

The finders, the steward and the harness were shaped on smoke worlds, seeds 47001 to 47999 as listed in the ledger, never counted; decision 0062 has what they gave. The outputs of the last smoke runs at 480 places (four kinds of link, and the seven path shapes) were lost unread when the scratch directory was cleared overnight, so at 480 places the swarm has been seen on three kinds of link only (steady, two together, sign by place), six links each. The worlds of the three earlier counts are spent and are not read here. No world with a seed from 48001 on has been made.

The path shapes and the nothing-predicts variants are those of the earlier counts; all have been seen by this session.

## The worlds

`synth/table_panel.py` as before: forty series by 60 years, places in groups of five; the finders see years 0 to 34, the referee scores years 35 to 59. Three sizes, numbered j = 0, 1, 2: **120 places** with links at 35%; **240 places** with links at 35% (near the real yearly table's 218); **480 places** with links at 20%.

**Where nothing predicts a year ahead:** six variants numbered i = 0 to 5 in the order none, none_strong, none_plain, none_rough, none_gaps, same_year, made as the second count made them.

| Panel | Worlds at 120, 240, 480 places | Seeds |
|---|---|---|
| `<variant>_<places>` | 30, 30, 15 | from 48001 + 1000j + 100i |

**A shared slow path added to a no-link world** by `shared_paths.add`: seven kinds numbered i = 0 to 6 in the order waves, cycle, boom, wander, regimes, quasi_cycle, mixed.

| Panel | Worlds at 120, 240, 480 places | Seeds |
|---|---|---|
| `path_<kind>_<places>` | 15, 15, 8 | from 51001 + 1000j + 100i |

**Where a link is planted,** three links a world, nine kinds numbered i = 0 to 8 in the order steady, threshold, extremes, pair, flip, flip_state, many, hidden, shared.

| Panel | Worlds at 120, 240, 480 places | Seeds |
|---|---|---|
| `<kind>_<places>` | 20, 20, 10 | from 54001 + 1000j + 100i |

1,166 worlds: 450 where nothing predicts, 266 with a shared path, 450 with links (1,350 links). Each is read once; the script will not read a (panel, seed) a second time.

## What is sent

Whatever the steward sends from the swarm's board: at most forty rows, each with a lift of at least three, under one bar. Nothing that knows the truth is among them. Every pass carries the referee's label. Each world is also read twice more, beside the count and under bars of their own: the first round's rows alone (where they differ), and the planted answers put in front of the board's rows. Neither of those readings enters a mark.

The harness, which alone knows what was planted, says afterwards how each sent row stands (decision 0062, point 8): *full*, *part*, *copy*, *path* or *other*. A link is **heard** when a row that names it in full passes. A pass of *other* **names nothing planted**. A pass of a near copy of a planted input predicts and is counted beside, not as false; so is a pass of a part.

## Marks

Counted at each size of table apart. A limit in worlds is the count a true rate of 1 world in 20 would exceed less than 3 times in 100 (`at_most`).

1. **Where nothing predicts, little passes.** Worlds with any pass: **at most 15 of 180** at 120 places, **15 of 180** at 240, **9 of 90** at 480.
2. **Where something is planted, a pass names it.** Of the linked and path worlds together, those with a pass that names nothing planted: **at most 22 of 285** at 120 places, **22 of 285** at 240, **13 of 146** at 480.
3. **Links are heard from the board alone.** Of each kind's links (60, 60 and 30), heard: steady **at least 45, 45 and 25**; threshold, extremes, two together, sign by place, many weak and hidden mover **at least 20, 30 and 15 each**. No mark for a sign that turns on a state or for a link from a series common to all places: both are reported.
4. **A shared path the swarm proposes is not left looking like a lead.** Of the path worlds, those in which a pass of a path's pair carries no label: **at most 10 of 105** at 120 places, **10 of 105** at 240, **6 of 56** at 480.

**If mark 1 or 2 fails at a size,** the floor that lowers the bar lets chance through at that size. The swarm is then not carried to a real table of that size with these settings: the floor or the number sent is changed on smoke seeds and the whole count is run again on fresh ones.

**If mark 3 fails for a kind at a size,** that kind is published as not found by this swarm at that size and share; the answer's own count beside it says whether the finder or the referee is the limit. It does not stop Stage B: it is the ruler Stage B is read with.

**If mark 4 fails at a size,** an unlabelled pass at that size is not to be called a lead, as the label's own count said for its mark; Stage B's baseline must carry the weight.

**If marks 1, 2 and 4 hold at 240 places,** the swarm, the steward and the referee go to Stage B with these settings, unchanged, and Stage B's own rule is written next.

## Expected, said beforehand

- Marks 1 and 2 are expected to hold at 120 and 240 places: no smoke world of 204 where nothing predicts had a pass, and no pass in a linked smoke world named nothing planted. At 480 places they are not known.
- Mark 3 at 240 places is expected to hold for every marked kind (smoke: 9 to 12 of 12). At 120 places it is near the line for threshold, extremes, many weak and hidden mover (smoke: 7 or 8 of 12, the mark is a third). At 480 places it is not known for threshold, extremes, many weak and hidden mover.
- Mark 4 is expected to hold: on smoke worlds the swarm rarely sends a path's pair at all (2 of 84 worlds had a path pass, both labelled).
- A sign that turns on a state is expected to be nearly unheard (smoke: 2 of 24), and its own answer barely passes.

## Measured beside, no mark

For each kind and size: links whose answer passes when put beside the board's rows; heard in the first round alone, which is what the board adds; heard by family, and the plan's rule for keeping a family (best or second best for some kind at some size); passes of a near copy and of a part; passes of a planted link that carry the label; rows posted and sent; the bar; seconds a world.

## Limits, known before the count

- One family of made-up worlds, the one the referee, the label and now the finders were shaped on. A real table differs in ways no count here measures.
- Links act one year ahead, in a quarter of the places, three a world, at 35% or 20% of what the outcome's own history leaves. Real links measured in this project so far are a few per cent. Nothing here says the swarm hears those.
- No member proposes a lag beyond two years or a link within the year.
- Boosted trees and the cross-spectrum of the plan's first set are not among the members (decision 0062, point 7).
- The steward's floor and shares were chosen on smoke worlds of the same family.

## Changed after the independent reading, before any counted seed

An independent reader went through this registration, decision 0062 and the code before the count (`docs/reviews/2026-11-11-finders-rule-check/`: brief, report, its scripts and outputs). It found no way for the scored years or the planted truth to reach a sent row, and that each mark's wording, denominator and limit match what the script computes. Three things it said must change before the count are changed here. No mark's limit, no setting of the swarm, the steward or the referee, and no seed is changed; no counted world had been made.

- **The bar is lower than decision 0062 says.** Its point 6 gives "about 2.3 to 2.7" with the floor. On the reader's 40 worlds where nothing predicts at 120 places (smoke seeds), rows sent were 0 to 11, the bar's middle was about 1.8 (0.83 to 2.82), and 15 of 40 bars were under 1.645; this session ran three of those worlds again and got the same bars. So with few rows sent the bar can sit below the check's 2, and what keeps chance out is then mostly the rules beside the bar: the check on the recent years, the rule of at least ten scored years in five groups, and the read without the best year. None of those 40 worlds had a pass; one chance row stood at t 4.69 on both reads and failed only because it applied in two scored years. A minimum on the bar was considered and not added: the count measures the pipeline as it was registered, and marks 1 and 2 say whether those rules are enough.
- **Rows chosen on the early years stand a little higher on the scored years than chance**, which the bar's draws do not model: a mean scored t of 0.18 against about 0.01 where nothing predicts, and 0.79 against 0.24 with a shared slow path of the kind with regimes at 240 places, where the floor raised worlds with a path's pass from 1 to 2 of 10 (both labelled). The count now reports this beside the marks.
- **Mark 4 is read only where it is tested.** A path's pair rarely passes at all (2 of 84 smoke worlds, 2 of the reader's 10), so "at most 10 of 105 unlabelled" could hold with the label never tried. The table now gives, at each size, the number of path worlds in which a path's pair passed at all. Where that is under 11, mark 4 is written as **not tested** at that size: it says the swarm rarely sends a path that passes, and nothing about the label, whose own record is the label's count (`results/finders-stage-a1c.md`). The condition for Stage B is then marks 1 and 2 at 240 places, with mark 4 either holding on at least 11 such worlds or not tested; either way Stage B's own baseline must carry the table's shared movements.
- **A pass of a part or of a near copy is looked at, not waved through.** A wide row (a main component names every series that differs by place; a gathered row names 5 to 20; a pair names two) is a "part" whenever one planted series is among those it names, so it can never count against mark 2. The table now gives part passes by family with the share of the row's weight that sits on the planted link's series, and near-copy passes in the worlds with a link from a common series apart from the rest (in 4 of the reader's 20 such worlds an unrelated common series went with the planted one at 0.5 or more by chance). A part pass with little weight on the link is to be read as a pass naming nothing planted when the result is written, and said so beside mark 2.
- **Also reported now, no mark:** the bar's middle, least and most at each size and the worlds with a bar under 2; rows that stood above the bar on both reads and did not pass, and which rule stopped them; sent rows' scored t by band of lift; and, for heard rows, the share of their places where the link acts.
- **Mark 1's limit is lenient**, as the reader notes: 15 of 180 would hold about half the time at a true rate near 8 in 100. The count and its interval are what is reported, not only "holds".

## Result

Counted once, 2026-11-11, 16:06 to 18:24 UTC: 1,166 worlds, each (panel, seed) read once, six processes; rows in `results/finders-stage-a2.jsonl`; `scripts/run_finders.py table` prints every table below and the ones left out here. **Every mark holds at every size. Mark 4 is not tested at any size.** The condition for Stage B is met.

**Mark 1, where nothing predicts: holds.** Worlds with any pass: 0 of 180 at 120 places (0.0% to 2.0%), 0 of 180 at 240 (0.0% to 2.0%), 2 of 90 at 480 (0.3% to 7.8%); limits 15, 15 and 9. Together 2 of 450 (0.1% to 1.6%). Both passes at 480 places are single rows of the extremes family (a low tail in the series to a low event in the outcome, lifts 3.45 and 3.15), in the worlds with gaps and with a same-year tie.

**Mark 2, a pass names what was planted: holds, and holds on the strictest reading.** Linked and path worlds with a pass naming nothing planted: 1 of 285 (0.0% to 1.9%), 2 of 285 (0.1% to 2.5%), 1 of 146 (0.0% to 3.8%); limits 22, 22 and 13. Three of those four passes are again tail-to-event rows; the fourth is a main component in a path world with regimes. As the reading asked, passes of a part are looked at: counting as false every world with a part pass that has under a third of its weight on the planted series gives 2, 7 and 3 worlds (1.0% to 5.0% at 240 places); counting every one with under a half gives 14, 15 and 11 (3.0% to 8.5% at 240; 3.8% to 13.1% at 480), still inside each limit. Those part passes are nearly all gathered rows in steady-link worlds: five series, one of them the planted input, which carries the row (weight 0.2). So a gathered row that passes says "something among these predicts", not that each of them does. A pair that passes with one planted series (weight 0.5) is the same case.

**Mark 3, links heard from the board alone, told nothing of where: holds for every marked kind at every size.**

| Kind | 120 places, of 60 | 240 places, of 60 | 480 places (share 20%), of 30 | The answer, told where: 120, 240, 480 |
|---|---|---|---|---|
| steady | 60 (45) | 60 (45) | 30 (25) | 60, 60, 30 |
| threshold | 23 (20) | 58 (30) | 28 (15) | 46, 60, 30 |
| extremes | 30 (20) | 58 (30) | 29 (15) | 36, 60, 30 |
| two together | 27 (20) | 54 (30) | 28 (15) | 42, 58, 30 |
| sign by place | 39 (20) | 60 (30) | 30 (15) | 60, 60, 30 |
| many weak | 22 (20) | 52 (30) | 29 (15) | 46, 60, 30 |
| hidden mover | 46 (20) | 59 (30) | 30 (15) | 60, 60, 30 |
| sign that turns on a state, no mark | 5 | 23 | 9 | 3, 11, 6 |
| from a series common to all places, no mark | 21 | 33 | 9 | 45, 46, 23 |

The mark is in brackets. At 240 places and more the board hears nearly everything the referee hears when told where; at 120 places it hears a third to two thirds of threshold, extremes, pairs, sign-by-place and many-weak links, and there the finder, not the referee, is the limit (the answer passes far more often). In Stage A1 the referee told nothing of where heard 4 of 1,620. A sign that turns on a state is heard a little (more often by the board than by its own answer), and a link from a series common to all places in a third to a half of cases, with the referee able to hear three quarters: the finder is the limit there too. Threshold at 120 places (23 against 20) and many weak (22 against 20) are near the line, as said beforehand.

**Mark 4: within its limit, and not tested.** Path worlds with a path's pass left unlabelled: 2 of 105, 2 of 105 and 0 of 56 (limits 10, 10, 6). A path's pair passed at all in 2, 7 and 3 worlds, under 11 at each size, so by the rule written before the count this says the swarm rarely sends a shared path that passes, and nothing about the label. Of 12 path passes, 8 carried the label; the 4 that did not are 2 at 120 places (boom, wander) and 2 at 240 (regimes). A real table's shared movements must be carried by Stage B's own baseline, as its rule has it.

**Each family earns its place** by the plan's rule (best or second best for some kind at some size): slope, shape, extremes, pairs and modes are all kept. Pairs alone hears two together, shape alone the sign by place, modes alone many weak series. The second round added nothing over the first: a link was heard in round one alone as often as from the whole board, or once or twice more (fewer rows sent, a lower bar). So the board's second round is not what gets links heard here, which the plan said would be the finding if so. It matters at Stage B: the member that tries every pair is in round one and cannot run at the real table's width, so two together must be heard there through the second round's pairs, and the rehearsal says whether it is.

**Beside the marks, as the reading asked.**

| Worlds | Bar where rows were sent: middle (least to most) | Worlds with a bar under 2 | Rows above the bar both ways that did not pass | Sent rows' middle scored t, lift 3 to 4 / 4 to 5 / above 5 |
|---|---|---|---|---|
| nothing, 120 | 1.79 (0.28 to 2.77) | 119 of 180 | 4 | -0.03 / -0.09 / 0.19 |
| nothing, 240 | 1.92 (0.50 to 3.01) | 102 of 180 | 5 | -0.04 / -0.11 / -0.08 |
| nothing, 480 | 2.07 (1.33 to 2.86) | 37 of 90 | 5 | 0.10 / 0.26 / -0.15 |
| path, 120 | 1.82 (0.49 to 2.79) | 69 of 105 | 6 | 0.01 / 0.01 / -0.16 |
| path, 240 | 2.01 (1.21 to 2.94) | 50 of 105 | 9 | 0.09 / 0.25 / 0.05 |
| path, 480 | 2.08 (1.55 to 3.03) | 24 of 56 | 12 | 0.04 / 0.08 / -0.61 |
| link, 120 | 2.54 (1.30 to 3.32) | 7 of 180 | 68 | 0.34 / 1.19 / 2.93 |
| link, 240 | 2.68 (1.89 to 3.22) | 3 of 180 | 69 | 0.52 / 1.50 / 3.81 |
| link, 480 | 2.65 (2.20 to 3.16) | 0 of 90 | 38 | 0.49 / 1.21 / 3.75 |

The bar is as low as the reading measured: under 2 in more than half the worlds where nothing predicts at 120 and 240 places. What kept chance out there was the rules beside the bar: 14 rows in 450 such worlds stood above the bar on both reads and were stopped, most by the check on the recent years. Where nothing predicts, a high lift on the early years says nothing about the scored years (middle t near zero in every band); where links are planted it does (near 3 to 4 above a lift of 5). Rows sent: 2 to 5 in the middle where nothing predicts, 6 to 22 with links. Near-copy passes: 25, 32 and 28, none in the worlds with a link from a common series. Of the places a heard row applies to, the middle share where the link acts is 1.00, 0.80 and 0.68: at larger tables the scan takes in places beyond the link's.

**What this says, and does not.** On made-up tables of this one family, the swarm with its steward and the referee pass something false in about 1 world in 200 where nothing predicts (at most 1.6 in 100) and hear links of a fifth to a third of what an outcome's history leaves, of seven kinds, without being told where. It does not say the same of a real table (other gaps, other shared movements, groups of other sizes), nor of links of a few per cent, which is the size of every real link this project has measured. Stage B's placebos and planted links on the real series are what measure those.

**Deviations.** None from the registration. The count was started in the order 240, 480, then 120 places instead of 120, 240, 480; each world is read alone under its own seed, so the order changes nothing counted. Disclosed.
