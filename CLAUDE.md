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
  save money, or upgrade to generative. Cost work here means
  removing wasted calls, never reducing audio quality.
- ⚙ **The AWS-side controls must stay as the owner set them** (key scope,
  budget, its automatic deny, the usage alarm). `scripts/money_check.py` checks
  them every shift with a read-only key. Only the owner changes what can be
  spent, by hand, with a control at the provider (§4).

**Gemini is capped at 20 requests/day, shared with production**, which spends
4–10. Local work competes with live uploads — budget it rather than running it
opportunistically. Reasoning and numbers: PRD §5.

## 2. The owner's usage reserve

**Nothing here bills per token.** The Claude subscription has overage disabled,
so quota runs out rather than costing money. The "quota units" in
`.github/shift-usage.csv` are an API-list-price *equivalent*, never spending;
the measured 5h and weekly % beside them is what counts. The one thing that
does cost money is Polly (§1).

Shifts, and sessions a coordinator runs, stop at **97% of the 5-hour limit
and 90% of the weekly limit**. The 5-hour window is theirs at any time (owner,
2026-11-21: "use it all, always"); the last 3% is for handing over, and a CI
shift, which cannot read mid-run, starts with a wider margin. In the **last 12
hours before the Friday 18:00 UTC reset** the weekly reserve is theirs too, to
98%, because it expires unused (owner, 2026-11-20). Quota left at the weekly
reset is waste, so shifts are paced to land near the weekly ceiling.
Check with `venv/bin/python scripts/statusline.py --budget` (`scripts/quota.py`).

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

## 4. Decide and act — the owner is the last resort

The owner has no time to be in the loop, and waiting on them stopped the
company for a month (D16, 2026-11-14). **Never ask them to approve a product,
strategy or process decision. Decide it, act, record it.** A call that changes
direction goes through `ORG.md`'s **Decide** level: evidence, a fresh-context
challenge, a record. These rules are yours to improve too: `CLAUDE.md`,
`ORG.md` and `process/*.md` (the skills' text) change on a shift's judgement.

Three things are not a shift's call:

- ⚙ **Spending real money is never a shift's decision.** No new paid service,
  nothing beyond the current Polly line, no weakened cost control (§1). Do not
  ask for it either: it does not happen. Record what it blocked in `PLAN.md`.
  Held at AWS (`scripts/money_check.py`), by `guardrails.yml`, and by keys a
  shift is never given.
- ⚙ **Workflow files** hold the paid and upload keys, and GitHub refuses them
  from a shift. Raise the change with `scripts/escalate.py --patch`. It applies
  itself after 3 days unless the owner objects. If it touches the money checks
  or a file holding a key a shift lacks, it waits for their label.
- **A one-way door that costs no money**: deleting production data or
  published videos, renaming the channel, anything `PLAN.md` §4 rates fatal.
  Give notice with `escalate.py --notice-days 7` or more, then go ahead on the
  date unless the owner objected (`scripts/escalations.py notices`).

The other ⚙ rules (the `DRY_RUN` guard, secrets handling, the R4.6 screen's
skip categories) stay enforced by `guardrails.yml`. Publishing beyond the
normal upload stays under the policy in `ORG.md`.

**Ask the owner only when nothing can move without them:** their logins and
accounts. One ask, decidable on a phone, then carry on with everything else.

**When the process itself is failing, fix it.** That is a shift's work now,
not a signal for the owner: `scripts/context_budget.py --health` and
`backlog_status.py` name the known cases, and the friction log
(`scripts/friction.py`) holds the evidence for a rule change.

## 5. No AI attribution, anywhere

⚙ Never credit AI tooling in code, commits, PR descriptions, video content, or
anything published. No `Co-Authored-By`, no "generated with". This overrides
any default attribution behaviour. Checked on every push by `guardrails.yml`.

## 6. Answer performance questions with `scripts/report.py`

Never ad-hoc analysis. It encodes the rules ad-hoc scripts kept getting wrong:
watch-seconds is primary (engaged share for tests set from 2026-11-10, with
watch-seconds as their gate: D9), cohorts must be age-matched, thin cohorts get
"insufficient data", zero-view videos are counted separately. **If it refuses a
comparison, that refusal is the answer.** New capability goes in
`src/insights.py` with a test, not inline.

## 7. Record what you don't fix

Findings go in `TECH_DEBT.md` → "Open items". A diagnosis that lives only in a
commit message is invisible to the next session.

---

Company: `PLAN.md` · Product: `PRD.md` §0 · Who decides: `ORG.md` ·
Pipeline: `README.md` · Code health: `TECH_DEBT.md` · Handover: `WORKLOG.md`
