# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/stand-in-voice`
- **Commit:** `9cd1022`
- **When:** 2026-10-23T22:16:54Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 29.9 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/40032165271)

What it picked:

```
Selected post: Why does my obese friend act like this?
Slate topics (rank order): health-body|nostalgia|politics-news|politics-news|other|other
Commentary: past its length cap, a placeholder or emoji, or a setup that is not a reaction: setup (2 words)
Commentary: dropped only the line(s) named above
Title style C, caps arm 1: 3 Answers That REALLY Nail It for Your Obese Friend
Commentary setup: (dropped)
Commentary reaction 1: Direct hit
Commentary reaction 2: Spot on
Commentary reaction 3: Deep insight
CTA: I'm raising my hand for 'She's projecting her insecurities onto you.' It explains SO much. Which one gets YOUR vote?
Commentary: our own words are 0.352 of the narration, 4 host line(s) shown
Assembled: 29.9s, bg=pexels_15168364.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/OkMedia1290: Why does my obese friend act like this?
```

## Last request

- **Branch:** `product/stand-in-voice`
- **When:** 2026-10-23T22:16:54Z
- **Outcome:** rendered -- see above
