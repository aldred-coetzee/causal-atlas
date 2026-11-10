# The label counted: does "may be moving together" mark the shared slow paths, and leave the planted leads alone?

**Outcome (2026-11-10): counted once, both marks hold at every size of table. Worlds in which a shared slow path passed and went unlabelled: 2 of 210 at 120 places (0.1% to 3.4%), 8 of 210 at 240 (1.7% to 7.4%), 3 of 210 at 480 (0.3% to 4.1%); the limit was 17. Worlds in which a planted lead's pass was labelled: 4 of 180 (0.6% to 5.6%), 4 of 180, 7 of 180 (1.6% to 7.8%); the limit was 15. Of 1,686 passes that were only a shared path, 1,669 carry the label; of 2,298 passes of a planted lead, 20 do. So a pass now comes with a label that is right about 99 times in 100 on these worlds, in both directions. Where a lead and a shared path sit in one pair, the lead is heard in about half the worlds and is then mostly labelled: a label does not mean there is no lead. At 240 places, near the real yearly table's size, seven of nine kinds of link at 35% are heard in at least 54 of 60 links. The section "Result" has it with its limits.** Everything above that section stands as it was written before the count.

Rule first, committed before any counted seed (rule 9). Stage A1 of `docs/plan-finders-and-referee.md`, a third count, of the label only. Authority: decisions 0040, 0055 to 0057, 0059, 0060 and 0061. Code: `src/causal_atlas/referee.py`, `scripts/run_referee_c.py` (which uses `scripts/run_referee.py` and `scripts/run_referee_b.py`), `synth/table_panel.py`, `synth/shared_paths.py`; tests in `tests/test_referee.py`. Seeds: `results/seed-ledger.md`. Rows: `results/finders-stage-a1c.jsonl`, one a world.

Made-up tables only. No real series is read.

## Why

The second count (`results/finders-stage-a1b.md`) found that the referee passes a series and an outcome that only move slowly together, and its rule says no real table is read until a pass carries a label that tells the two apart, registered and counted on fresh worlds. Decision 0061 is that label. A pass is labelled "may be moving together" when the same proposal turned round (the outcome a year before, for the series) stands by a lower mark, or when it is at least as strong read in the same year. The label is not charged in the bar and cannot make or unmake a pass, so nothing the first two counts said of passes changes.

Two questions, each with a mark:

1. Of the passes that are only a shared slow path, how many go unlabelled? Those are the ones a reader would take for a lead.
2. Of the passes that are a planted lead, how many are labelled? Those are real leads marked down.

And it is counted at three sizes of table, the middle one (240 places) near the real yearly table's 218, which no count has had.

## What has been looked at

The label was shaped on 257 smoke worlds, seeds 32041 to 32099, 32121 to 32201, 32213 to 32300 and 32521 to 32552 (decision 0061, with what they gave). Those seeds are never counted. The second count's worlds (33001 to 37830) were looked at after their count, which is where the lower mark was first seen; they are spent and are not read here. No world with a seed from 38001 on has been made.

The path shapes are the helper's seven of the second count. They are no longer unseen: this session has now seen passes on all of them, and the label was shaped on five of the seven at 120 and 480 places and on all seven at 240.

## The worlds

`synth/table_panel.py` as before: forty series by 60 years, places in groups of five, finders see years 0 to 34, the referee scores years 35 to 59. Three sizes, numbered j = 0, 1, 2: **120 places** with links at 35%; **240 places** with links at 35%; **480 places** with links at 20%.

**A shared slow path added to a no-link world** by `shared_paths.add`, as in the second count: two pairs, each an outcome and a series of the place's own, on one path in half the groups; nothing leads. Seven kinds numbered i = 0 to 6 in the order waves, cycle, boom, wander, regimes, quasi_cycle, mixed.

| Panel | Worlds | Seeds |
|---|---|---|
| `path_<kind>_<places>` | 30 | 38001 + 1000j + 100i to 38030 + 1000j + 100i |

**Where a link is planted,** three links a world, nine kinds numbered i = 0 to 8 in the order steady, threshold, extremes, pair, flip (sign differing by place), flip_state (sign by a third series' state), many (many weak), hidden (hidden mover), shared (from a series common to all places).

| Panel | Worlds | Seeds |
|---|---|---|
| `<kind>_<places>` | 20 | 41001 + 1000j + 100i to 41020 + 1000j + 100i |

**A lead and a path in one pair.** A linked world, and the first link's own outcome and first series are also given one slow path, in that link's places, by `beside` in the harness (this session's composition, from the helper's path makers). Three kinds numbered i = 0 to 2: steady with a cycle, steady with a wander, hidden mover with a wander.

| Panel | Worlds | Seeds |
|---|---|---|
| `<kind>+<shape>_<places>` | 15 | 44001 + 1000j + 100i to 44015 + 1000j + 100i |

1,305 worlds: 630 with a shared path, 540 with links, 135 with both in one pair. Each is read once; the script will not read a world a second time.

## What is sent

Forty proposals a world, under one bar, as in the second count but with no turned-round proposal sent (the referee now reads that itself, outside the bar):

- **With a shared path:** each of the two pairs on a path sent five ways (all places, by claim, the quarter and the half of the groups where the series went most with the outcome in the early years, and the places the path is truly in). The keen proposer fills the rest.
- **With links, and with a lead and a path:** each answer three ways (the link's own places, all places, by claim). The keen proposer fills the rest.

Every pass carries the referee's label. A keen pass is tagged afterwards as naming a path's pair, the pair with both a lead and a path, a planted input, a near copy of one, or none of these.

## Marks

Counted in worlds, at each size of table apart. Each limit is the count a true rate of 1 world in 20 would exceed less than 3 times in 100.

1. **A shared path is not left looking like a lead.** Of the 210 path worlds at each size, those in which any pass of a path's pair (sent directly in any of its five ways, or by the keen proposer) carries no label: **at most 17**.
2. **A planted lead is not marked down.** Of the 180 linked worlds at each size, those in which any pass of a planted link (its answer in any of its three ways, or a keen proposal that names a planted input) carries the label: **at most 15**.

**If mark 1 fails at a size,** the label misses shared movement at that size and this file says how often and for which shapes. A pass without the label is then not to be called a lead at that size of table; Stage B's rule would have to carry the weight, by putting the table's main shared movements in the baseline, and whether the label is changed again is decided on smoke seeds.

**If mark 2 fails at a size,** the label is too keen there: it would mark down real leads, and this file says for which kinds. The label is then reported as "cannot be told apart at this size" for those kinds, not as "moves together".

**Whatever the marks,** the words stay as the second count left them: a pass means the forecast improves; an unlabelled pass means the series comes first in time, never that it causes.

## Expected, said beforehand

- Mark 2 is expected to hold at every size. On smoke worlds one pass of a lead in 343 was labelled, and none of 95 through the harness.
- Mark 1 is expected to hold at 120 and at 480 places (no smoke world of 81 with a path pass left unlabelled). **At 240 places it is not known:** 2 of 35 smoke worlds had one, both on cycles, and 2 in 35 is about the rate the mark allows.
- Path worlds with any pass at all: few at 120 places, most at 480, as the second count found. Mark 1 counts worlds of all 210, so at 120 places it is held mostly by the referee refusing the path, and the label's own share is in the table beside.

## Measured beside, no mark

- Of path passes, the share labelled, by kind of path and size, and by which reading (turned round, same year).
- Of lead passes, the share labelled by kind of link and size. Passes whose inputs are all one series common to all places cannot be turned round; they are counted apart.
- **A lead and a path in one pair:** how often the link's pass is labelled. Both are true there, so there is no right answer and no mark. It says how often a label sits on a pair that also holds a lead.
- **The ceiling at 240 places:** the answer sent for the link's own places, how many of 60 links a kind pass. The first measure at the size of the real table. (Twenty worlds a kind, so it is rougher than the first two counts' 90 links.)
- Keen passes that name neither a path's pair nor a planted input nor a near copy; the bar; seconds a world.

## Limits, whatever the counts

- One family of worlds, and the referee and its label were shaped on it, three times now.
- Seven shapes of path, all seen before this count. A real table's slow movements are not bound to be like any.
- The made-up links act a year later and not within the year. A real link that acts in both will be labelled by the same-year reading (decision 0061, point 4); nothing here measures how often.
- Every lag here is one year.
- The directly sent pairs and the answers are handed over by a script that knows the layout. They measure the referee and its label, not any finder.
- The label cannot see an unrecorded thing that moves the series first and the outcome later: that is unlabelled, and is a lead in time and not a cause.

## Result (2026-11-10, counted once, 14:17 to 14:37 UTC, on commit 36b7380)

1,305 worlds, each read once, none read twice; no error in any log. Intervals are over worlds (exact binomial, 95%). `scripts/run_referee_c.py table` prints the tables from `results/finders-stage-a1c.jsonl`.

**Both marks hold at every size.**

| Places | Mark 1: path worlds with a pass left unlabelled (limit 17 of 210) | Mark 2: linked worlds with a lead's pass labelled (limit 15 of 180) |
|---|---|---|
| 120 | 2 (0.1% to 3.4%) | 4 (0.6% to 5.6%) |
| 240 | 8 (1.7% to 7.4%) | 4 (0.6% to 5.6%) |
| 480 | 3 (0.3% to 4.1%) | 7 (1.6% to 7.8%) |

### 1. A shared slow path

| Places | Worlds with a path pass, of 210 | of those, with one left unlabelled | Passes | labelled | by turning round | by the same year |
|---|---|---|---|---|---|---|
| 120 | 27 | 2 (0.9% to 24.3%) | 44 | 41 | 35 | 40 |
| 240 | 124 | 8 (2.8% to 12.3%) | 464 | 454 | 397 | 430 |
| 480 | 147 | 3 (0.4% to 5.8%) | 1,178 | 1,174 | 1,070 | 1,154 |

At 120 places mark 1 is held mostly by the referee refusing the path (183 of 210 worlds had no path pass), as said beforehand; of the 27 worlds where one passed, 2 left one unlabelled, and that interval is wide. At 240 places, where it was not known, 8 of 124.

By kind of path, worlds with a pass and with one unlabelled, of 30 (120, 240, 480 places): waves 0, 0, 0; cycle 4, 26, 30 with 0, 1, 1 unlabelled; boom 0, 0, 2 with 0, 0, 1; wander 8, 29, 30 with none; regimes 8, 29, 30 with 0, 2, 0; quasi_cycle 5, 25, 28 with 1, 2, 0; mixed 2, 15, 27 with 1, 3, 1. The one-off hump (boom) passed in 2 of 30 worlds at 480 places; in the second count it passed in none of 40.

The 17 unlabelled path passes, described after the count: 9 were sent by claim, and in 6 of those the turned-round form stood above the mark (2.4 to 3.1) but took nothing off its baseline's error, so it did not count as standing. In the other 11 the turned-round form stood below the mark (0.4 to 1.95). In all 17 the same-year reading fell just short of the forward one (by 0.05 to 0.9).

### 2. A planted lead

| Places | Passes of a lead | labelled | by turning round | by the same year | cannot be turned round | of those, labelled |
|---|---|---|---|---|---|---|
| 120 | 532 | 8 | 1 | 7 | 63 | 2 |
| 240 | 878 | 5 | 2 | 3 | 108 | 2 |
| 480 | 888 | 7 | 3 | 4 | 48 | 1 |

Answers alone: 4 of 394, 3 of 651, 5 of 664 labelled; keen passes naming a planted input: 4 of 138, 2 of 227, 2 of 224. By kind, the labelled passes: hidden mover 10, a series common to all places 5, many weak 4, sign differing by place 1; none for steady, thresholds, extremes, pairs or a sign by a third series' state. The hidden mover and the common series are labelled by the same year (a same-year reading a little above the forward one); many weak by turning round, a little above the mark (2.1 to 2.8).

### Beside, no mark

**A lead and a path in one pair** (135 worlds). The link that has a path beside it, sent for its own places, passed in 70 of 135 worlds (19 of 45 at 120 places, 26 at 240, 25 at 480), where the same kinds of link with no path beside them pass nearly always; and of those 70 passes 50 are labelled (10, 17 and 23). Counting every way it was sent and the keen proposer: 45, 74 and 85 passes at the three sizes, 21, 46 and 67 labelled. The world's other two links passed in 264 of 270 and 3 were labelled. So a slow path riding on a link's own pair hides the link about half the time (the path enters the series with either sign, so it can work against the link), and when the link is heard it mostly carries the label. Both are true of such a pair. **A label does not mean there is no lead.**

**The ceiling at 240 places**, the answer sent for the link's own places, of 60 links a kind (20 worlds, so rougher than the first two counts), beside 120 places at 35% and 480 places at 20% from the same count:

| Kind | 120 places, 35% | 240 places, 35% | 480 places, 20% |
|---|---|---|---|
| steady | 60 | 60 | 60 |
| threshold | 31 | 57 | 60 |
| extremes | 28 | 54 | 58 |
| pair | 27 | 56 | 60 |
| sign differing by place | 60 | 60 | 60 |
| sign by a third series' state | 8 | 10 | 17 |
| many weak | 29 | 60 | 60 |
| hidden mover | 53 | 60 | 60 |
| from a series common to all places | 27 | 41 | 24 |

At 240 places and 35%, seven of nine kinds are heard in at least 54 of 60 links; the two that are not both turn on a series common to all places, as before.

**Nothing else passed.** No keen pass in any of the 1,305 worlds named something that was neither a path's pair, a planted input, nor a near copy of one (near copies: 89 passes, all in worlds with links). The bar ran from 3.0 to 4.5. Seconds a world: middle 0.9 to 6.3 by size, 51.5 at most.

### What it changes

- **The second count's condition is met on made-up tables:** a pass carries a label, by a rule registered and counted on fresh worlds. On these worlds an unlabelled pass was a real lead in time and a labelled pass was shared slow movement about 99 times in 100 (1,669 of 1,686 path passes labelled; 20 of 2,298 lead passes labelled).
- **The words, from here on.** A pass: the forecast improves. An unlabelled pass: the series comes first in time. A labelled pass: the two may only be moving together, and a lead is not shown, nor ruled out. None of them: a cause.
- **At the size of the real yearly table** the referee hears seven of nine kinds of link at 35% when told where they are, and the label holds. That is the first measure at that size.
- **Still owed before a real table is read:** Stage B's own rule, with the table's main shared movements in the baseline (decision 0060). The label does not replace it: a lead riding on shared movement is hidden half the time and then labelled, so a real table full of shared movement would give few unlabelled passes whatever is in it.

### Limits

- One family of worlds, and the referee and the label were shaped on it; the seven path shapes had all been seen. The 99 in 100 is a figure for these worlds, not for a real table.
- The links here act a year later and never within the year. A real link that does both is labelled; how often real links are like that is not known.
- The hidden mover is the kind most often labelled (10 of its 430 passes), and it is also the kind the label cannot tell from a lead when it is unlabelled.
- Mark 1 at 120 places rests mostly on the referee refusing paths; among the 27 worlds where one passed the miss rate could be as high as one in four.
- Every lag is one year. A series common to all places cannot be turned round.
- The directly sent pairs and the answers are handed over by a script that knows the layout. They measure the referee and its label, not any finder.
