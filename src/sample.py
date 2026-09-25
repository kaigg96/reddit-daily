"""Free sample renders: a fixed post over silent narration (PRD §0, "Make
sample videos free").

A sample exists to prove a render change still produces a playable video.
Real narration bills Polly and real metadata spends Gemini requests shared
with production, so samples were rationed to one per 12h and finished changes
waited on them. This module supplies the three paid inputs -- the screened
post, the metadata, the narration -- for nothing. Not wired into the run yet.
"""
import numpy as np
from moviepy import AudioClip

from .content import PostContent
from .llm import MetadataResult

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
)


def silent_marks(text):
    """Word marks shaped like Polly's: evenly paced, byte offsets into UTF-8."""
    marks, raw, pos = [], text.encode("utf-8"), 0
    for i, word in enumerate(text.split()):
        w = word.encode("utf-8")
        pos = raw.index(w, pos)
        marks.append({"t": i / WORDS_PER_SECOND, "w": word, "end_offset": pos + len(w)})
        pos += len(w)
    return marks


def synthesize(text, out_path):
    """Write silent narration as long as `text` would take to read; return its
    marks. Stands in for tts.synthesize_with_marks and never calls Polly."""
    marks = silent_marks(text)
    duration = max(len(marks), 1) / WORDS_PER_SECOND + 0.3
    silence = lambda t: np.zeros((len(t), 2)) if np.ndim(t) else np.zeros(2)
    clip = AudioClip(silence, duration=duration, fps=44100)
    clip.write_audiofile(str(out_path), logger=None)
    clip.close()
    return marks
