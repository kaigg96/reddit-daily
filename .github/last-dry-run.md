# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `feature/r4.1-subreddit-rotation`
- **Commit:** `07486c8`
- **When:** 2026-10-06T10:54:32Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 28.9 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37452567193)

What it picked:

```
Selected post: Why do people forget about how bad the 70s actually were?
Slate topics (rank order): nostalgia|relationships-dating|fame-celebrity|other|money-work|politics-news|sex-adjacent
Title style B: Why do you forget how bad the 70s really were?
Today's top NoStupidQuestions post: Why do people forget about how bad the 70s actually were?
```

## Last request

- **Branch:** `feature/r4.1-subreddit-rotation`
- **When:** 2026-10-06T10:54:32Z
- **Outcome:** rendered -- see above
