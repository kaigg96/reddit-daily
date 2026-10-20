"""Read bet 1's host lines (#77) on fixed posts: one metadata request each.

    venv/bin/python scripts/tag_trial.py --model upload --posts 2,4,9
    venv/bin/python scripts/tag_trial.py --model sample        # all nine
    venv/bin/python scripts/tag_trial.py --model groq

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
import sys

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


def pick(spec):
    """1-based post numbers, "2,4,9", or every post when empty."""
    if not spec:
        return list(range(1, len(POSTS) + 1))
    chosen = [int(n) for n in spec.split(",")]
    if not all(1 <= n <= len(POSTS) for n in chosen):
        raise SystemExit(f"posts are numbered 1 to {len(POSTS)}")
    return chosen


def setup_model(model):
    """Point the metadata call at `model`, one try, no second model."""
    from src import config, llm
    llm.FALLBACK_MODEL = None
    config.GROQ_FALLBACK = False
    config.AI_PROVIDER = "groq" if model == "groq" else "gemini"
    config.DRY_RUN = model == "sample"
    config.METADATA_ON_UPLOAD_MODEL = False
    retrying = llm.generate_retrying
    llm.generate_retrying = lambda prompt, tries=2, **kw: retrying(prompt, tries=1, **kw)
    return llm


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", choices=["upload", "sample", "groq"], required=True)
    ap.add_argument("--posts", default="", help='1-based, e.g. "2,4,9"; default all')
    args = ap.parse_args(argv)
    chosen = pick(args.posts)
    cap = {"upload": UPLOAD_CAP, "sample": SAMPLE_CAP}.get(args.model)
    if cap is not None and len(chosen) > cap:
        raise SystemExit(f"--model {args.model} reads at most {cap} posts a run")
    llm = setup_model(args.model)
    for n in chosen:
        q, answers = POSTS[n - 1]
        meta = llm.get_metadata(q, answers, style="A", caps=True)
        h = meta.commentary
        print(json.dumps({"post": n, "source": meta.source,
                          "setup": h and h.setup, "reactions": h and h.reactions,
                          "vote": h and h.verdict}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
