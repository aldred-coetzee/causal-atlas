# causal-atlas: test framework proposal

Written 2026-11-06 for the owner's decision. Nothing here is built until he has seen it.

## The short answer

You were right to question this. We have been circling, though not for the reason I told you. I said we may have been failing a test nothing can pass. Today's measurement does not support that, and I withdraw it.

We kept trying new instruments on one question without ever measuring what was possible. When I measured that today, two things came out:

- **The fake worlds are not empty.** Told the exact link, our real baseline improves in most worlds.
- **Our screen is close to deaf.** Handed the exact answer as an input, it hears it in only 3 to 6 of 20 worlds. The strongest suspect is one setting of ours, a cap on counts.

Without a way to tell those two apart, every miss looked the same. A framework fixes that first.

**My recommendation: build it in small stages, and pause the rest of the current plan until a method has passed the first stages.**

## What we have tested, and whether it was the right test

| What we tried | Question | Result |
|---|---|---|
| First detector | Finds a planted link in 48 held-out months? | Missed. Afterwards we found the bar could not be met by any method in that window. |
| Refit forecaster | Beats the baseline when refitted over time? | Missed, with a crash and a baseline 143 times too high in one world, so we rebuilt the score. |
| R1: forecaster handed the right inputs | Can it hear the link at all? | 9 of 20 worlds over 8 years, 16 of 20 over 20 years. |
| R2: the screen, not told which input | Names the true input among many? | 1 to 5 of 20, 16 needed. False alarms fixed along the way, from 9 to 11 of 15 down to 0 or 1. |
| Ceiling check, today | Is it the world or the instrument? | Mostly the instrument. Most worlds hold something, two hold very little. Numbers below. |

**What was right, and stays:**
- writing the rule down before the numbers
- scoring on months the method has not seen
- worlds with no link, as a check on false alarms
- shifting the inputs by whole years as a fair comparison

These are what caught the errors, including a gate that went off on pure noise.

**What was wrong or missing:**
1. **No ruler for what was possible.** Each mark was set without knowing whether anything could reach it. R2 asked for 16 of 20, and even with the exact link in hand the baseline clears that same bar in only 11. That does not prove the bar is out of reach, but nobody had checked.
2. **No check on the instrument.** We never handed a method the answer to see if it could hear it. One run of that exposed the cap's cost. It had passed plan review, the audit and me.
3. **A narrow question.** Every world has 2 real inputs and one outcome, and the decoys are independent noise. The current methods have never run on a combination world. Nothing tests many related data sets, which is your actual aim.
4. **Forecasting as the only judge.** You asked to discover relationships and contributing factors. We have mostly scored forecast gain, so every fault in the baseline became a fault in the test. Much of the spend went on fixing that yardstick.
5. **The worlds never changed, while the score, marks and limits did**, several times in two days. Each change was disclosed, but that is the circling you sensed.

## Today's measurement

Same 35 worlds as R2, already seen, 8 years. Counts are rough.

| Given the exact link | Planted worlds, of 20 | Worlds with no link, of 15 |
|---|---|---|
| Real baseline: clears R2's bar | 11 (16 at the older bar of 0.02) | 0 |
| Screen as built | 6, 6, 3 (by form) | 0, 0, 1 |
| Screen with no cap on counts | 14, 12, 19 | 0, 0, 0 |

Limits on this:
- The exact link knows where and how the link works, and inputs later than a method may see. It leaves out the link's knock-on effects. So it is a strong reference, not a strict upper limit.
- By the reading table fixed beforehand, the baseline's 11 is mixed, with no verdict. Of the 9 misses, 7 show a real gain and fail on other conditions, and 2 are near nothing. The screen's 6, 6, 3 falls in the "cannot hear" band.
- The no-cap row comes from handing over the exact answer. It does not show the screen would find a real input among many, and that is untested.
- The cap removed 30% of events in the one world I looked inside, from 0.03% of its cell-months. It is the strongest suspect, not a proven cause.
- My first attempt at this check was invalid because of a bug of mine. It is recorded in `results/r2-ceiling.md`.
- The fresh reader who pushed for this measured it too, and its version flattered the worlds. The figures above are the fairer ones.

## The framework

**1. A ladder of fake worlds, each with a no-link twin.** Each rung adds one difficulty:
- **Toy:** smooth numbers and a simple lagged link. Any sane method must pass.
- **Today's count world.**
- **Many related inputs:** decoys that resemble the true inputs, as real data does.
- **Combinations only:** a link that exists only when two or three inputs act together.
- **A different kind of outcome:** a price or an index, not counts.
- **A link that switches on or off** partway through.

Difficulty is set by how much the exact link is worth in the months scored.

**2. One way in for every method.** It takes the data and returns a ranked list of claims: which input, what lag, where, with what partners, how strongly. It may also give a forecast. So today's screen, a no-cap screen and any later method face the same test.

**3. One scorecard, with the ceiling on every row.**
- **Relationships found**, checked against what was planted, with combinations on their own line.
- **Forecast gain** over the baseline, on unseen months.
- **False alarms**, with an interval, and runtime.
- Results read as "of the worlds where there was something to find, how many did it find". A miss counts against a method only if the ceiling shows something was there.

**4. Tests of the test, run before any method's score counts.**
- On pure noise, it goes off at the stated rate.
- Handed the exact answer, it fires. If not, the method is broken and no world is blamed.
- The baseline's level stays sane on no-link worlds.
- Marks are set against the ceiling and written down first.
- Enough worlds that a count means something, and a ledger of used seeds.

**5. Real data with known answers.** Links science already accepts, with the same series shifted by whole years as the control. From memory and unchecked, to be confirmed at source first: El Niño to rainfall in East and Southern Africa, rainfall to vegetation, drought to staple food prices. A method that cannot find these should not be believed on conflict.

**Left out for now:** maps and web pages, new domains, and any claim about cause or prevention. Other published methods come in only as plug-ins. The current 48-month held-out window will not decide anything, since it can hold nothing even when the link is large.

## Stages and cost

These are estimates, and my estimates here have run low. Phase 1 stands at about 6.4M of 20M.

| Stage | What | Tokens | What it answers |
|---|---|---|---|
| 1 | The harness, the toy and count rungs, tests of the test, today's screen with and without the cap as the first plug-ins | 1M to 2M | Can a blind search find a real input among many, once the instrument hears? |
| 2 | Related inputs and combination rungs, and a method that searches for combinations | 2M to 4M | Can we find what nobody thought to look for? This is your aim. |
| 3 | Real data with known answers | 1M to 2M | Does it work outside our own worlds? |

That is 4M to 8M in all, over weeks, with a report at each stage.

**What would change direction:**
- **Stage 1:** if nothing searching blind can get close to the ceiling on the count world after a few honest methods, I'd say so and stop before Stage 2.
- **Stage 3:** if a well-established real link adds almost nothing over a place's own history, finding relationships becomes the main product and forecasting the side one.

## Decisions for you

1. **Build this in stages?** I recommend yes, starting with Stage 1.
2. **What leads, relationships or forecasts?** I recommend relationships found on the fake worlds, since those are your words. Forecast gain stays as a second check, and the existing rule stays for real data: nothing is called a finding unless it beats the baseline on unseen months.
3. **Pause the current plan's next steps** (the R3 test, the mark and the conflict data) until a method passes Stage 1? I recommend yes. This changes the plan, so it is yours to decide.
4. **Anything you would add or cut on the ladder?** You know what you are hoping to find. I would especially like your view on the combinations rung, and whether the real-data stage should come sooner.
