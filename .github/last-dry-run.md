# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `integration/preview`
- **Commit:** `b1190de`
- **When:** 2026-11-13T11:04:51Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 24.5 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/43413615851)

What it picked:

```
Commentary: skipping a medical thread (topic) — After giving birth, can women feel that their body suddenly 
Selected post: What’s it like inside of Microsoft right now?
Slate topics (rank order): health-body|money-work|politics-news|dark-morbid|money-work
Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
Commentary setup, as written: "Pure chaos inside"
Commentary: dropped only the line(s) named above
Title style A, caps arm 1: What is REALLY happening inside Microsoft?
Commentary setup: (dropped)
CTA: I raise my hand for the suffering SREs. Which answer gets your vote?
Commentary: our own words are 0.201 of the narration, 1 host line(s) shown
Assembled: 24.5s, bg=pexels_15022349.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/SttSr: What’s it like inside of Microsoft right now?
```

## Last request

- **Branch:** `integration/preview`
- **When:** 2026-11-13T11:04:51Z
- **Outcome:** rendered -- see above
