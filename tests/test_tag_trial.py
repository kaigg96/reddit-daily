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
                                  ["--model", "sample", "--posts", "0"],
                                  ["--model", "upload", "--gemini-model", "gemini-9-pro", "--posts", "1"],
                                  ["--model", "sample", "--gemini-model", "gemini-3.8-flash", "--posts", "1"],
                                  ["--model", "groq", "--thinking", "low", "--posts", "1"],
                                  ["--model", "upload", "--gemini-model", "gemini-3.8-flash",
                                   "--thinking", "minimal", "--posts", "1"]])
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
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_grades"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL",
                 "HOST_REACTIONS"):
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
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_grades"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL",
                 "HOST_REACTIONS"):
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
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_grades"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL",
                 "HOST_REACTIONS"):
        monkeypatch.setattr(config, name, getattr(config, name))
    shipped = llm._commentary_ask(3)
    tt.setup_model("sample", reactions="ungraded")
    ask = llm._commentary_ask(3)
    assert "agreement" in shipped and "agreement" not in ask
    assert '"Spot on"' in ask and '"Spot on"' not in shipped
    assert ask.split('"reactions":', 1)[0] == shipped.split('"reactions":', 1)[0]
    assert ask.split('"cta":', 1)[1] == shipped.split('"cta":', 1)[1]


def test_react_only_drops_agreement_names_no_verdict_and_changes_the_reactions_only(monkeypatch):
    from src import config
    monkeypatch.setattr(llm, "_TAG_EDITS", list(llm._TAG_EDITS))
    monkeypatch.setattr(config, "HOST_TEXT", True)
    monkeypatch.setattr(config, "HOST_TAGS", True)
    for name in ("FALLBACK_MODEL", "generate_retrying", "_reads_as_reaction", "_grades"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL",
                 "HOST_REACTIONS"):
        monkeypatch.setattr(config, name, getattr(config, name))
    shipped = llm._commentary_ask(3)
    tt.setup_model("sample", reactions="react-only")
    ask = llm._commentary_ask(3)
    assert "agreement" in shipped and "agreement" not in ask
    assert "Only the vote takes a side" in ask and '"Spot on"' not in ask
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
    for name in ("FALLBACK_MODEL", "_reads_as_reaction", "_grades", "_TAG_EDITS"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL",
                 "HOST_REACTIONS"):
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


@pytest.mark.parametrize("candidate,thinking", [(c, None) for c in sorted(llm._LOWEST_THINKING)]
                         + [("gemini-3.6-flash", "low")])
def test_a_candidate_is_read_on_its_own_model_at_its_lowest_level(monkeypatch, capsys, candidate,
                                                                    thinking):
    """The successor trial (PRD §4, 11-07): one command per MODEL candidate,
    the request going to that model, timed, at the level it takes."""
    import json
    from src import config
    for name in ("MODEL", "FALLBACK_MODEL", "_reads_as_reaction", "_grades", "_TAG_EDITS",
                 "generate_retrying", "_LOWEST_THINKING"):
        monkeypatch.setattr(llm, name, getattr(llm, name))
    for name in ("GROQ_FALLBACK", "AI_PROVIDER", "DRY_RUN", "METADATA_ON_UPLOAD_MODEL",
                 "HOST_REACTIONS"):
        monkeypatch.setattr(config, name, getattr(config, name))
    sent = []

    class Reply:
        def raise_for_status(self):
            pass

        def json(self):
            text = json.dumps({"title": "A title", "keywords": ["a", "b", "c"], "cta": "c"})
            return {"candidates": [{"content": {"parts": [{"text": text}]}}]}

    monkeypatch.setattr(llm.requests, "post", lambda url, **kw: sent.append((url, kw["json"])) or Reply())
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    level = thinking or llm._LOWEST_THINKING[candidate]
    tt.main(["--model", "upload", "--gemini-model", candidate, "--posts", "1"]
            + (["--thinking", thinking] if thinking else []))
    (url, body), = sent
    assert f"/{candidate}:generateContent" in url
    assert body["generationConfig"]["thinkingConfig"] == {"thinkingLevel": level}
    row = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert row["model"] == candidate and isinstance(row["seconds"], float)


def test_a_blind_sheet_names_no_model_and_its_key_maps_every_row_back(tmp_path, capsys):
    """The successor's tag trial is scored blind (PRD §4, 11-07)."""
    import json
    import scripts.tag_sheet as ts
    runs = []
    for model, tags in (("gemini-3.6-flash", ["Glass costs more", "Plastic crack hurts", ""]),
                        ("gemini-3.8-flash", ["Ouch, lenses", "Wait, what?", "Yikes"])):
        path = tmp_path / f"{model}.jsonl"
        path.write_text("Gemini served x for a y request\n" + json.dumps(
            {"post": 2, "model": model, "seconds": 1.0, "setup": "S", "reactions": tags}) + "\n")
        runs.append(str(path))
    key_path = tmp_path / "key.json"
    ts.main([*runs, "--key", str(key_path), "--seed", "7"])
    sheet = capsys.readouterr().out
    assert "gemini" not in sheet and sheet.count("Tag: ") == 6 and "Tag: (none)" in sheet
    key = json.loads(key_path.read_text())
    assert sorted(r["model"] for r in key["rows"].values()) == ["gemini-3.6-flash"] * 3 + ["gemini-3.8-flash"] * 3
    for n, r in key["rows"].items():
        assert f"{n}. Q: {tt.POSTS[1][0]}" in sheet
        assert tt.POSTS[1][1][r["answer"] - 1] in sheet


def test_two_arms_on_one_model_stay_apart_in_the_key(tmp_path, capsys):
    """A wording or thinking-level trial runs both arms on MODEL (PRD §4,
    11-08), so the key names each row's run, never only its model."""
    import json
    import scripts.tag_sheet as ts
    runs = []
    for arm, tags in (("shipped", ["Glass costs more", "Plastic crack hurts", "Per day cost"]),
                      ("low", ["Ouch, lenses", "Wait, what?", "Yikes"])):
        path = tmp_path / f"{arm}.jsonl"
        path.write_text(json.dumps({"post": 2, "model": "gemini-3.6-flash", "seconds": 1.0,
                                    "setup": "S", "reactions": tags}) + "\n")
        runs.append(str(path))
    key_path = tmp_path / "key.json"
    ts.main([*runs, "--key", str(key_path), "--seed", "7"])
    sheet = capsys.readouterr().out
    assert "shipped" not in sheet and "low.jsonl" not in sheet
    key = json.loads(key_path.read_text())
    by_run = {}
    for r in key["rows"].values():
        by_run.setdefault(r["run"], []).append(r["tag"])
    assert sorted(by_run[runs[1]]) == ["Ouch, lenses", "Wait, what?", "Yikes"]
    assert len(by_run[runs[0]]) == 3
