# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `reliability/model-successor`
- **Commit:** `eec1071`
- **When:** 2026-11-07T17:14:49Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 18.6 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/42395157981)

What it picked:

```
Selected post: Which popular brand has died that people barely remember?
Slate topics (rank order): nostalgia|money-work|relationships-dating|humor-absurd|relationships-dating
Title style A, caps arm 1: Dead brands everyone FORGOT existed
CTA: What dead brand do you miss the most? Let me know.
Assembled: 18.6s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/ReyisME: Which popular brand has died that people barely remember?
```

## Last request

- **Branch:** `reliability/model-successor`
- **When:** 2026-11-07T17:14:49Z
- **Outcome:** rendered -- see above
