# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `strategy/own-questions-render`
- **Commit:** `7ef6b78`
- **When:** 2026-11-10T18:46:37Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 19.1 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/42878212014)

Failed soft (the video still passed):

```
Slate topics (rank order): (not collected)
```

What it picked:

```
Selected post: How should people spend a completely free Saturday?
Slate topics (rank order): (not collected)
Title style C, caps arm 0: 3 takes on how to spend a free Saturday
CTA: Which take is yours? Drop your Saturday plan in the comments.
Assembled: 19.1s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
```

## Last request

- **Branch:** `strategy/own-questions-render`
- **When:** 2026-11-10T18:46:37Z
- **Outcome:** rendered -- see above
