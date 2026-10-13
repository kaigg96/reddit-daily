# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `8a91c4c`
- **When:** 2026-10-13T15:57:14Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/38426231894)

## What the gates said

## Release validation

Route: **gemini**. Budget: at most 8 requests (Gemini's 20/day cap is shared with production).

### Gate 1 — merged metadata prompt

- ✅ `title`: What Hobby Will COST YOU Everything?
- ✅ `keywords`: expensive hobbies, hobbies, photography, Warhammer, costly pastimes
- ✅ `cta`: Photography gets my hand up. Those cameras are a financial black hole. What's YOUR vote?
- ✅ host setup: My wallet fears this question every single day.
- ✅ host reaction 1: Those lenses do look like serious investments!
- ✅ host reaction 2: Plastic crack? That sounds disturbingly accurate.

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
