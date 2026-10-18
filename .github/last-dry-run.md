# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `reliability/meta-fallback-model`
- **Commit:** `ac6bfa0`
- **When:** 2026-10-18T21:41:33Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 24.1 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/39168734520)

What it picked:

```
Selected post: What is the worst thing a guest has ever done in your home?
Slate topics (rank order): life-advice|dark-morbid|life-advice|money-work|life-advice|life-advice|nostalgia|humor-absurd
Title style B, caps arm 1: What would YOU do if a guest did this in your house?
CTA: What is the worst thing a guest did to you?
Assembled: 24.1s, bg=pexels_7565898.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Old-Enthusiasm-4943: What is the worst thing a guest has ever done in your home?
```

## Last request

- **Branch:** `reliability/meta-fallback-model`
- **When:** 2026-10-18T21:41:33Z
- **Outcome:** rendered -- see above
