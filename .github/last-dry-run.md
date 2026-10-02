# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `feature/title-style-b-weight`
- **Commit:** `73996ef`
- **When:** 2026-10-02T16:02:14Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 28.4 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37030728531)

What it picked:

```
Selected post: What happened to the friend you thought you'd have for the rest of your life?
Slate topics (rank order): relationships-dating|relationships-dating|other|nostalgia|dark-morbid|relationships-dating|humor-absurd
Title style A: Where did your lifelong best friend go?
Today's top AskReddit post: What happened to the friend you thought you'd have for the rest of your life?
```

## Last request

- **Branch:** `feature/title-style-b-weight`
- **When:** 2026-10-02T16:02:14Z
- **Outcome:** rendered -- see above
