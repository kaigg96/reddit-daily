"""The own-questions source (src/ownquestions.py, PLAN C16)."""
import json

import pytest

from src import config, llm, ownquestions
from src.screen import ScreenResult

GOOD = {"question": "Is it rude to recline your seat on a plane?",
        "takes": ["Recline away, the button is there for a reason.",
                  "Only on night flights, never during meals.",
                  "Never; the space behind you is not yours."]}
OTHER = {"question": "Should you tip at a self-checkout counter?",
         "takes": ["Never, nobody served you.", "Only if staff helped.", "Tip screens are a trap."]}


def test_a_usable_episode_is_parsed_from_a_wrapped_reply():
    reply = "Here you go: " + json.dumps(GOOD)
    assert ownquestions.parse(reply) == (GOOD["question"], GOOD["takes"])


def test_an_unusable_episode_is_refused_rather_than_narrated():
    def episode(**kw):
        return json.dumps({**GOOD, **kw})
    for reply in ("no json here", "{broken", None, episode(question="No question mark"),
                  episode(takes=GOOD["takes"][:2]),
                  episode(takes=[GOOD["takes"][0]] * 3),
                  episode(takes=GOOD["takes"][:2] + ["x" * (config.MAX_COMMENT_LENGTH + 1)]),
                  episode(takes=GOOD["takes"][:2] + ["My boss once read my medical notes."]),
                  episode(takes=GOOD["takes"][:2] + ["When I was a kid we never reclined."]),
                  episode(takes=GOOD["takes"][:2] + ["Coffee fuels my focus every morning."]),
                  episode(takes=GOOD["takes"][:2] + ["Tea, because I'm calmer on it."]),
                  episode(takes=GOOD["takes"][:2] + ["As a parent, never recline."]),
                  episode(takes=GOOD["takes"][:2] + ["Growing up, nobody reclined."]),
                  episode(takes=GOOD["takes"][:2] + ["Last week a stranger reclined into me."])):
        assert ownquestions.parse(reply) is None, reply


def _routes(monkeypatch, upload, groq):
    asked = {}
    monkeypatch.setattr(config, "GROQ_FALLBACK", True)

    def fake(prompt, **kw):
        asked.update(kw)
        return json.dumps(upload)
    monkeypatch.setattr(llm, "generate_retrying", fake)
    monkeypatch.setattr(llm, "_generate_groq", lambda prompt: json.dumps(groq))
    return asked


def test_the_upload_model_writes_it_and_no_one_is_credited(monkeypatch):
    asked = _routes(monkeypatch, GOOD, OTHER)
    post = ownquestions.select_post("an older question?")
    assert asked == {}   # the sample model in a dry run, MODEL in an upload
    assert post.title == GOOD["question"] and list(post.comments) == GOOD["takes"]
    assert not any(c.author for c in post.comments) and not post.subreddit


def test_a_refused_reply_gets_one_free_retry_then_fails_loudly(monkeypatch):
    persona = {**GOOD, "takes": GOOD["takes"][:2] + ["As a parent, never."]}
    _routes(monkeypatch, persona, GOOD)
    assert ownquestions.select_post().title == GOOD["question"]
    _routes(monkeypatch, persona, persona)
    with pytest.raises(RuntimeError):
        ownquestions.select_post()


def test_any_shipped_question_is_refused_not_only_the_last(monkeypatch):
    _routes(monkeypatch, GOOD, OTHER)
    post = ownquestions.select_post("last one?", uploaded={GOOD["question"].upper()})
    assert post.title == OTHER["question"]
    with pytest.raises(RuntimeError):
        ownquestions.select_post(OTHER["question"], uploaded={GOOD["question"]})


def test_the_screen_runs_and_a_skip_or_a_dropped_take_refuses_the_episode(monkeypatch):
    _routes(monkeypatch, GOOD, OTHER)
    seen, refused = [], []

    def screener(question, takes):
        seen.append((question, list(takes)))
        if question == GOOD["question"]:
            return ScreenResult("pass", unsafe={1}, source="gemini")
        return ScreenResult("pass", topic="money-work", source="gemini")
    post = ownquestions.select_post(screener=screener,
                                    on_verdict=lambda q, r, a: refused.append((q, a)))
    assert seen == [(GOOD["question"], GOOD["takes"]), (OTHER["question"], OTHER["takes"])]
    assert refused == [(GOOD["question"], "skip_post")]
    assert post.title == OTHER["question"] and post.topic == "money-work"
    assert post.screen_source == "gemini"
    with pytest.raises(RuntimeError):
        ownquestions.select_post(screener=lambda q, t: ScreenResult("skip_post", category="x"))


def test_a_failed_route_falls_to_the_other(monkeypatch):
    def boom(prompt, **kw):
        raise TimeoutError
    monkeypatch.setattr(llm, "generate_retrying", boom)
    monkeypatch.setattr(llm, "_generate_groq", lambda prompt: json.dumps(GOOD))
    monkeypatch.setattr(config, "GROQ_FALLBACK", True)
    assert ownquestions.select_post().title == GOOD["question"]
    monkeypatch.setattr(config, "GROQ_FALLBACK", False)   # off, as every call
    with pytest.raises(RuntimeError):
        ownquestions.select_post()


def test_swearing_or_an_emoji_refuses_an_episode():
    for bad in ("Recline away, damn the person behind.", "Recline away \U0001F600"):
        reply = json.dumps({**GOOD, "takes": GOOD["takes"][:2] + [bad]})
        assert ownquestions.parse(reply) is None, bad


def test_the_source_is_reddit_unless_switched_and_an_unknown_one_fails(monkeypatch):
    import importlib
    monkeypatch.delenv("SAMPLE", raising=False)
    try:
        for value, want in (("", "reddit"), ("reddit", "reddit"), (" Own ", "own")):
            monkeypatch.setenv("SOURCE", value)
            assert importlib.reload(config).SOURCE == want
        assert config.ANSWER_LABEL == "TAKE"
        monkeypatch.setenv("SOURCE", "stackexchange")
        with pytest.raises(SystemExit):
            importlib.reload(config)
    finally:
        monkeypatch.delenv("SOURCE", raising=False)
        importlib.reload(config)
    assert config.SOURCE == "reddit" and config.ANSWER_LABEL == "ANSWER"


def test_our_own_question_credits_no_one_and_names_no_subreddit():
    from src.run import upload_text
    desc, tags = upload_text("", GOOD["question"], GOOD["takes"], "", ["planes"])
    assert "Reddit" not in desc and "u/" not in desc and "#Shorts" in desc
    assert all(t in desc for t in GOOD["takes"]) and tags == ["Shorts", "planes"]
