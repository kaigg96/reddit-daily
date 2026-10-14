# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `product/host-line-fallback`
- **Commit:** `79a3873`
- **When:** 2026-10-14T16:07:48Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 16.0 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/38595017637)

What it picked:

```
Selected post: What celebrity doesn't want to realize their 15 minutes is over?
Slate topics (rank order): fame-celebrity|health-body|dark-morbid|dark-morbid|life-advice|humor-absurd|money-work
Title style A, caps arm 0: Celebrities who refuse to let go of the spotlight
Commentary setup: some famous people just do not know when to leave
Commentary reaction 1: trying way too hard to stay relevant these days
Commentary reaction 2: still sprinkling salt like anyone is watching anymore
CTA: salt bae gets my vote for refusing to stop seasoning. who gets yours?
Commentary: our own words are 0.661 of the narration, 4 host line(s) shown
Assembled: 16.0s, bg=pexels_7565434.mp4, music=funk_bg_lower.mp3
Today's top AskReddit post, asked by u/Agitated-Distance740: What celebrity doesn't want to realize their 15 minutes is over?
```

## Last request

- **Branch:** `product/host-line-fallback`
- **When:** 2026-10-14T16:07:48Z
- **Outcome:** rendered -- see above
