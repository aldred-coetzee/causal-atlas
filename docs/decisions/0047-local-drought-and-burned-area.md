# 0047: Each cell's own drought against its burned area, across places, with years as the unit of evidence

Status: accepted, 2026-11-10. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The burned-area known answer missed (`results/fire-enso.md`), and decision 0046 set the blind region search aside. Two reasons the miss could not be separated: twenty fitting years, and a search that sets one series against one region's average. The burned-area record's scoring years, 2004 to 2018, are unread.

A driver that differs from cell to cell uses the same twenty years with thousands of driver values in each. Drought (SPEI-3) is held already, on the same grid.

## Decision

1. **The next test is `results/fire-drought.md`:** each cell's own drought four to twelve months earlier against its burned area, slopes shared within five-degree blocks, the years as the unit of evidence, scored once on 2004 to 2018 over the six fields together.
2. **Choices that could favour a result, each fixed in that rule before any counted number:**
   - a link is claimed only when it passes on burned area **and** on burned area less what the share observed explains; the share observed is tested beside them;
   - the controls are all 14 whole-year shifts of the driver field on the scoring years, each scored as the real alignment is (the lesson of 0046);
   - the driver is its departure from the cell's own previous five years, so a steady drift is not evidence;
   - false alarms are measured on made-up panels before a real field is touched: nothing, instrument only, drift only, by seed and six at a time as the real fields are read; the script refuses the real fields if a mark misses;
   - an independent reader sees the rule, the code and the made-up results before any real field is fitted.
3. **The design was reached on four smoke seeds,** and every change made after seeing a smoke result is listed in the rule.
4. **No new data.** Burned area was admitted by decision 0045; drought has been held since Phase 0.

## Considered and not done

- **Centring or detrending the driver on the fitting years as well.** The year-shifted controls already keep a constant and so do not reward it. Left as a stated limit, with S under the shifts reported beside any pass.
- **A second, stronger drift panel.** One more guess about the real drift's size would not settle it; the shifted controls are what stand against drift on the real fields.
- **Taking El Niño out first.** It would make this a test of two things at once. It is the registered follow-up if a link is read.
- **Reading each field by itself.** Six readings at fifteen years each; the pooled reading is the one the made-up sixes measure.
- **Finer blocks, to say where.** The smoke runs show claims are not well placed even at five degrees. Where is not claimed.
- **Changing the 0.2 seen threshold or the outcome's preparation.** Kept exactly as registered in `results/fire-enso.md`, so nothing about the outcome is chosen with this driver in mind.

## Consequences

- Burned area's 2004 to 2018 are spent for this driver when step 3 runs, pass or miss.
- A pass is a named pair (drought, burned area) with place, season, lag and sign left to the data. It is not yet the brief's "without hypothesising"; it is the first step outside climate that could clear rule 2.
