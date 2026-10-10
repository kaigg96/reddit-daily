# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `release/caps-and-screen-fix`
- **Commit:** `844f993`
- **When:** 2026-10-10T09:56:11Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 38.2 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38042915493)

What it picked:

```
Selected post: If my car dies in the middle of a busy highway, can I call 911?
Slate topics (rank order): life-advice|sex-adjacent|relationships-dating
Title style B, caps arm 0: What would you do if your car died on a busy highway?
Today's top NoStupidQuestions post, asked by u/RaineRisin: If my car dies in the middle of a busy highway, can I call 911?
```

## Last request

- **Branch:** `release/caps-and-screen-fix`
- **When:** 2026-10-10T09:56:11Z
- **Outcome:** rendered -- see above
