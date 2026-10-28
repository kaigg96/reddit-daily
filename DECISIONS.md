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

## D15 · 2026-10-27 · Every finished item logs its hardest part, read weekly, judged by a rule set now

The owner, in session (2026-10-27): shifts struggle to find engineering work,
and progress stalls without the owner. Shifts did write "Friction:" notes in
the work log, about 18 distinct ones from 09-25 to 10-07, several recurring
(the render allowance on 3 days; answered questions re-asked on 3 shifts;
plans written after starting on 3). From 10-08, none: the log is the owner's
email, with no slot for them, a word budget, and its oldest entries deleted,
so no one could count a recurrence.

**Decision.** Every finished item (a merge, an answered question, an
escalation, a candidate dropped, an attempt abandoned) logs one row in
`.github/friction.csv`: its function, outcome, category from a fixed list, the
hardest part, what would have helped, and minutes lost. "None" is a valid
answer; an invented one is worse. The weekly review groups the rows, queues
the groups with most leverage (recurrence × minutes × functions hit, against
cost) in the one ranked queue, and records each resolution. Any function may
fix another's friction. General management owns it. Built as `PLAN.md` C17;
the spec is `scripts/friction.py`'s docstring (live 2026-10-27, #84).

**Alternatives.** Notes in the work log (tried; stopped unnoticed). One entry
per shift (gets summarized away). A ticketing system (premature; GitHub issues
are the step up past ~100 open groups).

**Assumptions.** Agents can name what slowed them, though not friction they
do not notice (re-deriving recorded state feels like ordinary work). Ranked in
the one queue, friction fixes will not crowd out bets (guardrail g). Logging
costs about a minute an item.

**Decision rule** (pre-committed 2026-10-27, before any row; START is the day
`scripts/friction.py` lands; quote this before any number):
- *Collection*, daily (`context_budget.py --health`) and at the first weekly
  review after START: (a) 80%+ of shifts log a row, and three silent shifts in
  a row escalate to the owner; (b) "none" is 5–80% of rows; (c) of 10 random
  rows, most name a specific doc, tool, rule or allowance.
- *Processing*, each weekly review: (d) no row older than 7 days ungrouped.
- *Results*, at the first monthly review 28+ days after START: (e) 2+ groups
  fixed by a shipped change; (f) 1+ group with 3+ rows before its fix logs at
  most 1 row in the 14 days after. Minutes lost is reported, never decisive.
- *Guardrails*, every read: (g) rows that fix a group are at most a third of
  the window's rows; (h) a week's processing takes about 20 minutes at most.
- **Keep** if all pass. **Change** if any fail: (a)–(c) point at how rows are
  written, (d)–(f) with (a)–(c) passing at how they are processed. **Stop** if
  (e)–(f) still fail at the monthly read after one change: remove the rule and
  the check, keep the data. **Not yet** under 28 days, or with no fix 14 days
  old. A guardrail trip caps friction work at one item a shift until the next
  read. Keep needs nothing from the owner; change and stop are process changes
  (`CLAUDE.md` §4).
- The thresholds are first guesses. A read may change one only for the next
  read, recorded here, never to rescue its own verdict.

**Generalized** (same session): every standing process needs an outcome
recorded each time it runs, a scheduled read, and a keep/change/stop rule set
in advance; `/audit` checks for all three. The experiment process has none of
them yet (`PLAN.md` C18).

**Revisit:** at the rule's read, and at each `/audit`.
**Re-reviewed 2026-10-28 (audit):** holds: all four shifts since it went live logged their rows, about 40% "none"; the rest untestable until the 11-24 read.

---

## D14 · 2026-10-19 · Audience first; the owner gives a viewer's feedback, shifts own the craft

The owner, in a session on 10-19 (recorded on #77): the likely first step to
money is an audience, which opens routes beyond YouTube views. Meeting
YouTube's monetization rules (reused content, our own words' share) is worth
pursuing but is **not the deciding test** for a format today; the owner doubts
YouTube checks a channel this size. So a format change is judged first on
whether a first-time viewer follows it and keeps watching; own-words share is
reported, never a gate. Separate: the spam policy (#80) risks strikes and
termination, not pay, and binds at any size.
Same session, on weak host tags: "I gave you the feedback, this is your (or
rather, the shifts) job to figure out what constitutes good reactions, how to
generate, test, etc." The owner reacts as a viewer; defining the bar, building
and testing are the shifts'. Bring back a result to watch, not a craft choice.
**Alternatives:** keep YouTube's rules as bet 1's done-when (the owner
declined it as a gate). **Assumptions:** (1) monetization review comes only
when we apply; (2) audience is the binding step (21 subscribers, §1).
**Revisit** before applying to any paid programme, or at 1,000 subscribers.
**Re-reviewed 2026-10-25 (audit):** holds; (2) unchanged (21 subscribers). Stale beside it: D9's and D10's 10-13 lines call YouTube's review bet 1's real gate, which D14 declined; PLAN §1 still rates Audience "none" (11-05 monthly).
**Re-reviewed 2026-10-28 (audit):** holds: 22 subscribers, engaged views ~757× short; (1) untestable, as nothing has been applied for.

## D13 · 2026-10-11 · Short shifts are the shift's to fix; what reaches the owner is one label

The owner on #67, after the unused-time alarm emailed them three times:
diagnosing and fixing it is the shifts' job, not the board's. The cause: the
queue was empty because its rows waited on the owner, and only asks needing
their hands or a session waited. So the alarm no longer escalates; it prints
at shift start with the rows waiting on the owner, and the shift reduces each
to one label before generating (bet 2 became #72 the same night).
**Alternatives:** fewer or shorter shifts (hides the cause); keep escalating
(the owner declined). **Assumptions:** (1) label-only asks close within a day
(12 of 12 since 09-25; #70 the same day; #72 in 11 minutes); (2) the hands-only remainder (keys,
logins, a listen) is small. **Revisit** if a label-only ask waits over three
days, or shifts still run short with no row waiting on the owner.
**Re-reviewed 2026-10-11 — trigger fired.** #53's re-label waited six days;
it is now withdrawn (it said the repo was private), so (1) is strained, not
yet false. (2) holds only loosely: #50, #65 and #59 need hands, the oldest six
days, and #50 is the root, since applying it makes #65 and any later skill
change label-only. So the handover leads with #50's four commands.
**Re-reviewed 2026-10-13 (audit):** (1) false for now: #74 and #75 have waited ~2 days, the owner's last close was 10-11, and #74 needs a watch, not only a label. The trigger fires 10-14 10:49. **Evidence for whoever reads it (10-13 night):** the owner's labels, closes and comments since 09-20 fall on 15 of 24 days, with gaps of up to 76 hours (10-01 to 10-05); the current gap began 10-11 21:17, when #74 still said "after Monday's read" and #75 did not exist. A three-day wait is inside their rhythm, so check whether the ask's form is the cause before changing it.
**Re-reviewed 2026-10-14 15:55 — trigger fired; the form is not the cause.** #74 has waited 3.2 days, but nothing of the owner's has moved since 10-11 21:17 (67 hours, inside their 76-hour longest gap): #75, a plain label, waits just as long. So it is absence, not the ask's shape; no re-ask (#74 was re-raised twice on 10-13). Revisit after 10-15 01:17, when the gap passes their longest; even then, change the ask only if they act on other issues while #74 sits.
**Re-reviewed 2026-10-17 21:42 (audit) — that condition was met, unnoticed.** On 10-15 01:26 the owner labelled #75 three hours after #77 opened, and passed over #77. Its body then said a label approved a rebuild and #74's label would ship it; a later comment said one label on #77 ships it. A re-raise only comments (`escalations.yml`), so the body, read first, went stale, and a label on it was ambiguous consent to go live. Rewritten as one ask (no email). The owner has been absent since; the 76-hour gap passes 10-18 05:26. (1) false for now, whatever the ask's form: #75, a plain label, waited three days too; #74 six, #77 three.
**Re-reviewed 2026-10-21 (audit) — (1) holds again.** The owner answered #81, a label, the day it opened (10-20), and gave #77 a session on 10-19 (D14). #77 now waits on hands, a narrated render only their machine can make (branch code never holds the Polly keys); #80, a label, is due by 11-01. Ten shifts ran 2–56 of 60 minutes (mean 38) with nothing ready: the hands-only remainder, not absence, is the cause. 10-17's "absent" line went stale and seeded a ship-unless-they-object candidate this shift; a stale assumption steers generation.
**Re-reviewed 2026-10-25 (audit) — trigger fired; absence, not hands.** #77 has been a label since 10-25 08:33 (the stand-in voice took the render off the owner's machine, 10-23), so 10-21's "hands" cause is gone. But #80, a label, has waited 5.6 days, and nothing of the owner's has moved since 10-20 21:12 (~4.5 days, past their 76-hour longest gap). (1) is false for now; no re-ask, since re-raising to an absent owner only adds email. #77's title and body asked for a local render after the ask became a label; both rewritten 10-25 (an edit sends no email). Nine shifts ran 26–43 of 60 minutes, every one with nothing ready.
**Re-reviewed 2026-10-28 17:15 — trigger fired; not absence: the owner settles what they can read.** #77 has been one label for 3.4 days, #80 for nine. On 10-27 the owner labelled #84 and #85, process wording, 7 and 12 hours after each opened, and passed over both. So (1) holds for asks settled by reading and fails for the two needing a judgement on direction (#80) or a watch (#77: a 10 MB download from the build page; its frames are in the comment). No re-ask: #77 was re-raised the day before. Its download expires 11-08; if #77 is open on 11-07, a shift renders a fresh sample rather than leave a dead link.

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
**Re-reviewed 2026-10-13 (audit):** holds. Market and Monetization did their first work (10-13); Audience is still none, blocked on #75, so a finding at the 11-05 monthly.
**Re-reviewed 2026-10-25 (audit):** holds. Stale beside it: the coverage table (PLAN §1, last set 10-05) still rates Audience "none" though D14 made audience the binding step; distribution and finance had no time in 20 shifts (`--allocation`). Both for the 11-05 monthly.
**Re-reviewed 2026-10-28 (audit):** (1) and (3) hold; (2) waits on the 11-05 monthly (audience, monetization and market still "none"); (4) strained: asks resting on outside evidence wait longest (#80 nine days, #82 seven).

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
**Re-reviewed 2026-10-13 (audit) — trigger fired:** after #70 closed, two shifts ran 26 and 25 of 60 minutes (shift-usage.csv); both ready items wait on #74. Carried by D13.
**Re-reviewed 2026-10-25 (audit) — trigger fired again:** nine shifts, every one with ready 0, ran 26–43 of 60 minutes. Its floor is 5 in `backlog_status.py` but 3 in the shift and backlog skills (and was in PRD §0, now pointing at the tool); assumption 3's "a floor of 3" is stale. The cause is D13's, not supply's: the work above the bar waits on the owner.
**Re-reviewed 2026-10-28 (audit):** (1) false: 0 ready against a floor of 5, for every shift since 10-25 that did not inherit work; (3) false: the shift skill says 3, the tool 5 (in the 11-05 bundle). The cause is D13's.

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
**Re-reviewed 2026-10-14 (named most due by the 10-13 audit):** holds. (1) revenue is still $0, and YouTube's bar doubling for new applicants on 1 February 2027 pushes "earning" further out, so this binds longer than first thought. The owner applied it both ways since: bet 2's narration spend approved with the bet (#72), Gemini's paid tier refused (#62, "find another solution"). (2) holds: the free answers keep coming (Groq for #62, samples on a separate free allowance). Revisit as written.

**Re-reviewed 2026-10-08:** still holds. The owner declined Gemini's paid tier,
asked for so Reddit posts stop reaching a free tier that trains on them (#62):
*"Not approved to spend money on this, find another solution."*
**Re-reviewed 2026-10-13 (audit):** (1) holds for longer: new applicants need 20M Shorts views from 1 Feb 2027 (PLAN §1). (2) in doubt: text-only commentary may fail YouTube's review, and a spoken host needs spend or the owner's voice.
**Re-reviewed 2026-10-25 (audit):** holds; revenue $0. (2)'s doubt about YouTube's review no longer steers bet 1 (D14). The Partner Program bar is about break-even, not profit, on any plan above Pro (PLAN §1, 10-25).
**Re-reviewed 2026-10-28 (audit):** holds: revenue $0, and free routes keep turning up (the stand-in voice, Groq). Its one-line stub, due since 10-25, is still owed.

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
**Re-reviewed 2026-10-13 (audit):** (b) at risk: `v8` is read on AskReddit alone (~1 a day under #3), so its 20 uploads take ~20 days and four a day (#4) could land mid-bake.
**2026-10-18:** the floor still reads the whole era, but the comparison now reads the release replaced, at 20+ uploads: `v7` read +20% over the pool, so `v8` could have fallen ~17% below it and passed.
**Re-reviewed 2026-10-25 (audit):** holds; still two uploads a day, and four a day waits on bet 1 (#80).
**Re-reviewed 2026-10-28 (audit):** holds: two a day, four waiting on #80; the Monday snapshot retries since 10-27.

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
**Re-reviewed 2026-10-13 (audit):** (2) weakened: `v7` raised watch-seconds 20% while the engaged share stayed 0.34–0.36 (PRD #8), and bet 1's real gate, YouTube's review, has no metric.
**Re-reviewed 2026-10-25 (audit):** "bet 1's real gate, YouTube's review" is superseded: the owner made a first-time viewer the test (D14, 10-19). The typed metrics stand; the revenue bar counts engaged views (PLAN §1).
**Re-reviewed 2026-10-28 (audit):** (1) strained: the zero-rate guardrail breached again (4.8% → 11.4%), as on 10-09; a breach on 11-02 too is the revisit trigger. (2) strained: watch-seconds is flat while the revenue bar counts engaged views.

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
**Re-reviewed 2026-10-13 (audit):** holds; the last three shifts ranked forward and reversed.
**Re-reviewed 2026-10-25 (audit):** holds; every shift since 10-21 ranked forward and reversed.
**Re-reviewed 2026-10-28 (audit):** holds, clean for a third audit (10-13, 10-25, 10-28): eligible to graduate into the backlog skill, a change for the 11-05 bundle.

## D7 · 2026-09-21 · Slack goes to research, not back to the clock — **absorbed by D11 and the shift skill**

A thin shift becomes a research shift, with no percentage cap; the value bar,
not a ceiling, stops padding. Its rule now lives in `/shift` §3 and §7, and its
evidence under D11 and D13: assumption 1 ("research always has work above the
bar") has been false since 10-09, because that work waits on the owner.
Compressed by the 2026-10-25 audit; full text and re-reviews in git (`8f71e60`).

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
**Re-reviewed 2026-10-13 (audit):** (1) strained: two shifts held back a rule fix to spare the owner's queue, and no skill change can land until #50 is applied (8 days).
**Re-reviewed 2026-10-25 (audit) — trigger fired.** #50 approved 10-05 and unapplied 20 days; #65 behind it 17. Its cost is now visible: the shift skill and the backlog skill say the ready floor is 3, `backlog_status.py` says 5, and the skill's "cannot read Actions logs" is false (`gh run view --log` works). Workflow-file patches never needed #50 (`apply-approved.yml` lands them on a label). For the 11-05 monthly: one bundled skill change, not more asks to an absent owner.
**Re-reviewed 2026-10-28 (audit):** (1) false: #50, approved 10-05, is still unapplied; (3) mixed: process wording is labelled within hours (#84, #85).

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
**Re-reviewed 2026-10-13 (audit):** the count fell to 21 of 25, but items grow instead (the Groq item runs ~500 words); (3) still strained.
**Re-reviewed 2026-10-25 (audit):** (3) worse: TECH_DEBT sits at 25 of 25 with items up to ~785 words, and WORKLOG's word budget holds two entries. Closure happened this audit (the 10-21 item resolved into this one), but item length is unbounded.
**Re-reviewed 2026-10-28 (audit):** (1) false for WORKLOG: ~1,000-word entries mean its word budget keeps two and the ten-entry cap never binds; (3) strained: TECH_DEBT at 24 of 25.

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
**Re-reviewed 2026-10-13 (audit):** holds; a sample and a fresh review caught bet 1's dropped host lines before merge.
**Re-reviewed 2026-10-25 (audit):** holds; gates caught real defects (two held samples, a truncation slur, a blank line dropping the host). Its text omits two later gates: the fresh-context review (CLAUDE.md §3) and the publishing-policy exception (§4).
**Re-reviewed 2026-10-28 (audit):** (1) strained: two commits reached `main` before their fresh review (friction F37), which CI does not enforce; (2) untestable, no bad release since; (3) holds.

## D1 · 2026-09-19 · Priority queue over allocation — **SUPERSEDED by D3**

Kept as the worked example of why this file exists.

**Why it was chosen:** primarily that remaining plan usage could not be read
programmatically, making allocation brittle; secondarily that a queue degrades
gracefully when a session ends mid-task.

**What went wrong:** the primary assumption was false within two hours — the
statusLine payload exposes `rate_limits.five_hour` and `.seven_day`. The
decision was never revisited, and it took the owner asking "why did you choose
this?" to surface it. The secondary reason survived into D3's ceiling rule
(itself superseded by D12); the primary did not.

**The lesson this file encodes:** record the assumption, not just the
conclusion. A conclusion cannot tell you when it has expired.
