# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `integration/preview`
- **Commit:** `ec2f077`
- **When:** 2026-10-25T08:31:06Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 30.3 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/40176650537)

What it picked:

```
Selected post: Daycare workers, what do you see parents doing that makes you shake your head?
Slate topics (rank order): life-advice|life-advice|politics-news|nostalgia|dark-morbid
Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
Commentary setup, as written: "My money's on..."
Commentary: dropped only the line(s) named above
Title style B, caps arm 1: Daycare fails: Which one are YOU?
Commentary setup: (dropped)
Commentary reaction 1: Oof
Commentary reaction 2: No way
Commentary reaction 3: Uh oh
CTA: I'm raising my hand for 'unfiltered media access'. What about you?
Commentary: our own words are 0.174 of the narration, 4 host line(s) shown
Assembled: 30.3s, bg=pexels_15168364.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Positive-Run-2411: Daycare workers, what do you see parents doing that makes you shake your head?
```

## Last request

- **Branch:** `integration/preview`
- **When:** 2026-10-25T08:31:06Z
- **Outcome:** rendered -- see above
