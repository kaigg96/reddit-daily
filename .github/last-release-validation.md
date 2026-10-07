# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `main`
- **Commit:** `c637fd6`
- **When:** 2026-10-07T15:33:43Z
- **Verdict:** ⚠️ INCONCLUSIVE — gates could not be exercised; not a failure

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/37644685401)

## What the gates said

## Release validation

Budget: at most 8 Gemini requests of the 20/day cap shared with production.

### Gate 1 — merged metadata prompt

- ✅ `title`: These Hobbies WILL Bankrupt You!
- ✅ `keywords`: expensive hobbies, hobbies too expensive, hobbies to avoid, costly hobbies, affordable hob
- ✅ `cta`: What hobby broke YOUR bank? Let us know below!

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty?
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho
Screen: Gemini failed (http_429) — using keyword backstop
??   want=PASS got=PASS                                               Which famous person died in the dumbest way possible?

4/4 as expected (1 inconclusive — fell through to the backstop)
```

- ⚠️ INCONCLUSIVE — a case fell through to the keyword backstop, so the screen was not actually exercised. Gemini was unreachable or the day's quota was spent. Not a verdict either way; the next scheduled run re-checks it.

### Verdict

**INCONCLUSIVE — could not be checked, not a failure**

- metadata: pass
- screen: inconclusive
