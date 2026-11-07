# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `5a44db0`
- **When:** 2026-11-05T16:31:09Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/42064489859)

## What the gates said

…(truncated)…
ate 1 — merged metadata prompt

- ✅ `title`: What hobby will bankrupt YOU?
- ✅ `keywords`: expensive hobbies, hobbies that cost too much, photography cost, warhammer expensive, skii
- ✅ `cta`: I'm raising my hand for 'Skiing' because those lift ticket prices are brutal. Which hobby 
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- ✅ host reaction 1: Ouch, lenses
- ✅ host reaction 2: Plastic crack, indeed
- ✅ host reaction 3: Two hundred dollars?!
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (2 words)
- ⚠️ Commentary setup, as written: "Relatable problem"

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
