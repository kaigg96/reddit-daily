# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `strategy/own-questions-source`
- **Commit:** `deb4fda`
- **When:** 2026-11-11T11:01:28Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 26.5 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/43008138907)

What it picked:

```
Selected post: Is it strictly prohibited for a therapist to tell your parents?
Slate topics (rank order): life-advice|sex-adjacent|health-body|politics-news|money-work
Title style B, caps arm 1: Can your therapist REALLY tell your parents everything you say?
CTA: Would your therapist tell your parents? Drop your thoughts below.
Assembled: 26.5s, bg=pexels_12488544.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/VerifiedHeroo: Is it strictly prohibited for a therapist to tell your parents?
```

## Last request

- **Branch:** `strategy/own-questions-source`
- **When:** 2026-11-11T11:01:28Z
- **Outcome:** rendered -- see above
