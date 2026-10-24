"""scripts/tag_trial.py spends live requests: its caps must hold before any call."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import scripts.tag_trial as tt
from src import llm


@pytest.fixture
def no_calls(monkeypatch):
    def refuse(*a, **k):
        raise AssertionError("a request was made")
    monkeypatch.setattr(llm, "_generate", refuse)
    monkeypatch.setattr(llm, "_generate_groq", refuse)


@pytest.mark.parametrize("argv", [["--help"], ["--model", "upload"],
                                  ["--model", "upload", "--posts", "1,2,3,4"],
                                  ["--model", "sample", "--posts", "0"]])
def test_it_refuses_before_spending(no_calls, argv):
    with pytest.raises(SystemExit):
        tt.main(argv)


def test_every_post_has_three_answers():
    assert len(tt.POSTS) == 11 and all(len(a) == 3 for _, a in tt.POSTS)


@pytest.mark.parametrize("setup, words", [("blurt", "blurt out the moment a friend asked you"),
                                          ("specific", "only this question could get")])
def test_a_setup_wording_reaches_the_prompt(monkeypatch, setup, words):
    from src import config
    monkeypatch.setattr(llm, "_TAG_EDITS", list(llm._TAG_EDITS))
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", True)
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_VERDICT"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL"):
        monkeypatch.setattr(config, name, getattr(config, name))
    shipped = llm._commentary_ask(3)
    tt.setup_model("sample", setup=setup)
    ask = llm._commentary_ask(3)
    assert words in ask and words not in shipped
    # Only the setup changes: every reaction rule is as shipped.
    assert ask.split('"reactions":', 1)[1] == shipped.split('"reactions":', 1)[1]


def test_the_spoken_reactions_change_the_reactions_only(monkeypatch):
    from src import config
    monkeypatch.setattr(llm, "_TAG_EDITS", list(llm._TAG_EDITS))
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", True)
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_VERDICT"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL"):
        monkeypatch.setattr(config, name, getattr(config, name))
    shipped = llm._commentary_ask(3)
    tt.setup_model("sample", reactions="spoken")
    ask = llm._commentary_ask(3)
    assert "never an adjective and a noun" in ask and "adjective and a noun" not in shipped
    assert ask.split('"reactions":', 1)[0] == shipped.split('"reactions":', 1)[0]
    assert ask.split('"cta":', 1)[1] == shipped.split('"cta":', 1)[1]


def test_the_ungraded_reactions_drop_agreement_and_change_the_reactions_only(monkeypatch):
    from src import config
    monkeypatch.setattr(llm, "_TAG_EDITS", list(llm._TAG_EDITS))
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", True)
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_VERDICT"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL"):
        monkeypatch.setattr(config, name, getattr(config, name))
    shipped = llm._commentary_ask(3)
    tt.setup_model("sample", reactions="ungraded")
    ask = llm._commentary_ask(3)
    assert "agreement" in shipped and "agreement" not in ask
    assert '"Spot on"' in ask and '"Spot on"' not in shipped
    assert ask.split('"reactions":', 1)[0] == shipped.split('"reactions":', 1)[0]
    assert ask.split('"cta":', 1)[1] == shipped.split('"cta":', 1)[1]


def test_groq_without_its_key_refuses_rather_than_spend_gemini(no_calls, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(SystemExit, match="GROQ_API_KEY"):
        tt.main(["--model", "groq", "--posts", "1"])


def test_a_trial_prints_the_setup_as_written_and_whether_it_would_ship(monkeypatch, capsys):
    """Through the real metadata call, so the gate's bypass is what is tested."""
    import json
    from src import config
    for name in ("FALLBACK_MODEL", "_reads_as_reaction", "_VERDICT", "_TAG_EDITS"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL"):
        monkeypatch.setattr(config, name, getattr(config, name))
    for name, on in (("COMMENTARY", True), ("HOST_TEXT", True), ("HOST_TAGS", True),
                     ("COMMENTARY_ANSWERS", 3)):
        monkeypatch.setattr(config, name, on)
    reply = json.dumps({"title": "A title", "keywords": ["a", "b", "c"], "setup": "The mystery",
                        "reactions": ["Oof.", "Spot on", "Wait, what?"],
                        "cta": "My hand goes up for the first. Which gets your vote?"})
    monkeypatch.setattr(llm, "generate_retrying", lambda prompt, *a, **k: reply)
    tt.main(["--model", "sample", "--posts", "1"])
    row = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert row["setup"] == "The mystery" and row["setup_ships"] is False
    assert row["reactions"] == ["Oof.", "Spot on", "Wait, what?"]
    assert row["reactions_ship"] == [True, False, True]
