# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `b74fc92`
- **When:** 2026-11-16T18:33:06Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/43929206688)

## What the gates said

…(truncated)…
metadata prompt

- ✅ `title`: Which hobby pricing is TRULY broken now?
- ✅ `keywords`: expensive hobbies, hobbies priced out, cost of skiing, warhammer expensive, photography le
- ✅ `cta`: I raise my hand for skiing tickets. Which over-priced hobby gets your vote?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- host reactions: off (the setup and the vote are the host)
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (3 words)
- ⚠️ Commentary setup, as written: "My wallet hurts"

### Gate 2 — R4.6 screen replay

```
ok   want=PASS got=PASS                                               ER workers, what stories do you have involving chiropracti [1 req, 26s]
ok   want=SKIP got=SKIP cat=named_wrongdoing                          What's a horrible thing that a famous person did that ever [2 req, 69s]
ok   want=SKIP got=SKIP cat=sexual_suggestive                         What's something innocent that feels dangerously flirty? [1 req, 53s]
ok   want=PASS got=PASS                                               What was one name mentioned in The Epstein Files which sho [1 req, 10s]
ok   want=PASS got=PASS                                               Which famous person died in the dumbest way possible? [1 req, 27s]

6 requests sent
5/5 as expected
```

- ✅ every case reached the expected verdict via Gemini

### Verdict

**PASS — release gates clear**

- metadata: pass
- screen: pass
