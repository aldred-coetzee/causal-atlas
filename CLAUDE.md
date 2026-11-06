# causal-atlas: standing brief

Read this, then `STATUS.md`, then the plan for the current phase. Decisions
and their reasons are in `docs/decisions/`. This file is a distillation; the
owner's brief of 2026-11-05 is the authority and is kept verbatim outside
this public repo, at `~/projects/box-config/docs/causal-atlas-brief-2026-11-05.md`.
If the two disagree, the brief wins and this file is wrong.

## Aim (working statement, 2026-11-05)

A spatiotemporal observatory: bring event and indicator data from different
domains (conflict, climate, food, prices and others) onto one grid of place
and month, find time-lagged relationships between domains, and use them to
predict trends. Pipeline: finder, cleanser, correlator, predictor.

Working hypothesis, to be tested and not assumed: lagged signals from other
domains improve the prediction of an outcome in a place beyond what that
place's own history and seasonality already give.

**Refined by the owner, 2026-11-05 evening** (his full words: decision 0021): given
a whole bunch of factors, and "we don't know what those factors are", find
"combinations of all of these things, some of these things, or any number of these
things that might actually help us to predict or infer a direction", including
combinations nobody would have thought of. A named hypothesis "could be one of the
things we look at as well". "I don't have the answers as to how we do this yet.
That's what we're trying to figure out." Phase 1's design, rules and not-now list
stand until a plan revision and his yes change them.

**Restated by the owner, 2026-11-06** (decision 0027): "We are trying to find a way to discover relationships between many separate data sets to see if behaviour emerges which would allow us to detect future events or if possible provide insight into contributing factors would perhaps accelerate or prevent events".

Update this statement, with the date, when the owner refines it.

## Who does what

- **This session** does the project's work: repo files, plan, code, results,
  and a report at each gate. It does not change box configuration; it asks.
- **next-pattern** (the coordinating session) relays the owner's decisions in
  his words, makes box-level settings, and audits exactly twice: the Phase 1
  plan and the Phase 1 result.
- **The owner decides.** Give him the options, a recommendation and the cost,
  in plain language. He works from a phone, about 8 hours a week, and the
  subscription limit is shared with every other session on the box.

## Fixed constraints

- Public and open source. History is permanent: nothing is committed that
  should not be public.
- MIT for code (`LICENSE`), CC BY 4.0 for text (`LICENSE-CC-BY-4.0`).
- No person-level inference. Limitations are published beside every finding.
- European, non-US-controlled infrastructure where practical.
- Deterministic at runtime: LLMs only inside sessions at design time. No model
  calls in pipeline code.
- Runs on this box: 8 cores, 16 GB RAM, 512 GB NVMe, shared with live apps.
  Python under uv, DuckDB and Parquet.
- Provisional, to be confirmed by test and not by reading: 0.5 degree
  PRIO-GRID-compatible cells, monthly; PCMCI (tigramite) and empirical dynamic
  modelling (pyEDM) as candidate methods.

## Rules

1. **Experiment before survey.** The first deliverable is a test result, not a
   document about the field.
2. **Baseline first.** The baseline is each cell's own history plus seasonality
   plus its neighbours' recent values. Nothing is a finding unless it beats that
   out of time.
3. **Known-answer test before discovery.** Run the method on a synthetic panel
   with planted lagged links and on a null panel with none. Report recovery,
   false discoveries and runtime on this box. The generator shares no code or
   assumptions with the detector.
4. **Data before theory.** Confirm a dataset can be fetched, is licensed for our
   use and covers the period before designing around it.
5. **Reading is pulled by a decision.** One question, one agent, one page back.
   No research map, no claim ledger, no batches of directions. Check at source
   only the claims a decision or a published number rests on. Nothing is cited
   from memory.
6. **Budgets and gates.** Each phase has a token cap. At each gate report in at
   most ten lines: what was done, the result with its interval and caveats,
   tokens against the cap, the proposed next step and its estimate. If the gate
   passes its pre-registered marks, send the report, say why it passed and carry
   on. Stop and ask only when it really needs his guidance: a missed mark, a
   surprise that questions the design, a rule change that could favour a result,
   a choice outside the plan. The end of 1d is always a stop (decision 0014,
   changing the brief at the owner's word). Step estimates are stated and overruns
   reported beside the result, not put to him and not a stop (decision 0035). If the owner says to go broader, quote this rule
   back and ask him to confirm.
7. **Subagents.** None by default. At most three at once, each with a written
   spec, estimated cost stated before spawning. Sonnet for mechanical work,
   Haiku for link and DOI checks. Independent review only for a result that
   decides something or is surprising. The owner allows Fable for deep thinking
   where it would help (2026-11-05); the spec and cost rules still apply.
8. **Context.** `autoCompactWindow` is checked, not assumed (200000 on
   2026-11-05). Keep `STATUS.md` good enough to start a cold session. Inspect
   data with DuckDB queries, never by reading large files into context.
9. **Pre-registration.** Metric, split, baseline and threshold go into the
   results file and are committed before any number is computed. The held-out
   set is scored once. Deviations are disclosed. Summaries keep the qualifiers
   of the file they summarise and report the interval, not only the verdict.
10. **Hygiene at entry.** Each dataset gets a manifest entry when first fetched:
    source URL, licence, date fetched, checksum, coverage, known biases. Data is
    never committed; fetch scripts and checksums are. Third-party text is quoted
    briefly, attributed, and keeps its owner's licence. No email address goes to
    an external service or into the repo. No secrets. No AI trailers in commits.
    **Before every push, sweep the staged changes for all of these.**

## Token caps

Phase 0: 300k. Phase 1: 20M (the owner, decision 0035; "on this" read as Phase 1). Both cover this session and next-pattern. A cap
counts fresh tokens (input + output + cache writes); cache reads are reported
beside them at every gate (decision 0006).

## Records

- `STATUS.md`: the honest current state.
- `docs/decisions/NNNN-title.md`: context, decision, consequences, status.
  Immutable: superseded by a new entry, never edited. A record, not reading:
  open one only when its reason is needed. Write a new entry only for a choice
  that could favour a result (if in doubt, it could), a change to a rule, or
  anything the owner ruled on. Any other choice goes in its commit message or
  the results file (decision 0022).
- `results/`: one file per experiment, rule first, committed before the numbers.
- `docs/plan-phase-1.md`: the pre-registered Phase 1 design.
- `docs/data-sources.md`: every source checked, its access route, links and licence
  requirements. The owner counts this as part of the project's value: update it in the
  same commit as any source change, with `data/manifest.toml` (decision 0013).

## Git

- Remote `origin`, branch `main`. Never force-push.
- Commits use a GitHub noreply address, set in this repo's local git config,
  because the box's global identity is a personal email (decision 0009). A fresh
  clone must set it again before committing: check `git config user.email`.
- No AI trailers, whatever a harness default suggests.

## Box facts

- `uv` is at `~/.local/bin/uv`. Anything missing: ask next-pattern; do not
  install system-wide.
- The Remote Control unit and the nightly work log for this project live in the
  private `box-config` repo, so no commit appears here that this session did not
  make.
- Long runs are `nice -n 19` with at most 6 threads: live apps share the box.

## Not now

Web UI, maps, API, more domains, global coverage, a generic adapter framework,
a dataset catalogue, a literature survey, causal-finance. Each needs a Phase 1
result and the owner's yes.
