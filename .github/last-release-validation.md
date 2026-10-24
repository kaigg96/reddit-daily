# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `46548ae`
- **When:** 2026-10-22T13:46:28Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/39789632579)

## What the gates said

…(truncated)…
most 8 requests (Gemini's 20/day cap is shared with production).

### Gate 1 — merged metadata prompt

- ✅ `title`: What hobbies will cost YOU a fortune?
- ✅ `keywords`: expensive hobbies, hobbies for rich, costly pastimes, hobbies to avoid, luxury hobbies
- ✅ `cta`: I raise my hand for skiing. Two hundred dollars for a lift ticket is just wild. Which one 
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- ✅ host reaction 1: Ouch, that's steep
- ✅ host reaction 2: Plastic crack, ha!
- ✅ host reaction 3: Daylight robbery!
- ⚠️ Commentary: past its length cap, a placeholder or emoji, or a setup that is not a reaction: setup (2 words)

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
