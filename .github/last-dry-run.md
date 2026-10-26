# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `reliability/shock-title-guard`
- **Commit:** `9103351`
- **When:** 2026-10-26T23:13:41Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 23.0 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/40417916937)

What it picked:

```
Selected post: What’s the worst cheating story you’ve ever heard?
Slate topics (rank order): relationships-dating|nostalgia|other|other
Title style A, caps arm 1: The most brutal betrayal stories EVER told on Reddit
CTA: What is the worst cheating story you have ever heard?
Assembled: 23.0s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Homunculus_316: What’s the worst cheating story you’ve ever heard?
```

## Last request

- **Branch:** `reliability/shock-title-guard`
- **When:** 2026-10-26T23:13:41Z
- **Outcome:** rendered -- see above
