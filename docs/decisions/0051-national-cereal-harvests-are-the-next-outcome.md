# 0051: National cereal harvests are the next outcome, from FAO's crop statistics, official figures only

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

Burned area gave a miss and a measured null; local food prices were set aside before any real fit, because a market's own price already carries what a dry season will do to it (decision 0050). That decision named national harvests as what is looked at next, for two reasons: a harvest's own past says little about next year's weather, so the baseline leaves room, and the record runs from 1961, which gives thirty or more forecast years where prices gave eleven.

Rule 4 first. FAO's crop statistics were fetched as one file with no account, the terms were read at source (CC BY 4.0), and coverage was counted on yields alone.

## Decision

1. **The next outcome is cereal yield by country and year, from FAOSTAT's "Crops and livestock products".** One file, 34 MB zipped, 1961 to 2024. Fetched 2026-11-10, entered in `data/manifest.toml` and `docs/data-sources.md` in the same commit as this record.
2. **Only official figures are forecast.** Each figure carries a flag. Estimated figures and figures from other organisations are often last year's number carried forward (9% and 19% of them equal the year before, against 1% of official ones), and a forecast scored against a carried figure would be scored against no harvest at all. Whether they may stand in the *past* a forecast is made from is left to the rule.
3. **Nothing is set against drought, or against any other driver, until a rule is committed.** The only numbers computed so far are counts of years per country and crop, the flags, and the join to country borders.
4. **The driver is the drought file already held (SPEI), over each country's own cells.** No crop calendar and no cropland map is brought in: which months matter is left to the data. That keeps to the aim (relationships found, not assumed) and it is a limit, stated below.
5. **This sets aside "more domains" on the brief's Not-now list for this one data set,** on the same reading of decision 0040 as decisions 0045 and 0049 used, and it is his to overrule.

## What the file holds, counted on yields alone

- Country series with 40 or more official years: maize 89, rice 83, wheat 74, sorghum 61, barley 58, millet 38. 116 countries have at least one.
- The latest years are less official: for maize, 88 of 163 figures in 2024 against 133 of 161 in 2010.
- Countries change. USSR, Yugoslav SFR, Czechoslovakia, Ethiopia PDR, Sudan (former) and Belgium-Luxembourg end and their successors begin; China appears three times.
- 139 of the 149 countries with a cereal of 30 or more official years match the country borders already held by code; the rest are the dissolved states and four that need matching by name.

## What is given up, and said beside any result

- **Place and month.** This is a country and a year. It is coarser than the grid the project is built on, and a country mean blurs a large country.
- **Novelty.** That drought lowers harvests is known. A pass would be a rediscovery: the first link from climate into another domain that this project's chain can hear and that beats the baseline out of time, not a finding about the world.
- **Measurement.** Yield is production divided by area, as reported by each country. A national figure is as good as the country's own statistics.
- **Lead.** The harvest year's own weather is the driver, so what could be shown first is an early estimate at the year's end, before the figure is published. A forecast ahead of the season would need the drought outlook chained in, and is a later step.

## Considered and not done

- **Sub-national yields.** Closer to the grid, but no single open file with a long record was looked for; one reading would be needed first. Taken up only if the national test hears something.
- **A crop calendar and a cropland map, to pick the months and places.** Would make a link easier to hear, and is how others do it. Left out so that the months are found and not given; it can be the registered follow-up if the plain test is silent.
- **Cereals as one total per country.** Hides crops that fail in different seasons. The unit, and the floor of official years, are fixed in the rule.
- **Using estimated figures as targets, to gain countries.** See 2.

## Consequences

- Real yields stay unread against any driver until the rule is in `results/` and committed.
- The made-up generator must imitate what is known about this record: trends, breaks, shocks shared between neighbours, and stretches of carried figures.
- Every outcome tried is listed in the README and in `STATUS.md`, whatever this one gives.
