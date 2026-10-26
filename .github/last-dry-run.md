# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `strategy/own-questions-sample`
- **Commit:** `b2dd123`
- **When:** 2026-10-26T09:57:27Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 18.8 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/40303172511)

Failed soft (the video still passed):

```
Slate topics (rank order): (not collected)
```

What it picked:

```
Selected post: What's the best way to relax after a long day?
Slate topics (rank order): (not collected)
Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (2 words)
Commentary setup, as written: "Tricky question"
Commentary: dropped only the line(s) named above
Title style A, caps arm 1: Unwind After a Long Day: The BEST Way YOU haven't tried?
Commentary setup: Three takes. All mine.
Commentary reaction 1: (dropped)
Commentary reaction 2: (dropped)
Commentary reaction 3: (dropped)
CTA: I'm raising my hand for reading a book to escape into a different world. Which one gets YOUR vote?
Commentary: our own words are 0.388 of the narration, 2 host line(s) shown
Assembled: 18.8s, bg=pexels_12488544.mp4, music=funk_bg_lower.mp3
Today's top  post: What's the best way to relax after a long day?
```

## Last request

- **Branch:** `strategy/own-questions-sample`
- **When:** 2026-10-26T09:57:27Z
- **Outcome:** rendered -- see above
