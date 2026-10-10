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


@pytest.fixture
def commentary_off(monkeypatch):
    monkeypatch.setattr(config, "COMMENTARY", False)


def _metadata(monkeypatch, reply):
    seen = []
    monkeypatch.setattr(llm, "generate_retrying",
                        lambda prompt, *a, **k: seen.append(prompt) or reply)
    meta = llm.get_metadata("What job looks easy but is brutal?", POST_ANSWERS)
    return meta, seen[0]


# --- the call -----------------------------------------------------------------

def test_off_asks_for_nothing_new_and_returns_no_host(monkeypatch, commentary_off):
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
                 "show\n   of hands",                     # the owner's stance (#70)
                 "Never restate the\n     question",        # "Reddit weighs in on ..."
                 "take no side on the issue"):            # a side taken on Israel
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
    # Not "skip_*", which the weekly digest audits as the screen's verdicts.
    assert verdicts == [(TITLES[0], "medical_excluded", "medical"),
                        (TITLES[1], "medical_excluded", "medical")]


def test_with_commentary_off_selection_is_unchanged(selection, commentary_off):
    post = content.select_post(_FakeReddit(TITLES), "", screener=_screener)
    assert post.title == TITLES[0]


def test_title_skips_do_not_use_up_the_screened_candidates(
        monkeypatch, selection, commentary_on):
    """Four medical titles ahead of a fine one must not leave the run postless."""
    titles = [f"Doctors, what is case {i}?" for i in range(config.MAX_SCREENED_CANDIDATES)]
    titles.append("What job looks easy but is brutal?")
    post = content.select_post(_FakeReddit(titles), "", screener=_screener)
    assert post.title == titles[-1] and post.candidate_rank == len(titles)


def test_off_the_screen_cap_is_unchanged(monkeypatch, selection, commentary_off):
    titles = [f"What is case {i}?" for i in range(6)]
    seen = []

    def skip_all(q, c):
        seen.append(q)
        return screen.ScreenResult("skip_post", category="x", source="gemini")
    with pytest.raises(ValueError):
        content.select_post(_FakeReddit(titles), "", screener=skip_all)
    assert len(seen) == config.MAX_SCREENED_CANDIDATES


@pytest.mark.parametrize("field,words", [("setup", 23), ("cta", 23)])
def test_a_line_far_past_its_cap_falls_back(monkeypatch, commentary_on, field, words):
    """Prompt caps alone could push a video past 60s and cost the upload."""
    meta, _ = _metadata(monkeypatch, json.dumps({**HOST, field: "word " * words}))
    assert meta.commentary is None


def test_a_line_a_little_past_its_cap_still_ships(monkeypatch, commentary_on):
    meta, _ = _metadata(monkeypatch, json.dumps({**HOST, "reactions": ["w " * 17, "ok"]}))
    assert meta.commentary is not None


def test_style_c_promises_the_two_answers_read(monkeypatch, commentary_on):
    seen = []
    monkeypatch.setattr(llm, "generate_retrying", lambda p, *a, **k: seen.append(p) or "{}")
    llm.get_metadata("q", POST_ANSWERS, style="C")
    assert '"2 Answers That' in seen[0] and '"3 ' not in seen[0]


def test_a_fallback_never_speaks_the_hosts_vote(commentary_on):
    """With commentary on, the call's "cta" is the vote; after a plain reading
    it is said by nobody about answers nobody argued, so the generic line closes."""
    meta = llm.MetadataResult("t", ["k"], "My hand goes up for X.", "gemini", "", None)
    assert run.closing_line(meta, None) is None


def test_off_the_closing_line_is_the_calls_cta(commentary_off):
    meta = llm.MetadataResult("t", ["k"], "Comment yours!", "gemini", "", None)
    assert run.closing_line(meta, None) == "Comment yours!"


def _too_long_until(n_segments):
    return lambda segs: len(segs) > n_segments


def test_the_guard_drops_the_setup_first():
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    outro = run.fit_to_length(segs, _too_long_until(6), host, _synth)
    assert HOST["setup"] not in [s.text for s in segs]
    assert POST_ANSWERS[1] in [s.text for s in segs] and outro == HOST["cta"]


def test_dropping_an_answer_replaces_the_vote_that_may_name_it():
    host = llm.Commentary(HOST["setup"], HOST["reactions"], HOST["cta"])
    segs = run.build_segments(_Post, host.verdict, host, _synth, "Stephen")
    outro = run.fit_to_length(segs, _too_long_until(4), host, _synth)
    assert [s.kind for s in segs] == ["title", "comment", "host", "outro"]
    assert outro == config.OUTRO_TEXT == segs[-1].text


def test_off_the_guard_drops_only_the_last_answer():
    segs = run.build_segments(_Post, "cta", None, _synth, "Stephen")
    outro = run.fit_to_length(segs, _too_long_until(4), None, _synth)
    assert [s.text for s in segs][1:3] == POST_ANSWERS[:2] and len(segs) == 4
    assert outro == "cta"
