"""The experiment ledger (PLAN.md C18): whether the experiment process can
tell a change that works. The rules existed; no record of them did, so a late
read, an overdue one, or a keep inside its own detection limit was invisible."""
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import insights

FIELDS = ["id", "item", "kind", "metric", "rule_set", "due", "read", "verdict",
          "effect", "n", "detectable", "credited", "source"]
TODAY = datetime.date(2026, 10, 27)


def rule(i, due="", read="", verdict="", effect="", detectable="", rule_set="2026-10-01",
         credited=""):
    return {"id": i, "item": "x", "kind": "release", "metric": "watch_seconds",
            "rule_set": rule_set, "due": due, "read": read, "verdict": verdict,
            "effect": effect, "n": "", "detectable": detectable, "credited": credited,
            "source": ""}


def test_on_time_late_and_overdue_reads():
    s = insights.experiment_ledger([
        rule("a", due="2026-10-10", read="2026-10-12", verdict="keep"),   # 2 days: on time
        rule("b", due="2026-10-01", read="2026-10-20", verdict="noise"),  # 19 days: late
        rule("c", due="2026-10-15"),                                      # unread, 12 days past
        rule("d", due="2026-11-02", detectable="~18%"),                   # not yet due
        rule("e", read="2026-10-05", verdict="recorded"),                 # no due date set
    ], TODAY)
    assert [r["id"] for r in s["on_time"]] == ["a"]
    assert [r["id"] for r in s["late"]] == ["b"]
    assert [r["id"] for r in s["overdue"]] == ["c"]
    assert [r["id"] for r in s["undated"]] == ["e"]
    assert ("d", "~18%", "2026-11-02") in s["upcoming"]
    assert s["verdicts"] == {"keep": 1, "noise": 1, "pending": 2, "recorded": 1}


def test_a_rule_dropped_unread_is_neither_pending_nor_upcoming():
    s = insights.experiment_ledger([rule("#7", verdict="drop"), rule("#3", due="2026-11-02")],
                                   TODAY)
    assert [r["id"] for r in s["closed_unread"]] == ["#7"]
    assert [u[0] for u in s["upcoming"]] == ["#3"]


def test_a_keep_is_credited_only_beyond_its_limit():
    s = insights.experiment_ledger([
        rule("v7", read="2026-10-12", verdict="keep", effect="+20%", detectable="13%"),
        rule("v6", read="2026-10-06", verdict="keep", effect="+10%", detectable="12%"),
        rule("v5", read="2026-09-21", verdict="keep", effect="−50%", detectable=""),
        rule("t", read="2026-09-22", verdict="noise", effect="+11%", detectable="12%"),
    ], TODAY)
    assert [r["id"] for r in s["credited"]] == ["v7"]
    assert [r["id"] for r in s["not_credited"]] == ["v6"]
    assert [r["id"] for r in s["unmeasured_keeps"]] == ["v5"]


def test_the_render_says_no_rule_has_reverted_and_a_keep_is_not_proof():
    text = insights.render_experiment_ledger(insights.experiment_ledger([
        rule("v7", due="2026-10-10", read="2026-10-12", verdict="keep",
             effect="+20%", detectable="13%"),
        rule("#3", due="2026-11-02", detectable="~18%"),
    ], TODAY))
    assert "2 pre-committed rules, 1 read, 1 not yet" in text
    assert "1 of 1 on time" in text
    assert "no rule has ever reverted" in text
    assert "not a measured gain" in text
    assert "#3: ~18%, 2026-11-02" in text
    text = insights.render_experiment_ledger(insights.experiment_ledger([
        rule("b-roll-views", read="2026-09-21", verdict="revert"),
        rule("v7", read="2026-10-12", verdict="keep")], TODAY))
    assert "reverts: 1 (b-roll-views)" in text


def test_no_ledger_says_so(tmp_path):
    assert insights.load_experiments(tmp_path / "missing.csv") == []
    assert "No experiment ledger" in insights.render_experiment_ledger(
        insights.experiment_ledger([], TODAY))


def test_the_backfilled_ledger_parses():
    rows = insights.load_experiments()
    assert rows, "analysis/experiments.csv is the C18 backfill"
    assert list(rows[0]) == FIELDS
    for r in rows:
        for k in ("rule_set", "due", "read"):
            assert not r[k] or insights._ledger_date(r[k]), (r["id"], k, r[k])
        assert r["verdict"] in ("keep", "revert", "drop", "noise", "lead", "recorded",
                                "parked", "retired", "pending"), r["id"]
        assert r["kind"] in ("release", "coin", "observational", "retire"), r["id"]
        assert not (r["read"] and r["verdict"] == "pending"), r["id"]
        assert r["credited"] in ("", "yes", "no"), r["id"]
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))


def test_the_records_own_credit_call_and_real_cells():
    # v7's +20% beat its 13% limit, but the record says "Not credited": its
    # lead was mostly length. A loss is never a gain, and a "bar" is a
    # threshold, not a detection limit.
    s = insights.experiment_ledger([
        rule("v7", read="2026-10-12", verdict="keep", effect="+20% (12.0 vs 10.0)",
             detectable="13%", credited="no"),
        rule("b-roll", read="2026-09-24", verdict="keep", effect="+22%", detectable="11%"),
        rule("neg", read="2026-10-01", verdict="keep", effect="−15%", detectable="12%"),
        rule("bar", read="2026-10-01", verdict="keep", effect="31% to 18% at 15 a side",
             detectable="bar ≥90% agreement"),
    ], TODAY)
    assert [r["id"] for r in s["credited"]] == ["b-roll"]
    assert [r["id"] for r in s["not_credited"]] == ["v7", "neg"]
    assert [r["id"] for r in s["unmeasured_keeps"]] == ["bar"]
    assert insights._percent("~82% views; ~16% watch_seconds") == 82
    assert insights._percent("−39%") == -39


def test_a_read_seven_days_late_is_on_time_and_eight_is_late():
    s = insights.experiment_ledger([
        rule("a", due="2026-10-05", read="2026-10-12", verdict="noise"),
        rule("b", due="2026-10-05", read="2026-10-13", verdict="noise"),
    ], TODAY)
    assert [r["id"] for r in s["on_time"]] == ["a"] and [r["id"] for r in s["late"]] == ["b"]
