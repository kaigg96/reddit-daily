"""Performance report — the standard way to answer "did X work?" (TECH_DEBT Pass 2).

Uses src/insights.py, so every answer inherits the rules that ad-hoc analysis
kept getting wrong: watch-seconds primary, age-matched cohorts, n-gating, and
zero-view videos counted separately rather than averaged in.

Usage:
  venv/bin/python scripts/report.py                    # channel overview
  venv/bin/python scripts/report.py --by format_version
  venv/bin/python scripts/report.py --by topic --metric views
  venv/bin/python scripts/report.py --compare candidate_rank=1 --metric watch_seconds
"""

import argparse
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import insights  # noqa: E402
from src.insights import Metric  # noqa: E402


def overview(videos, now):
    live = [v for v in videos if v.views > 0]
    zeros = [v for v in videos if v.views == 0]
    print(f"{len(videos)} logged uploads analyzed (>= {insights.MIN_AGE_DAYS} days old)")
    print(f"  median watch-seconds : {insights.median([v.watch_seconds for v in live]):.1f}s   (primary metric)")
    print(f"  median views         : {insights.median([v.views for v in live]):.0f}")
    print(f"  median avg-% viewed  : {insights.median([v.avg_view_pct for v in live]):.1f}%   (diagnostic only)")
    if zeros:
        print(f"  zero-view uploads    : {len(zeros)}  <-- suppression candidates, see R4.6")
        for v in sorted(zeros, key=lambda x: x.published)[-5:]:
            print(f"      {v.published.date()}  {v.meta.get('post_title','')[:58]}")


def by_dimension(videos, key, metric, now):
    groups = insights.split_by(videos, key)
    print(f"{metric} by {key}   (n<{insights.MIN_COHORT} shown but not conclusive)\n")
    rows = []
    for label, vids in groups.items():
        c = insights.summarize(vids, label, metric, now)
        rows.append(c)
    rows.sort(key=lambda c: (c.median if c.median == c.median else -1), reverse=True)
    print(f"  {'group':24} {'n':>4} {'median':>9} {'med age':>8} {'zero':>5}")
    for c in rows:
        mark = "" if c.sufficient else "  (thin)"
        print(f"  {c.label:24} {c.n:>4} {c.median:>9.1f} {c.median_age:>7.0f}d "
              f"{c.zero_view_count:>5}{mark}")

    # Age spread warning — comparing these groups may be measuring age.
    ages = [c.median_age for c in rows if c.sufficient and c.median_age == c.median_age]
    if len(ages) >= 2 and max(ages) > 1.5 * min(ages):
        print(f"\n  NOTE: median ages range {min(ages):.0f}d–{max(ages):.0f}d. "
              f"Cross-group differences may reflect age, not the variable.\n"
              f"  Use --compare for an age-matched two-way test.")


def compare(videos, spec, metric, now):
    key, _, value = spec.partition("=")
    a = [v for v in videos if str(v.meta.get(key, "")).strip() == value]
    b = [v for v in videos if str(v.meta.get(key, "")).strip() != value]
    print(insights.compare(a, b, f"{key}={value}", f"{key}!={value}", now, metric).render())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--by", help="group by an upload_log field (format_version, topic, ...)")
    p.add_argument("--compare", help="age-matched two-way test, e.g. candidate_rank=1")
    p.add_argument("--metric", default=Metric.WATCH,
                   choices=[Metric.WATCH, Metric.VIEWS, Metric.PCT, Metric.LIKES, Metric.COMMENTS])
    args = p.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)
    videos = insights.load_videos(now=now)
    if not videos:
        sys.exit("No analyzable uploads found.")

    if args.compare:
        compare(videos, args.compare, args.metric, now)
    elif args.by:
        by_dimension(videos, args.by, args.metric, now)
    else:
        overview(videos, now)


if __name__ == "__main__":
    main()
