# Last release validation

Written by `validate-release.yml`. A shift reads this instead of
needing live Gemini quota to find out whether the gates pass.

- **Branch:** `integration/preview`
- **Commit:** `ec2f077`
- **When:** 2026-10-30T15:04:08Z
- **Verdict:** ✅ PASS — safe to merge

[Full output](https://github.com/kaigg96/reddit-daily/actions/runs/41076840107)

## What the gates said

…(truncated)…
ate 1 — merged metadata prompt

- ✅ `title`: What hobby will ACTUALLY break the bank?
- ✅ `keywords`: expensive hobbies, hobbies cost too much, hobbies to avoid, photography cost, warhammer ex
- ✅ `cta`: I'm raising my hand for skiing: those lift tickets are wild! Which one gets YOUR vote?
- ⚠️ host setup: dropped, past its cap or not a reaction (the rest still ship)
- ✅ host reaction 1: Ouch, lenses
- ✅ host reaction 2: Plastic crack, lol
- ✅ host reaction 3: Two hundred?! No.
- ⚠️ Commentary: past its length cap, a placeholder or emoji, a setup that is not a reaction, or a tag that grades: setup (2 words)
- ⚠️ Commentary setup, as written: "Relatable problem"

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
