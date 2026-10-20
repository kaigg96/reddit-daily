"""Read bet 1's host lines (#77) on fixed posts: one metadata request each.

    venv/bin/python scripts/tag_trial.py --model upload --posts 2,4,9
    venv/bin/python scripts/tag_trial.py --model sample        # all nine
    venv/bin/python scripts/tag_trial.py --model groq
    venv/bin/python scripts/tag_trial.py --model upload --posts 2,4,9 --setup blurt
    venv/bin/python scripts/tag_trial.py --model groq --setup specific
    venv/bin/python scripts/tag_trial.py --model groq --groq-model qwen/qwen3.8-27b

The models differ, so read the one that matters: on 2026-10-20 the upload
model reacted to 7 of 9 answers where the sample model and Groq mostly
labelled (PRD §4). Score the output against §4's bar for a tag.

`--model upload` spends the allowance live uploads share (20 a day; a shift
may use 8, after 07:00 UTC and not within an hour of an upload), so it is
capped at UPLOAD_CAP per run, one try each: a 503 is not retried. The sample
model's own allowance is undocumented and is production's fallback, so it is
capped too.

The questions are real (upload_log.csv, October 2026); the answers are
written in Reddit's voice, as scripts/replay_screen.py does, because Reddit
refuses the runner shifts use. 2, 3, 6 and 7 carry answers that are only a
name, which drift to labels; 1 and 5 are politics.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, ".")

POSTS = [
    ("Why are Peter Thiel's Anti-christ lectures secret?",
     ["Because he's charging rich people to hear them and secrecy makes it feel exclusive.",
      "They're not really secret, they were private talks for a Catholic group and some recordings leaked.",
      "Because if normal people heard them they'd realize how unhinged it sounds."]),
    ("What's a high paying but soul crushing career that people romanticize far too much?",
     ["Investment banking.",
      "Big law.",
      "Pharma sales. You're basically a lunch delivery guy who gets yelled at by receptionists."]),
    ("What jobs do you think will completely disappear in the next 10 years?",
     ["Cashiers.",
      "Translators, sadly.",
      "Telemarketers. Nobody will miss them."]),
    ("What is up with the infantilization of 18-21 year olds?",
     ["Nobody can afford to move out, so you're still living in your childhood bedroom at 21.",
      "Colleges started treating students like customers, and customers get coddled.",
      "Every generation says this about the one after it."]),
    ("Best counter-argument to \"Why need privacy if you've got nothing to hide\"",
     ["Then hand me your phone, unlocked.",
      "You don't get to decide what counts as wrong ten years from now.",
      "I close the door when I use the bathroom. Not because I'm doing anything wrong."]),
    ("What movie can you rewatch endlessly without getting bored?",
     ["Memento.",
      "The Princess Bride",
      "Hot Fuzz. Every rewatch I catch a new background joke."]),
    ("What's a company that you're genuinely convinced HATES their customers?",
     ["Ticketmaster.",
      "Comcast. I spent four hours on the phone to cancel and they still billed me.",
      "Spirit Airlines charges you to print your boarding pass at the airport."]),
    ("Who is a celebrity that aged incredibly gracefully without trying to fight it?",
     ["Keanu Reeves",
      "Jamie Lee Curtis. She went grey on purpose and looks amazing.",
      "Morgan Freeman has looked 70 for about forty years now."]),
    ("How do donut shops stay in business?",
     ["Coffee. The donuts get you in the door, the coffee pays the rent.",
      "Most of them are family run and the whole family works there for free.",
      "Cops."]),
]
UPLOAD_CAP = 3
SAMPLE_CAP = len(POSTS)
# The setup's wording on trial (PRD §4, 2026-10-20 afternoon): on both Groq
# models, blind-scored, it reacted on 9 of 16 setups against 0 of 17 for the
# shipped one, but 4 of gpt-oss's 5 opened "Sounds ...". Unread on Gemini.
SETUP_BLURT = (
    '"setup": a tag of 1 to 3 words, shown as the question finishes: the words\n'
    '     you would blurt out the moment a friend asked you this question, before\n'
    '     any answer. React to the question; never name or title it: "Brutal\n'
    '     truth" and "The mystery" are titles, not reactions. It must make sense\n'
    '     to someone who has only just read the question:')
# SETUP_BLURT with the reactions' rule for sameness (#80's spam policy): a
# reaction only this question could get, and a stock opener named as one.
SETUP_SPECIFIC = SETUP_BLURT[:-1] + (
    '. Best is a\n'
    '     reaction only this question could get (to "What smell takes you straight\n'
    '     back to childhood?": "Oh, crayons!"); never a stock opener like\n'
    '     "Sounds..." or "Classic":')
SETUPS = {"blurt": SETUP_BLURT, "specific": SETUP_SPECIFIC}
# Groq's free tier allows ~8K tokens a minute and one metadata call is ~2K:
# unspaced, the sixth of nine posts met its cap (2026-10-20).
GROQ_SPACING = 15


def pick(spec):
    """1-based post numbers, "2,4,9", or every post when empty."""
    if not spec:
        return list(range(1, len(POSTS) + 1))
    chosen = [int(n) for n in spec.split(",")]
    if not all(1 <= n <= len(POSTS) for n in chosen):
        raise SystemExit(f"posts are numbered 1 to {len(POSTS)}")
    return chosen


def setup_model(model, setup="shipped", groq_model=None):
    """Point the metadata call at `model`, no second model; one try on Gemini.
    `setup="blurt"` or `"specific"` swaps in that wording for the shipped one.
    `groq_model` picks Groq's model; Qwen runs with reasoning off, as its free
    tier allows 1,000 output tokens a minute and it reasons ~2,000 a call."""
    from src import config, llm
    if setup in SETUPS:
        llm._TAG_EDITS = [(llm._TAG_EDITS[0][0], SETUPS[setup])] + llm._TAG_EDITS[1:]
    if groq_model:
        config.GROQ_MODEL = groq_model
    if model == "groq" and config.GROQ_MODEL.startswith("qwen"):
        post = llm.requests.post
        llm.requests.post = lambda url, json=None, **kw: post(
            url, json=dict(json or {}, reasoning_effort="none"), **kw)
    llm.FALLBACK_MODEL = None
    config.GROQ_FALLBACK = False
    config.AI_PROVIDER = "groq" if model == "groq" else "gemini"
    config.DRY_RUN = model == "sample"
    config.METADATA_ON_UPLOAD_MODEL = False
    if model != "groq":   # Groq is free: its per-minute cap is waited out
        retrying = llm.generate_retrying
        llm.generate_retrying = lambda prompt, tries=2, **kw: retrying(prompt, tries=1, **kw)
    return llm


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", choices=["upload", "sample", "groq"], required=True)
    ap.add_argument("--posts", default="", help='1-based, e.g. "2,4,9"; default all')
    ap.add_argument("--setup", choices=["shipped", *SETUPS], default="shipped",
                    help="the setup's wording: as shipped, or one of SETUPS")
    ap.add_argument("--groq-model", default=None,
                    help="with --model groq: e.g. qwen/qwen3.8-27b")
    args = ap.parse_args(argv)
    chosen = pick(args.posts)
    cap = {"upload": UPLOAD_CAP, "sample": SAMPLE_CAP}.get(args.model)
    if cap is not None and len(chosen) > cap:
        raise SystemExit(f"--model {args.model} reads at most {cap} posts a run")
    # Without its key, provider() quietly answers on Gemini's upload model:
    # uncapped and with retries, a run could spend 18 of the day's 20.
    if args.model == "groq" and not os.environ.get("GROQ_API_KEY"):
        raise SystemExit("--model groq needs GROQ_API_KEY; refusing before any request")
    llm = setup_model(args.model, args.setup, args.groq_model)
    for i, n in enumerate(chosen):
        if args.model == "groq" and i:
            time.sleep(GROQ_SPACING)
        q, answers = POSTS[n - 1]
        meta = llm.get_metadata(q, answers, style="A", caps=True)
        h = meta.commentary
        print(json.dumps({"post": n, "source": meta.source,
                          "setup": h and h.setup, "reactions": h and h.reactions,
                          "vote": h and h.verdict}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
