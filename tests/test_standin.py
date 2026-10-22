"""The stand-in voice for branch renders (src/standin.py, #77).

Kokoro itself is never installed for tests: these pin how its timings become
Polly-shaped marks, when it is used, and that a failure still renders.
"""
import os
import subprocess
import sys
from pathlib import Path

from moviepy import AudioFileClip

from src import config, sample, standin

ROOT = Path(__file__).resolve().parent.parent


def test_a_word_per_spoken_group_takes_the_voices_own_times():
    marks = sample.silent_marks("Waiting tables is brutal.")
    out = standin.word_marks(marks, [0.1, 0.6, 1.2, 1.5], 2.4)
    assert [m["t"] for m in out] == [0.1, 0.6, 1.2, 1.5]
    # Byte offsets are the text's, untouched.
    assert [m["end_offset"] for m in out] == [m["end_offset"] for m in marks]


def test_a_number_spoken_as_several_words_still_ends_with_the_speech():
    """'$1,200' is read as three words, so the counts differ: the span is
    shared out by length rather than the times shifting onto wrong words."""
    marks = sample.silent_marks("I spent $1,200 there.")
    out = standin.word_marks(marks, [0.1, 0.3, 0.7, 1.0, 1.4, 1.9], 2.5)
    times = [m["t"] for m in out]
    assert times[0] == 0.1 and times == sorted(times) and times[-1] < 2.5
    assert len(out) == len(marks)


def test_a_failed_stand_in_still_renders_silently(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(config, "STAND_IN_VOICE", True)

    def broken(*a, **k):
        raise RuntimeError("no network")
    monkeypatch.setattr(standin, "synthesize", broken)
    path = tmp_path / "comment.mp3"
    marks = sample.synthesize("one two three", path, "Danielle")
    clip = AudioFileClip(str(path))
    try:
        assert clip.duration > 1
    finally:
        clip.close()
    assert len(marks) == 3
    assert "Stand-in voice FAILED" in capsys.readouterr().out


def _flag(**env):
    clean = {k: v for k, v in os.environ.items()
             if k not in ("SAMPLE", "SILENT_NARRATION", "STAND_IN_VOICE")}
    done = subprocess.run(
        [sys.executable, "-c", "from src import config; print(config.STAND_IN_VOICE)"],
        cwd=ROOT, env={**clean, **env}, capture_output=True, text=True, check=True)
    return done.stdout.strip()


def test_branch_renders_get_the_voice_and_uploads_never_do():
    """dry-run.yml sets SILENT_NARRATION for every branch, and nothing else."""
    assert _flag(SILENT_NARRATION="1") == "True"
    assert _flag() == "False"                     # an upload, or a main dry run
    assert _flag(SAMPLE="1") == "False"           # the fixed post only proves it plays
    assert _flag(SILENT_NARRATION="1", STAND_IN_VOICE="0") == "False"


def test_every_package_and_file_the_voice_fetches_is_pinned():
    assert all("==" in p for p in standin.PACKAGES)
    assert all(len(digest) == 64 for _, digest in standin.FILES.values())
