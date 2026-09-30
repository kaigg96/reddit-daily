# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `chore/requests-2.33`
- **Commit:** `513490e`
- **When:** 2026-09-30T12:51:33Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 22.5 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/36717253313)

What it picked:

```
Selected post: What's an obsure item you own that you're sure 99.99% of the population does not have?
Slate topics (rank order): nostalgia|politics-news|life-advice|dark-morbid|other
Title style A: Items Only One Person On Earth Owns
Today's top AskReddit post: What's an obsure item you own that you're sure 99.99% of the population does not have?
```

## Last request

- **Branch:** `chore/requests-2.33`
- **When:** 2026-09-30T12:51:33Z
- **Outcome:** rendered -- see above
