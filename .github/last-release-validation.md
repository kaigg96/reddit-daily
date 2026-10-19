# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `0ddaae9`
- **When:** 2026-10-19T15:44:44Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/39279020815)

## What the gates said

…(truncated)…
Release validation

Route: **gemini**. Budget: at most 8 requests (Gemini's 20/day cap is shared with production).

### Gate 1 — merged metadata prompt

- ✅ `title`: What HOBBIES are costing YOU too much?
- ✅ `keywords`: expensive hobbies, costly pastimes, hobbies to avoid, photography cost, warhammer price
- ✅ `cta`: I'm raising my hand for 'Photography' – that gear adds up! Which one gets your vote?
- ✅ host setup: My wallet is already crying just thinking about it.
- ✅ host reaction 1: Those lenses are no joke, seriously pricey.
- ✅ host reaction 2: The 'plastic crack' truly hits different.
- ✅ host reaction 3: My knees hurt just looking at that lift ticket.

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
