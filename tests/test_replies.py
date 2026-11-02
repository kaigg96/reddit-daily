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
    assert replies.check_reply("So you hate your step mum?", "I hate my step mum") is None
    assert replies.check_reply("Wait, I hate my step mum too", "I hate my step mum") == "quotes the viewer"
    assert replies.check_reply("я люблю эту игру очень сильно правда", "я люблю эту игру очень сильно правда") == "quotes the viewer"
    for prose in ("I agree. Me too", "Exactly. Be kind", "Fair. Co-parenting is hard", "Good point. Tv shows too"):
        assert replies.check_reply(prose) is None, prose


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


class _Verdict:
    def __init__(self, verdict="pass", unsafe=(), category="", source="gemini"):
        self.verdict, self.unsafe, self.category, self.source = verdict, set(unsafe), category, source


class _Client:
    def __init__(self, comments, answered=(), fail=()):
        self.comments, self.answered, self.fail, self.posted = comments, set(answered), set(fail), []

    def comment(self, parent_id):
        return self.comments.get(parent_id)

    def replied(self, parent_id, channel_id):
        return parent_id in self.answered

    def post(self, parent_id, text):
        if parent_id in self.fail:
            return False
        self.posted.append(parent_id)
        return True


def _queued(*parents):
    return [_row(i + 1, parent=p) for i, p in enumerate(parents)]


def test_post_due_posts_only_what_passes_every_check():
    rows = _queued("ok", "gone", "ours", "answered", "unsafe", "backstop", "fails", "demoted")
    client = _Client({p: ("viewer", "a comment") for p in ("ok", "answered", "unsafe", "backstop", "fails", "demoted")}
                     | {"ours": ("US", "our pinned question")}, answered={"answered"}, fail={"fails"})
    demoted = _Verdict()
    demoted.demoted = "graphic_harm"
    verdicts = {"unsafe": _Verdict("skip_post", category="sexual"), "backstop": _Verdict(source="backstop"),
                "fails": _Verdict(), "ok": _Verdict(), "demoted": demoted}
    for r in rows:   # one reply text per row, so the screen can tell them apart
        r["reply"] = f"Nice one {r['parent_id']}"
    screen = lambda q, cs: verdicts.get(cs[0].split()[-1], _Verdict())
    log = replies.post_due(rows, TODAY, client, screen, "US", {}, NOW, dry_run=False, cap=10)
    status = {r["parent_id"]: (r["status"], r["note"]) for r in rows}
    assert client.posted == ["ok"]
    assert status["ok"][0] == "posted" and rows[0]["posted_utc"].startswith("2026-11-02")
    assert status["gone"] == ("refused", "comment gone")
    assert status["ours"] == ("refused", "our own comment")
    assert status["answered"] == ("refused", "already answered on YouTube")
    assert status["unsafe"][0] == "refused" and status["backstop"][0] == "refused"
    assert status["fails"][0] == "queued"                    # a failed post stays queued, to retry
    assert status["demoted"] == ("refused", "screen: pass, graphic_harm")
    assert len(log) == 8


def test_post_due_refuses_a_reply_quoting_the_live_comment_and_dry_run_changes_nothing():
    rows = _queued("q", "fine")
    rows[0]["reply"] = "You said I go to school every day with concealer"
    client = _Client({"q": ("viewer", "I go to school every day with concealer and mascara"),
                      "fine": ("viewer", "hello")})
    log = replies.post_due(rows, TODAY, client, lambda q, cs: _Verdict(), "US", {}, NOW, dry_run=True)
    assert client.posted == [] and all(r["status"] == "queued" for r in rows)
    assert any("quotes the viewer" in line for line in log) and any(line.startswith("would post") for line in log)


def test_post_due_survives_a_client_error_and_gives_up_after_three_failed_posts():
    class Boom(_Client):
        def comment(self, parent_id):
            if parent_id == "boom":
                raise RuntimeError("503")
            return super().comment(parent_id)

    rows = _queued("boom", "ok", "fails")
    rows[2]["note"] = "post failed 2"
    client = Boom({"ok": ("viewer", "hi"), "fails": ("viewer", "hi")}, fail={"fails"})
    log = replies.post_due(rows, TODAY, client, lambda q, cs: _Verdict(), "US", {}, NOW, dry_run=False)
    status = {r["parent_id"]: (r["status"], r["note"]) for r in rows}
    assert status["boom"][0] == "queued" and status["boom"][1] == "post failed 1"
    assert status["ok"][0] == "posted"
    assert status["fails"] == ("refused", "post failed 3 times")
    assert any(line.startswith("error") for line in log)
