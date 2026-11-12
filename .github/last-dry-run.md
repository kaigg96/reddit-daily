# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `strategy/own-questions-fixes`
- **Commit:** `c667d44`
- **When:** 2026-11-12T11:15:05Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 26.9 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/43206873847)

What it picked:

```
Selected post: What's the adult version of finding out Santa doesn't exist?
Slate topics (rank order): nostalgia|relationships-dating|other|life-advice|other
Title style B, caps arm 1: Which one hit YOU hardest?
CTA: What is your version? Drop it in the comments.
Assembled: 26.9s, bg=pexels_12488544.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Geno-64: What's the adult version of finding out Santa doesn't exist?
```

## Last request

- **Branch:** `strategy/own-questions-fixes`
- **When:** 2026-11-12T11:15:05Z
- **Outcome:** rendered -- see above
