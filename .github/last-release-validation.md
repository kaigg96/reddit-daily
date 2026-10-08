# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `main`
- **Commit:** `fd0f3f0`
- **When:** 2026-10-08T15:35:02Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/37801792344)

## What the gates said

## Release validation

Budget: at most 8 Gemini requests of the 20/day cap shared with production.

### Gate 1 — merged metadata prompt

- ✅ `title`: Hobbies That Broke the Bank: Are Yours On This List?
- ✅ `keywords`: expensive hobbies, hobbies too expensive, priciest hobbies, photography cost, warhammer pr
- ✅ `cta`: What hobby broke your bank? Share your thoughts below!

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti
ok   want=SKIP got=SKIP drop=[1, 2, 3, 4]|cat=named_wrongdoing        What's a horrible thing that a famous person did that ever
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty?
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho
ok   want=PASS got=PASS                                               Which famous person died in the dumbest way possible?

5/5 as expected
```

- ✅ every case reached the expected verdict via Gemini

### Verdict

**PASS — release gates clear**

- metadata: pass
- screen: pass
