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

import json

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


GOOD_JSON = ('{"title": "A Great Title", '
             '"keywords": ["one", "two"], "cta": "Comment your answer below!"}')


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


def test_metadata_is_one_request_not_three(captured):
    """The whole point: the free-tier cap is 20 requests/day and production was
    spending three of them on one post. Title, keywords and CTA now share a
    request, taking a run from 4-7 down to 2-5."""
    llm.get_metadata("q", ["a", "b", "c"], style="B")

    assert len(captured) == 1
    assert captured[0]["json"]["generationConfig"]["thinkingConfig"]["thinkingBudget"] == 0


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

    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert (meta.title, meta.keywords, meta.cta) == (None, None, None)
    assert "super-secret" not in capsys.readouterr().out


def test_metadata_parses_a_good_response(monkeypatch):
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: GOOD_JSON)
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert meta.title == "A Great Title"
    assert meta.keywords == ["one", "two"]
    assert meta.cta == "Comment your answer below!"


def test_metadata_survives_a_markdown_fence(monkeypatch):
    """Models wrap JSON in ```json fences unprompted; the screen already
    tolerates this and so must this."""
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: f"```json\n{GOOD_JSON}\n```")
    assert llm.get_metadata("q", ["a", "b", "c"]).title == "A Great Title"


def test_one_missing_field_does_not_cost_the_others(monkeypatch):
    """The risk merging three calls introduces: an all-or-nothing result would
    make a single bad field as expensive as a dead API. Fail-soft is per field.
    """
    monkeypatch.setattr(llm, "_generate",
                        lambda *a, **k: '{"title": "Kept", "keywords": ["k"]}')
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert meta.title == "Kept"
    assert meta.keywords == ["k"]
    assert meta.cta is None        # caller falls back to the generic outro only


def test_unparseable_json_falls_back_on_everything(monkeypatch, capsys):
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: "{not json at all")
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert (meta.title, meta.keywords, meta.cta) == (None, None, None)
    assert "fall back" in capsys.readouterr().out


def test_source_separates_a_dead_api_from_a_bad_answer(monkeypatch):
    """Both come back with three empty fields, and the release gate has to
    tell them apart: one means "could not check", the other "do not merge".
    Without this the shared 20/day quota running out reads as a release
    regression, which paged the owner three mornings running."""
    def boom(*a, **k):
        raise llm.requests.HTTPError("429 Too Many Requests")

    monkeypatch.setattr(llm, "_generate", boom)
    assert llm.get_metadata("q", ["a", "b", "c"]).source == "error"

    # Gemini answered -- badly. That IS evidence about the prompt.
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: "no json here")
    assert llm.get_metadata("q", ["a", "b", "c"]).source == "gemini"

    monkeypatch.setattr(llm, "_generate", lambda *a, **k: GOOD_JSON)
    assert llm.get_metadata("q", ["a", "b", "c"]).source == "gemini"


def test_keywords_distinguishes_a_missing_field_from_an_empty_one(monkeypatch):
    """None means the model never gave us the field; [] means it gave us
    nothing usable. Only the first says the call is unhealthy, and keywords_ok
    in the upload log depends on the difference."""
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: '{"title": "t", "keywords": []}')
    assert llm.get_metadata("q", ["a", "b", "c"]).keywords == []

    monkeypatch.setattr(llm, "_generate", lambda *a, **k: '{"title": "t"}')
    assert llm.get_metadata("q", ["a", "b", "c"]).keywords is None


def test_metadata_strips_the_junk_llms_add(monkeypatch):
    """Quotes, markdown emphasis, blanks and non-strings all show up in practice."""
    payload = json.dumps({
        "title": '  "Quoted"  ',
        "keywords": ["  a  ", "", None],
        "cta": "**Bold** line",
    })
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: payload)

    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert meta.title == "Quoted"
    assert meta.keywords == ["a"]      # blanks and non-strings dropped
    assert meta.cta == "Bold line"


def test_resolve_title_blanks_the_style_when_generation_failed():
    """The R2.2 contamination fix.

    An upload carrying the raw Reddit question is not evidence about style A, B
    or C. Logging one as style B is what biased the cohorts unevenly.
    """
    r = llm.resolve_title(None, style="B", fallback="Raw question?")
    assert r.title == "Raw question?"
    assert r.style == ""
    assert r.ok is False


def test_resolve_title_keeps_the_style_when_generation_worked():
    r = llm.resolve_title('  "Great Title"  ', style="C", fallback="Raw?")
    assert r.title == "Great Title"
    assert r.style == "C"
    assert r.ok is True


def test_resolve_title_treats_whitespace_only_as_a_failure():
    """sanitize_title would fall back anyway, so the style must not be claimed."""
    r = llm.resolve_title("   \n  ", style="A", fallback="Raw?")
    assert r.title == "Raw?"
    assert r.style == ""
    assert r.ok is False


def test_sanitize_title_falls_back_when_generation_failed():
    """The fallback path is what shipped raw Reddit questions as titles."""
    assert llm.sanitize_title(None, fallback="Raw question?") == "Raw question?"
    assert llm.sanitize_title('  "Quoted"  ', fallback="x") == "Quoted"
    assert len(llm.sanitize_title("z" * 200, fallback="x")) == 100


def _raises(exc):
    def boom(*a, **k):
        raise exc
    return boom


def test_failure_names_why_the_fields_are_empty(monkeypatch):
    """The upload log's ok-flags cannot tell the shared daily cap (429) from a
    timeout, and the two need different fixes. `failure` can."""
    quota = llm.requests.Response()
    quota.status_code = 429
    monkeypatch.setattr(llm, "_generate",
                        _raises(llm.requests.HTTPError("429", response=quota)))
    assert llm.get_metadata("q", ["a"]).failure == "http_429"

    monkeypatch.setattr(llm, "_generate", _raises(llm.requests.ReadTimeout()))
    assert llm.get_metadata("q", ["a"]).failure == "timeout"

    monkeypatch.setattr(llm, "_generate", lambda *a, **k: "no json here")
    assert llm.get_metadata("q", ["a"]).failure == "no_json"

    monkeypatch.setattr(llm, "_generate", lambda *a, **k: "{not: json}")
    assert llm.get_metadata("q", ["a"]).failure == "bad_json"

    monkeypatch.setattr(llm, "_generate", lambda *a, **k: GOOD_JSON)
    assert llm.get_metadata("q", ["a"]).failure == ""


def test_failure_label_never_carries_the_keyed_url(monkeypatch):
    monkeypatch.setattr(llm, "_generate", _raises(
        llm.requests.ConnectionError("failed for url: ...?key=super-secret")))
    assert llm.get_metadata("q", ["a"]).failure == "ConnectionError"


def test_the_upload_log_keeps_the_failure_kind():
    from src import log
    assert "meta_failure" in log.FIELDS


def _called_url(monkeypatch, dry_run):
    seen = {}

    class Resp:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": "ok"}]}}]}

    def post(url, **kw):
        seen["url"] = url
        return Resp()

    monkeypatch.setenv("GEMINI_API_KEY", "k")
    monkeypatch.setattr(llm.requests, "post", post)
    monkeypatch.setattr(llm.config, "DRY_RUN", dry_run)
    llm._generate("p")
    return seen["url"]


def test_production_calls_keep_the_production_model(monkeypatch):
    assert _called_url(monkeypatch, False) == (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent")


def test_a_dry_run_spends_a_different_models_allowance(monkeypatch):
    """The free tier is counted per model: a sample must not starve an upload."""
    assert "/gemini-3.5-flash-lite:generateContent" in _called_url(monkeypatch, True)


def test_title_styles_run_four_b_to_one_a_to_one_c():
    """§0 #10: any six consecutive days carry B:A:C = 4:1:1, A and C the control.
    Keyed on the date, so both daily uploads share a style and each day splits
    the rotation's two subreddits under one style (PRD §0 #3)."""
    import collections
    import datetime
    start = datetime.date(2026, 10, 6)
    for offset in range(12):
        days = [start + datetime.timedelta(d) for d in range(offset, offset + 6)]
        counts = collections.Counter(llm.title_style_for(d) for d in days)
        assert counts == {"B": 4, "A": 1, "C": 1}

def test_metadata_retries_a_503_once(monkeypatch):
    """One 503 cost the 2026-10-01 18:29 upload its title, keywords and CTA:
    the screen retried transient failures, the metadata call did not."""
    calls = []

    def flaky(*a, **k):
        calls.append(1)
        if len(calls) == 1:
            resp = FakeResponse(status=503)
            raise llm.requests.HTTPError("503", response=resp)
        return GOOD_JSON

    monkeypatch.setattr(llm, "_generate", flaky)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert len(calls) == 2
    assert meta.title == "A Great Title"


def test_a_503_waits_out_an_overload_before_retrying(monkeypatch):
    """A 4s wait did not outlast the 503s on the 2026-10-02 release check or
    the 2026-10-04 06:04 upload, which lost its title."""
    waits = []

    def overloaded(*a, **k):
        if not waits:
            raise llm.requests.HTTPError("503", response=FakeResponse(status=503))
        return GOOD_JSON

    monkeypatch.setattr(llm, "_generate", overloaded)
    monkeypatch.setattr(llm.time, "sleep", waits.append)
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert waits == [llm._OVERLOAD_WAIT] and llm._OVERLOAD_WAIT >= 30
    assert meta.title == "A Great Title"


def test_metadata_never_retries_a_429(monkeypatch):
    """A 429 is the shared daily cap; a retry only spends what is left."""
    calls = []

    def capped(*a, **k):
        calls.append(1)
        raise llm.requests.HTTPError("429", response=FakeResponse(status=429))

    monkeypatch.setattr(llm, "_generate", capped)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert len(calls) == 1
    assert meta.failure == "http_429"
