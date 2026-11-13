# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `b1190de`
- **When:** 2026-11-13T16:20:50Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/43461256406)

## What the gates said

…(truncated)…
adata prompt

- ✅ `title`: Hobbies you CANNOT afford anymore
- ✅ `keywords`: expensive hobbies, hobbies ruined by money, cost of skiing, warhammer pricing, photography
- ✅ `cta`: I am raising my hand for skiing because two hundred a day is wild. Which gets your vote?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- host reactions: off (the setup and the vote are the host)
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
- ⚠️ Commentary setup, as written: "My wallet hurts"

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS drop=[1, 3]|cat=unsafe_comments               ER workers, what stories do you have involving chiropracti [2 req, 66s]
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever [1 req, 3s]
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty? [1 req, 3s]
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho [1 req, 3s]
ok   want=PASS got=PASS                                               Which famous person died in the dumbest way possible? [1 req, 15s]

6 requests sent
5/5 as expected
```

- ✅ every case reached the expected verdict via Gemini

### Verdict

**PASS — release gates clear**

- metadata: pass
- screen: pass
