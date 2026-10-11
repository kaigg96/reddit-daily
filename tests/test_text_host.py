"""Bet 1's text-only host (PRD R3.2, after #71): our lines are shown, never
spoken, so a first-time viewer can tell them from Reddit's words."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import config, video


def test_a_segment_has_no_note_unless_given_one():
    assert video.Segment(kind="comment", text="x", audio_path="a.mp3", marks=[]).note == ""


def test_a_note_comes_in_partway_and_runs_to_the_next_segment():
    start, span = video.note_window(10.0, 4.0)
    assert 10.0 < start < 14.0
    assert abs((start + span) - (14.0 + config.INTER_SEGMENT_GAP)) < 1e-9


def test_notes_sit_between_the_captions_and_the_watermark():
    assert 700 < config.NOTE_Y < 1500 - config.NOTE_FONT_SIZE * 2


# --- the narration, text-only (HOST_TEXT) -------------------------------------

import pytest

from src import llm, run
from tests.test_commentary import HOST, POST_ANSWERS, _Post, _synth, _too_long_until


@pytest.fixture
def text_host(monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY", True)
    monkeypatch.setattr(config, "HOST_TEXT", True)


def _segments():
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    return host, run.build_segments(_Post, host.verdict, host, _synth, "Stephen")


def test_the_host_is_shown_never_heard(text_host):
    _, segs = _segments()
    assert [s.kind for s in segs] == ["title", "comment", "comment", "vote"]
    assert [s.note for s in segs] == [HOST["setup"], *HOST["reactions"], ""]
    assert all(s.speaker is None for s in segs)        # one voice: the narrator's
    assert segs[-1].text == HOST["cta"]                # the vote, spoken as a CTA


def test_the_guard_drops_an_answer_with_its_note(text_host):
    host, segs = _segments()
    outro = run.fit_to_length(segs, _too_long_until(3), host, _synth)
    assert [s.text for s in segs][1:2] == [POST_ANSWERS[0]] and len(segs) == 3
    assert HOST["reactions"][1] not in [s.note for s in segs]
    assert outro == config.OUTRO_TEXT == segs[-1].text  # the vote may name it


def test_own_words_count_the_notes_and_the_vote():
    segs = [video.Segment("title", "a" * 20, "", [], note="b" * 10),
            video.Segment("comment", "c" * 20, "", [], note="d" * 10),
            video.Segment("vote", "e" * 20, "", [])]
    assert run.own_words_share(segs) == "0.500"


def test_every_text_edit_matches_the_voiced_ask():
    # A reworded voiced ask would silently leave a text host told to "speak".
    for old, _ in llm._TEXT_EDITS:
        assert old in llm._COMMENTARY_ASK, old


def test_a_text_host_is_told_it_is_read_and_must_not_quote(text_host):
    ask = llm._commentary_ask(2)
    assert "never spoken" in ask and "Never\n     repeat the answer's own words" in ask
    assert "heard" not in ask


def test_a_voiced_host_keeps_its_ask(monkeypatch):
    monkeypatch.setattr(config, "HOST_TEXT", False)
    assert llm._commentary_ask(2) == llm._COMMENTARY_ASK.format(n=2)


def test_a_text_reaction_has_a_tighter_cap(text_host):
    assert not llm._within_cap(" ".join(["word"] * 16), "reaction")
    assert llm._within_cap(" ".join(["word"] * 15), "reaction")
