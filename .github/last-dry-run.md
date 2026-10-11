# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/text-host`
- **Commit:** `907d6ad`
- **When:** 2026-10-11T22:59:45Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 22.5 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38182399279)

What it picked:

```
Selected post: Do airports allow people to stay overnight?
Slate topics (rank order): other
Title style C, caps arm 0: 2 answers on whether you can sleep at airports
Commentary setup: packing a sleeping bag for terminal floor camping tonight.
Commentary reaction 1: terminal seats turn into community beds after midnight.
Commentary reaction 2: hub size dictates your sleeping comfort level.
CTA: raising my hand for yes youll be fine because floor camping builds character. which gets your vote?
Commentary: our own words are 0.548 of the narration
Assembled: 22.5s, bg=pexels_15168364.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/hugtreesmore: Do airports allow people to stay overnight?
```

## Last request

- **Branch:** `product/text-host`
- **When:** 2026-10-11T22:59:45Z
- **Outcome:** rendered -- see above
