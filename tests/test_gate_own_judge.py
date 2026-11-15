"""The release gate reads the own show's title judge (PLAN C16, #90): an
unanswered judge is "could not check", a refusal or junk is a verdict. Its own
file so bet 1's edits to the gate's tests merge without a clash."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import validate_release as vr  # noqa: E402
from src import llm  # noqa: E402
from src.llm import MetadataResult  # noqa: E402


def _metadata(monkeypatch, meta):
    monkeypatch.setattr("src.llm.get_metadata", lambda *a, **k: meta)
    monkeypatch.setattr(llm, "FALLBACK_MODEL", llm.FALLBACK_MODEL)  # restored after
    return vr.check_metadata()


def test_an_unanswered_own_title_judge_is_inconclusive_not_a_fail(monkeypatch):
    """Once the own show is live (#90) the gate runs its path, whose judge
    fails closed; a refusal the judge did give is still a verdict."""
    assert _metadata(monkeypatch, MetadataResult(
        None, ["a", "b", "c"], None, "gemini",
        "own_judge_http_429;own_judge_unanswered")) is None
    assert _metadata(monkeypatch, MetadataResult(
        None, ["a", "b", "c"], None, "gemini",
        "own_judge_title;own_judge_cta")) is False
    assert _metadata(monkeypatch, MetadataResult(          # junk is a broken prompt
        None, ["a", "b", "c"], None, "gemini",
        "own_judge_bad_json;own_judge_unanswered")) is False
