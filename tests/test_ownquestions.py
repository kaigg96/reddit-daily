"""The own-questions sample source (src/ownquestions.py, PLAN C16)."""
import json

from src import config, llm, ownquestions
from src.llm import Commentary

GOOD = {"question": "Is it rude to recline your seat on a plane?",
        "takes": ["Recline away, the button is there for a reason.",
                  "Only on night flights, never during meals.",
                  "Never; the space behind you is not yours."]}


def test_a_usable_episode_is_parsed_from_a_wrapped_reply():
    reply = "Here you go: " + json.dumps(GOOD)
    assert ownquestions.parse(reply) == (GOOD["question"], GOOD["takes"])


def test_an_unusable_episode_is_refused_rather_than_narrated():
    def episode(**kw):
        return json.dumps({**GOOD, **kw})
    for reply in ("no json here", "{broken", episode(question="No question mark"),
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


def test_the_upload_model_writes_it_and_no_one_is_credited(monkeypatch):
    asked = {}

    def fake(prompt, **kw):
        asked.update(kw)
        return json.dumps(GOOD)
    monkeypatch.setattr(llm, "generate_retrying", fake)
    monkeypatch.setattr(llm, "_generate_groq", lambda prompt: 1 / 0)
    post = ownquestions.select_post("an older question?")
    assert asked == {"model": llm.MODEL, "schema": ownquestions.SCHEMA}
    assert post.title == GOOD["question"] and list(post.comments) == GOOD["takes"]
    assert not any(c.author for c in post.comments)


def test_a_refused_reply_gets_one_free_retry_then_fails_loudly(monkeypatch):
    persona = json.dumps({**GOOD, "takes": GOOD["takes"][:2] + ["As a parent, never."]})
    monkeypatch.setattr(llm, "generate_retrying", lambda prompt, **kw: persona)
    monkeypatch.setattr(llm, "_generate_groq", lambda prompt: json.dumps(GOOD))
    assert ownquestions.select_post().title == GOOD["question"]
    monkeypatch.setattr(llm, "_generate_groq", lambda prompt: persona)
    try:
        ownquestions.select_post()
    except RuntimeError:
        return
    raise AssertionError("an episode with a persona was narrated")


def test_with_no_host_lines_the_note_still_names_the_takes():
    host = ownquestions.as_host(None)
    assert host.setup == ownquestions.OWN_SETUP and host.reactions == ["", "", ""]
    assert not host.verdict


def test_the_host_names_its_takes_and_reacts_to_none():
    host = ownquestions.as_host(Commentary("Oh no", ["Oof", "Ha", "Wait"], "Take two wins."))
    assert host.setup == ownquestions.OWN_SETUP
    assert host.reactions == ["", "", ""] and host.verdict == "Take two wins."
