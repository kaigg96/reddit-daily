# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `2e26595`
- **When:** 2026-10-18T12:36:55Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/39127928723)

## What the gates said

## Release validation

Route: **gemini**. Budget: at most 8 requests (Gemini's 20/day cap is shared with production).

### Gate 1 — merged metadata prompt

- ✅ `title`: What hobby will cost YOU a fortune?
- ✅ `keywords`: expensive hobbies, hobbies that cost too much, photography expensive, warhammer price, ski
- ✅ `cta`: I'm raising my hand for Warhammer: 'plastic crack' is too accurate! Which one gets your vo
- ✅ host setup: I bet a lot of these used to be affordable.
- ✅ host reaction 1: My wallet just screamed in terror.
- ✅ host reaction 2: Plastic crack is the perfect name!
- ✅ host reaction 3: My knees also can't afford that price tag now.

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
