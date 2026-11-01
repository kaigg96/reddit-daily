"""Midterm week (2026-11-03): questions about voting are not candidates, since
answers are read word for word and YouTube removes misleading voting claims."""
import datetime

import pytest

from src import config, content

D = datetime.date


def test_voting_questions_are_skipped_through_the_end_date():
    for title in ("Who are you voting for in the midterms?",
                  "What would make you vote for the other party?",
                  "Non-Americans, what do you think of the US election?",
                  "Have you ever been turned away at a polling place?",
                  "Is a mail-in BALLOT safe?",
                  "What time do polls close on Tuesday?",
                  "Should the electoral college go?"):
        assert content._election_week(title, D(2026, 11, 1)), title
        assert content._election_week(title, config.ELECTION_SKIP_UNTIL), title


def test_other_questions_and_later_dates_pass():
    assert not content._election_week("What's a hobby that costs too much?", D(2026, 11, 2))
    # whole words only: "devoted", "pivot", "selection" are not about voting
    assert not content._election_week("What are you devoted to? Pivot or selection?", D(2026, 11, 2))
    after = config.ELECTION_SKIP_UNTIL + datetime.timedelta(days=1)
    assert not content._election_week("Who are you voting for?", after)


def test_select_post_never_picks_a_voting_question(monkeypatch):
    class Post:
        def __init__(self, title):
            self.title, self.over_18, self.shortlink = title, False, "https://redd.it/x"

    class Sub:
        def top(self, time_filter, limit):
            return [Post("Who are you voting for on Tuesday?"), Post("What smell takes you back?")]

    class Reddit:
        def subreddit(self, name):
            return Sub()

    seen = []
    monkeypatch.setattr(content, "_election_week",
                        lambda title, today=None: seen.append(title) or "voting" in title)
    monkeypatch.setattr(content, "_comment_pool", lambda post, limit: ["a", "b", "c", "d"])
    picked = content.select_post(Reddit(), prev_title="")
    assert picked.title == "What smell takes you back?"
    assert "Who are you voting for on Tuesday?" in seen


def test_the_live_path_skips_it_and_says_why(monkeypatch, capsys):
    """No stub: the real rule, on today's UTC date, inside select_post."""
    class Post:
        def __init__(self, title):
            self.title, self.over_18, self.shortlink = title, False, "https://redd.it/x"

    class Reddit:
        def subreddit(self, name):
            return self

        def top(self, time_filter, limit):
            return [Post("How long was your wait at the polls?"), Post("What smell takes you back?")]

    class Today(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.datetime(2026, 11, 3, 15, tzinfo=datetime.timezone.utc)

    monkeypatch.setattr(content.datetime, "datetime", Today)
    monkeypatch.setattr(content, "_comment_pool", lambda post, limit: ["a", "b", "c", "d"])
    assert content.select_post(Reddit(), prev_title="").title == "What smell takes you back?"
    assert "About voting in election week, not a candidate: How long" in capsys.readouterr().out


class _Post:
    def __init__(self, title):
        self.title, self.over_18, self.shortlink = title, False, "https://redd.it/x"


class _Day:
    """A subreddit whose day list is `titles`, recording each fetch's depth."""
    def __init__(self, titles):
        self.titles, self.limits = titles, []

    def subreddit(self, name):
        return self

    def top(self, time_filter, limit):
        assert time_filter == "day"
        self.limits.append(limit)
        return [_Post(t) for t in self.titles[:limit]]


def _on_day(monkeypatch, day):
    class Today(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.datetime(day.year, day.month, day.day, 15, tzinfo=datetime.timezone.utc)

    monkeypatch.setattr(content.datetime, "datetime", Today)
    monkeypatch.setattr(content, "_comment_pool", lambda post, limit: ["a", "b", "c", "d"])


def test_an_all_election_top_ten_reads_deeper_instead_of_failing(monkeypatch, capsys):
    _on_day(monkeypatch, D(2026, 11, 4))
    titles = [f"Who did you vote for, part {i}?" for i in range(config.CANDIDATE_LIMIT)]
    titles += ["Who won the election in your town?", "What smell takes you back?"]
    reddit = _Day(titles)
    picked = content.select_post(reddit, prev_title="")
    assert picked.title == "What smell takes you back?"
    assert reddit.limits == [config.CANDIDATE_LIMIT, config.ELECTION_FALLBACK_LIMIT]
    assert "Election week left no candidate in the top 10" in capsys.readouterr().out


def test_the_deeper_read_never_runs_when_the_top_ten_has_a_candidate(monkeypatch):
    _on_day(monkeypatch, D(2026, 11, 4))
    reddit = _Day(["Who did you vote for?", "What hobby costs too much?", "What smell takes you back?"])
    assert content.select_post(reddit, prev_title="").title == "What hobby costs too much?"
    assert reddit.limits == [config.CANDIDATE_LIMIT]


def test_after_election_week_an_empty_list_still_fails_without_reading_deeper(monkeypatch):
    _on_day(monkeypatch, config.ELECTION_SKIP_UNTIL + datetime.timedelta(days=1))
    reddit = _Day(["A" * (config.MAX_TITLE_LENGTH + 1)] * config.CANDIDATE_LIMIT + ["What smell takes you back?"])
    with pytest.raises(ValueError):
        content.select_post(reddit, prev_title="")
    assert reddit.limits == [config.CANDIDATE_LIMIT]


def test_the_deeper_read_still_skips_voting_and_shipped_questions(monkeypatch):
    _on_day(monkeypatch, D(2026, 11, 4))
    titles = ["Who did you vote for?"] * config.CANDIDATE_LIMIT
    titles += ["What time do polls close?", "What smell takes you back?", "What hobby costs too much?"]
    reddit = _Day(titles)
    picked = content.select_post(reddit, prev_title="", uploaded=frozenset({"What smell takes you back?"}))
    assert picked.title == "What hobby costs too much?"
