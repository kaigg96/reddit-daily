---
name: backlog
description: How the company decides what to work on next — generating candidate work, prioritising the one queue, evaluating an experiment whose decision rule has come due, and challenging a constraint that costs more than it buys. Load when fewer than 3 items are ready (scripts/backlog_status.py), when ranking the queue, when a rule comes due, or when a constraint keeps forcing workarounds.
---

# Decide what to work on next

Three jobs shape the channel's direction, and each fails differently. They are
here rather than in `/shift` because they are methods, used when the work comes
up, not rules to carry every shift.

**One rule spans all three.** This channel has twice killed a plausible,
confident, wrong idea with its own data — R1.8/R1.9 and the b-roll retention
claim (`PRD.md` §4). Anything produced here is a **candidate**, not a finding.
It earns its place by surviving contact with `scripts/report.py`, not by
sounding right.

---

## 1. Generating candidates

The failure mode is measured, not hypothetical: language models **fixate** —
early outputs constrain later ones — and **favour typical text**, so asking
for ideas yields a handful of obvious, homogeneous ones. Left alone this lane
proposes the same safe list every time.

**Supply that never runs dry: research questions.** Anything the channel's own
data can answer is ready work — no sample video, no spend, no waiting on an
experiment. Add it to §0's research table with the test that answers it, then
run the test; the result becomes a finding (§4), a new question, or a backlog
item — and **the row leaves the table**, so it can never grow into a second
backlog. When the ready floor forces generation, fill it with these first: a
wrong one costs minutes, where a weak build idea costs a change.
#9 (loop the ending) is the model: tested and dropped in minutes. With one
experiment live at a time and each baking ~2 weeks, the feature lane is waiting
more often than not — this is what shifts do meanwhile.

**Draw from evidence, not from imagination.** Before generating, read at least
three of these, and say which you used:

- **The trajectory** — `scripts/report.py --trajectory`, first. If it says
  FLAT, the last few things we shipped did not work, and repeating that shape
  of idea is the mistake. Read *what we tried* in `PRD.md` §0 before proposing.
- **Failures** — `scripts/report.py --zeros`. What do the suppressed and
  zero-view uploads have in common?
- **The spread** — `--by topic`, `--by title_style`, `--by background_type`.
  Where is the variance, and what would exploit it?
- **The audience** — comments on our own uploads. The only direct signal we get.
- **Distribution** — `analysis/traffic_sources.csv`. Where views actually come
  from, which killed the SEO work once already.
- **Constraints** — anything in §3 below that is forcing workarounds.
- **The company** — `PLAN.md`: the revenue routes, and any risk in §4 with no
  item answering it. Candidates need not be product work: a price, a policy
  read, a platform, a proposal to the owner.
- **The gap** — decision rules in `PRD.md` §0 that cannot be answered yet, and
  what would make them answerable.

**Then generate divergently, and only then converge.** Keep the two apart; a
constraint applied during ideation is what collapses it to the obvious:

> Generate 8 candidate work items, each with an estimated probability that it
> is the highest-leverage thing we could do next. Include low-probability ones.

Asking for **explicit probabilities across a set** ("verbalized sampling")
measurably widens the range versus asking for a list — roughly 1.6–2.1× on
published benchmarks, without costing quality, and the gain is larger on
stronger models. Aim for spread: if all eight are the same shape, the sources
above were not actually consulted.

**Only now apply the filters.** Discard anything that contradicts a finding in
§4, costs more than its constraint allows, or cannot be measured by an existing
decision rule. Surviving candidates go to §2.

## 2. Prioritising

The failure mode here is that **the shift both generates and ranks**, and
models systematically favour their own output. Three biases are documented and
two are structural, so prompting alone will not fix them:

- **Self-preference** — a property of the judge, not the prompt. Mitigate by
  ranking in a **separate pass** with the candidates stripped of any note of
  who proposed them or in what order they arose.
- **Position bias** — order sensitivity that a rubric cannot reach. Mitigate by
  **scoring the list, then scoring it reversed**, and keeping only the items
  that rank well both ways.
- **Verbosity bias** — longer reads as better. Mitigate by scoring a **one-line
  statement** of each candidate, not its argument.

**Score each dimension separately before any overall judgement** — decomposing
a holistic call into dimension-wise ones roughly halves error against human
judgement. Dimensions, in this project's terms:

| | |
|---|---|
| **Effect on the path to revenue** | The company's goal (`PLAN.md` §1, D12). Scored first, for every candidate, product or not. |
| **Effect on watch-seconds** | The product's primary metric (`PRD.md` §4), for product candidates. Views are noisy — 27–50% at fixed age. |
| **Evidence** | Measured on *our* channel / measured elsewhere / reasoned. |
| **Cost** | Gemini requests, Polly characters, Actions minutes, shift time. |
| **Reversibility** | One `FORMAT_VERSION` bump, or something that cannot be undone. |
| **Blocked?** | Gated on uploads accumulating is not a reason to rank it high now. |

Rank on the dimensions, not on enthusiasm. Then write the top item into
`PRD.md` §0 (product) or `PLAN.md` §3 (everything else) **with its decision
rule, or its done-when, already stated** — an item
without one cannot be evaluated later, which is how an experiment becomes
permanent by default.

## 3. Challenging a constraint

`PRD.md` §5 marks each constraint 🔒 inviolable or 🔄 open to challenge. For a
🔄 one, use the five focusing steps — the standard treatment for a system
bottleneck:

1. **Identify** — which constraint is actually limiting throughput? Not the
   loudest one; the one whose removal would change what we can do.
2. **Exploit** — get more from it without changing it. *Merging three Gemini
   prompts into one was this.*
3. **Subordinate** — make everything else serve it. *Per-consumer request caps
   and timing shifts around the reset were this.*
4. **Elevate** — change the constraint itself. A paid tier, a different model,
   a different host.
5. **Repeat** — the constraint moves; find the next one.

**We stopped at step 3 and called it solved.** Every Gemini workaround was
exploit-or-subordinate, each correct on its own, and together they removed the
pressure that would have prompted step 4. That is the failure this section
exists to prevent: **steps 2 and 3 make a constraint survivable, which is how
it becomes permanent.**

**The trigger is measurable, not a feeling.** Elevate is due when *either*:

- one 🔄 constraint has forced **three or more** workarounds across shifts
  (`WORKLOG.md`, `TECH_DEBT.md`), or
- it has begun blocking planned work — a backlog item priced out by it is the
  clearest possible signal.

Then escalate with evidence, a concrete alternative, and its cost. **Elevating
is the owner's call; noticing that it is due is not.**

## 4. Evaluating an experiment whose rule has come due

This is the job this project has got wrong most often. Four conclusions reached
a decision in two weeks and all four were wrong (`TECH_DEBT.md` Pass 2): a
length thesis that nearly shipped two features, a b-roll effect that was pure
age artifact, a retention claim later retracted, and an alert with twelve false
positives. The tooling was then built to make those specific errors impossible
— age-matching, watch-seconds as primary, cohort floors, zero-view separation.
**`scripts/report.py` is not advice; it is the accumulated corrections.**

What the tooling cannot stop is the remaining failure: **reinterpreting the
rule once the answer is inconvenient.** A pre-committed rule only controls
error if it is applied as written, so:

1. **Quote the rule first, before looking at any number.** Copy it from
   `PRD.md` §0 into the `WORKLOG` entry verbatim. A rule you have to
   paraphrase after seeing the data is no longer a pre-commitment.
2. **Check the cohort qualifies before reading the verdict.** `report.py`
   refuses thin or age-mismatched comparisons; that refusal is the answer, not
   an obstacle to route around with a different cut of the data.
3. **Apply it exactly, and accept the result.** Keep or revert as written.
4. **"Not yet" is a third outcome** and the commonest one. A cohort too small
   to decide is not evidence of no effect, and it is not licence to substitute
   an easier test.

**Anything else you notice in the data is exploratory.** It may be true and it
is not a verdict — it went looking after the fact, which is how the length
thesis happened. Exploratory findings become **candidates in §1**, each needing
its own pre-committed rule before it can ever be acted on. Never act on one in
the shift that found it.

Record the verdict against the rule in `PRD.md` §0 so the next shift cannot
re-litigate it, and say plainly which outcome it was: kept, reverted, or not
yet.

## 5. Checking the tracker is true

```sh
venv/bin/python scripts/check_docs.py
```

Stale claims mislead worse than missing ones, because they are read with
confidence — a shift once lost its feature time to a blocker that had been
cleared ten days earlier, because two places disagreed. The checkable claims
are checked mechanically: live format against the code, branches described as
pending that have merged, cohort sizes quoted as current, and issues described
as open that are closed.

**Spend judgement on what it cannot check**: whether §0's priorities are still
right, whether a finding in §4 still holds, and whether a decision in
`DECISIONS.md` rests on an assumption that has quietly become false.
