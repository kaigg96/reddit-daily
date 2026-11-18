# E3 · Q1 2027: the business after the cutover
Status: proposed (challenged and amended 2026-11-15; T2 decides by 12-20)
Function: Strategy, Monetization, Distribution
Deadline: the quarter's bets set by 2026-12-20 (with E1 T9); the verdict by 2027-03-31
Measure: the owned show's reach per upload (engaged views at 7 days, median and tail) with subscribers per 1,000 views beside it; the projected date for both halves of the 500-subscriber tier
Rule: below under "The verdict"; written before Q1 starts, applied as written

## Why now

Every bet this quarter assumed Reddit, and the quarter's planning is now a
shift's (D16). Written in the owner's session on 2026-11-15 with the time to
think that a shift does not have, then **argued against the same night by a
fresh agent, which found the first draft's premise backwards** (below). T2
has it challenged again before the bets are set; the verdict rule is the one
part that should survive, because its value is that it was set before the
quarter's numbers existed.

## Where the company stands, plainly

- Revenue is $0. Costs are the Claude subscription and about $1 a month.
- Every route that pays has two halves, and on YouTube **views bind**
  (PLAN §1): the 500-subscriber tier is 203× short on engaged views and 19×
  on subscribers, the Partner Program 677× and 38×. The 500 tier needs both
  halves (500 subscribers *and* 3M engaged Shorts views in 90 days), and
  what it pays (fan funding, Shopping) on a channel with no comments and
  0.1% of views from subscribers is about nothing against the subscription.
  So no date for 500 subscribers is a date for revenue.
- **No combination of the levers the record supports reaches any YouTube
  route within 48 months**: volume ×2 (assumed, PRD #4), capitals ×2
  (observational, PRD §4), a subscriber rate ×3 (untried). At four a day the
  500 tier needs about 8,000 engaged views per upload; today's median is
  about 35. The paid channels in our genre have what we lack: a few videos
  that reach hundreds of thousands. **Q1 cannot be a march toward a bar. It
  is a search for a format that reaches**, and its first job is to say so.
- The subscriber rate (0.31 per 1,000; 12 gains on the last 38,240 views)
  is reported beside reach, never alone: a reading gives no reason to follow
  and the owned show can, but a rate without reach pays nothing.
- Bet 2 (double weekly views) will be read at two a day, because four a day
  waits for the show choice (PRD #4). Expect it to miss; that is a
  consequence of the cutover, not a finding about volume.

## The decision

**Q1 2027's bet: does any owned format reach?** E1's February comparison
(takes, play-along, perhaps Stack Exchange; one upload a day each, same
weeks) is the search. Each arm is read on engaged views per upload at 7
days, as a distribution (median *and* the share of uploads past 1,000 and
10,000), with its subscriber rate beside it. The levers inside an arm are
one bundle: a quarter brings too few subscriber gains to separate them
(PRD §4, 2026-10-17), so T2 may not promise a per-lever read.

1. **Lever inside every arm: a reason to come back, with the way to get
   it.** The owned show is a **Shorts series** (PRD §4, 2026-11-03: the
   feed plays the next episode; set up once in Studio, which is the owner's
   login, so one ask with the steps when the show is chosen; uploads join by
   `playlistItems.insert`). The closing line names tomorrow's question and
   the one way to get it; PRD §5 no. 9 bans fake engagement, not asking. The
   ask's wording is its own variable. The comment posted at upload carries
   the question (it cannot be pinned by API).
2. **The channel's own name and look** once the show is chosen (E1 T11,
   C12): a Decide, a notice, then the owner's login.
3. **Volume rides on the choice:** four a day starts the week after E1 T9
   (PRD #4's rule unchanged). If it has not shipped by 2027-01-15, the
   verdict is read at two a day's volume and says so.
4. **Titles:** if #14 keeps (read ~11-23), every Q1 title carries one
   capitalised word, the one measured views lever; reported, never a trigger.
5. **A second feed is its own line (T4), outside the verdict:** a follower
   elsewhere counts toward no YouTube bar. It answers PLAN §4's dependence
   risk and is measured on its own views per upload.
6. **No new route is applied for in Q1.** Every route is out of reach; the
   Reddit question (#60) is moot once nothing of Reddit's is uploaded.

**Rejected:** the first draft's bet, subscribers per 1,000 views ×3 (it
measured the half that does not bind and its Keep clause would have kept a
38-month plan); a direct-revenue bet (sponsors want 1,000 subscribers,
affiliates cannot be clicked from a Short, a product has no audience to sell
to); long-form (the same bars bind); doing nothing until E1 settles.

## The verdict (set 2026-11-15, amended the same night before any Q1 number)

At the first weekly review on or after **2027-03-31**, quote this rule, then
read T1's tool: for each arm, its reach distribution and rate, and the
projected date for **both halves** of the 500-subscriber tier (3M engaged
views in 90 days, 500 subscribers) at the volume actually running.

- **Keep going** only if some arm's projection for both halves is within
  **24 months**. The rate alone keeps nothing.
- **Change** if the best arm's projection is 24–48 months out: the next
  quarter runs that arm alone at four a day, and the successor epic says what
  it would take. The levers inside it carry forward as a bundle, unnamed.
- **Say plainly, and decide the pivot,** if the best projection is past 48
  months or no arm beat the readings' reach by ×2: the YouTube path cannot
  reach revenue above costs at this capability. The shift decides the pivot
  (a format, a platform or a product: a Decide with its reversible first
  step, `ORG.md` Strategy) and gives notice with the evidence. **Stopping
  is the owner's alone**, since the subscription is their money; the notice
  says the projection in months so they can make that call.

The 24 and 48 months are the owner's to move; they were chosen so that a
plan that pays in 2029 is named as such rather than carried quietly.

## Out of scope

Spending of any kind (no paid promotion, no paid tools); any application to
a programme; changing the experiment rules (D9, #18). The two owner-login
asks (the series in Studio; a second feed's account) are raised once each,
with exact steps, only when everything else is built.

## Assumptions to check

1. Per-upload subscriber gains are already collected (`subs_gained`, weekly
   since 2026-10-07, by video; the per-video sum matches the channel count).
   A week whose column was refused (10-26, one HTTP 500) is re-read from the
   next snapshot, since the counts are cumulative.
2. The owned show's episodes are allowed on a second feed under that feed's
   terms and ORG.md's publishing policy, with the same credit lines.
3. A quarter's aggregate can tell ×3 on the rate (12 against 37 expected
   gains: Poisson 95% intervals [6, 21] and [26, 51] do not overlap), but
   no per-arm or per-lever rate read can; T1 amends PRD §4's 2026-10-17 line
   to say exactly that.
4. The reach distribution at our volume can show a tail: a share past 1,000
   views is readable at ~60 uploads an arm; past 10,000 may show nothing,
   and nothing is a result.

## The challenge (2026-11-15, a fresh agent, before any ticket)

Accepted and applied above: views bind on YouTube, not followers (PLAN §1;
`--routes`); the 500 tier needs both halves and pays about nothing here;
the first draft's Keep clause fired at a 38-month projection; its Change
clause could not name a lever (too few gains per lever); "no subscribe CTA"
misread PRD §5 no. 9; `subs_gained` is already collected by video; comments
cannot be pinned by API; a Shorts series is the stronger reason to come
back; a second feed moves no YouTube bar; capitals, not volume, is the
measured views lever; the third outcome gave the owner a pivot that D16
makes a shift's. Kept against it: the owner's 24/48-month horizons, and the
pre-committed verdict as the pattern.

## Tickets

### T1 · Reach and rate are measurable per arm, and the baseline is on record
Status: ready
Needs: none
Touches: src/insights.py, scripts/report.py, scripts/weekly_analytics.py (only if a column is missing), tests/, analysis/experiments.csv, PRD.md §4
Context: assumptions 1, 3 and 4. `subs_gained` by video exists since 10-07; `--routes` prints the channel's rate. The bet needs, per arm (`show`, E1 T3): engaged views per upload at 7 days as median and the shares past 1,000 and 10,000; subscribers per 1,000 views with a chance gap; and the projected date for both halves of the 500 tier and the Partner bar at a given uploads-per-day. A refused week is re-read from the next snapshot.
Accept:
- [ ] `report.py --reach --compare show=<arm> --at-age 7` prints median engaged views, the two tail shares and the chance gaps, refusing thin cohorts as elsewhere
- [ ] `report.py --metric subs_per_1k --at-age 28 --compare show=<arm>` prints the rate with its chance gap; a week whose `subs_gained` was refused reads from the next snapshot, with a test
- [ ] `report.py --routes --per-day N` prints the projected date for both halves of the 500 tier and of the Partner bar at the given volume, from the last 90 days' per-upload figures
- [ ] PRD §4's 2026-10-17 line is amended: a rate rule may trigger on a quarter's aggregate once expected counts are separable, never per arm or per lever
- [ ] the baseline (readings' reach distribution, rate, projections at 2 and 4 a day) is in this file with the commands, and the ledger carries the verdict rule dated before Q1
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

### T3 · A reason to come back, with the way to get it, in every episode
Status: todo
Needs: none (E1 T7 for the play-along form; the takes show has its own closing line)
Touches: src/ (closing line, the comment posted at upload, `playlistItems.insert`), tests/, `.escalations/` (one ask: the series in Studio)
Context: lever 1. The closing line names tomorrow's question and the one way to get it; the comment `youtube.post_comment` posts at upload carries the question (it cannot be pinned). The owned show is a Shorts series: build the join (`playlistItems.insert`) and the test first, then one ask with the Studio steps, which the owner can do from a phone. Its own `FORMAT_VERSION`, one variable per release; the ask's wording is its own later variable. Read as part of the arm's bundle, never alone (assumption 3).
Accept:
- [ ] every upload's closing line and comment carry the next day's question, which the next day's upload actually asks (a test reads the queue)
- [ ] uploads join the series playlist once it exists, with a test against a fake API; the ask names the series title and the three Studio steps
- [ ] the ledger has the arm's rule before the first upload; the read is scheduled in PRD §0
Evidence:

### T4 · The same episodes on a second feed, measured on its own
Status: blocked: E1 T9 (the show chosen), then the owner's login for the account
Needs: none
Touches: a new workflow (the owner's label: it holds a new key), scripts/, PLAN.md §4 (the dependence risk)
Context: lever 5 and PLAN §4's dependence on one feed. Outside the verdict: a follower there counts toward no YouTube bar. Pick the feed by reach for this shape of video among comparable channels (Market intelligence), not by payout. The post job needs that feed's key, so its workflow lands only on the owner's label; the ask is one message with the exact steps once everything else is built and reviewed.
Accept:
- [ ] the feed is chosen with the evidence recorded in PRD §4, and the publishing policy (ORG.md) covers it
- [ ] the job is built and reviewed before the ask; the ask can be done from a phone in five minutes
- [ ] views and followers per upload on that feed are in the weekly snapshot within two weeks of the first post, as their own line in PLAN §1
Evidence:

### T5 · The verdict
Status: todo
Needs: T1
Touches: this file, DECISIONS.md, PLAN.md, `.escalations/` (a notice, in the third case)
Context: "The verdict" above, at the first weekly review on or after 2027-03-31. Quote the rule before any number; the projection is for both halves at the volume that actually ran.
Accept:
- [ ] the rule is quoted, the figures follow it, and one of the three outcomes is recorded with its evidence
- [ ] in the third case, the pivot is decided as a Decide with its reversible first step, and the owner is told by notice with the projection in months; stopping is left to them, never decided for them
Evidence:
