"""Music rotation (E1 T2): the public-domain tracks and the sealed funk bed
are all in rotation, a missing seal key still leaves the plain ones, and the
picker never takes the last upload's track."""
import random

from src import config, log, video


def _setup(monkeypatch, tmp_path, plain, sealed_unsealed):
    music = tmp_path / "music"
    music.mkdir()
    for name in plain:
        (music / name).write_bytes(b"")
    (music / "funk_bg_lower.mp3.enc").write_bytes(b"")   # sealed copy: never a candidate
    funk = tmp_path / "funk_bg_lower.mp3"
    if sealed_unsealed:
        funk.write_bytes(b"")
    monkeypatch.setattr(config, "MUSIC_DIR", music)
    monkeypatch.setattr(config, "FALLBACK_MUSIC", funk)


def _log(monkeypatch, tmp_path, last):
    p = tmp_path / "upload_log.csv"
    p.write_text("timestamp_utc,music_track\n2026-11-14T06:49:16+00:00,a.mp3\n"
                 f"2026-11-14T18:21:27+00:00,{last}\n")
    monkeypatch.setattr(config, "UPLOAD_LOG", p)


PLAIN = ["freepd_a.mp3", "freepd_b.mp3", "freepd_c.mp3"]


def test_the_picker_never_takes_the_last_uploads_track(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, PLAIN, sealed_unsealed=True)
    for last in PLAIN + ["funk_bg_lower.mp3"]:
        _log(monkeypatch, tmp_path, last)
        tracks = video._music_tracks()
        picks = {video._pick_track(tracks, random.Random(i))[0].name for i in range(80)}
        assert picks == set(PLAIN + ["funk_bg_lower.mp3"]) - {last}


def test_unsealed_funk_joins_at_its_own_volume(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, PLAIN, sealed_unsealed=True)
    vols = {p.name: v for p, v in video._music_tracks()}
    assert vols == {**{n: config.MUSIC_VOLUME_LIBRARY for n in PLAIN},
                    "funk_bg_lower.mp3": config.MUSIC_VOLUME_FALLBACK}


def test_without_the_seal_key_the_plain_tracks_still_play(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, PLAIN, sealed_unsealed=False)
    assert [p.name for p, _ in video._music_tracks()] == PLAIN


def test_one_track_or_no_record_still_picks(monkeypatch, tmp_path):
    _setup(monkeypatch, tmp_path, PLAIN[:1], sealed_unsealed=False)
    _log(monkeypatch, tmp_path, PLAIN[0])
    assert video._pick_track(video._music_tracks(), random.Random(0))[0].name == PLAIN[0]
    monkeypatch.setattr(config, "UPLOAD_LOG", tmp_path / "missing.csv")
    assert log.last_music_track() == ""
    empty = tmp_path / "empty"
    empty.mkdir()
    monkeypatch.setattr(config, "MUSIC_DIR", empty)
    assert video._pick_music(20.0, random.Random(0)) == (None, "none")


def test_the_committed_rotation_has_four_licensed_tracks():
    names = [p.name for p in sorted(config.MUSIC_DIR.glob("*.mp3"))]
    assert len([n for n in names if n.startswith("freepd_")]) >= 3
    licences = (config.MUSIC_DIR / "LICENSES.md").read_text()
    for n in names:
        assert f"`{n}`" in licences, n
    # with the sealed funk bed, unsealed in CI, that is at least four in rotation
    assert (config.ASSETS / "funk_bg_lower.mp3.enc").exists()
