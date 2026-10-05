from moviepy import AudioFileClip

from src import sample


def test_marks_point_at_each_words_end_in_utf8_bytes():
    """video.py reads end_offset as a byte offset, as Polly returns it."""
    text = "Café workers, what's brutal?"
    raw = text.encode("utf-8")
    marks = sample.silent_marks(text)
    assert [m["w"] for m in marks] == text.split()
    for m in marks:
        assert raw[:m["end_offset"]].endswith(m["w"].encode("utf-8"))
    assert [m["t"] for m in marks] == sorted(m["t"] for m in marks)


def test_silent_narration_lasts_as_long_as_reading_the_text(tmp_path):
    path = tmp_path / "comment.mp3"
    text = " ".join(["word"] * 27)
    marks = sample.synthesize(text, path)
    clip = AudioFileClip(str(path))
    try:
        assert abs(clip.duration - (27 / sample.WORDS_PER_SECOND + 0.3)) < 0.2
    finally:
        clip.close()
    assert len(marks) == 27


def test_the_fixture_is_a_complete_post_with_metadata():
    assert sample.POST.title and len(sample.POST.comments) == 3
    assert sample.METADATA.title and sample.METADATA.cta and sample.METADATA.keywords


def test_a_sample_is_always_a_dry_run(monkeypatch):
    """Nothing a sample renders is real, so it must never reach an upload."""
    import importlib
    from src import config
    monkeypatch.delenv("DRY_RUN", raising=False)
    monkeypatch.setenv("SAMPLE", "1")
    try:
        assert importlib.reload(config).DRY_RUN is True
    finally:
        monkeypatch.delenv("SAMPLE")
        importlib.reload(config)


def test_silent_narration_is_always_a_dry_run(monkeypatch):
    """Branch dry runs narrate silently because they hold no Polly keys
    (dry-run.yml). They must never reach an upload either."""
    import importlib
    from src import config
    monkeypatch.delenv("DRY_RUN", raising=False)
    monkeypatch.setenv("SILENT_NARRATION", "1")
    try:
        assert importlib.reload(config).DRY_RUN is True
    finally:
        monkeypatch.delenv("SILENT_NARRATION")
        importlib.reload(config)


def test_a_real_upload_refuses_to_start_without_the_channel_name(monkeypatch):
    """The name is a secret since the repo went public. A live video showing
    the placeholder would be worse than a missed upload."""
    import pytest
    from src import config, run
    monkeypatch.setattr(config, "DRY_RUN", False)
    monkeypatch.setattr(config, "CHANNEL_NAME_SET", False)
    with pytest.raises(SystemExit, match="CHANNEL_NAME"):
        run.check_channel_name()
    monkeypatch.setattr(config, "CHANNEL_NAME_SET", True)
    run.check_channel_name()
    monkeypatch.setattr(config, "CHANNEL_NAME_SET", False)
    monkeypatch.setattr(config, "DRY_RUN", True)
    run.check_channel_name()          # a dry run may use the placeholder
