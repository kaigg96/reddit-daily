# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `907d6ad`
- **When:** 2026-10-12T17:53:07Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/38287050983)

## What the gates said

## Release validation

Route: **gemini**. Budget: at most 8 requests (Gemini's 20/day cap is shared with production).

### Gate 1 — merged metadata prompt

- ✅ `title`: What Hobby Will BANKRUPT You?
- ✅ `keywords`: expensive hobbies, hobbies, Reddit hobbies, photography cost, Warhammer cost
- ✅ `cta`: I'm raising my hand for Photography. Those lenses are just too much! What's YOUR vote?
- ✅ host setup: My wallet already trembles at what's coming.
- ✅ host reaction 1: Lenses are a luxury car in disguise!
- ✅ host reaction 2: Plastic crack: the perfect term.

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
