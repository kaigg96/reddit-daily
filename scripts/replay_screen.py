"""Replay the R4.6 screen over known cases against live Gemini.

The standing weekly audit (PRD R4.6) can change the taxonomy or the prompt.
This is the regression check for that: the confirmed-zeroed shapes must still
skip, and the questions past audits found were wrongly skipped must now pass.
`tests/test_screen.py` covers the tier logic deterministically — this covers
the half that lives in the prompt, which unit tests cannot reach.

    venv/bin/python scripts/replay_screen.py

Comments are synthetic for cases whose originals weren't kept (screen_log.csv
stores only the title), so it validates the QUESTION-level verdict.

Costs one Gemini call per case against the same free-tier quota production
uses. Run it once, not in a loop — a 2026-09-09 replay exhausted the daily
quota, and while the screen fails open, that leaves live runs on the keyword
backstop until the quota resets.
"""
import sys, time
sys.path.insert(0, ".")
from src import config, llm, screen

MED = ["Sudden severe headache that came out of nowhere - that's a red flag.",
       "Unexplained weight loss. People shrug it off and it's often serious.",
       "New confusion in an older person. Everyone blames age.",
       "A mole that changed shape. Get it looked at."]
BAR = ["Guy got cut off, threw a punch, security handled it.",
       "She cried, called her mum, and was in bed by 10.",
       "He argued for twenty minutes then ordered a water.",
       "Regular got cut off, came back next day and apologised."]
ER  = ["Neck adjustment led to a vertebral artery dissection - he was 32.",
       "Most patients are fine honestly, it's a small minority.",
       "Saw one pneumothorax after an aggressive thoracic adjustment.",
       "Mostly people come in with soreness that resolves."]
BED = ["The way they dance says everything.",
       "Confidence in how they carry themselves.",
       "How attentive they are in conversation.",
       "Good rhythm usually tracks."]
FAM = ["A famous director settled a case quietly in the 90s and nobody remembers.",
       "That singer everyone loves did something awful to their first wife.",
       "The actor who hosted the charity gala had a whole hidden history.",
       "Everyone forgot what that talk show host was accused of."]
FLIRT = ["Someone fixing your collar. It's nothing but it's everything.",
         "Sharing a dessert with one spoon.",
         "Being handed a drink they already tasted.",
         "Someone remembering your coffee order."]
EPS = ["Seeing that name on the list genuinely shocked me.",
       "I had to read it twice, I never would have guessed.",
       "Half the list was unsurprising, one name was not.",
       "The reaction online said more than the list did."]
DUMB = ["Died trying to prove a window was unbreakable.",
        "Fell off a cliff taking a photo.",
        "Ate a poisonous fish on a dare.",
        "Tried to outrun a train for a bet."]

# Worded unlike anything in `_PROMPT`, so they test judgement, not memory:
# every case above is also one of its examples. One per side of the line.
SEXY = ["Rolling up their sleeves before fixing something.",
        "A low voice when they're tired.",
        "Being really good with their hands.",
        "Watching someone be calmly competent."]
ANAES = ["He proposed to me, then asked where his wife was.",
         "She was convinced she was a pirate captain.",
         "He apologised to the ceiling for ten minutes.",
         "Told me the secret to perfect pancakes, then fell asleep."]

# The FLIRT case ("...dangerously flirty?") is now also a calibration example
# in `_PROMPT` (src/screen.py, added 2026-09-20 after this exact case missed
# live with reasoning already restored). That makes it a memorization check, not a
# generalization check, from here on — swap in a fresh unseen paraphrase of the
# same sexual_suggestive shape next time quota allows a live re-verify, rather
# than trusting a pass on this one as proof the category generalizes.
CASES = [
    ("PASS", "ER workers, what stories do you have involving chiropractic patients?", ER),
    ("SKIP", "What's a horrible thing that a famous person did that everyone forgot about but you?", FAM),
    ("SKIP", "What's something innocent that feels dangerously flirty?", FLIRT),
    ("PASS", "What was one name mentioned in The Epstein Files which shocked you?", EPS),
    ("PASS", "Which famous person died in the dumbest way possible?", DUMB),
]
# Added only when the route under test is not the one the prompt was tuned on:
# two more requests would put the daily release gate at its 8-request cap.
if config.AI_PROVIDER == "groq":
    CASES += [
        ("SKIP", "What's a completely non-sexual thing that is secretly really sexy?", SEXY),
        ("PASS", "Nurses, what's the weirdest thing a patient said coming out of anaesthesia?", ANAES),
    ]

# Groq switched on without its key would answer every case from Gemini: seven
# requests of Gemini's 20 a day, all inconclusive. Stop before spending them.
if llm.provider() != config.AI_PROVIDER:
    print(f"inconclusive: AI_PROVIDER={config.AI_PROVIDER} but its key is not set; "
          "nothing was sent")
    sys.exit(1)

fails = skipped = 0
for want, q, comments in CASES:
    r = screen.screen(q, comments)
    got = "SKIP" if r.verdict == "skip_post" else "PASS"
    if r.source != config.AI_PROVIDER:
        # The route under test was unreachable, so this case exercised the
        # keyword backstop (or Gemini, for groq with no key), not the prompt
        # on that route. Not a verdict either way.
        ok, skipped = "??  ", skipped + 1
    elif got == want:
        ok = "ok  "
    else:
        ok, fails = "FAIL", fails + 1
    extra = []
    if r.demoted:
        extra.append(f"demoted={r.demoted}")
    if r.unsafe:
        extra.append(f"drop={sorted(i+1 for i in r.unsafe)}")
    if r.category:
        extra.append(f"cat={r.category}")
    print(f"{ok} want={want} got={got:4} {'|'.join(extra):45} {q[:58]}")
    time.sleep(2)
checked = len(CASES) - skipped
print(f"\n{checked - fails}/{checked} as expected"
      + (f" ({skipped} inconclusive — fell through to the backstop)" if skipped else ""))
sys.exit(1 if fails else 0)
