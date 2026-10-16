# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/host-three-answers`
- **Commit:** `b9bc23b`
- **When:** 2026-10-16T22:12:31Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 29.7 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38973971633)

What it picked:

```
Selected post: What job used to be considered the dream career, but is basically a nightmare now?
Slate topics (rank order): money-work|nostalgia|money-work|money-work|money-work|relationships-dating
Commentary: a host line ran past its length cap, or was a placeholder or emoji
Commentary: dropped only the long line(s)
Title style B, caps arm 0: Which of your dream jobs turned into a complete nightmare?
Commentary setup: Growing up, these fields promised the absolute world.
Commentary reaction 1: Eighty hours for a pink slip at the finish line.
Commentary reaction 2: Sending ten thousand applications just to hear crickets.
Commentary reaction 3: Watching the entire foundation of education crumble hurts.
CTA: Like, subscribe, and comment your answer below!
Commentary: our own words are 0.347 of the narration, 4 host line(s) shown
Assembled: 29.7s, bg=pexels_15168364.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/sexy-maud: What job used to be considered the dream career, but is basically a nightmare now?
```

## Last request

- **Branch:** `product/host-three-answers`
- **When:** 2026-10-16T22:12:31Z
- **Outcome:** rendered -- see above
