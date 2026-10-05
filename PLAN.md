# Company plan

The company's status: its goal, the queue for everything outside the channel
product, its risks, and when each review last ran. The channel product's status
is in [PRD.md](PRD.md) §0, and who owns what is in [ORG.md](ORG.md). Read at
shift start. **Keep it short:** answered items leave, and settled history lives
in git.

## 1. Goal and scorecard

**Goal:** monetization, meaning revenue above costs (`DECISIONS.md` D12). The
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

None yet. The first quarterly planning session with the owner is due (§5).
Until then, the queue is ranked on its effect on the path to revenue.

## 3. Work queue

Everything outside the channel product. Product work stays in PRD §0. The
statuses are the same as there, and `scripts/backlog_status.py` counts both
places.

| # | Status | Function | Item | Next step, and done when |
|---|---|---|---|---|
| C1 | ready | Strategy | **Price the revenue routes** | For each route: views needed, earnings per 1,000 views, eligibility, risk. Partner Program distance done (§1): 250–1,250× short on views. Left: confirm the per-1,000 pay (secondary sources say $0.01–$0.10, so ~$30–$330 a month at the threshold) and price the C8 platforms. Done when the monthly review can say which route, if any, the current path reaches. |
| C11 | ready | Data | **Collect the subscriber count** | Half of the Partner Program's bar, and no snapshot records it. Add it to the weekly statistics job's output. Done when a snapshot carries it. |
| C3 | ready | Legal | **Reddit's terms for monetized use** | Secondary sources say the free API tier is non-commercial and that commercial use needs Reddit's written approval. Confirm from Reddit's own pages. Done when the risk is stated, with a proposed response if one is needed. |
| C4 | ready | Editorial | **Originality: what would make the format ours** | YouTube's page lists what it monetizes: "a critical review", "reaction videos where you comment", "a storyline and commentary", or content where "the creator is either visible in the content or explains how the creator added to the content". Turn the candidates (commentary, narrative, curation) into Product experiments with decision rules. Done when one is in PRD §0. |
| C5 | ready | Audience | **Collect viewer comments into the repo** | The weekly analytics job already holds the YouTube keys, so it saves recent comments. That is a workflow change, so Propose. Done when a shift can read last week's comments. |
| C6 | ready | Security | **Branch code never holds the Polly keys** | See `TECH_DEBT.md` (dry runs). Real narration is made by `main`'s code in its own job, or branch renders use only the free sample mode. A workflow change, so Propose. |
| C7 | ready | Market intelligence | **Scan comparable channels** | 5–10 Reddit-story or AskReddit Shorts channels: format, cadence, views, monetization signals. Done when there is at least one hypothesis with a test, or the finding that nothing transfers. |
| C8 | ready | Distribution | **What other short-video platforms require and pay** | TikTok, Instagram Reels, Facebook Reels: eligibility, payouts, and each one's rule on reused content. Done when Strategy can price them in C1. |
| C9 | ready | Strategy | **Learning throughput** | One experiment at a time allows about two decisions a month. Options: a second product as a test bed, parallel tests, more uploads. Done when a proposal reaches the owner. |
| C10 | blocked: C5 | Audience | **Publishing pipeline** | A shift drafts replies into a queue, and a workflow posts them, under ORG.md's publishing policy. |

## 4. Risks

| Risk | Function | Likelihood / impact | Response |
|---|---|---|---|
| The format cannot be monetized under YouTube's reused-content policy | Legal, Editorial | **Confirmed** from YouTube's page (2026-10-05): "Content exclusively features readings of other materials you did not originally create, like text from websites" is not monetizable, and "applies to your channel as a whole". Today's format is exactly that / ends the Partner Program route | C4 |
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
| Weekly | never |
| Monthly | 2026-10-05 |
| Quarterly prep | never |
| Quarterly planning | never |
