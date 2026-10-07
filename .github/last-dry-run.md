# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/house-vote-dormant`
- **Commit:** `1db94a3`
- **When:** 2026-10-07T23:40:26Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 30.8 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37703273999)

What it picked:

```
Selected post: How do so many people do early mornings?
Slate topics (rank order): health-body|relationships-dating|other|money-work|politics-news
Title style B: How do you actually survive early mornings?
Today's top NoStupidQuestions post, asked by u/TrueSkonger: How do so many people do early mornings?
```

## Last request

- **Branch:** `product/house-vote-dormant`
- **When:** 2026-10-07T23:40:26Z
- **Outcome:** rendered -- see above
