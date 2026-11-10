# 0057: The owner: "We could just have deterministic swarms to start with"

**Date:** 2026-11-10, 10:25 UTC. **Status:** his words, typed here directly, after the report that a draft of the next plan was written (`docs/plan-finders-and-referee.md`), whose section on the swarm said "Noted, nothing done". The reading below them is this session's and his to correct.

## His words

"We could just have deterministic swarms to start with"

## The reading

1. **The finders are the swarm, and to start with every member is plain code.** Many small functions, each holding one kind of mathematical judgement, none making a model call. That is already what this project's fixed constraints ask of anything that runs (deterministic at run time), so nothing in the brief is set aside.
2. **They share one board.** Each posts its proposals, in the one form, to a table that is only ever added to. A later member may read what earlier members posted and build on it: a pair-finder starts from the inputs single-series finders put forward; a mode-builder gathers many weak proposals into one. Every row says who posted it and which earlier rows it was built from.
3. **Same inputs, same board, every time.** A fixed order of running and fixed seeds, so a result can be rebuilt from the repo and the data alone.
4. **Agreement between members is not evidence.** It may decide the order in which proposals go to the referee, by a rule fixed beforehand. Only the referee, on years no member saw, says what holds.
5. **"To start with" leaves room for members of other kinds later.** Not planned. A member that is not plain code would need a new decision, since the pipeline makes no model calls.
6. **Nothing is asked of the agentic-swarms project and none of its code is used.** This repository is public and has to stand by itself. The board here is built in this repo, in a shape the two could later share (rows that are never changed, addressed by a pointer). If the two are to meet, that goes through the coordinating session and is his to say.

## What it adds to the experiment

One more thing is measured on the made-up tables, because it is a claim about the design and not about any one finder: **do the members get more true links through the referee when they can read each other's proposals than when each works alone?** The kinds that should show it are the link that needs two series together and the many weak series with one hidden mover. If the board adds nothing there, it is said so.

## Consequences

- The draft plan is changed: "finders" are small members of several families; a section on the board; the swarm section rewritten; the scorecard gains the row above.
- `CLAUDE.md` carries his words under the aim.
- Considered and not done: asking him which of the two readings he meant (members as plain code here, or the other project's machinery brought in). Decision 0040 says not to ask; the first is the smaller step, is needed either way, and closes off nothing.
