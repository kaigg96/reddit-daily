"""The Stack Exchange sample source (src/stackexchange.py, PLAN C16)."""
from src import config, llm, stackexchange


def test_answers_become_plain_text():
    body = "<p>Push back &amp; <b>pad</b> the estimate.</p>\n<ul><li>Say no</li></ul>"
    assert stackexchange._plain(body) == "Push back & pad the estimate. Say no"


def test_three_short_sentences_are_kept(monkeypatch):
    monkeypatch.setattr(llm, "_generate_groq", lambda prompt: 'Sure: ["One.", " Two. ", "Three."]')
    assert stackexchange.condense("Q?", ["a", "b", "c"]) == ["One.", "Two.", "Three."]


def test_an_unusable_reply_is_refused_rather_than_narrated(monkeypatch):
    for reply in ("no json here", '["only", "two"]', '["a", "b", 3]', "[broken",
                  '["' + "x" * (config.MAX_COMMENT_LENGTH + 1) + '", "b", "c"]'):
        monkeypatch.setattr(llm, "_generate_groq", lambda prompt, r=reply: r)
        assert stackexchange.condense("Q?", ["a", "b", "c"]) is None, reply
