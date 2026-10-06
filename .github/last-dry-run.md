# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `main`
- **Commit:** `9a26ba0`
- **When:** 2026-10-05T22:51:11Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 23.2 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37384811887)

What it picked:

```
Selected post: What 'cheat code' for life do you wish you'd discovered earlier?
Slate topics (rank order): life-advice|hypotheticals|other|life-advice|humor-absurd|relationships-dating|hypotheticals
Title style C: 3 Real Life Cheat Codes You Wish You Knew Sooner
Today's top AskReddit post: What 'cheat code' for life do you wish you'd discovered earlier?
```

## Last request

- **Branch:** `main`
- **When:** 2026-10-05T22:51:11Z
- **Outcome:** rendered -- see above
