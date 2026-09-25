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



def _snapshot_metric_rows(metric_col="avg_view_duration_s"):
    """Weekly-snapshot rows shaped for insights.trajectory."""
    import csv as _csv
    import datetime as _dt
    import os as _os
    root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    path = _os.path.join(root, "analysis", "analytics_snapshots.csv")
    out = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for r in _csv.DictReader(f):
                try:
                    pub = _dt.datetime.fromisoformat(
                        (r.get("published_at") or "").replace("Z", "+00:00"))
                    snap = _dt.datetime.fromisoformat(
                        (r.get("snapshot_date") or "") + "T00:00:00+00:00")
                    val = float(r.get(metric_col) or 0)
                except (ValueError, TypeError):
                    continue
                out.append({"video_id": r.get("video_id"), "published": pub,
                            "snapshot": snap, "value": val})
    except OSError:
        pass
    return out


def _period_metrics(at_age=7, tolerance=4, half=3):
    """Metrics for the recent `half` publish-weeks vs the `half` before them.

    Every upload read at the same age, so the two periods are comparable.
    Duration comes from upload_log; the rest from the weekly snapshot.
    """
    import csv as _csv
    import datetime as _dt
    import os as _os
    root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

    durations = {}
    try:
        with open(_os.path.join(root, "upload_log.csv"), encoding="utf-8",
                  errors="ignore") as f:
            for r in _csv.DictReader(f):
                try:
                    durations[r["video_id"]] = float(r.get("duration_s") or 0)
                except (ValueError, TypeError):
                    pass
    except OSError:
        pass

    best = {}
    try:
        with open(_os.path.join(root, "analysis", "analytics_snapshots.csv"),
                  encoding="utf-8", errors="ignore") as f:
            for r in _csv.DictReader(f):
                try:
                    pub = _dt.datetime.fromisoformat(
                        (r.get("published_at") or "").replace("Z", "+00:00"))
                    snap = _dt.datetime.fromisoformat(
                        (r.get("snapshot_date") or "") + "T00:00:00+00:00")
                except (ValueError, TypeError):
                    continue
                age = (snap - pub).days
                if abs(age - at_age) > tolerance:
                    continue
                vid = r.get("video_id")
                prev = best.get(vid)
                if prev is None or abs(age - at_age) < abs(prev[0] - at_age):
                    best[vid] = (age, r, pub)
    except OSError:
        return None, None, 0, 0

    buckets = {}
    for vid, (_, r, pub) in best.items():
        buckets.setdefault(pub.strftime("%Y-W%V"), []).append((vid, r))
    weeks = sorted(w for w, v in buckets.items() if len(v) >= 5)
    if len(weeks) < half * 2:
        return None, None, 0, 0

    def agg(window):
        rows = [pair for w in window for pair in buckets[w]]
        def nums(col):
            out = []
            for _, r in rows:
                try:
                    v = float(r.get(col) or 0)
                except (ValueError, TypeError):
                    continue
                if v > 0:
                    out.append(v)
            return out
        views = nums("views")
        zeros = sum(1 for _, r in rows if float(r.get("views") or 0) == 0)
        m = {
            "watch_seconds": insights.median(nums("avg_view_duration_s")),
            "avg_view_pct": insights.median(nums("avg_view_pct")),
            "views": insights.median(views),
            "zero_rate": 100.0 * zeros / max(len(rows), 1),
        }
        d = [durations[v] for v, _ in rows if durations.get(v)]
        if d:
            m["duration_s"] = insights.median(d)
        if views:
            tv = sum(views) or 1
            m["likes_per_100"] = 100.0 * sum(nums("likes")) / tv
            m["comments_per_100"] = 100.0 * sum(nums("comments")) / tv
        return m

    prior, recent = weeks[-half * 2:-half], weeks[-half:]
    n_prior = sum(len(buckets[w]) for w in prior)
    n_recent = sum(len(buckets[w]) for w in recent)
    return agg(prior), agg(recent), n_prior, n_recent


def show_scorecard(args):
    """`--scorecard`: many metrics, one honest verdict, tensions visible."""
    then, now, n_then, n_now = _period_metrics(at_age=args.at_age or 7)
    if not then:
        print("not enough comparable history yet")
        return
    verdict, rows, notes = insights.scorecard(then, now)
    print(f"CHANNEL SCORECARD — every upload read at ~{args.at_age or 7} days old")
    print(f"  prior 3 weeks (n={n_then})  vs  recent 3 weeks (n={n_now})\n")
    kind = None
    for r in rows:
        if r["kind"] != kind:
            kind = r["kind"]
            print(f"  {kind}")
        print(f"    {r['metric']:18} {r['then']:>8.1f} -> {r['now']:>8.1f}  "
              f"{r['change']:+8.1f}   {r['read']}")
    print(f"\n  VERDICT: {verdict}")
    for n in notes:
        print(f"    - {n}")


def show_trajectory(args):
    """`--trajectory`: is the channel actually getting better?"""
    rows = _snapshot_metric_rows()
    series = insights.trajectory(rows, at_age=args.at_age or 7)
    if not series:
        print("not enough comparable history yet")
        return
    print(f"Median watch-seconds, every upload read at ~{args.at_age or 7} days old\n")
    print(f"  {'week':10} {'n':>4} {'median':>8}")
    for period, n, med in series:
        print(f"  {period:10} {n:>4} {med:>7.1f}s")

    floor = insights.median([abs(b[2] - a[2])
                            for a, b in zip(series, series[1:])]) or None
    verdict, why = insights.trajectory_verdict(series, floor=floor)
    print(f"\n  {verdict.upper()} — {why}")
    if floor:
        print(f"  (week-to-week drift on this channel is ~{floor:.1f}s)")
    if verdict == "flat":
        print("\n  Flat is the actionable verdict: the work being done is not"
              "\n  moving the outcome. See `/backlog` — this forces PM's priority.")


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
    p.add_argument("--scorecard", action="store_true",
                   help="many metrics at once: success, guardrails and "
                        "diagnostics, with one verdict that shows disagreement")
    p.add_argument("--trajectory", action="store_true",
                   help="is the channel improving? every upload read at the "
                        "same age, grouped by publish week")
    p.add_argument("--zeros", action="store_true",
                   help="list 0-view videos, classified into suppression candidates / "
                        "cold-spell / non-public")
    p.add_argument("--replays", action="store_true",
                   help="how many videos average over 100%% viewed, which only "
                        "replays can cause (backlog #9's first test)")
    p.add_argument("--metric", default=Metric.WATCH,
                   choices=[Metric.WATCH, Metric.VIEWS, Metric.PCT, Metric.LIKES, Metric.COMMENTS])
    p.add_argument("--offline", action="store_true",
                   help="read the committed weekly snapshot instead of the live "
                        "YouTube API (no credentials needed; a week stale)")
    args = p.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)

    if args.scorecard:      # many metrics; no single one can judge this channel
        show_scorecard(args)
        return

    if args.trajectory:     # the only surface that answers "are we improving?"
        show_trajectory(args)
        return

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

    if args.replays:
        show_replays(videos)
    elif args.compare:
        compare(videos, args.compare, args.metric, now)
    elif args.by:
        by_dimension(videos, args.by, args.metric, now)
    else:
        overview(videos, now)


def show_replays(videos):
    print(f"REPLAYS — videos with >= {insights.REPLAY_MIN_VIEWS} views averaging over 100% viewed")
    groups = {"all": videos, **insights.split_by(videos, "format_version")}
    for label, group in groups.items():
        replaying, eligible = insights.replay_share(group)
        if eligible < insights.MIN_COHORT:
            print(f"  {label:<8} insufficient data ({eligible} eligible)")
        else:
            print(f"  {label:<8} {replaying}/{eligible} ({100 * replaying / eligible:.0f}%)")


if __name__ == "__main__":
    main()
