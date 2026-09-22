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

## D6 · 2026-09-21 · A release verdict must clear the channel's own drift

`report.py --release` reads every upload at the same age from the weekly
snapshot series, and refuses to call a change a regression unless the drop
exceeds how much that metric moves between consecutive batches of uploads
anyway (measured on the era before the change: ~52% for day-7 views, ~11% for
watch-seconds).

**Alternatives:** compare medians directly — which, run live, ordered
reverting both `v5` and the b-roll library on one shared calendar swing; or
age-adjusted residuals, which attenuate a real 60% degradation to 11% because
a release's date and its videos' ages are perfectly collinear.

**Assumptions:** (a) the pre-change era is a fair reference for how much the
metric moves without us — it contains earlier releases, so the floor is
generous and the check errs toward missing a small regression rather than
inventing one; (b) upload cadence stays ~2/day, so batches of 8 span ~4 days
and the floor keeps meaning "a week's weather"; (c) the weekly snapshot keeps
running — without it there is no age-matched read at all.

**Revisit when:** cadence changes materially (assumption b), or any release
lands a verdict a human disagrees with. **Not yet settled:** §5 reverts on
watch-seconds *or* views, and views is 5× noisier — escalated as
`release-rule-metric-conflict`, owner's call.

## D9 · 2026-09-21 · Success is judged by typed metrics, never one number

One success metric (watch-seconds) that must improve, guardrails that must not
degrade past a stated margin, diagnostics that explain without voting, plus a
subjective comparative read at three horizons. A guardrail breach is **not**
outweighed by the success metric rising.

**Alternatives:** the single trajectory measure shipped hours earlier, which
read "flat, slightly up" while views and engagement had both halved; a
composite score, rejected because averaging hides the disagreement that *is*
the information.

**Why:** no single metric survives this channel. Avg-%-viewed was dropped as a
target because trimming inflates it; watch-seconds has the mirror flaw, rising
when videos merely get longer.

**Assumptions:**
1. The margins are right. `avg_view_pct` 5pts and `zero_rate` 3pts are guesses.
   Views deliberately has **no** margin — its ordinary swing here is 2.8x, and
   a fixed margin on it fired on weather in the first real run.
2. Watch-seconds is the right success metric — still one number carrying a lot.
3. A subjective comparative read adds signal that the numbers lag on.

**Revisit when:** a guardrail never fires, or fires every period (1 false); the
scorecard and the subjective series disagree persistently (2 or 3 false); or a
new guardrail blocks work on noise — each costs power, and ten at 80% leaves
about 11% combined.

## D8 · 2026-09-21 · PM's judgement jobs get methods, not exhortation

Generating candidate work, ranking it, evaluating a due experiment, verifying
the tracker and challenging a constraint each had one sentence. They set the
channel's direction and each is a job where a model's default behaviour is
measurably wrong, so each now has a method in `/backlog`.

*(Recorded late: this decision was written when the methods shipped and lost to
a silent assert failure in the script that was meant to append it. Rewritten
from the commit message.)*

**Why each:** generation fixates on early outputs and favours typical text, so
it draws from named evidence sources and asks for candidates *with
probabilities* (~1.6–2.1x wider range, no quality cost). Ranking suffers
self-preference, position and verbosity bias — two structural — so the fixes
are procedural: separate pass, forward and reversed, one-line statements,
dimension-wise scoring. Evaluation's remaining failure is reinterpreting a rule
once the answer is inconvenient, so the rule is quoted verbatim first and "not
yet" is a real outcome. Constraint challenge uses the five focusing steps,
which name what went wrong with Gemini: exploit and subordinate, never elevate.

**Assumptions:**
1. The techniques transfer from benchmarks to this project's few, high-stakes
   judgement calls.
2. A shift will follow a procedure slower than its intuition.

**Revisit when:** `/backlog` produces candidates that all look alike (1 false),
or `WORKLOG` shows the method skipped (2 false).

## D7 · 2026-09-21 · Slack goes to PM and research, not back to the clock

A shift whose maintenance and feature lanes are thin becomes a
PM-and-research shift, not a short one. Research has no percentage ceiling;
its output is governed by the value bar instead.

**Alternatives:** the previous rule — research capped at ~25% and unused budget
not redistributed — which contradicted itself. Capping research while also
refusing to redistribute meant a shift with an empty feature lane simply ended
with half its time unspent, which is the wasted capacity this whole workflow
exists to prevent.

**Why:** the owner's point is that there is always work — a backlog to
populate, decision rules to check, documentation to verify, questions about how
channels like this grow. A percentage cap was the wrong instrument for the real
worry, which is busywork. The value bar is the right one: a hypothesis with a
proposed test and no new documents.

**Assumptions:**
1. PM and research genuinely always have work above the value bar.
2. The value bar is strong enough to stop research becoming padding without a
   numeric cap.

**Revisit when:** `WORKLOG` shows research producing findings nobody acts on,
or shifts spending heavily on research while the backlog stays empty (2 false);
or shifts still ending early with time unspent (1 false).

## D5 · 2026-09-19 · The process rules are protected in CI, not in prose

`CLAUDE.md` and `.claude/skills/**` cannot change on `main` without an issue
the owner labelled `approved`, referenced as `Approved-In: #N`. Unapproved
changes are reverted automatically and escalated.

**Alternatives:** keep it as prose (it already was, in three places, and
nothing enforced it); require PR review (we deliberately removed that gate —
it was the bottleneck); protect via branch rules (cannot express "approved
issue exists").

**Why:** shifts are autonomous and audit their own process. Prose telling an
agent not to rewrite its own rules is advisory, and this project has learned
three times that advisory loses — the R4.6 tier guarantee moved into
`screen.py`, the Polly limit into `tts.py`, the context limit into a budget.

**Assumptions:**
1. Branch work stays unrestricted, so proposing costs nothing.
2. Reverting is safe — the change is never lost, only unlanded.
3. The owner is reachable to approve. *(Escalation email verified 2026-09-19.)*

**Revisit when:** approval becomes a bottleneck the way review did (1 or 3
failing); or a revert loses work rather than unlanding it (2 false).

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
