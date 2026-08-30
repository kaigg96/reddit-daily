# reddit-daily

Automated YouTube Shorts channel: twice a day, a GitHub Action turns the top
r/AskReddit post + its top 3 comments into a captioned vertical video and
uploads it. See [PRD.md](PRD.md) for the quality roadmap and requirement IDs,
and [TECH_DEBT.md](TECH_DEBT.md) for the code-health check-in log.

## Picking this up (new session / new contributor)

Read in this order — it's ~5 minutes and avoids re-deriving decisions:

1. **`PRD.md` §0 "Delivery plan"** — the single source of truth for what's
   shipped, what's next, and the experiment backlog with its pre-committed
   decision rules. **Update it whenever anything ships.**
2. **This README's "How it works"** (below) — the actual pipeline.
3. **`PRD.md` §4 Findings** — only if the task touches metrics or experiments.
   Several plausible-sounding ideas were killed by data recorded there; skipping
   it risks reviving one.
4. **`TECH_DEBT.md`** — only for code-health work.

Standing conventions, non-negotiable:
- Feature work goes on a branch; `main` runs live twice daily (see below).
- Don't start building a phase/feature until the owner explicitly says go.
- Answer performance questions with `scripts/report.py`, never ad-hoc analysis
  (see "Answering 'did X work?'").
- Never credit AI tooling in code, commits, or anything published.

## How it works

`python -m src.run` (entry point, run by
[.github/workflows/run-reddit-video.yml](.github/workflows/run-reddit-video.yml)):

1. `src/content.py` — walk today's top AskReddit posts, applying the basic
   filters (NSFW, profanity, emoji, >90-char titles, yesterday's repeat), and
   gather a pool of ~8 eligible comments per candidate.
2. `src/screen.py` — **suppression-risk screen** (PRD R4.6). One Gemini call
   per candidate decides: skip the post, drop individual risky answers (the
   pool backfills), or pass. Three uploads have been silently zeroed by
   YouTube "limited distribution"; this avoids publishing that shape of
   content. Fails open — an API error never blocks an upload. The same call
   also classifies the post's topic, logged for performance tracking.
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

## Dry runs (never touch the channel)

```sh
DRY_RUN=1 python -m src.run
```

Renders everything to `assets/gen/` and prints the would-be metadata, but
skips upload, thumbnail, and all state mutations. In GitHub: *Actions → Run
workflow → dry_run: true* — the rendered video is attached as a workflow
artifact for review.

## Development workflow (standing convention)

**`main` is the deployment branch — the video workflow runs from it twice
daily, so `main` must always be in a runnable state.** Because of that:

- **Do feature work on a branch**, not on `main`. Any change beyond a trivial
  one-liner (a new requirement, a multi-file change, anything touching the
  upload path) goes on a `feature/<short-name>` branch. Half-finished code must
  never sit on `main`, or the next scheduled run executes it.
- **Merge to `main` only after the rollout gate passes:** dry-run artifact →
  owner reviews the sample → approve → bump `FORMAT_VERSION` → merge → live.
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
report "insufficient data" instead of a misleading median, and zero-view
videos are counted separately as suppression candidates rather than averaged
in. Logic lives in `src/insights.py` and is unit-tested.

```sh
venv/bin/pip install -r requirements-dev.txt && venv/bin/python -m pytest tests/
```

## Versioning & experiments

`FORMAT_VERSION` in `src/config.py` stamps every upload-log row; bump it when
a release goes live. Work splits into **keepers** (high-confidence, batch-shipped,
no per-change bake) and **experiments** (might-revert bets, shipped one variable
at a time with a pre-committed decision rule and a ≥20-upload bake) — see PRD §8.
Judge changes on **watch-seconds**, not avg-%-viewed, and always against an
age-matched cohort (PRD §4); `scripts/report.py` enforces both.
