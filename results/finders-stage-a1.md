# The referee on made-up tables: does it pass what is not there, and what can it hear when handed the answer?

**Outcome (2026-11-10): counted once. The referee passed something in 3 of 600 worlds where nothing predicts (0.1% to 1.5%) and in 6 of 810 beside real links; every mark holds. Handed the answer and told where, it hears steady, sign-by-place and hidden-mover links at 35% in a table of 120 places and 60 years, and seven of nine kinds at 20% with four times the places; told nothing of where, it hears almost nothing at 120 places. One hole measured: a curving trend shared by a series and an outcome. The section "Result" has it with its limits.** Everything above that section stands as it was written before the count.

Rule first, committed before any counted seed (rule 9). Stage A1 of `docs/plan-finders-and-referee.md`: tests of the test. Authority: decisions 0040, 0055 to 0057 and 0059. Code: `src/causal_atlas/referee.py`, `scripts/run_referee.py`, `synth/table_panel.py`, tests in `tests/test_referee.py` and `tests/test_table_panel.py`. Seeds: `results/seed-ledger.md`. Rows: `results/finders-stage-a1.jsonl`, one a world.

Made-up tables only. No real series is read.

## Why

Every later stage rests on the referee: finders of any kind propose, and it alone decides what counts as found. So before any finder is built, two things are measured about it. Does it pass things in worlds where nothing predicts, when it is sent the forty proposals that fitted the early years best? And when it is handed the planted link itself, how often does it hear it? The second sets the ceiling: a finder cannot be blamed for a link the referee would not pass even when told.

## What has been looked at

The referee was shaped on smoke worlds from the same generator, seeds 27001 to 27086 (decision 0059, with what they gave). Those seeds are never counted. No world with a seed from 28001 on has been made.

## The worlds

`synth/table_panel.py`, written by a helper that never saw the referee. Forty series by 120 places by 60 years: 8 outcomes, 24 series of each place's own, 8 shared by all places. Places come in groups of five. A linked world plants three links of one kind, a year ahead, in the same quarter of the groups, at a stated share of what the outcome's own history leaves unexplained. Finders see years 0 to 34; the referee scores years 35 to 59.

**Where nothing predicts, 100 worlds each:**

| Panel | What | Seeds |
|---|---|---|
| none_plain | no link, no nuisance | 28001 to 28100 |
| none | no link; drift, a step, shared shocks, near copies, a change part-way, at the usual strength | 28101 to 28200 |
| none_strong | the same at twice the strength | 28201 to 28300 |
| none_rough | the same, with twice the spikes | 28301 to 28400 |
| none_gaps | the same, a tenth of the values missing | 28401 to 28500 |
| same_year | series move with outcomes in the same year, 35%; nothing leads | 28501 to 28600 |

**Where a link is planted, 30 worlds (90 links) a panel**, nine kinds, numbered 0 to 8: steady; threshold; extremes; pair; sign differing by place; sign differing by the state of a third series; many weak; hidden mover; steady from a series shared by all places. For kind i:

| Panel | What | Seeds |
|---|---|---|
| `<kind>_35` | 35%, 120 places | 29001 + 100i to 29030 + 100i |
| `<kind>_20` | 20%, 120 places | 30001 + 100i to 30030 + 100i |
| `<kind>_20_wide` | 20%, 480 places | 31001 + 100i to 31030 + 100i |

1,410 worlds. Each is read once; the script will not read a world a second time.

## What is sent

Forty proposals a world, under one bar.

- **The answer**, in linked and same-year worlds: each planted link in the form its kind calls for, sent three ways: for the places it is in; for all places; and by claim (each place's own past decides whether it applies). Up to nine of the forty.
- **A keen proposer** fills the rest, from the early years alone and knowing nothing of what was planted: half are the single-series slopes that fitted best over all places; half are the slopes that fitted best in the quarter of the groups where the series went most its pooled way, sent for those groups. It stands in for the worst a finder could do by choosing. Each of its proposals is tagged afterwards by the script, which knows the truth: it names a planted input of its outcome, its series is a near copy of one, or neither.

## Marks

1. **False passes.** On each panel where nothing predicts, at most 9 of 100 worlds have any pass at all; over the six, at most 40 of 600. On same_year the answers count: a same-year link passed a year ahead is a false pass. (At a true rate of 1 world in 20, ten or more of 100 comes about 3 times in 100, and more than 40 of 600 about 3 times in 100.)
2. **False passes beside real links.** Over the 810 linked worlds, at most 55 have a keen proposal pass that names neither a planted input nor a near copy of one.
3. **The ceiling.** For each of the nine kinds at 35%, the answer sent for the link's own places passes for at least 72 of the 90 links. A kind that does not is recorded as "could not be heard at this size of table", and no finder in a later stage is blamed for missing that kind at that size.
4. **No leak.** `tests/test_referee.py::test_no_later_year_reaches_an_earlier_score` holds for all twelve of its proposals on the commit that is counted.

If mark 1, 2 or 4 fails, the referee is not valid: nothing is built on it, the fault is found on smoke seeds, and the stage is run again on fresh seeds with this file saying so. Mark 3 is a measurement and cannot fail the referee; it says what can be asked of finders.

## Measured beside, no mark

- The same ceiling at 20%, and at 20% with four times the places.
- The answer sent for all places, and by claim: what not knowing where costs.
- The keen proposer's set proposals that name a planted input: how many pass, and how much of each passed set lies in the link's places. A first look at whether where a link holds can be found from the early years. It is one simple proposer, not a finder's test.
- The size reported for passed answers against the share planted. A passed size is the smaller of two forms and is of the squared error in each place's usual-error units, so it is not the planted share and is expected below it.
- The bar, and seconds a world.

## What it could change, said beforehand

- Kinds under the ceiling at 120 places and over it at 480: the yearly country table is too narrow for those kinds, and the data work that follows favours more places (sub-national series) for them.
- Kinds under it at both: finders for that kind are not built until the referee or the table changes.
- If the answer for all places stays unheard where the answer in its places passes, Stage A2's first finder is one that proposes where, not only what.

## Departures from the plan

- The plan named nuisance kinds one at a time (drift, step, near copies, a change part-way). The generator gives them together at a strength, so the panels vary strength, roughness and gaps.
- The plan sent one answer among thirty-nine other proposals. Here up to nine answers (three links, three ways) are among forty. The bar is over all forty either way.
- The keen proposer names sets of places as well as all places. It is not kept from the planted pairs: it may find them, and that is counted apart.
- Two kinds and one size are additions: the sign differing by the state of a third series, a link from a shared series, and the wide worlds.
- The referee itself: decision 0059.

## Limits, whatever the counts

- The referee has seen worlds from this generator, though not these. A pass here is on new worlds of one family. Real records have been rougher than made-up ones each time they were compared.
- Links of one world share their places and the bar, so 90 links are not 90 independent trials; intervals are taken over worlds.
- One length of record (60 years, 25 scored), one number of series (40), links one year ahead, in a quarter of the places.
- The ceiling is for the form the generator planted. A real link need not have one of these forms.

## Result (2026-11-10, counted once, 12:08 to 12:21 UTC, on commit acc6204)

All 1,410 worlds read, each once. `scripts/run_referee.py table` prints the full table from the rows; `scripts/referee_summary.py` the intervals; both read the rows only.

**Marks 1, 2 and 4 hold. Mark 3, the measurement: three of nine kinds are heard at this size of table.**

### 1. Where nothing predicts

| Panel | Worlds with any pass | Largest statistic of a proposal that did not pass (smaller form) | Mean bar |
|---|---|---|---|
| none_plain | 0 of 100 | 2.44 | 3.48 |
| none | 0 of 100 | 2.99 | 3.55 |
| none_strong | **3 of 100** (0.6% to 8.5%) | 3.64 | 3.64 |
| none_rough | 0 of 100 | 2.78 | 3.59 |
| none_gaps | 0 of 100 | 2.99 | 3.60 |
| same_year | 0 of 100, the 900 answers among them | 3.39 | 3.54 |
| all | **3 of 600** (0.1% to 1.5%) | | |

Mark: at most 9 a panel, 40 in all. Held. An empty panel's interval is 0% to 3.6%. Intervals are exact, over worlds.

### 2. Beside real links

**6 of 810** linked worlds (0.3% to 1.6%) had a keen proposal pass that named neither a planted input nor a near copy; 7 passes of 23,003 such proposals sent. Mark: at most 55. Held. **All six are among the 270 worlds with four times the places (0.8% to 4.8%); none among the 540 at 120 places (0% to 0.7%).**

### What those nine worlds were (a check after the count: `scripts/referee_look.py` makes them again; it changes no count)

- **Six are one thing: a curving drift the generator gives to an outcome and a series together**, place by place, in half the groups. The three at twice the usual strength (statistics 5.0 to 7.5 as the input fell, 3.6 to 6.0 with its past level and line removed, against bars near 3.6) and three more at the usual strength once there were 480 places. In the worlds as made, the series does go with the outcome a year later, out of time. It is a shared trend and not a link, and it is the weak point the independent reader of the other-crops rule found: **removing an input's past level and line does not remove a curve.** More places make the referee sharp enough to pass it at ordinary strength.
- **Three involve a series shared by all places.** In two the series goes with a planted shared input (by rank 0.46, under the 0.5 that counts as a near copy, and 0.74 with a planted input of another outcome), in worlds where the link itself is from a shared series. One (a shared series against an outcome with no link, in 120 of 480 places) has nothing behind it found here: the kind of false pass the stated rate allows.

### 3. The ceiling: the answer sent for the link's own places, links passed of 90

Intervals from drawing worlds again. Middle size: the share of squared error removed, smaller of the two forms, all 90.

| Kind | 35%, 120 places | middle size | 20%, 120 places | 20%, 480 places |
|---|---|---|---|---|
| steady | **90** (100% to 100%) | 20.7% | **84** (88% to 98%) | **90** |
| sign differing by place | **89** (97% to 100%) | 19.4% | **82** (84% to 98%) | **90** |
| hidden mover | **80** (83% to 94%) | 10.5% | 42 (38% to 57%) | **90** |
| from a series shared by all places | 64 (62% to 80%) | 21.9% | 29 (22% to 41%) | 56 (51% to 72%) |
| pair | 63 (57% to 81%) | 11.0% | 18 (12% to 29%) | **90** |
| threshold | 55 (52% to 70%) | 25.0% | 20 (14% to 31%) | **87** (92% to 100%) |
| extremes | 52 (47% to 69%) | 25.6% | 25 (19% to 39%) | **87** (93% to 100%) |
| many weak | 48 (43% to 63%) | 6.4% | 25 (19% to 38%) | **89** (97% to 100%) |
| sign differing by a third series' state | 21 (16% to 32%) | 5.8% | 5 (1% to 10%) | 38 (32% to 52%) |

Bold: at or over the mark of 72. **At 35% and 120 places: steady, sign by place and hidden mover are heard; the other six are recorded as "could not be heard at this size of table".** At 20% two kinds are heard. With four times the places, at 20%, seven of nine. The two that more places do not rescue both turn on a series that is the same for every place: what they can show grows with years, and there are 25 scored years however many places there are.

### Beside, no mark

**Not knowing where.** The same answers sent for all places, links passed of 90:

| Kind | 35%, 120 places | 20%, 120 places | 20%, 480 places |
|---|---|---|---|
| steady | 0 | 0 | 63 |
| sign differing by place | 0 | 1 | 72 |
| hidden mover | 0 | 0 | 24 |
| pair | 0 | 0 | 22 |
| threshold | 0 | 0 | 19 |
| many weak | 0 | 1 | 7 |
| extremes | 2 | 0 | 3 |
| sign by state | 0 | 0 | 2 |
| shared series | 0 | 0 | 1 |

At 120 places a link in a quarter of the places, sent for all places, passed 4 times in 1,620. The middle size was 0.2% to 2.3%.

**By claim** (each place's own past decides): steady 81 of 90 at 35%, 38 at 20%, 90 at 480 places; shared series 29, 3, 32; hidden mover 27, 0, 75; pair 8, 0, 53; many weak 2, 0, 15; threshold and extremes none anywhere. So a place's own past finds where a steady link holds when the link is strong or the table wide, and little else.

**The keen proposer's sets that named a planted input**, passed of sent, with how much of each passed set lay in the link's places:

| Kind | 35%, 120 places | 20%, 120 places | 20%, 480 places |
|---|---|---|---|
| steady | 86 of 90, every set at least four fifths inside (middle: all of it) | 69 of 89, the same | 90 of 90, middle 0.96 |
| hidden mover | 60 of 90, the same | 17 of 73 | 86 of 87, middle 0.88 |
| shared series | 57 of 90, 56 of them at least four fifths inside | 14 of 89 | 42 of 85, middle 0.92 |
| extremes | 17 of 69 | 1 of 37 | 20 of 44, middle 0.77 |
| threshold | 13 of 70 | 1 of 46 | 35 of 51, middle 0.75 |
| pair, sign by place, sign by state, many weak | none to speak of (1 of 106 for many weak) | none | none |

**So for the kinds a single slope can see, where a link holds can be found from the early years by something very simple, nearly as often as the referee passes the answer itself** (steady 86 against 90; shared 57 against 64; hidden 60 against 80). Its slopes for all places passed for no planted input at 120 places (0 of 474 at 35%) and for 62 of 88 steady ones at 480.

**Sizes.** A passed answer's middle size ran at about three fifths of the planted share for steady links (20.7% for 35%, 12.6% for 20%), about a third for hidden movers and pairs, about a fifth for many weak. Where few passed, those that did read larger than the middle of all sent (threshold at 20%: 24.9% against 19.3%): what gets over a bar is the lucky part, and a passed size from a weak panel overstates.

**Time.** 2,243 seconds of process time in all. About 0.6 seconds a world at 120 places and 1.9 at 480; threshold and extremes worlds took 3.6 and 14.

### What it changes

- **The referee is fit to build on, for this family of worlds:** it did not pass what was not there beyond its rate, and nothing later than a year reaches that year's score.
- **One hole is now measured and must be closed before any real table is read: a curving trend shared by a series and an outcome.** It is owed a third form of the inputs, or a baseline that carries a curve, shaped on smoke seeds and counted on fresh ones, with a wide no-link panel, which this stage did not have.
- **Where comes first.** As said beforehand: the answer for all places stayed unheard where the answer in its places passed, so Stage A2's first finder proposes where.
- **More places, for most kinds.** Threshold, extremes, pair, many weak, and the hidden mover at 20% are under the ceiling at 120 places and over it at 480. The yearly country table is too narrow for them; the data work that follows favours series below the country.
- **More years, for links through a common series.** A driver that is the same for every place (as an ocean index is) and a sign that turns on a common state are not rescued by more places. For those the route is more points in time, monthly where a source has months. Finders for a sign that turns on a common state are not built until then.
- **Finders are not blamed** for any kind in a cell of the ceiling table that is not bold.

### Limits

- Those written above the result, all of them. And: the six kinds "not heard" are not heard **by this referee at this size**; a sharper referee might hear them, and none was tried after the count.
- No panel had nothing planted and 480 places. The false-pass rate at that width is known only from keen proposals beside real links: 6 of 270 worlds, an interval that reaches 4.8%.
- The keen proposer is one simple rule. That it finds where steady links hold says such a finder is possible, not that it is good.
- The check of the nine worlds was made after the count and reads the generator's layout; it explains and decides nothing.
