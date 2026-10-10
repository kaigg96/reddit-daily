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
  venv/bin/python scripts/report.py --at-age 7 --compare topic=dark-morbid
  venv/bin/python scripts/report.py --trajectory --metric views   # total weekly views (bet 2)

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
    print(f"  {'group':24} {'n':>4} {'median':>9} {'med age':>8} {'zero':>5} "
          f"{'<=' + str(insights.BURIED_VIEWS) + ' views':>11}")
    for c in rows:
        mark = "" if c.sufficient else "  (thin)"
        total = c.n + c.zero_view_count
        print(f"  {c.label:24} {c.n:>4} {c.median:>9.{insights.decimals(metric)}f} {c.median_age:>7.0f}d "
              f"{c.zero_view_count:>5} {c.buried_count:>4}/{total:<4}  {mark}")

    pair = [c for c in rows if c.label != "(unset)"]
    if len(pair) == 2:
        a, b = pair
        p = insights.buried_rate_p(a.buried_count, a.n + a.zero_view_count,
                                   b.buried_count, b.n + b.zero_view_count)
        print(f"\n  <={insights.BURIED_VIEWS} views, {a.label} vs {b.label}: "
              f"Fisher p={p:.3f} (two-sided; not age-matched, so read --within an era)")
        strata = insights.buried_strata(groups[a.label], groups[b.label])
        if len(strata) > 1:
            print(f"  pooled within each of {len(strata)} formats (Mantel-Haenszel): "
                  f"p={insights.buried_rate_p_pooled(strata):.3f}")
    elif len(pair) > 2:
        tests = insights.buried_vs_rest(groups)
        if tests:
            print(f"\n  <={insights.BURIED_VIEWS} views, each group (n>={insights.MIN_COHORT}) vs the rest, "
                  f"pooled within formats: {len(tests)} tests, so only p < {0.05 / len(tests):.4f} counts")
            for label, hits, n, p in tests:
                print(f"    {label:24} {hits:>3}/{n:<4} p={p:.3f}")

    if metric == Metric.VIEWS and len(pair) >= 2 and key != "format_version":
        # The other tail: the top 10% earn ~42% of views (--concentration), so
        # a field that makes hits would matter more than one that avoids zeros.
        hit = insights.top_share_hits(videos)
        if len(pair) == 2:
            a, b = (groups[c.label] for c in pair)
            print(f"\n  top 10% of views within its release, {pair[0].label} "
                  f"{sum(map(hit, a))}/{len(a)} vs {pair[1].label} {sum(map(hit, b))}/{len(b)}, "
                  f"pooled within formats: p="
                  f"{insights.buried_rate_p_pooled(insights.buried_strata(a, b, hit=hit)):.3f}")
        tests = [] if len(pair) == 2 else insights.buried_vs_rest(groups, hit=hit)
        if tests:
            print(f"\n  top 10% of views within its release, each group (n>={insights.MIN_COHORT}) "
                  f"vs the rest, pooled within formats: {len(tests)} tests, "
                  f"so only p < {0.05 / len(tests):.4f} counts")
            for label, hits, n, p in tests:
                print(f"    {label:24} {hits:>3}/{n:<4} p={p:.3f}")

    # Age spread warning — comparing these groups may be measuring age.
    ages = [c.median_age for c in rows if c.sufficient and c.median_age == c.median_age]
    if len(ages) >= 2 and max(ages) > 1.5 * min(ages):
        print(f"\n  NOTE: median ages range {min(ages):.0f}d–{max(ages):.0f}d. "
              f"Cross-group differences may reflect age, not the variable.\n"
              f"  Use --compare for an age-matched two-way test.")


def zeros(now, videos=None):
    """List 0-view videos, separating the two things that masquerade as
    suppression: owner-privatised videos, and zeroes inside channel-wide cold
    spells. Only the isolated ones are real per-video suppression candidates.
    `videos` defaults to the live Data API read."""
    if videos is None:
        videos = insights.load_channel_videos(now)
    groups = insights.classify_zero_views(videos, now)
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


def compare(videos, spec, metric, now, pool=None, min_views=1):
    """Age-matched two-way test on one upload_log field.

    Videos where the field is unset are excluded from both cohorts — see
    insights.split_cohorts for why that matters. Beside the verdict, the gap
    random arms of the same two sizes reach one time in ten with nothing
    switched (`insights.coin_floor`, over `pool`). Tests read at ~15 per arm
    had a 12-13% limit, the *median* chance gap (PRD §4, 2026-10-09).
    `min_views` reads only uploads with that many plays, whose averages are
    steady (PRD §4, R4); since that hides a change that buries uploads, the
    buried rate over every upload prints first."""
    key, _, value = spec.partition("=")
    a, b, unset = insights.split_cohorts(videos, key, value)
    if unset:
        print(f"({unset} video(s) have no {key} recorded — excluded from both cohorts)")
    if min_views > 1:
        buried = lambda vs: sum(1 for v in vs if v.views <= insights.BURIED_VIEWS)
        p = insights.buried_rate_p(buried(a), len(a), buried(b), len(b))
        print(f"buried (<={insights.BURIED_VIEWS} views), every upload: {key}={value} "
              f"{buried(a)}/{len(a)} vs {key}!={value} {buried(b)}/{len(b)}, "
              f"Fisher p={p:.3f} (two-sided)")
        a = [v for v in a if v.views >= min_views]
        b = [v for v in b if v.views >= min_views]
        print(f"(read below: only uploads with >= {min_views} views)")
    result = insights.compare(a, b, f"{key}={value}", f"{key}!={value}", now, metric)
    print(result.render())
    when = lambda vs: [v.true_published or v.published for v in vs]
    if result.a.sufficient and result.b.sufficient and result.age_matched:
        (a0, a1), (b0, b1) = ((min(when(c)), max(when(c))) for c in (a, b))
        if key == "format_version" or a0 > b1 or b0 > a1:
            # Arms from different weeks carry drift a random split cannot see.
            print("    chance: the arms come from different weeks, so no random split "
                  "prices this; a flag-day change reads with --release")
        else:
            pool = pool or videos
            span = insights.CHANCE_SPAN
            gap = insights.coin_floor(pool, metric, result.a.n, other=result.b.n, span=span,
                                      min_views=min_views)
            windows = len(insights.coin_windows(pool, metric, result.a.n, result.b.n, span,
                                                min_views))
            seen = f" with >= {min_views} views" if min_views > 1 else ""
            print(f"    chance: random arms of {result.a.n} and {result.b.n} from the newest "
                  f"{max(span, result.a.n + result.b.n)} uploads{seen} "
                  + (f"differ by {gap:.1%} one time in ten ({windows} window(s); few means "
                     f"rough); only a gap beyond that is a finding"
                     if gap is not None else "- too few uploads to say (see --placebo)"))
            # One arm reaching weeks further back compares eras, not arms (PRD §0 #3).
            start = max(a0, b0)
            if abs(a0 - b0).days > 14:
                print(f"    WARNING: one arm starts {abs(a0 - b0).days} days before the other; "
                      f"read the weeks both ran with --since {start.date()}")
    if key != "format_version":
        for era, sa, sb in insights.era_imbalance(a, b):
            print(f"    WARNING: uneven across releases ({era}: {sa:.0%} vs {sb:.0%}) — "
                  f"check with --within format_version={era}")


def release(version, key, target_age, min_uploads=None, within_spec=None):
    """The auto-revert check for a flag-day change (`/shift` §5, issue #16).

    Reads every upload at a *common age* from the weekly snapshot series, which
    is the only way a release ever becomes age-matched against the era it
    replaced (`insights.release_read`, shared with the Monday digest). Needs no
    YouTube credentials, so a scheduled shift can run it. `min_uploads`
    defaults to the release's pre-committed size (`RELEASE_MIN_UPLOADS`)."""
    if min_uploads is None:
        min_uploads = insights.RELEASE_MIN_UPLOADS.get(version, insights.MIN_COHORT)
    read = insights.release_read(version, key, target_age, within_spec)
    if read is None:
        sys.exit(f"No upload has a snapshot at ~{target_age:.0f} days old.")
    if within_spec:
        print(f"(within {within_spec}: both sides of the release read inside it)")
    for line in read.load.caveats():
        print(f"AGE-MATCHED: {line}")
    print()
    if read.unset:
        print(f"({read.unset} upload(s) have no {key} recorded — in neither cohort)")
    if read.later:
        print(f"({read.later} upload(s) postdate {version} — excluded, so this compares it "
              f"with what it replaced rather than with its own successors)")
    print(insights.render_release(read.comparisons, read.floors, read.triggers, min_uploads))
    print(insights.render_duration(read.release, read.before))
    within_length = insights.render_within_length(read)
    if within_length:
        print(within_length)


def _snapshot_metric_rows(metric_col="avg_view_duration_s", path=None):
    """Weekly-snapshot rows shaped for insights.trajectory.

    A blank engaged_views means the snapshot predates the column (2026-10-05)
    or the API did not report it: the row is skipped, never read as zero, so
    a week read before the column is incomplete rather than reported low."""
    import csv as _csv
    import datetime as _dt
    import os as _os
    root = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    path = path or _os.path.join(root, "analysis", "analytics_snapshots.csv")
    out = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for r in _csv.DictReader(f):
                try:
                    pub = _dt.datetime.fromisoformat(
                        (r.get("published_at") or "").replace("Z", "+00:00"))
                    snap = _dt.datetime.fromisoformat(
                        (r.get("snapshot_date") or "") + "T00:00:00+00:00")
                    if (metric_col == Metric.ENGAGED_VIEWS and not r.get(metric_col)
                            and float(r.get("views") or 0) > 0):
                        continue    # unreported; a blank on a zero-view row is a zero
                    val = float(r.get(metric_col) or 0)
                except (ValueError, TypeError):
                    continue
                out.append({"video_id": r.get("video_id"), "published": pub,
                            "snapshot": snap, "value": val})
    except OSError:
        pass
    return out


def _within_rows(rows, spec):
    """Snapshot rows of the logged uploads matching `--within`, all if unset.
    The channel-wide figure (views gained) is left out under a filter: it
    counts the back catalogue, which has no upload_log fields to filter on."""
    if not spec:
        return rows
    ids = insights.ids_within(spec)
    print(f"(within {spec}: {len(ids)} logged upload(s))")
    return [r for r in rows if r.get("video_id") in ids]


def _period_metrics(at_age=7, tolerance=4, half=3, root=None):
    """Metrics for the recent `half` publish-weeks vs the `half` before them.

    Every upload read at the same age, so the two periods are comparable.
    Duration comes from upload_log; the rest from the weekly snapshot.
    """
    import csv as _csv
    import datetime as _dt
    import os as _os
    root = root or _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

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

    best, every = {}, []
    try:
        with open(_os.path.join(root, "analysis", "analytics_snapshots.csv"),
                  encoding="utf-8", errors="ignore") as f:
            for r in _csv.DictReader(f):
                every.append(r)
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

    # A zero-view upload the owner made private is not suppression: drop it as
    # the offline loaders do, or zero_rate disagrees with every other read.
    privacy = insights._snapshot_privacy(every)
    buckets = {}
    for vid, (_, r, pub) in best.items():
        views = insights._optional_float(r.get("views")) or 0.0
        if insights._privatised_zero(vid, views, privacy):
            continue
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
        engaged = insights.engaged_per_100([r for _, r in rows])
        if engaged is not None:
            m["engaged_per_100"] = engaged
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
    if args.metric in (Metric.VIEWS, Metric.ENGAGED_VIEWS):
        return show_weekly_views(args)
    if args.metric != Metric.WATCH:
        print(f"--trajectory reads watch-seconds, views or engaged_views, not {args.metric}")
        return
    rows = _within_rows(_snapshot_metric_rows(), args.within)
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


def show_weekly_views(args):
    """`--trajectory --metric views`: total weekly views, bet 2's measure.
    `--metric engaged_views` reads the same totals in the bar's own unit."""
    age = args.at_age or 7
    col = args.metric
    series = insights.weekly_totals(_within_rows(_snapshot_metric_rows(col), args.within),
                                    at_age=age)
    if not series:
        print("no publish week is fully read yet")
        return
    print(f"Total {col} per publish week, every upload read at ~{age} days old")
    print("(complete weeks only: the newest are still filling in)\n")
    print(f"  {'week':10} {'n':>4} {'total':>8} {'per upload':>11}")
    for period, n, total in series:
        print(f"  {period:10} {n:>4} {total:>8.0f} {total / n:>11.0f}")
    gained = [] if args.within else insights.views_gained(_snapshot_metric_rows(col))[-13:]
    if gained:
        days = sum(d for _, _, d in gained)
        total = sum(g for _, g, _ in gained)
        unit = ("in engaged views, the Partner Program's unit:" if col == Metric.ENGAGED_VIEWS
                else "in play starts (the Partner Program\n  counts only the engaged share of "
                     "these: --engaged-share):")
        print(f"\n  Channel-wide, every video counted, {unit}"
              f"\n  {total:.0f} {col} gained over the last {days} days between snapshots"
              f" (~{total * 90 / days:.0f} per 90 days)")
    change = insights.totals_change(series)
    if change is None:
        print(f"\n  only {len(series)} complete weeks: 8 are needed to compare 4 with 4")
        return
    prior, recent, ratio = change
    print(f"\n  last 4 weeks {recent:.0f} vs the 4 before {prior:.0f}"
          + (f" (x{ratio:.2f})" if ratio else ""))
    if args.within:
        # A filter moves how many uploads each week holds, so the totals'
        # ratio mixes count with performance; per upload separates them.
        n_prior = sum(n for _, n, _ in series[-8:-4])
        n_recent = sum(n for _, n, _ in series[-4:])
        if n_prior and n_recent and prior:
            print(f"  per upload {recent / n_recent:.0f} vs {prior / n_prior:.0f} "
                  f"(x{(recent / n_recent) / (prior / n_prior):.2f}; "
                  f"{n_recent} vs {n_prior} uploads)")
    print("  Views swing 27-50% at a fixed age with nothing changed, so read"
          "\n  only a doubling or a halving as a change. Never a revert trigger.")


def show_catalogue(args):
    """`--catalogue`: is a fall in new uploads' views the channel's, or theirs?"""
    rows = insights.views_gained_by_age(_snapshot_metric_rows("views"))
    if not rows:
        print("fewer than two snapshots: no answer")
        return
    print("Views gained per day between snapshots, by each video's age at the earlier one\n")
    print(f"  {'snapshot':10} {'days':>4} {'60d+ old':>9} {'recent':>8}")
    for snap, old, recent, days in rows:
        print(f"  {snap.date()!s:10} {days:>4} {old / days:>9.0f} {recent / days:>8.0f}")
    old = sum(o for _, o, _, _ in rows)
    total = old + sum(r for _, _, r, _ in rows)
    if not total:
        print("\n  No views gained between these snapshots: nothing to split.")
        return
    print(f"\n  The old catalogue earned {old / total:.1%} of these views. It gets no new"
          "\n  uploads, so a step in its column at the same snapshot as one in the"
          "\n  recent column is the channel's distribution; a column in single digits"
          "\n  is too small to show one. Neither column is age-matched: judge uploads"
          "\n  with --trajectory.")


def show_concentration(args):
    """`--concentration`: are the views earned by a few hits? (PRD §0 R4)"""
    age = args.at_age or 7
    result = insights.views_concentration(_snapshot_metric_rows("views"), at_age=age)
    if result is None:
        print(f"fewer than {insights.MIN_COHORT} uploads read at ~{age} days: no answer")
        return
    n, total, top_n, top_total, biggest = result
    print(f"Views concentration, every upload read at ~{age} days old (n={n}, "
          f"{total:.0f} views)\n")
    print(f"  top 10% ({top_n} uploads) earned {top_total:.0f}: {top_total / total:.0%}")
    print(f"  biggest single upload: {biggest:.0f} ({biggest / total:.0%})")
    print(f"  mean upload {total / n:.0f}")


def show_hit_rates(videos, key):
    """`--concentration --by F`: which values of F are over-represented among
    the top 10% of uploads by views? (PRD §0 R5)"""
    rows, cut = insights.hit_rates(videos, key)
    print(f"Hits (the top 10% by views, {cut} of {len(videos)}) by {key}\n")
    print(f"  {'group':24} {'n':>4} {'hits':>5} {'rate':>6} {'Fisher p':>9}")
    for label, n, hits, p in rows:
        print(f"  {label:24} {n:>4} {hits:>5} {hits / n:>6.0%} {p:>9.3f}")
    print("\n  p is each group against the rest, two-sided. Read it at the bar its "
          "\n  question pre-committed, and within an era: eras differ in views.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--by", help="group by an upload_log field (format_version, topic, ...)")
    p.add_argument("--compare", help="age-matched two-way test, e.g. candidate_rank=1")
    p.add_argument("--within", metavar="KEY=VALUE",
                   help="restrict --compare/--by/--release/--trajectory to one group, "
                        "e.g. video_length=short, or exclude one with KEY!=VALUE "
                        "(uploads with the field unset are in neither)")
    p.add_argument("--since", metavar="YYYY-MM-DD",
                   help="restrict --compare/--by to uploads published on or after a "
                        "date, so a test reads only the weeks it ran (PRD §0 #3, #10)")
    p.add_argument("--min-views", type=int, default=1, metavar="N",
                   help="--compare reads watch time only over uploads with N or more "
                        "views, the buried rate printed beside it (PRD §4, R4)")
    p.add_argument("--release", metavar="VERSION",
                   help="auto-revert check on a flag-day change, e.g. v6: its uploads "
                        "vs the era it replaced, both read at the same age")
    p.add_argument("--min-uploads", type=int, default=None,
                   help="--release: no verdict until the release has this many "
                        "measurable uploads — the experiment's pre-committed size "
                        "(default: insights.RELEASE_MIN_UPLOADS, else 8)")
    p.add_argument("--release-key", default="format_version",
                   help="upload_log field --release splits on (default format_version; "
                        "use background_type for the b-roll switch)")
    p.add_argument("--at-age", type=float, metavar="DAYS",
                   help="read every upload at this age from the snapshot series "
                        f"(--release defaults to {insights.AGE_MATCH_TARGET_DAYS:.0f}); "
                        "with --compare or --by it age-matches an interleaved field "
                        "like topic, which one snapshot of today cannot")
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
    p.add_argument("--engaged-check", action="store_true",
                   help="R2: does the minutes column encode engaged views? latest snapshot only")
    p.add_argument("--engaged-share", action="store_true",
                   help="share of views the Partner Program counts (engaged / all play "
                        "starts), all videos and the last 90 days; latest snapshot only")
    p.add_argument("--placebo", action="store_true",
                   help="noise with nothing changed: consecutive batches (how a release "
                        "is judged) vs alternate days in the same weeks (PLAN C9)")
    p.add_argument("--slate", action="store_true",
                   help="how often the slate's topic for the selected post matches "
                        "the screen's (read before R4.4's firing rate)")
    p.add_argument("--catalogue", action="store_true",
                   help="views gained between snapshots, back catalogue (60+ days "
                        "old) vs recent uploads: did a drop hit the whole channel?")
    p.add_argument("--concentration", action="store_true",
                   help="share of 7-day views the top 10%% of uploads earn: "
                        "are views a hit-rate problem? (PRD R4)")
    p.add_argument("--metric", default=Metric.WATCH,
                   choices=[Metric.WATCH, Metric.VIEWS, Metric.PCT, Metric.LIKES, Metric.COMMENTS,
                            Metric.TOTAL, Metric.ENGAGED, Metric.ENGAGED_SHARE,
                            Metric.ENGAGED_VIEWS])
    p.add_argument("--offline", action="store_true",
                   help="read the committed weekly snapshot instead of the live "
                        "YouTube API (no credentials needed; a week stale)")
    args = p.parse_args()
    if args.within:
        try:
            insights.ids_within(args.within)
        except ValueError as e:
            sys.exit(f"--within {args.within}: {e}")

    # Every other mode returns before the filter, so it would print unfiltered
    # numbers under a --since the reader believes applied.
    early = (args.scorecard, args.trajectory, args.engaged_check, args.engaged_share,
             args.placebo, args.catalogue, args.slate, args.zeros, args.release)
    if args.since and (any(early) or not (args.compare or args.by)):
        sys.exit("--since restricts --compare and --by only")
    if args.min_views > 1 and (any(early) or not args.compare):
        sys.exit("--min-views applies to --compare only")
    if args.min_views > 1 and args.metric not in (Metric.WATCH, Metric.PCT, Metric.ENGAGED,
                                                  Metric.ENGAGED_SHARE):
        # Per-play ratios only. A count (views, likes, total watch time) rises
        # with views, so leaving out the uploads with few would hide the very
        # effect it measures, such as a change that gets fewer uploads seen.
        sys.exit(f"--min-views reads per-play averages among seen uploads; --metric "
                 f"{args.metric} must count every upload")

    now = datetime.datetime.now(datetime.timezone.utc)

    if args.at_age is not None and args.at_age < insights.MIN_AGE_DAYS:
        # Younger reads are mostly reporting lag: excluding the zeros leaves a
        # median over whichever videos Analytics happened to report first.
        sys.exit(f"--at-age {args.at_age:g} is under {insights.MIN_AGE_DAYS} days, where "
                 f"Analytics has not yet reported many uploads; read at "
                 f"{insights.MIN_AGE_DAYS} or later.")

    if args.scorecard:     # many metrics; no single one can judge this channel
        show_scorecard(args)
        return

    if args.trajectory:     # the only surface that answers "are we improving?"
        show_trajectory(args)
        return

    if args.engaged_check:  # one snapshot, per video: no ages to match
        import csv as _csv
        from src import config
        with open(config.ANALYTICS_SNAPSHOTS) as f:
            rows = list(_csv.DictReader(f))
        latest = max(r["snapshot_date"] for r in rows)
        n, med, within = insights.engaged_check(r for r in rows if r["snapshot_date"] == latest)
        if not n:
            print(f"{latest}: no rows carry engaged_views")
        else:
            print(f"{latest}: implied/actual engaged share, n={n} videos with >=20 views: "
                  f"median {med:.2f}, {within:.0%} within 10% of 1")
        return

    if args.engaged_share:  # lifetime totals in one snapshot: a ratio, not a comparison
        import csv as _csv
        from src import config
        with open(config.ANALYTICS_SNAPSHOTS) as f:
            rows = list(_csv.DictReader(f))
        latest = max(r["snapshot_date"] for r in rows if r.get("engaged_views"))
        rows = [r for r in rows if r["snapshot_date"] == latest]
        cut = (datetime.datetime.fromisoformat(latest).replace(tzinfo=datetime.timezone.utc)
               - datetime.timedelta(days=90))
        print(f"Engaged share of views, snapshot {latest} (lifetime totals per video)")
        for label, since in (("all videos", None), ("published in the last 90 days", cut)):
            n, views, engaged, share = insights.engaged_share(rows, since)
            verdict = (f"{share:.0%}" if share is not None else
                       f"insufficient data (<{insights.ENGAGED_SHARE_MIN_VIDEOS} videos)")
            print(f"  {label:32} n={n:<5} views {views:>8,}  engaged {engaged:>8,}  share {verdict}")
        print("\n  The Partner Program's 10M bar counts qualified (engaged) views, so a"
              "\n  gap stated in views understates it by 1/share.")
        return

    if args.placebo:        # nothing switched: what each test design reads as noise
        load = insights.load_videos_at_age(args.at_age or 7)
        print(f"Noise with nothing changed, uploads read at ~{args.at_age or 7} days old "
              f"(n={len(load.videos)})\n")
        print(f"  {'metric':15} {'release-style':>14} {'alternate days':>15}")
        for m in (Metric.WATCH, Metric.VIEWS):
            r = insights.drift_floor(load.videos, m)
            a = insights.alternation_floor(load.videos, m)
            fmt = lambda x: f"{x:.0%}" if x is not None else "-"
            print(f"  {m:15} {fmt(r):>14} {fmt(a):>15}")
        print("\n  release-style: median swing between consecutive batches of 8"
              "\n  alternate days: median gap between odd- and even-day uploads"
              "\n  within the same 16. Smaller is a finer detection limit.")
        # A coin per run (PRD §0 #14): the gap random halves of the same weeks
        # reach 1 time in 10, by arm size. A keep threshold must clear it.
        print("\n  coin per run, 90th-percentile gap between random arms:")
        for arm in (15, 30, 45):
            row = "  ".join(f"{m} {fmt(insights.coin_floor(load.videos, m, arm))}"
                            for m in (Metric.WATCH, Metric.VIEWS))
            n = len(insights.coin_windows(load.videos, Metric.VIEWS, arm))
            print(f"    {arm} per arm: {row}   ({n} window(s); few means rough)")
        return

    if args.catalogue:      # the snapshot series, channel-wide
        show_catalogue(args)
        return

    if args.concentration and not args.by:  # the snapshot series, like --trajectory
        show_concentration(args)
        return

    if args.slate:          # reads only the upload log: no analytics involved
        show_slate_agreement()
        return

    if args.zeros:          # the Data API (near-real-time), or offline the weekly snapshot
        if args.offline:
            vids, asof = insights.load_channel_videos_offline()
            if vids is None:
                # Refusing is the honest answer: the classification turns on
                # privacy status, and calling privatised videos suppression is
                # the specific wrong conclusion classify_zero_views exists to prevent.
                sys.exit("--zeros needs privacy status, which the newest snapshot does "
                         "not record (snapshots carry it from the first weekly run after "
                         "2026-10-08); it cannot be answered offline.")
            print(f"(offline: the {asof:%Y-%m-%d} snapshot; ages and views as of then)\n")
            zeros(asof, vids)
            return
        try:
            zeros(now)
        except KeyError as e:
            # A shift holds no YouTube secrets; say so rather than die on a
            # bare KeyError, and name what it can read instead. Any other
            # KeyError is a real fault and stays loud.
            if not str(e.args[0] if e.args else "").startswith("YOUTUBE_"):
                raise
            sys.exit(f"No YouTube credentials ({e} is unset), so --zeros cannot run "
                     f"here.\nThe weekly digest runs it with credentials; offline, "
                     f"`--at-age 7 --by bg_clip --metric views` reads the buried rate.")
        return

    if args.release:    # reads the snapshot series at a fixed age, not one point in time
        # The rule judges watch-seconds, with total watch time and views beside
        # it. Any other --metric used to be dropped silently, so `--release v7
        # --metric engaged_share` printed watch-seconds as if it were the share
        # (2026-10-09, before #8's read).
        if args.metric not in (Metric.WATCH, Metric.VIEWS, Metric.TOTAL):
            age = insights.AGE_MATCH_TARGET_DAYS if args.at_age is None else args.at_age
            within = f" --within {args.within}" if args.within else ""
            sys.exit(f"--release judges watch-seconds by its rule (views and total "
                     f"watch time beside it) and does not read --metric {args.metric}. "
                     f"Read it per release instead: --by {args.release_key} --metric "
                     f"{args.metric} --at-age {age:g}{within}")
        release(args.release, args.release_key,
                insights.AGE_MATCH_TARGET_DAYS if args.at_age is None else args.at_age,
                args.min_uploads, args.within)
        return

    if (args.metric in (Metric.ENGAGED_SHARE, Metric.ENGAGED_VIEWS)
            and args.at_age is None and not args.offline):
        sys.exit(f"--metric {args.metric} comes from the weekly snapshot, which the "
                 f"live path does not read: add --offline or --at-age.")

    if args.at_age is not None:
        # A field that alternates between uploads (topic, voice) is not a flag
        # day, but one snapshot still reads a recent-heavy cohort younger, and
        # `compare` rightly refuses it. Every upload at one age removes that.
        load = insights.load_videos_at_age(args.at_age)
        videos, now = load.videos, load.anchor
        for line in load.caveats():
            print(f"AGE-MATCHED: {line}")
        print()
    elif args.offline:
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

    pool = videos           # the chance gap reads every upload, not one filtered slice
    if args.within:
        videos = insights.within(videos, args.within)
        print(f"(within {args.within}: {len(videos)} upload(s))")
    if args.since:
        try:
            since = datetime.date.fromisoformat(args.since)
        except ValueError:
            sys.exit(f"--since takes a date, YYYY-MM-DD, not {args.since!r}")
        videos = insights.since(videos, since)
        print(f"(since {since}: {len(videos)} upload(s))")
    if not videos:
        sys.exit("No analyzable uploads found.")

    if args.replays:
        show_replays(videos)
    elif args.compare:
        compare(videos, args.compare, args.metric, now, pool, args.min_views)
    elif args.by and args.concentration:
        show_hit_rates(videos, args.by)
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


def show_slate_agreement():
    import csv
    from collections import Counter
    from src import config
    with open(config.UPLOAD_LOG) as f:
        agree, labelled, pairs = insights.slate_agreement(csv.DictReader(f))
    print("SLATE AGREEMENT — the slate's topic for the selected post vs the screen's")
    if labelled < insights.MIN_COHORT:
        print(f"  insufficient data for a rate: {agree}/{labelled} agree "
              f"(need {insights.MIN_COHORT})")
    else:
        print(f"  {agree}/{labelled} agree ({100 * agree / labelled:.0f}%)")
    for (screen, slate), n in Counter(pairs).most_common():
        print(f"  screen {screen:<20} slate {slate:<20} x{n}")

    with open(config.UPLOAD_LOG) as f:
        fired, read = insights.slate_firing(csv.DictReader(f))
    print("\nR4.4 FIRING RATE — rank 1 weak-tier and a strong-tier candidate in the top 3")
    if read < insights.SLATE_FIRING_MIN_RUNS:
        print(f"  insufficient data: {read} runs with a slate, the rule reads at "
              f"{insights.SLATE_FIRING_MIN_RUNS} ({fired} fired so far)")
    else:
        print(f"  fired on {fired} of {read} runs ({100 * fired / read:.0f}%)")
        if fired:
            print(f"  at 2 uploads a day, 20 firings take ~{20 * read / fired / 2:.0f} days")


if __name__ == "__main__":
    main()
