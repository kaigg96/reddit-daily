# Dry runs

Written by `dry-run.yml`. A shift cannot render a video itself, so it queues
`scripts/dry_run.py request <branch>` and reads the result here. Merge only on
a PASS that names the branch's current commit.

## Last render

- **Branch:** `engineering/groq-route`
- **Commit:** `fe2f3eb`
- **When:** 2026-10-08T23:54:55Z
- **Verdict:** ✅ PASS -- playable: 1080x1920, 30 fps, 28.0 s, audio, no dead air

[Sample video and full output](https://github.com/kaigg96/reddit-daily/actions/runs/37861643212)

Failed soft (the video still passed):

```
Gemini metadata failed with HTTPError (title, keywords and CTA all fall back)
Title generation failed — shipping the Reddit question and logging no style (it was never applied)
```

What it picked:

```
Selected post: Who is your favorite example of positive masculinity?
Slate topics (rank order): life-advice|money-work|money-work|nostalgia|dark-morbid|humor-absurd|relationships-dating
Title style -: Who is your favorite example of positive masculinity?
Today's top AskReddit post, asked by u/make_me_already: Who is your favorite example of positive masculinity?
```

## Last request

- **Branch:** `engineering/groq-route`
- **When:** 2026-10-08T23:54:55Z
- **Outcome:** rendered -- see above
