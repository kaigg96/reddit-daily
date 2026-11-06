"""scripts/replay_text.py: the shipped-text replay gate for any change to
titles or closing lines (F159, F175)."""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import replay_text

FIELDS = ["video_id", "post_title", "video_title", "title_style", "title_caps"]


def _log(tmp_path, rows):
    path = tmp_path / "upload_log.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return str(path)


def test_compare_counts_refusals_and_lists_differences():
    rows = [{"video_id": v} for v in ("a", "b", "c", "d", "e")]
    a = {"title": ["Same", "REFUSED: swear word or emoji", "Old", "FALLBACK: Q?", "FALLBACK: Q?"]}
    b = {"title": ["Same", "REFUSED: swear word or emoji", "New", "Kept", "FALLBACK: Q?"]}
    n, refused, diffs = replay_text.compare(rows, a, b)
    assert n == 5
    # refused by one side only is a difference, never a refusal by both
    assert refused == {"swear word or emoji": 1, "fell back to the question": 1}
    assert diffs == [("c", "Old", "New"), ("d", "FALLBACK: Q?", "Kept")]


def test_replay_reads_each_tree_and_survives_the_cleaners_stdout(tmp_path, capsys):
    # The emoji title makes _clean_published print its refusal notice, which
    # corrupted hand-run replays that wrote their results to stdout (F175).
    log = _log(tmp_path, [
        {"video_id": "v1", "post_title": "What is it?", "video_title": "what is it",
         "title_style": "A", "title_caps": "0"},
        {"video_id": "v2", "post_title": "Pets?", "video_title": "Pets? \U0001f92b",
         "title_style": "B", "title_caps": ""},
        {"video_id": "v3", "post_title": "Your degree?", "video_title": "You Won't Believe These Degrees",
         "title_style": "B", "title_caps": "1"},
    ])
    out_dir = tmp_path / "out"
    (out_dir / "HEAD" / "src").mkdir(parents=True)
    (out_dir / "HEAD" / "src" / "stale.py").write_text("x = 1\n")  # a reused --out
    code = replay_text.main(["HEAD", "HEAD", "--out", str(out_dir)], log=log)
    out = capsys.readouterr().out
    assert code == 2  # the same src/ on both sides compares nothing, so never a pass
    assert "the replay compares nothing" in out
    assert not (out_dir / "HEAD" / "src" / "stale.py").exists()
    result = replay_text.json.load(open(out_dir / "HEAD" / "result.json"))
    assert result["module"].startswith(str(out_dir / "HEAD"))
    assert result["title"] == ["What is it", "REFUSED: swear word or emoji", "FALLBACK: Your degree?"]


def test_unknown_ref_exits_naming_it(tmp_path):
    log = _log(tmp_path, [{"video_id": "v1", "post_title": "q", "video_title": "t",
                           "title_style": "A", "title_caps": ""}])
    try:
        replay_text.main(["no-such-ref-xyz", "HEAD"], log=log)
    except SystemExit as e:
        assert "no-such-ref-xyz" in str(e)
    else:
        raise AssertionError("expected SystemExit")
