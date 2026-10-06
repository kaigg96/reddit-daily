# reddit-daily

Automated YouTube Shorts channel: twice a day, a GitHub Action turns the top
post of a question subreddit (`config.SUBREDDITS`, rotated per run; PRD R4.1)
+ its top 3 comments into a captioned vertical video and uploads it. See [PRD.md](PRD.md) for the quality roadmap and requirement IDs,
and [TECH_DEBT.md](TECH_DEBT.md) for the code-health check-in log.

## Picking this up (new session / new contributor)

Run **`/pickup`** (`.claude/skills/pickup/`), which walks this section and the
delivery plan, then reports where things stand before touching anything. Doing
it by hand instead — read in this order; it's ~5 minutes and avoids re-deriving
decisions:

1. **`PRD.md` §0 "Delivery plan"** — the product's source of truth: what's
   shipped, what's next, and the experiment backlog with its pre-committed
   decision rules. **Update it whenever anything ships.** The company around
   the product — its goal, its other functions' queue and its risks — is in
   **`PLAN.md`**, and who owns what in **`ORG.md`**.
2. **This README's "How it works"** (below) — the actual pipeline.
3. **`PRD.md` §4 Findings** — read this for almost any question, not just
   metrics ones. Review 2 item 6 (age-matching, and that Review 1 is "not
   trustworthy as stated") is load-bearing, and several plausible-sounding
   ideas were killed by data recorded there.
4. **`TECH_DEBT.md`** — only for code-health work.

Standing conventions, non-negotiable (the full set, with the reasoning, is in
[CLAUDE.md](CLAUDE.md) — loaded automatically in every session):
- **AWS Polly costs real money — never synthesize in bulk.** It is the only
  billed service here ($16/1M chars, billed twice per segment because of the
  speech-mark call). Production is ~$0.90/month; a batch job is where a
  surprise bill comes from. Reuse the mp3s in `assets/gen/` when iterating on
  visuals, and ask the owner before any deliberate bulk synthesis.
  `POLLY_CHAR_BUDGET` in `src/tts.py` enforces a per-process cap.
- Feature work goes on a branch; `main` runs live twice daily (see below).
- Work autonomously and merge your own work (owner, 2026-09-19) — under the
  gates in `.claude/skills/shift/SKILL.md` §4. Safety and cost controls,
  production data and spending still need the owner.
- Answer performance questions with `scripts/report.py`, never ad-hoc analysis
  (see "Answering 'did X work?'").
- Never credit AI tooling in code, commits, or anything published.
- **Record any finding you don't fix** in `TECH_DEBT.md` → "Open items (logged
  between passes)". A diagnosis that lives only in a commit message is
  invisible to the next session — that is how a known CSV line-ending problem
  went unrecorded through an otherwise complete feature.

## How it works

`python -m src.run` (entry point, run by
[.github/workflows/run-reddit-video.yml](.github/workflows/run-reddit-video.yml)):

1. `src/content.py` — pick this run's subreddit (morning and evening split
   the list, and the start moves on each day), walk its top posts, applying the basic
   filters (NSFW, profanity, emoji, >90-char titles, yesterday's repeat), and
   gather a pool of ~8 eligible comments per candidate.
2. `src/screen.py` — **suppression-risk screen** (PRD R4.6). One Gemini call
   per candidate decides: skip the post, drop individual risky answers (the
   pool backfills), or pass. Two uploads have been silently zeroed by
   YouTube "limited distribution"; this avoids publishing that shape of
   content. Categories sit in **two tiers** — only those with a confirmed
   zeroed upload behind them (or a severity that never fires here) may discard
   a whole post; the rest can only drop an answer, because a skip costs the
   top-ranked candidate of the day and a drop costs nothing. Fails open — an
   API error never blocks an upload. The same call also classifies the post's
   topic, logged for performance tracking.
3. `src/llm.py` — Gemini generates SEO keywords, a CTR-oriented title (style
   A/B/C rotates by day), and a question-specific CTA. All fail soft; the
   video ships either way.
4. `src/tts.py` — AWS Polly narrates every segment (one voice per video) and
   returns **word-level speech marks** that drive the animated captions.
5. `src/video.py` assembles one continuous timeline: no silent gaps,
   karaoke-style captions, question header + `ANSWER n/3` progress badge,
   persistent watermark, whoosh SFX between answers, background music.
   Background layers come from `src/background.py` (b-roll from
   `assets/broll/`, else a procedural drifting-glow animation), the thumbnail
   from `src/thumbnail.py`, and a `.srt` subtitle track from the same caption
   timings. Renders 1080x1920@30.
6. `src/youtube.py` — upload video, thumbnail, subtitle track, and an
   engagement comment posted from the channel account.
7. On success `src/log.py` appends `upload_log.csv` (one row per upload — the
   experiment log, joined against analytics on `video_id`) and, when the
   screen acted, `analysis/screen_log.csv` (audit trail for weekly
   false-positive review). Both plus `prev_post.txt` are committed back by the
   workflow.

`src/analytics.py` holds the OAuth client helpers and channel-video-listing
logic shared by the reporting scripts below (`weekly_analytics.py`,
`weekly_digest.py`, `analyze_channel.py`) — all three read the live channel
via OAuth, no separate Data API key needed.

The Monday job (`weekly-analytics.yml`) also appends
`analysis/traffic_sources.csv` — views by traffic source (PRD R4.7), at three
cohort scopes: `channel_lifetime`, `channel_7d` (a fresh non-overlapping window
each week, so the series shows drift), and `logged_uploads` (the current-format
cohort — **read this one for decisions**; lifetime is mostly pre-overhaul v1
content). Per-video breakdown isn't possible: the Analytics API rejects
`dimensions="video,insightTrafficSourceType"` and a `video==` filter aggregates
the list rather than splitting it. The digest surfaces the 7d mix as one line.

## Dry runs (never touch the channel)

```sh
DRY_RUN=1 python -m src.run
```

Renders everything to `assets/gen/` and prints the would-be metadata, but
skips upload, thumbnail, and all state mutations. In GitHub: *Actions → Run
workflow → dry_run: true* — the rendered video is attached as a workflow
artifact for review. A shift holds no render credentials, so it asks instead:
`scripts/dry_run.py request <branch>` queues a render that `dry-run.yml` runs
with no YouTube credentials, recording the verdict in `.github/last-dry-run.md`
(the video is attached to that run too).

## Development workflow (standing convention)

**`main` is the deployment branch — the video workflow runs from it twice
daily, so `main` must always be in a runnable state.** Because of that:

- **Do feature work on a branch**, not on `main`. Any change beyond a trivial
  one-liner (a new requirement, a multi-file change, anything touching the
  upload path) goes on a `feature/<short-name>` branch. Half-finished code must
  never sit on `main`, or the next scheduled run executes it.
- **Merge to `main` once the automated gates pass** (revised 2026-09-19 — the
  owner-review step is retired): tests green → `DRY_RUN=1` produces a playable
  MP4 and sane metadata → bump `FORMAT_VERSION` if the video changed → merge →
  live. One variable per release, so the cohort stays separable.
  (See PRD §8 "Delivery model & rollout".)
- The GitHub Actions bot commits `prev_post.txt` / `upload_log.csv` /
  `analysis/*` back to `main` directly — that's expected and separate from
  feature work.

This applies to every version release (`v4`, `v5`, …), not just the first one.

## Local setup

```sh
python3.10 -m venv venv && venv/bin/pip install -r requirements.txt
```

Secrets go in `.env` (gitignored): `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`,
`REDDIT_USER_AGENT`, `AWS_POLLY_ACCESS_KEY`, `AWS_POLLY_SECRET_ACCESS_KEY`,
`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`,
`GEMINI_API_KEY`. The same names exist as Actions secrets in CI.

## One-time setup tasks (owner)

1. ~~**B-roll library (PRD R1.3)**~~ — done 2026-08-15: 7 dark/moody Pexels
   clips in `assets/broll/`, sources in `assets/CREDITS.md`. To add more:
   `venv/bin/python scripts/prep_broll.py <downloaded file> <short_name>`,
   then record the source URL. Prefer dark/mid-tone footage — bright clips
   wash out the white captions even under the scrim.
2. **Music variety (PRD R1.6, optional — still open).** The current track
   (`funk_bg_lower.mp3`) is from the YouTube Audio Library and license-clean.
   For per-video variety, drop 2–3 more Audio Library tracks into
   `assets/music/` (rotation is automatic) and list them in
   `assets/CREDITS.md`.

### OAuth re-auth (reference — already done)

Completed 2026-07-19: the consent screen is published to production (refresh
tokens no longer expire after 7 days) and the token carries upload +
channel-management + analytics scopes. Keeping the walkthrough here in case
the token ever needs re-minting (e.g. new scopes for a future phase):

1. **Publish the OAuth consent screen** if it ever reverts to Testing status
   (Testing caps refresh tokens at 7 days; production tokens don't expire
   while in regular use). [console.cloud.google.com](https://console.cloud.google.com)
   → the project owning the OAuth client → **APIs & Services → OAuth
   consent screen** (newer console: *Google Auth Platform → Audience*) →
   **Publish app**. Do **not** submit for verification — not needed for
   personal use.
2. **Mint a new token** (only after step 1, or the 7-day expiry sticks):
   `venv/bin/python regen_refresh_token.py` → a browser tab opens → sign
   in with the **channel's** Google account → on the "Google hasn't
   verified this app" screen click **Advanced → Go to … (unsafe)** →
   approve all three permissions → the script prints the refresh token.
3. **Store it**: GitHub repo → Settings → Secrets and variables →
   Actions → `YOUTUBE_REFRESH_TOKEN` → Update → paste. Also replace
   `YOUTUBE_REFRESH_TOKEN` in the local `.env`.
4. **Verify** (optional, uploads nothing — a read the old upload-only
   scope couldn't do):

   ```sh
   venv/bin/python -c "
   from src.analytics import youtube_client
   yt = youtube_client()
   print('token OK for:', yt.channels().list(mine=True, part='snippet')
         .execute()['items'][0]['snippet']['title'])"
   ```

## Answering "did X work?"

```sh
venv/bin/python scripts/report.py                          # channel overview
venv/bin/python scripts/report.py --by format_version      # group by any upload_log field
venv/bin/python scripts/report.py --by topic --metric views
venv/bin/python scripts/report.py --compare background_type=broll   # age-matched two-way test
```

Always use this rather than ad-hoc analysis — it enforces the rules that
ad-hoc scripts kept getting wrong (see TECH_DEBT.md Pass 2): **watch-seconds**
is the primary metric (avg-%-viewed is a ratio inflated by simply trimming the
video), cohorts must be **age-matched** or no verdict is given, thin cohorts
report "insufficient data" instead of a misleading median, zero-view
videos are counted separately as suppression candidates rather than averaged
in, and `--compare` **excludes videos where the field is unset** rather than
sweeping the whole pre-field history into the opposing cohort. Logic lives in `src/insights.py` and is unit-tested.

```sh
venv/bin/python scripts/report.py --zeros    # 0-view videos, classified
```

**Which data source to use.** `report.py` reads the **live APIs**, so it is
current. `analysis/traffic_sources.csv` is weekly-snapshot data too, and has no
`report.py` path — it is small enough to read directly. `analysis/analytics_snapshots.csv` is a *weekly* snapshot and can be up
to 8 days stale — fine for trends, wrong for "did this specific video get
suppressed?". For a fresh question about a recent video, always go live;
`--zeros` does.

Zero-view videos are classified rather than listed flat, because three things
masquerade as suppression and all have caused wrong conclusions here:
**non-public** videos (owner-privatised — 10 of the channel's 41 zeroes),
**cold-spell** zeroes (the whole channel was dead that week, so it wasn't
per-video moderation), and videos **too new to judge** (under 3 days old — a
fresh upload has no views yet and every neighbour is older, so it always looks
isolated). Only the **isolated** ones are real candidates.

```sh
venv/bin/pip install -r requirements-dev.txt && venv/bin/python -m pytest tests/
```

**After changing the R4.6 screen** (prompt wording or taxonomy), also run the
live-Gemini regression — unit tests can't reach the half of the behaviour that
lives in the prompt:

```sh
venv/bin/python scripts/replay_screen.py
```

It costs one Gemini call per case against the same free-tier quota production
uses, so run it once rather than in a loop. The screen fails open, so an
exhausted quota degrades live runs to the keyword backstop until it resets
rather than breaking them.

## Versioning & experiments

`FORMAT_VERSION` in `src/config.py` stamps every upload-log row; bump it when
a release goes live. Work splits into **keepers** (high-confidence, batch-shipped,
no per-change bake) and **experiments** (might-revert bets, shipped one variable
at a time with a pre-committed decision rule and a ≥20-upload bake) — see PRD §8.
Judge changes on **watch-seconds**, not avg-%-viewed, and always against an
age-matched cohort (PRD §4); `scripts/report.py` enforces both.
