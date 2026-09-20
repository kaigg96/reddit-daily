# Work log

One entry per shift, newest first. **This is not a status tracker** — status
lives in [PRD.md](PRD.md) §0 and code health in [TECH_DEBT.md](TECH_DEBT.md).
This file records *what happened, what's queued next, and what's blocked on
what*, so a cold session can resume without re-deriving anything.

Keep it to ~10 entries; delete older ones (git history keeps them).

**Every entry starts with an allocation line**, in exactly this shape, so the
next shift can compute starvation floors and `/audit` can see whether slices
are being finished or filled:

    Allocation (planned→actual %): rounds 10→8 · maintenance 15→25 · pm 15→12 · research 10→0 · feature 40→35 · close 10→10

`0` actual is fine and often correct — say why in the entry. Read it with
`venv/bin/python scripts/context_budget.py --allocation`.

---

## 2026-09-20 (evening) — maintenance + PM (a guardrail that cost quota daily)

    Allocation (planned→actual %): rounds 10→10 · maintenance 45→45 · security 10→5 · pm 15→20 · research 10→0 · feature 10→10 · close 10→10

No preemption: both uploads landed, `prev_post.txt` intact, nothing waiting to
ship, recorded FAIL stale by 16 commits.

**The release gate could never skip itself, and the early upload paid.**
`validate-release.yml`'s "don't re-validate a commit that already passed"
branch cannot fire: recording a verdict *commits to `main`*, so next morning
HEAD is always past the sha just recorded. `a4fb38c` names `c6ee5f7` and sits
directly on top of it. Cost: **6 of the day's 20 Gemini requests, every day,
forever** — shared with live uploads, and the ~05:00 publish is *last* in the
07:00→07:00 window, so it starves first. That is why the 05:01 upload shipped
the raw Reddit question as its title (`title_ok=0`).

Fix compares the code the gates exercise, expires a PASS after 7 days (the
model drifts with no commit of ours), and runs the unit tests unconditionally
— free, and **the only pytest anywhere in CI**. Logic moved from bash into a
tested function; the version it replaces failed silently and nothing could
have noticed.

**Half of it is not mine to ship.** `should_validate` + 12 tests landed
(`4cfc1c4`), inert. The wiring is **issue #14**: `.github/workflows/**` is
protected precisely because a shift editing it "could disable its own
supervision", and this reduces how often that supervision runs.

**Two process findings.** (1) A shift cannot propose a workflow change on a
branch either — the push is rejected for lack of `workflows` permission, so
`.escalations/README.md`'s "propose freely on a branch" is not the real route
for these; diff inlined in #14. (2) `report.py` dies on
`KeyError: 'YOUTUBE_REFRESH_TOKEN'` — shifts are rightly denied YouTube
secrets, so **a scheduled shift can answer no performance question at all.**

**PM.** Three TECH_DEBT items described already-shipped work (merged
`get_metadata`, the `*_ok` columns, `title_style` blanking). PRD §4 still said
8–14 requests/day, contradicting §2's corrected 4–10. Fixed; items 25 → 24.

**Feature (10%) ended in a blocker, not code.** R4.4 is gated on re-running
the topic analysis, which needs `report.py` — see finding (2). The fix is an
offline read-only loader in `insights.py`; not rushed at shift end, because
`load_videos` encodes two rules a naive snapshot reader breaks silently.
Details in `TECH_DEBT.md`.

**Research 0%** — nothing above the bar once the gate bug surfaced; 2
consecutive shifts at 0, floor is 5. **Security clean** — secrets never
committed and still ignored, permissions scoped.

**Queued next:** (1) the offline analytics loader, unblocking R4.4 and every
future PM lane; (2) #14 needs the owner before the quota fix does anything;
(3) tomorrow's 08:17 gate is the authoritative verdict on the screen fix — it
*will* run, since `src/screen.py` and `scripts/` changed; (4)
`replay_screen.py`'s FLIRT case is still a memorization check.

**Spent no Gemini, no Polly** — today's window was already drawn down.

## 2026-09-20 (afternoon) — maintenance (stale-then-real gate failure)

    Allocation (planned→actual %): rounds 10→5 · maintenance 15→70 · pm 15→15 · research 10→0 · feature 40→0 · close 10→10

The recorded FAIL was stale, but re-checking found a real, different fault:
with reasoning restored, the R4.6 screen still missed a paraphrase of the
identical `sexual_suggestive` shape while catching the literal in-prompt
example. **One example doesn't generalize a category.** Fixed in `89bc245`,
pinned by a test; full finding in `TECH_DEBT.md`.

**A fix verified once, live, is a sample of one.**

## 2026-09-20 — maintenance (incident-led)

    Allocation (planned→actual %): rounds 10→10 · maintenance 15→65 · pm 15→20 · research 15→0 · feature 35→0 · close 10→5

**FAULT 1 — the screen lost its judgment, live.** Disabling Gemini thinking
everywhere (2026-09-19) fixed title latency and silently broke the one genuine
judgment task. 512 reasoning tokens restored, pinned by a test. **The CI gate
is the only reason this surfaced before it cost an upload.**

**FAULT 2 — the first scheduled shift did nothing and reported success.**
`claude-code-action` grants no shell access without `--allowedTools`. Fixed.
**A shift that leaves no trace is indistinguishable from one that never ran**,
and every health signal reads `WORKLOG.md`.

**Both faults were caught by the checks, not by looking. Green is not
evidence.**

## 2026-09-19 — first session (pre-dates the allocation model)

    Allocation (planned→actual %): rounds 0→0 · maintenance 0→30 · pm 0→50 · research 0→5 · feature 0→5 · close 0→10

Built the workflow rather than running it. Merged `v6`; shipped `/shift` +
`/audit`. **Still open:** `escalations.yml` discards the issue number it
creates; no automated *video* check. **Every threshold was an unvalidated
guess** — under test (`DECISIONS.md` D4, D5).
