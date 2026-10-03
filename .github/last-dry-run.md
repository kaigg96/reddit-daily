# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `feature/r4.1-subreddit-rotation`
- **Commit:** `46508d3`
- **When:** 2026-10-03T14:24:36Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 22.9 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37129315847)

What it picked:

```
Selected post: If you were a billionaire would you pay for your best friend’s first class ticket?
Slate topics (rank order): money-work|relationships-dating|life-advice|health-body|nostalgia
Title style A: Would a billionaire buy their best friend first class?
Today's top NoStupidQuestions post: If you were a billionaire would you pay for your best friend’s first class ticket?
```

## Last request

- **Branch:** `feature/r4.1-subreddit-rotation`
- **When:** 2026-10-03T14:24:36Z
- **Outcome:** rendered -- see above
