# Run a review

A shift works the queue; a review steps back from it. `ORG.md` §5 sets the
rhythm and `scripts/cadence.py` says what is due. **A due review is the
shift's first work that day**, one per shift. When it is done and time
remains, the shift carries on with the queue. Its `WORKLOG.md` entry is the report,
headed `## <date> — <Weekly|Monthly> review: <one line>`.

**Finish by updating the review's row in `PLAN.md` §5** with today's date —
that is what `cadence.py` reads. A review that does not update its row will
be due again tomorrow.

Every review follows the same rules:

- **Findings land in the trackers, not in new documents.** Work goes to
  `PLAN.md` §3 or `PRD.md` §0 with a Status; risks to `PLAN.md` §4; product
  findings to `PRD.md` §4. Decisions are the review's own to make (`CLAUDE.md` §4,
  `ORG.md` **Decide**); only what needs the owner's login goes to
  `scripts/escalate.py`.
- **Outside evidence may justify a change of direction** (D12), decided at the
  **Decide** level, never on one source alone.
- **Answer performance questions with `scripts/report.py`** (`CLAUDE.md` §6).
- **Skip a step only by saying why** in the entry — "no new comments" is a
  finding, silence is not.

---

## Weekly — after Monday's analytics snapshot

Due when there is a snapshot no weekly review has read.

1. **Data & insights.** What the new snapshot answers: research questions in
   `PRD.md` §0 that were waiting on it; anything blocked on "the next
   snapshot" in either tracker.
2. **Product.** Any decision rule now due → `/backlog` §4, rule quoted first.
   Then `report.py --scorecard` and `--trajectory`: is the product moving?
3. **Audience.** Read last week's viewer comments once they are collected
   (`PLAN.md` C5). Until then, note that they are not.
4. **Distribution.** Where views came from (`analysis/traffic_sources.csv`),
   and how any packaging experiment is reading.
5. **Reliability and Security.** The week's uploads: all landed, with titles?
   Dependency advisories. `money_check.py` was clean every day?
6. **General management.** Every Status in both trackers true; re-rank the
   ready queue on the path to revenue (`/backlog` §2); close what finished.
   **The friction log** (D15): `friction.py report`. Group every new row,
   queue the groups worth fixing with their counts, record each resolution.

7. **Lessons** (E2 T7, from 2026-11-15). Read the friction log's groups
   (`scripts/friction.py`, `.github/friction-groups.csv`): a group with
   three or more rows since the last weekly becomes a lesson in
   `process/lessons.md` (rule, evidence ids, the role and paths it applies
   to, when it retires) or a ticket on the board; a lesson with no new
   evidence in eight weeks is retired, and the file never holds more than 30.

## Monthly — the business review

Due once per calendar month. **This entry is the owner's monthly packet**, so
it carries these sections, in this order, in plain language:

```
## 2026-11-01 — Monthly review: one line on where the company stands

    Worked (% of the shift): strategy 30 · finance 10 · legal 20 · market 20 · gm 20

**Summary:** Two sentences: are we closer to revenue than a month ago, and what decides the next month.

### Where we stand
### Money
### Risks
### Market and policy
### Decisions made
### Next month
### Better?
```

1. **Finance** (Money). `money_check.py`: this month's spend against the line
   and the budget, and every control intact. Any proposal priced this month,
   and its outcome.
2. **Strategy** (Where we stand). The scorecard against the goal, and the
   revenue routes as priced (`PLAN.md` C1). Say plainly whether the current
   path can reach the goal, and on what evidence. "Not yet known" is a real
   answer if it names what would make it known.
3. **Monetization.** Distance to each route's eligibility; what must change
   before an application could succeed.
4. **Legal & policy** (Market and policy). Re-read YouTube's monetization
   policies and Reddit's terms for changes since last month, from their own
   pages. Any new asset's licence in `assets/CREDITS.md`.
5. **Market intelligence** (Market and policy). Comparable channels and
   platform changes. Turn each finding into a hypothesis with a test (Product)
   or evidence for a proposal (Strategy) — or discard it in a sentence.
6. **Risks.** Update `PLAN.md` §4: new risks, changed likelihoods, and any risk
   with no item answering it (add one).
7. **General management.** Update the function coverage in `PLAN.md` §1. A
   function still at "none" after its first monthly review is a finding (D12).
   A function with ready work that kept losing the ranking, likewise.
   D15's rule when `friction.py evaluate` says it is due: quoted before any
   number, applied as written; a change or stop is the review's to make (D16).
8. **Decisions made.** Each larger call with its evidence, the alternative
   rejected, a reversible first step and its cost, listed in the entry.

## Quarterly — setting the bets

**Both halves are a shift's since D16 (2026-11-14).** The owner may hold the
planning session if they choose; nothing waits for them to.

**Prep** (due once per quarter): draft **at most three bets** for the quarter.
Each one needs a line on how it moves the company toward revenue, the evidence
for it, its first reversible step, and the decision rule that will say whether
it worked. Draw on the latest monthly review, and on the **experiment ledger**
(`report.py --experiments`, PLAN C18): quote what it says about reads on time
and keeps beyond their limits before proposing any bet's rule. Update the
"Quarterly prep" row.

**Planning** (a later shift than prep, so the bets meet fresh eyes): each bet
is a **Decide** (`ORG.md` §2), with a fresh-context agent arguing against it.
Record the bets kept in `PLAN.md` §2 with their decision rules, retire last
quarter's with a verdict each, and update the "Quarterly planning" row. A bet
that would spend money is dropped, not asked for. Run `/audit` in the same session
if ~ten shifts have passed since the last one.
