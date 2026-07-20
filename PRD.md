# PRD: Reddit Shorts Pipeline — Video Quality Overhaul

| | |
|---|---|
| **Status** | Phase 0 + 1 live (`v2`) — measuring; see status section below |
| **Date** | 2026-07-18 |
| **Owner** | kaigg96 |
| **Implementer** | Automated tooling with full repo access |
| **Repo** | github.com/kaigg96/reddit-daily (local folder: `reddit-digest`) |

---

## 0. Implementation status & next steps *(living section — update when anything ships)*

**Last updated:** 2026-07-19 · **Live format:** `v2` (commit `eb7b716`, first live upload 2026-07-18)

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
| R2.1–R2.2 | Title hygiene, style rotation | ⬜ v3 | start after v2 measurement window |
| R2.3 | Branded thumbnail | 🟡 partial | basic card pulled forward into v2 |
| R3.1–R3.5 | CTA, 2nd voice, auto-comment, watermark, SRT | ⬜ v4 | **blocked on one-time OAuth re-auth (owner)** |
| R4.1 | Subreddit rotation | ⬜ v5 | |
| R4.2 | Weekly analytics pull | ⬜ v5 | needs re-auth scopes |
| R4.3 | Historical content analysis | ✅ 2026-07-19 | 869 videos analyzed → `analysis/topic_performance.md`; re-run anytime (`scripts/analyze_channel.py`, classifications cached). Add `YOUTUBE_DATA_API_KEY` to Actions secrets before R4.2's weekly job |
| R4.4 | Topic avoidance gate | ⬜ | depends on R4.3 findings + owner-approved blocklist |
| R5.1–R5.2 | Localization | 🔒 gated | requires proven format (see Phase 5 gate) |

Also shipped outside the numbered requirements: audio-mix calibration (music ~10 dB under voice, SFX ~-20 dBFS peaks), `CHANNEL_NAME` = "AskReddit Shorts" branding, no-AI-attribution scrub.

### Next steps, in order

1. ~~YouTube Data API key + R4.3~~ ✅ done 2026-07-19 — findings in `analysis/topic_performance.md`. Owner: review it and note tentative `BLOCKED_TOPICS`/preferred-topics candidates for R4.4 (no action ships without approval; current evidence favors *preferring* nostalgia/dark-morbid/humor-absurd over blocking anything — weak buckets are mild, not toxic).
2. **Owner (~30 min, anytime):** b-roll curation (`scripts/prep_broll.py` + README instructions). Optional: extra Audio Library tracks into `assets/music/` for variety. Also add `YOUTUBE_DATA_API_KEY` to GitHub Actions secrets (already in local `.env`) so R4.2's weekly job can use it later. Safe mid-window: every video logs which background/music it used, so their effect is separable.
3. **Wait for data:** v2 needs ≥14 days / ≥20 uploads (~Aug 1). Watch in Studio per Short: *viewed vs swiped away* (target ≥70%), *average % viewed* (target ≥70%), median views.
4. **Then Phase 2 (`v3`):** title hygiene + style rotation. Nothing needed from owner.
5. **Then Phase 3 (`v4`):** owner runs the one-time OAuth re-auth (expanded scopes in `regen_refresh_token.py`), then CTA/second-voice/auto-comment/watermark/SRT land together.
6. **Phase 4 (`v5`)** after its evaluation window; **Phase 5** only when its gate is met.

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

All metrics via YouTube Studio / Analytics API, evaluated over ≥ 14 days or ≥ 20 uploads per format version — individual Shorts are high-variance; never judge a change on 1–2 videos.

| Area | Metric | Baseline | Target after P1–P3 |
|---|---|---|---|
| Retention | Average % viewed (avgViewPercentage) | unknown (likely <40%) | **≥ 70%** on ≤ 35s videos |
| Retention | "Viewed vs swiped" (Shorts feed, Studio only) | unknown | ≥ 70% viewed |
| Distribution | Median views/Short, trailing 14d | < 100 | ≥ 1,000 (milestone 1) |
| Engagement | Likes per 100 views | unknown | ≥ 3 |
| Engagement | Comments per 100 views | unknown | ≥ 0.3 |

Directional, not contractual — the algorithm is stochastic. The system's job is to make every upload *worthy* of distribution and measurable (R0.2), so format versions can be compared honestly.

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

Priorities: **P0** = must ship first / prerequisite. **P1** = core value. **P2** = valuable, ship after P1s. **P3** = nice-to-have/stretch.

### Phase 0 — Enabling work

#### R0.1 — DRY_RUN mode — **P0**
- Env var `DRY_RUN` (truthy → dry run). When set: render the full video to `assets/`, print the would-be title/description/tags/CTA-comment, and **skip** YouTube upload, thumbnail set, comment posting, and `prev_post.txt`/log mutations.
- Add a `dry_run` boolean input to the workflow's `workflow_dispatch` (default `false`) wired to the env var, so CI dry runs are triggerable. Scheduled runs remain live.
- **Acceptance:** `DRY_RUN=1` local run produces a playable MP4 and touches nothing remote; grep confirms every mutating call is behind the flag.

#### R0.2 — Upload/experiment log — **P0**
- Append one row per successful **live** upload to `upload_log.csv` (committed back by the workflow alongside `prev_post.txt`): `timestamp_utc, video_id, subreddit, post_title, video_title, title_style, voice, bg_clip, music_track, format_version, duration_s`.
- `FORMAT_VERSION` string constant in code; `"v1"` = pre-overhaul; bump on each phase rollout (`v2` = Phase 1 live, etc.). This is the backbone that makes every experiment in this PRD measurable against YouTube analytics (join on `video_id`).
- **Acceptance:** header row + append logic; workflow commit step updated to add exactly `prev_post.txt upload_log.csv`; dry runs don't append.

#### R0.3 — Notebook → module refactor — **P1 (recommended, not optional in practice)**
Nearly every requirement below touches Cell 7's monolith; refactor first: `src/` package (suggested: `content.py` (Reddit), `llm.py` (Gemini), `tts.py` (Polly), `video.py` (assembly), `youtube.py` (upload/comment), `run.py` (orchestrator reading env)). Workflow runs `python -m src.run` instead of nbconvert (drop the nbconvert install). Keep or delete the notebook; if kept, it must not be the executed path.
- **Acceptance:** `DRY_RUN=1 python -m src.run` produces an equivalent video locally; a `workflow_dispatch` dry run passes in CI.

#### R0.4 — Committed brand font — **P0** (prerequisite for R1.2)
- Commit an OFL display font to `assets/fonts/` — recommended: **Anton** (ultra-bold, condensed — the genre standard look), downloadable from the google/fonts GitHub repo (OFL license; commit the license file too). Pass the **file path** to `TextClip(font=...)` everywhere; delete the Lato/Arial try/except. Record in `assets/CREDITS.md`.
- **Acceptance:** identical rendering locally and in CI; no font-name resolution at runtime.

#### R0.5 — Hygiene fixes — **P2**
- Gitignore `*TEMP_MPY*` moviepy temp files; fix thumbnail upload mimetype (`image/png`); sanitize Gemini title output (strip wrapping quotes/newlines, collapse whitespace, hard-cap ≤ 100 chars, fallback to `reddit_title`); set `selfDeclaredMadeForKids: false` in upload status; switch category to 24 (Entertainment).

### Phase 1 — Retention (highest leverage; ship together as `v2`)

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

### Phase 2 — Packaging / CTR (`v3`)

#### R2.1 — Title hygiene — **P1**
- Remove the `" #shorts #foryou"` suffix (auto-detection makes it useless; it costs characters and credibility). Description: keep question + answers + link; trim hashtags to ≤ 3 (`#AskReddit` etc.). Sanitization per R0.5.

#### R2.2 — Title-style rotation experiment — **P1**
- Three Gemini prompt variants: **A** curiosity rephrase (current), **B** direct-address second person ("You'll never guess…" / "Which of these are you?"), **C** number-led ("3 answers that…"). Select deterministically (e.g., `day_of_year % 3`), record `title_style` in `upload_log.csv`. Evaluation happens offline against analytics (R4.2) — no in-code winner-picking.
- **Acceptance:** style distribution roughly uniform across a week of dry-run simulations; logged correctly.

#### R2.3 — Branded thumbnail template — **P3 (deliberately deprioritized)**
- Thumbnails don't render in the Shorts feed; they matter only on channel/search/browse surfaces. Replace the frame-0 screenshot with a Pillow-generated card: dark background, Anton headline (Gemini-shortened ≤ 8-word version of the question), channel mark (R3.4). Keep < 2 MB, correct mimetype.

### Phase 3 — Engagement & persona (`v4`)

> **Prerequisite:** one-time OAuth re-consent with expanded scopes. Update [regen_refresh_token.py](regen_refresh_token.py) `SCOPES` to `["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/yt-analytics.readonly"]`; owner runs it locally once and updates the `YOUTUBE_REFRESH_TOKEN` secret. Document in README. All Phase 3/4 API features must degrade gracefully (log + skip) if the token lacks scopes.

#### R3.1 — Question-specific CTA — **P1**
- Replace the generic outro. Gemini generates a ≤ 12-word CTA tied to the question (e.g., "Comment the city you thought of — no explaining."; fallback: current generic line). Voiced by the **primary narrator voice** (fixes the Danielle hardcode bug), captioned per R1.2, total segment ≤ 3s. Additionally overlay a small "⬇ comment your answer" strip during the final comment so the ask lands before peak drop-off.
- **Acceptance:** dry-run output shows question-specific CTA text; voice matches narrator across all segments.

#### R3.2 — Two-voice reaction beat — **P2**
- The *unused* voice of {Danielle, Stephen} delivers one Gemini-written quip (≤ 10 words, reacting to one comment — prompt for "surprised/amused friend" tone, no profanity) placed after comment 2 as a mid-video pattern interrupt. Distinct caption color for the second voice. **Fails soft:** any Gemini/Polly error → omit the beat entirely, video still valid.
- This is also the start of an actual channel persona (and helps the "meaningfully transformed content" bar for YPP review).

#### R3.3 — Auto-post engagement comment — **P2**
- After a live upload, post one top-level comment from the channel account via `commentThreads().insert` (requires `youtube.force-ssl` scope) — content: the CTA question or a "Which answer wins — 1, 2, or 3?" prompt. Respect DRY_RUN. Fail soft.
- **Known limitation:** the Data API cannot **pin** comments (no such endpoint) — pinning stays manual and optional; do not build for it.

#### R3.4 — Persistent watermark/brand mark — **P2**
- Small semi-transparent (~60%) channel mark, corner of the safe area, all frames. Fetch the channel title at runtime via `channels().list(mine=True)` (needs re-auth scopes; cache it; fall back to a hardcoded constant) and render as a text mark in the brand font — no logo file required, zero manual steps.

#### R3.5 — Machine-readable content surfaces — **P2**
- Upload a real subtitle track per video via `captions().insert` (requires this phase's `youtube.force-ssl` scope). The word-level timings from Polly speech marks make generating an accurate `.srt` nearly free — the pipeline already has every timestamp. Real caption tracks improve accessibility, search indexing, and how well every legitimate machine reader (YouTube's own content-understanding systems, search engines, AI assistants that surface and summarize video) can parse the video.
- Keep descriptions fully self-describing (already true: question + all answers in plain text). The description is the channel's crawlable text surface — never degrade it into teaser copy.
- **Scope boundary:** this requirement is about maximal legibility to legitimate machine readers, which compounds with human discovery. It is explicitly NOT bot-view optimization — see §7 for why that is excluded.

### Phase 4 — Content & measurement loop (`v5`)

#### R4.1 — Subreddit rotation (Q&A-mode) — **P2**
- Config list of question-style subreddits (e.g., AskReddit, NoStupidQuestions, AskMen, AskWomen, AskUK — owner-editable constant). Rotate deterministically per run; existing filters apply; log `subreddit` (R0.2).
- Replace `prev_post.txt` with `recent_posts.txt`: rolling last 30 posted titles (dedupe window across all subs). Migrate the workflow commit step.
- **Story-mode subs (r/tifu, r/AmItheAsshole, r/confession) are a stretch (P3):** different format — Gemini condenses the selftext to a ≤ 35s script, CTA becomes a verdict poll ("NTA or YTA? Comment."). Build only after Q&A rotation ships and has data.

#### R4.2 — Weekly analytics pull — **P2**
- Second workflow (weekly cron): YouTube Analytics API v2 (`yt-analytics.readonly`) `reports.query` with `dimensions=video` for recent uploads → append `analytics.csv` (committed): views, likes, comments, shares, averageViewDuration, averageViewPercentage. Join key: `video_id` from `upload_log.csv`. Note: impressions / swipe-rate may not be exposed by the API (Studio-only) — implementer should verify current API surface and include them only if available.
- This closes the loop: every experiment in this PRD becomes evaluable from two committed CSVs.
- Also append a weekly public-stats snapshot for **all** uploads to `analysis/stats_snapshots.csv` (views/likes/comments per video_id + date), so views@7d / views@28d deltas become computable going forward (see R4.3, which otherwise has only single-snapshot data).

#### R4.3 — Historical content-performance analysis — **P1, sequencing-independent**
- **Motivation:** ~2 uploads/day since early 2025 means several hundred published Shorts whose descriptions embed the complete content (question + 3 answers). This is an unused dataset for learning which topics and phrasings get distributed vs. suppressed. Suppression is a real mechanism, not just taste: advertiser-unfriendly topics (tragedy, sex-adjacent, drugs, ongoing legal/news stories) can receive limited distribution on Shorts. Note the honest framing: low views for a topic may mean algorithmic suppression *or* weak audience interest — the analysis can't fully separate them, but both point to the same action (avoid the topic), so the ambiguity doesn't block the mechanism.
- **Data acquisition — no OAuth needed.** All required fields (title, description, tags, publishedAt, duration, viewCount, likeCount, commentCount) are public metadata, fetchable with a free **YouTube Data API key** (new Actions/`.env` secret `YOUTUBE_API_KEY`; see OQ-4): derive the uploads playlist from the channel id (`UC…` → `UU…`), page through `playlistItems.list`, then `videos.list(part=snippet,statistics,contentDetails)` in batches of 50 (1 quota unit per call — the whole channel costs <20 units of the 10k/day budget). Output: `analysis/channel_videos.csv`.
- **Content recovery:** parse question + answers back out of each description (the format is stable across v1 and v2: `Today's top AskReddit post: …` + numbered comments).
- **Analysis** (`scripts/analyze_channel.py`, run locally or via a `workflow_dispatch`; outputs committed under `analysis/`):
  - Control for confounders before comparing anything: video age (views accumulate), upload slot (00:00 vs 12:00 UTC), and format version (everything pre-v2 is old format). Compare age-adjusted residuals (e.g., regress log-views on age) or quantiles within rolling cohorts — never raw view counts across months.
  - **Topic buckets:** batch-classify each question via Gemini into a fixed taxonomy (~12 buckets, e.g. relationships/dating, money/work, dark-morbid, politics-news, fame-celebrity, nostalgia, humor-absurd, sex-adjacent, health, hypotheticals, life-advice, other). Report per-bucket n and median adjusted performance.
  - **Distinctive-terms pass:** TF-IDF / distinctive n-grams of top-quartile vs bottom-quartile videos over question+answer text.
  - **Deliverable:** `analysis/topic_performance.md` — ranked buckets, winner/loser terms, and explicit caveats (correlation ≠ causation, small-n buckets, algorithm drift over the sample period).
- **Acceptance:** CSVs + report committed and reproducible; zero OAuth scopes used; findings framed as hypotheses with proposed `BLOCKED_TOPICS` candidates for R4.4.

#### R4.4 — Topic avoidance gate at selection — **P2 (depends on R4.3 results)**
- At selection time, classify the candidate post's title into the R4.3 taxonomy (one Gemini call, **fail-open**: on any error no post is blocked) and skip candidates whose bucket is in a `BLOCKED_TOPICS` config list — selection already iterates the top 10 posts, so it falls through to the next candidate.
- **Policy:** the analysis *proposes* the blocklist; the owner approves it before it ships — a data artifact must not silently change content policy. Add a `topic` column to `upload_log.csv` so the gate's effect is itself measurable, and bump `FORMAT_VERSION` when the gate first ships (a content-selection change is a format change for attribution purposes).
- **Acceptance:** dry run with a seeded candidate list shows a blocked-topic post being skipped; `topic` logged per upload; fail-open path verified.

### Phase 5 — Localization: one channel per language (`v6+`)

**Gate:** start only after the English format is proven — ≥1 month of post-v2 data with retention around the ≥70% target and a clearly rising view floor. Localization multiplies a format's reach; it cannot fix a format that doesn't retain, and every new channel independently faces its own YPP thresholds (1,000 subs + 10M Shorts views/90d **per channel**). Do not start Phase 5 to rescue a weak format.

**Structure decision:** separate channel per language, mapped 1:1 (the owner's instinct is correct): audience-language coherence is what lets YouTube's recommender build a stable audience per channel, and the multi-audio-track feature does not apply to Shorts. The same Google account can own all channels as brand accounts; OAuth consent is granted per channel, yielding one refresh-token secret per channel (`YOUTUBE_REFRESH_TOKEN_ES`, …).

#### R5.1 — Spanish pilot channel — **P2 (post-gate)**
- Same daily selected post → Gemini translates question + answers + title + description (prompt for natural colloquial Spanish, not literal; keep proper nouns) → Polly Spanish neural voices (Lupe es-US / Mia es-MX / Sergio es-ES; confirm speech-mark support per voice) → the existing visual system unchanged (Anton covers Spanish diacritics) with localized fixed strings (header, outro, CTA) → upload to the ES channel.
- Bookkeeping: add a `channel` column to `upload_log.csv`; per-channel dedupe files; render sequentially in the same Action run (~5 extra minutes).
- Language economics: while the goal is the 10M-view threshold, pick volume-first languages (Spanish, Portuguese-BR, Hindi have the largest Shorts populations). High-CPM/low-volume locales (German, French) only matter post-YPP.
- **Acceptance:** one DRY_RUN produces both language videos; ES upload path verified against the pilot channel; per-channel log rows separable.

#### R5.2 — Additional languages; RTL support — **P3**
- Portuguese-BR (Camila/Thiago) and Hindi (Kajal) are near drop-ins on the R5.1 template.
- **Arabic is not a drop-in.** RTL + script shaping means: Pillow must be built with libraqm (otherwise Arabic renders as disconnected left-to-right letters — visibly broken), an Arabic-script font is required (Cairo or Tajawal, OFL), caption grouping must display in RTL order (the existing byte-offset handling already survives multibyte UTF-8), and Polly Arabic voices (Hala/Zayd, ar-AE) need speech-mark verification. Treat Arabic as its own mini-project with frame-level visual verification before anything uploads.
- At >3 languages, move from sequential rendering to a workflow matrix to keep job time reasonable.

## 7. Explicitly out of scope

- Paid services (ElevenLabs, stock subscriptions, editors). Any per-video manual step. Posting-frequency increases. Engagement manipulation of any kind. Long-form video. Shorts poll stickers (not exposed via API). Comment pinning (no API). Reposting/compiling third-party video content. Migrating off the notebook's current infra (Actions + Polly + Gemini stack stays).
- **Bot-view optimization.** Excluded on both factual and policy grounds. Factual: YPP thresholds count only *valid* public views — YouTube filters traffic it identifies as automated *before* it counts, so views from external bots/scrapers have approximately zero monetization yield regardless of how well content caters to them. Policy: deliberately cultivating artificial traffic falls under YouTube's fake-engagement enforcement (up to channel termination) — an uncapped downside against a ~zero upside, aimed at the exact asset we're trying to monetize. The legitimate core of the idea — content that machines can accurately read, index, and surface — is in scope as R3.5 and costs nothing extra given the speech-mark infrastructure.

## 8. Sequencing & rollout

1. **Phase 0** entirely (R0.1 first — nothing else proceeds without DRY_RUN).
2. **Phase 1** as one release: dry-run in CI → owner reviews the sample MP4 (attach as a workflow artifact) → owner approves → bump `FORMAT_VERSION` to `v2` → live.
3. **Phase 2** (`v3`), **Phase 3** (`v4` — after the one-time re-auth), **Phase 4** (`v5`), each gated the same way: dry-run artifact → owner approval → version bump → live. **Phase 5** (`v6+`) additionally requires its own gate (see the Phase 5 section) before it may start.
4. Evaluate each version only after ≥ 14 days or ≥ 20 uploads; compare medians by `format_version` via the two CSVs.

Do not interleave phases — attribution requires clean version boundaries.

Exception: **R4.3 (historical analysis) is read-only with respect to published content** — it changes nothing viewers see — so it may run at any time, including during v2's measurement window. Only its downstream gate (R4.4) is a content change and rolls out like any phase.

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
- **OQ-4 — R4.3 credentials:** ~~resolved 2026-07-19~~ — owner created a Data API key as `YOUTUBE_DATA_API_KEY` (note: this name, not `YOUTUBE_API_KEY`); in local `.env`, still to be added to Actions secrets for R4.2.
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
