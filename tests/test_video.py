"""Tests for the video timeline (src/video.py).

Nothing else exercises assemble() before a live run: a shift has no Polly
credentials and cannot dispatch the dry-run workflow, so a composition bug would
first surface as a failed upload. These build the real timeline from silent
placeholder narration -- no Polly, no render -- and pin the one variable `v7`
is testing: what the opening frame shows.
"""

import random

import numpy as np
import pytest
from moviepy import AudioClip, TextClip

from src import config, video

QUESTION = "What is something everybody pretends to enjoy but secretly can't stand?"


def _segment(tmp_path, kind, text, seconds):
    path = tmp_path / f"{kind}_{len(list(tmp_path.iterdir()))}.mp3"
    AudioClip(lambda t: np.zeros((np.size(t), 2)), duration=seconds, fps=22050).write_audiofile(
        str(path), logger=None)
    words = text.split()
    step = seconds / len(words)
    offsets, pos = [], 0
    for w in words:
        pos = text.index(w, pos) + len(w)
        offsets.append(pos)
    marks = [{"t": i * step, "w": w, "end_offset": o} for i, (w, o) in enumerate(zip(words, offsets))]
    return video.Segment(kind=kind, text=text, audio_path=str(path), marks=marks)


@pytest.fixture(scope="module")
def timeline(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("audio")
    segments = [
        _segment(tmp, "title", QUESTION, 2.0),
        _segment(tmp, "comment", "Brunch. It is just breakfast with a queue.", 2.0),
        _segment(tmp, "comment", "Camping, for anyone over thirty.", 2.0),
        _segment(tmp, "outro", config.OUTRO_TEXT, 1.5),
    ]
    return video.assemble(QUESTION, segments, random.Random(0))


def _text_on_screen(result, t):
    # "caption" TextClips store their text already wrapped; compare unwrapped.
    return [" ".join(c.text.split()) for c in result.video.clips
            if isinstance(c, TextClip) and c.start <= t < c.end]


def test_opening_frame_shows_the_whole_question(timeline):
    assert QUESTION in _text_on_screen(timeline, 0.0)


def test_opening_frame_carries_no_format_label(timeline):
    opening = _text_on_screen(timeline, 0.0)
    assert "TODAY'S TOP QUESTION" not in opening
    # Branding survives as the low watermark, not as a header.
    assert opening.count(config.CHANNEL_NAME) == 1


def test_question_stays_pinned_through_the_answers(timeline):
    badges = [c for c in timeline.video.clips
              if isinstance(c, TextClip) and c.text.startswith("ANSWER")]
    assert len(badges) == 2
    for badge in badges:
        assert QUESTION in _text_on_screen(timeline, badge.start)
    assert QUESTION in _text_on_screen(timeline, timeline.duration - 0.1)


def test_a_question_selection_accepts_is_never_truncated():
    longest = "x" * config.MAX_TITLE_LENGTH
    assert video._truncate(longest, config.MAX_TITLE_LENGTH) == longest
