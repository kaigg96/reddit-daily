# Company plan

The company's status: its goal, the queue for everything outside the channel
product, its risks, and when each review last ran. The channel product's status
is in [PRD.md](PRD.md) §0, and who owns what is in [ORG.md](ORG.md). Read at
shift start. **Keep it short:** answered items leave, and settled history lives
in git.

## 1. Goal and scorecard

**Show of Hands** (working name, `ORG.md`). **Goal:** monetization, meaning
revenue above costs (`DECISIONS.md` D12). The
YouTube Partner Program is the assumed route; the others, priced 2026-10-05,
are no nearer on the current path (§1).

| | Today |
|---|---|
| Revenue | $0 |
| Costs | Claude subscription, plus about $0.90/month of Polly (AWS budget $3/month; `scripts/money_check.py`) |
| Path to revenue | **No route is within reach of the current path** (Strategy, 2026-10-05). Partner Program: 1,000 subscribers and 10M Shorts views in 90 days (YouTube's page); the channel gains ~32,000–37,000 play starts per 90 days, back catalogue included though it earns under 1% (`report.py --trajectory --metric views`, `--catalogue`), but **the bar counts engaged views**, and only **36%** of ours are (`report.py --engaged-share`, 2026-10-05): ~11,000–13,000 per 90 days, **~760–880× short**. It has **21 subscribers** (weekly digest, 2026-10-05), ~48× short. Views are the binding half. YouTube publishes no per-1,000 rate: creators keep 45% of a pool shared by engaged views, and secondary sources put it at $0.01–$0.10. Other routes: **TikTok** Creator Rewards is nearest (its own page, 2026-10-06): 10k followers and 100k views in 30 days (~8× short), only original videos over one minute, and **the account must be based in the US, UK, Germany, Japan, South Korea, France, Mexico or Brazil**; ours run ~21s; **Facebook** (secondary sources) is invite-only, 10k followers and 600k minutes in 60 days (~160× short); **Instagram** pays no reliable per-view rate |
| Product scorecard | `venv/bin/python scripts/report.py --scorecard` |

**Function coverage.** General management updates this at each monthly review.
A function still at "none" after its first monthly review is a finding (D12).

| None | Thin | Partial | Strong |
|---|---|---|---|
| Audience, Monetization, Market intelligence | Strategy, Distribution, Editorial, Legal | General management, Product management, Finance, Security | Engineering, Reliability, Data |

## 2. This quarter's bets

None yet. Three are drafted for the owner's first planning session
(#55, 2026-10-05; bet 1 also asked by label, #70): make the format ours
(PRD #7, #12); double weekly views (PRD #10, #3, #4; baseline fixed 2026-10-05: **8,300** views at 7 days over publish weeks W36–W39, 56 uploads, `report.py --trajectory --metric views`, so the bar is 16,600 over the quarter's last four complete weeks; in play starts; #55 now asks to read it in engaged views too); price the other routes
and pilot the best (C8; Reddit's terms, §4). Until then, the queue ranks on effect on the
path to revenue.

## 3. Work queue

Everything outside the channel product. Product work stays in PRD §0. The
statuses are the same as there, and `scripts/backlog_status.py` counts both
places.

| # | Status | Function | Item | Next step, and done when |
|---|---|---|---|---|
| C11 | baking: commit line applied 2026-10-05 (#52); first snapshot 2026-10-12 | Data | **Collect the subscriber count** | Half of the Partner Program's bar. The weekly statistics job saves it, failing soft so it can never cost the per-video snapshot. Done when a snapshot carries it, and each upload's subscribers gained (added 2026-10-07, fail-soft). |
| C5 | blocked: owner applies its commit patch (escalated 2026-10-05) | Audience | **Collect viewer comments into the repo** | The weekly analytics job saves recent comments (a workflow change, #53). Done when a shift can read last week's comments. |
| C8 | blocked: the owner's logged-in read of Meta's rules (TikTok's confirmed 2026-10-06) | Distribution | **What other short-video platforms require and pay** | TikTok, Instagram Reels, Facebook Reels: eligibility, payouts, and each one's rule on reused content, which YouTube's rules out for today's format (§4). Logged out, Meta's pages withhold their rule lists even from a browser (2026-10-06). Done when the owner's read confirms or corrects them. |
| C10 | blocked: C5 | Audience | **Publishing pipeline** | A shift drafts replies into a queue, and a workflow posts them, under ORG.md's publishing policy. |
| C12 | blocked: the owner's bet-1 choice (PRD #7, #12) | Editorial | **A public brand** | The company's working name is Show of Hands, and the channel's current name uses Reddit's. Once the kept originality step settles what the show is, check the trademark, domain and YouTube/TikTok/Instagram handles for the name (free), and propose whether and how to rename the channel. Renaming is the owner's. Done when the owner has decided. |
| C14 | blocked: the owner's six checks (#59) | Security | **Quarterly account-security check** | The fatal risk's only response; never held. The logins are the owner's. Done when the owner reports a date; the next is due a quarter later. |

## 4. Risks

| Risk | Function | Likelihood / impact | Response |
|---|---|---|---|
| The format cannot be monetized under YouTube's reused-content policy | Legal, Editorial | **Confirmed** from YouTube's page (2026-10-05): "Content exclusively features readings of other materials you did not originally create, like text from websites" is not monetizable, and "applies to your channel as a whole". Today's format is exactly that. A second rule refuses content "that looks like it's made with a template" / ends the Partner Program route | Bet 1 (PRD #7, #12) |
| Reddit's terms forbid monetized use of API data | Legal | **Confirmed** from Reddit's Developer Terms (2024-09-24) and the Data API Terms they incorporate (read first-hand 2026-10-06). Without written approval, no use "by or on behalf of a business", and no one may "derive revenues from the use or provision of the Data APIs … unless there is express written approval from Reddit", and commercial use needs "a separate agreement". Wider than monetization: §2.4 licenses posts and comments only "to copy and display … solely as necessary to … run your App to your App Users", and "You may not modify the User Content except to format it for such display", so even today's unpaid videos sit outside a plain reading. Its ban on training AI on posts binds those "acting on your behalf", and Gemini's free tier, which reads every post we consider, is "used to improve our products"; the paid tier is not (Google's pages, 2026-10-06) | Owner (#60): ask Reddit now. Gemini's paid tier declined (#62, no spend); Groq's free tier, which bans training by contract, is merged switched off, awaiting the owner (PRD #13; #68, #69). Stack Exchange is no drop-in fallback: 0 of 95 hot questions on six sites had three answers under 150 characters (median 1,094; 2026-10-07), so it needs a format that condenses answers |
| Shorts revenue is too small at any reachable scale | Strategy | High / high — ~800× short of the Partner Program's bar in engaged views, and no other route is nearer (§1) | Bets 2 and 3 |
| Dependence on one platform (96.7% of views come from the Shorts feed) | Distribution, Strategy | Medium / high | C8 |
| Loss of the YouTube channel or the Google account | Security | Low / fatal | C14, quarterly |
| A runaway Polly bill | Security, Finance | Low / bounded by the budget action | `money_check.py` every shift; branch code never holds the Polly keys |

## 5. Reviews

`scripts/cadence.py` reads this table to say what is due. A review updates its
own row when it finishes.

| Review | Last held |
|---|---|
| Weekly | 2026-10-05 |
| Monthly | 2026-10-05 |
| Quarterly prep | 2026-10-05 |
| Quarterly planning | never |
