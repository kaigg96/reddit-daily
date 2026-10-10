# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `release/commentary-v8`
- **Commit:** `8dd8577`
- **When:** 2026-10-10T22:46:51Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 29.5 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38092495305)

What it picked:

```
Selected post: How would you feel if the next U.S. president withdrew all support for Israel?
Slate topics (rank order): politics-news|humor-absurd|relationships-dating|money-work|other
Title style B, caps arm 1: How would YOU feel about ending Israel support?
Today's top AskReddit post, asked by u/romalis07: How would you feel if the next U.S. president withdrew all support for Israel?
```

## Last request

- **Branch:** `release/commentary-v8`
- **When:** 2026-10-10T22:46:51Z
- **Outcome:** rendered -- see above
