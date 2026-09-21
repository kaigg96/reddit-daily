"""Performance report — the standard way to answer "did X work?" (TECH_DEBT Pass 2).

Uses src/insights.py, so every answer inherits the rules that ad-hoc analysis
kept getting wrong: watch-seconds primary, age-matched cohorts, n-gating, and
zero-view videos counted separately rather than averaged in.

Usage:
  venv/bin/python scripts/report.py                    # channel overview
  venv/bin/python scripts/report.py --by format_version
  venv/bin/python scripts/report.py --by topic --metric views
  venv/bin/python scripts/report.py --compare candidate_rank=1 --metric watch_seconds
  venv/bin/python scripts/report.py --release v6       # the auto-revert check
  venv/bin/python scripts/report.py --release broll --release-key background_type
  venv/bin/python scripts/report.py --zeros            # suppression candidates
  venv/bin/python scripts/report.py --offline --by topic   # no YouTube credentials

--offline reads the committed weekly snapshot instead of the live API, so a
scheduled shift — which is deliberately given no YouTube secrets — can still
answer a performance question. It is a week stale by construction and is never
chosen silently: ask for it, and every answer carries its as-of date.
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


def zeros(now):
    """List 0-view videos, separating the two things that masquerade as
    suppression: owner-privatised videos, and zeroes inside channel-wide cold
    spells. Only the isolated ones are real per-video suppression candidates."""
    groups = insights.classify_zero_views(insights.load_channel_videos(now), now)
    print(f"{len(groups['isolated'])} isolated zero(s) — genuine suppression candidates:")
    for v in sorted(groups["isolated"], key=lambda x: x["published"], reverse=True):
        print(f"  {v['published'][:10]}  {v['id']}  neighbour median={v['neighbour_median']:.0f}"
              f"  {v['title'][:44]}")
    print(f"\n{len(groups['cold_spell'])} zero(s) inside channel-wide cold spells "
          f"— NOT per-video moderation:")
    for v in sorted(groups["cold_spell"], key=lambda x: x["published"], reverse=True)[:6]:
        print(f"  {v['published'][:10]}  {v['id']}  neighbour median={v['neighbour_median']:.0f}")
    if len(groups["cold_spell"]) > 6:
        print(f"  ... and {len(groups['cold_spell']) - 6} more")
    print(f"\n{len(groups['non_public'])} zero(s) are non-public (owner action, not suppression)")
    if groups["too_new"]:
        print(f"{len(groups['too_new'])} zero(s) are under {insights.ZERO_MIN_AGE_DAYS}d old "
              f"— too new to judge, not counted above:")
        for v in sorted(groups["too_new"], key=lambda x: x["published"], reverse=True):
            print(f"  {v['published'][:10]}  {v['id']}  {v['title'][:44]}")


def compare(videos, spec, metric, now):
    """Age-matched two-way test on one upload_log field.

    Videos where the field is unset are excluded from both cohorts — see
    insights.split_cohorts for why that matters."""
    key, _, value = spec.partition("=")
    a, b, unset = insights.split_cohorts(videos, key, value)
    if unset:
        print(f"({unset} video(s) have no {key} recorded — excluded from both cohorts)")
    print(insights.compare(a, b, f"{key}={value}", f"{key}!={value}", now, metric).render())


def release(version, key, target_age):
    """The auto-revert check for a flag-day change (`/shift` §5, issue #16).

    Has its own loader rather than using the shared one: it reads every upload
    at a *common age* from the weekly snapshot series, which is the only way a
    release ever becomes age-matched against the era it replaced. Needs no
    YouTube credentials, so a scheduled shift can run it."""
    load = insights.load_videos_at_age(target_age)
    for line in load.caveats():
        print(f"AGE-MATCHED: {line}")
    print()
    if not load.videos:
        sys.exit(f"No upload has a snapshot at ~{target_age:.0f} days old.")

    a, b, unset, later = insights.release_cohorts(load.videos, key, version)
    if unset:
        print(f"({unset} upload(s) have no {key} recorded — in neither cohort)")
    if later:
        print(f"({later} upload(s) postdate {version} — excluded, so this compares it "
              f"with what it replaced rather than with its own successors)")
    metrics = (Metric.WATCH, Metric.VIEWS)
    comparisons = [insights.compare(a, b, f"{key}={version}", f"before {version}",
                                    load.anchor, metric) for metric in metrics]
    # The floor comes from the era BEFORE the change. Measuring it on the
    # release's own uploads would let a volatile release excuse itself.
    floors = {m: insights.drift_floor(b, m) for m in metrics}
    print(insights.render_release(comparisons, floors))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--by", help="group by an upload_log field (format_version, topic, ...)")
    p.add_argument("--compare", help="age-matched two-way test, e.g. candidate_rank=1")
    p.add_argument("--release", metavar="VERSION",
                   help="auto-revert check on a flag-day change, e.g. v6: its uploads "
                        "vs the era it replaced, both read at the same age")
    p.add_argument("--release-key", default="format_version",
                   help="upload_log field --release splits on (default format_version; "
                        "use background_type for the b-roll switch)")
    p.add_argument("--at-age", type=float, default=insights.AGE_MATCH_TARGET_DAYS,
                   metavar="DAYS", help="age at which --release reads every upload "
                                        f"(default {insights.AGE_MATCH_TARGET_DAYS:.0f})")
    p.add_argument("--zeros", action="store_true",
                   help="list 0-view videos, classified into suppression candidates / "
                        "cold-spell / non-public")
    p.add_argument("--metric", default=Metric.WATCH,
                   choices=[Metric.WATCH, Metric.VIEWS, Metric.PCT, Metric.LIKES, Metric.COMMENTS])
    p.add_argument("--offline", action="store_true",
                   help="read the committed weekly snapshot instead of the live "
                        "YouTube API (no credentials needed; a week stale)")
    args = p.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)

    if args.zeros:          # uses the Data API (near-real-time), not the weekly snapshot
        if args.offline:
            # Refusing is the honest answer: the classification turns on privacy
            # status, and calling privatised videos suppression is the specific
            # wrong conclusion classify_zero_views exists to prevent.
            sys.exit("--zeros needs live privacy status, which the snapshot does not "
                     "record; it cannot be answered offline.")
        zeros(now)
        return

    if args.release:    # reads the snapshot series at a fixed age, not one point in time
        release(args.release, args.release_key, args.at_age)
        return

    if args.offline:
        load = insights.load_videos_offline()
        videos, now = load.videos, load.asof
        for line in load.caveats():
            print(f"OFFLINE: {line}")
        print()
    else:
        try:
            videos = insights.load_videos(now=now)
        except KeyError as e:
            # The scheduled-shift case: no YouTube secrets by design. Say so and
            # name the way through, rather than dying on a bare KeyError.
            sys.exit(f"No YouTube credentials ({e} is unset), so the live API is "
                     f"unavailable.\nRe-run with --offline to use the committed "
                     f"weekly snapshot instead.")

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
