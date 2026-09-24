# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `feature/v7-open-on-hook`
- **Commit:** `fa8190d`
- **When:** 2026-09-24T14:20:01Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 14.2 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/36011745814)

## Last request

- **Branch:** `feature/v7-open-on-hook`
- **When:** 2026-09-24T14:20:01Z
- **Outcome:** rendered -- see above
