"""Tests for the suppression screen's two-tier taxonomy (PRD R4.6).

The point of these is the cost asymmetry: skipping a post throws away the
top-ranked candidate of the day, dropping an answer costs almost nothing. The
2026-08-30 evidence correction found the screen was spending slots on
categories whose evidence had been retracted, so "this category can never skip
a post" needs to be a property of the code, not of prompt wording.
"""

import json

import pytest

from src import content, screen


class FakePost:
    def __init__(self, title):
        self.title = title
        self.over_18 = False
        self.shortlink = f"https://redd.it/{title[:6]}"


def gemini(monkeypatch, payload):
    """Make the screen's one Gemini call return `payload` verbatim."""
    monkeypatch.setattr(screen, "_generate_screened", lambda prompt: json.dumps(payload))


# --- tier enforcement -------------------------------------------------------

@pytest.mark.parametrize("category", screen.DROP_ONLY_CATEGORIES)
def test_drop_only_category_never_skips_the_post(monkeypatch, category):
    gemini(monkeypatch, {"post_risk": category, "reason": "invites medical harm detail",
                         "unsafe_comments": [], "topic": "dark-morbid"})
    r = screen.screen("Doctors of Reddit, what symptom terrifies you?", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.demoted == category
    assert r.reason  # the model's rationale survives onto the audit row


@pytest.mark.parametrize("category", screen.SKIP_CATEGORIES)
def test_skip_category_still_skips_the_post(monkeypatch, category):
    gemini(monkeypatch, {"post_risk": category, "reason": "why",
                         "unsafe_comments": [], "topic": "other"})
    r = screen.screen("some question", ["a", "b", "c"])
    assert r.verdict == "skip_post"
    assert r.category == category


def test_demoted_post_still_drops_its_unsafe_answers(monkeypatch):
    gemini(monkeypatch, {"post_risk": "graphic_harm", "reason": "gore in answer 2",
                         "unsafe_comments": [2], "topic": "dark-morbid"})
    r = screen.screen("q", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.unsafe == {1}


def test_unknown_category_is_ignored(monkeypatch):
    gemini(monkeypatch, {"post_risk": "vibes_off", "reason": "", "unsafe_comments": [],
                         "topic": "other"})
    r = screen.screen("q", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.demoted == ""


# --- the specific false positives that prompted the retier -------------------

@pytest.mark.parametrize("question", [
    "Doctors/nurses of Reddit, what's a symptom patients brush off that actually terrifies you?",
    "Bartenders of Reddit, what was a \"cut off\" gone wrong?",
    "ER workers, what stories do you have involving chiropractic patients?",
])
def test_audited_false_positives_reach_selection(monkeypatch, question):
    """Each of these was skipped live under a retracted-evidence category."""
    gemini(monkeypatch, {"post_risk": "graphic_harm", "reason": "harm detail",
                         "unsafe_comments": [], "topic": "dark-morbid"})
    assert screen.screen(question, ["a", "b", "c"]).verdict == "pass"


# --- fail-open backstop -----------------------------------------------------

def test_backstop_graphic_terms_drop_answers_but_keep_the_post():
    r = screen._backstop(
        "ER workers, what stories do you have involving chiropractic patients?",
        ["they had a vertebral artery dissection", "fine answer", "also fine"],
    )
    assert r.verdict == "pass"
    assert r.unsafe == {0}


def test_backstop_still_skips_sexual_questions():
    r = screen._backstop("What's a sign someone is amazing in bed?", ["a", "b", "c"])
    assert r.verdict == "skip_post"
    assert r.source == "backstop"


def test_gemini_failure_falls_through_to_backstop(monkeypatch):
    def boom(prompt, **kw):   # both models, so the fallback misses too
        raise RuntimeError("API down")
    monkeypatch.setattr(screen, "_generate_screened", boom)
    r = screen.screen("a perfectly ordinary question", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.source == "backstop"


# --- audit trail ------------------------------------------------------------

def test_demoted_verdict_is_recorded_once_with_its_category(monkeypatch):
    """A demotion must reach screen_log.csv, or the override is invisible."""
    seen = []
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: ["a", "b", "c", "d"])
    monkeypatch.setattr(content.profanity, "contains_profanity", lambda t: False)

    class FakeReddit:
        def subreddit(self, name):
            class S:
                def top(self, time_filter, limit):
                    return [FakePost("Bartenders, what was a cut off gone wrong?")]
            return S()

    def screener(question, comments):
        return screen.ScreenResult("pass", topic="dark-morbid", demoted="graphic_violence",
                                   reason="invites violent stories")

    post = content.select_post(FakeReddit(), "", screener=screener,
                               on_verdict=lambda t, r, a: seen.append((a, r.demoted)))
    assert post.candidate_rank == 1
    assert seen == [("demoted_post_risk", "graphic_violence")]


# --- transient-failure retry ------------------------------------------------

def test_timeout_is_retried_once(monkeypatch):
    """A read timeout used to drop straight to keyword-only screening. It is
    retried once — not more, because the daily request budget is tight."""
    import requests
    calls = []

    def flaky(prompt, thinking_budget=0):
        calls.append(1)
        if len(calls) < 2:
            raise requests.Timeout("slow")
        return json.dumps({"post_risk": "none", "reason": "", "unsafe_comments": [],
                           "topic": "other"})

    monkeypatch.setattr(screen.llm, "_generate", flaky)
    monkeypatch.setattr(screen.llm.time, "sleep", lambda s: None)
    r = screen.screen("q", ["a", "b", "c"])
    assert len(calls) == 2
    assert r.source == "gemini"


def test_persistent_timeout_still_fails_open(monkeypatch):
    import requests

    def always_slow(prompt, thinking_budget=0, model=None):
        raise requests.Timeout("slow")

    monkeypatch.setattr(screen.config, "DRY_RUN", False)
    monkeypatch.setattr(screen.llm, "_generate", always_slow)
    monkeypatch.setattr(screen.llm.time, "sleep", lambda s: None)
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.source == "backstop"
    assert r.failure == "timeout;fallback_timeout"


def _http_error(code):
    import requests
    resp = requests.Response()
    resp.status_code = code
    return requests.HTTPError(response=resp)


def _main_model_fails(monkeypatch, code=503, fallback_reply=None, fallback_code=None):
    """The main model always raises `code`; the fallback model answers
    `fallback_reply`, or raises `fallback_code`. Returns the models called."""
    calls = []

    def fake(prompt, thinking_budget=0, model=None):
        calls.append(model)
        if model is None:
            raise _http_error(code)
        if fallback_code:
            raise _http_error(fallback_code)
        return fallback_reply

    monkeypatch.setattr(screen.config, "DRY_RUN", False)
    monkeypatch.setattr(screen.llm, "_generate", fake)
    monkeypatch.setattr(screen.llm.time, "sleep", lambda s: None)
    return calls


def test_an_overload_falls_back_to_the_other_model(monkeypatch):
    """The 2026-10-09 06:21 upload went to the keyword backstop on two 503s.
    The free tier is counted per model, so the other one usually answers."""
    calls = _main_model_fails(monkeypatch, 503, fallback_reply=json.dumps(
        {"post_risk": "none", "reason": "", "unsafe_comments": [2], "topic": "other"}))
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert calls == [None, None, screen.FALLBACK_MODEL]   # one retry, then one fallback
    assert r.source == "gemini_fallback"   # the log tells it from a main-model answer
    assert r.failure == "http_503"         # and says why it ran
    assert r.unsafe == {1}
    assert r.topic == "other"


def test_the_fallback_model_can_still_skip_a_post(monkeypatch):
    _main_model_fails(monkeypatch, 429, fallback_reply=json.dumps(
        {"post_risk": "sexual_suggestive", "reason": "r", "unsafe_comments": [],
         "topic": "sex-adjacent"}))
    r = screen.screen("q", ["a", "b", "c"])
    assert r.verdict == "skip_post"
    assert r.source == "gemini_fallback"
    assert r.failure == "http_429"


def test_both_models_failing_reaches_the_backstop_once(monkeypatch):
    calls = _main_model_fails(monkeypatch, 503, fallback_code=429)
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert calls == [None, None, screen.FALLBACK_MODEL]   # the fallback is never retried
    assert r.source == "backstop"
    assert r.failure == "http_503;fallback_http_429"   # the main model's reason first


def test_a_fallback_reply_without_json_reaches_the_backstop(monkeypatch):
    _main_model_fails(monkeypatch, 503, fallback_reply="Looks fine to me.")
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert r.source == "backstop"
    assert r.failure == "http_503;fallback_no_json"


@pytest.mark.parametrize("unsafe", [None, 2, "2", ["²", 2.0, True, "x"]])
def test_a_malformed_unsafe_list_never_raises(monkeypatch, unsafe):
    """`"unsafe_comments": null` raised TypeError out of screen(), which costs
    the slot its upload. Junk entries are ignored; the verdict still stands."""
    gemini(monkeypatch, {"post_risk": "none", "reason": "", "unsafe_comments": unsafe,
                         "topic": "other"})
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.unsafe == set()
    assert r.topic == "other"


def test_the_fallback_request_sends_no_thinking_budget(monkeypatch):
    """Gemini 3.x answers thinkingBudget with HTTP 400 (2026-09-26), so the
    fallback, unlike the main model, must go out without one."""
    sent = []

    class Resp:
        def __init__(self, status, payload=None):
            self.status_code, self._payload = status, payload

        def raise_for_status(self):
            if self.status_code >= 400:
                raise screen.llm.requests.HTTPError(response=self)

        def json(self):
            return self._payload

    def post(url, headers, json, timeout):
        sent.append((url, json))
        if screen.llm.MODEL in url:
            return Resp(503)
        text = '{"post_risk": "none", "reason": "", "unsafe_comments": [], "topic": "other"}'
        return Resp(200, {"candidates": [{"content": {"parts": [{"text": text}]}}]})

    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setattr(screen.config, "DRY_RUN", False)
    monkeypatch.setattr(screen.llm.requests, "post", post)
    monkeypatch.setattr(screen.llm.time, "sleep", lambda s: None)
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert r.source == "gemini_fallback"
    main, fallback = sent[0][1], sent[-1][1]
    assert screen.FALLBACK_MODEL in sent[-1][0]
    assert "thinkingConfig" in main["generationConfig"]   # the main model still reasons
    assert "generationConfig" not in fallback


@pytest.mark.parametrize("setting", ["dry_run", "groq", "disabled"])
def test_no_fallback_where_it_would_test_or_send_the_wrong_thing(monkeypatch, setting):
    """A dry run is already on the fallback model; Groq exists to keep posts
    off Gemini; the replay switches it off because it tests the main model."""
    calls = _main_model_fails(monkeypatch, 503, fallback_reply="{}")
    if setting == "dry_run":
        monkeypatch.setattr(screen.config, "DRY_RUN", True)
    elif setting == "groq":
        monkeypatch.setattr(screen.llm, "provider", lambda: "groq")
    else:
        monkeypatch.setattr(screen, "FALLBACK_MODEL", None)
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert calls == [None, None]   # the main model and its retry, nothing else
    assert r.source == "backstop"
    assert r.failure == "http_503"


def test_screen_source_reaches_the_upload_log(monkeypatch):
    """A run that fell back to the backstop must be distinguishable afterwards."""
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: ["a", "b", "c", "d"])
    monkeypatch.setattr(content.profanity, "contains_profanity", lambda t: False)

    class FakeReddit:
        def subreddit(self, name):
            class S:
                def top(self, time_filter, limit):
                    return [FakePost("An ordinary question?")]
            return S()

    def degraded(question, comments):
        return screen.ScreenResult("pass", source="backstop", failure="http_503")

    post = content.select_post(FakeReddit(), "", screener=degraded)
    assert post.screen_source == "backstop"
    assert post.screen_failure == "http_503"   # why, not just that
    assert post.topic == ""


def test_a_reply_without_json_is_a_failure_not_a_pass(monkeypatch):
    """A prose-only reply used to parse as {} -- risk none, logged as gemini --
    so the post shipped unscreened while the log said it had been screened."""
    monkeypatch.setattr(screen, "_generate_screened", lambda prompt: "Looks fine to me.")
    r = screen.screen("What's a sign someone is amazing in bed?", ["a", "b", "c"])
    assert r.source == "backstop"
    assert r.failure == "no_json"     # same label as the metadata call's
    assert r.verdict == "skip_post"   # the backstop still gets its say


def test_a_malformed_json_reply_is_a_failure_not_a_pass(monkeypatch):
    monkeypatch.setattr(screen, "_generate_screened", lambda prompt: '{"post_risk": none,}')
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert r.source == "backstop"
    assert r.failure == "bad_json"


def test_429_is_not_retried(monkeypatch):
    """A 429 here is a daily-budget exhaustion that persists for hours. Retrying
    cannot succeed and spends requests the title/keyword/CTA calls still need."""
    import requests
    calls = []

    def limited(prompt, thinking_budget=0, model=None):
        calls.append(model)
        resp = requests.Response()
        resp.status_code = 429
        raise requests.HTTPError(response=resp)

    monkeypatch.setattr(screen.config, "DRY_RUN", False)
    monkeypatch.setattr(screen.llm, "_generate", limited)
    monkeypatch.setattr(screen.llm.time, "sleep", lambda s: None)
    r = screen.screen("q", ["a", "b", "c"])
    assert calls.count(None) == 1   # one attempt on the main model, no retry
    assert r.source == "backstop"   # still fails open
    assert r.failure.startswith("http_429")  # the daily cap, distinguishable from a timeout


def test_the_screen_asks_for_reasoning(monkeypatch):
    """The screen must NOT run with thinking disabled.

    Pins a live regression. Disabling thinking for every Gemini call on
    2026-09-19 fixed a real latency problem for titles, and quietly broke the
    screen: it began passing a sexual_suggestive question backed by one of the
    two confirmed zeroed uploads. Caught by the CI gate on 2026-09-20, after
    it had already reached main.

    Titles, keywords and CTAs are transformations and are fine at zero. The
    screen is a judgment call and is not.
    """
    seen = {}

    def fake(prompt, thinking_budget=0):
        seen["budget"] = thinking_budget
        return json.dumps({"post_risk": "none", "reason": "",
                           "unsafe_comments": [], "topic": "other"})

    monkeypatch.setattr(screen.llm, "_generate", fake)
    screen.screen("A harmless question?", ["a", "b", "c", "d"])

    assert seen["budget"] > 0, "the screen must request reasoning tokens"


def test_prompt_generalizes_sexual_suggestive_beyond_one_example():
    """Pins a live regression found 2026-09-20, same day as the fix above.

    Restoring reasoning tokens was not enough on its own: a live replay still
    missed replay_screen.py's paraphrase ("...dangerously flirty?") while
    correctly catching the literal in-prompt example ("...excellent in bed?").
    One example doesn't generalize a category — the paraphrase now needs to be
    an explicit calibration example too, not just a held-out test case.
    """
    assert "dangerously flirty" in screen._PROMPT


# --- author credit (PLAN C15) -------------------------------------------------

def test_comment_pool_keeps_each_author_and_leaves_unprintable_names_out():
    """Reddit's terms ask for each user's name. Names are untrusted input:
    a deleted account or a profane name is left uncredited, not printed."""
    from types import SimpleNamespace as NS

    class Comments(list):
        def replace_more(self, limit):
            pass

    who = lambda name: None if name is None else NS(name=name)
    post = NS(comments=Comments([NS(body="first", author=who("alice")),
                                 NS(body="second", author=who(None)),
                                 NS(body="third", author=who("shitlord99")),
                                 NS(body="fourth", author=who("[deleted]"))]))
    pool = content._comment_pool(post, 10)
    assert pool == ["first", "second", "third", "fourth"]
    assert [c.author for c in pool] == ["alice", "", "", ""]


def test_screen_drops_keep_each_author_with_their_answer(monkeypatch):
    """A dropped answer must take its name with it, or credits shift by one."""
    pool = [content.Answer(t, n) for t, n in [("a", "ann"), ("b", "bob"), ("c", "cat"),
                                              ("d", "dan"), ("e", "eve")]]
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: list(pool))
    monkeypatch.setattr(content.profanity, "contains_profanity", lambda t: False)
    monkeypatch.setattr(content.config, "NUM_COMMENTS", 3)

    class FakeReddit:
        def subreddit(self, name):
            class S:
                def top(self, time_filter, limit):
                    p = FakePost("What is a question?")
                    p.author = type("R", (), {"name": "quinn"})()
                    return [p]
            return S()

    def screener(question, comments):
        return screen.ScreenResult("pass", unsafe=[1], category="unsafe_comments")

    post = content.select_post(FakeReddit(), "", screener=screener)
    assert post.comments == ["a", "c", "d"]
    assert [c.author for c in post.comments] == ["ann", "cat", "dan"]
    assert post.author == "quinn"
