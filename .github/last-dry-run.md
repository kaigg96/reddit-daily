# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/text-host`
- **Commit:** `66ccebb`
- **When:** 2026-10-11T10:48:45Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 16.8 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38133147926)

What it picked:

```
Selected post: What is a job that makes the person instantly 10 times hotter?
Slate topics (rank order): money-work|fame-celebrity|nostalgia|life-advice|health-body
Title style C, caps arm 0: 2 jobs that instantly make you more attractive
Commentary setup: looking past the paycheck to find real charm.
Commentary reaction 1: the bar for excitement is surprisingly low.
Commentary reaction 2: bare minimum effort getting way too much credit.
CTA: raising my hand for employed because stability is the ultimate flex. which one gets your vote?
Commentary: our own words are 0.673 of the narration
Assembled: 16.8s, bg=pexels_12488544.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/doublethebass: What is a job that makes the person instantly 10 times hotter?
```

## Last request

- **Branch:** `product/text-host`
- **When:** 2026-10-11T10:48:45Z
- **Outcome:** rendered -- see above
