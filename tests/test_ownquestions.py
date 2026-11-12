"""The own-questions source (src/ownquestions.py, PLAN C16)."""
import json
import re

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
    assert refused == [(GOOD["question"], "skip_unsafe_takes")]
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


def test_the_metadata_call_never_passes_takes_off_as_peoples_answers(monkeypatch):
    sent = []
    monkeypatch.setattr(llm, "generate_retrying", lambda prompt, **kw: sent.append(prompt) or "{}")
    for style in "ABC":
        monkeypatch.setattr(config, "SOURCE", "own")
        llm.get_metadata(GOOD["question"], GOOD["takes"], style=style, caps=style == "B")
        monkeypatch.setattr(config, "SOURCE", "reddit")
        llm.get_metadata(GOOD["question"], GOOD["takes"], style=style, caps=style == "B")
    own, reddit = sent[0::2], sent[1::2]
    for p in own:
        body, ban = p.rsplit("Never present", 1)
        assert "Reddit" not in body and "People" not in body and "discussion" not in body
        assert not re.search(r"\banswers?\b", body.replace("not real people's answers", ""), re.I)
        assert "never mention Reddit" in ban
    assert all("Reddit question" in p for p in reddit)
    assert "People Reveal" in reddit[2] and "never mention Reddit" not in reddit[2]


def test_only_our_instructions_are_reworded_never_the_question_or_its_takes(monkeypatch):
    # 11-11 review: the answer->take swap reached the question ("the best take
    # to small talk") and the swap's own "not real people's answers".
    sent = []
    monkeypatch.setattr(llm, "generate_retrying", lambda prompt, **kw: sent.append(prompt) or "{}")
    monkeypatch.setattr(config, "SOURCE", "own")
    question = "What is the best answer to small talk in this discussion?"
    takes = ["Answers should be short.", "Ask a question back.", "Answer honestly, then move on."]
    for style in "ABC":
        llm.get_metadata(question, takes, style=style, caps=style == "B")
    for p in sent:
        assert question in p and all(t in p for t in takes)
        assert "not real people's answers:" in p and "\x00" not in p
        body = p.rsplit("Never present", 1)[0]
        for kept in (question, *takes, "not real people's answers"):
            body = body.replace(kept, "")
        assert not re.search(r"\banswers?\b", body, re.I) and "discussion" not in body


def test_a_demoted_post_risk_is_logged_as_on_the_reddit_path(monkeypatch):
    _routes(monkeypatch, GOOD, OTHER)
    logged = []
    ownquestions.select_post(
        screener=lambda q, t: ScreenResult("pass", topic="other", source="gemini",
                                           demoted="named_wrongdoing"),
        on_verdict=lambda q, r, a: logged.append((q, a)))
    assert logged == [(GOOD["question"], "demoted_post_risk")]


@pytest.mark.parametrize("field, value", [
    ("title", "3 People Reveal Their Seat Etiquette"), ("title", "Reddit settles the recline debate"),
    ("title", "Strangers confess their worst flight habit"), ("cta", "Tell r/AskReddit which take wins.")])
def test_a_field_naming_reddit_or_peoples_answers_falls_back(monkeypatch, field, value):
    reply = {"title": "3 Takes On Reclining Your Seat", "keywords": ["reclining seat", "reddit ama"],
             "cta": "Which take do you pick? Tell us below."}
    reply[field] = value
    monkeypatch.setattr(llm, "generate_retrying", lambda prompt, **kw: json.dumps(reply))
    monkeypatch.setattr(config, "SOURCE", "own")
    meta = llm.get_metadata(GOOD["question"], GOOD["takes"], style="C", caps=False)
    assert getattr(meta, field) is None and meta.keywords == ["reclining seat"]
    other = "cta" if field == "title" else "title"
    assert getattr(meta, other) == reply[other]
    monkeypatch.setattr(config, "SOURCE", "reddit")   # the show itself names Reddit freely
    meta = llm.get_metadata(GOOD["question"], GOOD["takes"], style="C", caps=False)
    assert getattr(meta, field) and "reddit ama" in meta.keywords


@pytest.mark.parametrize("title, dropped", [
    ("What Your Coffee Order Reveals About You", False), ("The Most Revealing Morning Habit", False),
    ("Gender Reveal Parties: Worth It?", False), ("Are R/C cars a waste of money?", False),
    ("Do people still recline their seats?", False), ("3 Strangers On Reclining", True),
    ("Real People Answer: Recline Or Not?", True), ("What people told us about reclining", True),
    # 11-12 merge review: a question about people, or a list of them, is not their answers
    ("Why do people say sorry so much?", False), ("Why Do People Tell White Lies?", False),
    ("3 People You Meet at Every Wedding", False), ("Why don't people say thanks anymore?", False),
    ("3 People Reveal Their Seat Etiquette", True), ("5 Strangers Share Their Recline Rules", True),
    ("People Share Their Worst Flight", True), ("Redditors weigh in on reclining", True),
    ("Post yours on /r/tifu", True), ("Why do so many people say sorry?", False),
    ("Why don’t people say thanks anymore?", False), ("Can people tell when you're lying?", False),
    ("3 People's Hot Takes On Reclining", True), ("3 Strangers Weigh In", True),
    ("We Asked 100 People About Reclining", True), ("People’s Answers On Reclining", True),
    ("3 People, 3 Takes On Reclining", True), ("Strangers Vote: Recline?", True)])
def test_the_title_check_catches_people_telling_not_ordinary_words(monkeypatch, title, dropped):
    reply = {"title": title, "keywords": ["recline"], "cta": "Which take do you pick?"}
    monkeypatch.setattr(llm, "generate_retrying", lambda prompt, **kw: json.dumps(reply))
    monkeypatch.setattr(config, "SOURCE", "own")
    meta = llm.get_metadata(GOOD["question"], GOOD["takes"], style="C", caps=False)
    assert (meta.title is None) == dropped
