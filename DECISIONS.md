# Decisions

Process and architecture decisions, with **the assumptions they rest on**.

Not read every shift — the project-management lane and `/audit` read it. The
point is not a record for its own sake; it is that a decision stops being right
when an assumption underneath it stops being true, and nothing notices unless
the assumptions were written down. That happened on day one: the choice of a
priority queue over allocation rested on "usage isn't readable", which became
false two hours later, and the decision stood unexamined anyway.

**Reviewing one:** for each assumption, ask *is this still true?* If any is
false, the decision is due for re-litigation — not necessarily reversal.
Record the re-review inline with a date, including "still holds".

Product and experiment decisions live in `PRD.md` §4 Findings, not here.

Keep entries short. One decision, the alternatives, the assumptions, the
revisit trigger.

**Retention — this file must not grow forever** (cap: 15 entries, checked by
`scripts/context_budget.py`):

- **Superseded decisions compress to one line** — title, date, "superseded by
  Dn" — unless kept deliberately as a worked example, as D1 is.
- **A decision confirmed stable across three audits graduates.** Fold it into
  the rules it implies (`CLAUDE.md`, a skill) and leave a one-line stub here.
  A decision record is for things still live enough to be worth revisiting; a
  settled one belongs in the rules, where it is actually read.
- Past the cap, **resolve before adding**.

---

## D4 · 2026-09-19 · Retention caps on the append-only docs

`WORKLOG.md` 10 entries, `DECISIONS.md` 15, `TECH_DEBT.md` 25 open items,
counted by `scripts/context_budget.py`. Past a cap, close before adding.

**Alternatives:** rely on judgment during audits (the status quo, and it was
already failing — tech debt hit 24 of 25 in one session with nothing watching);
or word budgets like the loaded docs (wrong unit — the problem is too many open
*things*, not too many words).

**Assumptions:**
1. These numbers are roughly right. They are **guesses**, not measurements.
2. Things genuinely can close — items are fixable, decisions do settle.
3. Counting items is a good proxy for whether a doc is still readable.

**Revisit when:** a cap blocks work that should have happened (1 too low); a
doc becomes unmaintainable while still under cap (1 too high, or 3 false); or
items get closed by deletion-without-reasoning to stay under (2 false — the
cap is then producing dishonesty rather than hygiene).

## D3 · 2026-09-19 · Full allocation across workstreams each shift

Every shift allocates across all lanes rather than spending itself on one.

**Alternatives:** one lane per shift (cheapest, but starves lanes); parallel
subagents (avoids the context-switch cost, far more machinery).

**Why:** at this size no lane has a shift's worth of high-value work — of six
experiment-backlog items only one is actionable, and seven decision rules are
gated on uploads accumulating rather than on effort. A large uninterrupted
allocation to one stream invites filling it, and this project's real failures
(R1.8/R1.9, the b-roll retention claim, a taxonomy fitted to n=1) were all
capacity being filled, never capacity running out.

**Assumptions:**
1. No single lane holds a shift's worth of genuinely valuable work.
2. The ~1.3–1.6x context-switching cost is acceptable at this scale.
3. Slices behave as ceilings, not quotas — shifts end early rather than pad.

**Revisit when:** a lane repeatedly cannot fit its valuable work in its slice
(1 false); or usage becomes the binding constraint on progress (2 false); or
`WORKLOG` shows slices being filled rather than finished (3 false).

## D2 · 2026-09-19 · Autonomy bounded by guardrails, not by review

Shifts merge to `main` themselves, including live-path changes. Owner review is
replaced by automated gates plus auto-revert. Weakening a safety or cost
control, spending, rewriting production data and publishing still escalate.

**Alternatives:** owner reviews every merge (the previous rule — it had become
the bottleneck, with one branch waiting 8 days while six stacked behind it).

**Assumptions:**
1. The gates catch what review would have: tests, a dry run producing a
   playable MP4, `FORMAT_VERSION` discipline, one variable per release.
2. Auto-revert actually fires — something is watching released changes.
3. Escalations reach the owner. *(Verified 2026-09-19: email confirmed.)*

**Revisit when:** anything reaches `main` the gates should have stopped (1);
a bad release survives more than a few days (2); or the escalation rate looks
wrong in either direction — trivia means too tight, silence means shifts are
deciding what they shouldn't (3).

## D1 · 2026-09-19 · Priority queue over allocation — **SUPERSEDED by D3**

Kept as the worked example of why this file exists.

**Why it was chosen:** primarily that remaining plan usage could not be read
programmatically, making allocation brittle; secondarily that a queue degrades
gracefully when a session ends mid-task.

**What went wrong:** the primary assumption was false within two hours — the
statusLine payload exposes `rate_limits.five_hour` and `.seven_day`. The
decision was never revisited, and it took the owner asking "why did you choose
this?" to surface it. The secondary reason survived and now shapes D3's ceiling
rule; the primary did not.

**The lesson this file encodes:** record the assumption, not just the
conclusion. A conclusion cannot tell you when it has expired.
