# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `e1-t7-narrated-render`
- **Commit:** `cf45fcc`
- **When:** 2026-11-17T12:13:17Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 16.9 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/44080706464)

What it picked:

```
Narration: stand-in voice
```

## Last request

- **Branch:** `e1-t7-narrated-render`
- **When:** 2026-11-17T12:13:17Z
- **Outcome:** rendered -- see above
