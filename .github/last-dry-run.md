# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `editorial/election-week-skip`
- **Commit:** `5e2772a`
- **When:** 2026-10-31T23:06:26Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 29.3 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/41250932069)

What it picked:

```
Selected post: I unfortunately have to use adult diapers, can others smell them?
Slate topics (rank order): health-body|relationships-dating|humor-absurd|humor-absurd|nostalgia|life-advice
Title style B, caps arm 0: Do you worry people can smell when you wear adult diapers?
CTA: Would you notice? Drop your thoughts in the comments.
Assembled: 29.3s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/Character_Pattern424: I unfortunately have to use adult diapers, can others smell them?
```

## Last request

- **Branch:** `editorial/election-week-skip`
- **When:** 2026-10-31T23:06:26Z
- **Outcome:** rendered -- see above
