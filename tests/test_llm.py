"""Tests for the Gemini request shape.

These pin a live production regression found 2026-09-19: gemini-2.5-flash
thinks by default, a title call spent 546 reasoning tokens to emit an 8-token
title and took 33.1s, and the module's 30s timeout turned that into a
ReadTimeout. The call fails soft, so nothing broke loudly — roughly a quarter
of uploads in the two weeks before the fix simply shipped the raw Reddit
question as their YouTube title, and the R4.6 screen fell to its keyword
backstop. Nothing in the logs said so.

The request shape is therefore load-bearing, not incidental, and it lives in
one place that every caller shares.
"""

import pytest

from src import llm


class FakeResponse:
    def __init__(self, text="a title", status=200):
        self._text = text
        self.status_code = status

    def raise_for_status(self):
        if self.status_code >= 400:
            raise AssertionError("unexpected error status in this test")

    def json(self):
        return {"candidates": [{"content": {"parts": [{"text": self._text}]}}]}


@pytest.fixture
def captured(monkeypatch):
    """Capture the outgoing request instead of calling Gemini."""
    calls = []

    def fake_post(url, **kw):
        calls.append({"url": url, **kw})
        return FakeResponse()

    monkeypatch.setattr(llm.requests, "post", fake_post)
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    return calls


def test_thinking_is_disabled_by_default(captured):
    """The fix itself. Default thinking is what blew the timeout."""
    llm._generate("hello")
    cfg = captured[0]["json"]["generationConfig"]["thinkingConfig"]
    assert cfg["thinkingBudget"] == 0


def test_every_caller_gets_thinking_disabled(captured):
    """Keywords, title and CTA all share _generate — none may opt back in
    silently, since each one failing soft is invisible in the logs."""
    llm.get_keywords("q", ["a", "b", "c"])
    llm.get_video_title("q", ["a", "b", "c"], style="B")
    llm.get_cta("q")

    assert len(captured) == 3
    for call in captured:
        assert call["json"]["generationConfig"]["thinkingConfig"]["thinkingBudget"] == 0


def test_uses_v1beta_because_v1_rejects_thinking_config(captured):
    """v1 answers thinkingConfig with HTTP 400 'Thinking is not enabled for
    api version v1'. Dropping back to v1 would silently restore the bug."""
    llm._generate("hello")
    assert "/v1beta/" in captured[0]["url"]


def test_a_caller_can_still_opt_into_reasoning(captured):
    """The budget is a parameter, not a hardcode — a genuinely reasoning-heavy
    prompt can ask for it, deliberately and visibly."""
    llm._generate("hello", thinking_budget=512)
    cfg = captured[0]["json"]["generationConfig"]["thinkingConfig"]
    assert cfg["thinkingBudget"] == 512


def test_timeout_is_generous_enough_to_be_a_backstop(captured):
    """30s was a routine limit that real calls crossed. It should now only
    catch a stalled socket."""
    llm._generate("hello")
    assert captured[0]["timeout"] >= 60


def test_the_api_key_is_never_in_the_request_body(captured):
    """It goes in the query string; keeping it out of the body means an error
    log that echoes the body can't leak it."""
    llm._generate("hello")
    assert "test-key" not in str(captured[0]["json"])


def test_failures_stay_soft_and_do_not_echo_the_keyed_url(monkeypatch, capsys):
    """HTTPError messages embed the keyed URL, so callers print the exception
    type only. A leak here would publish the key in the Actions log."""
    def boom(url, **kw):
        raise llm.requests.HTTPError(f"403 Client Error for url: {url}")

    monkeypatch.setattr(llm.requests, "post", boom)
    monkeypatch.setenv("GEMINI_API_KEY", "super-secret")

    assert llm.get_keywords("q", ["a", "b", "c"]) == []
    assert llm.get_video_title("q", ["a", "b", "c"]) is None
    assert llm.get_cta("q") is None
    assert "super-secret" not in capsys.readouterr().out


def test_sanitize_title_falls_back_when_generation_failed():
    """The fallback path is what shipped raw Reddit questions as titles."""
    assert llm.sanitize_title(None, fallback="Raw question?") == "Raw question?"
    assert llm.sanitize_title('  "Quoted"  ', fallback="x") == "Quoted"
    assert len(llm.sanitize_title("z" * 200, fallback="x")) == 100
