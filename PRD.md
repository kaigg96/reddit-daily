# PRD: Reddit Shorts Pipeline — Video Quality Overhaul

| | |
|---|---|
| **Status** | `v4` live (Sprint 1 shipped 2026-07-22); next: R4.6 suppression-risk screen (`v5`) — see §0 Delivery plan |
| **Date** | 2026-07-18 |
| **Owner** | kaigg96 |
| **Implementer** | Automated tooling with full repo access |
| **Repo** | github.com/kaigg96/reddit-daily (local folder: `reddit-digest`) |

---

## 0. Implementation status & next steps *(living section — update when anything ships)*

**Last updated:** 2026-07-27 · **Live format:** `v4` (Sprint 1 bar-raising batch shipped 2026-07-22; v3 packaging 2026-07-19; v2 retention overhaul 2026-07-18)

> **Cadence model (revised 2026-07-22):** work is sorted onto two tracks by *whether we'll act on a change's individual result*, not by theme — a **bar-raising batch** (high-confidence keepers, shipped fast) and an **experiment backlog** (bets, isolated + baked with a pre-committed decision rule). The old "bake every version ~1 month" rule conflated attribution with validation; see §8 for the full rationale and the [Delivery plan](#delivery-plan) below for the concrete bucketing. Prior note (still true): v3 was metadata-only, so v1→v2 retention remains a clean comparison.

### Requirement status

| Req | What | Status | Notes |
|---|---|---|---|
| R0.1 | DRY_RUN mode | ✅ v2 | workflow `dry_run` input attaches sample artifact |
| R0.2 | upload_log.csv | ✅ v2 | first row logged 2026-07-18 |
| R0.3 | Notebook → `src/` | ✅ v2 | notebook kept but deprecated |
| R0.4 | Anton font | ✅ v2 | owner confirmed Anton over 3 alternatives |
| R0.5 | Hygiene fixes | ✅ v2 | title sanitize, madeForKids, category 24, mimetype |
| R1.1 | No dead air, hook at 0 | ✅ v2 | silencedetect-verified |
| R1.2 | Word-timed captions | ✅ v2 | Polly speech marks |
| R1.3 | Motion background | ✅ v2 | procedural glow live; **b-roll library empty (owner task)** |
| R1.4 | Caption legibility | ✅ v2 | dark bg + stroke; scrim ready for b-roll |
| R1.5 | Header + progress badge | ✅ v2 | + question pinned across answers (owner feedback) |
| R1.6 | Music + SFX | ✅ v2 | SFX synthesized; track confirmed YT Audio Library (2026-07-18); extra tracks optional for variety |
| R1.7 | Duration guard | ✅ v2 | + 2.0s min display for short answers (owner feedback) |
| R1.8 | Short format (~14–16s: 2 comments, no spoken outro) | ⬜ experiment — **top of backlog** | strongest prior on the board: fixed ~10–12s watch budget (§4 findings); absorbs R3.1b |
| R1.9 | Narration rate (+~10% SSML) | ⬜ experiment | same watch-budget thesis; run after R1.8 |
| R2.1 | Title hygiene | ✅ v3 | hashtag suffix removed; description ≤3 hashtags |
| R2.2 | Title style rotation | ✅ v3 | A/B/C by day-of-year; logged per upload |
| R2.3 | Branded thumbnail | 🟡 partial | basic card live since v2; full Gemini-headline version deferred (low value — not in feed) |
| R3.1a | CTA wording (question-specific) + voice fix | ✅ v4 | Gemini CTA, markdown-stripped, fail-soft |
| R3.1b | CTA placement | 🔀 absorbed into R1.8 | the no-spoken-outro arm is the live question; overlay strip ships with R1.8 |
| R3.2 | Two-voice reaction beat | ⬜ experiment — **demoted to bottom** (2026-07-27) | adds length + interruption, directly against the watch-budget finding |
| R3.3 | Auto-post engagement comment | ✅ v4 | commentThreads.insert, fail-soft; first fires on next live run |
| R3.4 | Persistent watermark | ✅ v4 | "AskReddit Shorts", 55% opacity, low-center, all frames |
| R3.5 | Subtitle (SRT) track | ✅ v4 | SRT from caption timings + captions.insert, fail-soft |
| R4.5 | Cron de-jitter + publishedAt logging | ✅ v4 | cron `23 0,12` + pip cache; publish_hour derivable from snapshot |
| R4.6 | Suppression-risk screen | ⬜ **next keeper (`v5`)** | evidence-anchored: 2 confirmed limited-distribution zeroings (sexual-suggestive, graphic medical harm) |
| R4.7 | Traffic-source telemetry | ⬜ keeper (no version bump) | add `insightTrafficSourceType` to weekly job — feed-vs-search split |
| R4.1 | Subreddit rotation | ⬜ experiment — **reframed** (2026-07-27) | inventory prerequisite for a future posting-volume increase, not just a content bet |
| R4.2 | Weekly analytics pull + digest | ✅ 2026-07-20 | `weekly-analytics.yml` Mondays 06:00 UTC → `analysis/analytics_snapshots.csv` + **weekly digest GitHub issue** (owner-approved layout: status/health/performance/top video/TODOs; emails via GitHub notifications). Single-file design via Analytics API OAuth — no Data API key in CI; impressions confirmed not API-exposed. **Deferred until scale warrants** (owner 2026-07-20): engagement-rate scoreboard (when median views/Short ≳500), per-video `subscribersGained` (when subs ≳100), exact rolling-90d windowed views query, experiments section in digest |
| R4.3 | Historical content analysis | ✅ 2026-07-19 | 869 videos analyzed → `analysis/topic_performance.md`; re-run anytime (`scripts/analyze_channel.py`, classifications cached). Migrated to OAuth 2026-07-21 (refactor pass) — no longer needs `YOUTUBE_DATA_API_KEY`; see TECH_DEBT.md |
| R4.4 | Topic avoidance/preference gate | ⬜ experiment | depends on R4.3 findings + owner-approved list |
| R5.1–R5.2 | Localization | 🔒 gated | requires proven format (see R5 localization gate) |

Also shipped outside the numbered requirements: audio-mix calibration (music ~10 dB under voice, SFX ~-20 dBFS peaks), `CHANNEL_NAME` = "AskReddit Shorts" branding, no-AI-attribution scrub.

<a name="delivery-plan"></a>
### Delivery plan

Two tracks (rationale in §8). Every unshipped item is tagged Sprint 1 (bar-raising keeper) or Experiment (bet), and carries a decision rule.

**Expectation:** Sprint 1 raises/defends the *floor* (production quality) — it is **not** expected to spike views. The ceiling levers (content, hooks, titles) live in the experiment backlog. Flat views during Sprint 1 ≠ failure.

**One read kept honest (non-blocking):** did v1→v2 actually move retention? Still recoverable (v3 was metadata-only), matures on its own in the weekly digest, consulted before over-investing in the "production quality → retention" thesis — but does **not** gate Sprint 1.

#### Sprint 1 — bar-raising batch ✅ shipped as `v4` (2026-07-22)

| Item | Req | Status |
|---|---|---|
| Subtitle (SRT) track upload | R3.5 | ✅ SRT from caption timings + `captions.insert` (fail-soft) |
| Question-specific CTA *wording* (+ narrator-voice fix) | R3.1a | ✅ Gemini CTA, markdown-stripped, fail-soft to generic |
| Auto-post engagement comment | R3.3 | ✅ `commentThreads.insert` (fail-soft); first fires next live run |
| Persistent watermark / brand mark | R3.4 | ✅ 55% opacity, low-center, all frames |
| Cron de-jitter + pip caching + `publishedAt` | R4.5 | ✅ cron `23 0,12` + pip cache; publish_hour derivable from snapshot |
| B-roll library *(owner asset task)* | R1.3 | ⬜ owner, anytime — no version bump. *Expectation recalibrated 2026-07-27: affects first-impression/swipe margin, not the watch budget (§4)* |
| Extra music tracks *(owner asset task)* | R1.6 | ⬜ owner, anytime — drops in with no version bump |
| Branded thumbnail card | R2.3 | ⏸ full Gemini-headline version deferred (low value — not shown in feed) |

Code merged to `main` via `feature/sprint-1` (fast-forward, branch deleted). The two owner asset tasks remain optional and version-bump-free. Untested until the first live run: the real `captions.insert` / `commentThreads.insert` calls (both fail-soft — a scope/API hiccup logs and continues without breaking the upload).

#### Next keeper release (`v5`) + measurement keepers

| Item | Req | Decision rule |
|---|---|---|
| Suppression-risk screen at selection | R4.6 | Keep; audit `analysis/screen_log.csv` weekly — if skips look like false positives or exceed ~15% of candidate posts, narrow the prompt rather than revert. |
| Traffic-source telemetry in weekly job | R4.7 | Keep — measurement-only, no version bump; ship whenever convenient. |

#### Experiment backlog (isolated, pre-committed decision rule, ≥20-upload / ~2-week bake)

Reordered 2026-07-27 by prior strength after the watch-budget findings (§4).

| # | Item | Req | Decision rule (pre-committed) |
|---|---|---|---|
| 1 | **Short format** (~14–16s: 2 comments, no spoken outro; CTA as overlay + pinned comment only) | R1.8 | After ≥20 uploads: keep if median avg-%-viewed ≥65% **and** median views ≥ the prior-format baseline; revert if views drop >30% despite the retention gain. Absorbs R3.1b. |
| 2 | Narration rate (+~10% via Polly SSML prosody) | R1.9 | After ≥20 uploads: keep if avg-%-viewed and views hold or improve; revert on a clear views drop. Run after R1.8 settles. |
| 3 | Topic/hook candidate ranker | R4.4 | Owner-approved list only; `topic` logged per upload; keep only buckets/rankings that hold up in R4.3-style analysis. Upgraded rationale: views↔retention decoupling (§4) says hook/topic drives test-pool expansion. |
| 4 | Subreddit rotation — *inventory prerequisite for volume* | R4.1 | Compare age-adjusted median views per subreddit after ≥15 uploads each; drop underperformers vs the AskReddit baseline. Success unlocks the posting-volume revisit (§7). |
| 5 | Posting-volume increase (2 → 3–4/day) | — | Only after R4.1 proves inventory quality; hold per-video medians within ~30% of baseline at higher volume, else fall back. |
| 6 | Localization (per-language channels) | R5.1–R5.2 | Gated — requires a proven English format first (R5 localization gate). |
| 7 | Upload-time-of-day optimization | R4.5 (deferred half) | Deferred until retention is solved + enough volume per slot. Not a growth lever. |
| 8 | Two-voice reaction beat — **demoted** | R3.2 | Adds length against a fixed watch budget — weakest prior on the board. If ever run: revert if beat cohort median avg-%-viewed ≥2 pts below non-beat after ≥20 uploads. |

#### Done / owner-side
- ~~Engagement (R3.x) OAuth prerequisite~~ ✅ 2026-07-19 — production consent screen + expanded scopes; killed the weekly-token chore permanently.
- ~~R4.3 historical analysis~~ ✅ — owner to review `analysis/topic_performance.md` for tentative R4.4 candidates (evidence favors *preferring* nostalgia/dark-morbid/humor-absurd over blocking anything).

---

## 1. Background & goal

This repo generates and uploads a YouTube Short twice daily (00:00 and 12:00 UTC) from the top r/AskReddit post of the day. Videos currently average **under 100 views each**. The owner's goal is YouTube Partner Program monetization, whose Shorts route requires **1,000 subscribers + 10M valid public Shorts views in a trailing 90-day window** (the long-form route is 4,000 watch-hours/12mo). At 2 posts/day, 10M/90d implies ~55K average views per video — the strategy is to (a) raise the floor via production quality and (b) raise the ceiling (hit probability) via better hooks and content variety.

Sub-100 views on Shorts means the algorithm's initial test pool (a few hundred impressions served automatically to every new Short) is not converting. The dominant signal for further distribution is **retention** (viewed vs. swiped away, average % watched), followed by engagement (likes/comments/shares per view). "Click rate" in the classic thumbnail sense barely applies inside the Shorts feed — the real analog is **surviving the first 1–2 seconds**. Titles/thumbnails matter mainly on search, channel page, and browse surfaces.

A secondary motivation: YPP review rejects "repetitious/duplicative" content. A TTS reading of Reddit comments over a static image is close to that line. The personality/production requirements below (motion, editing, commentary voice) also serve to make the content clearly transformed.

## 2. Current system (as-built)

Everything lives in one notebook, [create_video.ipynb](create_video.ipynb), executed headlessly by [.github/workflows/run-reddit-video.yml](.github/workflows/run-reddit-video.yml) via `jupyter nbconvert --to notebook --execute` on `ubuntu-latest`, Python 3.10.

Pipeline (cell by cell):

1. **Cell 0–1 — setup.** PRAW (r/AskReddit), boto3 Polly client (`us-west-2`). `MAX_COMMENT_LENGTH = 150`.
2. **Cell 2 — content selection.** Top post of the day (`time_filter='day'`, limit 10) filtered for: NSFW, profanity (`better_profanity`), title > 90 chars, emoji, and equality with `prev_post.txt` (last posted title). Top 3 comments ≤ 150 chars, not deleted, no emoji/profanity. Raises if < 3 valid comments (run fails, nothing posts).
3. **Cell 3 — Gemini keywords.** `gemini-2.5-flash` REST call → 10 SEO keywords. Fails soft (empty list).
4. **Cell 4 — Gemini title.** CTR-optimized rephrasing of the question. Fails soft (falls back to Reddit title).
5. **Cell 5–6 — Polly TTS.** Neural engine, voice randomly `Danielle` or `Stephen` for title + 3 comments. Fixed outro "Like, subscribe, and comment your answer below!" — **bug: always voiced by Danielle even when Stephen narrates**.
6. **Cell 7 — video assembly (MoviePy 2.1.2).** Sequence: `gap(0.5s) → title → gap → "Reddit's top responses..." (audio only, blank screen) → gap → comment1 → gap → comment2 → gap → comment3 → gap → outro`. Every segment is a **static** 1080×1920 `assets/bg.png` (white with orange Reddit logos in bottom third) with the full text as one orange (`#ff5d01`) static block (font `Lato-Bold` in CI, `Arial` locally, via try/except). Background music `assets/funk_bg_lower.mp3` (unknown provenance/license) under the whole video. Output: 1080×1920@30fps H.264, ~28s. Thumbnail = frame 0 of title clip.
7. **Cell 8 — upload.** YouTube Data API v3, refresh-token auth. Title = Gemini title + `" #shorts #foryou"`. Description = question + 3 comments + link + hashtags. Category 22. Then `thumbnails().set()` (PNG sent with `image/jpeg` mimetype). 
8. **Cell 9 — dedupe.** Writes posted title to `prev_post.txt`; workflow commits it back.

Known environment facts:
- Secrets available in Actions: `REDDIT_*`, `AWS_POLLY_*`, `YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN`, `GEMINI_API_KEY`. Local dev uses `.env` / `praw.ini` (both gitignored, **not tracked** — verified).
- The YouTube refresh token was minted with **only** the `https://www.googleapis.com/auth/youtube.upload` scope ([regen_refresh_token.py](regen_refresh_token.py)). Anything beyond upload/thumbnail (commenting, channel reads, analytics) needs a one-time re-auth with more scopes.
- The workflow installs `ttf-mscorefonts-installer` (Arial, Impact, etc.).
- MoviePy is 2.1.2 — the **2.x API** (`with_duration`, `with_start`, `with_position`, `subclipped`, `resized`, Pillow-backed `TextClip` that wants a **font file path**). Do not use 1.x idioms from old tutorials.
- Stray artifacts exist locally (`final_askreddit_videoTEMP_MPY_wvf_snd.mp3` — crashed-render temp; `assets/.funk_bg.mp3.icloud`). Non-blocking.

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

| Area | Metric | Baseline | Target after P1–P3 |
|---|---|---|---|
| Retention | Average % viewed (avgViewPercentage) | unknown (likely <40%) | **≥ 70%** on ≤ 35s videos |
| Retention | "Viewed vs swiped" (Shorts feed, Studio only) | unknown | ≥ 70% viewed |
| Distribution | Median views/Short, trailing 14d | < 100 | ≥ 1,000 (milestone 1) |
| Engagement | Likes per 100 views | unknown | ≥ 3 |
| Engagement | Comments per 100 views | unknown | ≥ 0.3 |

Directional, not contractual — the algorithm is stochastic. The system's job is to make every upload *worthy* of distribution and measurable (R0.2), so format versions can be compared honestly.

### Findings — two-snapshot data review (2026-07-27)

First real read of the format eras (snapshots 07-21 + 07-27; videos ≥3 days old):

1. **Production quality moved distribution, not retention.** v1 recent cohort (n=83): median 26 views, 54.2% avg-viewed. v2/v3 (n=14): median 90 views (3.5×), max 923 vs 115 — but avg-viewed only 57.1%. The founding "quality → retention → distribution" chain is better described as "quality → first-impression/swipe margin → distribution."
2. **Fixed watch budget ~10–12 s.** Median watch-seconds: v1 = 12.0, v2/v3 = 10.0 — unchanged across a total format overhaul. Avg-%-viewed is therefore ≈ `11s ÷ duration`: every video ≤16s scored 55–74%; every video ≥23s scored 35–37%. **Length, not polish, is the retention lever** — the ≥70% target is expected to be reached via R1.8 (short format), not further production work.
3. **Views and retention are decoupled at this scale.** 923- and 671-view videos sat at ~55% while a 62-view video hit 73.7% — topic/hook drives test-pool expansion at least as much as retention (rationale upgrade for R4.4).

Strategic implication: 10M views/90d ≈ 110K/day vs the current ~1–2K/week — floor-raising alone can never cover that distance. Sequencing goal: maximize hit probability per slot (length, hook, topic), then multiply slots (volume after R4.1).

## 5. Constraints & guardrails (binding on the implementer)

1. **$0 budget.** No new paid services. Existing Polly/Gemini/YouTube usage stays. (Note: Polly neural is ~$16/1M chars once past free tier; speech-mark calls double character usage → still ≈ $1–2/mo at 60 videos. Accepted. Gemini 2.5 Flash free tier covers the added calls.)
2. **100% automated per-video.** No human step per upload. One-time setup tasks (asset curation, OAuth re-consent) are allowed and must be clearly documented in the README when introduced.
3. **Must run headlessly on `ubuntu-latest`** GitHub Actions, twice daily, within reasonable job time (< 30 min).
4. **DRY_RUN guardrail (build first — R0.1).** All development/verification runs must use DRY_RUN. **Never upload to the live channel, post comments, or mutate `prev_post.txt`/logs during development.** The first live run of any new format version requires explicit owner approval.
5. **Never commit secrets.** `.env`, `praw.ini`, `client_secret.json`, `token.json` stay gitignored. When extending the workflow's commit step, `git add` only the specific intended files (never `-A`).
6. **Licensing:** every committed media asset (b-roll, music, SFX, fonts) must be free for commercial use without attribution (CC0/Pixabay License/Mixkit License/YouTube Audio Library/OFL fonts) and its source URL recorded in `assets/CREDITS.md`. No gameplay footage of copyrighted games, no clips with embedded music/watermarks/logos/visible people prominently featured.
7. **Policy:** no fake engagement, no engagement pods, no view manipulation, no posting-frequency increase as a substitute for quality. Existing content filters (NSFW/profanity/emoji) must remain.
8. **Repo hygiene:** each committed b-roll/music file < 25 MB; total new committed assets < 300 MB. (If the library needs to grow beyond that later, move to GitHub Release assets + `actions/cache` — out of scope now.)

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
Nearly every requirement below touches Cell 7's monolith; refactor first: `src/` package (suggested: `content.py` (Reddit), `llm.py` (Gemini), `tts.py` (Polly), `video.py` (assembly), `youtube.py` (upload/comment), `run.py` (orchestrator reading env)). Workflow runs `python -m src.run` instead of nbconvert (drop the nbconvert install). Keep or delete the notebook; if kept, it must not be the executed path.
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
- **Fallback:** if `assets/broll/` is empty/missing → Ken Burns pan/zoom on `bg.png` (`ImageClip.resized(lambda t: 1 + 0.015*t)` + position drift). The pipeline must never render a fully static frame again.
- One-time setup task (owner or implementer-with-browser): download/curate the clips per guidance; record sources in `assets/CREDITS.md`. Alternative if fully-automated sourcing is preferred: free Pexels API key as a new secret + fetch script (decision: **Open Question OQ-1**).
- **Acceptance:** two frames 3s apart are visibly different (pixel-diff > threshold) in every segment; b-roll audio absent; CI artifact plays smoothly.

#### R1.4 — Readability layer over motion — **P0** (part of R1.3/R1.2)
- Captions must stay legible on any b-roll: black stroke per R1.2 **plus** a subtle dark scrim behind the text band (e.g., semi-transparent rounded rect at ~35% opacity) or global slight darken of the b-roll (`multiply` ~0.85). Implementer picks whichever renders cleaner; verify against the brightest clip in the library.
- **Acceptance:** extracted frames over the brightest clip show unambiguous legibility.

#### R1.5 — Persistent context header + progress cue — **P1**
- Small persistent header near the top (inside safe area): the question in compact form on comment segments, or a fixed brand line — plus a **progress badge** ("1/3", "2/3", "3/3") during answers. Signals finite length; carries the "top answers" framing dropped in R1.1.
- **Acceptance:** frames during each comment show the correct badge.

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
- Also append a weekly public-stats snapshot for **all** uploads to `analysis/stats_snapshots.csv` (views/likes/comments per video_id + date), so views@7d / views@28d deltas become computable going forward (see R4.3, which otherwise has only single-snapshot data).

#### R4.3 — Historical content-performance analysis — **shipped ✅ (P1, sequencing-independent)**
- **Motivation:** ~2 uploads/day since early 2025 means several hundred published Shorts whose descriptions embed the complete content (question + 3 answers). This is an unused dataset for learning which topics and phrasings get distributed vs. suppressed. Suppression is a real mechanism, not just taste: advertiser-unfriendly topics (tragedy, sex-adjacent, drugs, ongoing legal/news stories) can receive limited distribution on Shorts. Note the honest framing: low views for a topic may mean algorithmic suppression *or* weak audience interest — the analysis can't fully separate them, but both point to the same action (avoid the topic), so the ambiguity doesn't block the mechanism.
- **Data acquisition — originally no OAuth needed.** All required fields (title, description, tags, publishedAt, duration, viewCount, likeCount, commentCount) are public metadata, so this shipped against a free **YouTube Data API key** (avoiding a dependency on the not-yet-unblocked Phase 3 re-auth; see OQ-4): derive the uploads playlist from the channel id (`UC…` → `UU…`), page through `playlistItems.list`, then `videos.list(part=snippet,statistics,contentDetails)` in batches of 50 (1 quota unit per call — the whole channel costs <20 units of the 10k/day budget). Output: `analysis/channel_videos.csv`. **Superseded 2026-07-21:** now that OAuth is live, this script was migrated onto the same authenticated client the other reporting scripts use (`src/analytics.py`), eliminating a second auth mechanism and a hardcoded channel-ID constant — see TECH_DEBT.md.
- **Content recovery:** parse question + answers back out of each description (the format is stable across v1 and v2: `Today's top AskReddit post: …` + numbered comments).
- **Analysis** (`scripts/analyze_channel.py`, run locally or via a `workflow_dispatch`; outputs committed under `analysis/`):
  - Control for confounders before comparing anything: video age (views accumulate), upload slot (00:00 vs 12:00 UTC), and format version (everything pre-v2 is old format). Compare age-adjusted residuals (e.g., regress log-views on age) or quantiles within rolling cohorts — never raw view counts across months.
  - **Topic buckets:** batch-classify each question via Gemini into a fixed taxonomy (~12 buckets, e.g. relationships/dating, money/work, dark-morbid, politics-news, fame-celebrity, nostalgia, humor-absurd, sex-adjacent, health, hypotheticals, life-advice, other). Report per-bucket n and median adjusted performance.
  - **Distinctive-terms pass:** TF-IDF / distinctive n-grams of top-quartile vs bottom-quartile videos over question+answer text.
  - **Deliverable:** `analysis/topic_performance.md` — ranked buckets, winner/loser terms, and explicit caveats (correlation ≠ causation, small-n buckets, algorithm drift over the sample period).
- **Acceptance:** CSVs + report committed and reproducible; findings framed as hypotheses with proposed `BLOCKED_TOPICS` candidates for R4.4. (Original acceptance bar was "zero OAuth scopes used" — no longer applicable after the 2026-07-21 OAuth migration; superseded, not failed.)

---

### Sprint 1 — bar-raising batch (next release, ships as `v4`)

High-confidence, non-regression keepers. Ship together through the review gate (dry-run artifact → owner eyeball → `FORMAT_VERSION` → live); no per-change bake; measured in aggregate.

> **OAuth prerequisite ✅ done 2026-07-19** — scopes `youtube.upload`, `youtube.force-ssl`, `yt-analytics.readonly`; consent screen in production. API features degrade gracefully (log + skip) if a scope is ever missing. Two owner **asset tasks** also land in this batch — b-roll library (completes R1.3) and extra music tracks (R1.6); they're listed in the §0 Delivery plan and not re-specced here.

#### R3.1a — Question-specific CTA wording — **Sprint 1 (keeper)**
- Replace the generic outro. Gemini generates a ≤ 12-word CTA tied to the question (e.g., "Comment the city you thought of — no explaining."; fallback: current generic line). Voiced by the **primary narrator voice** (fixes the Danielle hardcode bug), captioned per R1.2, total segment ≤ 3s.
- **Acceptance:** dry-run output shows question-specific CTA text; voice matches narrator across all segments.

#### R3.3 — Auto-post engagement comment — **Sprint 1 (keeper)**
- After a live upload, post one top-level comment from the channel account via `commentThreads().insert` (requires `youtube.force-ssl` scope) — content: the CTA question or a "Which answer wins — 1, 2, or 3?" prompt. Respect DRY_RUN. Fail soft.
- **Known limitation:** the Data API cannot **pin** comments (no such endpoint) — pinning stays manual and optional; do not build for it.

#### R3.4 — Persistent watermark/brand mark — **Sprint 1 (keeper)**
- Small semi-transparent (~60%) channel mark, corner of the safe area, all frames. Use the `CHANNEL_NAME` constant (already set to "AskReddit Shorts"; optionally confirm live via `channels().list(mine=True)` and cache) rendered as a text mark in the brand font — no logo file required, zero manual steps.

#### R3.5 — Machine-readable content surfaces — **Sprint 1 (keeper)**
- Upload a real subtitle track per video via `captions().insert` (requires `youtube.force-ssl` scope). The word-level timings from Polly speech marks make generating an accurate `.srt` nearly free — the pipeline already has every timestamp. Real caption tracks improve accessibility, search indexing, and how well every legitimate machine reader (YouTube's own content-understanding systems, search engines, AI assistants that surface and summarize video) can parse the video.
- Keep descriptions fully self-describing (already true: question + all answers in plain text). The description is the channel's crawlable text surface — never degrade it into teaser copy.
- **Scope boundary:** this requirement is about maximal legibility to legitimate machine readers, which compounds with human discovery. It is explicitly NOT bot-view optimization — see §7 for why that is excluded.

#### R4.5 — Upload-time predictability & logging — **Sprint 1 (keeper); time-of-day tuning deferred**
- **Problem:** scheduled runs currently publish 45–105 min after their cron slot. Most of that is GitHub Actions queue jitter at the top of the hour (`0 0,12`), plus ~7–11 min of uncached `pip install` + render. The publish time is therefore *unpredictable across a ~60-min window*, which makes any time-of-day analysis impossible.
- **Sprint 1 scope (keeper, plumbing — no growth claim):**
  - Move the cron off the top of the hour (e.g. `23 0,12 * * *`) to dodge queue congestion; cache pip deps (`actions/setup-python` cache or `actions/cache`) to shave render-start latency. If a specific *publish* clock-time is ever targeted, set the cron ~10 min earlier to absorb the irreducible pipeline runtime.
  - Join YouTube's actual `publishedAt` (already pulled in R4.2's snapshot) into the experiment data, and add a `publish_hour_utc` to the analytics join so slot becomes analyzable later.
  - **Acceptance:** post-change scheduled runs land within a tighter, consistent window; `publishedAt` present per video in the joined data.
- **Deferred (experiment backlog):** actually *optimizing* time-of-day. For Shorts the magnitude is genuinely uncertain (long discovery tail, global test pool — weaker lever than for long-form), and it's second-order to retention. Revisit only once retention is solved and there's enough volume per slot for a comparison to mean anything. **Not** framed as a growth lever.

#### R2.3 — Branded thumbnail template — **Sprint 1 (keeper, low priority)**
- A basic frame-0 card already ships (pulled forward into v2); this is the full version. Thumbnails don't render in the Shorts feed — they matter only on channel/search/browse surfaces, hence low priority. Replace the screenshot with a Pillow-generated card: dark background, Anton headline (Gemini-shortened ≤ 8-word version of the question), channel mark (R3.4). Keep < 2 MB, correct mimetype. Include if cheap, else defer.

---

### Next keeper release (`v5`)

#### R4.6 — Suppression-risk screen at selection — **Keeper (content-selection change → own `FORMAT_VERSION` bump, feature branch)**
- **Problem (evidence, 2026-07-27):** two uploads confirmed zeroed by silent **limited distribution** — public, `processed`, *not* age-restricted via API, yet exactly 0 views while same-period uploads got 28–923: `Your Secret Sign: Amazing In Bed?` (sexual-suggestive framing) and `qvNzVCzWebk` / `When Chiropractic Lands You In The ER` (graphic medical harm: "cervical/vertebral artery dissection", "pneumothorax"). Limited distribution is Studio-only — the API cannot see it, so prevention has to happen at selection. Cost of a zeroed upload: a wasted slot and plausibly worse channel-level classifier priors (the stronger "momentum poisoning" claim is unsubstantiated — not the justification here).
- **Counter-evidence that keeps the screen narrow:** Epstein/named-celebrity content served fine (42–923 views incl. an Elon Musk question at 70); three videos *mentioning* chiropractic served fine (95–158). The trigger is the **framing** (suggestive / graphic-harm), not the topic. General "controversy" must NOT be filtered — dark-morbid is a top-performing bucket.
- **Mechanism:** one Gemini call at selection time evaluating the candidate post title + its 3 chosen comments as a package against the categories YouTube's classifiers demonstrably enforce: sexual/suggestive framing · graphic medical harm/injury detail · sexual content in minors' contexts · hard drugs · graphic violence · slurs. Named-individuals-with-criminal-allegations is **log-only** (watched, not filtered — evidence says it isn't suppressed). Use the confirmed-zeroed videos and the fine-serving near-misses above as in-prompt calibration examples.
- **Verdicts:** `skip_post` (question itself risky → selection falls through to the next of the top 10) · `drop_comment` (one risky answer → replace with next valid comment, keep post) · `pass`. **Fail-open:** any Gemini/API error blocks nothing.
- **Audit trail (the anti-over-filtering guard):** every non-`pass` verdict appends to a committed `analysis/screen_log.csv` (date, post title, verdict, category, reason) for weekly owner review. Decision rule: false positives in the log or a skip rate above ~15% of candidates → narrow the prompt, don't revert the screen.
- **Digest addition:** flag logged videos whose `privacyStatus` ≠ public (distinguishes owner-privatized videos from suppression when investigating zero-view flags; the existing 0-views-after-3-days flag remains the suppression detector).
- **Acceptance:** dry run with seeded risky candidates shows skip/drop/pass each firing correctly; fail-open path verified; screen_log row schema written; existing filters (NSFW/profanity/emoji) untouched.

#### R4.7 — Traffic-source telemetry — **Keeper (measurement-only, no version bump)**
- Add `insightTrafficSourceType` (Analytics API dimension) to the weekly snapshot job — per-video or channel-level views by source (Shorts feed / search / browse / external).
- **Why:** tells us whether the SEO surface (tags, titles-for-search, SRT) earns anything, or whether distribution is ~100% Shorts feed — which decides whether search-oriented work is ever worth revisiting. Currently flying blind on this.
- **Acceptance:** new column(s)/file appended by the Monday job; a first snapshot committed.

---

### Experiment backlog

"Might revert" bets. Ship **one variable per version**, each with a real bake window (≥ 20 uploads / ~2 weeks) and a **pre-committed decision rule** (see §8). Order below follows the 2026-07-27 re-prioritization (Delivery plan).

#### R1.8 — Short format — **Experiment, top of backlog (strongest prior)**
- **Thesis (§4 findings):** viewers grant a fixed ~10–12s watch budget; avg-%-viewed ≈ `11s ÷ duration`. Current videos run 15–26s; the ≥23s ones score 35–37%, the ≤16s ones 55–74%. Shrink the video to fit the budget.
- **Format change:** title + **2 comments** (drop the 3rd) + **no spoken outro**. CTA survives as (a) the R3.1a question-specific text rendered as a short overlay strip near the end and (b) the auto-posted pinned-style comment (R3.3). Target duration ~14–16s. Duration guard tightens accordingly.
- Also expected: loop potential (Shorts loops count as re-watches; avg-%-viewed can exceed 100).
- **Trade-off being tested:** less content per video vs. much higher relative retention. Our data shows no view advantage for longer videos (the 23–26s videos: 41–57 views).
- **Absorbs R3.1b** — "no spoken outro + overlay CTA" *is* the placement experiment's live arm.
- **Decision rule:** after ≥20 uploads — keep if median avg-%-viewed ≥65% **and** median views ≥ prior-format baseline; revert if views drop >30% despite the retention gain (distribution didn't follow).
- **Acceptance:** dry-run sample at ~15s with overlay CTA; `FORMAT_VERSION` bump; duration logged.

#### R1.9 — Narration rate — **Experiment (run after R1.8 settles)**
- Same watch-budget thesis from the other side: fit more content per second. Wrap Polly input in SSML `<prosody rate="~110%">` (verify neural-voice SSML support per voice; speech marks must still align — verify timestamps against the sped audio).
- **Decision rule:** after ≥20 uploads — keep if avg-%-viewed and views hold or improve; revert on a clear views drop (too-fast narration reads as spammy).

#### R3.1b — CTA placement — **🔀 absorbed into R1.8 (2026-07-27)**
- The live question ("does removing the spoken outro + overlaying the CTA help?") ships as part of R1.8's format change. No separate experiment.

#### R3.2 — Two-voice reaction beat — **Experiment — demoted to bottom of backlog (2026-07-27)**
- The *unused* voice of {Danielle, Stephen} delivers one Gemini-written quip (≤ 10 words, reacting to one comment — prompt for "surprised/amused friend" tone, no profanity) placed after comment 2 as a mid-video pattern interrupt. Distinct caption color for the second voice. **Fails soft:** any Gemini/Polly error → omit the beat entirely, video still valid.
- Adds mid-video length + an interruption — genuinely could raise or lower retention. Also the start of an actual channel persona (and helps the "meaningfully transformed content" bar for YPP review).
- **Demotion rationale (2026-07-27):** the watch-budget finding (§4) makes anything that *adds* length the weakest prior on the board. Persona value stands, but not at the cost of seconds.
- **Decision rule:** if the reaction-beat cohort's median avg-%-viewed is ≥2 pts below the non-beat cohort after ≥20 uploads → revert.

#### R4.1 — Subreddit rotation (Q&A-mode) — **Experiment — reframed 2026-07-27: inventory prerequisite for posting volume**
- **Why it matters more now:** a future posting-volume increase (backlog #5) needs more than one subreddit's worth of daily post inventory — proving rotation works is the gate to that lever, not just a content experiment.
- Config list of question-style subreddits (e.g., AskReddit, NoStupidQuestions, AskMen, AskWomen, AskUK — owner-editable constant). Rotate deterministically per run; existing filters apply; log `subreddit` (R0.2).
- Replace `prev_post.txt` with `recent_posts.txt`: rolling last 30 posted titles (dedupe window across all subs). Migrate the workflow commit step.
- **Decision rule:** compare age-adjusted median views per subreddit after ≥15 uploads each; drop any that underperform the AskReddit baseline.
- **Story-mode subs (r/tifu, r/AmItheAsshole, r/confession) are a stretch:** different format — Gemini condenses the selftext to a ≤ 35s script, CTA becomes a verdict poll ("NTA or YTA? Comment."). Build only after Q&A rotation ships and has data.

#### R4.4 — Topic avoidance/preference gate at selection — **Experiment (depends on R4.3 results)**
- At selection time, classify the candidate post's title into the R4.3 taxonomy (one Gemini call, **fail-open**: on any error no post is blocked) and skip/deprioritize candidates by bucket — selection already iterates the top 10 posts, so it falls through to the next candidate. (Current R4.3 evidence favors a *preference ranker* — prefer nostalgia/dark-morbid/humor-absurd when available — over an outright blocklist; weak buckets are mild, not toxic.)
- **Policy:** the analysis *proposes* the list; the owner approves it before it ships — a data artifact must not silently change content policy. Add a `topic` column to `upload_log.csv` so the gate's effect is itself measurable, and bump `FORMAT_VERSION` when the gate first ships (a content-selection change is a format change for attribution purposes).
- **Decision rule:** keep only the buckets/rankings that hold up in R4.3-style age-adjusted analysis after the gate has run ≥20 uploads.
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
- **Posting-frequency increases — moved from excluded to conditionally deferred (2026-07-27).** The original exclusion ("no volume as a substitute for quality") was right when quality was poor. With a stable format, volume is the most reliable multiplier toward 10M/90d — but only *after* R4.1 proves multi-subreddit inventory can sustain quality at 3–4/day. See experiment backlog #5; never volume *instead of* fixing a broken format.
- **Bot-view optimization.** Excluded on both factual and policy grounds. Factual: YPP thresholds count only *valid* public views — YouTube filters traffic it identifies as automated *before* it counts, so views from external bots/scrapers have approximately zero monetization yield regardless of how well content caters to them. Policy: deliberately cultivating artificial traffic falls under YouTube's fake-engagement enforcement (up to channel termination) — an uncapped downside against a ~zero upside, aimed at the exact asset we're trying to monetize. The legitimate core of the idea — content that machines can accurately read, index, and surface — is in scope as R3.5 and costs nothing extra given the speech-mark infrastructure.

## 8. Delivery model & rollout

Changes are sorted onto two tracks by one question: **will we act on this change's individual result?** The concrete bucketing is the [Delivery plan](#delivery-plan) in §0; this section is the rationale.

**Why this sorting (and why the old rule was wrong).** There are two distinct reasons to wait between changes, and the original "bake every version ~1 month" rule conflated them:
1. **Attribution** — ship A then B fast, views move, you can't tell which did it.
2. **Validation** — you want to know whether a change worked so you can decide to keep / revert / iterate.
Attribution only has *value* if you'll act on it. For high-confidence changes we'll keep regardless (motion background, captions, branding, subtitles), neither reason applies — so per-change bake time is pure delay. For genuine bets we might revert, both apply — so they get isolated and baked.

**Track 1 — bar-raising batch.** High-confidence, non-regression keepers. Batch-shipped as a single `FORMAT_VERSION`, minimal bake. We deliberately give up *within-batch* attribution (they're all keepers, so we'd never act on it). Measured only in aggregate as a sanity check.

**Track 2 — experiment backlog.** "Might revert" changes. One variable per version, a real bake window (≥ 20 uploads / ~2 weeks), and a **decision rule pre-committed before shipping** (keep/revert/iterate on a named metric threshold). No bet ships without its rule — a bake window with no pre-committed action is just a delay, which was the gap in the original plan (we never defined what to do after the wait).

**The review gate is preserved on both tracks and is *not* the slow part:** feature branch → build → dry-run artifact in CI → owner reviews the sample MP4 → approve → bump `FORMAT_VERSION` → merge to `main` → live. That gate catches actual regressions (a visual bug, a broken render) — distinct from statistical bake time, which is what we compress for keepers. **Feature work happens on a branch, never directly on `main`** — the live workflow runs from `main` twice daily, so it must stay runnable; this is a standing convention documented in the README's *Development workflow* section.

**Sort per-change, not per-phase.** Confidence can be miscalibrated, and the old thematic phases mixed safe and risky work (Phase 3's watermark/subtitles are keepers; its reaction beat is a real retention experiment). Every unshipped item carries an explicit bucket tag in the Delivery plan.

**One clean read is protected:** the v1→v2 retention comparison (does production quality move avg-%-viewed at all?) stays recoverable because v3 was metadata-only. It matures in parallel via the weekly digest and is consulted before over-investing in the production-quality thesis — but does **not** block Sprint 1.

**R4.3 exception retained:** read-only analysis (changes nothing viewers see) may run any time, including mid-bake.

**Localization (R5.x)** keeps its own separate gate (proven English format) on top of all the above.

## 9. Verification playbook (for the implementing agent)

- **Render:** `DRY_RUN=1 python -m src.run` (or notebook equivalent pre-R0.3).
- **Structure:** `ffprobe -show_entries format=duration,stream=width,height,avg_frame_rate` → 1080×1920@30, 20–40s.
- **Dead air:** `ffmpeg -i out.mp4 -af silencedetect=n=-35dB:d=0.3 -f null -` → no detected silence.
- **Visuals:** extract frames (`ffmpeg -vf fps=1`) at t=0.3, mid-title, each comment, CTA → verify caption word-groups, header/badge, watermark, legibility, motion (pixel-diff two frames 3s apart).
- **Caption sync:** unit check comparing speech-mark times to caption clip start times (±150 ms).
- **Safety greps:** every network mutation (`videos().insert`, `thumbnails().set`, `commentThreads().insert`, file/log writes) is behind the DRY_RUN flag; workflow commit step adds only intended files.
- **CI:** `workflow_dispatch` with `dry_run=true` must pass end-to-end on `ubuntu-latest` before any live rollout.
- **Never** verify by uploading publicly. If an end-to-end upload test is ever truly needed, ask the owner first (option: `privacyStatus: "private"` test upload, then delete — owner approval required).

## 10. Open questions (defaults apply if unanswered)

- **OQ-1 — B-roll sourcing:** manual one-time curation by owner (default, better quality control) vs. automated Pexels API fetch (needs a free API key added as a secret). 
- **OQ-2 — Channel brand name** for watermark/persona: default = fetch channel title via API (R3.4).
- **OQ-3 — Caption styling specifics** (colors beyond white/black stroke, highlight color for the second voice): implementer's discretion within the readability rules; keep the orange `#ff5d01` as an accent for brand continuity.
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
