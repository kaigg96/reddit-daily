# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `main`
- **Commit:** `0ee18e71`
- **When:** 2026-11-20T16:59:27Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/44778284839)

## What the gates said

…(truncated)…
data prompt

- ✅ `title`: Which hobbies are REALLY pricing everyone out?
- ✅ `keywords`: expensive hobbies, hobbies too expensive, cost of skiing, warhammer cost, photography budg
- ✅ `cta`: Skiing gets my vote for those insane day rates. Which one broke your bank?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- host reactions: off (the setup and the vote are the host)
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
- ⚠️ Commentary setup, as written: "My wallet hurts"

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti [1 req, 25s]
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever [1 req, 46s]
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty? [1 req, 3s]
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho [1 req, 18s]
ok   want=PASS got=PASS                                               Which famous person died in the dumbest way possible? [1 req, 10s]

5 requests sent
5/5 as expected
```

- ✅ every case reached the expected verdict via Gemini

### Verdict

**PASS — release gates clear**

- metadata: pass
- screen: pass
