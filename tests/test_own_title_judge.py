"""The own-question show's title judge (PLAN C16; TECH_DEBT's own-title item):
one request after the metadata reply, failing closed, and never on Reddit's path."""
import pytest

from src import config, llm

REPLY = '{"title": "3 Takes On Tipping", "keywords": ["tipping"], "cta": "Which gets your vote?"}'


@pytest.fixture
def own(monkeypatch):
    monkeypatch.setattr(config, "SOURCE", "own")
    calls = []

    def answer(judge):
        def fake(prompt, tries=2, **kw):
            calls.append(prompt)
            if len(calls) == 1:
                return REPLY
            if isinstance(judge, Exception):
                raise judge
            return judge
        monkeypatch.setattr(llm, "generate_retrying", fake)
        return calls
    return answer


def test_a_cleared_title_and_line_ship_on_one_extra_request(own):
    calls = own('{"title": "no", "cta": "no"}')
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title == "3 Takes On Tipping" and m.cta == "Which gets your vote?"
    assert len(calls) == 2 and m.failure == ""
    assert "3 Takes On Tipping" in calls[1] and "Which gets your vote?" in calls[1]


@pytest.mark.parametrize("judge, cta_ships, failure", [
    ('{"title": "yes", "cta": "no"}', True, "own_judge_title"),   # judged as passing the takes off
    ('{"cta": "no"}', True, "own_judge_title"),                    # no verdict for it
    ('{"title": "maybe", "cta": "no"}', True, "own_judge_title"),  # anything but a plain no
    ('{"title": "yes", "cta": "yes"}', False, "own_judge_title;own_judge_cta"),
    ('["no", "no"]', False, "own_judge_no_json;own_judge_unanswered"),   # wrong shape
    ('{"title": no}', False, "own_judge_bad_json;own_judge_unanswered"),
    ('{"title": "no"', False, "own_judge_no_json;own_judge_unanswered"),
    ('not json', False, "own_judge_no_json;own_judge_unanswered"),
    (RuntimeError("503"), False, "own_judge_RuntimeError;own_judge_unanswered"),         # the request failed
])
def test_anything_but_a_plain_no_refuses_the_line(own, monkeypatch, judge, cta_ships, failure):
    """The refusal is logged, so it does not read as a title the model never
    wrote (TECH_DEBT's own-title item, 11-14). No rescue: it has its own tests."""
    monkeypatch.setattr(config, "DRY_RUN", True)
    own(judge)
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title is None
    assert m.cta == ("Which gets your vote?" if cta_ships else None)
    assert m.failure == failure and m.source == "gemini"


def test_reddit_runs_make_no_judge_request(monkeypatch):
    monkeypatch.setattr(config, "SOURCE", "reddit")
    calls = []
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda prompt, tries=2, **kw: calls.append(prompt) or REPLY)
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title == "3 Takes On Tipping"
    assert len(calls) == 1


def test_a_line_the_word_list_dropped_is_not_sent_to_the_judge(monkeypatch):
    prompts = []
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda prompt, tries=2, **kw: prompts.append(prompt) or '{"cta": "no"}')
    out, label = llm._own_judged({"title": None, "cta": "Which gets your vote?", "keywords": []})
    assert label == "" and out["cta"] == "Which gets your vote?" and out["title"] is None
    assert len(prompts) == 1 and "title:" not in prompts[0]


def test_nothing_left_to_judge_makes_no_request(monkeypatch):
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("asked")))
    assert llm._own_judged({"title": None, "cta": ""}) == ({"title": None, "cta": ""}, "")


def test_a_failed_judge_is_rescued_as_the_metadata_call_is(own, monkeypatch):
    """A 503 or a spent cap on the main model: the fallback answers the judge
    too, rather than refusing both lines (fresh review, 11-14)."""
    calls = own(RuntimeError("503"))
    monkeypatch.setattr(config, "DRY_RUN", False)
    rescued = []
    monkeypatch.setattr(llm, "_rescue_metadata",
                        lambda prompt, prior: rescued.append(prompt) or
                        ('{"title": "no", "cta": "no"}', llm.FALLBACK_SOURCE, prior))
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title == "3 Takes On Tipping" and m.cta == "Which gets your vote?"
    assert len(calls) == 2 and len(rescued) == 1 and rescued[0] == calls[1]
    assert m.failure == "own_judge_RuntimeError"   # rescued: kept, nothing refused


def test_a_judge_no_route_answers_refuses_both(own, monkeypatch):
    own(RuntimeError("503"))
    monkeypatch.setattr(config, "DRY_RUN", False)
    tried = []
    monkeypatch.setattr(llm, "_rescue_metadata",
                        lambda prompt, prior: tried.append(prompt) or (None, "gemini", prior))
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title is None and m.cta is None
    assert len(tried) == 1 and m.failure == "own_judge_RuntimeError;own_judge_unanswered"


def test_a_refusal_follows_a_rescued_metadata_reply(monkeypatch):
    """The metadata call's own failure stays first, as `_then` keeps Gemini's."""
    monkeypatch.setattr(config, "SOURCE", "own")
    monkeypatch.setattr(config, "DRY_RUN", False)
    calls = []

    def fake(prompt, tries=2, **kw):
        calls.append(prompt)
        if len(calls) == 1:
            raise RuntimeError("503")
        return '{"title": "yes", "cta": "no"}'
    monkeypatch.setattr(llm, "generate_retrying", fake)
    monkeypatch.setattr(llm, "_rescue_metadata",
                        lambda prompt, prior: (REPLY, llm.FALLBACK_SOURCE, prior))
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.source == llm.FALLBACK_SOURCE and m.title is None
    assert m.cta == "Which gets your vote?" and len(calls) == 2
    assert m.failure == "RuntimeError;own_judge_title"


def test_every_part_of_a_judge_failure_is_named_the_judges(monkeypatch):
    """A rescued metadata reply, then a judge no route answers: each part of the
    judge's chain carries its prefix, so none reads as the metadata call's
    (fresh review, 11-14)."""
    monkeypatch.setattr(config, "SOURCE", "own")
    monkeypatch.setattr(config, "DRY_RUN", False)

    def fail(prompt, tries=2, **kw):
        raise RuntimeError("503")
    monkeypatch.setattr(llm, "generate_retrying", fail)
    replies = iter([(REPLY, llm.FALLBACK_SOURCE, "http_503"),
                    (None, "gemini", "http_429_day;fallback_http_429_day")])
    monkeypatch.setattr(llm, "_rescue_metadata", lambda prompt, prior: next(replies))
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title is None and m.cta is None and m.source == llm.FALLBACK_SOURCE
    assert m.failure == ("http_503;own_judge_http_429_day;own_judge_fallback_http_429_day;"
                         "own_judge_unanswered")


def test_a_rescued_judge_that_refuses_logs_both(monkeypatch):
    monkeypatch.setattr(config, "SOURCE", "own")
    monkeypatch.setattr(config, "DRY_RUN", False)
    calls = []

    def fake(prompt, tries=2, **kw):
        calls.append(prompt)
        if len(calls) == 1:
            return REPLY
        raise RuntimeError("503")
    monkeypatch.setattr(llm, "generate_retrying", fake)
    monkeypatch.setattr(llm, "_rescue_metadata", lambda prompt, prior: (
        '{"title": "no", "cta": "yes"}', llm.FALLBACK_SOURCE, prior))
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title == "3 Takes On Tipping" and m.cta is None
    assert m.failure == "own_judge_RuntimeError;own_judge_cta"
