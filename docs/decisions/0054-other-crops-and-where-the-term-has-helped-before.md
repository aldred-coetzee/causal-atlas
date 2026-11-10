# 0054: The next records are the other crops in the same FAO file, and the question is whether the drought term is large enough to use where it has helped before

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The cereal test read a link (decisions 0051 to 0053): each country's drought index takes 1.67% off the squared error of a forecast of its cereal yields, about 0.8% of a typical error. That is real and too small to use. The same result said where to look next. Ten countries gave more than half of the gain, and the third of records where the term had helped most before 2005 kept 5.3% afterwards, while the rest kept nothing. So the link is strong in some records and absent in most, and a forecast that used the term only where it had already shown itself might be worth having.

That reading was made after the fact, on a record that is now spent for this driver. It can be tested only on records not yet read, with the rule written first.

## Decision

1. **The records are every other crop in the FAO file with enough long series.** A crop is in when it is a single crop (FAOSTAT item code under 1700; the codes above are sums), is not one of the six cereals already read, and has at least 30 country series with 30 or more official years of yield. That gives **47 crops**: potatoes, tomatoes, tobacco, onions, dry beans, groundnuts, cabbages, carrots, cucumbers, soya beans, grapes, seed cotton, dry peas, oats and 33 more. The panel is 2,339 records in 139 countries, with 78,552 official figures from 1986 to 2024. They were chosen by that count alone, on yields alone. No crop was picked or dropped for being thought rain-fed, irrigated, annual or a tree crop: that would be a hypothesis, and choosing by hand after the cereal result would be choosing with knowledge.
2. **The forecast is the cereal test's, unchanged** (`harvest.run`, as registered in `results/harvest-drought.md`): same baselines, same six months of the drought index, same five scales, same weights shared by all records, same 62 other-year controls, same flat driver. Two changes to the code, neither to any number: it now returns its parts record by record, and the flat driver can be run as a separate call. The cereal record's stored sums are reproduced exactly.
3. **One thing is added, the claim.** Each year, for each record, the slope of the baseline's error on the drought term is taken through the origin over the record's own earlier scored years, at least ten of them. The record **claims** that year when the slope stands 1.5 or more of its standard errors above zero. Where it claims, the forecast is the baseline plus the term at that slope, and **never at more than the term as it stands**: a record's past may shrink its term, not enlarge it. Everything is known before the year's figure is.
4. **The six cereals run beside the other crops and are not scored.** They are in the forecast, so they inform the baseline chosen each year, the slopes shared within a country and the shared weights; only the other crops' records are scored, and only they can claim. The cereal record is spent as an outcome for this driver; here it is an input, and each year uses only its earlier years.
5. **The interval draws countries and years again, both, from the start**, as decision 0053 found it should; sizes are of squared error, with the plain size beside.
6. **All crops are run together, not crop by crop.**
7. **No real yield of these crops is set beside any drought value until the rule is committed, its made-up marks hold and an independent reader has seen it.** So far their yields have been counted and put in a panel, alone.

## How the rule was shaped, and on what

On the spent cereal record and on made-up records with smoke seeds (`results/seed-ledger.md`), all of it development and none of it a result:

- **The claim from a record's own slope** covered more record-years than a claim from the record's past gain, at the same size.
- **The cap.** Letting a record's slope enlarge its term up to twice gave a larger point size on the cereal record and a wider interval, which at mid-year included zero. Capped at the term as it stands, both variants stayed above zero and the two halves of the years agreed. So the cap is 1.
- **Tried and dropped**, each because it did worse on the cereal record and on made-up records: using one scale's forecast and not the weighted five; the scale that had done best for the record; the mean of the scales; weights fitted record by record (much worse: the shared weights are what keeps the term from fitting noise).
- **Crop by crop** was tried on made-up records of 47 crops and was worse than all together: with fifty or so records a crop, the weights are noisy, and worlds with no link gave losses.
- **The cereals beside.** On made-up records, with the six cereal-like crops linked and no other crop linked, running them beside gave no gain in the other crops (−0.01% over all their records, with the cereals beside and without). Where other crops were linked, the linked records gained a little more with the cereals beside (0.42% against 0.32%; 1.50% against 1.15%). Those three worlds were run before the cap was fixed at 1; the leak was looked for again afterwards, through the script as it now stands, and not found (two worlds, −0.3% and −0.5% on the claims).

What the cereal record gave under this rule, for what a development number is worth: 6.3% of squared error on the claims at year-end (interval 3.5% to 8.9%, countries and years both drawn), on about a sixth of the record-years able to claim; 5.1% (2.1% to 7.7%) mid-year. **These numbers chose the rule, so they cannot also test it.** The other crops can.

## What is given up, and said beside any result

- **Not independent of the cereals.** Same countries, same weather years, same statistics offices. A pass would say the rule carries to other records, not that it has been confirmed on other evidence.
- **Dilution.** Vegetables under irrigation and tree crops are in, because the count rule let them in. If most of the 47 crops carry no link, the shared weights shrink the term for all of them. The made-up records measure how much link a silence would rule out; the smoke runs say it is a lot: a link taking 20% of a record's departures, in a sixth of the records, was not read, and one taking 35% was. So the made-up mark is set at 35%, and 20% is measured beside it.
- **A claim is not a named link.** At 1.5 standard errors a record with no link claims now and then by chance: in made-up worlds with no link in the other crops, such claims held about 5% of the squared error that could have been claimed. What is tested is the forecast on all claims together, not any one record.
- **Size.** The size words are the cereal test's, fixed before its result: under 1% of squared error too small to forecast with, 1% to 5% a real but small aid, 5% or more a usable aid; and here "usable" also needs the interval's lower end at 1% or more. Five percent of squared error is about 2.5% of a typical error.
- **Still a known link, still not cause**, and every limit of the cereal result applies: a country mean and not cropland, heat and El Niño not separated, some official yields perhaps estimated with weather.

## Considered and not done

- **Choosing rain-fed field crops by hand** (pulses, oil crops, roots). Would likely make a pass easier and the result narrower. It needs outside knowledge the method is not given; it can be a registered follow-up if the plain test is silent.
- **Reading the other crops with the pooled rule alone**, as the cereals were. Reported beside, with the same six conditions, but it does not answer whether the gain is large enough to use.
- **A different driver or a second driver.** One thing at a time: the claim is what is new here.

## Consequences

- `src/causal_atlas/claims.py`, `scripts/run_claims.py`, `tests/test_claims.py`; `yields.py` builds a panel for any set of crops; the made-up generator can make worlds of many crops, some of them cereal-like, and a link world that also carries a drift or a step. Spent seeds' worlds are unchanged, checked by hash.
- The rule, the made-up panels and their marks are in `results/crops-drought.md`, committed with this record and before any counted number.
- `docs/data-sources.md` and `data/manifest.toml` say what the FAO file is now used for.
