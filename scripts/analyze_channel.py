"""Historical content-performance analysis (PRD R4.3).

Downloads all channel videos' public metadata via OAuth, recovers
question+answers from descriptions, classifies topics via Gemini, and
reports which content performs above/below the channel's age-adjusted
baseline.

Usage: venv/bin/python scripts/analyze_channel.py
Env:   YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN,
       GEMINI_API_KEY (topic classification)

Outputs: analysis/channel_videos.csv, analysis/topic_performance.md
Re-runnable: fetches fresh stats each time; safe to re-run as data grows.
"""

import csv
import datetime
import json
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import analytics, config, llm  # noqa: E402  (config loads .env)

OUT_DIR = config.ROOT / "analysis"

TAXONOMY = [
    "relationships-dating", "money-work", "dark-morbid", "politics-news",
    "fame-celebrity", "nostalgia", "humor-absurd", "sex-adjacent",
    "health-body", "hypotheticals", "life-advice", "other",
]

MIN_AGE_DAYS = 7  # too-fresh videos have meaningless view counts

STOPWORDS = set("""a an and are as at be been but by for from had has have he her his i if in is it its
just me my not of on one or our out she so that the their them they this to was we were what when which
who will with you your whats youve dont didnt im its ive youre thats
""".split())


# ---------------------------------------------------------------- fetch


def fetch_all_videos(yt):
    items = analytics.list_uploaded_videos(yt, part="contentDetails")
    ids = [it["contentDetails"]["videoId"] for it in items]

    videos = []
    for it in analytics.fetch_video_details(yt, ids, part="snippet,statistics,contentDetails"):
        sn, st = it["snippet"], it.get("statistics", {})
        videos.append({
            "video_id": it["id"],
            "published_at": sn["publishedAt"],
            "title": sn["title"],
            "description": sn.get("description", ""),
            "duration": it.get("contentDetails", {}).get("duration", ""),
            "views": int(st.get("viewCount", 0)),
            "likes": int(st.get("likeCount", 0)),
            "comments": int(st.get("commentCount", 0)),
        })
    return videos


# ---------------------------------------------------------------- parse


def parse_description(desc):
    """Recover (question, answers_text) from the stable description format."""
    q = re.search(r"Today's top AskReddit post:\s*(.+)", desc)
    answers = re.findall(r"^\s*\d+\.\s*(.+)$", desc, flags=re.MULTILINE)
    return (q.group(1).strip() if q else None), " ".join(answers)


def age_days(published_at, now):
    pub = datetime.datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    return max(0.04, (now - pub).total_seconds() / 86400)


# ---------------------------------------------------------------- topic classification


def _generate_with_retry(prompt, tries=5):
    """Free-tier friendly: back off on 429/503, honoring Retry-After. Never print
    exception bodies — requests' HTTPError message embeds the URL including the
    API key."""
    delay = 15
    for attempt in range(tries):
        try:
            return llm._generate(prompt)
        except requests.HTTPError as e:
            code = e.response.status_code if e.response is not None else "?"
            if code in (429, 503) and attempt < tries - 1:
                retry_after = e.response.headers.get("Retry-After") if e.response is not None else None
                wait = int(retry_after) if retry_after and retry_after.isdigit() else delay
                print(f"  gemini {code}; retrying in {wait}s")
                time.sleep(wait)
                delay = min(delay * 2, 120)
            else:
                raise RuntimeError(f"gemini failed with HTTP {code}") from None


def classify_topics(questions):
    """question -> bucket via Gemini, batched. Results are cached on disk so
    re-runs (and quota-interrupted runs) only classify new questions.
    Unclassified -> 'other'."""
    cache_path = OUT_DIR / "topics_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    missing = [q for q in questions if q not in cache]
    print(f"topics: {len(cache)} cached, {len(missing)} to classify")

    for i in range(0, len(missing), 80):
        batch = missing[i:i + 80]
        numbered = "\n".join(f"{j + 1}. {q}" for j, q in enumerate(batch))
        prompt = (
            "Classify each numbered question into exactly one of these topics: "
            + ", ".join(TAXONOMY)
            + ".\nReturn only lines of the form '<number>. <topic>' with no other text.\n\n"
            + numbered
        )
        try:
            reply = _generate_with_retry(prompt)
            for m in re.finditer(r"(\d+)\.\s*([a-z-]+)", reply):
                idx, topic = int(m.group(1)) - 1, m.group(2)
                if 0 <= idx < len(batch) and topic in TAXONOMY:
                    cache[batch[idx]] = topic
            cache_path.write_text(json.dumps(cache, indent=0))
            print(f"  classified {min(i + 80, len(missing))}/{len(missing)}")
        except Exception as e:
            print(f"classification batch failed ({e}); leaving batch unclassified")
        time.sleep(7)  # stay under free-tier RPM
    return defaultdict(lambda: "other", cache)


# ---------------------------------------------------------------- analysis


def age_adjusted_residuals(videos, now):
    """Residual of log-views vs the channel's log-age trend; >0 = overperformed."""
    xs = np.array([math.log(age_days(v["published_at"], now)) for v in videos])
    ys = np.array([math.log1p(v["views"]) for v in videos])
    slope, intercept = np.polyfit(xs, ys, 1)
    for v, x, y in zip(videos, xs, ys):
        v["residual"] = float(y - (slope * x + intercept))
    return slope, intercept


def topic_table(videos, key="residual"):
    """Per-topic median residual, ordered best to worst."""
    by_topic = defaultdict(list)
    for v in videos:
        by_topic[v["topic"]].append(v)
    rows = []
    for topic, vs in by_topic.items():
        res = [v[key] for v in vs]
        rows.append({
            "topic": topic, "n": len(vs),
            "median_residual": analytics.median(res),
            "median_views": analytics.median([v["views"] for v in vs]),
            "over_rate": sum(r > 0 for r in res) / len(res),
        })
    return sorted(rows, key=lambda r: -r["median_residual"])


def rank_correlation(rows_a, rows_b, min_n=3):
    """Spearman rho between two eras' topic orderings.

    This is the question R4.4 actually needs answered: not "what is each topic
    worth" (per-bucket medians on the current cohort are far too thin for that)
    but "does the pre-overhaul ordering still hold for the format we ship now?"
    A rank correlation over ~12 buckets survives thin buckets far better than
    any individual median does."""
    a = {r["topic"]: r["median_residual"] for r in rows_a if r["n"] >= min_n}
    b = {r["topic"]: r["median_residual"] for r in rows_b if r["n"] >= min_n}
    shared = sorted(set(a) & set(b))
    if len(shared) < 4:
        return None, shared
    def ranks(d):
        order = sorted(shared, key=lambda t: d[t])
        return {t: i for i, t in enumerate(order)}
    ra, rb = ranks(a), ranks(b)
    xs = np.array([ra[t] for t in shared], dtype=float)
    ys = np.array([rb[t] for t in shared], dtype=float)
    return float(np.corrcoef(xs, ys)[0, 1]), shared


def tokenize(text):
    words = re.findall(r"[a-z']+", text.lower())
    words = [w.strip("'") for w in words if w.strip("'") not in STOPWORDS and len(w) > 2]
    return words + [f"{a} {b}" for a, b in zip(words, words[1:])]


def distinctive_terms(top_docs, bottom_docs, k=15, min_df=3):
    """Log-odds (add-1) of document frequencies, top vs bottom quartile."""
    def doc_freq(docs):
        df = Counter()
        for d in docs:
            df.update(set(tokenize(d)))
        return df

    df_top, df_bot = doc_freq(top_docs), doc_freq(bottom_docs)
    scores = {}
    for term in set(df_top) | set(df_bot):
        if df_top[term] + df_bot[term] < min_df:
            continue
        p_top = (df_top[term] + 1) / (len(top_docs) + 2)
        p_bot = (df_bot[term] + 1) / (len(bottom_docs) + 2)
        scores[term] = math.log(p_top / p_bot)
    ranked = sorted(scores.items(), key=lambda kv: kv[1])
    return ranked[-k:][::-1], ranked[:k]


# ---------------------------------------------------------------- main


def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    OUT_DIR.mkdir(exist_ok=True)

    videos = fetch_all_videos(analytics.youtube_client())
    print(f"fetched {len(videos)} videos")

    for v in videos:
        v["question"], v["answers"] = parse_description(v["description"])
        v["age_days"] = round(age_days(v["published_at"], now), 1)
        v["upload_slot"] = datetime.datetime.fromisoformat(
            v["published_at"].replace("Z", "+00:00")).hour

    sample = [v for v in videos if v["question"] and v["age_days"] >= MIN_AGE_DAYS]
    print(f"analyzable (parsed question, age>={MIN_AGE_DAYS}d): {len(sample)}")

    # Era split. `upload_log.csv` is exactly the current-format cohort (v2+);
    # everything older is pre-overhaul v1. Same cohort definition R4.7 uses for
    # `logged_uploads`, which the README already names as the one to decide on.
    logged = set()
    if config.UPLOAD_LOG.exists():
        with open(config.UPLOAD_LOG) as f:
            logged = {r["video_id"] for r in csv.DictReader(f)}
    for v in videos:
        v["era"] = "current" if v["video_id"] in logged else "pre-overhaul"

    slope, _ = age_adjusted_residuals(sample, now)

    # Residuals again WITHIN each era. The global fit absorbs the format's own
    # ~6x distribution gain into the age slope, since current-format videos are
    # both younger and better-performing; a within-era fit removes the era's
    # level so the two topic orderings are comparable.
    eras = {}
    for name in ("pre-overhaul", "current"):
        vs = [v for v in sample if v["era"] == name]
        if len(vs) >= 10:
            age_adjusted_residuals(vs, now)
            for v in vs:
                v["era_residual"] = v["residual"]
            eras[name] = vs
        print(f"  era {name}: {len(vs)} analyzable")
    # restore the whole-channel residuals for every other table below
    age_adjusted_residuals(sample, now)

    topics = classify_topics({v["question"] for v in sample})
    # Snapshot the keys BEFORE the loop below: `topics` is a defaultdict, so
    # reading a missing question inserts it as "other" and the coverage check
    # would then see 100% resolved no matter what failed.
    resolved = set(topics)
    for v in videos:
        v["topic"] = topics[v["question"]] if v.get("question") else ""

    # classify_topics defaults unresolved questions to "other", so a Gemini
    # outage produces a report that looks entirely normal while most of the
    # sample sits in one meaningless bucket. Fail loudly instead — and check the
    # current era separately, since it is the newest content and therefore the
    # least likely to be already cached.
    for name, vs in [("overall", sample)] + list(eras.items()):
        unresolved = sum(1 for v in vs if v["question"] not in resolved) / max(1, len(vs))
        if unresolved > 0.15:
            sys.exit(f"ABORT: {unresolved:.0%} of the {name} sample is unclassified "
                     f"(Gemini failures). Re-run when the API recovers — the cache "
                     f"keeps what did classify, so a re-run only retries the rest.")

    # ---- write full CSV ----
    fields = ["video_id", "published_at", "age_days", "upload_slot", "title", "question",
              "answers", "topic", "duration", "views", "likes", "comments", "residual"]
    with open(OUT_DIR / "channel_videos.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for v in sorted(videos, key=lambda v: v["published_at"]):
            w.writerow(v)

    # ---- per-topic table ----
    topic_rows = topic_table(sample)
    era_tables = {name: topic_table(vs, key="era_residual") for name, vs in eras.items()}
    rho, shared = (rank_correlation(era_tables["pre-overhaul"], era_tables["current"])
                   if len(era_tables) == 2 else (None, []))

    # ---- distinctive terms, top vs bottom quartile ----
    ranked = sorted(sample, key=lambda v: v["residual"])
    q = len(ranked) // 4
    docs = lambda vs: [f"{v['question']} {v['answers']}" for v in vs]
    winners, losers = distinctive_terms(docs(ranked[-q:]), docs(ranked[:q]))

    slot_med = {s: analytics.median([v["residual"] for v in sample if v["upload_slot"] == s])
                for s in sorted({v["upload_slot"] for v in sample})}

    # ---- report ----
    lines = [
        "# Channel content-performance analysis (PRD R4.3)",
        "",
        f"Generated {now.date()} · {len(videos)} videos fetched, {len(sample)} analyzed "
        f"(parsed + ≥{MIN_AGE_DAYS} days old) · age model: log-views slope {slope:.2f}",
        "",
        "Performance metric: **age-adjusted residual** — how far a video's log-views sit above/below",
        "the channel's own age trend. residual > 0 = overperformed for its age. Raw views are NOT",
        "comparable across months and are shown only for scale.",
        "",
        "## Topic performance",
        "",
        "| Topic | n | median residual | median views | % overperforming |",
        "|---|---|---|---|---|",
    ]
    for r in topic_rows:
        flag = " ⚠️ small n" if r["n"] < 10 else ""
        lines.append(f"| {r['topic']}{flag} | {r['n']} | {r['median_residual']:+.2f} "
                     f"| {r['median_views']} | {r['over_rate']:.0%} |")
    # ---- era comparison: does the pre-overhaul topic prior still hold? ----
    lines += ["", "## Does the topic prior survive the format change? (R4.4 gate)", ""]
    if len(era_tables) < 2:
        lines += ["Not enough videos in one of the two eras to compare.", ""]
    else:
        lines += [
            "The table above pools eras. R4.4 would seed a ranker from these priors, but they",
            "were measured almost entirely on pre-overhaul v1 content, and v1->v4 moved median",
            "views ~6x (PRD §4 Review 2). Below, residuals are refit **within** each era, so the",
            "era's own level is removed and only the topic ordering is compared.",
            "",
            "| Topic | v1 n | v1 residual | current n | current residual |",
            "|---|---|---|---|---|",
        ]
        cur = {r["topic"]: r for r in era_tables["current"]}
        for r in era_tables["pre-overhaul"]:
            c = cur.get(r["topic"])
            cn = str(c["n"]) if c else "—"
            cr = f"{c['median_residual']:+.2f}" if c else "—"
            thin = " ⚠️" if c and c["n"] < 5 else ""
            lines.append(f"| {r['topic']}{thin} | {r['n']} | {r['median_residual']:+.2f} | {cn} | {cr} |")
        lines += [""]
        if rho is None:
            lines += [f"**Too few shared topic buckets ({len(shared)}) to correlate the orderings.**", ""]
        else:
            verdict = ("the prior TRANSFERS — the ranker may seed from the v1 table"
                       if rho >= 0.5 else
                       "the prior does NOT transfer — do not seed a ranker from the v1 table"
                       if rho <= 0.2 else
                       "INCONCLUSIVE — weak agreement, not enough to seed a ranker on")
            lines += [
                f"**Spearman rho = {rho:+.2f}** across {len(shared)} shared buckets "
                f"(buckets with n<3 in either era excluded): {verdict}.",
                "",
                "Read the rho, not the individual current-era medians — per-bucket n is small,",
                "but the ordering across ~10 buckets is far more robust than any one median.",
                "",
            ]

    lines += [
        "",
        "## Distinctive terms (top quartile vs bottom quartile)",
        "",
        "| In overperformers | In underperformers |",
        "|---|---|",
    ]
    for (wt, _), (lt, _) in zip(winners, losers):
        lines.append(f"| {wt} | {lt} |")
    lines += [
        "",
        "## Upload slot",
        "",
        "| UTC hour | median residual |",
        "|---|---|",
    ] + [f"| {s:02d}:00 | {m:+.2f} |" for s, m in slot_med.items()] + [
        "",
        "## Caveats (read before acting)",
        "",
        "- **Single snapshot.** Views are lifetime totals adjusted by a fitted age curve, not true",
        "  views@7d. The weekly snapshotting in R4.2 will fix this going forward.",
        "- **Correlation ≠ causation.** Topic buckets with few videos (⚠️) are noise-prone.",
        "- **Suppression vs. interest is not separable** from this data — but both imply the same",
        "  action for weak topics.",
        "- **Upload-slot medians are era-confounded**: posting times changed over the channel's life,",
        "  so slot differences partly encode channel age/maturity. Don't reschedule from this table.",
        "- The pooled topic table is still dominated by pre-v2 videos; for anything that",
        "  drives selection, read the era-comparison section rather than the pooled table.",
        "- Proposed `BLOCKED_TOPICS` candidates require owner approval before any gate ships (R4.4).",
    ]
    (OUT_DIR / "topic_performance.md").write_text("\n".join(lines))
    print(f"wrote {OUT_DIR}/channel_videos.csv and topic_performance.md")


if __name__ == "__main__":
    main()
