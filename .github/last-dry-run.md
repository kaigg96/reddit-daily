# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/host-line-fallback`
- **Commit:** `0fbc37c`
- **When:** 2026-10-13T23:21:55Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 28.8 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38483439606)

What it picked:

```
Selected post: My close friends are becoming obsessed with discourse about "hypergamy"
Slate topics (rank order): relationships-dating
Title style B, caps arm 0: are your friends losing their minds to algorithm brainrot?
Commentary setup: watching a buddy vanish into an endless internet rabbit hole.
Commentary reaction 1: impossible to pull someone back once the feed takes over.
Commentary reaction 2: every hang turns into the exact same broken record.
CTA: raising my hand for the sad reality of algorithms ruining chats. which one gets your vote?
Commentary: our own words are 0.439 of the narration, 4 host line(s) shown
Assembled: 28.8s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
Today's top NoStupidQuestions post, asked by u/Unable-Barber1511: My close friends are becoming obsessed with discourse about "hypergamy"
```

## Last request

- **Branch:** `product/host-line-fallback`
- **When:** 2026-10-13T23:21:55Z
- **Outcome:** rendered -- see above
