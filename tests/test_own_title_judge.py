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
    assert len(calls) == 2
    assert "3 Takes On Tipping" in calls[1] and "Which gets your vote?" in calls[1]


@pytest.mark.parametrize("judge, cta_ships", [
    ('{"title": "yes", "cta": "no"}', True),      # judged as passing the takes off
    ('{"cta": "no"}', True),                       # no verdict for it
    ('{"title": "maybe", "cta": "no"}', True),     # anything but a plain no
    ('["no", "no"]', False),                       # wrong shape
    ('not json', False),
    (RuntimeError("503"), False),                  # the request failed
])
def test_anything_but_a_plain_no_refuses_the_line(own, judge, cta_ships):
    own(judge)
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title is None
    assert m.cta == ("Which gets your vote?" if cta_ships else None)


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
    out = llm._own_judged({"title": None, "cta": "Which gets your vote?", "keywords": []})
    assert out["cta"] == "Which gets your vote?" and out["title"] is None
    assert len(prompts) == 1 and "title:" not in prompts[0]


def test_nothing_left_to_judge_makes_no_request(monkeypatch):
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError("asked")))
    assert llm._own_judged({"title": None, "cta": ""}) == {"title": None, "cta": ""}


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


def test_a_judge_no_route_answers_refuses_both(own, monkeypatch):
    own(RuntimeError("503"))
    monkeypatch.setattr(config, "DRY_RUN", False)
    monkeypatch.setattr(llm, "_rescue_metadata", lambda prompt, prior: (None, "gemini", prior))
    m = llm.get_metadata("How much should you tip?", ["a", "b", "c"])
    assert m.title is None and m.cta is None
