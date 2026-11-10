# 0049: Local staple food prices are the third domain, from the World Bank's market file, observed prices only

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

Burned area gave two misses: the known answer (`results/fire-enso.md`) and each place's own drought (`results/fire-drought.md`), the second a measured null. On that record the test could have heard a link moving 5% of the variance in a fifth of the places, no smaller, and three faults in the test were found (listed in that results file). The owner's aim is relationships between separate data sets that help detect future events. A third outcome is needed, one where a lead of months is plausible and others have measured it.

Rule 4 first: a bounded reading asked which place-by-place price data can be fetched by script with no account, on what terms, and whether the prices are observed or modelled (`docs/reading/food-prices.md`).

## Decision

1. **The third domain is local staple food prices: the World Bank's "Monthly food price estimates by product and market" (Real Time Food Prices), release 2026-11-02.** One file, 133 MB zipped, 37 countries, 3,229 markets, monthly from 2007-01, latitude and longitude for 3,192 of them. Fetched 2026-11-10 with no account, entered in `data/manifest.toml` and `docs/data-sources.md` in the same commit as this record.
2. **Only the observed prices are used.** The file carries, for each item, a column of prices as collected and several columns of model estimates that fill every month. The estimates borrow from other markets, other items and the season, which would blur or manufacture a local signal. A market-month with no observed price is missing, not filled.
3. **Nothing is set against drought until a rule is committed.** The only numbers computed so far are counts of observed months per market, on prices alone (below).
4. **The three faults found on burned area are fixed in the test, and shown fixed on made-up panels, before any real price is fitted.**
5. **This sets aside "more domains" on the brief's Not-now list for this one data set,** on the same reading of decision 0040 as decision 0045 used, and it is his to overrule.

## What the file holds, counted on prices alone

- Observed months of the main cereals: rice 142,009, maize 98,550, millet 66,690, sorghum 62,955, wheat flour 29,332, wheat 10,390; a second set of columns from FAO adds about 48,000.
- **571 markets in 33 countries have one cereal with 120 or more observed months; 272 have 180 or more.** Most are in the Sahel: Mali 66, Burkina Faso 63, Niger 60, Senegal 48. Then Malawi 39, Ethiopia 25, The Gambia 24, Mozambique 23, Burundi 22, Chad 20. Indonesia, Madagascar, Liberia and Libya have none.
- Where an observed price exists, the model's closing estimate equals it in about 90% of months and differs in the rest. That fits the documentation's "outliers in the data are often adjusted" applying to the estimates. That the plain column is the price as collected is read from the file; the documentation seen does not say so in words.

## Considered and not done

- **FAO's price tool (GIEWS FPMA).** Longer records (from 1987; 714 cereal series in 95 countries spanning 15 years or more), observed prices, hosted in Rome. But it has no coordinates, so each market would be placed by name; many series belong to third parties that FAO's open licence excludes; and it is a live service with no dated release. Kept as the fallback if the World Bank file proves too short.
- **FEWS NET and WFP's own service.** The first forbids automated access; the second gives credentials only by email. Neither touched.
- **The model-estimated columns,** which would give every market every month. Not used, for the reason in point 2.

## Consequences

- **The host is the World Bank, in the United States.** The brief asks for European, non-US-controlled infrastructure where practical. No European source with coordinates and a dated release was found. Only a checksum and a fetch script are kept here.
- **The record is short:** 2007 to 2024 where it meets the drought file, eighteen years at most, fewer for most markets. The fitting and scoring spans will both be short, the interval wide, and the years include shocks shared by every market (2008, 2011, 2022). The design has to say what it can hear before it reads anything.
- **Prices move together.** Markets in one country share a currency, a border policy and a harvest, so the number of independent pieces of evidence is far below the number of markets. Years remain the unit of evidence.
- A pass would be the first link here between a climate record and an economic one. Others have published the link (sizes in the reading page), so a pass is a rediscovery with a forecast attached, not a discovery.
