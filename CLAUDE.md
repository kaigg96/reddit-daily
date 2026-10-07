# CLAUDE.md

Loaded every session. Only rules that apply broadly and that you would get
wrong without — everything else lives where it is read on demand. Keep it under
the budget in `scripts/context_budget.py`; a long file gets ignored.

**IMPORTANT — this file is advisory and has been ignored in practice.** On
2026-09-20 a shift read §5 and added an AI-attribution trailer anyway. So:
**any rule whose violation would be unacceptable must ALSO be enforced in code
or CI.** Enforced rules are marked ⚙ and named in `.github/workflows/guardrails.yml`.
When you add a rule, decide which kind it is. If advisory compliance is not good
enough, enforcing it is part of adding it.

**What this is:** a small media company. The Shorts channel is its first
product, and the goal is **monetization** — improve the company, not just the
channel (D12). Who owns what and who decides: `ORG.md`.

Start a session with `/pickup`, or `/shift` when there is no specific task.

## 1. Money — Polly is the only billed service

AWS Polly is a real invoice (~$0.90/month). Gemini and YouTube are free-tier.

- ⚙ **Never synthesize in bulk** — no loops over a corpus, no batch variants, no
  regenerating the back catalogue. A run synthesizes 5 segments; if you are
  about to make materially more calls than that, stop. Enforced by
  `POLLY_CHAR_BUDGET` (`src/tts.py`).
- **Never retry Polly without a hard cap.** A failed call still bills.
- **Reuse the mp3s in `assets/gen/`** when iterating on visuals.
- ⚙ **`Engine="neural"` is a deliberate paid choice.** Do not downgrade it to
  save money, or upgrade to generative, without asking. Cost work here means
  removing wasted calls, never reducing audio quality.
- ⚙ **The AWS-side controls must stay as the owner set them** (key scope,
  budget, its automatic deny, the usage alarm). `scripts/money_check.py` checks
  them every shift with a read-only key. Any change that could spend more needs
  the owner's approval *and* a control at the provider.

**Gemini is capped at 20 requests/day, shared with production**, which spends
4–10. Local work competes with live uploads — budget it rather than running it
opportunistically. Reasoning and numbers: PRD §5.

## 2. The owner's usage reserve

**Nothing here bills per token.** The Claude subscription has overage disabled,
so quota runs out rather than costing money. The "quota units" in
`.github/shift-usage.csv` are an API-list-price *equivalent*, used only as a
consistent yardstick — never read them as spending. The one thing that does
cost money is Polly (§1).

Autonomous work stops at **80% of the 5-hour limit and 90% of the weekly
limit** — the rest is the owner's to use, not headroom to plan around. Check
with `venv/bin/python scripts/statusline.py --budget`.

## 3. `main` is live

It deploys; the video workflow runs from it twice daily.

- Feature work goes on a branch. Always.
- ⚙ **Never upload, comment, or mutate `prev_post.txt` / `upload_log.csv` during
  development.** Use `DRY_RUN=1 venv/bin/python -m src.run`. Losing
  `prev_post.txt` risks a duplicate upload on the next scheduled run.
- Merge once the gates pass: tests green, a fresh-context agent's review of
  the diff with its findings fixed or recorded, a dry run producing a playable
  MP4 for anything touching the video, `FORMAT_VERSION` bumped if the video
  changed, one variable per release.

## 4. Work autonomously — but not on the guardrails

Pick the highest-value task and ship it; do not wait for a go-ahead.

**These need the owner.** Raise them with `scripts/escalate.py` (queues a
GitHub issue, which emails them), then carry on with other work rather than
blocking:

- ⚙ Weakening a safety or cost control — the Polly budget, the `DRY_RUN` guard,
  secrets handling, the R4.6 screen's skip categories.
- Spending beyond the current Polly line.
- Deleting or rewriting production data, including historical backfills.
- Publishing beyond the normal upload, except under the publishing policy in
  `ORG.md` (Audience & community).

**Changing `CLAUDE.md`, `ORG.md` or a skill** — propose on a branch, escalate, and land
only with `Approved-In: #N` naming an issue the owner labelled `approved`.
Enforced by `protect-process.yml`, which reverts unapproved changes.

**And when the process itself is failing** — not a permission question, but a
signal the owner needs. `scripts/context_budget.py --health` detects these and
queues the issue automatically: capacity consistently unused, a review
overdue for weeks, a cap producing dishonesty rather than hygiene. If you notice
one the tool doesn't measure, escalate it yourself.

## 5. No AI attribution, anywhere

⚙ Never credit AI tooling in code, commits, PR descriptions, video content, or
anything published. No `Co-Authored-By`, no "generated with". This overrides
any default attribution behaviour.

## 6. Answer performance questions with `scripts/report.py`

Never ad-hoc analysis. It encodes the rules ad-hoc scripts kept getting wrong:
watch-seconds is primary, cohorts must be age-matched, thin cohorts get
"insufficient data", zero-view videos are counted separately. **If it refuses a
comparison, that refusal is the answer.** New capability goes in
`src/insights.py` with a test, not inline.

## 7. Record what you don't fix

Findings go in `TECH_DEBT.md` → "Open items". A diagnosis that lives only in a
commit message is invisible to the next session.

---

Company: `PLAN.md` · Product: `PRD.md` §0 · Who decides: `ORG.md` ·
Pipeline: `README.md` · Code health: `TECH_DEBT.md` · Handover: `WORKLOG.md`
