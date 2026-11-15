# E3 · Q1 2027: the business after the cutover
Status: proposed
Function: Strategy, Monetization, Distribution
Deadline: the quarter's bets set by 2026-12-20 (with E1 T9); the verdict by 2027-03-31
Measure: subscribers gained per 1,000 views, and the projected date the 500-subscriber tier is reached
Rule: below under "The verdict"; written before Q1 starts, applied as written

## Why now

Every bet this quarter assumed Reddit, and the quarter's planning is now a
shift's (D16). Written in the owner's session on 2026-11-15, with the time to
think that a shift does not have. **The first shift on it has a fresh agent
argue against it** and may amend it on evidence; the verdict rule is the one
part that should survive, because its whole value is that it was set before
the quarter's numbers existed.

## Where the company stands, plainly

- Revenue is $0. Costs are the Claude subscription and about $1 a month.
- Every route that pays has two halves, views and followers, and **followers
  bind everywhere** (PLAN §1): the Partner Program needs 1,000 subscribers
  (we have 26, ~38×) against 10M engaged views (~677×); the 500-subscriber
  tier is 19× away on subscribers and 203× on views. TikTok's programme is
  closed to our country. So the number that decides whether this company
  ever earns is **subscribers per 1,000 views**, today **0.31**. At that rate
  and today's reach (~40,000 play starts a quarter), 500 subscribers take
  about nine years.
- The rate has never been a variable. A reading of other people's words gives
  no reason to follow; the own show can (a daily question, a tomorrow). Views
  are 200× short and have one evidenced lever (volume, ×2 at four a day).
  The rate is 19× short and has levers nobody has pulled: a reason to come
  back, a name that is ours (C12), the same show on more than one feed.
- Bet 2 (double weekly views) will be read at two a day, because four a day
  waits for the show choice (PRD #4). Expect it to miss; that is a consequence
  of the cutover, not a finding about volume, and the quarter's verdict says so.

## The decision

**Q1 2027's bet is the subscriber rate, on the owned show.** Not views, not
a revenue route: those follow from the rate or not at all.

1. **The bar: subscribers per 1,000 views ×3 over Q1**, from 0.31 to 0.93,
   read on the quarter's uploads at 28 days (subscriptions arrive later than
   views; `channel_stats.csv` gives the count, the ledger the rule). At two
   a day that is roughly 40 subscribers against 12 expected at today's rate,
   a difference the counts can show (reasoned from Poisson noise; T1 confirms
   with the tool). Views are reported beside it and never trigger.
2. **Three levers, each its own ticket, one variable per release:** a reason
   to come back built into the show (E1's "tomorrow" line and pinned
   question); the channel's own name and look once the show is chosen (E1
   T11, C12); and the same episodes on a second feed, as audience, not
   revenue (T4).
3. **Volume rides on the choice:** four a day starts the week after E1 T9
   (PRD #4's rule unchanged), so bet 2's lever is tested in Q1 at the show
   that will carry it.
4. **No new route is applied for in Q1.** Every route's followers half is
   out of reach; applying costs attention and the Reddit question (#60) is
   moot once nothing of Reddit's is uploaded.

**Rejected:** a views bet (200× short, and the one lever is already queued);
a direct-revenue bet (sponsors want 1,000 subscribers, affiliates cannot be
clicked from a Short, a product has no audience to sell to); long-form (the
same 1,000-subscriber half binds); doing nothing until E1 settles (the rate
can be measured on the takes arm from day one).

## The verdict (set 2026-11-15, before any Q1 number; D15's pattern)

At the first weekly review on or after **2027-03-31**, quote this rule, then
read `report.py --routes` and the rate ticket's figures:

- **Keep going** if the rate reached 0.93 per 1,000 or better, or the
  projected date for 500 subscribers at Q1's measured rate and volume is
  within **24 months** of the read.
- **Change** if the rate improved but the projection is 24–48 months out:
  the next quarter's bet is whichever lever moved the rate most, at four a
  day, and this epic's successor says what it would take.
- **Tell the owner plainly** if the projection is past 48 months or the rate
  did not move: the current path cannot reach revenue above costs in a
  horizon worth the subscription, and the recommendation is a pivot (a
  format, a platform or a product) or stopping. This is the one message a
  shift owes the owner that is not an ask (`ORG.md`, Strategy: "say plainly
  when the current path cannot reach the goal"). It goes as a notice with
  the evidence, not a question.

The 24 and 48 months are the owner's to move; they were chosen so that a
plan that pays in 2029 is named as such rather than carried quietly.

## Out of scope

Spending of any kind (no paid promotion, no paid tools); any application to
a programme; changing the experiment rules (D9, #18). A second platform's
account is the owner's login (one ask, with the exact steps, only when T4 is
ready to post).

## Assumptions to check

1. Subscriber counts per upload are readable at 28 days from the weekly
   snapshot (`channel_stats.csv` is channel-level; per-upload may need the
   Analytics API's `subscribersGained` by video, which the weekly job can
   add within its present scope).
2. The owned show's episodes are allowed on a second feed under that feed's
   terms and ORG.md's publishing policy, with the same credit lines.
3. ×3 is detectable at Q1's volume: T1 checks with `report.py`'s chance gap
   on real counts before the bar is final.

## Tickets

### T1 · The rate is measurable, and the baseline is on record
Status: ready
Needs: none
Touches: scripts/weekly_analytics.py, src/insights.py, scripts/report.py, tests/, analysis/experiments.csv
Context: assumption 1 and 3. `report.py --routes` already prints subscribers per 1,000 views for the channel; the bet needs it per upload (or per week) with a chance gap, and by `show` once E1 T3 lands. The Analytics API's `subscribersGained` dimensioned by video is the likely source; stay inside the job's present scope.
Accept:
- [ ] the weekly snapshot records subscribers gained per upload (or per publish week if per-video is not available, and the ticket says which)
- [ ] `report.py --metric subs_per_1k --at-age 28` runs, refuses thin cohorts, prints a chance gap, and `--compare show=` works once the column exists
- [ ] `report.py --routes` prints the projected date for 500 and 1,000 subscribers at the last 90 days' rate and pace
- [ ] the baseline (rate, volume, projection) is written into this file with the commands, and the ledger carries the bar as a rule dated before Q1
Evidence:

### T2 · Q1's bets are set
Status: todo
Needs: T1
Touches: PLAN.md §2, DECISIONS.md, this file
Context: with E1 T9, by 2026-12-20. A Decide: this epic is the draft, a fresh agent argues against it, and the bets that survive go into PLAN §2 with their rules. Last quarter's bets retire with a verdict each; bet 2's says it was read at two a day.
Accept:
- [ ] PLAN §2 names Q1's bet and bar; DECISIONS.md records the decision, the alternatives and the challenge's objections
- [ ] the verdict rule above is in the ledger unchanged, or changed with the reason recorded before any Q1 number
Evidence:

### T3 · A reason to come back is in every episode
Status: todo
Needs: none (E1 T7 for the play-along form; the takes show has its own closing line)
Touches: src/ (closing line, pinned comment), tests/
Context: lever 1. The closing line names tomorrow's question in five words, and the pinned comment carries it. No "subscribe" (PRD §5 no. 9); the reason is the question. Its own `FORMAT_VERSION`, one variable per release, read on the rate at 28 days under T1's tool.
Accept:
- [ ] every upload's closing line and pinned comment carry the next day's question, which the next day's upload actually asks (a test reads the queue)
- [ ] the ledger has its rule before the first upload; the read is scheduled in PRD §0
Evidence:

### T4 · The same episodes on a second feed, as audience
Status: blocked: E1 T9 (the show chosen), then the owner's login for the account
Needs: none
Touches: a new workflow (the owner's label: it holds a new key), scripts/, PLAN.md §4 (the dependence risk)
Context: lever 3 and PLAN §4's dependence on one feed. Pick the feed by reach for this shape of video among comparable channels (Market intelligence), not by its payout, since none pays us. The post job needs that feed's key, so its workflow lands only on the owner's label; the ask is one message with the exact steps once everything else is built and reviewed.
Accept:
- [ ] the feed is chosen with the evidence recorded in PRD §4, and the publishing policy (ORG.md) covers it
- [ ] the job is built and reviewed before the ask; the ask can be done from a phone in five minutes
- [ ] followers and views per upload on that feed are in the weekly snapshot within two weeks of the first post
Evidence:

### T5 · The verdict
Status: todo
Needs: T1
Touches: this file, DECISIONS.md, PLAN.md, `.escalations/` (a notice, only in the third case)
Context: "The verdict" above, at the first weekly review on or after 2027-03-31. Quote the rule before any number.
Accept:
- [ ] the rule is quoted, the figures follow it, and one of the three outcomes is recorded with its evidence
- [ ] in the third case, the owner is told as a notice with the projection and the recommendation, never as a question
Evidence:
