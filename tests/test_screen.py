"""Tests for the suppression screen's two-tier taxonomy (PRD R4.6).

The point of these is the cost asymmetry: skipping a post throws away the
top-ranked candidate of the day, dropping an answer costs almost nothing. The
2026-08-30 evidence correction found the screen was spending slots on
categories whose evidence had been retracted, so "this category can never skip
a post" needs to be a property of the code, not of prompt wording.
"""

import json

import pytest

from src import content, screen


class FakePost:
    def __init__(self, title):
        self.title = title
        self.over_18 = False
        self.shortlink = f"https://redd.it/{title[:6]}"


def gemini(monkeypatch, payload):
    """Make the screen's one Gemini call return `payload` verbatim."""
    monkeypatch.setattr(screen, "_generate_screened", lambda prompt: json.dumps(payload))


# --- tier enforcement -------------------------------------------------------

@pytest.mark.parametrize("category", screen.DROP_ONLY_CATEGORIES)
def test_drop_only_category_never_skips_the_post(monkeypatch, category):
    gemini(monkeypatch, {"post_risk": category, "reason": "invites medical harm detail",
                         "unsafe_comments": [], "topic": "dark-morbid"})
    r = screen.screen("Doctors of Reddit, what symptom terrifies you?", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.demoted == category
    assert r.reason  # the model's rationale survives onto the audit row


@pytest.mark.parametrize("category", screen.SKIP_CATEGORIES)
def test_skip_category_still_skips_the_post(monkeypatch, category):
    gemini(monkeypatch, {"post_risk": category, "reason": "why",
                         "unsafe_comments": [], "topic": "other"})
    r = screen.screen("some question", ["a", "b", "c"])
    assert r.verdict == "skip_post"
    assert r.category == category


def test_demoted_post_still_drops_its_unsafe_answers(monkeypatch):
    gemini(monkeypatch, {"post_risk": "graphic_harm", "reason": "gore in answer 2",
                         "unsafe_comments": [2], "topic": "dark-morbid"})
    r = screen.screen("q", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.unsafe == {1}


def test_unknown_category_is_ignored(monkeypatch):
    gemini(monkeypatch, {"post_risk": "vibes_off", "reason": "", "unsafe_comments": [],
                         "topic": "other"})
    r = screen.screen("q", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.demoted == ""


# --- the specific false positives that prompted the retier -------------------

@pytest.mark.parametrize("question", [
    "Doctors/nurses of Reddit, what's a symptom patients brush off that actually terrifies you?",
    "Bartenders of Reddit, what was a \"cut off\" gone wrong?",
    "ER workers, what stories do you have involving chiropractic patients?",
])
def test_audited_false_positives_reach_selection(monkeypatch, question):
    """Each of these was skipped live under a retracted-evidence category."""
    gemini(monkeypatch, {"post_risk": "graphic_harm", "reason": "harm detail",
                         "unsafe_comments": [], "topic": "dark-morbid"})
    assert screen.screen(question, ["a", "b", "c"]).verdict == "pass"


# --- fail-open backstop -----------------------------------------------------

def test_backstop_graphic_terms_drop_answers_but_keep_the_post():
    r = screen._backstop(
        "ER workers, what stories do you have involving chiropractic patients?",
        ["they had a vertebral artery dissection", "fine answer", "also fine"],
    )
    assert r.verdict == "pass"
    assert r.unsafe == {0}


def test_backstop_still_skips_sexual_questions():
    r = screen._backstop("What's a sign someone is amazing in bed?", ["a", "b", "c"])
    assert r.verdict == "skip_post"
    assert r.source == "backstop"


def test_gemini_failure_falls_through_to_backstop(monkeypatch):
    def boom(prompt):
        raise RuntimeError("API down")
    monkeypatch.setattr(screen, "_generate_screened", boom)
    r = screen.screen("a perfectly ordinary question", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.source == "backstop"


# --- audit trail ------------------------------------------------------------

def test_demoted_verdict_is_recorded_once_with_its_category(monkeypatch):
    """A demotion must reach screen_log.csv, or the override is invisible."""
    seen = []
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: ["a", "b", "c", "d"])
    monkeypatch.setattr(content.profanity, "contains_profanity", lambda t: False)

    class FakeReddit:
        def subreddit(self, name):
            class S:
                def top(self, time_filter, limit):
                    return [FakePost("Bartenders, what was a cut off gone wrong?")]
            return S()

    def screener(question, comments):
        return screen.ScreenResult("pass", topic="dark-morbid", demoted="graphic_violence",
                                   reason="invites violent stories")

    post = content.select_post(FakeReddit(), "", screener=screener,
                               on_verdict=lambda t, r, a: seen.append((a, r.demoted)))
    assert post.candidate_rank == 1
    assert seen == [("demoted_post_risk", "graphic_violence")]


# --- transient-failure retry ------------------------------------------------

def test_timeout_is_retried_before_giving_up(monkeypatch):
    """A read timeout used to drop straight to keyword-only screening."""
    import requests
    calls = []

    def flaky(prompt):
        calls.append(1)
        if len(calls) < 3:
            raise requests.Timeout("slow")
        return json.dumps({"post_risk": "none", "reason": "", "unsafe_comments": [],
                           "topic": "other"})

    monkeypatch.setattr(screen.llm, "_generate", flaky)
    monkeypatch.setattr(screen.time, "sleep", lambda s: None)
    r = screen.screen("q", ["a", "b", "c"])
    assert len(calls) == 3
    assert r.source == "gemini"


def test_persistent_timeout_still_fails_open(monkeypatch):
    import requests

    def always_slow(prompt):
        raise requests.Timeout("slow")

    monkeypatch.setattr(screen.llm, "_generate", always_slow)
    monkeypatch.setattr(screen.time, "sleep", lambda s: None)
    r = screen.screen("an ordinary question", ["a", "b", "c"])
    assert r.verdict == "pass"
    assert r.source == "backstop"
