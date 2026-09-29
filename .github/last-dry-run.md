# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `feature/r4.1-subreddit-rotation`
- **Commit:** `7cb9924`
- **When:** 2026-09-27T14:50:32Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 18.2 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/36327216645)

## Last request

- **Branch:** `feature/r4.1-subreddit-rotation`
- **When:** 2026-09-27T14:50:32Z
- **Outcome:** rendered -- see above
