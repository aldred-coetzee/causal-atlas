# 0050: The price test is set aside before any real price is fitted; national harvests are looked at next

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

Decision 0049 chose local staple food prices as the eighth iteration's outcome, with the seventh's three faults to be fixed first and shown fixed on made-up panels. The test was built (`src/causal_atlas/rolling.py`): every year forecast from the years before it only, the baseline chosen and fitted again at each year, slopes shared by every market, then by wide squares, then by five-degree squares placed twice. So was a generator of made-up price records (`synth/price_panel.py`): national price levels that change pace part-way, world price rises reaching every market, gaps.

It was tried on six smoke panels (seeds 21801 to 21806), three with a link planted and three with none. The planted link raises the log price of a staple grown nearby by 0.1 for each unit the growing season's moisture index fell short, in about a quarter of the series, building over four months. That is at or above the sizes others have published (`docs/reading/food-prices.md`). Nothing here is a counted result, and no real price was set against drought.

What the smoke panels showed:

- **Three months ahead, a link of that size cannot be told from none.** With a link the forecast error changed by +0.5%, −0.2% and +0.2%; with none by −0.4%, +0.4% and −0.7%. One of the three panels with no link beat all ten year-shifted drivers. No panel passed, link or none.
- **The reason is measured, and it is about prices, not about the test's faults.** A market's own price three months back already tells most of what a dry season will do to it: once the price has started to move, it carries the news. Fitted on the planted series alone, in sample, with the answer's shape given, the driver takes about an eighth of what the baseline leaves; over every series, out of time, that is a fraction of one percent.
- **Setting each market against its country's other markets steadies the years** (its price change less the country's mean for that staple, its drought less the country's mean). One month ahead, three of three link panels were read as a link and none of three without; three months ahead, one of three. The sizes were 0.07% to 0.3% of the forecast error.

## Decision

1. **No rule is registered and no real price is fitted.** A test on this record could at best detect a link whose value to a forecast is a fraction of one percent, one month ahead. That is not a usable result, and rule 3 says a method that cannot hear a planted link of realistic size is not pointed at real data. The real prices stay unread against any driver, so they are still unspent.
2. **The code is kept, tested, and labelled as tried on made-up panels only.** The repairs to the seventh iteration's three faults exist in it. They have not been shown by a counted run, and this decision does not claim they have.
3. **The next outcome looked at is national harvests:** cereal yield by country and year, from FAO. Two reasons, both about what failed here. A harvest's own history says little about next year's weather, so the baseline leaves room where a price's does not. And the record runs from 1961, which gives thirty or more forecast years as the unit of evidence where prices gave eleven. Others have published the link from drought to yields, so it is a known answer and a pass would be a rediscovery; it would also be the first link here from climate into another domain.
4. **Rule 4 comes first.** The file is confirmed to be fetchable, licensed and long enough before anything is designed around it. If it is, it is admitted by its own decision and entered in the manifest and the sources page at first fetch.

## Considered and not done

- **Registering the within-country test at one month.** It would spend a reader and the record on a detection with no forecast value.
- **Choosing the lead after seeing what passes.** One month passed on smoke panels where three did not. A lead picked that way on made-up panels is still a design choice, but the three-month lead was the one named in decision 0049 for being usable, and nothing found here makes one month usable.
- **Country-level prices against country-level drought.** About thirty countries and eleven years, with inflation regimes in several: too few independent units.

## Consequences

- Prices remain held and recorded (decision 0049). A later test with a driver that leads by more than the price's own memory, or an outcome built from prices at a longer horizon, could use them.
- The harvest record is annual and national. That is coarser than the grid of place and month this project started from; if it is admitted the decision that admits it says what is given up.
- Every outcome tried is listed in `README.md` and `STATUS.md`, including this one, which stopped before a real fit.
