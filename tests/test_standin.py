"""The stand-in voice for branch renders (src/standin.py, #77).

Kokoro itself is never installed for tests: these pin how its timings become
Polly-shaped marks, when it is used, and that a failure still renders.
"""
import os
import subprocess
import sys
from pathlib import Path

from moviepy import AudioFileClip

from src import config, sample, standin, standin_worker, video

ROOT = Path(__file__).resolve().parent.parent


def test_a_word_per_spoken_group_takes_the_voices_own_times():
    marks = sample.silent_marks("Waiting tables is brutal.")
    out = standin.word_marks(marks, [0.1, 0.6, 1.2, 1.5], 2.4)
    assert [m["t"] for m in out] == [0.1, 0.6, 1.2, 1.5]
    # Byte offsets are the text's, untouched.
    assert [m["end_offset"] for m in out] == [m["end_offset"] for m in marks]


def test_a_number_spoken_as_several_words_still_ends_with_the_speech():
    """'$1,200' is read as several words, so the counts differ: the span is
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


def _flag(name="STAND_IN_VOICE", **env):
    clean = {k: v for k, v in os.environ.items()
             if k not in ("SAMPLE", "SILENT_NARRATION", "STAND_IN_VOICE",
                          "METADATA_ON_UPLOAD_MODEL")}
    done = subprocess.run(
        [sys.executable, "-c", f"from src import config; print(config.{name})"],
        cwd=ROOT, env={**clean, **env}, capture_output=True, text=True, check=True)
    return done.stdout.strip()


def test_branch_renders_get_the_voice_and_uploads_never_do():
    """dry-run.yml sets SILENT_NARRATION for every branch, and nothing else."""
    assert _flag(SILENT_NARRATION="1") == "True"
    assert _flag() == "False"                     # an upload, or a main dry run
    assert _flag(SAMPLE="1") == "False"           # the fixed post only proves it plays
    assert _flag(SILENT_NARRATION="1", STAND_IN_VOICE="0") == "False"


def test_a_render_judged_by_ear_shows_the_upload_models_tags():
    """The free sample model's tags were labels where the upload model's
    reacted (10-20), so a speaking branch render spends one upload-model
    request to show what an upload would; nothing else changes model."""
    up = "METADATA_ON_UPLOAD_MODEL"
    assert _flag(up, SILENT_NARRATION="1") == "True"
    assert _flag(up, SILENT_NARRATION="1", STAND_IN_VOICE="0") == "False"
    assert _flag(up, SAMPLE="1") == "False"
    assert _flag(up) == "False"


def test_every_package_and_file_the_voice_fetches_is_locked_by_hash():
    import re
    lines = [l for l in standin.LOCK.read_text().splitlines() if l and not l.startswith("#")]
    assert len(lines) == 16
    assert all(re.fullmatch(r"[A-Za-z0-9._-]+==\S+ --hash=sha256:[0-9a-f]{64}", l) for l in lines)
    assert all(re.fullmatch(r"[0-9a-f]{64}", digest) for _, digest in standin.FILES.values())


def test_counts_that_match_by_chance_do_not_place_a_number():
    """'I paid $5 - worth it.': five marks once the dash is dropped, and the
    voice may say 'five dollars' in five groups too -- equal counts that would
    put 'dollars' on the wrong word."""
    marks = sample.silent_marks("I paid $5 - worth it.")
    assert [m["w"] for m in marks] == ["I", "paid", "$5", "worth", "it"]
    out = standin.word_marks(marks, [0.1, 0.3, 0.6, 0.9, 1.2], 2.0)
    assert [m["t"] for m in out] != [0.1, 0.3, 0.6, 0.9, 1.2]
    assert [m["t"] for m in out] == sorted(m["t"] for m in out)


def test_captions_break_at_punctuation_as_they_do_with_polly():
    text = "Oof, deceptively hard."
    marks = standin.word_marks(sample.silent_marks(text), [0.1, 0.5, 0.9], 1.6)
    groups = video.group_words(marks, text, 1.6)
    assert [g.text for g in groups] == ["Oof", "deceptively hard"]


class _T:
    def __init__(self, phoneme, start):
        self.phoneme, self.start = phoneme, start


def test_the_worker_starts_a_word_per_spoken_group_and_skips_a_dash():
    timings = [_T("h", 0.1), _T("ˈaɪ", 0.15), _T(" ", 0.3), _T("—", 0.35),
               _T(" ", 0.4), _T("ðˈɛɹ", 0.5), _T(".", 0.7)]
    assert standin_worker.word_starts(timings) == [0.1, 0.5]


def test_one_failure_silences_the_rest_of_the_run_at_once(monkeypatch, tmp_path):
    monkeypatch.setitem(standin._state, "broken", None)
    calls = []

    def ensure():
        calls.append(1)
        raise RuntimeError("pip exited 1")
    monkeypatch.setattr(standin, "ensure", ensure)
    for _ in range(3):
        try:
            standin.synthesize("hi there", tmp_path / "a.mp3", "Danielle", [])
        except RuntimeError:
            pass
    assert calls == [1]


def test_a_stale_or_half_built_environment_is_built_again(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "GEN", tmp_path)
    monkeypatch.setitem(standin._state, "started", None)
    home = tmp_path / "standin"
    (home / "venv" / "bin").mkdir(parents=True)
    (home / "venv" / "bin" / "python").write_text("")
    (home / "installed.txt").write_text("kokoro-onnx==0.0.1")   # yesterday's pins
    for name in standin.FILES:
        (home / name).write_text("model")
    ran = []
    monkeypatch.setattr(standin, "_digest", lambda path: standin.FILES[Path(path).name][1])
    monkeypatch.setattr(standin, "_python", lambda: home / "venv" / "bin" / "python")
    # The venv is removed before rebuilding; stand in for venv creating it.
    def run(args, **kw):
        ran.append(args[1:3])
        (home / "venv" / "bin").mkdir(parents=True, exist_ok=True)
        (home / "venv" / "bin" / "python").write_text("")
    monkeypatch.setattr(standin, "_run", run)
    standin.ensure()
    assert ["-m", "venv"] in ran and ["-m", "pip"] in ran
    assert (home / "installed.txt").read_text() == standin.LOCK.read_text()
    ran.clear()
    standin.ensure()      # now current: nothing to do
    assert ran == []


def test_a_model_file_off_its_digest_is_refused_and_not_kept(monkeypatch, tmp_path):
    import io
    monkeypatch.setattr(config, "GEN", tmp_path)
    monkeypatch.setitem(standin._state, "started", None)
    home = tmp_path / "standin"
    (home / "venv" / "bin").mkdir(parents=True)
    (home / "venv" / "bin" / "python").write_text("")
    (home / "installed.txt").write_text(standin.LOCK.read_text())
    monkeypatch.setattr(standin, "_python", lambda: home / "venv" / "bin" / "python")
    monkeypatch.setattr(standin.urllib.request, "urlopen",
                        lambda url, timeout: io.BytesIO(b"not the model"))
    try:
        standin.ensure()
        assert False, "a file off its digest must be refused"
    except RuntimeError as e:
        assert "digest" in str(e)
    assert not any(p for p in home.iterdir() if p.is_file() and p.name != "installed.txt")


def test_third_party_code_never_sees_the_jobs_keys(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "secret")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "secret")
    env = standin._clean_env()
    assert "PATH" in env and not any("secret" == v for v in env.values())


def test_only_a_silent_run_reaches_the_stand_in():
    """What keeps uploads off the stand-in is run.main's gate: the one call
    into sample.synthesize sits under `if silent:`, and silent means SAMPLE or
    SILENT_NARRATION, which an upload never sets."""
    import inspect
    import re
    from src import run
    source = inspect.getsource(run.main)
    # Assigned once, to exactly this: widened (say, "or STAND_IN_VOICE") or
    # reassigned, a run that is not a dry run could narrate with the stand-in.
    assert re.findall(r"^\s*silent\s*=(.*)$", source, re.M) == \
        [" config.SAMPLE or config.SILENT_NARRATION"]
    assert source.count("sample.synthesize(") == 1
    assert "if silent:\n            marks = sample.synthesize(" in source
    assert "standin." not in source        # no route around sample.synthesize
