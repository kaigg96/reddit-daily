# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `reliability/groq-switch`
- **Commit:** `74c81a7`
- **When:** 2026-10-13T10:43:58Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 14.7 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38385064997)

What it picked:

```
Selected post: Introverted guys how did you meet your girlfriend/wife?
Slate topics (rank order): relationships-dating|politics-news|life-advice|health-body
Commentary: a host line ran past its length cap
Title style B, caps arm 1: How did YOU actually find your girlfriend?
Commentary: no usable host lines -- shipping today's reading
CTA: Like, subscribe, and comment your answer below!
Commentary: our own words are 0.000 of the narration
Assembled: 14.7s, bg=pexels_9668945.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Accomplished-Call5: Introverted guys how did you meet your girlfriend/wife?
```

## Last request

- **Branch:** `reliability/groq-switch`
- **When:** 2026-10-13T10:43:58Z
- **Outcome:** rendered -- see above
