# Company plan

The company's status: its goal, the queue for everything outside the channel
product, its risks, and when each review last ran. The channel product's status
is in [PRD.md](PRD.md) §0, and who owns what is in [ORG.md](ORG.md). Read at
shift start. **Keep it short:** answered items leave, and settled history lives
in git.

## 1. Goal and scorecard

**Show of Hands** (working name, `ORG.md`). **Goal:** monetization, meaning
revenue above costs (`DECISIONS.md` D12). The
YouTube Partner Program is the assumed route until Strategy has priced the
others (C1).

| | Today |
|---|---|
| Revenue | $0 |
| Costs | Claude subscription, plus about $0.90/month of Polly (AWS budget $3/month; `scripts/money_check.py`) |
| Path to revenue | Partner Program out of reach at current scale: it needs 1,000 subscribers and 10M Shorts views in 90 days (YouTube's own page, 2026-10-05); the channel's best 90 days at its weekly rate is ~8k–39k, and ~90k in its whole life. Other routes not yet priced (C1) |
| Product scorecard | `venv/bin/python scripts/report.py --scorecard` |

**Function coverage.** General management updates this at each monthly review.
A function still at "none" after its first monthly review is a finding (D12).

| None | Thin | Partial | Strong |
|---|---|---|---|
| Audience, Monetization, Market intelligence | Strategy, Distribution, Editorial, Legal | General management, Product management, Finance, Security | Engineering, Reliability, Data |

## 2. This quarter's bets

None yet. Three are drafted for the owner's first planning session
(escalation `quarterly-planning-2026-Q4`, 2026-10-05): make the format ours
(PRD #7, #12); double weekly views (PRD #10, #3, #4); price the other routes
and pilot the best (C1, C8, C3). Until the owner sets them, the queue is
ranked on its effect on the path to revenue.

## 3. Work queue

Everything outside the channel product. Product work stays in PRD §0. The
statuses are the same as there, and `scripts/backlog_status.py` counts both
places.

| # | Status | Function | Item | Next step, and done when |
|---|---|---|---|---|
| C1 | ready | Strategy | **Price the revenue routes** | For each route: views needed, earnings per 1,000 views, eligibility, risk. Partner Program distance done (§1): 250–1,250× short on views. YouTube publishes no per-1,000 rate (its Shorts revenue page, 2026-10-05): creators keep 45% of a pool shared by engaged views, and music in a Short diverts part of its revenue to music partners. So the $0.01–$0.10 per 1,000 (~$30–$330 a month at the threshold) rests on secondary sources only. Left: price the C8 platforms. Done when the monthly review can say which route, if any, the current path reaches. |
| C11 | blocked: owner applies its commit patch (escalated 2026-10-05) | Data | **Collect the subscriber count** | Half of the Partner Program's bar, and no snapshot records it. Add it to the weekly statistics job's output, failing soft like the traffic snapshot so it can never cost the per-video one. The job already calls YouTube's channel endpoint, so it is one more field. Its workflow commits named files only, so a new file also needs a `git add` line: Propose that with `--patch`, or the data is silently dropped. Done when a snapshot carries it. |
| C3 | blocked: Reddit's pages refuse a shift's reads (terms, help centre and archive copy all failed 2026-10-05); needs a browser | Legal | **Reddit's terms for monetized use** | Secondary sources say the free API tier is non-commercial and that commercial use needs Reddit's written approval. Confirm from Reddit's own pages. Done when the risk is stated, with a proposed response if one is needed. |
| C5 | blocked: owner applies its commit patch (escalated 2026-10-05) | Audience | **Collect viewer comments into the repo** | The weekly analytics job already holds the YouTube keys, so it saves recent comments. That is a workflow change, so Propose. Done when a shift can read last week's comments. |
| C6 | done | Security | **Branch code never holds the Polly keys** | Done 2026-10-05: branch dry runs narrate silently over the real post, and only `main` gets the keys (`dry-run.yml`). The job-token half remains in `TECH_DEBT.md`. |
| C7 | ready | Market intelligence | **Scan comparable channels** | 5–10 Reddit-story or AskReddit-style Shorts channels: format, cadence, views, monetization signals. Done when there is at least one hypothesis with a test, or the finding that nothing transfers. |
| C8 | ready | Distribution | **What other short-video platforms require and pay** | TikTok, Instagram Reels, Facebook Reels: eligibility, payouts, and each one's rule on reused content, which YouTube's rules out for today's format (§4). TikTok's help pages and Meta's monetization policies render empty to a shift's fetch (2026-10-05); they need a browser. Done when Strategy can price them in C1. |
| C9 | ready | Strategy | **Learning throughput** | One experiment at a time allows about two decisions a month. Options: a second product as a test bed, parallel tests, more uploads. Done when a proposal reaches the owner. |
| C10 | blocked: C5 | Audience | **Publishing pipeline** | A shift drafts replies into a queue, and a workflow posts them, under ORG.md's publishing policy. |
| C12 | blocked: the owner's bet-1 choice (PRD #7, #12) | Editorial | **A public brand** | The company's working name is Show of Hands, and the channel's current name uses Reddit's. Once the kept originality step settles what the show is, check the trademark, domain and YouTube/TikTok/Instagram handles for the name (free), and propose whether and how to rename the channel. Renaming is the owner's. Done when the owner has decided. |

## 4. Risks

| Risk | Function | Likelihood / impact | Response |
|---|---|---|---|
| The format cannot be monetized under YouTube's reused-content policy | Legal, Editorial | **Confirmed** from YouTube's page (2026-10-05): "Content exclusively features readings of other materials you did not originally create, like text from websites" is not monetizable, and "applies to your channel as a whole". Today's format is exactly that. A second rule, generic or repetitive content, refuses content "that looks like it's made with a template" and "AI-generated content made with generic or unoriginal templates" / ends the Partner Program route | Bet 1 (PRD #7, #12) |
| Reddit's terms forbid monetized use of API data | Legal | Unknown / high | C3 |
| Shorts revenue is too small at any reachable scale | Strategy | High / high — the Partner Program threshold alone is 250–1,250× today's views (§1) | C1, C9 |
| Dependence on one platform (96.7% of views come from the Shorts feed) | Distribution, Strategy | Medium / high | C8 |
| Loss of the YouTube channel or the Google account | Security | Low / fatal | Quarterly account-security check |
| A runaway Polly bill | Security, Finance | Low / bounded by the budget action | `money_check.py` every shift; C6 |

## 5. Reviews

`scripts/cadence.py` reads this table to say what is due. A review updates its
own row when it finishes.

| Review | Last held |
|---|---|
| Weekly | 2026-10-05 |
| Monthly | 2026-10-05 |
| Quarterly prep | 2026-10-05 |
| Quarterly planning | never |
