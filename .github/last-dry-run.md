# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/stand-in-voice`
- **Commit:** `bc97bf2`
- **When:** 2026-10-22T08:56:07Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 18.4 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/39751048212)

What it picked:

```
Selected post: Can I legally start my will with 'alright fuckers'?
Slate topics (rank order): humor-absurd|relationships-dating|life-advice|health-body|life-advice|humor-absurd
Commentary: past its length cap, a placeholder or emoji, or a setup that is not a reaction: setup (2 words), vote (25 words)
Commentary: dropped only the line(s) named above
Title style B, caps arm 1: Can YOU legally start your will with an insult?
Commentary setup: (dropped)
Commentary reaction 1: Doubtful
Commentary reaction 2: Extreme
Commentary reaction 3: Bulletproof
CTA: Like, subscribe, and comment your answer below!
Commentary: our own words are 0.098 of the narration, 3 host line(s) shown
Assembled: 18.4s, bg=pexels_15022349.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/WinterIsOnReddit: Can I legally start my will with 'alright fuckers'?
```

## Last request

- **Branch:** `product/stand-in-voice`
- **When:** 2026-10-22T08:56:07Z
- **Outcome:** rendered -- see above
