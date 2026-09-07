# PRD: Reddit Shorts Pipeline — Video Quality Overhaul

| | |
|---|---|
| **Status** | `v5` live (suppression screen shipped 2026-08-23); next: R4.4 topic/hook ranker — see §0 Delivery plan |
| **Date** | 2026-07-18 |
| **Owner** | kaigg96 |
| **Implementer** | Automated tooling with full repo access |
| **Repo** | github.com/kaigg96/reddit-daily (local folder: `reddit-digest`) |

---

## 0. Status & delivery plan *(living section — update when anything ships)*

**Last updated:** 2026-08-23 · **Live format:** `v5` (suppression screen 2026-08-23; v4 Sprint 1 2026-07-22; v3 packaging 2026-07-19; v2 retention overhaul 2026-07-18)

> **Cadence model (revised 2026-07-22):** work is sorted onto two tracks by *whether we'll act on a change's individual result*, not by theme — a **bar-raising batch** (high-confidence keepers, shipped fast) and an **experiment backlog** (bets, isolated + baked with a pre-committed decision rule). The old "bake every version ~1 month" rule conflated attribution with validation; see §8 for the full rationale and the [Delivery plan](#delivery-plan) below for the concrete bucketing. The v1→v2 retention read that v3's metadata-only design kept clean was cashed in on 2026-07-27 — see §4 Findings.

<a name="delivery-plan"></a>
### Delivery plan *(the single tracker — per-requirement detail lives in §6)*

**Shipped**
- `v2` — retention overhaul (2026-07-18): R0.1–R0.5, R1.1–R1.7 · plus audio-mix calibration (music ~10 dB under voice, SFX ~−20 dBFS peaks), "AskReddit Shorts" branding, no-AI-attribution scrub, basic branded thumbnail card (R2.3 partial)
- `v3` — packaging (2026-07-19): R2.1 title hygiene, R2.2 title-style A/B/C rotation
- `v4` — Sprint 1 bar-raising batch (2026-07-22, via `feature/sprint-1`): R3.1a question CTA, R3.3 auto-comment, R3.4 watermark, R3.5 subtitle tracks, R4.5 cron de-jitter — caption + comment live paths **verified in production 2026-07-27**
- Standalone (no version bump): R4.2 weekly analytics + digest (2026-07-20) · R4.3 historical topic analysis (2026-07-19) · OAuth production consent + expanded scopes (2026-07-19 — ended the weekly token chore) · R1.3 b-roll library completed (2026-08-15, 7 clips — first live use on the next scheduled run after push)
- `v5` — suppression-risk screen (2026-08-23, via `feature/r4.6-suppression-screen`): R4.6. Validated pre-merge: 3/3 confirmed-suppressed cases skipped with correct category; replay over 18 live uploads = skip 6% / drop 11% / pass 83%, the single skip being exactly the video that was zeroed. Also fixed a digest false-positive (zero-view alert fired on videos postdating the last snapshot: 12 → 1).
- The Sprint-1-era open question — *did production quality move retention?* — was answered 2026-07-27: distribution yes (3.5× median views), retention no. See §4 Findings.

#### Next keepers

| Item | Req | Decision rule |
|---|---|---|
| ~~Suppression-risk screen~~ ✅ `v5` | R4.6 | Shipped 2026-08-23. **Standing audit:** review `analysis/screen_log.csv` weekly (digest surfaces a line whenever skips occurred); if skips look like false positives or exceed ~15% of candidates, narrow the prompt rather than revert. Screen is mitigation, not a guarantee — the digest zero-view flag remains the detector for categories it hasn't learned yet. |
| Traffic-source telemetry in weekly job | R4.7 | Keep — measurement-only, no version bump; ship whenever convenient. |

#### Experiment backlog (isolated, pre-committed decision rule, ≥20-upload / ~2-week bake)

Reordered 2026-08-23 after Review 2 (§4 Findings): duration is not a lever, so the format-geometry experiments are cancelled and content/hook quality moves to the top.

| # | Item | Req | Decision rule (pre-committed) |
|---|---|---|---|
| 1 | **Topic/hook candidate ranker** | R4.4 | Score the top-10 candidates on hook strength + topic prior (seeded from `analysis/topic_performance.md`), pick the best rather than always #1. After ≥20 uploads: keep if median **watch-seconds** and median views both hold or improve vs an age-matched baseline; revert if either drops materially. |
| 2 | Subreddit rotation — *inventory prerequisite for volume* | R4.1 | Compare age-adjusted median views per subreddit after ≥15 uploads each; drop underperformers vs the AskReddit baseline. Success unlocks the posting-volume revisit (§7). |
| 3 | Posting-volume increase (2 → 3–4/day) | — | Only after R4.1 proves inventory quality; hold per-video medians within ~30% of baseline at higher volume, else fall back. |
| 4 | Localization (per-language channels) | R5.1–R5.2 | Gated — requires a proven English format first (R5 localization gate). |
| 5 | Upload-time-of-day optimization | R4.5 (deferred half) | Deferred until there's enough volume per slot. Not a growth lever. |
| 6 | Two-voice reaction beat | R3.2 | Persona value, unclear retention effect. Now judged on **watch-seconds**, not avg-% (its old demotion rationale — "adds length" — died with the duration thesis). Revert if watch-seconds drop vs age-matched baseline after ≥20 uploads. |
| ~~—~~ | ~~Short format (R1.8) / narration rate (R1.9)~~ | — | **Cancelled 2026-08-23.** Both assumed shortening raises real retention. Data says duration doesn't separate winners from losers (`corr(duration, log views) = −0.17`; top-12 median 19.2s vs 19.8s for the rest) and that trimming only inflates the avg-% proxy. See §4 Findings, Review 2. |

#### Owner tasks (anytime, no version bump)
- ~~**B-roll library** (R1.3)~~ ✅ 2026-08-15 — 7 dark/moody Pexels clips live (`assets/broll/`, sources in CREDITS.md). Nine curated, two dropped at the R1.4 legibility gate for washing out white captions. Pipeline auto-switched off the procedural background; `bg_clip` logged per upload so per-clip performance is separable later. Expectation (§4): first-impression/swipe margin, not the watch budget.
- **Music variety** (R1.6): drop 2–3 more YouTube Audio Library tracks into `assets/music/`; rotation is automatic.
- **Review `analysis/topic_performance.md`** → tentative preference list for R4.4 (evidence favors *preferring* nostalgia/dark-morbid/humor-absurd over blocking).

---

## 1. Background & goal

This repo generates and uploads a YouTube Short twice daily (00:00 and 12:00 UTC) from the top r/AskReddit post of the day. Videos currently average **under 100 views each**. The owner's goal is YouTube Partner Program monetization, whose Shorts route requires **1,000 subscribers + 10M valid public Shorts views in a trailing 90-day window** (the long-form route is 4,000 watch-hours/12mo). At 2 posts/day, 10M/90d implies ~55K average views per video — the strategy is to (a) raise the floor via production quality and (b) raise the ceiling (hit probability) via better hooks and content variety.

Sub-100 views on Shorts means the algorithm's initial test pool (a few hundred impressions served automatically to every new Short) is not converting. The dominant signal for further distribution is **retention** (viewed vs. swiped away, average % watched), followed by engagement (likes/comments/shares per view). "Click rate" in the classic thumbnail sense barely applies inside the Shorts feed — the real analog is **surviving the first 1–2 seconds**. Titles/thumbnails matter mainly on search, channel page, and browse surfaces.

A secondary motivation: YPP review rejects "repetitious/duplicative" content. A TTS reading of Reddit comments over a static image is close to that line. The personality/production requirements below (motion, editing, commentary voice) also serve to make the content clearly transformed.

## 2. Starting system — the v1 baseline this PRD replaced *(historical; superseded at v2)*

At the time this PRD was written, everything lived in one notebook, `create_video.ipynb` (deleted in the 2026-08-23 cleanup; recoverable from git history), executed headlessly by [.github/workflows/run-reddit-video.yml](.github/workflows/run-reddit-video.yml) via `jupyter nbconvert --to notebook --execute` on `ubuntu-latest`, Python 3.10.

Pipeline (cell by cell):

1. **Cell 0–1 — setup.** PRAW (r/AskReddit), boto3 Polly client (`us-west-2`). `MAX_COMMENT_LENGTH = 150`.
2. **Cell 2 — content selection.** Top post of the day (`time_filter='day'`, limit 10) filtered for: NSFW, profanity (`better_profanity`), title > 90 chars, emoji, and equality with `prev_post.txt` (last posted title). Top 3 comments ≤ 150 chars, not deleted, no emoji/profanity. Raises if < 3 valid comments (run fails, nothing posts).
3. **Cell 3 — Gemini keywords.** `gemini-2.5-flash` REST call → 10 SEO keywords. Fails soft (empty list).
4. **Cell 4 — Gemini title.** CTR-optimized rephrasing of the question. Fails soft (falls back to Reddit title).
5. **Cell 5–6 — Polly TTS.** Neural engine, voice randomly `Danielle` or `Stephen` for title + 3 comments. Fixed outro "Like, subscribe, and comment your answer below!" — **bug: always voiced by Danielle even when Stephen narrates**.
6. **Cell 7 — video assembly (MoviePy 2.1.2).** Sequence: `gap(0.5s) → title → gap → "Reddit's top responses..." (audio only, blank screen) → gap → comment1 → gap → comment2 → gap → comment3 → gap → outro`. Every segment is a **static** 1080×1920 `assets/bg.png` (white with orange Reddit logos in bottom third) with the full text as one orange (`#ff5d01`) static block (font `Lato-Bold` in CI, `Arial` locally, via try/except). Background music `assets/funk_bg_lower.mp3` (unknown provenance/license) under the whole video. Output: 1080×1920@30fps H.264, ~28s. Thumbnail = frame 0 of title clip.
7. **Cell 8 — upload.** YouTube Data API v3, refresh-token auth. Title = Gemini title + `" #shorts #foryou"`. Description = question + 3 comments + link + hashtags. Category 22. Then `thumbnails().set()` (PNG sent with `image/jpeg` mimetype). 
8. **Cell 9 — dedupe.** Writes posted title to `prev_post.txt`; workflow commits it back.

**Environment (kept current — this block describes the system as it is today, not the v1 baseline above):**
- **Runtime:** Python 3.10 on `ubuntu-latest`, entry point `python -m src.run`. Twice daily at `23 0,12 * * *` (off the hour to dodge Actions queue jitter), plus a `workflow_dispatch` with a `dry_run` input.
- **Secrets in Actions:** `REDDIT_*`, `AWS_POLLY_*`, `YOUTUBE_CLIENT_ID`/`_SECRET`/`_REFRESH_TOKEN`, `GEMINI_API_KEY`. Local dev reads the same names from `.env` (gitignored). `YOUTUBE_DATA_API_KEY` exists locally but is no longer used by any script.
- **OAuth:** the refresh token carries `youtube.upload`, `youtube.force-ssl` (comments + captions) and `yt-analytics.readonly`. The consent screen is published **in production**, so tokens no longer expire after 7 days (see README for the re-mint walkthrough).
- **Fonts:** Anton is committed to `assets/fonts/` and passed to `TextClip` by path — no system font installation, so CI and local renders are identical.
- **MoviePy 2.1.2** — 2.x API only; see Appendix A for the specific gotchas. (`moviepy.__version__` self-reports `2.1.1` despite the 2.1.2 pin — an upstream metadata quirk, not a wrong install.)
- **Gemini usage per run:** 1–4 screen calls (R4.6, capped by `MAX_SCREENED_CANDIDATES`) plus keywords, title, and CTA. Comfortably inside the free tier at 2 runs/day; heavy *local* testing is what exhausts quota, not production.

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

**Review 2 (2026-08-23, n=66 logged uploads, live Analytics, ≥3 days old) — supersedes parts of Review 1.**

1. **Duration is NOT a lever — the earlier "shorten the video" conclusion was wrong.** `corr(duration, log views) = −0.17`; the top 12 videos and the rest have effectively the **same** median duration (19.2s vs 19.8s). What separates them is **watch-seconds** (11.0s vs 9.0s) and the avg-% that follows from it.
2. **Avg-%-viewed is a gameable proxy and must not be a target.** Watch-seconds are roughly flat against duration (`corr = +0.13`), so trimming a video mechanically inflates avg-%-viewed while adding zero real watch time. R1.8/R1.9 were built on exactly this mistake and are **cancelled** — they would have "passed" their decision rule while delivering nothing.
3. **What predicts views:** `corr(avg-%-viewed, log views) = +0.34` and `corr(watch-seconds, log views) = +0.34` — equal. Since duration doesn't differ between winners and losers, the differentiator is **content/hook quality**, not format geometry (promotes R4.4 to the top of the backlog). Note +0.34 leaves most variance unexplained: much of Shorts success is outside anything we currently measure, so treat R4.4 as improving odds per slot, not as a reliable lever.
4. **Loops are real upside that shortening cannot buy:** the best performers include a 17s video at **227% avg-viewed** (40s watched) and another at 100%. Watch-seconds above duration only come from content worth re-watching.
5. **Distribution gain from the overhaul confirmed and larger than first measured:** v4 median **166 views** (n=52) vs recent-era v1 median **28** (n=76) — roughly 6× (Review 1 estimated 3.5× on n=14).
6. **Methodological rule now binding: cohorts must be age-matched.** Avg-%-viewed *declines as a video ages* (broader, colder audiences). Same-week (3–9d) videos sit at ~65% regardless of background, while the older overall pool sits near 48–50%. Two consequences: (a) **b-roll shows no measurable retention effect** once age-matched (65.5% vs 64.9%) — an apparent advantage was pure age artifact; (b) Review 1's "retention didn't move" claim compared v4 against much older v1 videos and is **not trustworthy as stated** — the distribution half stands, the retention half is unresolved.

**Review 1 (2026-07-27, n=14, two snapshots) — retained for history; items 1 and 2 below are superseded above.**

1. ~~Production quality moved distribution, not retention~~ — distribution finding confirmed (and revised upward to ~6×); the retention half was age-confounded (see Review 2 item 6).
2. ~~Fixed watch budget ⇒ length is the retention lever~~ — the *observation* (viewers give ~9–12s) holds; the *inference* (therefore shorten) was wrong (Review 2 items 1–2).
3. **Views and retention are decoupled at this scale** — holds, and strengthened: topic/hook drives expansion more than format geometry.

Strategic implication (unchanged): 10M views/90d ≈ 110K/day vs the current ~1–2K/week — floor-raising alone can never cover that distance. Sequencing goal: maximize hit probability per slot (hook, topic), then multiply slots (volume after R4.1).

## 5. Constraints & guardrails (binding on the implementer)

1. **$0 budget.** No new paid services. Existing Polly/Gemini/YouTube usage stays. (Note: Polly neural is ~$16/1M chars once past free tier; speech-mark calls double character usage → still ≈ $1–2/mo at 60 videos. Accepted. Gemini 2.5 Flash free tier covers the added calls.)
2. **100% automated per-video.** No human step per upload. One-time setup tasks (asset curation, OAuth re-consent) are allowed and must be clearly documented in the README when introduced.
3. **Must run headlessly on `ubuntu-latest`** GitHub Actions, twice daily, within reasonable job time (< 30 min).
4. **DRY_RUN guardrail (build first — R0.1).** All development/verification runs must use DRY_RUN. **Never upload to the live channel, post comments, or mutate `prev_post.txt`/logs during development.** The first live run of any new format version requires explicit owner approval.
5. **Never commit secrets.** `.env`, `client_secret.json`, `token.json` stay gitignored. (`praw.ini` was removed 2026-08-23 — Reddit auth reads `REDDIT_*` from the environment.) When extending the workflow's commit step, `git add` only the specific intended files (never `-A`).
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
  - Control for confounders before comparing anything: video age (views accumulate), upload slot (00:00 vs 12:00 UTC), and format version (everything pre-v2 is old format). Compare age-adjusted residuals (e.g., regress log-views on age) or quantiles within rolling cohorts — never raw view counts across months.
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
- **As-built:** "AskReddit Shorts", 34px, 55% opacity, low-center (y=1500) — clear of captions, header, and the Shorts UI.

#### R3.5 — Machine-readable content surfaces — **✅ v4 (caption tracks live-verified 2026-07-27)**
- Upload a real subtitle track per video via `captions().insert` (requires `youtube.force-ssl` scope). The word-level timings from Polly speech marks make generating an accurate `.srt` nearly free — the pipeline already has every timestamp. Real caption tracks improve accessibility, search indexing, and how well every legitimate machine reader (YouTube's own content-understanding systems, search engines, AI assistants that surface and summarize video) can parse the video.
- Keep descriptions fully self-describing (already true: question + all answers in plain text). The description is the channel's crawlable text surface — never degrade it into teaser copy.
- **Scope boundary:** this requirement is about maximal legibility to legitimate machine readers, which compounds with human discovery. It is explicitly NOT bot-view optimization — see §7 for why that is excluded.

#### R4.5 — Upload-time predictability & logging — **✅ v4 shipped; ⚠️ partially regressed (2026-09-07)**
- **Original problem:** scheduled runs published 45–105 min after their cron slot — top-of-hour GitHub Actions queue congestion plus ~7–11 min of pipeline runtime — making publish time unpredictable across a ~60-min window.
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
- A basic branded card already ships (since v2: dark bg frame, channel tag, full question). This spec is the full version — Gemini-shortened ≤ 8-word headline, channel mark. Deferred per "include if cheap, else defer": thumbnails don't render in the Shorts feed, so the marginal value is limited to channel/search/browse surfaces. Revisit only if those surfaces ever matter (see R4.7 traffic-source data).

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

#### R4.7 — Traffic-source telemetry — **Keeper (measurement-only, no version bump)**
- Add `insightTrafficSourceType` (Analytics API dimension) to the weekly snapshot job — per-video or channel-level views by source (Shorts feed / search / browse / external).
- **Why:** tells us whether the SEO surface (tags, titles-for-search, SRT) earns anything, or whether distribution is ~100% Shorts feed — which decides whether search-oriented work is ever worth revisiting. Currently flying blind on this.
- **Acceptance:** new column(s)/file appended by the Monday job; a first snapshot committed.

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

#### R4.4 — Topic/hook candidate ranker — **Experiment #1 (top of backlog, promoted 2026-08-23)**
- At selection time, classify the candidate post's title into the R4.3 taxonomy (one Gemini call, **fail-open**: on any error no post is blocked) and skip/deprioritize candidates by bucket — selection already iterates the top 10 posts, so it falls through to the next candidate. (Current R4.3 evidence favors a *preference ranker* — prefer nostalgia/dark-morbid/humor-absurd when available — over an outright blocklist; weak buckets are mild, not toxic.)
- **Policy:** the analysis *proposes* the list; the owner approves it before it ships — a data artifact must not silently change content policy. Add a `topic` column to `upload_log.csv` so the gate's effect is itself measurable, and bump `FORMAT_VERSION` when the gate first ships (a content-selection change is a format change for attribution purposes).
- **Design principle (owner, 2026-08-23) — deviation from Reddit's ranking requires justification.** The channel's premise is human-generated *and* human-validated content: upvotes are free, high-quality signal that the content already landed with real people. Overriding that ranking with our own judgment is allowed, but only where we can name a specific reason our audience's preference diverges — never merely because we think we know better.
  - **Grounded, so in scope:** topic priors measured on *our own* channel. Age-adjusted over n=607 classified videos, the spread between best and worst topic bucket is ~1.6× (dark-morbid +0.58 / nostalgia +0.56 / humor-absurd +0.51 at the top; fame-celebrity +0.13 / money-work +0.13 / life-advice +0.15 at the bottom). Reddit's top-of-day ranking is topic-agnostic; our audience is not. Mechanism: Reddit voters read threaded text with full context, our viewer gets ~20s of narration with none.
  - **Not grounded, so cut:** LLM "hook strength" scoring. Unvalidated, subjective, and it substitutes machine judgment for the human vote signal that is the point of the channel. Removed from scope.
  - **Precedent:** we already deviate (≤150-char comment filter, profanity/emoji/NSFW filters, R4.6 screen), so this is a question of degree and basis, not principle.
- **Revised mechanism — Reddit rank is the default, our data is a narrow exception.** Take the top-ranked eligible post *unless* its topic sits in the measured-weak tier **and** another candidate within the top few sits in the measured-strong tier. This layers our audience's revealed preference on top of Reddit's rather than replacing it. **Comments are not reordered** — within a single thread, vote ranking is the strongest signal available and the audience mismatch is smallest; only R4.6 may drop a comment.
- **Step 0 — ✅ shipped 2026-08-23 (telemetry only, no behavior change).** `candidate_rank` and `topic` are now logged per upload (`upload_log.csv`; topic piggybacks on the existing R4.6 screen call, so zero extra Gemini quota). Existing filters already push selection off rank 1 sometimes, so this accumulates the counterfactual we've never had: **does taking a lower-ranked post actually cost views?** Build the ranker only once that data supports it — if rank turns out not to matter, the topic exception is cheap; if lower ranks measurably underperform, the exception bar should rise.
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

- **Unit tests:** `venv/bin/pip install -r requirements-dev.txt && venv/bin/python -m pytest tests/` — covers the pure analysis logic (`src/insights.py`). Run before any change touching selection, logging, or analysis.
- **Render:** `DRY_RUN=1 python -m src.run`.
- **Structure:** `ffprobe -show_entries format=duration,stream=width,height,avg_frame_rate` → 1080×1920@30, 20–40s.
- **Dead air:** `ffmpeg -i out.mp4 -af silencedetect=n=-35dB:d=0.3 -f null -` → no detected silence.
- **Visuals:** extract frames (`ffmpeg -vf fps=1`) at t=0.3, mid-title, each comment, CTA → verify caption word-groups, header/badge, watermark, legibility, motion (pixel-diff two frames 3s apart).
- **Caption sync:** unit check comparing speech-mark times to caption clip start times (±150 ms).
- **Safety greps:** every network mutation (`videos().insert`, `thumbnails().set`, `commentThreads().insert`, file/log writes) is behind the DRY_RUN flag; workflow commit step adds only intended files.
- **CI:** `workflow_dispatch` with `dry_run=true` must pass end-to-end on `ubuntu-latest` before any live rollout.
- **Performance questions:** use `scripts/report.py` (`--by`, `--compare`, `--metric`) — never ad-hoc analysis. It enforces watch-seconds-primary, age-matched cohorts, and n-gating; see TECH_DEBT.md Pass 2 for why that matters.
- **Screen behaviour:** after changing `src/screen.py`, re-check it against the three confirmed-suppressed cases and the five fine-serving controls listed in R4.6 before merging.
- **Never** verify by uploading publicly. If an end-to-end upload test is ever truly needed, ask the owner first (option: `privacyStatus: "private"` test upload, then delete — owner approval required).

## 10. Open questions (defaults apply if unanswered)

- **OQ-1 — B-roll sourcing:** ~~resolved 2026-08-15~~ — manual curation chosen and done (7 Pexels clips). No API key needed. Selection criterion learned in practice: dark/mid-tone only; two of nine candidates were rejected at the R1.4 legibility gate for washing out white captions.
- **OQ-2 — Channel brand name:** ~~resolved 2026-07-22~~ — hardcoded `CHANNEL_NAME = "AskReddit Shorts"` in `src/config.py` rather than fetched per run; it never changes, and a constant avoids an API call plus a failure mode on the render path.
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
