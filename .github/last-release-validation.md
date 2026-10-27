# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `ec2f077`
- **When:** 2026-10-27T14:29:04Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/40521293709)

## What the gates said

…(truncated)…

### Gate 1 — merged metadata prompt

- ✅ `title`: What HOBBY will make YOU broke?
- ✅ `keywords`: expensive hobbies, hobbies that cost too much, reddit expensive hobbies, photography cost,
- ✅ `cta`: I'm raising my hand for skiing: those lift tickets are BRUTAL. Which one gets YOUR vote?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- ✅ host reaction 1: Ouch, that's real
- ✅ host reaction 2: Plastic crack, ha!
- ✅ host reaction 3: So much money
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
