# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `debcf72`
- **When:** 2026-11-09T18:46:27Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/42676682808)

## What the gates said

…(truncated)…
`: Hobbies you CANNOT afford anymore
- ✅ `keywords`: expensive hobbies, hobbies ruined by price, cost of skiing, warhammer pricing, photography
- ✅ `cta`: I raise my hand for skiing tickets. Which price tag hurt you the most?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- ✅ host reaction 1: lens cost more
- ✅ host reaction 2: plastic gold
- ✅ host reaction 3: per day price
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (2 words)
- ⚠️ Commentary setup, as written: "wallet killer"

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti [1 req, 22s]
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever [1 req, 3s]
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty? [1 req, 5s]
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho [1 req, 7s]
ok   want=PASS got=PASS                                               Which famous person died in the dumbest way possible? [1 req, 2s]

5 requests sent
5/5 as expected
```

- ✅ every case reached the expected verdict via Gemini

### Verdict

**PASS — release gates clear**

- metadata: pass
- screen: pass
