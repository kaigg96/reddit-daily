# Company plan

The company's goal, queue outside the product, risks and reviews. The product:
[PRD.md](PRD.md) §0; who owns what: [ORG.md](ORG.md). **Keep it short:** answered items leave; history lives
in git.

## 1. Goal and scorecard

**Show of Hands** (working name, `ORG.md`). **Goal:** monetization, meaning
revenue above costs (`DECISIONS.md` D12).

| | Today |
|---|---|
| Revenue | $0 |
| Costs | Claude subscription (Pro $20/month, Max from $100; plan unrecorded), Polly ~$0.90/month (budget $3; `scripts/money_check.py`). **Break-even (10-25):** the Partner Program bar covers Pro at any reported rate; Max only above $0.03–0.06 per 1,000 engaged views (at $0.01: 30–60M per 90 days) |
| Path to revenue | **No route is within reach of the current path** (2026-10-05). Partner Program: 1,000 subscribers and 10M Shorts views in 90 days. **The bar counts engaged views**: ours are ~13,200 per 90 days (37% of ~35,700 play starts), **~757× short** (2026-10-26; every distance: `report.py --routes`). **22 subscribers**, ~45× short: views bind. **From 1 February 2027 new applicants need 20M, and Shorts ad revenue 10M held every 90 days** (YouTube's blog, 2026-08-10); the unchanged 500-subscriber tier (3M in 90 days: fan funding, Shopping) is the nearest Shorts route, ~227× short. Creators keep 45% of a pool shared by engaged views; secondary sources say $0.01–$0.10 per 1,000, so ~$34–340 a month at the bar. **Long-form**: nearest on paper (~45×), but out of scope (PRD §4, §7). Other routes: **TikTok** Creator Rewards (10-06): 10k followers bind (~33M views at our rate); original videos over a minute, eight countries only; ours run ~21s; **Facebook** (March 2026) is invite-only and demonetises pages that mostly narrate "what's already on screen"; **Instagram** pays no reliable rate; **Snapchat**: invited, 50k followers, 15,000 hours watched in 28 days (ours ~37), "original", 30s+; **X** (via a report): paid Premium, 500 verified followers, 500k verified impressions in 90 days, no reuploads. **No route pays for a reading**: bet 1 comes first everywhere |
| Product scorecard | `venv/bin/python scripts/report.py --scorecard` |

**Function coverage.** General management updates this at each monthly review.
A function still at "none" after its first monthly review is a finding (D12).

| None | Thin | Partial | Strong |
|---|---|---|---|
| Audience, Monetization, Market intelligence | Strategy, Distribution, Editorial, Legal | General management, Product management, Finance, Security | Engineering, Reliability, Data |

## 2. This quarter's bets

**Bet 1 approved** (#70): make the format ours, viewers first (D14); no
voice (#71, PRD #15). Bet 2
approved (#72); bet 3's pilot waits on bet 1. Bet 2: double weekly views (PRD #14, #10, #3, #4; baseline fixed 2026-10-05: **8,300** views at 7 days over publish weeks W36–W39, `report.py --trajectory --metric views`, so the bar is 16,600 over the quarter's last four full weeks, in play starts. Beside it, in engaged views (pre-committed 2026-10-14): W40–W43's 7-day total at two a day, doubled (W40: 1,762; `--metric engaged_views`)); price other routes
and pilot the best (§1; Reddit's terms, §4). Bet 2 needs bet 1 merged by ~10-30–11-06 (PRD §4).

## 3. Work queue

Everything outside the channel product (PRD §0), with the same statuses;
`scripts/backlog_status.py` counts both.

| # | Status | Function | Item | Next step, and done when |
|---|---|---|---|---|
| C10 | parked: comments on one upload a week (7 on 10-19, 1 on 10-26) (`scripts/comments.py`); reopen when a weekly read shows them on 3+ | Audience | **Publishing pipeline** | A shift drafts replies; a workflow posts them under ORG.md's publishing policy. |
| C12 | blocked: bet 1's next step keeping (PRD #15) | Editorial | **A public brand** | The working name, Show of Hands, is an English folk duo's since 1986, YouTube channel included; the channel's current name uses Reddit's. Once the kept originality step settles the show, check the name's trademark, domain and handles (free), and propose whether and how to rename. **Propose the old videos' fate with it** (2026-10-09): all 1,041 are readings, 883 pre-pipeline earning under 1%. Reviewers check the "main theme": at two a day the new show stays a minority for a year. Delete or start fresh: YouTube's rejection FAQ says "edit or delete" violating videos (10-11); private ones go unmentioned. Renaming is the owner's. Done when the owner has decided. |
| C16 | blocked: the 11-05 review (both samples in PRD §4) | Strategy | **A source after Reddit** | All bets assume Reddit (§4). Done when both samples are on the 11-05 review. |
| C14 | blocked: the owner's six checks (#59) | Security | **Quarterly account-security check** | The fatal risk's only response; never held. Done when the owner reports a date. |

## 4. Risks

| Risk | Function | Likelihood / impact | Response |
|---|---|---|---|
| The format cannot be monetized under YouTube's reused-content policy | Legal, Editorial | **Confirmed** from YouTube's page (2026-10-05): "Content exclusively features readings of other materials you did not originally create, like text from websites" is not monetizable, and "applies to your channel as a whole". Today's format is that. A second rule refuses content "that looks like it's made with a template" / ends the Partner Program route. Since July 2026 it names content "designed to shock or surprise viewers"; refused in titles since 10-26 (PRD §0). Whether a text-only host passes is unsettled (PRD §4) | Not the deciding test now (D14). Bet 1 (PRD #15); old videos (C12); music variety (owner task, PRD §0) |
| Reddit's terms forbid monetized use of API data | Legal | **Confirmed** from Reddit's Developer and Data API Terms (read 2026-10-06). Without written approval, no use "by or on behalf of a business" and no revenue derived from the Data APIs. Even unpaid, our videos sit outside a plain reading of its display licence (#60). Its ban on training AI on posts binds Gemini's free tier, which trains on what it is sent. Deleted posts and comments must go "as soon as possible" (§3.3), which a published video cannot short of deletion (C12) | Owner (#60, 2026-10-10): not yet, since we earn nothing; ask before applying to any programme. Gemini's paid tier declined (#62); Groq (bans training) is only `v8`'s fallback (PRD #13). No drop-in source replaces Reddit (PRD §4; C16) |
| Reddit's free API, our only source, ends March 2027; unregistered apps lose it 2027-01-12 | Legal, Strategy | **Confirmed** by Reddit's page registering "existing apps" (archived 10-13): 10-31 binds new requests only / fatal: uploads stop. Then "commercial deals" (~$12k/month reported); Devvit lacks Python | The owner registers our app (#82); C16 |
| Shorts revenue is too small at any reachable scale | Strategy | High / high — ~757× short (§1); at four a day each upload needs ~70× our best (PRD §4) | Bets 2 and 3 |
| Dependence on one platform (96.7% of views come from the Shorts feed) | Distribution, Strategy | Medium / high | Bet 3 (#55); every route needs bet 1 (§1). Its 10-01 originality change: PRD §4 |
| Loss of the YouTube channel or the Google account | Security, Legal | Low / fatal. Also the spam policy (strikes, termination; read 2026-10-19), whose example of mass-production ("the exact same background music", AI imagery, an AI script) shares our one music track | C14; bet 1; music variety; four a day after bet 1 (#80) |
| A runaway Polly bill | Security, Finance | Low / bounded by the budget action | `money_check.py` every shift; branch code never holds the Polly keys |

## 5. Reviews

`scripts/cadence.py` reads this table to say what is due. A review updates its
own row when it finishes.

| Review | Last held |
|---|---|
| Weekly | 2026-10-26 |
| Monthly | 2026-10-05 |
| Quarterly prep | 2026-10-05 |
| Quarterly planning | 2026-10-10 |
