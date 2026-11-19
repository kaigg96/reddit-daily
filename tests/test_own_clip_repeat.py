"""The own-questions show never repeats the last upload's background clip
(PLAN C16, #90's sameness check); Reddit's pick is unchanged."""
import random
from pathlib import Path

from src import background, config, log

FILES = [Path(f"pexels_{n}.mp4") for n in (1, 2, 3)]


def test_the_own_show_never_takes_the_last_uploads_clip(monkeypatch):
    monkeypatch.setattr(config, "SOURCE", "own")
    monkeypatch.setattr(log, "last_bg_clip", lambda: "pexels_2.mp4")
    picks = {background._pick_broll(FILES, random.Random(i)).name for i in range(60)}
    assert picks == {"pexels_1.mp4", "pexels_3.mp4"}


def test_one_clip_or_no_record_still_picks(monkeypatch):
    monkeypatch.setattr(config, "SOURCE", "own")
    monkeypatch.setattr(log, "last_bg_clip", lambda: "pexels_1.mp4")
    assert background._pick_broll(FILES[:1], random.Random(0)).name == "pexels_1.mp4"
    monkeypatch.setattr(log, "last_bg_clip", lambda: "")
    assert background._pick_broll(FILES, random.Random(0)) in FILES


def test_reddits_pick_is_unchanged_draw_for_draw(monkeypatch):
    monkeypatch.setattr(config, "SOURCE", "reddit")
    monkeypatch.setattr(log, "last_bg_clip", lambda: (_ for _ in ()).throw(AssertionError("read")))
    for seed in range(20):
        assert background._pick_broll(FILES, random.Random(seed)) == random.Random(seed).choice(FILES)


def test_the_last_clip_is_read_from_the_log(monkeypatch, tmp_path):
    p = tmp_path / "upload_log.csv"
    p.write_text("timestamp_utc,bg_clip\n2026-11-14T06:49:16+00:00,a.mp4\n"
                 "2026-11-14T18:21:27+00:00,b.mp4\n")
    monkeypatch.setattr(config, "UPLOAD_LOG", p)
    assert log.last_bg_clip() == "b.mp4"
    monkeypatch.setattr(config, "UPLOAD_LOG", tmp_path / "missing.csv")
    assert log.last_bg_clip() == ""
