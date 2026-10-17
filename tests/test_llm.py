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

from src import config, llm


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


def test_metadata_asks_gemini_for_its_exact_shape(captured):
    """The 2026-10-17 release check: asked for JSON in the prompt alone, the
    three-answer reply did not parse, and a live retry gave four reactions for
    three answers. Either cost the upload every host line."""
    llm.get_metadata("q", ["a", "b", "c"], style="B")
    cfg = captured[0]["json"]["generationConfig"]
    assert cfg["responseMimeType"] == "application/json"
    assert cfg["thinkingConfig"]["thinkingBudget"] == 0
    reactions = cfg["responseSchema"]["properties"]["reactions"]
    assert reactions["minItems"] == reactions["maxItems"] == llm.config.COMMENTARY_ANSWERS
    assert cfg["responseSchema"]["required"] == ["title", "keywords", "setup", "reactions", "cta"]


def test_the_schema_counts_the_answers_actually_read(captured):
    """A thread with fewer answers than the setting reads fewer, one note each."""
    llm.get_metadata("q", ["a", "b"], style="B")
    reactions = captured[0]["json"]["generationConfig"]["responseSchema"]["properties"]["reactions"]
    assert reactions["minItems"] == reactions["maxItems"] == 2


def test_the_plain_reading_asks_only_for_its_three_fields(captured, monkeypatch):
    monkeypatch.setattr(llm.config, "COMMENTARY", False)
    llm.get_metadata("q", ["a", "b", "c"], style="B")
    schema = captured[0]["json"]["generationConfig"]["responseSchema"]
    assert schema["required"] == ["title", "keywords", "cta"]


def test_a_sample_model_gets_the_schema_without_a_thinking_budget(captured):
    """Gemini 3.x 400s on thinkingBudget, so the schema must not bring it back."""
    llm._generate("x", model="gemini-3.5-flash-lite", schema={"type": "OBJECT"})
    assert captured[0]["json"]["generationConfig"] == {
        "responseMimeType": "application/json", "responseSchema": {"type": "OBJECT"}}


def test_other_calls_are_not_switched_to_json_mode(captured):
    """Only the metadata call changed; the screen's request stays as validated."""
    llm._generate("hello")
    assert set(captured[0]["json"]["generationConfig"]) == {"thinkingConfig"}


def test_an_unparseable_reply_is_quoted_near_the_fault(monkeypatch, capsys):
    """The 2026-10-17 failure logged only "unparseable JSON", so its cause could
    not be read; the log now shows the reply around the error, on one line."""
    # The fault sits past the excerpt's width, so the excerpt must follow it.
    reply = ('{"title": "Ok", "keywords": [' + '"pad", ' * 60 + '"x"], '
             '"cta": "Vote for "plastic crack" now"}')
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: reply)
    llm.get_metadata("q", ["a", "b", "c"])
    out = capsys.readouterr().out
    assert "plastic crack" in out and "fall back" in out
    assert len(out.strip().splitlines()) == 1 and len(out) < 400


def test_a_trailing_comma_no_longer_costs_every_field(monkeypatch, capsys):
    """Measured 2026-10-17 on the sample model, in JSON mode: a pretty-printed
    reply ending `"cta": "...",\\n}`. Strict parsing dropped title, keywords,
    vote and host lines over one comma. The repair is logged, not silent."""
    reply = ('{\n  "title": "T",\n  "keywords": ["a", "b",],\n  "setup": "S",\n'
             '  "reactions": ["r1", "r2", "r3"],\n  "cta": "Which one, YOU?",\n}')
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: reply)
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert (meta.title, meta.keywords, meta.cta) == ("T", ["a", "b"], "Which one, YOU?")
    assert meta.failure == ""
    assert "trailing comma" in capsys.readouterr().out


def test_a_comma_inside_a_line_is_never_touched(monkeypatch):
    """The repair only runs on a reply that failed, and only drops a comma
    that sits before a closing bracket."""
    reply = '{"title": "Wait, really?", "keywords": ["x"], "cta": "One, two, three",}'
    monkeypatch.setattr(llm, "_generate", lambda *a, **k: reply)
    meta = llm.get_metadata("q", ["a", "b", "c"])
    assert (meta.title, meta.cta) == ("Wait, really?", "One, two, three")


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


def test_an_all_lower_case_title_ships_in_sentence_case():
    """PRD §0 #14: the no-capitals arm came back with no capitals at all."""
    cases = {
        "how to get jehovah's witnesses to leave you alone":
            "How to get jehovah's witnesses to leave you alone",
        "which celeb aged best without trying? you decide.":
            "Which celeb aged best without trying? You decide.",
        "is your 'dream' career on this list?": "Is your 'dream' career on this list?",
        "(not) a dumb question?": "(Not) a dumb question?",
        "if they lose: what do you think happens next?":
            "If they lose: what do you think happens next?",
        "what i'd tell my younger self... and why": "What I'd tell my younger self... and why",
        "3 answers about wi-fi": "3 answers about wi-fi",
        "i.e. what now?": "I.e. what now?",
        "what is a.i. doing? you tell me": "What is a.i. doing? You tell me",
        "wi-fi or i/o?": "Wi-fi or i/o?",
    }
    for generated, shipped in cases.items():
        r = llm.resolve_title(generated, style="B", fallback="Raw?")
        assert (r.title, r.style, r.ok) == (shipped, "B", True)


def test_a_title_with_any_capital_is_left_as_the_model_wrote_it():
    """Capitals are #14's variable: only a title with none at all is touched,
    so neither arm's capitals are added to or taken away."""
    for title in ("Who's YOUR hero?", "when did Reddit go bad for you?",
                  "3 Answers: Is Baby Formula REALLY Necessary?", "i love NYC"):
        assert llm.resolve_title(title, style="A", fallback="Raw?").title == title


def test_the_raw_fallback_is_never_recased():
    """A raw Reddit question is its own cohort (title_source=raw), including
    when the reply cleans to nothing, which must not claim a style either."""
    for generated in (None, "'"):
        r = llm.resolve_title(generated, style="B", fallback="why do cats knead?")
        assert (r.title, r.style, r.ok) == ("why do cats knead?", "", False)


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


def test_the_upload_log_names_who_answered_the_metadata_call():
    """A Groq title for a failed Gemini must not count unmarked in the title
    reads (#10, #14): the run logs the source the call returned."""
    import inspect
    from src import log, run
    assert "meta_source" in log.FIELDS
    assert '"meta_source": meta.source' in inspect.getsource(run.main)


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


def _metadata_prompt(monkeypatch, vote_rule):
    seen = []
    monkeypatch.setattr(llm.config, "HOUSE_VOTE_RULE", vote_rule)
    monkeypatch.setattr(llm.config, "COMMENTARY", False)  # bet 1's fuller step supersedes it
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda prompt, *a, **k: seen.append(prompt) or '{"cta": "c"}')
    llm.get_metadata("What is the scariest story?", ["one", "two", "three"])
    return seen[0]


def test_the_closing_line_is_unchanged_until_the_owner_sets_a_vote_rule(monkeypatch):
    """Bet 1 ships dormant (PRD R3.2): with no rule the prompt is today's,
    byte for byte, so merging it changes no video."""
    prompt = _metadata_prompt(monkeypatch, None)
    # Main's closing-line instruction as it stood before bet 1, copied rather
    # than read from llm, so an edit to llm._CTA_ASK fails here too.
    assert """
3. CTA — a spoken outro line of AT MOST 12 words asking viewers to comment
   their own answer to this specific question. Direct, punchy, conversational.
   No hashtags, no emoji, no profanity.

Return ONLY a JSON object""" in prompt
    assert "vote" not in prompt


def test_a_vote_rule_cannot_ship_under_the_current_format_version():
    """Switching the vote on changes every video, so its uploads must log under
    a new FORMAT_VERSION or bet 1's read cannot tell them from v7's. Bet 1 is
    the next release, so v7 is the version it must not share."""
    if config.HOUSE_VOTE_RULE:
        assert config.FORMAT_VERSION != "v7"


def test_a_vote_rule_turns_the_closing_line_into_the_hosts_vote(monkeypatch):
    """YouTube pays for the creator's own perspective and refuses AI advice on
    health, law, money or politics (PRD R3.6), so the vote judges and never
    advises, and it is written from the owner's rule, not a generic tone."""
    rule = "the answer that's true for the most people, not the funniest"
    prompt = _metadata_prompt(monkeypatch, rule)
    assert rule in prompt
    assert "never advise" in prompt and "never a stock phrase" in prompt
    # Its first real run voted "because autism affects socialization most"
    # (2026-10-07): a claim about a condition, not a judgement of an answer.
    assert "never on the person" in prompt
    assert "asking viewers to comment" not in prompt
    # The line it replaces is capped at 12 words. Held equal, so bet 1's read
    # is not confounded by length the way v7's was (PRD §4, 2026-10-07).
    assert "AT MOST 12 words" in prompt


# ------------------------------------------------ Groq route (#62's follow-up)


class FakeGroqResponse(FakeResponse):
    def json(self):
        return {"choices": [{"message": {"content": self._text}}]}


@pytest.fixture
def groq(monkeypatch):
    calls = []

    def fake_post(url, **kw):
        calls.append({"url": url, **kw})
        return FakeGroqResponse()

    monkeypatch.setattr(llm.requests, "post", fake_post)
    monkeypatch.setattr(config, "AI_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "groq-test-key")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    return calls


def test_gemini_answers_unless_the_route_is_switched():
    """A key alone must change nothing: the switch is flipped only after the
    screen replay and a sample pass on the new route. A fresh process, so
    reloading config cannot leak into other tests."""
    import os, subprocess, sys
    env = dict(os.environ, GROQ_API_KEY="present")
    # Empty, as an unset Actions variable arrives. It also keeps a local .env's
    # AI_PROVIDER out, since config only fills variables that are not set.
    env["AI_PROVIDER"] = ""
    out = subprocess.run([sys.executable, "-c", "from src import config; print(config.AI_PROVIDER)"],
                         env=env, capture_output=True, text=True, check=True,
                         cwd=str(config.ROOT))
    assert out.stdout.strip() == "gemini"


def test_a_groq_reply_with_no_content_reads_as_empty_text(groq, monkeypatch):
    """Callers regex the reply outside their try block, so None would crash
    post selection rather than fall back."""
    class Empty(FakeGroqResponse):
        def json(self):
            return {"choices": [{"message": {"content": None}}]}
    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: Empty())
    assert llm._generate("hello") == ""


def test_groq_route_sends_every_call_there_with_the_key_in_a_header(groq):
    assert llm._generate("hello") == "a title"
    assert llm._generate("slate", model=config.SLATE_MODEL) == "a title"
    assert all(c["url"].startswith("https://api.groq.com/") for c in groq)
    body = groq[0]["json"]
    assert body["model"] == config.GROQ_MODEL
    assert body["messages"] == [{"role": "user", "content": "hello"}]
    assert "groq-test-key" not in json.dumps(body)
    assert groq[0]["headers"]["Authorization"] == "Bearer groq-test-key"


def test_groq_reasons_harder_only_where_the_caller_asked(groq):
    llm._generate("title")
    llm._generate("screen", thinking_budget=512)
    assert [c["json"]["reasoning_effort"] for c in groq] == ["low", "medium"]


def test_metadata_parses_on_the_groq_route(groq, monkeypatch):
    monkeypatch.setattr(llm.requests, "post",
                        lambda url, **kw: FakeGroqResponse(GOOD_JSON))
    m = llm.get_metadata("What is it?", ["a", "b", "c"])
    assert m.title == "A Great Title" and m.cta and m.keywords == ["one", "two"]


def _groq_429(retry_after=None):
    resp = FakeGroqResponse(status=429)
    resp.headers = {} if retry_after is None else {"retry-after": retry_after}
    return llm.requests.HTTPError("429", response=resp)


def test_groq_waits_out_its_per_minute_cap_once(groq, monkeypatch):
    """Groq's free tier caps tokens per minute (8K), so the screen and the
    metadata call back to back can hit a 429 a few seconds' wait clears.
    Gemini's 429 is the daily cap and stays unretried."""
    calls, waits = [], []

    def limited(*a, **k):
        calls.append(1)
        if len(calls) == 1:
            raise _groq_429("7")
        return GOOD_JSON

    monkeypatch.setattr(llm, "_generate", limited)
    monkeypatch.setattr(llm.time, "sleep", waits.append)
    assert llm.get_metadata("q", ["a", "b", "c"]).title == "A Great Title"
    assert waits == [7.0]


@pytest.mark.parametrize("retry_after", [None, "3600", "soon"])
def test_groq_does_not_retry_its_daily_cap_or_an_unreadable_wait(groq, monkeypatch, retry_after):
    calls = []

    def capped(*a, **k):
        calls.append(1)
        raise _groq_429(retry_after)

    monkeypatch.setattr(llm, "_generate", capped)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    assert llm.get_metadata("q", ["a", "b", "c"]).failure == "http_429"
    assert len(calls) == 1


def test_a_switched_on_route_with_no_key_falls_back_to_gemini(groq, monkeypatch):
    """A missing key used to raise KeyError inside every call, so uploads
    would ship raw titles with nothing in the log saying why."""
    monkeypatch.delenv("GROQ_API_KEY")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-test-key")
    sent = []
    monkeypatch.setattr(llm.requests, "post",
                        lambda url, **kw: sent.append(url) or FakeResponse(GOOD_JSON))
    m = llm.get_metadata("What is it?", ["a", "b", "c"])
    assert m.title == "A Great Title" and m.source == "gemini"
    assert "generativelanguage.googleapis.com" in sent[0]


def test_the_log_records_which_route_answered(groq, monkeypatch):
    """screen_source and the metadata source said "gemini" whatever answered,
    so the log could not show the switch, or a fallback from it."""
    from src import screen
    monkeypatch.setattr(llm.requests, "post",
                        lambda url, **kw: FakeGroqResponse(GOOD_JSON))
    assert llm.get_metadata("What is it?", ["a", "b", "c"]).source == "groq"
    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: FakeGroqResponse(
        '{"post_risk": "none", "topic": "other", "unsafe_comments": []}'))
    assert screen.screen("What is it?", ["a", "b"]).source == "groq"
    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: FakeGroqResponse("no json"))
    assert llm.get_metadata("What is it?", ["a", "b", "c"]).source == "groq"


def test_a_gemini_429_is_not_retried_even_when_it_names_a_short_wait(monkeypatch):
    """Gemini's 429 is the daily cap whatever its header says; only Groq's
    per-minute cap earns the wait."""
    calls = []

    def capped(*a, **k):
        calls.append(1)
        resp = FakeResponse(status=429)
        resp.headers = {"retry-after": "7"}
        raise llm.requests.HTTPError("429", response=resp)

    monkeypatch.setattr(llm, "_generate", capped)
    monkeypatch.setattr(llm.time, "sleep", lambda s: pytest.fail("slept on a Gemini 429"))
    assert llm.get_metadata("q", ["a", "b", "c"]).failure == "http_429"
    assert len(calls) == 1


def test_a_groq_key_alone_leaves_every_call_on_gemini(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "groq-test-key")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-test-key")
    sent = []
    monkeypatch.setattr(llm.requests, "post",
                        lambda url, **kw: sent.append(url) or FakeResponse(GOOD_JSON))
    assert llm.get_metadata("What is it?", ["a", "b", "c"]).source == "gemini"
    assert sent and all("generativelanguage.googleapis.com" in u for u in sent)


def _caps_prompt(monkeypatch, caps):
    seen = []
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda prompt, *a, **k: seen.append(prompt) or '{"title": "t"}')
    llm.get_metadata("What is the scariest story?", ["one", "two", "three"],
                     style="B", caps=caps)
    return seen[0]


def test_each_capitals_arm_asks_for_its_own_title_and_both_ban_shock_phrases(monkeypatch):
    """PRD §0 #14: the arms differ only in the capitals line."""
    on, off = _caps_prompt(monkeypatch, True), _caps_prompt(monkeypatch, False)
    assert "exactly ONE word in capitals" in on and "Do not write any word in capitals" not in on
    assert "Do not write any word in capitals" in off and "exactly ONE word" not in off
    assert "Never use shock phrases" in on and "Never use shock phrases" in off
    assert on.replace(llm._CAPS_GUIDANCE[True], "") == off.replace(llm._CAPS_GUIDANCE[False], "")


def test_no_arm_leaves_the_title_prompt_as_it_was(monkeypatch):
    """Callers that pass no arm (the release gate's old call, tests) see no new line."""
    prompt = _caps_prompt(monkeypatch, None)
    assert "capitals" not in prompt and "shock phrases" not in prompt


def test_the_capitals_coin_lands_both_ways():
    import random
    arms = {llm.title_caps_arm(random.Random(seed)) for seed in range(20)}
    assert arms == {True, False}


# PRD §0 #13: Groq answers the metadata call when Gemini fails, behind the
# screen's switch (config.GROQ_FALLBACK) and on its terms.

def _gemini_429(monkeypatch, groq_reply=None, groq_error=None):
    """Gemini's call fails on the daily cap; Groq answers `groq_reply` or
    raises `groq_error`. Returns the prompts Groq was sent."""
    quota = llm.requests.Response()
    quota.status_code = 429
    monkeypatch.setattr(llm, "_generate",
                        _raises(llm.requests.HTTPError("429", response=quota)))
    sent = []

    def groq(prompt, reasoning=False):
        sent.append(prompt)
        if groq_error:
            raise groq_error
        return groq_reply
    monkeypatch.setattr(llm, "_generate_groq", groq)
    monkeypatch.setattr(config, "AI_PROVIDER", "gemini")
    monkeypatch.setattr(config, "DRY_RUN", False)
    monkeypatch.setattr(config, "GROQ_FALLBACK", True)
    monkeypatch.setenv("GROQ_API_KEY", "k")
    return sent


def test_groq_answers_the_metadata_when_gemini_fails(monkeypatch):
    sent = _gemini_429(monkeypatch, groq_reply=GOOD_JSON)
    meta = llm.get_metadata("q", ["a"])
    assert len(sent) == 1
    assert meta.title and meta.keywords and meta.cta
    # Gemini's failure stays, so the log shows why Groq ran.
    assert (meta.source, meta.failure) == ("groq_fallback", "http_429")


def test_off_keyless_dry_or_already_on_groq_the_fields_fall_back_as_before(monkeypatch):
    for case in ("off", "keyless", "dry", "groq"):
        sent = _gemini_429(monkeypatch, groq_reply=GOOD_JSON)
        if case == "off":
            monkeypatch.setattr(config, "GROQ_FALLBACK", False)
        elif case == "keyless":
            monkeypatch.delenv("GROQ_API_KEY")
        elif case == "dry":
            monkeypatch.setattr(config, "DRY_RUN", True)
        else:
            monkeypatch.setattr(config, "AI_PROVIDER", "groq")
        meta = llm.get_metadata("q", ["a"])
        assert sent == [], case
        assert (meta.title, meta.source, meta.failure) == (None, "error", "http_429"), case


def test_a_groq_miss_is_named_after_geminis(monkeypatch):
    _gemini_429(monkeypatch, groq_error=llm.requests.ReadTimeout())
    meta = llm.get_metadata("q", ["a"])
    assert (meta.title, meta.source, meta.failure) == (None, "error", "http_429;groq_timeout")

    _gemini_429(monkeypatch, groq_reply="no json here")
    meta = llm.get_metadata("q", ["a"])
    assert (meta.title, meta.source, meta.failure) == (None, "groq_fallback", "http_429;groq_no_json")

    _gemini_429(monkeypatch, groq_reply="{not: json}")
    assert llm.get_metadata("q", ["a"]).failure == "http_429;groq_bad_json"


def test_the_rescue_waits_out_groqs_minute_cap_once(monkeypatch, capsys):
    """Review, 2026-10-12: with Gemini spent, the screens and the metadata
    call reach Groq in one minute, over its 8K-token cap."""
    _gemini_429(monkeypatch)
    replies = [_groq_429("7"), GOOD_JSON]
    slept = []

    def groq(prompt, reasoning=False):
        r = replies.pop(0)
        if isinstance(r, Exception):
            raise r
        return r
    monkeypatch.setattr(llm, "_generate_groq", groq)
    monkeypatch.setattr(llm.time, "sleep", slept.append)
    meta = llm.get_metadata("q", ["a"])
    assert slept == [7.0]
    assert (meta.source, meta.failure) == ("groq_fallback", "http_429")
    # The success leaves no failure label, so the wait is printed instead.
    assert "per-minute cap" in capsys.readouterr().out


def _groq_503(retry_after):
    resp = FakeGroqResponse(status=503)
    resp.headers = {"retry-after": retry_after}
    return llm.requests.HTTPError("503", response=resp)


def test_the_rescue_never_waits_twice_on_a_daily_cap_or_off_a_429(monkeypatch):
    cases = ((["7", "7"], [7.0], 2, "groq_http_429"), (["3600"], [], 1, "groq_http_429"),
             ([None], [], 1, "groq_http_429"), (["503:7"], [], 1, "groq_http_503"))
    for headers, sleeps, calls, groq_failure in cases:
        _gemini_429(monkeypatch)
        errors = [_groq_503(h[4:]) if h and h.startswith("503:") else _groq_429(h)
                  for h in headers]
        slept, sent = [], []

        def groq(prompt, reasoning=False):
            sent.append(prompt)
            raise errors.pop(0)
        monkeypatch.setattr(llm, "_generate_groq", groq)
        monkeypatch.setattr(llm.time, "sleep", slept.append)
        meta = llm.get_metadata("q", ["a"])
        assert (slept, len(sent)) == (sleeps, calls), headers
        assert meta.failure == f"http_429;{groq_failure}", headers
