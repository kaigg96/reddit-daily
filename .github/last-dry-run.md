# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/e1-t4-show-slots`
- **Commit:** `c1bab69`
- **When:** 2026-11-18T11:49:43Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 32.1 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/44297376984)

What it picked:

```
Selected post: When have you seen the statement “every accusation is a confession” actually happen?
Slate topics (rank order): politics-news|relationships-dating|dark-morbid|humor-absurd|health-body|fame-celebrity|nostalgia
Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
Commentary setup, as written: "Seen this daily."
Commentary: dropped only the line(s) named above
Title style B, caps arm 0: Have you caught someone accusing you of their own secret?
Commentary setup: (dropped)
CTA: My hand goes to the food stealing dog for pure audacity. Which one got your vote?
Narration: stand-in voice (Kokoro), not Polly
Commentary: our own words are 0.172 of the narration, 1 host line(s) shown
Assembled: 32.1s, bg=pexels_9668945.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/InstancePale9207: When have you seen the statement “every accusation is a confession” actually happen?
```

## Last request

- **Branch:** `product/e1-t4-show-slots`
- **When:** 2026-11-18T11:49:43Z
- **Outcome:** rendered -- see above
