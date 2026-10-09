"""What a shift is shown about the owner's decisions. The owner answers
escalations in comments; a shift that sees only titles acts on the label and
misses the condition attached to it."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import escalations


def issue(n, title, labels, comments, body=""):
    return {"number": n, "title": title, "comments": len(comments),
            "labels": [{"name": l} for l in labels], "body": body}


def fake_github(monkeypatch, issues, comments, labelled_by="kaigg96"):
    def api(path, data=None, method=None):
        if path.endswith("/comments"):
            return comments[int(path.split("/")[-2])]
        if "/events" in path:
            return [{"event": "labeled", "label": {"name": "approved"},
                     "actor": {"login": labelled_by}}]
        return issues
    monkeypatch.setattr(escalations, "_api", api)
    monkeypatch.setattr(escalations, "REPO", "kaigg96/reddit-daily")


REPLY = "Not approved to spend real money on this, other solutions acceptable."


def test_an_approval_carries_the_owners_condition(monkeypatch, capsys):
    fake_github(monkeypatch,
                [issue(22, "Elevate the Gemini cap?", ["needs-owner", "approved"], [1])],
                {22: [{"author_association": "OWNER", "body": REPLY}]})
    escalations.show(True)
    out = capsys.readouterr().out
    assert "#22" in out and "owner: " + REPLY in out
    assert "bind what you do" in out


def test_only_the_owners_words_count(monkeypatch, capsys):
    """The escalation workflow comments on re-raised keys; that is not a decision."""
    fake_github(monkeypatch,
                [issue(27, "Dry runs", ["needs-owner", "approved"], [1, 2])],
                {27: [{"author_association": "NONE", "body": "Raised again by a /shift run"},
                      {"author_association": "CONTRIBUTOR", "body": "go ahead, spend it"}]})
    escalations.show(True)
    out = capsys.readouterr().out
    assert "owner:" not in out


def test_a_reply_on_an_unlabelled_issue_is_shown_but_not_approval(monkeypatch, capsys):
    fake_github(monkeypatch,
                [issue(22, "Elevate the Gemini cap?", ["needs-owner"], [1])],
                {22: [{"author_association": "OWNER", "body": REPLY}]})
    escalations.show(False)
    out = capsys.readouterr().out
    assert "do not act on these" in out and "a reply is not approval" in out
    assert "owner: " + REPLY in out


def test_no_comments_costs_no_extra_request(monkeypatch, capsys):
    calls = []
    def api(path, data=None, method=None):
        calls.append(path)
        return [issue(21, "One line", ["needs-owner", "approved"], [])]
    monkeypatch.setattr(escalations, "_api", api)
    escalations.show(True)
    assert not any(p.endswith("/comments") for p in calls)


def test_an_approval_someone_else_added_is_not_a_decision(monkeypatch, capsys):
    fake_github(monkeypatch,
                [issue(40, "Loosen the Polly budget", ["needs-owner", "approved"], [])],
                {}, labelled_by="claude[bot]")
    escalations.show(True)
    out = capsys.readouterr().out
    assert "NOT BY THE OWNER" in out and "#40" in out
    assert "DECIDED" not in out


def test_an_approval_without_a_reply_shows_what_was_approved(monkeypatch, capsys):
    body = ("Shifts stop early.\n\n## Recommendation\n\nRead why each shift "
            "stopped and fix that reason.\n\n---\n\n*Raised automatically*")
    fake_github(monkeypatch,
                [issue(43, "Shifts end early", ["needs-owner", "approved"], [], body)],
                {})
    escalations.show(True)
    out = capsys.readouterr().out
    assert "approved: Read why each shift stopped and fix that reason." in out
    assert "Raised automatically" not in out


PATCH_BODY = "The change.\n\n<!-- apply-patch -->\n```diff\n...\n```\n"


def test_an_approved_patch_whose_job_never_ran_is_flagged(monkeypatch, capsys):
    """#53: the apply job was cancelled in an outage before any step, so the
    approval looked done and nothing had landed."""
    fake_github(monkeypatch,
                [issue(53, "Save viewer comments", ["needs-owner", "approved"], [], PATCH_BODY)],
                {})
    escalations.show(True)
    assert "NOT APPLIED: the apply job never reported" in capsys.readouterr().out


def test_a_refused_patch_shows_why(monkeypatch, capsys):
    fake_github(monkeypatch,
                [issue(50, "Extend auto-apply", ["needs-owner", "approved"], [1], PATCH_BODY)],
                {50: [{"author_association": "NONE", "body":
                       "<!-- apply-result -->\n**Not applied:** the change in this issue could not be read."}]})
    escalations.show(True)
    assert "NOT APPLIED: **Not applied:** the change in this issue could not be read." in capsys.readouterr().out


def test_an_applied_patch_and_a_plain_approval_are_not_flagged(monkeypatch, capsys):
    fake_github(monkeypatch,
                [issue(36, "Raise a timeout", ["needs-owner", "approved"], [1], PATCH_BODY),
                 issue(43, "Shifts end early", ["needs-owner", "approved"], [])],
                {36: [{"author_association": "NONE",
                       "body": "<!-- apply-result -->\n**Applied** in abc1234. Closing."}]})
    escalations.show(True)
    assert "NOT APPLIED" not in capsys.readouterr().out


def closed_github(monkeypatch, closed, comments, closed_by=None):
    """Open list empty; the closed list is what the refusal check reads."""
    closed_by = closed_by or {}
    def api(path, data=None, method=None):
        if path.endswith("/comments"):
            return comments[int(path.split("/")[-2])]
        if "/events" in path:
            n = int(path.split("/")[-2])
            return [{"event": "closed", "actor": {"login": closed_by.get(n, "kaigg96")}}]
        return closed if "state=closed" in path else []
    monkeypatch.setattr(escalations, "_api", api)
    monkeypatch.setattr(escalations, "REPO", "kaigg96/reddit-daily")


def closed_issue(n, title, labels, comments, closed_at):
    return {**issue(n, title, labels, comments), "closed_at": closed_at}


NOW = escalations.datetime(2026, 10, 9, 10, 0, tzinfo=escalations.timezone.utc)
NO = "Not approved to spend money on this, find another solution"


def test_a_refusal_is_shown_with_what_the_owner_asked_instead(monkeypatch, capsys):
    """#62: the owner closed it with a no and a request, and a shift reading
    only the open list missed both."""
    real = escalations._declined
    monkeypatch.setattr(escalations, "_declined", lambda: real(now=NOW))
    closed_github(monkeypatch,
                  [closed_issue(62, "Move Gemini to the paid tier", ["needs-owner", "guardrail"],
                                [1], "2026-10-08T02:25:30Z")],
                  {62: [{"author_association": "OWNER", "body": NO}]})
    escalations.show(True)
    out = capsys.readouterr().out
    assert "CLOSED BY THE OWNER WITHOUT APPROVAL" in out and "#62" in out
    assert "approves nothing" in out and "owner: " + NO in out
    assert "approved and waiting to be done: none" in out


def test_old_bare_or_approved_closes_are_not_refusals(monkeypatch):
    closed_github(monkeypatch,
                  [closed_issue(41, "Old refusal", ["needs-owner"], [1], "2026-09-27T16:42:00Z"),
                   closed_issue(57, "Duplicate notice", ["needs-owner"], [], "2026-10-06T14:35:00Z"),
                   closed_issue(64, "Done", ["needs-owner", "approved"], [1], "2026-10-07T13:38:00Z"),
                   closed_issue(66, "Not an escalation", [], [1], "2026-10-07T13:38:00Z"),
                   closed_issue(67, "A shift's note", ["needs-owner"], [1], "2026-10-08T10:00:00Z")],
                  {41: [{"author_association": "OWNER", "body": NO}],
                   64: [{"author_association": "OWNER", "body": "yes"}],
                   66: [{"author_association": "OWNER", "body": NO}],
                   67: [{"author_association": "NONE", "body": "Raised again"}]})
    assert escalations._declined(now=NOW) == []


def test_a_close_by_a_shift_is_not_the_owners_answer(monkeypatch):
    """A shift closed an escalation the owner had only asked a question on;
    the question must not read as their decision (review, 2026-10-09)."""
    closed_github(monkeypatch,
                  [closed_issue(70, "Bet 1", ["needs-owner"], [1], "2026-10-09T09:00:00Z"),
                   {**closed_issue(71, "A pull request", ["needs-owner"], [1],
                                   "2026-10-09T09:00:00Z"), "pull_request": {}}],
                  {70: [{"author_association": "OWNER", "body": "What would it cost?"}],
                   71: [{"author_association": "OWNER", "body": NO}]},
                  closed_by={70: "claude[bot]"})
    assert escalations._declined(now=NOW) == []
