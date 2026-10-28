"""The live upload retries a transient error by resuming, and nothing after it raises (src/youtube.py)."""
import http.client

import google.auth.exceptions
import httplib2
import pytest
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

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
    assert r.calls == 3 and waits == [4, 16]


@pytest.mark.parametrize("dropped", [http.client.IncompleteRead(b""),
                                     httplib2.ServerNotFoundError("dns")])
def test_dropped_connections_that_are_not_oserror_are_resumed(dropped):
    r = _request(dropped, (None, {"id": "abc"}))
    assert youtube._next_chunk_retrying(r, lambda s: None) == (None, {"id": "abc"})


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


def test_the_chunk_is_a_multiple_of_256_kib():
    assert youtube.UPLOAD_CHUNK % (256 * 1024) == 0


# The library behaviour the retry's safety rests on, driven for real: the
# installed googleapiclient against a scripted server, so an upgrade that
# changes how it resumes fails here rather than on a live upload.
SIZE = 1_000_000


class _Server:
    def __init__(self, *script):
        self.script, self.sent = list(script), []

    def request(self, uri, method="GET", body=None, headers=None, **kw):
        self.sent.append((method, dict(headers or {})))
        out = self.script.pop(0)
        if isinstance(out, Exception):
            raise out
        info, content = out
        return httplib2.Response(info), content


def _upload(tmp_path, server):
    path = tmp_path / "v.mp4"
    path.write_bytes(b"\0" * SIZE)
    client = build("youtube", "v3", http=server, static_discovery=True)
    media = MediaFileUpload(str(path), chunksize=youtube.UPLOAD_CHUNK, resumable=True,
                            mimetype="video/mp4")
    request = client.videos().insert(part="snippet", body={"snippet": {}}, media_body=media)
    return youtube._next_chunk_retrying(request, lambda s: None)


_SESSION = ({"status": "200", "location": "https://upload.example/session"}, b"")
_DONE = ({"status": "200"}, b'{"id": "abc"}')


def test_a_reset_mid_upload_resumes_from_what_arrived(tmp_path):
    server = _Server(_SESSION, ConnectionResetError("reset"),
                     ({"status": "308", "range": "bytes=0-524287"}, b""), _DONE)
    assert _upload(tmp_path, server) == (None, {"id": "abc"})
    methods = [m for m, _ in server.sent]
    assert methods == ["POST", "PUT", "PUT", "PUT"]
    assert server.sent[2][1]["Content-Range"] == f"bytes */{SIZE}"
    assert server.sent[3][1]["Content-Range"] == f"bytes 524288-{SIZE - 1}/{SIZE}"


def test_a_lost_completion_returns_the_video_without_a_second_upload(tmp_path):
    server = _Server(_SESSION, http.client.IncompleteRead(b""), _DONE)
    assert _upload(tmp_path, server) == (None, {"id": "abc"})
    assert [m for m, _ in server.sent] == ["POST", "PUT", "PUT"]
    assert server.sent[2][1]["Content-Range"] == f"bytes */{SIZE}"


# After the video is live, nothing may raise before run.py records it.
class _Client:
    """Any call chain (thumbnails().set(...)) ends in an execute() that fails."""
    def __init__(self, error):
        self.error = error

    def __getattr__(self, name):
        return lambda *a, **k: self

    def execute(self):
        raise self.error


@pytest.mark.parametrize("call, failed", [
    (lambda: youtube.upload_thumbnail("abc", "t.png"), None),
    (lambda: youtube.upload_caption("abc", "c.srt"), False),
    (lambda: youtube.post_comment("abc", "hi"), False),
])
@pytest.mark.parametrize("error", [ConnectionResetError("reset"),
                                   http.client.IncompleteRead(b""),
                                   google.auth.exceptions.TransportError("token")])
def test_the_calls_after_an_upload_never_raise(monkeypatch, capsys, call, failed, error):
    def fail(*a, **k):
        raise error
    monkeypatch.setattr(youtube, "MediaFileUpload", lambda *a, **k: None)
    monkeypatch.setattr(youtube, "_authenticate", fail)                  # sign-in
    assert call() is failed
    monkeypatch.setattr(youtube, "_authenticate", lambda: None)
    monkeypatch.setattr(youtube, "build", fail)                          # client
    assert call() is failed
    monkeypatch.setattr(youtube, "build", lambda *a, **k: _Client(error))  # the call
    assert call() is failed
    out = capsys.readouterr().out
    assert out.count("::warning::") == 3 and type(error).__name__ in out
