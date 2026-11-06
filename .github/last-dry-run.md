# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/cta-sentence-case`
- **Commit:** `7225d18`
- **When:** 2026-11-04T19:27:24Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 26.9 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/41896592041)

What it picked:

```
Selected post: What happens to Elon musk now that blue won?
Slate topics (rank order): politics-news|politics-news|politics-news
Title style C, caps arm 1: 3 Reddit answers on what happens to Elon now that Democrats REIGN
CTA: What do you think happens to Elon now? Comment below.
Assembled: 26.9s, bg=pexels_7565898.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/Many_Difficulty_490: What happens to Elon musk now that blue won?
```

## Last request

- **Branch:** `product/cta-sentence-case`
- **When:** 2026-11-04T19:27:24Z
- **Outcome:** rendered -- see above
