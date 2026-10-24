# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `reliability/profanity-quotes`
- **Commit:** `58e0b2b`
- **When:** 2026-10-24T14:39:32Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 27.3 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/40103205395)

What it picked:

```
Selected post: What costume are you expecting to see 50 times this Halloween?
Slate topics (rank order): nostalgia|politics-news|nostalgia|money-work|nostalgia|fame-celebrity|other|health-body
Title style B, caps arm 0: Which tired costume are you seeing everywhere this year?
CTA: Which costume are you sick of seeing? Drop yours below.
Assembled: 27.3s, bg=pexels_15168364.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/iowoman8583: What costume are you expecting to see 50 times this Halloween?
```

## Last request

- **Branch:** `reliability/profanity-quotes`
- **When:** 2026-10-24T14:39:32Z
- **Outcome:** rendered -- see above
