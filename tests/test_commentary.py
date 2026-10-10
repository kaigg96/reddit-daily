"""Bet 1's first step (#70, PRD R3.2): a host's commentary is half the video.

YouTube refuses "readings of other materials" and pays for "reaction videos
where you comment". The owner approved a host who sets up the question, reacts
to each of the top two answers and casts a vote, inside the one metadata call.
It ships switched off; these hold what must be true when it is switched on.
"""

import json

import pytest

from src import config, content, llm, log, run, screen
from src.video import Segment

POST_ANSWERS = ["Waiting tables, ten hours on your feet.",
                "Lifeguarding: boredom, then thirty seconds that matter.",
                "Teaching kindergarten."]

HOST = {"title": "t", "keywords": ["k"],
        "setup": "Everyone thinks they could do these. Let's hear it.",
        "reactions": ["Ten hours of smiling is the hard part.",
                      "Boredom then terror. No thanks."],
        "cta": "My hand goes up for lifeguarding. Which gets your vote?"}


@pytest.fixture
def commentary_on(monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY", True)


def _metadata(monkeypatch, reply):
    seen = []
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda prompt, *a, **k: seen.append(prompt) or reply)
    meta = llm.get_metadata("What job looks easy but is brutal?", POST_ANSWERS)
    return meta, seen[0]


# --- the call -----------------------------------------------------------------

def test_off_asks_for_nothing_new_and_returns_no_host(monkeypatch):
    meta, prompt = _metadata(monkeypatch, json.dumps(HOST))
    assert "COMMENTARY" not in prompt and "reactions" not in prompt
    assert '3. "Teaching kindergarten."' in prompt
    assert meta.commentary is None and meta.cta == HOST["cta"]


def test_on_asks_for_the_hosts_lines_on_the_top_two_answers_only(monkeypatch, commentary_on):
    """The answers stay the top two in vote order (owner, 2026-08-23; #70)."""
    meta, prompt = _metadata(monkeypatch, json.dumps(HOST))
    assert '1. "Waiting tables' in prompt and '2. "Lifeguarding' in prompt
    assert "Teaching kindergarten" not in prompt
    assert "exactly 2 lines" in prompt and '"reactions"' in prompt
    assert meta.commentary == llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])


def test_the_prompt_carries_each_rule_the_drafts_needed(monkeypatch, commentary_on):
    """Each failure the 2026-10-09 drafts showed has a rule (PRD §4)."""
    _, prompt = _metadata(monkeypatch, "{}")
    for rule in ("never a stock phrase",                  # YouTube's template rule
                 "Never state a fact, statistic or\n     diagnosis",  # a wrong artery
                 "Judge, never advise",                   # AI personas advising
                 "never by its number",                   # numbers never heard
                 "never on the person",                   # the autism vote
                 "never about the harm",                  # off-tone on grim threads
                 "make sense heard once",                 # one nonsense line
                 "show\n   of hands"):                    # the owner's stance (#70)
        assert rule in prompt, rule


@pytest.mark.parametrize("broken", [
    {"reactions": ["only one"]},
    {"reactions": "not a list"},
    {"setup": ""},
    {"cta": None},
    {"reactions": ["fine", "  "]},
])
def test_any_missing_line_falls_back_to_todays_video(monkeypatch, commentary_on, broken):
    """All or nothing: a half-set would leave an answer unreacted to."""
    meta, _ = _metadata(monkeypatch, json.dumps({**HOST, **broken}))
    assert meta.commentary is None


def test_commentary_cannot_ship_under_the_current_format_version():
    """It changes every video, so its uploads must log under a new version."""
    if config.COMMENTARY:
        assert config.FORMAT_VERSION != "v7"


# --- the narration ------------------------------------------------------------

class _Post:
    title = "What job looks easy but is brutal?"
    comments = POST_ANSWERS


def _synth(name, text, kind, speaker=None):
    seg = Segment(kind=kind, text=text, audio_path=name, marks=[])
    seg.speaker = speaker
    return seg


def test_host_lines_follow_their_answers_in_the_hosts_voice():
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    assert [s.kind for s in segs] == ["title", "host", "comment", "host",
                                      "comment", "host", "host"]
    assert [s.text for s in segs][2:6] == [POST_ANSWERS[0], HOST["reactions"][0],
                                          POST_ANSWERS[1], HOST["reactions"][1]]
    assert all(s.speaker == "Stephen" for s in segs if s.kind == "host")
    assert all(s.speaker is None for s in segs if s.kind != "host")


def test_without_host_lines_the_narration_is_todays():
    segs = run.build_segments(_Post, "cta", None, _synth, "Stephen")
    assert [s.kind for s in segs] == ["title", "comment", "comment", "comment", "outro"]
    assert all(s.speaker is None for s in segs)


def test_the_duration_guard_drops_a_reaction_with_its_answer():
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    dropped = run.drop_last_answer(segs)
    assert dropped.text == POST_ANSWERS[1]
    assert HOST["reactions"][1] not in [s.text for s in segs]
    assert segs[-1].text == HOST["cta"]


def test_own_words_share_counts_only_the_hosts_lines():
    segs = [Segment("title", "a" * 20, "", []), Segment("host", "b" * 30, "", []),
            Segment("comment", "c" * 20, "", []), Segment("host", "d" * 30, "", [])]
    assert run.own_words_share(segs) == "0.60"


def test_the_log_keeps_bet_1s_done_when():
    assert {"commentary_ok", "own_words_share"} <= set(log.FIELDS)


# --- selection ----------------------------------------------------------------

@pytest.mark.parametrize("title,topic,medical", [
    ("ER workers, what stories involve chiropractors?", "", True),
    ("Doctors of Reddit, what is the dumbest thing you've seen?", "", True),
    ("If my car dies on a busy highway, can I call 911?", "", True),
    ("What were you doing when the power went out?", "", False),
    ("What job looks easy but is brutal?", "", False),
    ("What is something your body just does?", "health-body", True),
])
def test_medical_threads_are_recognised(title, topic, medical):
    assert content.is_medical(title, topic) is medical


class _FakePost:
    def __init__(self, title):
        self.title, self.over_18, self.shortlink = title, False, "https://redd.it/x"


class _FakeReddit:
    def __init__(self, titles):
        self.titles = titles

    def subreddit(self, name):
        titles = self.titles

        class S:
            def top(self, time_filter, limit):
                return [_FakePost(t) for t in titles]
        return S()


@pytest.fixture
def selection(monkeypatch):
    monkeypatch.setattr(content, "_comment_pool", lambda post, n: ["a", "b", "c", "d"])
    monkeypatch.setattr(content.profanity, "contains_profanity", lambda t: False)


TITLES = ["Nurses, what's the worst shift you ever worked?",
          "What is something your body just does?",
          "What job looks easy but is brutal?"]


def _screener(question, comments):
    topic = "health-body" if "body" in question else "money-work"
    return screen.ScreenResult("pass", topic=topic, source="gemini")


def test_with_commentary_on_medical_threads_are_skipped_and_logged(
        monkeypatch, selection, commentary_on):
    seen, verdicts = [], []

    def screener(q, c):
        seen.append(q)
        return _screener(q, c)

    post = content.select_post(_FakeReddit(TITLES), "", screener=screener,
                               on_verdict=lambda t, r, a: verdicts.append((t, a, r.category)))
    assert post.title == TITLES[2] and post.candidate_rank == 3
    # The title check runs before the screen, so it spends no request.
    assert TITLES[0] not in seen
    assert verdicts == [(TITLES[0], "skip_medical", "medical"),
                        (TITLES[1], "skip_medical", "medical")]


def test_with_commentary_off_selection_is_unchanged(selection):
    post = content.select_post(_FakeReddit(TITLES), "", screener=_screener)
    assert post.title == TITLES[0]
