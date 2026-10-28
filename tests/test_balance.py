"""`report.py --balance`: a coin's arms against another field, from the upload
log alone, so a read's confounders can be checked before the read (PRD §0 #14, R2)."""
import datetime

import pytest

from src import insights


def _rows(*cells, since="2026-10-20"):
    return [{"timestamp_utc": f"{since}T05:00:00+00:00", "title_caps": coin, "subreddit": sub}
            for coin, sub, n in cells for _ in range(n)]


def test_arms_with_one_mix_are_not_flagged():
    arms, levels, counts, p = insights.assignment_balance(
        "title_caps", "subreddit", rows=_rows(("0", "A", 5), ("0", "B", 5), ("1", "A", 5), ("1", "B", 5)))
    assert arms == ["0", "1"] and levels == ["A", "B"]
    assert counts["1"] == {"A": 5, "B": 5} and p == {"A": 1.0, "B": 1.0}


def test_arms_drawn_from_different_mixes_are_flagged():
    *_, p = insights.assignment_balance(
        "title_caps", "subreddit", rows=_rows(("0", "A", 12), ("0", "B", 1), ("1", "A", 1), ("1", "B", 12)))
    assert p["A"] < 0.001 and p["A"] == p["B"]


def test_since_and_an_unset_coin_leave_uploads_out():
    rows = (_rows(("0", "A", 3), ("1", "B", 3), since="2026-10-01")
            + _rows(("0", "A", 2), ("1", "A", 2), ("", "B", 9)))
    arms, levels, counts, _ = insights.assignment_balance(
        "title_caps", "subreddit", since=datetime.date(2026, 10, 15), rows=rows)
    assert levels == ["A"] and counts == {"0": {"A": 2}, "1": {"A": 2}}


def test_a_coin_without_two_arms_is_refused():
    with pytest.raises(ValueError, match="1 arm"):
        insights.assignment_balance("title_caps", "subreddit", rows=_rows(("0", "A", 4)))
