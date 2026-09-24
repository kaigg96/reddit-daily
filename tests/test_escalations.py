"""What a shift is shown about the owner's decisions. The owner answers
escalations in comments; a shift that sees only titles acts on the label and
misses the condition attached to it."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import escalations


def issue(n, title, labels, comments):
    return {"number": n, "title": title, "comments": len(comments),
            "labels": [{"name": l} for l in labels]}


def fake_github(monkeypatch, issues, comments):
    def api(path, data=None, method=None):
        if path.endswith("/comments"):
            return comments[int(path.split("/")[-2])]
        return issues
    monkeypatch.setattr(escalations, "_api", api)


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
