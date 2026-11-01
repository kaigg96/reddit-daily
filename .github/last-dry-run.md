# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `editorial/election-week-fallback`
- **Commit:** `88ecde5`
- **When:** 2026-11-01T23:12:04Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 32.3 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/41360710964)

What it picked:

```
Selected post: What’s the nichest thing that you’re probably top 1% in the world at?
Slate topics (rank order): humor-absurd|humor-absurd|hypotheticals|money-work|humor-absurd|dark-morbid
Title style A, caps arm 1: The weirdest things people are actually top ONE percent at
CTA: What is your weirdest top one percent skill? Comment below.
Assembled: 32.3s, bg=pexels_9668945.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Necesito_ir_al_bano: What’s the nichest thing that you’re probably top 1% in the world at?
```

## Last request

- **Branch:** `editorial/election-week-fallback`
- **When:** 2026-11-01T23:12:04Z
- **Outcome:** rendered -- see above
