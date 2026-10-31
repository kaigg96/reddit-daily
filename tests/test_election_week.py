"""Midterm week (2026-11-03): questions about voting are not candidates, since
answers are read word for word and YouTube removes misleading voting claims."""
import datetime

from src import config, content

D = datetime.date


def test_voting_questions_are_skipped_through_the_end_date():
    for title in ("Who are you voting for in the midterms?",
                  "What would make you vote for the other party?",
                  "Non-Americans, what do you think of the US election?",
                  "Have you ever been turned away at a polling place?",
                  "Is a mail-in BALLOT safe?"):
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
