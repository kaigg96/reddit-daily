"""Free sample renders: a fixed post over silent narration (PRD §0, "Make
sample videos free").

A sample exists to prove a render change still produces a playable video.
Real narration bills Polly and real metadata spends Gemini requests shared
with production, so samples were rationed to one per 12h and finished changes
waited on them. This module supplies the three paid inputs -- the screened
post, the metadata, the narration -- for nothing. Not wired into the run yet.
"""
import unicodedata

import numpy as np
from moviepy import AudioClip

from . import config, standin
from .content import PostContent
from .llm import Commentary, MetadataResult

# Near Polly neural's pace, so captions and the duration guard see
# realistic segment lengths.
WORDS_PER_SECOND = 2.7

POST = PostContent(
    subreddit="AskReddit",
    title="What's a job that looks easy but is actually brutal?",
    comments=[
        "Waiting tables. You are on your feet for ten hours and smiling the whole time.",
        "Lifeguarding. Hours of boredom, then thirty seconds that matter more than anything.",
        "Teaching kindergarten. Twenty tiny people and none of them want to sit down.",
    ],
    shortlink="https://redd.it/sample",
    topic="money-work",
    screen_source="sample",
)

METADATA = MetadataResult(
    title="3 Brutal Jobs That Seem Easy",
    keywords=["hard jobs", "jobs that look easy"],
    cta="Which job would YOU never do? Tell us below!",
    source="sample",
    # Used only while config.COMMENTARY is on (bet 1, #70).
    commentary=Commentary(
        # Tags (config.HOST_TAGS, #77), as the ask now writes them.
        setup="Oof, deceptively hard.",
        reactions=["Smiling is cardio.",
                   "Boredom, then chaos.",
                   "Twenty tiny bosses."],
        verdict="My hand goes up for lifeguarding. Which one gets your vote?",
    ),
)


def _spoken(c):
    """Kept at a word's edge: everything but punctuation, so "$5" and "50%"
    caption as written while a comma or quote stays outside the word."""
    return not unicodedata.category(c).startswith("P") or c in "%#&@"


def silent_marks(text):
    """Word marks shaped like Polly's: evenly paced, byte offsets into UTF-8.
    As Polly's, a word's text and end leave out the punctuation around it
    (video.group_words reads the byte after the end for a sentence break), and
    a token of punctuation alone (a dash) gets no mark."""
    marks, raw, pos = [], text.encode("utf-8"), 0
    for word in text.split():
        pos = raw.index(word.encode("utf-8"), pos)
        first = next((i for i, c in enumerate(word) if _spoken(c)), None)
        if first is not None:
            last = max(i for i, c in enumerate(word) if _spoken(c))
            core = word[first:last + 1]
            end = pos + len(word[:last + 1].encode("utf-8"))
            marks.append({"t": len(marks) / WORDS_PER_SECOND, "w": core, "end_offset": end})
        pos += len(word.encode("utf-8"))
    return marks


def synthesize(text, out_path, voice=None):
    """Write narration that never calls Polly; return its marks. Stands in for
    tts.synthesize_with_marks: the free stand-in voice while
    config.STAND_IN_VOICE is on, else silence as long as `text` would take to
    read. A stand-in that fails falls back to silence and says so."""
    marks = silent_marks(text)
    if config.STAND_IN_VOICE:
        try:
            return standin.synthesize(text, out_path, voice, marks)
        except Exception as e:   # a sample must still render
            print(f"Stand-in voice FAILED, narrating silently: {type(e).__name__}: {e}")
    duration = max(len(marks), 1) / WORDS_PER_SECOND + 0.3
    silence = lambda t: np.zeros((len(t), 2)) if np.ndim(t) else np.zeros(2)
    clip = AudioClip(silence, duration=duration, fps=44100)
    clip.write_audiofile(str(out_path), logger=None)
    clip.close()
    return marks
