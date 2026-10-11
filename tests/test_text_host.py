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
