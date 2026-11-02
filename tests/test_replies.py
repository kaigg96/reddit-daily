"""The reply queue enforces the publishing policy's rules (ORG.md, Audience &
community; PLAN C10) before any post exists to break them."""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import replies

NOW = dt.datetime(2026, 11, 2, 21, 0, tzinfo=dt.timezone.utc)
TODAY = NOW.date()


def test_check_reply_allows_a_plain_answer():
    assert replies.check_reply("Board games count! Which one do you play most?") is None


def test_check_reply_refuses_each_policy_breach():
    assert replies.check_reply("") == "empty"
    assert replies.check_reply("x" * 201).startswith("over")
    for link in ("see https://example.com", "www.example.com", "check example.com",
                 "example . com", "example dot com", "shop.co.uk"):
        assert replies.check_reply(link) == "contains a link"
    for about_us in ("I'm an AI", "This reply was generated", "made by a bot",
                     "I'm a real person", "As a human I agree", "ChatGPT says so", "I'm real",
                     "a chatbot wrote it", "robots", "AIs are", "LLMs", "OpenAI", "humans like us"):
        assert replies.check_reply(about_us) == "mentions AI, automation or being a person", about_us
    assert replies.check_reply("that is fucking great") == "profanity"
    viewer = "I go to school every day with a bit of concealer and mascara"
    assert replies.check_reply("You go to school every day with a bit of it?", viewer) == "quotes the viewer"
    assert replies.check_reply("Minimal makeup still counts!", viewer) is None


def test_queue_reply_appends_once_per_comment_and_refuses_bad_drafts():
    rows = []
    assert replies.queue_reply(rows, "vid", "c1", " Great question ", now=NOW) is None
    assert rows[0]["reply"] == "Great question" and rows[0]["status"] == "queued"
    assert replies.queue_reply(rows, "vid", "c1", "Another one", now=NOW) == "already replied or queued"
    assert replies.queue_reply(rows, "vid", "c2", "visit www.x.com", now=NOW) == "contains a link"
    assert replies.queue_reply(rows, "", "c3", "Fine", now=NOW).startswith("needs")
    assert len(rows) == 1


def _row(i, status="queued", parent=None, posted="", reply="Nice one"):
    return {"queued_utc": f"2026-11-02T0{i}:00:00+00:00", "video_id": "v", "parent_id": parent or f"c{i}",
            "reply": reply, "status": status, "posted_utc": posted, "note": ""}


def test_due_caps_the_day_counting_what_was_already_posted():
    rows = [_row(i) for i in range(1, 9)]
    assert [r["parent_id"] for r in replies.due(rows, TODAY)[0]] == ["c1", "c2", "c3", "c4", "c5"]
    rows[0].update(status="posted", posted_utc="2026-11-02T10:00:00+00:00")
    rows[1].update(status="posted", posted_utc="2026-11-01T10:00:00+00:00")   # yesterday: not counted
    assert len(replies.due(rows, TODAY)[0]) == 4
    for r in rows[2:7]:
        r.update(status="posted", posted_utc="2026-11-02T11:00:00+00:00")
    assert replies.due(rows, TODAY) == ([], [])          # the day's cap is used up


def test_due_skips_failing_text_and_a_second_reply_to_one_comment():
    rows = [_row(1, reply="see www.x.com"), _row(2, parent="c9"), _row(3, parent="c9"),
            _row(4, status="posted", parent="c5", posted="2026-10-30T10:00:00+00:00"), _row(5, parent="c5")]
    post, refuse = replies.due(rows, TODAY)
    assert [r["queued_utc"][11:13] for r in post] == ["02"]
    assert sorted(r["queued_utc"][11:13] for r in refuse) == ["01", "03", "05"]


def test_load_and_save_round_trip_with_lf(tmp_path):
    path = tmp_path / "community" / "replies.csv"
    assert replies.load(path) == []
    rows = []
    replies.queue_reply(rows, "vid", "c1", "Thanks for watching", now=NOW)
    replies.save(rows, path)
    assert b"\r\n" not in path.read_bytes()
    assert replies.load(path)[0]["reply"] == "Thanks for watching"
