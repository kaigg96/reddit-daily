# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `dab9773`
- **When:** 2026-11-11T16:10:25Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/43055243782)

## What the gates said

…(truncated)…
now?
- ✅ `keywords`: expensive hobbies, hobbies priced out, cost of skiing, warhammer expensive, photography le
- ✅ `cta`: I raise my hand for skiing because those lift prices are unreal. Which gets yours?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- ✅ host reaction 1: cheaper than glass
- ✅ host reaction 2: pure plastic addiction
- ✅ host reaction 3: rent a mountain
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
- ⚠️ Commentary setup, as written: "wallet is sweating"

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti [1 req, 2s]
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever [1 req, 2s]
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty? [1 req, 2s]
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho [1 req, 1s]
ok   want=PASS got=PASS                                               Which famous person died in the dumbest way possible? [1 req, 1s]

5 requests sent
5/5 as expected
```

- ✅ every case reached the expected verdict via Gemini

### Verdict

**PASS — release gates clear**

- metadata: pass
- screen: pass
