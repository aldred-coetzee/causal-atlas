# Plan: many finders, one referee, and the data in one shape

**The plan since 2026-11-10, 11:09 UTC.** It was committed as a draft while the other-crops test was open; that test is closed (`results/crops-drought.md`: read, a real but small aid), and the referee below is written from its rule, from what the independent reader found in it, and from what the real record did. Nothing here is registered as a test: each counted stage gets a results file with its marks, committed before any counted seed. **Built so far (2026-11-10, 12:10 UTC):** the made-up tables, the held data in one table, and the referee with its tests; the referee departs from points 5, 7 and 8 below as decision 0059 records, and its tests of the test are registered in `results/finders-stage-a1.md`. **Counted the same day, 12:21 UTC:** every mark holds; three of nine kinds are heard at 35% in 120 places, seven at 20% in 480; a link sent for all places is not heard at 120 places; a curving trend shared by a series and an outcome is passed and must be closed before Stage B. So Stage A2 begins with a finder of where, and the data work favours series below the country, and monthly series for drivers common to all places.

For decisions 0055, 0056 and 0057. A plan for an experiment and a build, not a survey (rules 1, 3, 5). No real series is set beside another under this plan until its last stage, which gets its own registered rule.

## What it is for, in the owner's words

"many, many data sets across which we find unexpected correlations for prediction"; "the right maths and things in place to find those connections"; "collecting the data and making it consumable and comparable"; "various forms of mathematics, not just the typical ones"; links that "won't be hypothesis based. They'll be emergent"; "how we're going to tie them together"; and in the end "what factors should we change to end up with a different outcome". And on how to begin: "We could just have deterministic swarms to start with".

## What ten iterations taught, which this is built on

1. **The judge that has held is the forecast on unseen years against a place's own history.** Every naming step judged by shifted copies of the candidates has had a fault of its own (decisions 0043, 0046). The two real results came from a forecast scored once.
2. **Real links are small.** About a sixth of the error where El Niño speaks; 1.7% of squared error for drought and cereals, most of it in a minority of records; 0.3% over 47 other crops, and 1.6% on the record-years their own past picked out. They were heard only by pooling many places.
3. **A baseline chosen once goes stale.** It is chosen again each year from the past (the harvest and other-crops tests do this).
4. **A miss means nothing without a ceiling.** Hand the method the exact answer first; if it cannot hear that, the instrument is at fault and no world is blamed (framework proposal, 2026-11-06).
5. **Made-up records must carry what real ones do:** drift, a step, shocks shared within a country, near copies of one series, a record that changes behaviour part-way.
6. **The maths has been read once already** (`docs/reading/further-maths.md`, `maths-for-combinations.md`, `multi-block-integration.md`, `ccm-edm-borrow.md`, 2026-11-05). Each page ends in a first test and a drop rule. None of those tests was run, because the work went to one driver at a time. This plan runs them, in one harness.
7. **Where matters as much as what.** Choosing place-years by each place's own past concentrated a thin link about five times on records never read (other crops, 2026-11-10). So "where" is part of every proposal, and "by claim" is one of its values.
8. **A check by someone with no part in the work has changed the wording or the rule every time.** Each counted stage that decides something gets one before its last step.

## The idea

- **Finding is free.** Any kind of maths may propose a link, by any route, on the early years only.
- **The finders are a swarm of small plain-code functions** (decision 0057). Each holds one kind of judgement. None makes a model call. They post to one shared board and may build on what others posted.
- **A proposal is a description, not a number.** Which outcome, which series, where, how far ahead, under what condition, in what form. One small vocabulary, the same for every finder.
- **One referee fits and scores every proposal the same way**, on years no finder saw, against the baseline, and charges for how many were proposed.
- **What passes says "helps predict".** "Changing it would change the outcome" is a different claim with its own evidence, and is a later layer.

Why this ties the kinds together: the error rate belongs to the referee alone. A finder can be strange, new or wrong without making a result dishonest; all it can do is waste its proposals. So kinds of maths can be added and dropped by measurement, and none has to be trusted.

## Stage A: which maths hears which kind of link (made-up records only)

### The made-up tables

Shaped like the table the data layer below produces: places by years by series, some series the same for every place (as an ocean index is). Small: 120 places, 60 years, 40 series. One size like the real table, set once the data layer has counted it. Every world carries the nuisances in point 5, and is rough as real records are: heavy tails and a few very rough places. The generator lives in `synth/` (`table_panel.py`, to the brief in `docs/specs/2026-11-10-made-up-tables.md`), is written by a helper that never sees a finder or the referee, and shares no code with either.

Each world plants a few links of one kind, a year ahead, in a quarter of the places, at a stated share of what the outcome's own history leaves unexplained (10%, 20%, 35%: the sizes of the other-crops panels, so the rulers compare).

| Kind | What is planted | Why it is there |
|---|---|---|
| Steady | the outcome moves with the series a year before | the usual case; the reference |
| Threshold | only beyond a level | droughts, not dry years |
| Extremes | an extreme in one makes an extreme in the other likelier; nothing in between | "detect future events" |
| Two together | A and B together move the outcome; neither alone does | combinations nobody would think of |
| Flipping | the sign differs by place or by the state of a third series | a pooled slope sees nothing |
| Many weak | twenty series each carry a little of one hidden mover | emergent: no single series shows it |
| Hidden mover | something unseen moves a series now and the outcome later | predicts, but changing the series would do nothing |
| Same-year only | series move together in the same year, nothing leads | must not be named a lead |
| None, drift, step, near copies | no link | false alarms |

### The proposal, in one form

`outcome`, `inputs` (one or more series, each with how far ahead), `where` (all places, a named set, or by claim: see the referee), `when` (always, or a condition on a series), `form` (one of: slope; hinge; tail event; product; slope by group; a mode built from named series with fixed weights). Nothing fitted to the outcome travels with it. A finder may send at most a fixed number per world.

### The board

One table that is only ever added to. A row is a proposal in the form above, with who posted it and which earlier rows it was built from. Members run in a fixed order with fixed seeds, in rounds: the first round reads the data; later rounds may also read the board (a pair-finder starts from the inputs single-series members put forward; a mode-builder gathers many weak proposals into one). Same inputs, same board, every time.

A steward, also plain code, chooses what goes to the referee within the fixed number, by a rule set beforehand: a share for each family, then proposals that members of different families arrived at separately. **Agreement decides the order, never the verdict.**

### The finders, first set

Each row below is a family of small members (one lag, one tail level, one scale each), not one large program.

| Finder | Kind of maths | Should hear | Read in |
|---|---|---|---|
| Lagged slope | pooled slope of what own history leaves, on each series a year before | steady | the reference; what has been used so far |
| Any shape | dependence on ranks and distances; and how far slopes differ between places | threshold, flipping | `further-maths` (transfer entropy is this in other units) |
| Extremes | how often tail events in one follow tail events in another, against chance | extremes, threshold | `maths-for-combinations` (subset scan, pattern search) |
| Trees and pairs | boosted trees on every lagged series, judged on held-back early years; then every pair among the top inputs on what single effects leave | two together, threshold | `maths-for-combinations` (FAST pairs; forests set aside there for naming, used here only to propose) |
| Shared modes | components of each domain's block, and the lagged cross-spectrum between blocks against a noise line from the null worlds | many weak, hidden mover | `further-maths` (random matrix), `multi-block-integration` (two-step angles) |
| The answer | told the planted link | the ceiling for every row | framework proposal |

Held for a second set, each only if a kind stays unheard by the first: exhaustive search for rare yes/no conditions; state-dependent methods on pooled short series (multispatial cross mapping; its own page says only after a known-answer test); top-down testing by family; regimes; rising spread and memory as warning signs.

### The referee

The other-crops rule, made general and with its weak points mended. The finders see the early years (the first 35 of 60 in the made-up tables); the referee scores every later year, forecasting each from the years before it. For each proposal sent:

1. **The term.** One number for each place and year, known before the year, built from the proposal's inputs as its form says: the input a year (or more) before; the part of it beyond a stated level of its own past; a yes or no for a tail event; the product of two inputs; the input with one slope for each named group of places or each state of a named series; a sum of named series with the proposal's fixed weights. Where the `when` condition is not met the term is zero.
2. **The baseline** for each outcome series is chosen again each year, by its error on the years before, from a small fixed set: the place's own past mean, its last value, its mean with a share of its last departure, its own line, and the mean of its group the year before. One baseline for an outcome, the same for every proposal on it. *As built (decision 0060):* the choice is made for each place, by its own earlier error with ten years of every place's usual error beside it, and a sixth baseline is among those chosen from: the line through the place's last fifteen years, carried forward. A place on a slow path of its own then gets a baseline that follows it.
3. **The fit.** Each year, the slope of the baseline's error on the term over every earlier year and every place the proposal applies to; one slope a proposal (one a group or state where the form says so), shrunk toward zero by a fixed amount. No slope of a place's own and no cap: on the real crop record the cap never acted, so it is left out and not claimed as a protection.
4. **Where.** All places; a set named by the finder from the early years; or **by claim**: each year a place is in when the slope of its own baseline error on the term, over ten or more of its own earlier years, stands 1.5 standard errors above zero. That is the other-crops rule. On the real record it multiplied a thin link about five times, and most single claims were worth nothing; it is a way to choose place-years, not to name places.
5. **The score** is the share of the baseline's squared error removed on the place-years the proposal applies to. For an event the forecast is a chance and the error is the squared miss of that chance, against the baseline's chance; the score is the same share. *As built (decision 0059):* errors are counted in each place's usual error so far, none as more than three of them, and an input's comparable form is held within three of its own past spreads; the share against the outcome as it fell is reported beside.
6. **Twice.** Once with each input as it fell, once with its level and line removed, the line fitted on earlier years only (the crop tests removed a line fitted over the whole record; this lets no later year in). A proposal must pass both, and its size is the smaller. A pass by one form is never a read: a trend shared by an input and an outcome passed the first form alone in 2 of 10 made-up worlds built for it, and the second form in none (decision 0058). *As built (decision 0060):* a curve shared by an input and an outcome passed both (Stage A1's hole), so there is a third read, a check that is not charged in the bar: each input as its departure from its own recent line. A proposal must stand two of its own spreads above zero there and take something off the baseline's error.
7. **The interval, and the charge for how many were sent.** Groups of places and years are both drawn again, the same draws for every proposal in the run. In each draw every proposal's score departs from its own by some number of its own spreads; the bar is set by the largest such departure among all proposals and both forms, at the level that 19 draws in 20 stay under. A proposal passes when its score stands more than that bar of its spreads above zero. *As built (decision 0059):* what is held to the bar is the agreement between the baseline's error and what the proposal adds to the forecast, about twice as sharp on made-up worlds; the share removed must be above zero besides, and is the size reported, with its own interval. So forty unlike proposals face a higher bar than one, and forty near copies face about the bar of one. The stated rate is: in a world where nothing predicts, any pass at all in at most 1 run in 20.
8. **And** the score stays above zero without its best year, and the proposal applies in at least five groups of places and ten scored years.
9. **Reported beside, deciding nothing:** the score with the inputs moved to other years (a weak control alone, because under the true alignment the fitted term is larger; decision 0058); the score on the place-years a claim left out; how many places and place-years; minutes.
10. **Nothing is chosen after the scores are seen.** A combination of proposals is a proposal like any other: posted before the referee runs, or kept for years not yet opened.

What the real record adds to this, to be remembered at Stage B: a rule shaped on one record gave 6.3% there and 1.6% on records never read, a fourfold fall; and the real record was rougher than any made-up one (a few very rough series, heavier tails), so the made-up tables here are made rough on purpose.

Tests of the test, marks set in the stage's results file before any counted seed:
- **False passes.** On worlds where nothing predicts (none; a strong shared drift, straight and curving; a step; near copies; a record that changes part-way; same-year movement with nothing leading), the referee is sent the forty proposals that fit the early years best, the hardest case there is for choosing, and passes stay at or under the stated rate, each kind by itself and all together. *As registered:* the generator gives its nuisances together at a strength and not one at a time, so the panels are no nuisance, all at the usual strength, all at twice it, rougher, with gaps, and same-year movement; half of the forty are slopes for all places and half are slopes in a set of places chosen from the early years.
- **The ceiling.** The answer, sent among thirty-nine such proposals so that it faces the full bar, passes in at least 8 of 10 worlds for each kind at 35%. *As registered:* a world has three links, and each link's answer is sent three ways in the one run of forty; the mark is 8 in 10 of the links, sent for the link's own places. It is sent three ways: with the true places, with all places, and by claim, so the cost of not knowing where is measured for every kind. A kind where it does not pass is reported as "could not be heard at this length", and no finder is blamed for it.
- **Leak.** Noise from a cut year onward changes no term, fit, claim or score of an earlier year.
- **Shared slow paths** (added after Stage A1's hole; `results/finders-stage-a1b.md`). The pairs that share the generator's curving drift are sent directly, at 120 and at 480 places; and paths of shapes a helper chose without sight of the referee are added to no-link worlds. A path the place's own history gives is to be refused. A path with fresh movement of its own is a hidden mover and is expected to pass (decision 0060), so before any real table is read a pass is labelled when it also passes turned round.

### The scorecard

For each kind and size: how often the answer passes; for each family, how often the true link is among its proposals, how often it then passes, how many false passes, and the minutes it took. A row for all families together under the one count. **And a row for the board: the same members with later rounds allowed to read it, against each working alone.** The kinds that should show a difference are "two together" and "many weak"; if the board adds nothing there, that is the finding.

### What is fixed beforehand

A finder is kept if, for some kind at 20% or 35%, it is the best or second best at getting the true link passed, and all finders together still keep the false passes under the stated rate without it being dropped. Otherwise it is dropped. No finder has a pass mark of its own: this stage is a measurement that chooses.

### What it could change

- Which maths is carried to real data, by count and not by taste.
- The ruler at this length: how strong and how widespread each kind of link must be to be found among this many series.
- **If the answer itself cannot pass at 20% with sixty yearly points, the yearly country table is too short for emergent links,** and the data work turns to monthly and sub-national series, where there are ten times the points. That decides what is collected next.

## The data in one shape (a build, beside Stage A; nothing is tested)

- Three tables in Parquet, read with DuckDB: `series` (id, source, domain, what it measures, unit, kind of value, how it is transformed, native place and period, first and last, licence), `place` (id, level, parent, coordinates), `obs` (series, place, period, value, a flag for estimated figures).
- First grid: country by year, and country by month where a source has months. Brought in from what is already held, by one adapter a source: FAO crops (every item with enough long series, yields, areas and production), the drought index as country means by month, El Niño and the 25 other climate indices, burned area, conflict events, market prices.
- **Comparable** means one function, used by every finder and the referee: each value as its departure from its own past, in units of its own past spread, using earlier years only; logs for quantities that cannot be negative, as the series table says.
- **Bringing series into the table sets nothing beside anything.** What is reported from the build is each series alone: counts by domain, lengths, gaps, memory.
- **A ledger of what has been read** (`results/spent-ledger.md`), like the seed ledger: which outcomes, against which series, over which years. The cereal and other-crop yields against drought, the drought fields against El Niño, burned area against drought are spent as recorded; prices are unread against anything (decision 0050).
- New data sets come in one at a time, each confirmed at source first for access, licence and coverage (rule 4), chosen by a count rule and not by hand, and preferring sources already in the table's shape.

## Stage B: the first run across many real series

Not planned here. It needs Stage A's table, the data layer's counts and its own rule, committed first: which years the finders see, which the referee keeps, what is already spent, and what a silence would rule out. An independent reader before the referee's years are opened.

## What to change, later

A passed proposal says a series helps predict. Before anything is called a factor that could be changed, it needs one of: the same link holding across places and periods that differ in other ways; a natural experiment; a known mechanism. Every result carries the label of which it has. Stage A plants the hidden mover so that this difference is measured from the start: how often each finder proposes a link that predicts and would not respond to change.

## The swarm

The finders are one, of plain-code members, from the start (decision 0057, the owner's "deterministic swarms to start with"). Nothing is taken from the agentic-swarms project and nothing is asked of it; the board here is kept in a shape the two could later share. A member that is not plain code would need a new decision: this project's pipeline makes no model calls at run time.

## Stages and cost

| Stage | What | Estimate, fresh tokens |
|---|---|---|
| Data layer | three tables from held sources (a helper, to `docs/specs/2026-11-10-data-in-one-shape.md`), the comparable function, the ledger (started: `results/spent-ledger.md`) | 0.5M to 1M |
| A1 | made-up tables, the proposal form, the referee, the answer, tests of the test | 1M to 1.5M |
| A1, second count | the shared-curve hole closed (decision 0060), a helper's shapes of shared path, the referee counted again | not estimated beforehand; counted and reported with its result |
| A2 | five finders, the registered rule, the counted run, an independent reader | 1.5M to 2.5M |
| B | its own plan | not estimated |

Estimates here have run low before. Tokens are counted and reported beside each result.

## Not in this plan

Maps, a web page, an API, global gridded coverage, a literature survey, any claim about cause. Monthly and sub-national tables wait for Stage A's ruler.
