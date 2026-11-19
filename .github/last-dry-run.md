# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `e1-t5-switch-on-render`
- **Commit:** `3311579`
- **When:** 2026-11-19T11:46:20Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 21.1 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/44517244985)

Failed soft (the video still passed):

```
Slate topics (rank order): (not collected)
```

What it picked:

```
Selected post: How long should you wait before texting someone back?
Slate topics (rank order): (not collected)
Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
Commentary setup, as written: "Depends on who"
Commentary: dropped only the line(s) named above
Title style A, caps arm 1: How long should YOU wait to text back?
Commentary setup: (dropped)
CTA: I raise my hand for no games and instant replies. Which option gets your vote?
Narration: stand-in voice (Kokoro), not Polly
Commentary: our own words are 0.270 of the narration, 1 host line(s) shown
Assembled: 21.1s, bg=pexels_7565898.mp4, music=freepd_city_sunshine.mp3
```

## Last request

- **Branch:** `e1-t5-switch-on-render`
- **When:** 2026-11-19T11:46:20Z
- **Outcome:** rendered -- see above
