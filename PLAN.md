# Company plan

The company's status: its goal, the queue for everything outside the channel
product, its risks, and when each review last ran. The channel product's status
is in [PRD.md](PRD.md) §0, and who owns what is in [ORG.md](ORG.md). Read at
shift start. **Keep it short:** answered items leave, and settled history lives
in git.

## 1. Goal and scorecard

**Show of Hands** (working name, `ORG.md`). **Goal:** monetization, meaning
revenue above costs (`DECISIONS.md` D12).

| | Today |
|---|---|
| Revenue | $0 |
| Costs | Claude subscription, plus about $0.90/month of Polly (AWS budget $3/month; `scripts/money_check.py`) |
| Path to revenue | **No route is within reach of the current path** (2026-10-05). Partner Program: 1,000 subscribers and 10M Shorts views in 90 days. The channel gains ~37,000 play starts per 90 days, under 1% from the back catalogue, but **the bar counts engaged views**, and only **37%** of ours are: ~13,800 per 90 days, **~720× short** (2026-10-19; every distance here: `report.py --routes`). It has **21 subscribers** (2026-10-19, none net in a week), ~48× short. Views are the binding half. **From 1 February 2027 new applicants need 20M, and Shorts ad revenue 10M held every 90 days** (YouTube's blog, 2026-08-10); the unchanged 500-subscriber tier (3M in 90 days: fan funding, Shopping) is the nearest Shorts route, ~220× short. Creators keep 45% of a pool shared by engaged views; secondary sources say $0.01–$0.10 per 1,000, so ~$34–340 a month at the bar. **Long-form**: nearest on paper, as subscribers (~48×) bind, but out of scope (PRD §4, 2026-10-18; §7). Other routes: **TikTok** Creator Rewards (2026-10-06): 100k views in 30 days (~8× short) and 10k followers, the binding half: ~33M views at our follow rate (11 gains: ~18–65M), nearer than the 500 tier only at over ~4× it. Only original videos over a minute, from an account **based in the US, UK, Germany, Japan, South Korea, France, Mexico or Brazil**; ours run ~21s; **Facebook** (March 2026) is invite-only and demonetises pages that mostly narrate "what's already on screen"; **Instagram** pays no reliable rate. **No route pays for a reading**: bet 1 comes first everywhere |
| Product scorecard | `venv/bin/python scripts/report.py --scorecard` |

**Function coverage.** General management updates this at each monthly review.
A function still at "none" after its first monthly review is a finding (D12).

| None | Thin | Partial | Strong |
|---|---|---|---|
| Audience, Monetization, Market intelligence | Strategy, Distribution, Editorial, Legal | General management, Product management, Finance, Security | Engineering, Reliability, Data |

## 2. This quarter's bets

**Bet 1 approved** (#70): make the format ours, viewers first (D14); no
voice (#71, PRD #15). Bet 2
approved (#72, 2026-10-10); bet 3's pilot waits on bet 1. Bet 2: double weekly views (PRD #14, #10, #3, #4; baseline fixed 2026-10-05: **8,300** views at 7 days over publish weeks W36–W39, `report.py --trajectory --metric views`, so the bar is 16,600 over the quarter's last four full weeks, in play starts. Beside it, in engaged views (pre-committed 2026-10-14): W40–W43's 7-day total at two a day, doubled (W40: 1,762; `--metric engaged_views`)); price other routes
and pilot the best (priced 2026-10-11, §1; Reddit's terms, §4).

## 3. Work queue

Everything outside the channel product (PRD §0), with the same statuses;
`scripts/backlog_status.py` counts both.

| # | Status | Function | Item | Next step, and done when |
|---|---|---|---|---|
| C10 | parked: the first read (10-19, `scripts/comments.py`) found 7 viewer comments, all on one heated political upload, so a screened queue would post nothing; reopen when a read shows them on 3+ uploads | Audience | **Publishing pipeline** | A shift drafts replies; a workflow posts them under ORG.md's publishing policy. |
| C12 | blocked: bet 1's next step keeping (PRD #15) | Editorial | **A public brand** | The company's working name is Show of Hands, and the channel's current name uses Reddit's. Once the kept originality step settles the show, check the name's trademark, domain and handles (free), and propose whether and how to rename. **Propose the old videos' fate with it** (2026-10-09): all 1,041 are readings, 883 pre-pipeline earning under 1%. Reviewers check the "main theme": at two a day the new show stays a minority for a year. Delete or start fresh: YouTube's rejection FAQ says "edit or delete" violating videos (10-11); private ones go unmentioned. Renaming is the owner's. Done when the owner has decided. |
| C14 | blocked: the owner's six checks (#59) | Security | **Quarterly account-security check** | The fatal risk's only response; never held. The logins are the owner's. Done when the owner reports a date. |

## 4. Risks

| Risk | Function | Likelihood / impact | Response |
|---|---|---|---|
| The format cannot be monetized under YouTube's reused-content policy | Legal, Editorial | **Confirmed** from YouTube's page (2026-10-05): "Content exclusively features readings of other materials you did not originally create, like text from websites" is not monetizable, and "applies to your channel as a whole". Today's format is that. A second rule refuses content "that looks like it's made with a template" / ends the Partner Program route. Since July 2026 it names content "designed to shock or surprise viewers for the sole purpose of getting views"; 9 of 166 titles do (PRD #14). No report shows text-only commentary passing; YouTube's FAQ (2026-10-13) and policy call reactions "without added voice commentary" and "non-verbal reactions" reused (PRD §4) | Not the deciding test now (D14). Bet 1 (PRD #15); old videos (C12); music variety (owner task, PRD §0; one track) |
| Reddit's terms forbid monetized use of API data | Legal | **Confirmed** from Reddit's Developer Terms (2024-09-24) and the Data API Terms they incorporate (read 2026-10-06). Without written approval, no use "by or on behalf of a business" and no revenue derived from the Data APIs; commercial use needs "a separate agreement". Wider than monetization: §2.4 licenses display only "solely as necessary to … run your App", unmodified "except to format it", so even today's unpaid videos sit outside a plain reading. Its ban on training AI on posts binds those "acting on your behalf", and Gemini's free tier, which reads every post we consider, trains on what it is sent (Google's pages, 2026-10-06) | Owner (#60, 2026-10-10): not yet, since we earn nothing; ask before applying to any programme. Gemini's paid tier declined (#62, no spend); Groq's free tier, which bans training by contract, lands with bet 1's release (PRD #13, #68). No drop-in source replaces Reddit (PRD §4) |
| Shorts revenue is too small at any reachable scale | Strategy | High / high — ~720× short of the Partner Program's bar, ~1,450× for new channels from February 2027 (§1) | Bets 2 and 3 |
| Dependence on one platform (96.7% of views come from the Shorts feed) | Distribution, Strategy | Medium / high | Bet 3 (#55); every route needs bet 1 (§1). Its 10-01 originality change: PRD §4 |
| Loss of the YouTube channel or the Google account | Security, Legal | Low / fatal. Also the spam policy (strikes, termination; read 2026-10-19), whose example of mass-production ("the exact same background music", AI imagery, an AI script) shares our one music track | C14; bet 1; music variety; four a day after bet 1 (#80) |
| A runaway Polly bill | Security, Finance | Low / bounded by the budget action | `money_check.py` every shift; branch code never holds the Polly keys |

## 5. Reviews

`scripts/cadence.py` reads this table to say what is due. A review updates its
own row when it finishes.

| Review | Last held |
|---|---|
| Weekly | 2026-10-19 |
| Monthly | 2026-10-05 |
| Quarterly prep | 2026-10-05 |
| Quarterly planning | 2026-10-10 |
