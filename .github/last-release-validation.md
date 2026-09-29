# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `main`
- **Commit:** `ab7d628`
- **When:** 2026-09-29T14:51:10Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/36585635282)

## What the gates said

## Release validation

Budget: at most 8 Gemini requests of the 20/day cap shared with production.

### Gate 1 — merged metadata prompt

- ✅ `title`: Hobbies That Broke the Bank: Is Yours on This List?
- ✅ `keywords`: expensive hobbies, hobbies too expensive, reddit expensive hobbies, photography cost, warh
- ✅ `cta`: Which hobby broke YOUR bank? Tell us in the comments!

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever
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
