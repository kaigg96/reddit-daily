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
    assert len(tt.POSTS) == 9 and all(len(a) == 3 for _, a in tt.POSTS)
