"""The live upload retries a transient error by resuming (src/youtube.py)."""
import pytest
from googleapiclient.errors import HttpError

from src import youtube


class _Resp(dict):
    def __init__(self, status):
        super().__init__(status=str(status))
        self.status, self.reason = status, "x"


def _request(*outcomes):
    class Request:
        calls = 0

        def next_chunk(self):
            Request.calls += 1
            out = outcomes[min(Request.calls, len(outcomes)) - 1]
            if isinstance(out, Exception):
                raise out
            return out
    return Request()


def test_a_server_error_or_dropped_connection_is_resumed():
    r = _request(HttpError(_Resp(503), b""), OSError("reset"), (None, {"id": "abc"}))
    waits = []
    assert youtube._next_chunk_retrying(r, waits.append) == (None, {"id": "abc"})
    assert r.calls == 3 and waits == [1, 2]


def test_a_refusal_is_not_retried():
    r = _request(HttpError(_Resp(403), b"quotaExceeded"), (None, {"id": "abc"}))
    with pytest.raises(HttpError):
        youtube._next_chunk_retrying(r, lambda s: None)
    assert r.calls == 1


def test_retries_are_capped():
    r = _request(HttpError(_Resp(500), b""))
    with pytest.raises(HttpError):
        youtube._next_chunk_retrying(r, lambda s: None)
    assert r.calls == youtube.UPLOAD_RETRIES + 1


def test_upload_video_still_returns_none_on_a_lasting_error(monkeypatch, tmp_path):
    class Videos:
        def insert(self, **kw): return _request(HttpError(_Resp(400), b"bad"))

    class Client:
        def videos(self): return Videos()

    monkeypatch.setattr(youtube, "_authenticate", lambda: None)
    monkeypatch.setattr(youtube, "build", lambda *a, **k: Client())
    monkeypatch.setattr(youtube, "MediaFileUpload", lambda *a, **k: None)
    assert youtube.upload_video(tmp_path / "v.mp4", "t", "d", ["k"]) is None
