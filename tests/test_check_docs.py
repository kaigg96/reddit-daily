"""The tracker's checkable claims (scripts/check_docs.py). A false positive
here is not harmless: the fix a shift reaches for is deleting the citation."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import check_docs as c


def test_a_closed_issue_described_as_pending_is_caught():
    assert c.describes_as_open("Patch queued, awaiting #33's label.", 33)


def test_an_unrelated_open_elsewhere_on_a_long_row_is_not():
    row = ("| 1 | baking | **Open on the hook, not the format label** — "
           + "detail " * 30 + "Views never trigger (#18). |")
    assert not c.describes_as_open(row, 18)


def test_an_open_word_in_the_next_table_cell_is_not_this_issues():
    row = ("| ready | frames inline (keep while #74 is open) | **Bet 1's next step, "
           "under #71's limits** | R3.2 |")
    assert not c.describes_as_open(row, 71)
    assert c.describes_as_open(row, 74)
    assert c.describes_as_open("| blocked: awaiting #71's label | Item |", 71)


def test_an_open_word_inside_another_word_is_not_one():
    assert not c.describes_as_open('your #62 decision on "no new spending"', 62)
    assert c.describes_as_open("#62, still pending", 62)
    assert c.describes_as_open("the owner reopened #62", 62)


def test_a_longer_number_is_not_the_cited_issue():
    assert not c.describes_as_open("#180 is still open", 18)


def test_only_the_newest_worklog_entry_is_read_as_current():
    log = ("# Work log\n\n```\n## 2026-09-21 — template\n```\n\n---\n\n"
           "## 2026-10-04 (07:37) — newest\n\n- Blocked on #45.\n\n"
           "## 2026-10-02 (15:52) — older\n\n- Waiting on your edit (issue #44).\n")
    entry = c.latest_worklog_entry(log)
    assert entry.startswith("## 2026-10-04") and "#45" in entry
    assert "#44" not in entry and "template" not in entry


def _repo(tmp_path):
    import subprocess
    git = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True,
                                    capture_output=True, text=True)
    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@t"); git("config", "user.name", "t")
    (tmp_path / "f.txt").write_text("a\n")
    git("add", "."); git("commit", "-q", "-m", "base")
    git("checkout", "-q", "-b", "next")
    (tmp_path / "f.txt").write_text("next\n")
    git("commit", "-qam", "next")
    git("checkout", "-q", "main")
    return git


def _git_version():
    import re
    import subprocess
    out = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout
    m = re.search(r"(\d+)\.(\d+)", out)
    return tuple(map(int, m.groups())) if m else (0, 0)


# `merge-tree --write-tree` arrived in git 2.38; the owner's machine has 2.37,
# where the check itself answers "unknown" and these two would fail (TECH_DEBT).
needs_merge_tree = pytest.mark.skipif(
    _git_version() < (2, 38), reason="git merge-tree --write-tree needs git 2.38")


@needs_merge_tree
def test_a_release_branch_that_merges_cleanly_passes(tmp_path):
    git = _repo(tmp_path)
    (tmp_path / "g.txt").write_text("other\n")
    git("add", "."); git("commit", "-q", "-m", "unrelated")
    ok, why = c.check_next_release_merges(str(tmp_path), "main", "next")
    assert ok is True, why


@needs_merge_tree
def test_a_release_branch_that_conflicts_with_main_is_caught(tmp_path):
    """10-14: main's own work conflicted with bet 1's branch in one test file."""
    git = _repo(tmp_path)
    git("checkout", "-q", "next")
    (tmp_path / "h.txt").write_text("next\n")
    git("add", "."); git("commit", "-q", "-m", "next adds h")
    git("checkout", "-q", "main")
    (tmp_path / "f.txt").write_text("main\n")
    (tmp_path / "h.txt").write_text("main\n")
    git("add", "."); git("commit", "-q", "-m", "main moved")
    ok, why = c.check_next_release_merges(str(tmp_path), "main", "next")
    assert ok is False and "conflicts in f.txt, h.txt;" in why


def test_unrelated_histories_are_unknown_not_clean(tmp_path):
    git = _repo(tmp_path)
    git("checkout", "-q", "--orphan", "lone")
    (tmp_path / "f.txt").write_text("lone\n")
    git("add", "."); git("commit", "-q", "-m", "lone")
    assert c.check_next_release_merges(str(tmp_path), "main", "lone")[0] is None


def test_a_missing_release_branch_is_skipped_not_failed(tmp_path):
    _repo(tmp_path)
    assert c.check_next_release_merges(str(tmp_path), "main", "nope")[0] is None


def _clone_with_remote_branches(tmp_path):
    """A shift's clone: local `main` only; `product/done` merged into main,
    `product/next` not, both only on the remote."""
    import subprocess
    up = tmp_path / "up"
    up.mkdir()
    git = _repo(up)
    git("checkout", "-q", "-b", "product/done", "next")
    git("checkout", "-q", "main")
    git("merge", "-q", "--no-ff", "-m", "merge done", "product/done")
    git("checkout", "-q", "-b", "product/next")
    (up / "n.txt").write_text("unmerged\n")
    git("add", "."); git("commit", "-q", "-m", "unmerged")
    git("checkout", "-q", "main")
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "-q", "-b", "main", str(up), str(clone)],
                   check=True, capture_output=True)
    return clone


def test_a_merged_branch_only_the_remote_has_is_caught(tmp_path):
    clone = _clone_with_remote_branches(tmp_path)
    ok, why = c.check_merged_branches(str(clone), "Built on `product/done`, awaiting merge.")
    assert ok is False and "product/done" in why


def test_an_unmerged_branch_only_the_remote_has_is_not_gone(tmp_path):
    clone = _clone_with_remote_branches(tmp_path)
    assert c.check_merged_branches(str(clone), "On `product/next`, awaiting the label.")[0]


def test_a_file_path_is_not_a_branch(tmp_path):
    clone = _clone_with_remote_branches(tmp_path)
    (clone / "analysis").mkdir()
    (clone / "analysis" / "log.csv").write_text("x\n")
    assert c.check_merged_branches(str(clone), "`analysis/log.csv` is pending a read.")[0]
