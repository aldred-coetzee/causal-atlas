# 0048: What the independent check changed before any real field is fitted

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule. Amends decision 0047 and the rule in `results/fire-drought.md`. Every change is stricter.

## Context

The rule required an independent reader before any real field was fitted. Its report is `docs/reviews/2026-11-10-fire-drought-rule-check/report.md`. It found no leak and that the code matches the rule. It showed two ways the rule could read a link where none was planted, each on made-up panels of its own:

1. **The instrument check only removes what the same month's view explains.** When what is recorded depends on how well the month before was seen, panels with no link were read as a link 8 times in 9 at a strong setting, 0 in 6 at a weak one.
2. **A drift that quickens passes "beats all 14 shifts".** A five-year departure turns a straight-line drift into a constant, not a curved one. If driver and outcome both rise across the scoring years, the true pairing of years beats every reshuffle of them. One panel in three passed at a strong setting; the shifted drivers carried 1.87 of its 2.00 points.

It also noted that step 3 fits again without checking it has the model step 2 recorded, and that a gain which also shows in what the satellite saw should not be called a link.

This session reran two of its examples and its look at the real fields (burned area against the share observed, 1982 to 2003, no drought) and got its numbers.

## Decision

1. **One more condition for a pass.** The reading is repeated with every driver term, shifted or not, less its own straight line across the scoring years, so a rise or fall shared over those years earns nothing. A pass needs the first reading as registered and this one too: interval above zero and better than all 14 shifts. On the reader's passing drift panel this reading gives −0.06% and beats 13 of 14: no pass. On two planted-link smoke panels it changes nothing.
2. **A made-up panel for the month before's view, with a mark.** `before`: instrument only, what is recorded going as this month's share times the month before's to the power 0.3. That setting is above every real field on the reader's measure (panel: r about 0.10, band means spanning 0.44 standard deviations; largest real field, Australia: r −0.07, spanning 0.25). At most 2 of 24 seeds read as a link, and its four sixes join the empty sixes: at most 1 of 22.
3. **A quickening drift is measured, with no mark.** `curve`, at the reader's strong setting, 12 seeds. No mark because nothing ties that setting to the real fields: the real driver's own drift over 2004 to 2018 is near what chance gives (the reader's look at the driver alone).
4. **Names for the real reading.** Burned area and adjusted burned area both pass and the share observed does not: "a link". All three pass: "not separable from what the satellite saw", and not called a link. Otherwise: "no link". The words "not only what the satellite could see" are cut back to what is tested: not through the same month's view, nor through the month before's at the size seen in the fitting years.
5. **Step 3 refuses to score** unless every model it fits is the one step 2 recorded.
6. **Sizes.** S is quoted with S under the shifted drivers (mean) and S with terms less their line beside it; the smaller of the two S is the headline. The pooled reading is also given without 2018, the year the share observed falls in every field. That reading marks nothing.
7. **All made-up panels are run again under the amended verdict,** same panels and seeds, as rows of kind `made_up_2`; the first run's rows stay. The real fields are refused unless every mark holds on the new rows.

## Considered and not done

- **The reader's own repair for drift,** an interval above zero for S less its mean under the shifts. When driver and outcome both rise, each year adds to that difference with the same sign, so an interval over years would not be expected to stop it (reasoned, not computed). Taking the line out was run and does stop it.
- **A second adjustment for the month before's share.** On the reader's panels it closed the false link and cut a planted one to 1 of 3. It was built on the reader's own panel. Left out; the panel in point 2 measures the risk at the real size instead.
- **A panel with several satellite eras, or with drought that persists longer.** Stated as limits. The shifted drivers are the real driver, with its real persistence.
- **A lower setting for `before`.** 0.3 is already above the real fields; lower would be easier to pass.

## Consequences

- A pass is harder. A link that is itself a shared rise or fall over fifteen years will not be read.
- The instrument check is validated against two forms of instrument effect, not all. A sign opposite to the panel's (as in Australia) is not imitated.
- Seen before the fit, and disclosed: real burned area against the share observed on the fitting years, with no drought; the real driver's drift alone. No burned-area value has been set against drought.
