# The finders and the board counted: told nothing of where, what does the swarm get the referee to hear, and what does it pass falsely?

**Outcome: not yet counted.**

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

Not yet counted.
