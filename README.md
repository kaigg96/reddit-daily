# reddit-daily

Automated YouTube Shorts channel: twice a day, a GitHub Action turns the top
r/AskReddit post + its top 3 comments into a captioned vertical video and
uploads it. See [PRD.md](PRD.md) for the quality roadmap and requirement IDs.

## How it works

`python -m src.run` (entry point, run by
[.github/workflows/run-reddit-video.yml](.github/workflows/run-reddit-video.yml)):

1. `src/content.py` — pick today's top AskReddit post (filters: NSFW,
   profanity, emoji, >90-char titles, yesterday's repeat) + 3 clean comments.
2. `src/llm.py` — Gemini generates SEO keywords and a CTR-oriented title
   (fails soft; the video ships either way).
3. `src/tts.py` — AWS Polly narrates every segment (one voice per video) and
   returns **word-level speech marks** that drive the animated captions.
4. `src/video.py` — MoviePy assembles one continuous timeline: no silent gaps,
   karaoke-style captions, animated background (b-roll if present in
   `assets/broll/`, otherwise a procedural drifting-glow background), question
   header + `ANSWER n/3` progress badge, whoosh SFX between answers,
   background music. Renders 1080x1920@30 + a thumbnail card.
5. `src/youtube.py` — upload video + thumbnail.
6. On success: `prev_post.txt` (dedupe) and `upload_log.csv` (experiment log,
   one row per upload — join against YouTube Analytics on `video_id`) are
   committed back by the workflow.

## Dry runs (never touch the channel)

```sh
DRY_RUN=1 python -m src.run
```

Renders everything to `assets/gen/` and prints the would-be metadata, but
skips upload, thumbnail, and all state mutations. In GitHub: *Actions → Run
workflow → dry_run: true* — the rendered video is attached as a workflow
artifact for review.

## Local setup

```sh
python3.10 -m venv venv && venv/bin/pip install -r requirements.txt
```

Secrets go in `.env` (gitignored): `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`,
`REDDIT_USER_AGENT`, `AWS_POLLY_ACCESS_KEY`, `AWS_POLLY_SECRET_ACCESS_KEY`,
`YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`,
`GEMINI_API_KEY`. The same names exist as Actions secrets in CI.

## One-time setup tasks (owner)

Still open — the pipeline works without them but improves with them:

1. **B-roll library (PRD R1.3).** Download 10–15 vertical motion clips
   (satisfying/abstract/scenic; no logos, people close-ups, or embedded music)
   from Pexels/Pixabay/Mixkit, then for each:
   `venv/bin/python scripts/prep_broll.py <downloaded file> <short_name>` and
   record the source URL in `assets/CREDITS.md`. Until then the procedural
   background is used.
2. **Music variety (PRD R1.6, optional).** The current track
   (`funk_bg_lower.mp3`) is from the YouTube Audio Library and license-clean.
   For per-video variety, drop 2–3 more Audio Library tracks into
   `assets/music/` (rotation is automatic) and list them in
   `assets/CREDITS.md`.
3. **OAuth re-auth (PRD Phase 3 prerequisite — also permanently fixes the
   7-day token expiry).** Detailed walkthrough:

   1. **Publish the OAuth consent screen** (this is why tokens have been
      expiring weekly: "Testing" status caps refresh tokens at 7 days;
      "In production" tokens don't expire while in regular use).
      [console.cloud.google.com](https://console.cloud.google.com) → select
      the project that owns the OAuth client → **APIs & Services → OAuth
      consent screen** (newer console: *Google Auth Platform → Audience*) →
      Publishing status shows *Testing* → click **Publish app** → confirm.
      Do **not** submit for verification — not needed for personal use.
   2. **Mint the new token** (only after step 1, or the 7-day expiry sticks):
      `venv/bin/python regen_refresh_token.py` → a browser tab opens → sign
      in with the **channel's** Google account → on the "Google hasn't
      verified this app" screen click **Advanced → Go to … (unsafe)** →
      approve all three permissions (upload, channel management, analytics)
      → the script prints the refresh token in the terminal.
   3. **Store it**: GitHub repo → Settings → Secrets and variables →
      Actions → `YOUTUBE_REFRESH_TOKEN` → Update → paste. Also replace
      `YOUTUBE_REFRESH_TOKEN` in the local `.env`.
   4. **Verify** (optional, uploads nothing — a read that the old
      upload-only token couldn't do):

      ```sh
      venv/bin/python -c "
      from src.youtube import _authenticate
      from googleapiclient.discovery import build
      yt = build('youtube', 'v3', credentials=_authenticate())
      print('token OK for:', yt.channels().list(mine=True, part='snippet')
            .execute()['items'][0]['snippet']['title'])"
      ```

   After this, the weekly token regeneration is never needed again.

## Versioning & experiments

`FORMAT_VERSION` in `src/config.py` stamps every upload-log row. Bump it only
when a phase goes live, and judge format changes on ≥14 days / ≥20 uploads of
data (PRD §8), never on individual videos.

`create_video.ipynb` is the deprecated pre-v2 pipeline, kept for reference;
CI no longer executes it.
