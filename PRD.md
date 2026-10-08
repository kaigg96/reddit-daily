# PRD: Reddit Shorts Pipeline — Video Quality Overhaul

| | |
|---|---|
| **Status** | See §0 below — the single tracker (this row restated it and fell out of date) |
| **Date** | 2026-07-18 |
| **Owner** | kaigg96 |
| **Implementer** | Automated tooling with full repo access |
| **Repo** | github.com/kaigg96/reddit-daily (local folder: `reddit-digest`) |

---

## 0. Status & delivery plan *(living section — update when anything ships)*

**Last updated:** 2026-10-08 · **Live format:** `v7` (opens on the question, merged 2026-09-25; earlier releases under **Shipped**). `integration/preview` is stale (releases merge straight to `main`). **Do not delete it:** `validate-release.yml` defaults to it and exits "nothing to validate" on a missing target *before* falling through to `main`, so deleting it silently retires the daily gate on live code.

> **Cadence model (revised 2026-07-22):** work is sorted onto two tracks by *whether we'll act on a change's individual result*, not by theme — a **bar-raising batch** (high-confidence keepers, shipped fast) and an **experiment backlog** (bets, isolated + baked with a pre-committed decision rule). The old "bake every version ~1 month" rule conflated attribution with validation; see §8 for the full rationale and the [Delivery plan](#delivery-plan) below for the concrete bucketing.

<a name="delivery-plan"></a>
### Delivery plan *(the single tracker — per-requirement detail lives in §6)*

**Shipped**
- `v2` — retention overhaul (2026-07-18): R0.1–R0.5, R1.1–R1.7 · plus audio-mix calibration, channel-name branding, no-AI-attribution scrub, basic branded thumbnail card (R2.3 partial)
- `v3` — packaging (2026-07-19): R2.1 title hygiene, R2.2 title-style A/B/C rotation
- `v4` — Sprint 1 bar-raising batch (2026-07-22, via `feature/sprint-1`): R3.1a question CTA, R3.3 auto-comment, R3.4 watermark, R3.5 subtitle tracks, R4.5 cron de-jitter — caption + comment live paths **verified in production 2026-07-27**
- Standalone (no version bump): R4.2 weekly analytics + digest (2026-07-20) · R1.3 b-roll library (2026-08-15, 7 clips) · offline reporting (2026-09-21) — `report.py --offline`, so a shift without YouTube secrets can still run the revert check · release check (2026-09-21, #16) — `report.py --release <version>` reads every upload at the same age. Verdicts: `v5` **keep**; b-roll **keep** (watch-seconds +22%); `v6` **keep** (2026-10-06, watch-seconds +10%, n=10)
- `v5` — suppression-risk screen (2026-08-23): R4.6, validated pre-merge (§6).
- **`v6` — merged to `main` 2026-09-19** (four branches: cost guardrails, Gemini thinking-timeout fix, R4.6 screen retiering, analytics zero-view fix).
- **`v7` — opens on the question (2026-09-25):** experiment #1 below, judged under its rule at the 2026-10-12 snapshot.

#### Next keepers

| Item | Status | Req | Decision rule |
|---|---|---|---|
| ~~Suppression-risk screen~~ ✅ `v5` · retiered `v6` | done | R4.6 | **Standing audit:** review `analysis/screen_log.csv` weekly; if skips look like false positives or exceed ~15% of candidates, narrow the prompt rather than revert (§6). |
| ~~Traffic-source telemetry~~ ✅ shipped | done | R4.7 | Search earns ~1.3% of views, so search-oriented work stays parked (§4). |
| ~~Make sample videos free~~ ✅ 2026-09-25 | done | — | `SAMPLE=1 venv/bin/python -m src.run` renders a fixed post over silent narration: no Reddit, Gemini or Polly call, always a dry run. It proves a **render** change is playable; a change to the Reddit, screen, Gemini or Polly path still needs a real sample (`dry_run.py request`), whose Gemini calls go to `SAMPLE_MODEL`'s separate free tier. |

#### Experiment backlog (isolated, pre-committed decision rule, ≥20-upload / ~2-week bake)

| # | Status | Item | Req | Decision rule (pre-committed) |
|---|---|---|---|---|
| 1 | baking | **Open on the hook, not the format label** — the first second currently shows the channel name and "TODAY'S TOP QUESTION" while the question starts being read. Give the question the whole opening instead; branding moves later. The question is pinned from frame 0; branding stays as the watermark. **✅ Live as `v7` from 2026-09-25.** Read at the **2026-10-12** snapshot, when its 20th upload is 7 days old | R1.x (new) | Ship as `v7`, one variable. Read `report.py --release v7 --min-uploads 20`: **keep** if median watch-seconds holds or improves; **revert** only if it drops by more than the detection limit the tool prints beside the verdict (12% at n≥8). Views never trigger (§5). **Length, pre-committed 2026-10-07, before the read:** `v7`'s posts ran 3s longer for reasons outside its code (§4). The rule stands, with #39's check that total watch time also holds (the tool applies it). Beside it, `--release` prints the gain within each length half. Credit it to `v7` only if it holds there beyond drift (10-07: +8%, n=9, does not). |
| 2 | parked: fires on 5 of 20 runs (2026-10-07, §4), too few for its rule to tell from drift; reopen on a ~50% topic lead at 7 days, or a rule reading the firings alone (~40 days) | **Topic/hook candidate ranker** — gate cleared 2026-09-11; slate telemetry live 2026-09-25 (§6) | R4.4 | Pick the best of the top 10 on hook strength + topic prior rather than always #1. After ≥20 uploads, `report.py --release <version>`: **keep** if median **watch-seconds** holds or improves; **revert** only if it drops beyond the detection limit the tool prints (#18). |
| 3 | baking: merged 2026-10-06; first NoStupidQuestions upload 10-07 evening | Subreddit rotation — *inventory for volume*. Runs alongside #10: each day's two uploads share a title style and split the subreddits, so both reads balance; a third subreddit would pin styles to subreddits (2026-10-01). | R4.1 | At ≥15 uploads each, `report.py --at-age 7 --compare subreddit=X`: drop any below AskReddit beyond the detection limit on watch-seconds (#18). Unlocks volume (§7). |
| 4 | blocked: #3's read (~2026-11-02 snapshot; fits the Gemini cap, §2) and the owner (#55, narration spend). Repeat guard built 2026-10-08; inventory does not bind (§4) | Posting volume 2 → **4**/day, the evidenced views lever (nothing we log predicts a hit, §4). Not 3: its best case, ×1.5 views, is under the ×2 that `--trajectory --metric views` can read (2026-10-07). Build: raise `CANDIDATE_LIMIT` (§4); add a concurrency group to the video workflow (TECH_DEBT) | — | After R4.1 proves inventory quality. **Keep** unless median watch-seconds falls beyond the detection limit (#18) or the 4-week view total falls; views per upload may dilute. |
| 5 | parked: proven English format first | Localization (per-language channels) | R5.1–R5.2 | Gated — requires a proven English format first (R5 localization gate). |
| 7 | blocked: the owner's stance (#55, which carries its spend). Merged off 2026-10-07 (`HOUSE_VOTE_RULE`); turning it on is a release with a real sample. Need not wait for rows 3 and 10: they split each day, so a flag day hits both arms evenly; read #7 within AskReddit (2026-10-07; `--release <v> --within subreddit=AskReddit`) | Two-voice reaction beat — **originality candidate 1 (bet 1, PLAN §2)**: YouTube pays for "reaction videos where you comment", not "readings of other materials" (PLAN §4). One quip is the cheapest step, not proof; it must react to the specific comment (template rule), inside the metadata call. | R3.2 | **Keep** unless median watch-seconds falls beyond the detection limit `report.py --release` prints, at 7 days on ≥20 uploads (#18); views never trigger. Keep → a fuller commentary step; revert → try narrative or curation. |
| 12 | blocked: #7 first (one experiment at a time; bet 1, PLAN §2); escalate any added Polly spend before building | **Host storyline — originality candidate 2**: a host setup line before the answers and a verdict line after them, length held. Curation folds in here (spec §6). | R3.6 | **Keep** unless median watch-seconds at 7 days on ≥20 uploads falls beyond the detection limit `report.py --release` prints (#18); views never trigger. Keep → the host's frame defines the show (C12). Revert, with #7 also reverted → bet 1 failed; the concept goes back to the owner. |
| 8 | blocked: the 2026-10-12 snapshot. Reader built 2026-10-06 (`--metric engaged_share`); `v6`'s 7-day snapshots predate the column, so read at 14 days | **Engaged-view rate** — since 2025 a Shorts "view" is any play start; the Analytics API's `engagedViews` keeps the older, stricter count, so their ratio is the share of plays that get past the opening. That is the variable #1 changes, and watch-seconds sees it only diluted by the rest of the video. **Collecting since 2026-09-24** (`engaged_views` in the weekly snapshot, filled from 2026-10-05) | R4.2 (ext) | **Hypothesis:** `v7` moves the engaged rate more than watch-seconds. **Test:** read `v6` vs `v7` on engaged/views once both have ≥8 uploads in a snapshot. A diagnostic beside #1's rule, **never a trigger**; #1 stays judged on watch-seconds as pre-committed. |
| 10 | baking: merged 2026-10-05; first upload 10-06 | **Weight titles toward style B** ("You…"). Views, 2026-09-28: B **+47% at 7 days, +41% at 14** (n=42 vs 87), in each era (+40% `v4`, +82% `v5`); +9% within Danielle's. | R2.2 | B:A:C = 4:1:1, keeping A and C as a control. Keep unless watch-seconds falls beyond drift at 7 days on ≥15 B uploads (#18). |
| 13 | blocked: the owner's Groq key and patch (#68, #69); merged switched off 2026-10-08 | **Move every AI call to Groq** (Legal, PLAN §4): its free tier bans training on what we send; Gemini's allows it, and Reddit's terms forbid that. It changes the video: the closing line comes from the metadata call, and the screen picks the post. | R4.6, R2.1 | Switch only once the screen replay passes on Groq with nothing inconclusive and a sample renders; ship as its own `FORMAT_VERSION`. **Revert** if `--release <v>` shows watch-seconds down beyond the detection limit at 7 days on ≥20 uploads (#18), or titles fall back on ≥4 of its first 20 (Gemini: 3 of the last 30). Read views beside it (#10); they never trigger. |
| ~~11~~ | done | **Retired 2026-09-28: b-roll clip `pexels_16482908`**, half its uploads buried at 7 days (§4). | R1.3 | Retired, no version bump (as R1.3). Each snapshot, `report.py --at-age 7 --by bg_clip --metric views`: retire any clip whose buried rate against the rest is under the corrected p it prints (pre-committed 2026-10-06; `pexels_15168364` watched). |

#### Research questions (answerable from data we already have)

The source of ready work that never waits on a sample video or costs money. When fewer than 3 items above are `ready`, add questions here (`/backlog` §1); each result becomes a finding (§4), a new question, or a backlog item, and **the row is removed once answered** (a test fails a push that leaves one).

| # | Status | Question | Test |
|---|---|---|---|
| R1 | blocked: 2 more dark-morbid uploads aged 7 days (n=10 at the 2026-10-05 snapshot, lead +12%) | **Does dark-morbid's lead survive more data?** (+27% at 7 days, n=9, all `v5`, so read within era; §4) | `report.py --at-age 7 --compare topic=dark-morbid` at n≥12. Holds at ~+50% → reopens R4.4 (§0 #2); otherwise recorded. |
| R3 | blocked: the 2026-10-12 snapshot (10-05: ≤7 per voice within `v6`/`v7`; refused) | **Does one narrator voice get fewer uploads distributed?** Buried (≤5 views): Danielle 11/67 vs Stephen 2/65 (pooled p=0.010); morning vs evening alike. 7 of the 9 Danielle-morning ones fall 09-06→09-19: likely a cluster (2026-10-04). Hits lean Stephen too (12/74 vs 5/75, p=0.07; 10-07) | Rerun `--by voice` and `--by slot` with `v6`/`v7`. Gap persists → propose a one-voice experiment; gone → recorded. |

#### Owner tasks (anytime, no version bump)
- ~~**B-roll library** (R1.3)~~ ✅ 2026-08-15 — 7 dark/moody Pexels clips live (`assets/broll/`, sources in CREDITS.md). Nine curated, two dropped at the R1.4 legibility gate for washing out white captions. Pipeline auto-switched off the procedural background; `bg_clip` logged per upload so per-clip performance is separable later. Expectation (§4): first-impression/swipe margin, not the watch budget.
- **Music variety** (R1.6): 2–3 more Audio Library tracks in `assets/music/`, sealed by `scripts/seal_assets.sh` (public repo).

---

## 1. Background & goal

> **Company context (2026-10-05, D12):** this is the Shorts channel's product
> document. The company's goal is monetization by whatever route, and its plan
> and organisation are in `PLAN.md` and `ORG.md`. The Partner Program target
> below is one route to that goal, not the goal itself.

This repo generates and uploads a YouTube Short twice daily from the top r/AskReddit post of the day (cron `23 0,12 * * *`; actual publish has drifted to ~04:50 and ~16:45 UTC — GitHub queue delay, see R4.5). Videos currently average **under 100 views each**. The owner's goal is YouTube Partner Program monetization, whose Shorts route requires **1,000 subscribers + 10M valid public Shorts views in a trailing 90-day window** (the long-form route is 4,000 watch-hours/12mo). At 2 posts/day, 10M/90d implies ~55K average views per video — the strategy is to (a) raise the floor via production quality and (b) raise the ceiling (hit probability) via better hooks and content variety.

Sub-100 views on Shorts means the algorithm's initial test pool (a few hundred impressions served automatically to every new Short) is not converting. The dominant signal for further distribution is **retention** (viewed vs. swiped away, average % watched), followed by engagement (likes/comments/shares per view). "Click rate" in the classic thumbnail sense barely applies inside the Shorts feed — the real analog is **surviving the first 1–2 seconds**. Titles/thumbnails matter mainly on search, channel page, and browse surfaces.

A secondary motivation: YPP review rejects "repetitious/duplicative" content. A TTS reading of Reddit comments over a static image is close to that line. The personality/production requirements below (motion, editing, commentary voice) also serve to make the content clearly transformed.

## 2. Starting system — the v1 baseline this PRD replaced *(historical; superseded at v2)*

At the time this PRD was written, everything lived in one notebook, `create_video.ipynb`: the top AskReddit post and 3 comments, Gemini keywords and title, Polly narration (Danielle or Stephen), a static MoviePy render with silent gaps and audio-only announcer segments, and an upload with a `#shorts #foryou` suffix. §3 lists what was wrong with it. The cell-by-cell description was compressed on 2026-10-06 (audit prune); it is in git history before that date.

**Environment (kept current — this block describes the system as it is today, not the v1 baseline above):**
- **Gemini model/endpoint:** `gemini-2.5-flash` on **`v1beta`** with `thinkingConfig.thinkingBudget = 0`. Thinking is disabled deliberately (2026-09-19): it added 30s+ of latency on prompts needing ~8 output tokens and was timing out, silently degrading ~25% of uploads. `v1` cannot express this — it rejects `thinkingConfig` with HTTP 400.
- **Runtime:** Python 3.10 on `ubuntu-latest`, entry point `python -m src.run`. Twice daily at `23 0,12 * * *` (off the hour to dodge Actions queue jitter), plus a `workflow_dispatch` with a `dry_run` input.
- **Secrets in Actions:** `REDDIT_*`, `AWS_POLLY_*`, `YOUTUBE_CLIENT_ID`/`_SECRET`/`_REFRESH_TOKEN`, `GEMINI_API_KEY`. Local dev reads the same names from `.env` (gitignored). `YOUTUBE_DATA_API_KEY` exists locally but is no longer used by any script.
- **OAuth:** the refresh token carries `youtube.upload`, `youtube.force-ssl` (comments + captions) and `yt-analytics.readonly`. The consent screen is published **in production**, so tokens no longer expire after 7 days (see README for the re-mint walkthrough).
- **Fonts:** Anton is committed to `assets/fonts/` and passed to `TextClip` by path — no system font installation, so CI and local renders are identical.
- **MoviePy 2.1.2** — 2.x API only; see Appendix A for the specific gotchas. (`moviepy.__version__` self-reports `2.1.1` despite the 2.1.2 pin — an upstream metadata quirk, not a wrong install.)
- **Gemini usage per run:** 1–4 screen calls (R4.6, capped by `MAX_SCREENED_CANDIDATES`) plus **one** metadata call covering title + keywords + CTA = **2–5 requests per run, 4–10 per day** (was 4–7 / 8–14 until the three metadata prompts were merged on 2026-09-19). ⚠️ **Corrected 2026-09-19: this is NOT comfortably inside the free tier.** The cap is **20 requests/day** for `gemini-2.5-flash` on this project (measured from the 429 body: `GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue=20`), so production alone is **40–70% of it**. Any local testing competes directly with live uploads, and a single screen replay is a third of the day's budget. The quota counts **requests, not tokens**, so the structural fix is fewer calls — the three metadata prompts were merged for exactly this reason. Reset is midnight Pacific ≈ 07:00 UTC, which falls *between* the two scheduled runs, so the ~05:00 UTC run is last in the window and the one exposed to a budget already spent. It shipped a raw title on 2026-09-20 for that reason. The per-consumer caps (production 10, release gate 8, a shift 8) still sum past 20 with no shared ledger — see TECH_DEBT.md. **Measured for volume (2026-10-05, PLAN C13):** a run screens at most `candidate_rank` candidates, and 80 of 84 runs logged rank 1 (none above 2; the last 40 all 1), so a typical run spends **2 requests** and production ~4/day. At 4 uploads/day that is ~8, plus ≤8 for the 08:17 release check: ~16 of 20, so **volume fits typically**. Only the theoretical worst case (5 per run → 20/day before the release check) breaks the cap. The free route for that tail is `MAX_SCREENED_CANDIDATES` 4 → 2 (worst 3/run → 12/day), at the cost of a run finding no post if two candidates in a row are skipped, which has not happened in 84 runs. Set it in the volume release, not before.

## 3. Diagnosis (why <100 views)

Ranked by expected impact:

1. **Dead air:** 5–6 half-second silent freezes (`gap_clip`) including one at t=0, before any speech. Shorts are won/lost in the first 1–2s.
2. **Zero motion:** a static frame for ~28s. The genre standard (and retention baseline) is constant background motion + word-timed animated captions.
3. **Text presented as a paragraph block** rather than word-by-word captions synced to speech — viewers read ahead, finish early, swipe.
4. **Two audio-only segments over a blank screen** ("top responses" announcer).
5. **No branding/persona** — nothing to subscribe *to*; content identical to dozens of larger channels posting the same daily post.
6. **Generic bolted-on CTA** after most drop-off has already happened; `#shorts #foryou` title suffix adds nothing (Shorts are auto-detected by aspect/duration) and reads spammy.

## 4. Objectives & success metrics

All metrics via YouTube Studio / Analytics API. The **≥ 14 days / ≥ 20 uploads** bake rule applies to **experiment-backlog** changes — the ones we'll act on (keep/revert/iterate); individual Shorts are high-variance, so never judge *a bet* on 1–2 videos. **Bar-raising keepers do not carry per-change bake** — they're kept regardless, so there's no decision to wait for; they're sanity-checked in aggregate. (See §8 for why this split is correct.)

**Primary metric is `averageViewDuration` (watch-seconds), not `averageViewPercentage`** — revised 2026-08-23. Avg-%-viewed is a ratio whose denominator we control: trimming a video inflates it without adding a single second of real watch time, so targeting it invites optimizing the proxy instead of the outcome (this mistake produced and then killed R1.8/R1.9 — see §4 Findings, Review 2). Watch-seconds cannot be gamed that way, and it is what separates the channel's top videos from the rest.

| Area | Metric | Baseline (2026-08-23) | Target |
|---|---|---|---|
| Attention | **Median watch-seconds** (`averageViewDuration`) | 9.0s (top-12 videos: 11.0s) | **≥ 12s** |
| Attention | Avg % viewed — *diagnostic only, never a target* | 50% (v4, n=52) | — (interpret only at fixed duration) |
| Distribution | Median views/Short, trailing 14d | 166 (v4, n=52; recent-era v1 was 28) | ≥ 1,000 (milestone 1) |
| Engagement | Likes per 100 views | ~1 | ≥ 3 |
| Engagement | Comments per 100 views | <0.5 | ≥ 0.3 |

**Comparisons must be age-matched.** Avg-%-viewed and views both drift with video age, so any cohort comparison (format versions, experiments, background types) must hold age roughly constant or it will measure age instead of the change.

Directional, not contractual — the algorithm is stochastic, and the strongest measured predictor of views explains only part of the variance (`r ≈ +0.34`). The system's job is to make every upload *worthy* of distribution and measurable (R0.2), so format versions can be compared honestly.

### Findings — data reviews

**Four a day was blocked by a repeat bug, not by inventory (2026-10-08, for #4).** The picker excluded only the last upload's title, so a post repeats whenever another run comes between: it did on 2026-07-20 (01:23 and 13:46, a manual run at 04:07 between). Today's rotation at four runs a day draws one subreddit four runs in a row, so a post still on top would ship again two runs later. Fixed: selection skips every title in the upload log. Inventory: AskReddit's top 10 left **4–8** eligible posts per run (median 6, n=20 runs with slate telemetry; 6 runs at exactly 4), so one subreddit can feed four a day, but on its thinnest days the fourth run has one candidate left and a screen skip (4% of screened candidates since 08-25) would cost the upload. #4's build should raise `CANDIDATE_LIMIT` (a Reddit fetch, no Gemini cost).

**`v7`'s videos run 3s longer, and its lead is mostly that length; the ranker would fire on 1 run in 4 (2026-10-07).** `v7`'s 24 uploads median **23.4s** against 20.3–20.4s for `v4`–`v6` (n=123; a shift that large in a 24-upload median came up in 2% of 20,000 random relabellings, against 19.8–21.5s in each earlier run of 24). `v7`'s code changes on-screen text only, and no setting that sets length has moved since July, so the posts got longer, not the format. `--release v7` reads watch-seconds **+25%** and flags the shift. Within long videos (`--at-age 7 --compare format_version=v7 --within video_length=long`) it is **+8%** (n=9 vs 69), inside drift; the short half has n=3. Read in the 12 October rule (§0 #1). **R4.4's firing rate:** `report.py --slate` at its 20th slated run, **5 of 20 (25%)**. A ranker changing 1 upload in 4 moves a release's median by about a quarter of its per-firing effect. To clear the 13% detection limit, each firing would need a ~50% lead. The largest current-format topic lead is +12% (dark-morbid, n=10, R1). Its own rule could not tell it from drift, so it is parked (§0 #2). Slate and screen labels agree on 12 of 19.

**Two plays in three do not count toward the Partner Program, and no logged trait changes that (2026-10-06).** The bar counts qualified (engaged) views, not play starts (PLAN §1). `report.py --engaged-share`, 2026-10-05 snapshot: **36%** of play starts on the last 90 days' uploads are engaged (11,397 of 31,815), 21% across the catalogue. Per upload (`--offline --by X --metric engaged_share`, lifetime, similar ages) the median sits at 0.29–0.32 for every title style, voice, length and slot, so the share moves only with what the video does, which is #1's variable. Title style B's view lead holds in engaged views (+60%, #10). Exploratory and one snapshot: re-read at a common age once the series allows (`--at-age 14`, from 10-12).

**Views are neither hit-driven nor flat; R4 lands between its thresholds (2026-10-06).** `report.py --concentration`, n=169 at 7 days: the top 10% of uploads earned **42%** of 31,494 views, and the biggest single upload **3%** (1,050). The rule's band was ≤30% broad / ≥50% hit-driven, so it is recorded and bet 2 keeps its total-views measure. The premise held: roughly 90% of channel-wide views arrive in an upload's first week (`--trajectory --metric views`: ~27,400 first-week views in W30–W39 of 30,889 gained over the same 76 days), so the back catalogue does not compound and the bar is uploads × first-week views. At 4 uploads a day, that is ~28,000 first-week views per upload against a mean of 186. **No logged trait predicts a hit (R5, same day).** `--at-age 7 --concentration --by F` (15 hits of 150) over title style, voice, topic, slot, video length, clip and title source: the lowest p was 0.10 (one-upload groups), and title style B was 0.25 (hit rate 14% against A's 9% and C's 7%), against the pre-committed bar of 0.007. Recorded; no candidate. The directions match the views findings above, and with 15 hits only a large effect could ever clear the bar.

**Alternating a test by day would not sharpen it; the noise is sample size, not the calendar (2026-10-05).** `report.py --placebo`, nothing switched, n=150 at 7 days: watch-seconds halves split by alternate days within the same 16 uploads differ by a median **12%**, against **13%** between consecutive batches of 8. So the 6–15% batch swing (above) is mostly the noise of 8-upload medians, and only more uploads per arm narrows it. This refuted the same shift's proposal to run tests on alternate days (PLAN C9). The lever for learning speed is volume (§0 #4).

**Comparable channels (2026-10-05, market scan; search-snippet figures, approximate).** Of eight Reddit-narration channels, every large one has a human voice or face and delivers a verdict (rSlash ~1.9M subscribers, Am I the Jerk? ~1.2M), and the TTS ones stay small even at volume (Reddit Short Stories: ~9 uploads/day since 2022, ~13k videos, ~1k views each, 7k subscribers). YouTube renamed "repetitious" to "inauthentic content" in July 2025, with the example "narrated stories with only superficial differences". Two **candidates, not findings**: (1) one first-person story ending on a verdict instead of an answer list (R4.1's story mode, §6), judged on watch-seconds like any release; (2) continuous-motion gameplay footage instead of b-roll, on weak evidence (TikTok accounts only). No named Reddit-narration channel was found demonetized.

**Watch time grows with length up to ~31s; past that it is unmeasured (2026-10-05, for TikTok's 60-second bar, PLAN §1).** Within `v5`, uploads over 20s earned 37% more watch-seconds at 7 days than shorter ones (13.0 vs 9.5, n=29/22, `--compare video_length=long --within format_version=v5`); `v6`/`v7` are refused as too thin. Observational, since longer posts differ in content too. No upload has run past 31.5s, so a 60-second format would need its own measured test on YouTube before any TikTok pilot. **Views do not follow length either way (2026-10-07):** within `v5` the long half earned 28% *more* views at 7 days (75 vs 54, n=29/22, inside views' 27–50% swing); pooled, the short half reads +10% only because eras differ; the top-10% hit rate is 11% long vs 9% short (Fisher p=0.79, `--concentration --by video_length`). So within 15–31s, trimming would not buy views, and a step that adds a line (bet 1) has no measured views cost.

**Looping the ending into the opening was dropped (2026-09-25):** `report.py --replays` finds 3/110 videos averaging over 100% viewed, so heavy replay is rare; light replay is unmeasured. Reopen only with a direct replay measure.

**Measurement capacity (2026-09-21, n=117 uploads read at 7 days old from the weekly snapshot series) — how big a change has to be before we can see it at all.**

Age-matching removes the age confound; it does not remove the calendar one. Read at a fixed age, with no change of ours in between, **median views move 27–52% between consecutive batches of uploads** (batch size 8–15) and **median watch-seconds 6–15%**. Half-month medians of day-7 views run 82 → 228 → 114 → 62 while the format was unchanged for most of that — a 2.8× swing inside a single version.

Three consequences, all binding:

1. **Views cannot carry a decision at this volume.** Any rule that reverts or rejects on a view drop smaller than ~50% is reading weather. The first run of the new release check duly ordered reverting both `v5` (−50%) and the b-roll library (−39%) — the last two things shipped, on one shared calendar swing. `report.py --release` now prints the detection limit beside every verdict and requires a drop to exceed it.
2. **Watch-seconds is judgeable and views is not** — a five-fold difference in noise, independent of, and pointing the same way as, Review 2's argument from gameability.
3. **A "keep" is not proof.** At 2 uploads/day nothing establishes a view effect under ~50%, so absence of a detected regression must never be written up as evidence a change worked.

External calibration (2026-09-21, secondary sources, **not adopted**): 50–500 views in the first 48 h is reported as the normal band for a sub-1k-subscriber channel, with occasional 5,000 outliers. Our day-7 median (62–228) sits inside it, which says the volatility is the platform's per-video lottery rather than a channel defect. The same sources claim Shorts ranking moved from swipe rate to watch time in 2026 — **our own data points the other way** (day-7 watch-seconds rose 9.0 → 10.0 → 11.5 by month while day-7 views fell), so it is recorded as a hypothesis, not a fact. They also push a 65%-retention threshold for sub-30s Shorts, which is the R1.8/R1.9 mistake Review 2 killed; explicitly not adopted.

**Title style is a measured null, and titles are the wrong surface anyway (2026-09-22, n=119 across three arms).** The A/B/C rotation (R2.2, shipped in `v3`) separates nothing: median watch-seconds A 10.0 / B 10.0 / C 9.0, at comparable median ages (38d / 32d / 33d). The age-matched two-way test puts A **11%** ahead of the rest — *below* the 12% detection limit the same tool prints, so it is drift, not an effect. Two consequences: (a) this is the first well-powered null the channel has produced, and it is evidence about the *surface*, not just the wording — `analysis/traffic_sources.csv` says **96.6% of views arrive through the Shorts feed and 1.4% through search**, so a title is barely a distribution lever here whatever it says; (b) the opening 1–2 seconds of *video*, which is where that 96.6% is won or lost (§1, §3), has never been experimented on. That asymmetry is why the opening-seconds item is now #1 in §0's backlog. **Not a reason to remove the rotation** — it costs nothing to keep, and removing it would spend a release slot to buy nothing. **Revised 2026-09-28:** null on watch-seconds still holds, but "barely a distribution lever" does not. Style B reads +47% on views at 7 days, and holds within each release era (§0, experiment 10).

**Review 2 (2026-08-23, n=66 logged uploads, live Analytics, ≥3 days old) — supersedes parts of Review 1.**

1. **Duration is NOT a lever — the earlier "shorten the video" conclusion was wrong.** `corr(duration, log views) = −0.17`; the top 12 videos and the rest have effectively the **same** median duration (19.2s vs 19.8s). What separates them is **watch-seconds** (11.0s vs 9.0s) and the avg-% that follows from it.
2. **Avg-%-viewed is a gameable proxy and must not be a target.** Watch-seconds are roughly flat against duration (`corr = +0.13`), so trimming a video mechanically inflates avg-%-viewed while adding zero real watch time. R1.8/R1.9 were built on exactly this mistake and are **cancelled** — they would have "passed" their decision rule while delivering nothing.
3. **What predicts views:** `corr(avg-%-viewed, log views) = +0.34` and `corr(watch-seconds, log views) = +0.34` — equal. Since duration doesn't differ between winners and losers, the differentiator is **content/hook quality**, not format geometry (promotes R4.4 to the top of the backlog). Note +0.34 leaves most variance unexplained: much of Shorts success is outside anything we currently measure, so treat R4.4 as improving odds per slot, not as a reliable lever.
4. **Loops are real upside that shortening cannot buy:** the best performers include a 17s video at **227% avg-viewed** (40s watched) and another at 100%. Watch-seconds above duration only come from content worth re-watching.
5. **Distribution gain from the overhaul confirmed and larger than first measured:** v4 median **166 views** (n=52) vs recent-era v1 median **28** (n=76) — roughly 6× (Review 1 estimated 3.5× on n=14).
6. **Methodological rule now binding: cohorts must be age-matched.** Avg-%-viewed *declines as a video ages* (broader, colder audiences). Same-week (3–9d) videos sit at ~65% regardless of background, while the older overall pool sits near 48–50%. Two consequences: (a) **b-roll shows no measurable retention effect** once age-matched (65.5% vs 64.9%) — an apparent advantage was pure age artifact; (b) Review 1's "retention didn't move" claim compared v4 against much older v1 videos and is **not trustworthy as stated** — the distribution half stands, the retention half is unresolved.

**R4.4 gate CLEARED (2026-09-11) — the topic prior survives the format change.** The gate review below said the ranker's topic prior was measured on pre-overhaul content and was therefore an assumption. Re-running R4.3 with an era split settles it.

**Spearman rho = +0.79** between the pre-overhaul and current-format topic orderings, across the 10 buckets with n≥3 in both eras. The strong tier (nostalgia, humor-absurd, dark-morbid) and the weak tier (life-advice, money-work, fame-celebrity) both hold, and the weak tier reads *weaker* on current content, not softer.

Validated three ways, because the headline rests on only 10 points:
- **Classifier independence.** All 106 current-era questions were re-labelled by hand against the same taxonomy: **93% agreement** with Gemini (7 disagreements, mostly film/TV questions filed as `fame-celebrity` and a sports question as `politics-news`). Substituting the corrected labels moves rho by **0.00** — the result is not an artifact of how gemini-flash buckets things.
- **Robust to the bucket floor:** n≥4 → +0.78, n≥5 → +0.76, n≥6 → +0.76.
- **No single bucket drives it.** Leave-one-bucket-out spans +0.72 (drop nostalgia) to +0.88 (drop `other`). That `other` is the biggest drag is expected — it is a grab-bag, not a topic.

**The one real sensitivity:** fitting the age model on only the *classified* videos rather than all era videos gives **+0.66**. Fitting on everything is the better choice (the age→views trend is topic-independent, so more data is strictly better), but it means the honest range is **+0.66 to +0.79** rather than a point estimate. Every variant is strongly positive, so the *direction* is solid and the magnitude is soft. That is enough to seed a ranker; it is not enough to weight one finely.

**Caveats that travel with the number:** current-era buckets run n=1–23, three are too thin to enter the correlation at all, and 163 pre-overhaul videos are excluded as unclassified by design (the re-run only tops up the era the question turns on).

**R4.4 gate review (2026-09-09) — both of the ranker's evidence bases are currently unusable.**

R4.4 Step 0 shipped 2026-08-23 to accumulate the rank counterfactual *before* building the ranker. Checking what it has produced:

1. **The rank counterfactual will not arrive on a useful timeline.** 35 uploads carry `candidate_rank`: **32 rank 1, 3 rank 2, nothing lower** — and all three off-rank cases were caused by R4.6 screen skips, not by the basic filters. `report.py --compare candidate_rank=1` correctly refuses a verdict at n=3. At ~9% of uploads the cohort reaches n=15 around **early December**, and it **cannot be backfilled**: Reddit's top-of-day for a past date isn't retrievable, so no historical reconstruction exists. (Until `--compare` was fixed the same query read 24 vs 75 and looked conclusive — the 75 were videos logged before the column existed.)
2. **The topic prior is measured on content we no longer make.** The ~1.6× spread R4.4 cites comes from `analysis/topic_performance.md` (n=607), whose own caveats say: *"Nearly all analyzed videos are pre-v2 format; re-run after v2 accumulates data."* Given that v1→v4 moved median views ~6× (Review 2 item 5), whether topic preference survives that format change is an **assumption, not evidence**. On the current format `report.py --by topic` has n=24 classified across 10 buckets — every bucket flagged thin.
3. **The firing rate is unknowable from the current log.** The mechanism is a narrow exception (top candidate in a weak tier **and** another top-few candidate in a strong tier), but the log records only the *selected* post's topic, never the slate we passed over. So R4.4's own ≥20-upload bake cannot even be scheduled — it might need months to accumulate 20 firings.

**Recommendation: re-run R4.3's topic analysis on the current-format cohort before building anything.** It is pure analysis — ~107 Gemini title classifications, since `analysis/topics_cache.json` covers the v1 era and holds only 1 of the 108 logged uploads — and it tests the single assumption R4.4 rests on. If the topic spread survives on v2+ content, the topic exception can ship on that evidence and the rank gate is droppable as a nice-to-have that was never load-bearing. If it does not survive, R4.4's premise needs rework and the build is avoided. Either way the answer arrives in an afternoon instead of in December. **Owner decision required** — this changes what "supported by data" meant when Step 0 was written.

**First current-format topic reading (2026-09-25) — a lead, not evidence.** `report.py --at-age 7` now age-matches interleaved fields (one snapshot of today read the recent-heavy topic cohort 11d vs 17d, and `compare` refused it). At 7 days, dark-morbid holds **14.0 vs 11.0 watch-seconds (+27%, n=9 vs 31)**, but at 3 and 14 days it is n=5 and the 3-day read points the other way. The same tool finds voice null (Danielle 10.0 n=53, Stephen 10.0 n=63) and upload slot inside drift (morning +5–10%, n≈58 each; #6 dropped). Question length is the one clear gap: long questions (>63 chars) **11.0 vs 9.0 watch-seconds (+22%) at every age**, but they make ~2s longer videos (21.3s vs 19.2s median) and a *lower* avg-% (49.6 vs 58.7), and **within each half of video length the gap vanishes** (−5% to +9%, `--within video_length=…`): it is length, not the question. Dropped. **Nor does addressing the viewer (2026-10-03):** questions saying "you" read +5% at 7 and 14 days (`--compare question_person=you`, n=74 vs 57) but flip sign by era (−5% `v4`, +9% `v5`). Null. The residue matters more: **videos over ~20s hold 11.0 vs 9.0 watch-seconds (+22%, n=61/56)** — duration does not predict views (Review 2), but it does move the metric every release is judged on. `v5`/`v6` did not shift length (20.4s vs 20.3s); the b-roll switch did (21.1s vs 19.3s at a common age), so part of its +22% is length — keep stands. `--release` now prints each cohort's length and flags a ≥1s shift, so `v7` is not judged on length. **Read releases at 7 days, no sooner and no later** (`insights.early_read_stability`, rank correlation of each upload's readings from different snapshots): 3→7 days ρ=0.22 (n=69), 7→14 days ρ=0.95 (n=108). **Length trades seconds for views:** total watch time (`--metric total_watch_s`) is flat across `video_length` (+3% at 7d, −13% at 14d), so watch-seconds alone rewards lengthening — escalated as a narrow trigger change. Not enough to seed R4.4's prior; re-read queued in §0.

**Incidental (not actionable on its own):** `topic_performance.md`'s upload-slot table is era-confounded and its caveats explicitly forbid rescheduling from it. Noting it only because it intersects the publish-drift item in TECH_DEBT: the second daily slot has drifted from ~12:xx UTC (+0.42 median residual in that table) to ~16:45 (−0.18 to −0.47). **Age-matched read (2026-09-30): no consistent slot effect.** `--at-age 7 --compare slot=morning` gives morning +17% on watch-seconds in `v4` (n=28 vs 29) but −12% in `v5` (n=25 vs 26); the pooled +10% (11.0 vs 10.0) is within the ~1.0s drift. Upload time need not constrain R4.1's slot balancing or #4's added slots.

**One b-roll clip looks suppressed; voice's views lead is era mix (2026-09-28).** Earlier clip and voice reads used watch-seconds only. On views at 7 days, `pexels_16482908` left **8 of 16 uploads at ≤5 views** (1, 5, 1, 5, 1, 3, 0, 0), against 3 of 62 on the other clips; within `v5` its median is 5 vs 94. Watch-seconds barely differ (10.5 vs 12.0), so viewers who get it watch; it is not shown. Cause unknown: a widely reused stock clip tripping reused-content detection is one guess. Stephen's pooled +50% views is mostly composition: he read 37 of 57 `v4` uploads, a high-view era; within era +6% `v4`, +42% `v5`. `report.py --compare` now warns on such uneven mixes. Raw titles are also `v5`-heavy (67% vs 37%); within `v5` they still lean worse on views (32 vs 94, n=7, refused). **Reuse is not the cause (R4, 2026-10-04):** without that clip, a clip's uses 1–4 were buried 1/24 and later uses 3/37 (p=1.0), so it is that clip, not reuse. `report.py --by clip_use` keeps it checkable.

**A failed title costs no watch-seconds (R2, 2026-09-28).** At 7 days, raw-question titles read **11.0 vs 10.0** (`--compare title_source=raw`, n=11 vs 120), so title reliability is not worth work. The title call is **not** dropped on that: views read 66 vs 130 (−49%) and total watch time −67%. Views swing 27–50% at fixed age here, so that is not proof titles drive reach, but it is too large to bet against, and title, keywords and CTA share one merged call, so dropping the title frees no Gemini request. **Length is not the mechanism (2026-10-04):** raw titles run ~64 characters, generated ~41, but within generated titles `--compare title_length=short` reads views +16% (132 vs 114, n=63 vs 57, inside the noise) and watch-seconds −9%, far short of raw's −49%. Only 9 generated titles reach 55+ characters, so raw lengths themselves stay unread; no length cap is warranted.

**Nothing we log makes hits, and views fell for no logged reason (2026-10-07).** The top 10% of uploads earn 42% of 7-day views (`--concentration`), so a field that made hits would be worth more than one that avoids zeros. `--by <field> --metric views` now tests each group's share of its own release's top 10% (pooled within formats): **title style, topic, voice, clip, slot and question length all null** (closest: Stephen 12/74 vs Danielle 5/75, p=0.07). Title B lifts the median (#10) but makes no more hits (7/49). Engaged share of views, the bar's unit, is also flat across every field within a release (b-roll vs procedural 0.32 vs 0.32 within `v4`; voice 0.32 vs 0.30; style A/B/C 0.31/0.29/0.32), so B's views lead carries into engaged views whole. **The September drop** (views per upload ×0.59, last 4 weeks vs the 4 before, a cliff in W37) **is not the retired clip:** without it, still ×0.65 per upload (173 vs 266; `--trajectory --metric views --within 'bg_clip!=pexels_16482908.mp4'`), **nor W37–W38's failed titles** (×0.66 without them; W37 still 84 an upload). It lands in both slots (×0.57, ×0.60) and both voices (×0.59, ×0.73), per upload; voice totals alone mislead (×0.41 vs ×1.11), as Danielle read more of the recent weeks. Whether it was the channel's distribution cannot be read: the back catalogue earns **0.9%** of views (~3 a day, `--catalogue`), too few to show a step. Views gained in the week to 10-05 (617 a day) are the series high, so the drop may be passing; the 10-12 snapshot will say. Consequence for the strategic line below: no measured lever raises a slot's hit chance, so **more slots (#4) is the one views lever with evidence behind it**, and bet 2's W36–W39 baseline is not depressed by a cause already fixed.

**Gemini silently degraded ~25% of uploads for two weeks (found 2026-09-19).** `gemini-2.5-flash` thinks by default; a title call was measured spending **546 reasoning tokens to emit an 8-token title, taking 33.1s** against a 30s timeout. The call fails soft, so nothing broke loudly — the run just shipped the raw Reddit question as its YouTube title. Rate by week: **0% in W29–W32, then 29% (W37) and 25% (W38)**. `src/llm.py` had not changed since v4 in July, so this was environmental. A live screen replay the same evening lost **4 of 5 calls** to `ReadTimeout`. Disabling thinking puts the same call at **0.6s**.

Three consequences worth carrying forward:
1. **The R2.2 title-style comparison is contaminated and the contamination is uneven** — 10 of 127 rows record a style that was never applied (A 7% / B 12% / C 5%, and 23% of the last 30). That biases the cohorts rather than just adding noise. Fixed going forward; historical rows are **not** backfilled, since rewriting production history on an inference is an owner call.
2. **Fail-soft without telemetry is indistinguishable from working.** Three of the four Gemini call sites left no trace when they failed; this was only findable by comparing `video_title` back to `post_title`. Now logged as `title_ok`/`keywords_ok`/`cta_ok`, the same pattern as `caption_ok`. This is the third time the same lesson has landed (`caption_ok` 2026-09-07, `screen_source` 2026-09-09).
3. **The free-tier cap is 20 requests/day, not the few hundred assumed** — measured from the 429 body. The quota counts *requests*, not tokens, so the lever is fewer calls: merging keywords + title + CTA into one `get_metadata` call (2026-09-19) took production from 8–14/day to **4–10**. That is still 20–50% of the cap, and local work competes with live uploads. See §2 and TECH_DEBT.

**Traffic-source baseline (2026-09-07, R4.7 first snapshot).** Distribution is the Shorts feed and essentially nothing else. On the current-format cohort (`logged_uploads`, n=103): **Shorts feed 96.7%**, other YouTube pages 1.8%, **search 1.3%**, everything else < 0.2%. Channel lifetime is barely different (93.7% / 2.4% / 3.4%) — the older v1 content drew *more* search share than what we ship now, so the SEO surface is not something the overhaul lost, it was never large.

Consequences:
1. **Search-oriented work is not worth revisiting** at this scale. Tags, search-shaped titles and the SRT track earn ~1.3% of views; even tripling that moves total views by ~3%. Keep them (they cost nothing and the SRT serves accessibility), but do not build for them.
2. **The thumbnail question is settled the same way** — R2.3's full version was deferred because thumbnails don't render in the Shorts feed, and the surfaces where they do render (channel pages, search, browse) are 2.4% + 1.3% + 0.15% combined. Leave it deferred.
3. **Retention on the feed is the only lever that matters**, which is the same place §4 Review 2 and R4.4 already point.
4. Re-check rather than re-derive: `channel_7d` rows accumulate weekly, so a genuine shift in the mix will show up in the series instead of needing another investigation.

**Review 1 (2026-07-27, n=14, two snapshots) — retained for history; items 1 and 2 below are superseded above.**

1. ~~Production quality moved distribution, not retention~~ — distribution finding confirmed (and revised upward to ~6×); the retention half was age-confounded (see Review 2 item 6).
2. ~~Fixed watch budget ⇒ length is the retention lever~~ — the *observation* (viewers give ~9–12s) holds; the *inference* (therefore shorten) was wrong (Review 2 items 1–2).
3. **Views and retention are decoupled at this scale** — holds, and strengthened: topic/hook drives expansion more than format geometry.

Strategic implication (unchanged): 10M views/90d ≈ 110K/day vs the current ~1–2K/week — floor-raising alone can never cover that distance. Sequencing goal: maximize hit probability per slot (hook, topic), then multiply slots (volume after R4.1).

## 5. Constraints & guardrails (binding on the implementer)

**Two kinds, and the difference matters.** Marking everything "binding" made the
whole section unchallengeable, so a cost that recurred for weeks — the 20/day
Gemini cap degrading real uploads — was managed around every time and never
questioned. That is the wrong outcome: a constraint that costs more than it
saves should be *proposed against*, not silently absorbed.

- 🔒 **Inviolable** (1, 2, 6, 7, 8, 9): the owner's money, the safety guard that
  stops development touching the live channel, secrets, licensing, platform
  policy. Not open to challenge. Changing one needs the owner even to *discuss*.
- 🔄 **Current choices** (3, 4, 5, 10): true today, and reasonable, but they
  are decisions rather than laws. **Open to challenge with justification.**
  Bring evidence that the constraint costs more than it buys, a concrete
  alternative, and its cost — then escalate it (`scripts/escalate.py`). The
  owner decides; a shift does not lift one unilaterally.

Finding these is the project-management lane's job, not something that has to
be pre-written here.


1. 🔒 **No new spending until the channel earns money.** No new paid services, and no growth in what existing ones cost — Polly stays at its current line (no. 2). **Owner, 2026-09-25:** *"spending money is not on the table until the channel is actually earning money somehow, but pretty much anything else is on the table."* Unlocks only when the channel earns revenue (e.g. the YouTube Partner Program); until then, do not raise spending proposals. **A cost constraint is therefore a creative problem, not a purchase** — the project-management and research lanes' job (`/backlog` §3). Was 🔄 "$0 budget" until this ruling.
2. 🔒 **AWS Polly is the one line item that costs the owner real money — treat call volume as the constraint.** Neural is $16/1M characters and every segment is synthesized **twice** (mp3 + speech marks), so characters bill double. Production is ~910 billed chars/video ≈ **$0.90/month** at 2/day, and must stay in that range. The exposure is not per-video cost but **bulk synthesis**: 10,000 test renders is ~$144, and 10,000 calls at Polly's 3K-char cap is ~$960. **No bulk synthesis, no un-capped retries, reuse `assets/gen/` audio when iterating on visuals, and ask the owner before any deliberate batch job.** Enforced in code by the per-process budget in `src/tts.py` (`POLLY_CHAR_BUDGET`) — prose is not an enforcement mechanism. **The neural engine is a deliberate paid quality choice** (the owner is past the 12-month free tier and pays from the first character): standard voices are 4x cheaper and would save ~$0.65/month while degrading the channel's core audio — never make that trade, and don't move to the pricier generative/long-form engines without asking either. Cost work here means removing wasted calls, never reducing audio quality. Full rules in [CLAUDE.md](CLAUDE.md) §1.
3. 🔄 **Gemini's free tier is a shared daily request budget**, not per-process: local analysis and the live 2x/day pipeline draw on the same key, and exhausting it silently degrades real uploads to keyword-backstop screening and un-generated titles (observed 2026-09-10 — see TECH_DEBT.md). Budget local Gemini work rather than running it opportunistically. **Challenged 2026-09-22, decided 2026-09-24 (#22):** no paid tier; free routes accepted. The allowance is counted **per model** (our 429 names `GenerateRequestsPerDayPerProjectPerModel`), so new Gemini work goes on a second model with its own allowance (R4.4's slate call, `SLATE_MODEL`), and the model behind shipped titles and the screen stays as it is.
4. 🔄 **100% automated per-video.** No human step per upload. One-time setup tasks (asset curation, OAuth re-consent) are allowed and must be clearly documented in the README when introduced.
5. 🔄 **Must run headlessly on `ubuntu-latest`** GitHub Actions, twice daily, within reasonable job time (< 30 min).
6. 🔒 **DRY_RUN guardrail (build first — R0.1).** All development/verification runs must use DRY_RUN. **Never upload to the live channel, post comments, or mutate `prev_post.txt`/logs during development.** ~~The first live run of any new format version requires explicit owner approval.~~ **Revised 2026-09-19:** a new format version goes live once the automated gates pass (tests green, dry run produces a playable MP4, `FORMAT_VERSION` bumped, one variable per release) — see §8. The DRY_RUN guardrail itself is unchanged and still absolute.
7. 🔒 **Never commit secrets.** `.env`, `client_secret.json`, `token.json` stay gitignored. (`praw.ini` was removed 2026-08-23 — Reddit auth reads `REDDIT_*` from the environment.) When extending the workflow's commit step, `git add` only the specific intended files (never `-A`).
8. 🔒 **Licensing:** every committed media asset (b-roll, music, SFX, fonts) must be free for commercial use without attribution (CC0/Pixabay License/Mixkit License/YouTube Audio Library/OFL fonts) and its source URL recorded in `assets/CREDITS.md`. No gameplay footage of copyrighted games, no clips with embedded music/watermarks/logos/visible people prominently featured.
9. 🔒 **Policy:** no fake engagement, no engagement pods, no view manipulation, no posting-frequency increase as a substitute for quality. Existing content filters (NSFW/profanity/emoji) must remain.
10. 🔄 **Repo hygiene:** each committed b-roll/music file < 25 MB; total new committed assets < 300 MB. (If the library needs to grow beyond that later, move to GitHub Release assets + `actions/cache` — out of scope now.)

## 6. Requirements

**Requirement IDs are stable identifiers, not a sequence.** The leading digit is a *thematic family* — **0** enabling · **1** retention · **2** packaging · **3** engagement · **4** content/measurement · **5** localization — and families scatter across delivery buckets (e.g. R4.2/R4.3 shipped while R4.5 is Sprint 1 and R4.1/R4.4 are experiments). Sequencing is by **bucket** below, matching the [Delivery plan](#delivery-plan) in §0. Legacy **P0–P3** tags on shipped items just record the order they were built in.

### Shipped (v2–v3)

*(Retained as build reference. Which version each landed in is in the §0 status table; grouped here by thematic family.)*

**Enabling — R0.x (shipped v2)**

#### R0.1 — DRY_RUN mode — **P0**
- Env var `DRY_RUN` (truthy → dry run). When set: render the full video to `assets/`, print the would-be title/description/tags/CTA-comment, and **skip** YouTube upload, thumbnail set, comment posting, and `prev_post.txt`/log mutations.
- Add a `dry_run` boolean input to the workflow's `workflow_dispatch` (default `false`) wired to the env var, so CI dry runs are triggerable. Scheduled runs remain live.
- **Acceptance:** `DRY_RUN=1` local run produces a playable MP4 and touches nothing remote; grep confirms every mutating call is behind the flag.

#### R0.2 — Upload/experiment log — **P0**
- Append one row per successful **live** upload to `upload_log.csv` (committed back by the workflow alongside `prev_post.txt`): `timestamp_utc, video_id, subreddit, post_title, video_title, title_style, voice, bg_clip, music_track, format_version, duration_s`.
- `FORMAT_VERSION` string constant in code; `"v1"` = pre-overhaul; bump on each release (`v2` = retention overhaul, `v3` = packaging, etc.). This is the backbone that makes every experiment in this PRD measurable against YouTube analytics (join on `video_id`).
- **Acceptance:** header row + append logic; workflow commit step updated to add exactly `prev_post.txt upload_log.csv`; dry runs don't append.

#### R0.3 — Notebook → module refactor — **P1 (recommended, not optional in practice)**
Nearly every requirement below touches Cell 7's monolith (the notebook's single video-assembly cell); refactor first: `src/` package (suggested: `content.py` (Reddit), `llm.py` (Gemini), `tts.py` (Polly), `video.py` (assembly), `youtube.py` (upload/comment), `run.py` (orchestrator reading env)). Workflow runs `python -m src.run` instead of nbconvert (drop the nbconvert install). Keep or delete the notebook; if kept, it must not be the executed path.
- **Acceptance:** `DRY_RUN=1 python -m src.run` produces an equivalent video locally; a `workflow_dispatch` dry run passes in CI.

#### R0.4 — Committed brand font — **P0** (prerequisite for R1.2)
- Commit an OFL display font to `assets/fonts/` — recommended: **Anton** (ultra-bold, condensed — the genre standard look), downloadable from the google/fonts GitHub repo (OFL license; commit the license file too). Pass the **file path** to `TextClip(font=...)` everywhere; delete the Lato/Arial try/except. Record in `assets/CREDITS.md`.
- **Acceptance:** identical rendering locally and in CI; no font-name resolution at runtime.

#### R0.5 — Hygiene fixes — **P2**
- Gitignore `*TEMP_MPY*` moviepy temp files; fix thumbnail upload mimetype (`image/png`); sanitize Gemini title output (strip wrapping quotes/newlines, collapse whitespace, hard-cap ≤ 100 chars, fallback to `reddit_title`); set `selfDeclaredMadeForKids: false` in upload status; switch category to 24 (Entertainment).

**Retention overhaul — R1.x (shipped v2)**

#### R1.1 — Kill all dead air; hook at frame zero — **P0**
- Remove every `gap_clip`. Remove the `question.mp3` / `top_responses.mp3` announcer segments entirely (their framing moves to a persistent overlay, R1.5). Title narration begins at t ≈ 0 (first spoken word audible within 0.3s).
- Segment boundaries become hard cuts, optionally with a short (≤ 0.4s, non-blocking — overlap, don't insert silence) whoosh/pop SFX at ~-12 dB (R1.6 assets).
- **Acceptance:** ffprobe duration ≈ Σ(speech segments); extracted frame at t=0.3 shows the title caption mid-render; no silent stretch > 0.25s anywhere (verifiable with `ffmpeg -af silencedetect`).

#### R1.2 — Word-timed animated captions — **P0**
- For each Polly synthesis, make a **second** Polly call with `OutputFormat='json', SpeechMarkTypes=['word']` (same Text/VoiceId/Engine — timings align with the mp3). Response is newline-delimited JSON: `{"time": <ms>, "type": "word", "start": …, "end": …, "value": "…"}`.
- Replace static text blocks with karaoke-style captions: 1–3 words on screen at a time, Anton font ≥ 90px, white fill, black stroke (`stroke_color='black'`, `stroke_width≈8`), centered in the middle band of frame (safe from the Shorts UI: keep text inside x∈[60,1020], y∈[250,1500]). Each word group appears within ±150 ms of its speech mark. Applies to title, comments, reaction (R3.2), CTA (R3.1).
- Implementation: one `TextClip` per word group with `.with_start()/.with_duration()`, composited; ~60–100 clips per video is fine. Optional polish (P3): current-group scale "pop" (e.g., `resized` 1.0→1.08 over 0.1s).
- **Acceptance:** frames extracted at 3+ speech-mark timestamps show exactly the expected word group; a caption-timing unit check asserts group start times equal mark times within tolerance.

#### R1.3 — Motion background — **P0**
- New `assets/broll/` library: **10–15 vertical loopable clips**, sources: Pexels / Pixabay / Mixkit (free commercial licenses). Curation guidance: satisfying/abstract/scenic motion (kinetic sand, marble runs, drone coastline, timelapse, macro ink-in-water, rain on glass); ≥ 720×1280; 10–30s; re-encode to 1080×1920 (crop-to-fill) H.264 CRF 26–28, strip audio; target 5–15 MB each. Provide `scripts/prep_broll.py` (ffmpeg wrapper) for normalization.
- Runtime: pick a random clip (log it, R0.2), random start offset, `subclipped` to length, loop via `vfx.Loop` if short, muted, base layer under captions. A subtle slow zoom on top is optional polish.
- **Fallback (as-built):** if `assets/broll/` is empty/missing → a procedural drifting-glow animation generated in code (`src/background.py`). The originally-specced Ken Burns pan over `bg.png` was never implemented; the procedural background proved better and `bg.png` was deleted in the 2026-08-23 workspace cleanup. The pipeline must never render a fully static frame again.
- One-time setup task (owner or implementer-with-browser): download/curate the clips per guidance; record sources in `assets/CREDITS.md`. Alternative if fully-automated sourcing is preferred: free Pexels API key as a new secret + fetch script (decision: **Open Question OQ-1**).
- **Acceptance:** two frames 3s apart are visibly different (pixel-diff > threshold) in every segment; b-roll audio absent; CI artifact plays smoothly.

#### R1.4 — Readability layer over motion — **P0** (part of R1.3/R1.2)
- Captions must stay legible on any b-roll: black stroke per R1.2 **plus** a subtle dark scrim behind the text band (e.g., semi-transparent rounded rect at ~35% opacity) or global slight darken of the b-roll (`multiply` ~0.85). Implementer picks whichever renders cleaner; verify against the brightest clip in the library.
- **Acceptance:** extracted frames over the brightest clip show unambiguous legibility.

#### R1.5 — Persistent context header + progress cue — **P1**
- Small persistent header near the top (inside safe area): the question in compact form on comment segments, or a fixed brand line — plus a **progress badge** ("1/3", "2/3", "3/3") during answers. Signals finite length; carries the "top answers" framing dropped in R1.1.
- **Acceptance:** frames during each comment show the correct badge.
- **As-built additions (owner feedback):** the question stays pinned across all answers and the outro (only the badge swaps); short answers hold ≥2.0s on screen (`MIN_COMMENT_DISPLAY`).

#### R1.6 — Licensed music + SFX — **P1**
- ~~Replace `funk_bg_lower.mp3` (unknown license)~~ *Resolved 2026-07-18: owner confirmed the track is from the YouTube Audio Library — license-clean.* Remaining (optional): add 2–3 more Audio Library tracks to `assets/music/` for per-video variety, randomly rotated, logged (R0.2). Keep music ~9–10 dB under speech; optional final `ffmpeg loudnorm` pass to ≈ −14 LUFS.
- Add 2–3 CC0 transition SFX for R1.1.
- **Acceptance:** `assets/CREDITS.md` lists sources/licenses for every audio asset in the repo; old track deleted.

#### R1.7 — Duration guard — **P2**
- Assert and log total duration; target 20–40s. If assembled duration > 45s, drop comment 3 (prefer shorter over longer). Never exceed 60s.

**Packaging — R2.x (shipped v3)**

#### R2.1 — Title hygiene — **P1**
- Remove the `" #shorts #foryou"` suffix (auto-detection makes it useless; it costs characters and credibility). Description: keep question + answers + link; trim hashtags to ≤ 3 (`#AskReddit` etc.). Sanitization per R0.5.

#### R2.2 — Title-style rotation experiment — **P1**
- Three Gemini prompt variants: **A** curiosity rephrase (current), **B** direct-address second person ("You'll never guess…" / "Which of these are you?"), **C** number-led ("3 answers that…"). Select deterministically (e.g., `day_of_year % 3`), record `title_style` in `upload_log.csv`. Evaluation happens offline against analytics (R4.2) — no in-code winner-picking.
- **Acceptance:** style distribution roughly uniform across a week of dry-run simulations; logged correctly.

**Measurement — R4.2/R4.3 (shipped; landed ahead of the R3 work — more evidence the old phase order was fiction)**

#### R4.2 — Weekly analytics pull — **shipped ✅ (P2)**
- Second workflow (weekly cron): YouTube Analytics API v2 (`yt-analytics.readonly`) `reports.query` with `dimensions=video` for recent uploads → append `analytics.csv` (committed): views, likes, comments, shares, averageViewDuration, averageViewPercentage. Join key: `video_id` from `upload_log.csv`. Note: impressions / swipe-rate may not be exposed by the API (Studio-only) — implementer should verify current API surface and include them only if available.
- This closes the loop: every experiment in this PRD becomes evaluable from two committed CSVs.
- Also append a weekly snapshot for **all** uploads so views@7d / views@28d deltas become computable going forward (see R4.3, which otherwise had only single-snapshot data). **As-built:** this merged into the single file `analysis/analytics_snapshots.csv` rather than a separate `stats_snapshots.csv` — the Analytics API returns views/likes/comments alongside the retention metrics, so two files would have been redundant.
- **As-built (2026-07-20):** single-file design — `weekly-analytics.yml` Mondays 06:00 UTC appends `analysis/analytics_snapshots.csv` (Analytics API over OAuth; no Data API key in CI; impressions confirmed not API-exposed) **plus a weekly digest GitHub issue** (owner-approved layout: status-in-title / pipeline health / performance / top video / TODOs; emails via GitHub watch notifications; anomaly flags expire after 7 days). **Deferred until scale warrants** (owner 2026-07-20): engagement-rate scoreboard (when median views/Short ≳500), per-video `subscribersGained` (when subs ≳100), exact rolling-90d windowed views query, experiments section in the digest.

#### R4.3 — Historical content-performance analysis — **shipped ✅ (P1, sequencing-independent)**
- **Motivation:** ~2 uploads/day since early 2025 means several hundred published Shorts whose descriptions embed the complete content (question + 3 answers). This is an unused dataset for learning which topics and phrasings get distributed vs. suppressed. Suppression is a real mechanism, not just taste: advertiser-unfriendly topics (tragedy, sex-adjacent, drugs, ongoing legal/news stories) can receive limited distribution on Shorts. Note the honest framing: low views for a topic may mean algorithmic suppression *or* weak audience interest — the analysis can't fully separate them, but both point to the same action (avoid the topic), so the ambiguity doesn't block the mechanism.
- **Data acquisition — originally no OAuth needed.** All required fields (title, description, tags, publishedAt, duration, viewCount, likeCount, commentCount) are public metadata, so this shipped against a free **YouTube Data API key** (avoiding a dependency on the not-yet-unblocked Phase 3 re-auth; see OQ-4): derive the uploads playlist from the channel id (`UC…` → `UU…`), page through `playlistItems.list`, then `videos.list(part=snippet,statistics,contentDetails)` in batches of 50 (1 quota unit per call — the whole channel costs <20 units of the 10k/day budget). Output: `analysis/channel_videos.csv`. **Superseded 2026-07-21:** now that OAuth is live, this script was migrated onto the same authenticated client the other reporting scripts use (`src/analytics.py`), eliminating a second auth mechanism and a hardcoded channel-ID constant — see TECH_DEBT.md.
- **Content recovery:** parse question + answers back out of each description (the format is stable across v1 and v2: `Today's top AskReddit post: …` + numbered comments).
- **Analysis** (`scripts/analyze_channel.py`, run locally or via a `workflow_dispatch`; outputs committed under `analysis/`):
  - Control for confounders before comparing anything: video age (views accumulate), upload slot (the early vs late daily run), and format version (everything pre-v2 is old format). Compare age-adjusted residuals (e.g., regress log-views on age) or quantiles within rolling cohorts — never raw view counts across months.
  - **Topic buckets:** batch-classify each question via Gemini into a fixed taxonomy (~12 buckets, e.g. relationships/dating, money/work, dark-morbid, politics-news, fame-celebrity, nostalgia, humor-absurd, sex-adjacent, health, hypotheticals, life-advice, other). Report per-bucket n and median adjusted performance.
  - **Distinctive-terms pass:** TF-IDF / distinctive n-grams of top-quartile vs bottom-quartile videos over question+answer text.
  - **Deliverable:** `analysis/topic_performance.md` — ranked buckets, winner/loser terms, and explicit caveats (correlation ≠ causation, small-n buckets, algorithm drift over the sample period).
- **Acceptance:** CSVs + report committed and reproducible; findings framed as hypotheses with proposed `BLOCKED_TOPICS` candidates for R4.4. (Original acceptance bar was "zero OAuth scopes used" — no longer applicable after the 2026-07-21 OAuth migration; superseded, not failed.)

---

### Sprint 1 — bar-raising batch (next release, ships as `v4`)

High-confidence, non-regression keepers. Ship together through the review gate (dry-run artifact → owner eyeball → `FORMAT_VERSION` → live); no per-change bake; measured in aggregate.

> **OAuth prerequisite ✅ done 2026-07-19** — scopes `youtube.upload`, `youtube.force-ssl`, `yt-analytics.readonly`; consent screen in production. API features degrade gracefully (log + skip) if a scope is ever missing. Two owner **asset tasks** also land in this batch — b-roll library (completes R1.3) and extra music tracks (R1.6); they're listed in the §0 Delivery plan and not re-specced here.

#### R3.1a — Question-specific CTA wording — **✅ v4**
- Replace the generic outro. Gemini generates a ≤ 12-word CTA tied to the question (e.g., "Comment the city you thought of — no explaining."; fallback: current generic line). Voiced by the **primary narrator voice** (fixes the Danielle hardcode bug), captioned per R1.2, total segment ≤ 3s.
- **As-built:** markdown emphasis stripped from Gemini output before TTS (asterisks were being spoken); the CTA text doubles as the R3.3 comment.

#### R3.3 — Auto-post engagement comment — **✅ v4 (live-verified 2026-07-27)**
- After a live upload, post one top-level comment from the channel account via `commentThreads().insert` (requires `youtube.force-ssl` scope) — content: the CTA question or a "Which answer wins — 1, 2, or 3?" prompt. Respect DRY_RUN. Fail soft.
- **Known limitation:** the Data API cannot **pin** comments (no such endpoint) — pinning stays manual and optional; do not build for it.

#### R3.4 — Persistent watermark/brand mark — **✅ v4**
- Small semi-transparent channel mark, inside the safe area, all frames. Use the `CHANNEL_NAME` constant rendered as a text mark in the brand font — no logo file required, zero manual steps.
- **As-built:** the channel name, 34px, 55% opacity, low-center (y=1500) — clear of captions, header, and the Shorts UI.

#### R3.5 — Machine-readable content surfaces — **✅ v4 (caption tracks live-verified 2026-07-27)**
- Upload a real subtitle track per video via `captions().insert` (requires `youtube.force-ssl` scope). The word-level timings from Polly speech marks make generating an accurate `.srt` nearly free — the pipeline already has every timestamp. Real caption tracks improve accessibility, search indexing, and how well every legitimate machine reader (YouTube's own content-understanding systems, search engines, AI assistants that surface and summarize video) can parse the video.
- Keep descriptions fully self-describing (already true: question + all answers in plain text). The description is the channel's crawlable text surface — never degrade it into teaser copy.
- **Scope boundary:** this requirement is about maximal legibility to legitimate machine readers, which compounds with human discovery. It is explicitly NOT bot-view optimization — see §7 for why that is excluded.

#### R4.5 — Upload-time predictability & logging — **✅ v4 shipped; ⚠️ partially regressed (2026-09-07)**
- **Original problem:** scheduled runs published 45–105 min after their cron slot — top-of-hour GitHub Actions queue congestion plus pipeline runtime (~7–11 min when measured in July; **actually ~3.4 min as of 2026-09-19**, measured over 60 runs) — making publish time unpredictable across a ~60-min window.
- **Shipped in v4:** cron moved off the hour to `23 0,12 * * *`, pip caching added. Drift tightened to ~45–100 min.
- **⚠️ Regression (observed 2026-09-07):** drift stepped up around 08-27→08-29 and has since held at a **stable ~250–325 min (~4.4h) late**, oscillating rather than growing. GitHub delays scheduled workflows under load and that delay is outside our control; moving the cron minute no longer helps.
- **Impact is low, and deliberately not being chased:**
  - **Cadence is unaffected** — exactly 2 uploads/day for 19 consecutive days, gaps a steady 11–13h. Nothing is missed or colliding.
  - Per §4, **time-of-day is not a growth lever** for Shorts (long discovery tail, global test pool). Chasing a specific clock time optimises something we've already concluded doesn't matter.
  - Compensating by shifting the cron earlier would be fragile: the offset is a queue artifact that can change without notice, and we'd then overshoot early.
- **What was done instead:** made it *observable*. The weekly digest now reports median publish drift and bolds it past 120 min — previously the cadence check counted uploads per calendar day, so hours of slide stayed invisible for ten days.
- **If timing ever does matter** (i.e. the deferred time-of-day experiment is revived), the fix is not cron tuning but **self-gating frequent runs**: schedule hourly, exit immediately unless the target window is open and the slot is unfilled. That converts "fire at 00:23 and hope" into "publish as early in the window as the queue allows", at the cost of ~24 short no-op runs/day.
- **Deferred (experiment backlog):** actually optimising time-of-day. Unchanged — not a growth lever.

#### R2.3 — Branded thumbnail template — **⏸ deferred (2026-07-22, at v4 ship)**
- A basic branded card already ships (since v2: dark bg frame, channel tag, full question). This spec is the full version — Gemini-shortened ≤ 8-word headline, channel mark. Deferred per "include if cheap, else defer": thumbnails don't render in the Shorts feed, so the marginal value is limited to channel/search/browse surfaces. Revisit only if those surfaces ever matter — **answered 2026-09-07: they don't** (R4.7 measured them at ~3.9% of views combined; see §4 Findings). Stays deferred.

---

### Next keeper release (`v5`)

#### R4.6 — Suppression-risk screen at selection — **Keeper (content-selection change → own `FORMAT_VERSION` bump, feature branch)**
- **Problem (evidence, 2026-07-27, extended 2026-08-23):** **three** uploads confirmed zeroed by silent **limited distribution** — public, `processed`, *not* age-restricted via API, yet exactly 0 views while same-period uploads got 50–1048:
  1. `Your Secret Sign: Amazing In Bed?` — **sexual_suggestive** framing
  2. `qvNzVCzWebk` / `When Chiropractic Lands You In The ER` — **graphic_harm** ("cervical/vertebral artery dissection", "pneumothorax")
  3. `_0MNAf8AzNg` / *"What's a horrible thing that a famous person did that everyone forgot about but you?"* (2026-08-21) — **named_wrongdoing**; answers alleged specific misconduct by named celebrities (Naomi Campbell/Epstein, George Lopez)
  Limited distribution is Studio-only — the API cannot see it, so prevention has to happen at selection. Cost of a zeroed upload: a wasted slot and plausibly worse channel-level classifier priors (the stronger "momentum poisoning" claim is unsubstantiated — not the justification here).
- **Taxonomy correction (2026-08-23):** case 3 overturned the earlier call that named-individual content is safe. It is safe *unless the question solicits specific unproven misconduct allegations about named real people.* Live counter-evidence keeps the line precise — all served fine: Epstein-files question (923), "famous person died in the dumbest way" (141), "celebrity downfall you can't wait for" (127), "What YouTuber really fell off?" (113), Trump "draft dodger, crook" (257). So `named_wrongdoing` is promoted from log-only to an active category, narrowly scoped to *soliciting* wrongdoing claims — not naming, negativity, politics, or death.
- **Counter-evidence that keeps the screen narrow:** three videos *mentioning* chiropractic served fine (95–158). The trigger is **framing**, not topic. General "controversy" must NOT be filtered — dark-morbid is a top-performing bucket.
- **Mechanism:** one Gemini call at selection time evaluating the candidate post title + a pool of its top comments against seven categories: `sexual_suggestive` · `graphic_harm` · `named_wrongdoing` · `minors_sexual` · `hard_drugs` · `graphic_violence` · `slurs`. All three confirmed-zeroed videos and five fine-serving near-misses are in-prompt calibration examples. A narrow keyword **backstop** runs only when Gemini is unavailable, so an outage doesn't mean zero protection.
- **Verdicts:** `skip_post` (question itself risky → selection falls through to the next of the top 10) · `drop_comment` (one risky answer → replace with next valid comment, keep post) · `pass`. **Fail-open:** any Gemini/API error blocks nothing.
- **Audit trail (the anti-over-filtering guard):** every non-`pass` verdict appends to a committed `analysis/screen_log.csv` (date, post title, verdict, category, reason) for weekly owner review. Decision rule: false positives in the log or a skip rate above ~15% of candidates → narrow the prompt, don't revert the screen.
- **Digest addition:** flag logged videos whose `privacyStatus` ≠ public (distinguishes owner-privatized videos from suppression when investigating zero-view flags; the existing 0-views-after-3-days flag remains the suppression detector).
- **Acceptance:** dry run with seeded risky candidates shows skip/drop/pass each firing correctly; fail-open path verified; screen_log row schema written; existing filters (NSFW/profanity/emoji) untouched.
- **As-built validation (2026-08-23, pre-merge):** 3/3 then-believed cases skipped with the correct category; replay over 18 live uploads gave skip 6% / drop 11% / pass 83%; fail-open verified.
- **⚠️ EVIDENCE CORRECTION (2026-08-30) — this requirement was overclaimed.** A fresh review of all 970 channel videos found the validation above rests on a selection-biased sample:
  - **Confirmed case #2 is not supported.** `qvNzVCzWebk` (chiropractic/ER, the sole basis for `graphic_harm`) sits inside a channel-wide cold spell — neighbours read `1, 0, 0, 3, 1, [0], 37, 15`. The original check confirmed public/processed/not-age-restricted but never checked neighbours. It is not evidence of per-video moderation.
  - **The real-world arm was n=1.** The 18-upload replay contained exactly one zeroed video and the screen caught it. One true positive does not validate a seven-category taxonomy.
  - **The screen does not explain about half the phenomenon.** Of ~16 genuinely isolated zeroes across channel history, roughly half are benign under the screen's own instructions (first-date icks, "what did you stop doing", a teen-social-media political question, this week's `lBa1wGF7KrE` about free software) — several of which the prompt explicitly forbids flagging.
  - **The rate has not moved:** ~3.9% (v1 2025) → 4.7% (v1 2026) → 4.1% (v2–v4) → 6.2% (v5, n=16). At a ~4% base rate, ~66 consecutive clean uploads (~33 days) would be needed for 95% confidence, and the streak has already broken.
  - **Cost/benefit is plausibly negative:** the screen spends ~6.7% of slots (one `skip_post` in ~15 live runs, discarding the top-ranked candidate) against a phenomenon costing ~2.6% of era views, and explains at best half of it.
  - **Do NOT add a category in response to a single new zero.** That is exactly the n=1 fitting that produced this taxonomy and the cancelled R1.8/R1.9.
  - **Recommended posture:** keep the screen (free, fail-open, catches the sexual/named-wrongdoing shapes, and its call carries the `topic` telemetry R4.4 needs), **freeze the taxonomy**, and reclassify 0-views in §0 as accepted background loss rather than an open workstream. Verify with `scripts/report.py --zeros`, which now encodes the private-video and cold-spell traps.

- **FIRST STANDING AUDIT (2026-09-09) → two-tier taxonomy, ships as `v6`.** `analysis/screen_log.csv` over 2026-08-25 … 2026-09-10: 6 verdicts across 33 uploads — 3 `skip_post`, 3 `drop_comments`. The **rate** is fine (well under the ~15% narrow-the-prompt threshold); the **composition** is not. Two of the three skips came from the two categories with the weakest evidence:
  - `2026-09-05` *"Doctors/nurses of Reddit, what's a symptom patients brush off that actually terrifies you?"* → **`graphic_harm`**, the category whose only confirmed case (`qvNzVCzWebk`) the 2026-08-30 correction above retracted as a cold-spell artifact.
  - `2026-08-26` *"Bartenders of Reddit, what was a 'cut off' gone wrong?"* → **`graphic_violence`**, which never had a confirmed case at all — it was reasoned into the taxonomy, not observed.
  Both are ordinary high-engagement AskReddit shapes, and dark-morbid is a top-performing bucket (§4). The screen was spending its most expensive action on its least-supported categories.
- **Change — split the taxonomy by cost, not by severity.** Skipping a post discards the top-ranked candidate of the day; dropping an answer costs one answer and the pool backfills. A category now earns post-skip authority only if a confirmed zeroed upload supports it, or its severity means it never fires here anyway:
  - **`SKIP_CATEGORIES`** (may discard the post): `sexual_suggestive` and `named_wrongdoing` (the two surviving confirmed cases), plus `minors_sexual` / `hard_drugs` / `slurs` — zero-cost tail guards that have never fired on this channel, so removing them would buy nothing.
  - **`DROP_ONLY_CATEGORIES`** (answer-level only, never a skip): `graphic_harm`, `graphic_violence`.
  Enforced **in code**, not just in the prompt — the model may still raise one of these against a question, and `screen.py` demotes it to a pass. A prompt instruction is not an enforcement mechanism.
- **The counterfactual stays visible.** A demoted verdict writes a `demoted_post_risk` row to `screen_log.csv` carrying the category we declined to skip on. If zeroes rise, the audit can see exactly what was let through — this is the record that would justify a re-promotion, and the only thing that should.
- **Also corrected:** the retracted chiropractic case was still sitting in the prompt as a *"WAS suppressed"* calibration example, teaching the model the pattern the evidence no longer supports. Removed. The three audited false positives are now in-prompt as questions that must pass. The confirmed-case count drops to **two** here and in the README.
- **This is a narrowing, not an addition** — consistent with "freeze the taxonomy" above, which forbids *adding* categories off single zeroes. The standing decision rule already prescribes exactly this action ("false positives in the log → narrow the prompt, don't revert").
- **Validation (2026-09-09):** 18 unit tests in `tests/test_screen.py` lock the tier guarantee per category (a `DROP_ONLY` category can never return `skip_post`), the audit's three false positives, the fail-open backstop's matching two-tier split, the `demoted_post_risk` audit row, and the retry fix below. Live-Gemini replay via the new `scripts/replay_screen.py`, **4 of 8 cases confirmed before the free-tier quota ran out**:
  - ✅ *"Doctors/nurses … symptom that terrifies you?"* → **pass** (was a live `graphic_harm` skip)
  - ✅ *"Bartenders … a 'cut off' gone wrong?"* → **pass, one answer dropped** (was a live `graphic_violence` skip) — the tier working as intended: keep the slot, drop the one risky answer
  - ✅ *"ER workers … chiropractic patients?"* → **pass, two graphic answers dropped** — via the backstop, which now also declines to skip on those terms
  - ✅ *"…hints someone's excellent in bed?"* → **still skips `sexual_suggestive`** (confirmed-zeroed case)
  - ⚠️ **Not yet re-verified live: `named_wrongdoing`.** The prompt lost a calibration example in this change (the retracted chiropractic case), so the surviving confirmed shapes deserve a live re-check. Re-run `scripts/replay_screen.py` once quota resets — this is the one open item before merge.
- **Reliability fix found by that replay, then corrected 2026-09-11:** `_generate_screened` retried HTTP 429/503 but **not** `Timeout`/`ConnectionError`, so a transient read timeout dropped straight to keyword-only screening — 3 of the first 8 replay calls hit exactly that. Timeouts are now retried.
  - **But retrying 429 was wrong and is now removed.** On this free tier a 429 is a *daily* budget exhaustion, not a per-minute burst — it persists for hours and clears at midnight PT. Retrying it cannot succeed, and each wasted request comes out of the same budget the keyword, title and CTA calls later in the same run still need, so it makes the run's output worse rather than better. Measured: a verification pass on 2026-09-11 retried 429s and spent ~40 requests to make 8 useful calls. `tries` is also reduced 3 → 2, so a screen call costs at most 2 requests instead of 3. Fail-open behaviour is unchanged.
- **Screen coverage is lower than assumed — `screen_source` added (2026-09-09).** 5 of the 35 uploads since the screen shipped (**14%**) carry no `topic`, which means the Gemini call failed and the run shipped on the keyword backstop. Nothing recorded that, so the standing audit has been auditing a screen it could not confirm ran, and R4.4's topic telemetry has a 14% hole. `upload_log.csv` now records `screen_source` (`gemini` | `backstop`) per upload, the same pattern as the 2026-09-07 `caption_ok`/`comment_ok` columns. This also makes the retry fix above measurable: if those failures were transient, the backstop share should fall.
- **Version:** content-selection change → `FORMAT_VERSION` bump to `v6` for attribution, per the rule in R4.4.

#### R4.7 — Traffic-source telemetry — **shipped ✅ 2026-09-07 (measurement-only, no version bump)**
- Add `insightTrafficSourceType` (Analytics API dimension) to the weekly snapshot job — per-video or channel-level views by source (Shorts feed / search / browse / external).
- **Why:** tells us whether the SEO surface (tags, titles-for-search, SRT) earns anything, or whether distribution is ~100% Shorts feed — which decides whether search-oriented work is ever worth revisiting. Currently flying blind on this.
- **Acceptance:** new column(s)/file appended by the Monday job; a first snapshot committed.
- **As-built (2026-09-07) — cohort-level, not per-video.** The API forbids the per-video breakdown: `dimensions="video,insightTrafficSourceType"` returns 400 *"The query is not supported"*, and a `video==` filter **aggregates** the id list instead of splitting it. A true per-video mix therefore costs one call per video (~985/week here) for denominators around 100 views — noise. Three cohort scopes are appended instead, one row per (scope, source), to `analysis/traffic_sources.csv`:
  - `channel_lifetime` — all-time level, dominated by the ~900 pre-overhaul v1 uploads.
  - `channel_7d` — trailing week, non-overlapping between Monday runs, so repeated runs build a **drift series**. `endDate` is the run date and Analytics lags 1–2 days, so it really covers ~5–6 settled days; the bias is constant, so week-over-week stays comparable.
  - `logged_uploads` — the `upload_log.csv` cohort, i.e. the format we actually ship today. This is the scope to read for decisions; the lifetime number answers a question about content we no longer make.
- **As-built additions:** one `Traffic mix (7d)` bullet under the digest's Performance block (the CSV alone would go unread); pure aggregation/share/label logic in `src/insights.py` with unit tests, API calls in `scripts/weekly_analytics.py`. The traffic step is **fail-soft** — a traffic query error must never cost the per-video snapshot — and each CSV now guards its own same-day double-append independently, so a rerun after a partial failure fills in only what is missing.

---

### Experiment backlog

"Might revert" bets. Ship **one variable per version**, each with a real bake window (≥ 20 uploads / ~2 weeks) and a **pre-committed decision rule** (see §8). Order below follows the 2026-07-27 re-prioritization (Delivery plan).

#### R1.8 / R1.9 — Short format & narration rate — **❌ CANCELLED 2026-08-23 (never built)**

Both were premised on a fixed ~10–12s watch budget implying that shortening a video raises real retention. Review 2 (§4 Findings, n=66) refuted the inference:
- `corr(duration, log views) = −0.17` — longer is not worse, and duration barely matters.
- Top-12 videos vs the rest: **same** median duration (19.2s vs 19.8s); they differ on **watch-seconds** (11.0s vs 9.0s).
- Watch-seconds are flat against duration (`corr = +0.13`), so trimming inflates avg-%-viewed *arithmetically* while adding zero watch time. R1.8 would have satisfied its own decision rule while delivering nothing.
- Loops (one video at 227% avg-viewed = 40s watched on 17s) are real upside that removing content cannot buy.

Retained as a cautionary record: the failure mode was targeting a ratio whose denominator we control. §4 now makes **watch-seconds** the primary metric for this reason. Superseded by R4.4 (content/hook quality), which addresses the variable that actually separates winners.

#### R3.1b — CTA placement — **⬜ unscheduled (2026-08-23)**
- Was folded into R1.8; that experiment is cancelled, so this is standalone again and currently unscheduled. The open question — does moving the ask earlier (overlay strip during the final answer) help or annoy? — is untested. Low priority: it's a small change against an unmeasured effect, and §4 now says judge it on watch-seconds. Revive only with a specific reason.

#### R3.2 — Two-voice reaction beat — **Experiment, originality candidate 1 (bet 1, §0 #7)**
- The *unused* voice of {Danielle, Stephen} delivers one line (≤ 12 words) written from the **house stance the owner sets** (#55; three drafted 2026-10-07: a "show of hands" vote, a skeptic, a "noticer"), inside the existing metadata call (0 extra Gemini requests). Distinct caption colour for the second voice. It must name something in *this* post's answers, never a stock phrase (template rule), and judge, never advise (R3.6's policy notes apply).
- **Placement follows the stance:** a vote comes after the last answer and ends on asking the viewer's vote. Every video already ends on a spoken CTA from the same call (`llm.get_metadata`, ≤ 12 words asking for the viewer's answer), so **the vote can replace the CTA**: no added length, no extra request, about the same narration. That is the cheapest first step of bet 1, and it is R3.6's verdict line, so build the two as one. **First trial (2026-10-07, five real posts, sample model, a stand-in rule):** four votes named something specific; one voted "because autism affects socialization most", so the prompt now says vote on the answer, never on the person. A reaction to one answer sits straight after that answer.
- **Fails soft and is counted:** any Gemini/Polly error → the video ships without the line, logged per upload (a `reaction_ok`-style column), so a silent fallback is visible.
- **Length is not held:** the line adds ~3 s, and dropping a comment to offset it would change the content too. The release check covers it: total watch time must also hold (#39), and the gain is credited only within each length half (2026-10-07).
- **Read** within AskReddit while #3 runs (§0 #7). **Decision rule:** §0 #7's. Beside it, never as triggers (pre-committed 2026-10-07): comments and subscribers gained per upload (`subs_gained`, from 2026-10-12), the two things a vote is for.

#### R3.6 — Host storyline — **Experiment, originality candidate 2 (drafted 2026-10-05)**
- YouTube pays for "edited content with a storyline and commentary" (PLAN §4). The host voice adds a one-line setup before the answers and a one-line verdict after them: what the answers have in common, or which one wins, ending on the show's own question to the viewer (fits *Show of Hands*). Comments stay verbatim and in vote order (owner, 2026-08-23).
- Both lines come from the existing metadata call (0 extra Gemini requests) and must refer to this post's answers, never a stock phrase (template rule). **The verdict line is R3.2's vote** (2026-10-07): it replaces the spoken CTA (built switched off, `product/house-vote-dormant`); the setup line is what remains.
- **Length held:** when the two lines would lengthen the video, the last comment drops (as R1.7), so this varies authorship, not length, the weakest prior (§4 watch budget). Narration roughly unchanged; at most ~17¢/month more if no comment drops.
- **Fails soft and is counted:** missing lines → the video ships without them, logged per upload so a silent fallback is visible.
- **Curation is not a separate candidate:** choosing other people's text is still a reading under the policy, and reordering comments breaks the owner's vote-order principle. Its useful half, our verdict on the answers, is this spec.
- **Applies to R3.2 too (YouTube's policy page, read first-hand 2026-10-06):** (a) AI personas "providing advice to viewers on topics such as health, legal issues, finances, or politics" cannot monetize, and 27 of 79 topic-tagged uploads sit there (life-advice, money-work, health-body, politics-news). So the lines react and judge, and never advise. (b) "AI-generated content made with generic or unoriginal templates … without adding the creator's original, authentic insights or perspective" cannot either. The prompt should write from a house stance the owner sets, not a generic tone (#55).

#### R4.1 — Subreddit rotation (Q&A-mode) — **Experiment — reframed 2026-07-27: inventory prerequisite for posting volume**
- **Why it matters more now:** a future posting-volume increase (backlog #5) needs more than one subreddit's worth of daily post inventory — proving rotation works is the gate to that lever, not just a content experiment.
- Config list of question-style subreddits (e.g., AskReddit, NoStupidQuestions, AskMen, AskWomen, AskUK — owner-editable constant). Rotate deterministically per run; existing filters apply; log `subreddit` (R0.2).
- Replace `prev_post.txt` with `recent_posts.txt`: rolling last 30 posted titles (dedupe window across all subs). Migrate the workflow commit step.
- **Decision rule:** compare age-adjusted median views per subreddit after ≥15 uploads each; drop any that underperform the AskReddit baseline.
- **Build note (2026-09-26):** the rule above is superseded by §0's watch-seconds rule (#18). Keep `prev_post.txt` rather than migrating to `recent_posts.txt`: the migration rewrites production data and the workflow's commit step, both owner calls, and last-title dedupe across subreddits is enough for a first version. Replay the R4.6 screen on each new subreddit's top posts before shipping; AskMen/AskWomen will hit its skip categories more often than AskReddit. **2026-09-27:** description and tags now name the post's own subreddit (AskReddit's are byte-identical, test-pinned). Still AskReddit-worded: the on-video watermark (`CHANNEL_NAME`, the channel's name, so arguably right) and the slate prompt's wording. Next to screen, chosen by our own topic prior rather than size: AskOldPeople (nostalgia, a top bucket at +0.56) before AskMen/AskWomen. That +0.56 is the historical prior alone: on the current format `--at-age 7 --compare topic=nostalgia` refuses at n=4 (2026-09-29), and the slate labels more posts nostalgia than the screen does (§6 R4.4), so the rotation's own ≥15-upload read is the first current evidence.
- **Story-mode subs (r/tifu, r/AmItheAsshole, r/confession) are a stretch** (though the large comparable channels are all story-shaped, §4 2026-10-05): different format — Gemini condenses the selftext to a ≤ 35s script, CTA becomes a verdict poll ("NTA or YTA? Comment."). Build only after Q&A rotation ships and has data.

#### R4.4 — Topic/hook candidate ranker — **Experiment #1 (top of backlog, promoted 2026-08-23)**
- At selection time, classify the candidate post's title into the R4.3 taxonomy (one Gemini call, **fail-open**: on any error no post is blocked) and skip/deprioritize candidates by bucket — selection already iterates the top 10 posts, so it falls through to the next candidate. (Current R4.3 evidence favors a *preference ranker* — prefer nostalgia/dark-morbid/humor-absurd when available — over an outright blocklist; weak buckets are mild, not toxic.)
- **Policy:** the analysis *proposes* the list; the owner approves it before it ships — a data artifact must not silently change content policy. Add a `topic` column to `upload_log.csv` so the gate's effect is itself measurable, and bump `FORMAT_VERSION` when the gate first ships (a content-selection change is a format change for attribution purposes).
- **Design principle (owner, 2026-08-23) — deviation from Reddit's ranking requires justification.** The channel's premise is human-generated *and* human-validated content: upvotes are free, high-quality signal that the content already landed with real people. Overriding that ranking with our own judgment is allowed, but only where we can name a specific reason our audience's preference diverges — never merely because we think we know better.
  - **Grounded, so in scope:** topic priors measured on *our own* channel. Age-adjusted over n=607 classified videos, the spread between best and worst topic bucket is ~1.6× (dark-morbid +0.58 / nostalgia +0.56 / humor-absurd +0.51 at the top; fame-celebrity +0.13 / money-work +0.13 / life-advice +0.15 at the bottom). Reddit's top-of-day ranking is topic-agnostic; our audience is not. Mechanism: Reddit voters read threaded text with full context, our viewer gets ~20s of narration with none.
  - **Not grounded, so cut:** LLM "hook strength" scoring. Unvalidated, subjective, and it substitutes machine judgment for the human vote signal that is the point of the channel. Removed from scope.
  - **Precedent:** we already deviate (≤150-char comment filter, profanity/emoji/NSFW filters, R4.6 screen), so this is a question of degree and basis, not principle.
- **Revised mechanism — Reddit rank is the default, our data is a narrow exception.** Take the top-ranked eligible post *unless* its topic sits in the measured-weak tier **and** another candidate within the top few sits in the measured-strong tier. This layers our audience's revealed preference on top of Reddit's rather than replacing it. **Comments are not reordered** — within a single thread, vote ranking is the strongest signal available and the audience mismatch is smallest; only R4.6 may drop a comment.
- **Step 0 — ✅ shipped 2026-08-23 (telemetry only, no behavior change).** `candidate_rank` and `topic` are now logged per upload (`upload_log.csv`; topic piggybacks on the existing R4.6 screen call, so zero extra Gemini quota). Existing filters already push selection off rank 1 sometimes, so this accumulates the counterfactual we've never had: **does taking a lower-ranked post actually cost views?** Build the ranker only once that data supports it — if rank turns out not to matter, the topic exception is cheap; if lower ranks measurably underperform, the exception bar should rise.
  - **⚠️ Step 0 reviewed 2026-09-09 — the gate as written will not open.** 35 uploads in: 32 rank 1, 3 rank 2, and all three of those were caused by R4.6 skips rather than the basic filters. The estimate that "existing filters already push selection off rank 1 sometimes" turned out to mean ~9% of uploads, which puts a usable cohort in December, and the history cannot be backfilled. Two further gaps: the topic prior this ranker would use is measured almost entirely on pre-v2 content (`topic_performance.md`'s own caveat says to re-run it), and the log keeps only the *selected* post's topic, so the ranker's firing rate — and therefore the length of its own bake window — is unknowable from the current data. Full analysis and the recommended unblock are in §4, "R4.4 gate review".
  - **✅ Gate cleared 2026-09-11 — two of those three gaps are closed.** The R4.3 re-run put Spearman rho at **+0.79** between the pre-overhaul and current-format topic orderings, so the topic prior survives the format change and is no longer an assumption. Per the gate review's own terms, that makes the rank counterfactual droppable — it was never load-bearing, and it still reads n=3 (`--compare candidate_rank=1` refuses a verdict, checked again 2026-09-21). **The third gap is still open and is now the only thing between here and a build:** the log records the selected post's topic, never the slate passed over, so the ranker's firing rate — and therefore the length of its own bake — cannot be estimated.
  - **Unpriced cost found 2026-09-21: the mechanism needs the slate classified, and the slate is not free.** `select_post` returns on the first candidate that passes, so a run makes **one** screen call today. Ranking "the top few" means labelling N candidates instead of 1, against a Gemini free tier of **20 requests/day** that production already draws 4–10 from and that starved a live upload on 2026-09-20. A per-candidate scan of the top 10 would exceed the whole day's cap on its own; even the top 3 pushes production to 8–14/day. **Proposed Step 0.5 (telemetry only, no behaviour change): one batched call per run that classifies all ~10 candidate *titles* together** — titles need no comment context — logged as the slate we passed over, at **+1 request per run (+2/day)**. That makes the firing rate measurable before any selection logic ships, which is the third gap, and it establishes the affordable shape of the ranker itself. The per-candidate scan should not be built.
  - **Step 0.5 live 2026-09-25 (dry run PASS on `2720369`).** `upload_log.slate_topics` holds every eligible candidate's topic in rank order, from one call on `config.SLATE_MODEL` (`gemini-2.5-flash-lite`). The free tier is counted per model, so this adds **0** to the budget titles and the screen share. That is route A from #22, applied only to the new call, so the model behind shipped titles is unchanged. Telemetry only: never read at selection, a failure costs only the column, never retried. `slate[candidate_rank - 1]` is the selected post, so agreement with the screen's topic is measured for free. **Firing-rate read:** after ≥20 uploads, count the runs where rank 1 is weak-tier and a strong-tier candidate sits within the top 3. That count sets the ranker's bake length. **Read `report.py --slate` first (2026-09-29: 2 of 6 agree, too thin for a rate).** The slate's titles-only labels disagree with the screen's on most posts, and mostly by being more specific (screen `other`, slate `nostalgia`). The prior in `topic_performance.md` is mostly batched titles-only labels, so if agreement stays low, the ranker should rank on the slate's labels, and R1's screen-labelled read is not a read of the prior's buckets.
- **Decision rule:** after ≥20 uploads, keep if median **watch-seconds** and median views both hold or improve against an age-matched baseline; revert if either drops materially. (Judged on watch-seconds, not avg-%-viewed — see §4.)
- **Acceptance:** dry run with a seeded candidate list shows a blocked/deprioritized post being skipped; `topic` logged per upload; fail-open path verified.

#### Localization — one channel per language (R5.x) — **Experiment (separately gated)**

**Gate (in addition to the standard experiment bake):** start only after the English format is proven — ≥1 month of post-v2 data with retention around the ≥70% target and a clearly rising view floor. Localization multiplies a format's reach; it cannot fix a format that doesn't retain, and every new channel independently faces its own YPP thresholds (1,000 subs + 10M Shorts views/90d **per channel**). Do not start localization to rescue a weak format.

**Structure decision:** separate channel per language, mapped 1:1 (the owner's instinct is correct): audience-language coherence is what lets YouTube's recommender build a stable audience per channel, and the multi-audio-track feature does not apply to Shorts. The same Google account can own all channels as brand accounts; OAuth consent is granted per channel, yielding one refresh-token secret per channel (`YOUTUBE_REFRESH_TOKEN_ES`, …).

##### R5.1 — Spanish pilot channel — **Experiment (post-gate)**
- Same daily selected post → Gemini translates question + answers + title + description (prompt for natural colloquial Spanish, not literal; keep proper nouns) → Polly Spanish neural voices (Lupe es-US / Mia es-MX / Sergio es-ES; confirm speech-mark support per voice) → the existing visual system unchanged (Anton covers Spanish diacritics) with localized fixed strings (header, outro, CTA) → upload to the ES channel.
- Bookkeeping: add a `channel` column to `upload_log.csv`; per-channel dedupe files; render sequentially in the same Action run (~5 extra minutes).
- Language economics: while the goal is the 10M-view threshold, pick volume-first languages (Spanish, Portuguese-BR, Hindi have the largest Shorts populations). High-CPM/low-volume locales (German, French) only matter post-YPP.
- **Acceptance:** one DRY_RUN produces both language videos; ES upload path verified against the pilot channel; per-channel log rows separable.

##### R5.2 — Additional languages; RTL support — **Experiment (post-gate stretch)**
- Portuguese-BR (Camila/Thiago) and Hindi (Kajal) are near drop-ins on the R5.1 template.
- **Arabic is not a drop-in.** RTL + script shaping means: Pillow must be built with libraqm (otherwise Arabic renders as disconnected left-to-right letters — visibly broken), an Arabic-script font is required (Cairo or Tajawal, OFL), caption grouping must display in RTL order (the existing byte-offset handling already survives multibyte UTF-8), and Polly Arabic voices (Hala/Zayd, ar-AE) need speech-mark verification. Treat Arabic as its own mini-project with frame-level visual verification before anything uploads.
- At >3 languages, move from sequential rendering to a workflow matrix to keep job time reasonable.

## 7. Explicitly out of scope

- Paid services (ElevenLabs, stock subscriptions, editors). Any per-video manual step. Engagement manipulation of any kind. Long-form video. Shorts poll stickers (not exposed via API). Comment pinning (no API). Reposting/compiling third-party video content. Migrating off the notebook's current infra (Actions + Polly + Gemini stack stays).
- **Posting-frequency increases — moved from excluded to conditionally deferred (2026-07-27).** The original exclusion ("no volume as a substitute for quality") was right when quality was poor. With a stable format, volume is the most reliable multiplier toward 10M/90d — but only *after* R4.1 proves multi-subreddit inventory can sustain quality at 4/day. See experiment backlog #4; never volume *instead of* fixing a broken format.
- **Bot-view optimization.** Excluded on both factual and policy grounds. Factual: YPP thresholds count only *valid* public views — YouTube filters traffic it identifies as automated *before* it counts, so views from external bots/scrapers have approximately zero monetization yield regardless of how well content caters to them. Policy: deliberately cultivating artificial traffic falls under YouTube's fake-engagement enforcement (up to channel termination) — an uncapped downside against a ~zero upside, aimed at the exact asset we're trying to monetize. The legitimate core of the idea — content that machines can accurately read, index, and surface — is in scope as R3.5 and costs nothing extra given the speech-mark infrastructure.

## 8. Delivery model & rollout

Changes are sorted onto two tracks by one question: **will we act on this change's individual result?** The concrete bucketing is the [Delivery plan](#delivery-plan) in §0; this section is the rationale.

**Why this sorting (and why the old rule was wrong).** There are two distinct reasons to wait between changes, and the original "bake every version ~1 month" rule conflated them:
1. **Attribution** — ship A then B fast, views move, you can't tell which did it.
2. **Validation** — you want to know whether a change worked so you can decide to keep / revert / iterate.
Attribution only has *value* if you'll act on it. For high-confidence changes we'll keep regardless (motion background, captions, branding, subtitles), neither reason applies — so per-change bake time is pure delay. For genuine bets we might revert, both apply — so they get isolated and baked.

**Track 1 — bar-raising batch.** High-confidence, non-regression keepers. Batch-shipped as a single `FORMAT_VERSION`, minimal bake. We deliberately give up *within-batch* attribution (they're all keepers, so we'd never act on it). Measured only in aggregate as a sanity check.

**Track 2 — experiment backlog.** "Might revert" changes. One variable per version, a real bake window (≥ 20 uploads / ~2 weeks), and a **decision rule pre-committed before shipping** (keep/revert/iterate on a named metric threshold). No bet ships without its rule — a bake window with no pre-committed action is just a delay, which was the gap in the original plan (we never defined what to do after the wait).

**The release gate is preserved on both tracks and is *not* the slow part** — but as of 2026-09-19 it is **automated rather than owner-reviewed**: feature branch → build → tests green → `DRY_RUN=1` produces a playable MP4 with sane metadata → bump `FORMAT_VERSION` → merge to `main` → live. The owner-review step was removed because it had become the binding constraint (a branch sat 8 days while six more stacked behind it), and unshipped work is inventory, not progress. What replaces the owner's eyes is **auto-revert**: a later shift that finds a release degraded median watch-seconds against an age-matched baseline reverts it (views are reported, never a trigger: owner, #18). Shipping without review only works if something watches the result. That gate catches actual regressions (a visual bug, a broken render) — distinct from statistical bake time, which is what we compress for keepers. **Feature work happens on a branch, never directly on `main`** — the live workflow runs from `main` twice daily, so it must stay runnable; this is a standing convention documented in the README's *Development workflow* section.

**Sort per-change, not per-phase.** Confidence can be miscalibrated, and the old thematic phases mixed safe and risky work (Phase 3's watermark/subtitles are keepers; its reaction beat is a real retention experiment). Every unshipped item carries an explicit bucket tag in the Delivery plan.

**One clean read is protected:** the v1→v2 retention comparison (does production quality move avg-%-viewed at all?) stays recoverable because v3 was metadata-only. It matures in parallel via the weekly digest and is consulted before over-investing in the production-quality thesis — but does **not** block Sprint 1.

**R4.3 exception retained:** read-only analysis (changes nothing viewers see) may run any time, including mid-bake.

**Localization (R5.x)** keeps its own separate gate (proven English format) on top of all the above.

## 9. Verification playbook (for the implementing agent)

- **Unit tests:** `venv/bin/pip install -r requirements-dev.txt && venv/bin/python -m pytest tests/` — covers the pure analysis logic (`src/insights.py`). Run before any change touching selection, logging, or analysis.
- **Render:** `DRY_RUN=1 python -m src.run`.
- **Structure:** `ffprobe -show_entries format=duration,stream=width,height,avg_frame_rate` → 1080×1920@30, 10–59s. *(Was 20–40s until 2026-09-24: 25 of the last 60 real uploads ran under 20s, the shortest 12.8s, so the old floor failed healthy renders. The gate is for broken renders, not format.)*
- **Dead air:** `ffmpeg -i out.mp4 -af silencedetect=n=-35dB:d=1.0 -f null -` → no silence of 1s or more. *(Was d=0.3: a render that shipped has a natural 0.34s pause after the title.)*
- **Automated:** `scripts/dry_run.py check <mp4>` applies both of the above plus audio presence and a full decode — the check `dry-run.yml` runs on every requested render.
- **Visuals:** extract frames (`ffmpeg -vf fps=1`) at t=0.3, mid-title, each comment, CTA → verify caption word-groups, header/badge, watermark, legibility, motion (pixel-diff two frames 3s apart).
- **Caption sync:** unit check comparing speech-mark times to caption clip start times (±150 ms).
- **Safety greps:** every network mutation (`videos().insert`, `thumbnails().set`, `commentThreads().insert`, file/log writes) is behind the DRY_RUN flag; workflow commit step adds only intended files.
- **CI:** `workflow_dispatch` with `dry_run=true` must pass end-to-end on `ubuntu-latest` before any live rollout.
- **Performance questions:** use `scripts/report.py` (`--by`, `--compare`, `--metric`) — never ad-hoc analysis. It enforces watch-seconds-primary, age-matched cohorts, and n-gating; see TECH_DEBT.md Pass 2 for why that matters.
- **Screen behaviour:** after changing `src/screen.py`, re-check it against the three confirmed-suppressed cases and the five fine-serving controls listed in R4.6 before merging.
- **Never** verify by uploading publicly. If an end-to-end upload test is ever truly needed, ask the owner first (option: `privacyStatus: "private"` test upload, then delete — owner approval required).

## 10. Open questions (defaults apply if unanswered)

- **OQ-1 — B-roll sourcing:** ~~resolved 2026-08-15~~ — manual curation chosen and done (7 Pexels clips). No API key needed. Selection criterion learned in practice: dark/mid-tone only; two of nine candidates were rejected at the R1.4 legibility gate for washing out white captions.
- **OQ-2 — Channel brand name:** ~~resolved 2026-07-22~~ — a fixed `CHANNEL_NAME` rather than fetched per run: it never changes, and a constant avoids an API call plus a failure mode on the render path. **Since 2026-10-05 it comes from the `CHANNEL_NAME` secret** so the public repo does not name the channel, and a real upload refuses to start without it.
- **OQ-3 — Caption styling:** ~~resolved as-built~~ — white fill, black stroke, Anton, brand orange `#ff5d01` reserved for the `ANSWER n/N` badge and channel tag. The only open sliver is a second-voice highlight colour, which is moot unless R3.2 ships.
- **OQ-4 — R4.3 credentials:** ~~resolved 2026-07-19~~ — owner created a Data API key as `YOUTUBE_DATA_API_KEY`. ~~Superseded 2026-07-21~~ — R4.3 migrated to OAuth in the refactor pass; the key is unused by any script now and doesn't need to exist as an Actions secret.
- **OQ-5 — Localization pilot language:** default Spanish (largest Shorts-population overlap with zero new rendering technology); Arabic deliberately deferred to R5.2 because of the RTL/shaping work.

## Appendix A — API notes & snippets

**Polly word marks (timings for R1.2)** — separate call from audio; same Text/Voice/Engine:
```python
resp = polly.synthesize_speech(Text=text, OutputFormat='json',
                               SpeechMarkTypes=['word'],
                               VoiceId=voice_id, Engine='neural')
marks = [json.loads(l) for l in resp['AudioStream'].read().decode().splitlines() if l]
# {'time': 6, 'type': 'word', 'start': 0, 'end': 4, 'value': 'What'}  (time in ms)
```

**MoviePy 2.1.2 gotchas:** `subclipped()` not `subclip()`; `with_*` not `set_*`; effects via `clip.with_effects([vfx.Loop(duration=d)])`; `TextClip(font=<path-to-ttf>, text=..., method='caption', size=(950, None), stroke_color=..., stroke_width=...)`; strip b-roll audio with `.without_audio()`. Verify exact names against installed 2.1.2, not web tutorials (mostly 1.x).

**Caption clip sketch:**
```python
TextClip(font='assets/fonts/Anton-Regular.ttf', text=chunk, font_size=110,
         color='white', stroke_color='black', stroke_width=8,
         method='caption', size=(950, None), text_align='center')\
    .with_start(t0).with_duration(t1 - t0).with_position(('center', 800))
```

**Engagement comment (R3.3):**
```python
youtube.commentThreads().insert(part='snippet', body={'snippet': {
    'videoId': video_id,
    'topLevelComment': {'snippet': {'textOriginal': cta_text}}}}).execute()
```

**Quota sanity:** uploads cost 1,600 units each; 2/day + thumbnails (50) + comments (50) ≪ 10,000/day default quota.

**Asset sources:** fonts — github.com/google/fonts (OFL). B-roll — pexels.com, pixabay.com, mixkit.co (check each file's license page; record URL in `assets/CREDITS.md`). Music — YouTube Audio Library (download via Studio; safest for Content ID). SFX — Pixabay/Mixkit.
