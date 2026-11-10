# causal-atlas

A spatiotemporal observatory, at an early stage. The aim is to bring event and
indicator data from different domains (conflict, climate, food, prices and
others) onto one grid of place and month, find time-lagged relationships between
domains, and use them to predict trends.

The owner's aim, refined on 2026-11-05, is broader than any one link: from many
factors, not known in advance, find combinations that help to predict or infer a
direction, including combinations nobody would have thought of. How to do that is
still an open question. His words are in
`docs/decisions/0021-owner-refines-the-aim.md`. The first experiment below tests
the narrower question.

**Where it stands (2026-11-10).** Nothing new about the world has been found.
What has been shown is that the chain works end to end on links that are already
known: one inside climate, and since 2026-11-10 one from weather into farm
statistics, small and independently checked, and carried the same day to 47
other crops, where it is smaller still (the paragraphs on harvests below).
Among 31 decoys, the search named El Niño blind as a driver of drought on
four continents and stayed silent in Europe. A forecast built from that, fitted
on 1950 to 1999 and scored once on 2000 to 2024, had about a sixth less error
(17%, between 12% and 22%) than a forecast from each region's own history, on the
region-months where it made a claim. Each of the four passes by itself, North
America narrowly (its own interval starts just above zero). A side check
afterwards, which is not a test, measured El Niño on a fixed base instead of
NOAA's moving one: the four together still pass, at 13% to 14%, and North America
by itself does not. An earlier attempt on
Africa missed and is published as a miss. The result, its limits, an independent
check and an audit are in `results/real-enso-continents.md`; the independent
reader's report and code are in `docs/reviews/`.

This is a climate-to-climate link. No claim about conflict follows from it. One limit
touches every number here: the drought file used carries an error its makers have
acknowledged (small, they say, and largest in dry regions), and a corrected file
is not yet out.

From that tested model there is a dated outlook for November 2026 to September
2027, with the rule for scoring it fixed in advance: `results/outlook-2026-27.md`.
It is a test of the method that can fail in public, not a warning service.

The step after that handed the search 25 more real climate series at once, chosen
by a rule and not by hand. The first attempt stopped at its own check: among that
many real candidates the search could no longer reliably hear a link planted on
purpose, and nothing was scored (`results/real-indices.md`). The cause was a defect
in the search's controls. With it corrected, and the same pass marks on fresh
seeds, the search passed every check and named 16 series-and-region pairs beyond
El Niño. Scored once on 2000 to 2024, none of them improves the forecast four or
more months ahead once each region's own history and El Niño are in it
(`results/real-indices-2.md`). So among these climate series El Niño is the only
usable lead found. An independent reader has since found that the corrected
controls are themselves lopsided and let the search raise false alarms more often
than was assumed, so the search is set aside until that is put right and measured
(`docs/decisions/0046-the-corrected-controls-are-lopsided.md`). The step that
used it named nothing that survived, so no claim rests on it.

The first step outside climate was burned area from satellites, 1982 to 2018, with
a link others have published (El Niño leading fire) to rediscover first. It missed
(`results/fire-enso.md`): on twenty fitting years the search named El Niño nowhere,
and its own false-alarm checks failed. The forecast step was not run. An
independent reader confirmed the miss and corrected the explanation first given
for it: the false alarms come mostly from the lopsided controls, not only from the
short record, and the product does not show 1997, the year the published link is
best known for, as a large fire year in equatorial Asia, so the known answer may
not have been there to find. One thing about the data came out of it: in this
product El Niño shows more clearly in how much land the satellite could see than
in what it reports as burned.

A different test on the same record was then run (`results/fire-drought.md`):
each place's own drought, four or more months earlier, against its burned area,
with a check that a link is not only what the satellite could see. It passed its
checks on made-up data, where the answer is known. An independent check of the
rule and code found two ways it could read a link that is not there; the rule
was tightened for both and the made-up checks held again. Scored once on 2004
to 2018, **it found nothing**: the drought term changes the forecast error by
−0.03% (interval −0.08% to +0.03%) over six continental fields. One thing about
the data came out of this too: after 2003 the record does not behave as it did
before, in a way the made-up data did not imitate. So a link of known size was
then added to the real record and scored the same way, to see what the silence
can rule out. It rules out a link moving 5% or more of the variance in a fifth
of the places when the link lies in areas the method's five-degree blocks sit
inside, and only 20% or more when it lies in patches astride them; smaller
links, and links of a more realistic shape, are not ruled out. It also showed
that the rule as registered could not have reported a link on this record at
all, because one of its conditions leans on a baseline that had gone stale.
The null stands on the measured size, which is zero within a narrow interval;
the faults are listed in the results file for whatever is built next.

Local food prices came next: the World Bank's file of staple prices as collected at
markets, monthly from 2007. The test was rebuilt for them and tried on made-up
price records only. A drought link of the size others have published could not
be told from no link three months ahead, because a market's own price three
months back already carries most of what a dry season will do to it. A month
ahead it could be heard, at a fraction of one percent of the forecast error,
which is no use to anyone. So **no real price was set against drought**, and the
prices are still unread (`docs/decisions/0050-the-price-test-is-set-aside-before-any-real-fit.md`).
National harvests came next: FAO's cereal yields by country and year, 503 records
in 141 countries, where a record's own past says little about next year's
weather. Each year from 1986 to 2024 was forecast from the years before it, with
and without each country's drought index at six fixed months. The rule was
committed first, checked on made-up records with a link and with none (70
records with no link, each read two ways, none read as a link), and read by an
independent reader before any real yield was touched. Scored once, **it read a link** (`results/harvest-drought.md`):
the drought index takes 1.67% off the forecast's squared error (interval 0.97%
to 2.35% as registered; 0.6% to 2.8% when the interval allows for a country's
crops sharing one weather record), and 1.11% with the weather known only to
June. In the size of a typical error that is about 0.8%. The weather of 62 other
years, tried the same way, does nothing, and neither does the weather of a
country far away. In the third of records where it had helped most before 2005,
it went on to take 5.3% off (3.9% to 6.7%) in 2005 to 2024; in the rest of the
records long enough to rank, it took nothing off.

What that is: the first time here that a series from one domain has improved a
forecast in another under these rules. What it is not: new, large, or proof of
cause. Everyone knows drought cuts harvests; what the method was not told is
which months, crops, countries or sign. Under one percent of a typical error is
too small to plan by, and about a fifth of the countries, mostly dry places
that farm on rain, carry all of it. Heat and El Niño move with the index and are not separated, and anything
that drives both the index and the yield would be read the same way. The index
is a country's mean over all its land, not its cropland. Some official yields
may themselves be estimated with the help of weather. A second independent
reader rebuilt the forecast with its own code and found the same thing a little
smaller (1.2%), found no leak, and had the wording here corrected; its report is
in `docs/reviews/2026-11-10-harvest-result-check/`.

The next test (`results/crops-drought.md`) asked whether that small gain is large enough to use in the records where it
has shown itself before: each year a record "claims" if, over its own earlier
years, the drought term has gone with its yield, and only claims are forecast
with drought. It was to be scored once on the 47 other crops in the same FAO
file (2,339 records, chosen by a count and not by hand), with the cereals
running beside them unscored. The rule was shaped on the cereal record, which
is why the cereals cannot test it. On made-up records every mark set
beforehand held: of 75 runs on 55 worlds where only the cereal-like crops are
linked, or nothing is, none was read; a link taking 35% of the year-to-year
departures in about a quarter of the records was read in 15 of 15 worlds at
year-end and 9 of 10 at mid-year; a 20% link in 4 of 10, and a 35% link in a
tenth of the records in 5 of 10 (5 of the 8 worlds that had a linked record). So a silence on the real record would rule out
only a strong and fairly widespread link. An independent reader then tried to make the rule read
something that was not there and could not; it had five things said more
plainly, among them that the real record is rougher than the made-up ones and
that a trend shared by drought and yields is held off only by the second form
of the driver, with its level and line removed. No condition of the rule
changed (`docs/reviews/2026-11-10-crops-rule-check/`). 

**The real record was then read, once (2026-11-10): a real but small aid.** In
the record-years that claimed, drought took 1.62% off the squared error of the
yield forecast (interval 0.84% to 2.46%; about 0.8% of a typical error) with
the weather known to December of the harvest year, and 1.01% (0.27% to 1.78%)
with it known to June. Every condition set beforehand held, with the driver as
it fell and with its level and line removed. It is not enough to forecast
with: the mark for a usable aid was 5%. Over all 2,339 records the gain is
0.31% (0.05% to 0.57%), about a fifth of the cereals', so choosing where to
use drought by each record's own past concentrates a thin link about five
times. Five crops give half of the gain (sugar beet, soya beans, oats,
sunflower seed, potatoes) and vegetables and fruit give none; Spain gives 14%
and ten countries 65%; more of the records that claim lose a little than gain.
The rule had given 6.3% on the cereal record it was shaped on, and gives 1.6%
on records never read before. This result was not rebuilt by a second reader,
is not independent of the cereal result (same countries, weather years and
statistics offices), and does not show cause. These crops' records are now
spent for this driver.

`STATUS.md` says where things stand in more detail.

## The question

Do lagged signals from other domains improve the prediction of an outcome in a
place beyond what that place's own history and seasonality already give? This is
a working hypothesis, to be tested and not assumed. It may well be false; a
clean "no" is an acceptable result and would be published the same way.

## How it is run

The first deliverable is a test, not a survey. A baseline comes first, and
nothing counts as a finding unless it beats that baseline out of time. A method
must recover planted links in synthetic data, and find none in null data, before
it is pointed at real data. Metric, split and threshold are committed before any
number is computed, and the held-out set is scored once. The rules, and the
failure in an earlier project that produced them, are in
`docs/decisions/0004-working-rules.md`.

The analysis is at the level of grid cells and months. There is no person-level
inference, and limitations are published beside every finding. Pipeline code
makes no model calls: it is deterministic at runtime.

## Layout

- `CLAUDE.md`: the standing brief for the working session.
- `STATUS.md`: the honest current state.
- `docs/data-sources.md`: every source checked, how to get it and what its
  licence requires.
- `docs/plan-phase-1.md`: the first design, on synthetic data.
- `docs/decisions/`: decision records, immutable once written.
- `docs/reviews/`: reports of independent checks, as written, with their code.
- `results/`: one file per experiment, its rule committed before its numbers.
- `data/manifest.toml`: versions and checksums. `scripts/`: fetch scripts.

## Licence

Code is MIT (`LICENSE`). Text is CC BY 4.0 (`LICENSE-CC-BY-4.0`). Third-party
material keeps its owner's licence. No dataset is held in this repo: only fetch
scripts, checksums and a manifest recording each source's own terms.

Burned-area data: this project acknowledges the ESA Climate Change Initiative and
the Fire CCI project. Chuvieco, E.; Pettinari, M.L.; Otón, G. (2020): ESA Fire
Climate Change Initiative (Fire_cci): AVHRR-LTDR Fire_cci Burned Area Grid
product, version 1.1. Centre for Environmental Data Analysis.
doi:10.5285/62866635ab074e07b93f17fbf87a2c1a. Every source's terms and citation
are in `docs/data-sources.md`.
