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

## D12 · 2026-10-05 · A media company with functions, not a channel with lanes

The owner's reframe: the company is the unit being improved, and the channel
is its first product. The goal is monetization, and the YouTube Partner
Program is only one route. Pivots are allowed when justified. `ORG.md` maps
fourteen functions. Each states what it answers for, plus responsibilities
tagged with a cadence and a decision level (Act / Propose / Owner). The six
lanes become seats feeding one ranked queue. Owner decisions on the same day:
outside evidence may justify a proposal; agents may publish beyond the upload,
under a policy; the owner will create platform accounts; PRD §7 exclusions are
challengeable; shifts get read-only AWS access.

**Alternatives:**
- **Add lanes to the time-sliced shift.** Fourteen slices of a 25-minute
  session is about two minutes each, plus a "nothing this shift" heading for
  most of them.
- **An agent "CEO" over agent workers.** Project Vend found a same-model
  manager shared the worker's blind spots, while procedures helped most.

**Why:** across 27 shifts, revenue, other platforms, competitors, viewer
comments, monetization policy and data-source terms each came up zero times.
Every lane faced the pipeline. Three risks to monetization itself went
unowned:
- the current format matches an example in YouTube's reused-content policy;
- Reddit's free API may not cover monetized use;
- Shorts revenue at the Partner Program threshold is about $30–$330 a month.

**Assumptions:**
1. One agent session can hold several seats if the queue ranks across them.
2. Written procedures per function deliver the depth that hierarchy would not.
3. Weekly, monthly and quarterly sessions fit the owner's usage reserve and the
   Actions minutes.
4. Outside evidence improves proposals more than it adds noise.

**Revisit when:** a function stays at "none" after its first monthly cycle
(1 or 2 false); proposals from outside evidence are mostly declined or pile up
unanswered (4 false); or the cadences push shifts past the reserve (3 false).

## D11 · 2026-09-25 · Supply is ready work, with a floor the system refills

A shift's supply is backlog items whose next step can be taken **now**
(`scripts/backlog_status.py`). Below 3 `ready`, generating and ranking more is
the PM lane's first job; research questions answerable from existing data are
the source that never runs dry. The unused-capacity alarm reads minutes from
the usage ledger, and every shift report states minutes used and ready work left.

**Alternatives:** seeding problems by hand when shifts run short (done once,
and correctly called a bandaid); forcing a second agent turn onto leftover time
(mechanical, but spends quota whether or not anything is worth doing).

**Why:** generation triggered on "the feature lane is empty", and blocked items
kept it from ever looking empty; the alarm compared self-reported percentages,
which always add up, so two short shifts went unflagged. With one experiment
live at a time and each baking ~2 weeks, a waiting feature lane is the normal
state, not the exception.

**Assumptions:**
1. Generation keeps finding work above the bar — research questions especially.
2. Shifts keep Status values true. A test fails a push on an unknown status or a
   row cut off from its table; truthfulness itself is the audit's to check.
3. A floor of 3 fills a 25-minute shift.

**Revisit when:** the alarm fires with ready work at or above the floor (3
false, or shifts stop with work available); ready items pile up undone (1 is
producing padding); generation keeps reporting nothing above the bar (1 false —
itself a finding about the channel).

**Re-reviewed 2026-10-05:** assumption 3 changed with the shift. Shifts went
from 25 to 60 minutes, three a day (D12, approved in #54), so the floor rose to 5.

**Re-reviewed 2026-10-06:** assumption 1 holds only in part. Generation found
two research questions above the bar (PRD R4, R5), but each was answered within
the shift, so the ready count stayed at 0 against the floor of 5. Research
refills a shift's time, not the floor. While the owner's planning session (#55)
is pending, the floor measures that wait, not the shift. Not yet a trigger: one
day.

**Re-reviewed 2026-10-09 (audit) — trigger fired.** Assumption 1 is false while
the owner's queue is this long. Three shifts in a row handed over 30–40 minutes
early with 0 ready against 5, and #67 has been raised three times. The binding
limit is the owner's hands, not generation. Every escalation since 09-25 that a
label could answer was answered, most within a day (12 of 12). All 8 still open
ask for a session, a login, a script, a key or a hand edit. D11 stands, because
the floor makes that wait visible, which is its job. The response is to shape
asks as labels (#70 splits bet 1 out of #55). Revisit if shifts still end early
once #70 is answered.

## D10 · 2026-09-25 · No new spending until the channel earns money

The owner's ruling, when asked to let sample videos cost ~$1.80/month more:
*"spending money is not on the table until the channel is actually earning
money somehow, but pretty much anything else is on the table - as such you may
need to get creative."* PRD §5 no. 1 moves from 🔄 to 🔒.

**Alternatives:** judging each small spend on its merits, which is how the
question arose — a dollar or two for faster shipping is easy to justify alone,
and the sum of such justifications is the bill.

**Why:** the channel earns nothing, so every cost is a pure loss until it does.
The ruling is not "work around this once"; it redirects effort. A constraint
that cannot be bought away has to be designed away, and that is what the PM and
research lanes are for.

**Assumptions:**
1. The channel does not yet earn revenue.
2. Creative, free routes exist for the constraints that matter (the first test:
   PRD §0, "Make sample videos free").

**Revisit when:** the channel earns money (1 false) — then spending proposals
reopen, sized against revenue.

**Re-reviewed 2026-10-06:** assumption 1 still holds (revenue $0). The drafted
bets (#55) each ask for a little Polly spend: bet 1 about 6 cents a month, bet 2
1–2 cents per extra upload. The packet asks for it explicitly, so the owner's
answer there re-decides this ruling for those items. No shift may read it as
lifted until then.

**Re-reviewed 2026-10-08:** still holds. The owner declined Gemini's paid tier,
asked for so Reddit posts stop reaching a free tier that trains on them (#62):
*"Not approved to spend money on this, find another solution."*

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
lands a verdict a human disagrees with. **Settled 2026-09-24:** the owner chose
watch-seconds only (#18, `b303b37`); views never trigger a revert.

**Re-reviewed 2026-10-06:** still holds at 2 uploads a day. Bet 2's volume step
(PRD #4, 3–4 a day) would break (b): batches of 8 would span two days, not
four. Any release judged during it needs its floor re-measured on uploads at
the new cadence, not borrowed from the 2-a-day era.

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

**Re-reviewed 2026-10-09 (audit):** 2 is under strain, not false. `v7`'s lead
was mostly length (PRD §4, 10-07), patched by the total-watch-time check (#39),
and the revenue bar counts engaged views (PLAN §1). The 12 October engaged-share
read (§0 #8) is the evidence; re-review then. The 3-point `zero_rate` margin
breaches today on 2.4% → 5.6% (n=42 vs 36), which the scorecard itself calls
weather at this size.

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

**Re-reviewed 2026-09-25 — trigger fired.** Two shifts ended early with time
unspent (8 of ~25 minutes on 09-24, 7 on 09-25), the second despite being told
its exact deadline. Assumption 1 is under strain rather than false: both shifts
did real work, then judged every lane done. The limiter was upstream — shipping
waits on rationed sample videos — and D10 makes such constraints PM and
research problems. The first response -- seeding the sample-video ration as PM's top item -- the
owner called a bandaid the same evening: it refills the queue once. The
durable response is D11.

**Re-reviewed 2026-10-06:** the trigger's shape for 2 appeared: about a third
of a shift went on research while the ready count stayed at 0. It was not
padding. Both questions (PRD R4, R5) had decision rules fixed before the data
and tied to bet 2, and both were answered. If the next shifts' research again
changes no rule, 2 is false.

**Re-reviewed 2026-10-09 (audit):** 1 is false for now, for the reason under D11:
the work above the bar waits on the owner's hands. 2 holds. This shift's research
(commentary drafts, PRD §4) changed a proposal (#70) rather than padding.

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

**Re-reviewed 2026-10-06:** 3 holds; the owner approved #52 and #54 within a
day. The weak link is the apply step after approval. Of the last three
approved patches, #52 landed, #53 was lost to GitHub's 5 October outage, and
#50's could not be read. Each failure costs the owner another round trip.

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

**Re-reviewed 2026-10-09 (audit):** assumption 1 is false for `WORKLOG.md`. Its
word budget (2,600) binds at **2** entries, so the 10-entry cap never binds, and
the audit reads older entries from git. The budget also costs churn: about ten
trim commits across 8 shifts, and 15 log commits in one. The header now says
the word budget decides. 3 is strained for `TECH_DEBT.md`: 24 of 25, and its
largest item runs past 500 words, so items grow rather than count. Shorter
entries would come from the template, which is what the owner reads. Left as is.

## D3 · 2026-09-19 · Full allocation across workstreams each shift — **SUPERSEDED by D12**

Per-lane time slices each shift; replaced by one ranked queue (re-reviewed 2026-10-06). Full text in git history.

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
