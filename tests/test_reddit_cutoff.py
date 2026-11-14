"""PLAN §4: unregistered apps lose Reddit's API on 2027-01-12 (#82). Reddit
then answers 401 or 403. Pinned here: that refusal ends the run with an error,
before any Polly call, title request, upload or live-state write
(`prev_post.txt`, the upload log), whether it comes on the post listing or on
a comment fetch after the screen has already spent a request. Which error is
left open: skipping one refused post is fine, so long as the run still ends
without spending or writing anything."""
import types

import prawcore
import pytest

from src import config, content, log, run, screen, tts


def _refusal(status):
    response = types.SimpleNamespace(status_code=status, headers={}, text="")
    return (prawcore.exceptions.Forbidden if status == 403
            else prawcore.exceptions.ResponseException)(response)


class _Comments:
    def __init__(self, error=None):
        self.error = error

    def replace_more(self, limit=0):
        if self.error:
            raise self.error

    def __iter__(self):
        return iter(types.SimpleNamespace(body=f"answer {i}", author=None) for i in range(6))


def _post(title, error=None):
    return types.SimpleNamespace(title=title, over_18=False, comments=_Comments(error))


def _reddit(top):
    class Sub:
        def top(self, time_filter, limit):
            return top()
    return types.SimpleNamespace(subreddit=lambda name: Sub())


class Tripped(BaseException):
    """Outside Exception, so the run's own catches and pytest.raises(Exception)
    both let it through."""


@pytest.fixture
def live_run(monkeypatch, tmp_path):
    """run.main on the live path with every side effect a tripwire."""
    def tripwire(name):
        def fail(*a, **k):
            raise Tripped(f"{name} ran after Reddit refused")
        return fail

    monkeypatch.setattr(config, "DRY_RUN", False)
    monkeypatch.setattr(config, "SAMPLE", False)
    monkeypatch.setattr(config, "SOURCE", "reddit")
    monkeypatch.setenv("RUN_SCHEDULE", config.LEGACY_CRON)
    monkeypatch.setattr(run, "check_channel_name", lambda: None)
    prev = tmp_path / "prev_post.txt"
    prev.write_text("yesterday's question")
    monkeypatch.setattr(config, "PREV_POST_FILE", prev)
    monkeypatch.setattr(log, "uploaded_titles", lambda: set())
    for mod, name in ((tts, "make_polly"), (tts, "synthesize_with_marks"),
                      (run.youtube, "upload_video"), (log, "append_upload_log"),
                      (run.llm, "get_metadata")):
        monkeypatch.setattr(mod, name, tripwire(name))
    screens = []
    monkeypatch.setattr(screen, "classify_slate", lambda titles: screens.append("slate") or None)

    def skip_first(title, pool):
        screens.append(title)
        return screen.ScreenResult("skip_post", category="test", source="gemini")
    monkeypatch.setattr(screen, "screen", skip_first)
    monkeypatch.setattr(log, "append_screen_log", lambda row: None)
    return types.SimpleNamespace(prev=prev, screens=screens)


@pytest.mark.parametrize("status", [401, 403])
def test_a_refused_listing_fails_the_run_before_any_spend(monkeypatch, live_run, status):
    def top():
        raise _refusal(status)
    monkeypatch.setattr(content, "make_reddit", lambda: _reddit(top))
    with pytest.raises(Exception):
        run.main()
    assert live_run.screens == []
    assert live_run.prev.read_text() == "yesterday's question"


@pytest.mark.parametrize("status", [401, 403])
def test_a_refused_comment_fetch_after_a_screen_fails_the_run(monkeypatch, live_run, status):
    """The first post's comments load and its screen spends a request (and
    skips it); the second post's comment fetch is refused."""
    posts = [_post("First question?"), _post("Second question?", error=_refusal(status))]
    monkeypatch.setattr(content, "make_reddit", lambda: _reddit(lambda: posts))
    with pytest.raises(Exception):
        run.main()
    assert live_run.screens == ["slate", "First question?"]
    assert live_run.prev.read_text() == "yesterday's question"
