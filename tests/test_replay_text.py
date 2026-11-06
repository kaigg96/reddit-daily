"""scripts/replay_text.py: the shipped-text replay gate for any change to
titles or closing lines (F159, F175)."""
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts import replay_text

FIELDS = ["video_id", "post_title", "video_title", "cta"]


def _log(tmp_path, rows):
    path = tmp_path / "upload_log.csv"
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return str(path)


def test_compare_counts_refusals_and_lists_differences():
    rows = [{"video_id": v} for v in ("a", "b", "c", "d")]
    a = {"title": ["Same", "REFUSED: shock phrase", "Old", "REFUSED: shock phrase"],
         "cta": [None, "x", None, None]}
    b = {"title": ["Same", "REFUSED: shock phrase", "New", "Kept"],
         "cta": [None, "x", None, None]}
    report = replay_text.compare(rows, a, b)
    n, refused, diffs = report["title"]
    assert n == 4
    assert refused == {"shock phrase": 1}  # refused by one side only is a difference
    assert diffs == [("c", "Old", "New"), ("d", "REFUSED: shock phrase", "Kept")]
    assert report["cta"] == (1, {}, [])  # an unlogged closing line is not compared


def test_replay_reads_each_tree_and_survives_the_cleaners_stdout(tmp_path, capsys):
    # The emoji title makes _clean_published print its refusal notice, which
    # corrupted hand-run replays that wrote their results to stdout (F175).
    log = _log(tmp_path, [
        {"video_id": "v1", "post_title": "What is it?", "video_title": "what is it", "cta": ""},
        {"video_id": "v2", "post_title": "Pets?", "video_title": "Pets? 🤫", "cta": "tell us"},
    ])
    code = replay_text.main(["HEAD", "HEAD", "--out", str(tmp_path / "out")], log=log)
    out = capsys.readouterr().out
    assert code == 0
    assert "the replay compares nothing" in out  # same ref twice says so
    assert "titles: 2 of 2 identical, 1 refused by both (swear word or emoji 1)" in out
    assert "closing lines: 1 of 1 identical" in out
    result = replay_text.json.load(open(tmp_path / "out" / "HEAD" / "result.json"))
    assert result["module"].startswith(str(tmp_path / "out" / "HEAD"))
    assert result["title"][0] == "What is it"  # sentence_case ran
    assert result["cta"] == [None, "Tell us"]


def test_unknown_ref_exits_naming_it(tmp_path):
    log = _log(tmp_path, [{"video_id": "v1", "post_title": "q", "video_title": "t", "cta": ""}])
    try:
        replay_text.main(["no-such-ref-xyz", "HEAD"], log=log)
    except SystemExit as e:
        assert "no-such-ref-xyz" in str(e)
    else:
        raise AssertionError("expected SystemExit")
