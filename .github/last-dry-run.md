# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `integration/preview`
- **Commit:** `0ddaae9`
- **When:** 2026-10-19T09:45:01Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 18.0 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/39232065017)

What it picked:

```
Selected post: What jobs do you think will completely disappear in the next 10 years?
Slate topics (rank order): money-work|nostalgia|money-work|health-body|other|other|other|other
Commentary: a host line ran past its length cap, or was a placeholder or emoji
Commentary: dropped only the long line(s)
Title style B, caps arm 0: Will your job still exist in ten years?
Commentary setup: Some of these are coming for us all.
Commentary reaction 1: The robots are finally taking over the phones.
Commentary reaction 2: Shirley better start packing her desk right now.
Commentary reaction 3: Goodbye to whoever is reading my chat prompts.
CTA: Like, subscribe, and comment your answer below!
Commentary: our own words are 0.421 of the narration, 4 host line(s) shown
Assembled: 18.0s, bg=pexels_9668945.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Alice6918: What jobs do you think will completely disappear in the next 10 years?
```

## Last request

- **Branch:** `integration/preview`
- **When:** 2026-10-19T09:45:01Z
- **Outcome:** rendered -- see above
