# 0063: The first read across the real table: between data sets, departures from the year's middle, placebos first

Status: accepted, 2026-11-11. Made by this session under decision 0040; reported to the owner, his to overrule.

## Context

The referee and the finders have been counted on made-up tables only. The plan says no real table is read until a rule of its own, committed first, puts the table's shared movements in the baseline. The table now holds 1,125 series. Each choice below could favour a result, so each is fixed here before any real series is set beside another. The rule itself, with its marks, is `results/stage-b-first-read.md`.

## Decision

1. **Country and year, 1961 to 2024.** The finders see 1961 to 1995 (thirty-five years, as in every count), the referee scores 1996 to 2014, and 2015 to 2024 is kept unopened for one last reading of whatever passes. Series that start later wait for a read with a later split.

2. **The panel is cut by a count rule** on coverage, each series alone: no series or place is chosen by hand.

3. **Only between data sets.** Four sets (crops, World Bank, exchange rates, climate); a row may name only series outside its outcome's set. This is the owner's aim as he states it, "relationships between many separate data sets", and it keeps out the ties that come from how one set is made. What it gives up: links between domains inside the World Bank's file (the economy against health, say). Those are a later read with its own rule, because that file's modelled figures need a guard this read does not have.

4. **Shared movements go into the baseline through the data, not the referee.** Each series that differs by place is read as its departure from the year's middle across places. The referee is left exactly as counted. Its bar already draws years and groups of places again, so shocks common to a year or a region widen the bar.

5. **The swarm as counted, less the every-pair member**, which cannot run at this width, and with a cut on what a row may name. Both are changes to what was counted; the placebos below are run with them.

6. **One bar over the whole read**: the steward's forty rows from all outcomes, at the counted rate. The whole read then has about a one in twenty chance of any pass where nothing predicts. More rows, or a bar for each set, would hear more and say less plainly what the chance is.

7. **Placebos on the real series before the real read, with marks that stop it.** Places moved round between sets, and years moved round between sets. The made-up tables do not carry everything the real one does; this measures the false-pass rate where it matters.

8. **A known answer planted on the real table**, so that a silence says what it rules out.

9. **Confirmation on the last ten years at a lower mark than a pass**: above the bar for one row, both ways, with something off the baseline's error, in five groups and five years. Ten years cannot carry the referee's full rule, and a row reaches this step only by passing it on nineteen.

10. **Groups are subregions**, small ones pooled, as the neighbours a baseline may use.

## Considered and not done

- **Changing the referee so a gathered term speaks where some of its series are missing.** It would wake the modes family on a table with gaps. It is a change to the counted referee, and is left for a later read.
- **Every pair of domains, inside the World Bank's file too.** See 3.
- **A bar for each set of outcomes.** See 6.
- **Monthly series.** The finders and the referee were counted on yearly tables of sixty years.

## Consequences

`results/stage-b-first-read.md`; `scripts/run_stage_b.py`; a small change to `src/causal_atlas/finders.py` that leaves every counted board the same; seeds 58001 on in `results/seed-ledger.md`.
