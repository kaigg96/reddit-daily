# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `editorial/election-week-polls`
- **Commit:** `92948f7`
- **When:** 2026-11-01T11:09:49Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 28.6 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/41300378457)

What it picked:

```
Selected post: When some men say they don’t like makeup , what does that mean exactly?
Slate topics (rank order): relationships-dating|nostalgia|humor-absurd|life-advice|other|relationships-dating
Title style A, caps arm 0: What men actually mean when they say they hate makeup
CTA: What do you think they really mean? Let me know below.
Assembled: 28.6s, bg=pexels_9668945.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/BiIIie-Eyelash: When some men say they don’t like makeup , what does that mean exactly?
```

## Last request

- **Branch:** `editorial/election-week-polls`
- **When:** 2026-11-01T11:09:49Z
- **Outcome:** rendered -- see above
