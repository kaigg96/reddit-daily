"""The own-question title judge's one-request check (scripts/judge_own_cases.py):
one request carrying all 17 cases, graded by the judge's own rule."""
import json
import sys

import pytest

sys.path.insert(0, "scripts")
import judge_own_cases as jc  # noqa: E402

from src import llm  # noqa: E402


def _reply(flip=()):
    return json.dumps({str(i): ("yes" if refuse != (i in flip) else "no")
                       for i, (_, refuse) in enumerate(jc.CASES, 1)})


def test_the_prompt_is_the_judges_with_every_case():
    p = jc.prompt()
    assert p.startswith(llm._OWN_JUDGE[:60])
    assert all(json.dumps(line, ensure_ascii=False) in p for line, _ in jc.CASES)
    assert f'"{len(jc.CASES)}": "yes" or "no"' in p and len(jc.CASES) == 26


@pytest.mark.parametrize("raw, code", [
    (_reply(), 0), (_reply(flip={2}), 1), (_reply(flip={15}), 1),
    ("not json", 2), ('["no"]', 2), ('{"1": no}', 2)])
def test_one_request_and_every_case_must_be_right(monkeypatch, capsys, raw, code):
    sent = []
    monkeypatch.setattr(llm, "_generate", lambda prompt, model=None, **kw:
                        sent.append(model) or raw)
    assert jc.main([]) == code
    assert sent == [llm.SAMPLE_MODEL]
    if code == 1:
        assert "WRONG" in capsys.readouterr().out


def test_a_missing_or_hedged_verdict_counts_as_a_refusal():
    rows = jc.grade(json.dumps({"12": "maybe"}))
    by_line = {line: right for right, _, line in rows}
    assert by_line["Redditors Reveal Their Worst Date"]          # refused, as it should be
    assert not by_line["Should two people split the bill?"]     # "maybe" refuses an ordinary one


def test_a_failed_request_prints_its_label_not_its_message(monkeypatch, capsys):
    def fail(prompt, model=None, **kw):
        raise RuntimeError("https://example/?key=SECRET")
    monkeypatch.setattr(llm, "_generate", fail)
    assert jc.main(["--model", "gemini-3.6-flash"]) == 2
    out = capsys.readouterr().out
    assert "SECRET" not in out and "RuntimeError" in out
