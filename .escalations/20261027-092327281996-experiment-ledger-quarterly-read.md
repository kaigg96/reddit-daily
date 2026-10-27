---
title: Approve the experiment ledger's two lines of process wording (C18)
key: experiment-ledger-quarterly-read
labels: needs-owner
raised_at: 2026-10-27T09:23:27+00:00
---

## What you are approving

Two protected-file changes on branch `process/experiments-quarterly-read`:

- **Review skill, quarterly prep:** before proposing any bet's decision rule, quote what the experiment ledger says (`report.py --experiments`): how many rules were read on time, and how many keeps cleared the limit printed beside them.
- **Backlog skill, §4:** each rule set or read also updates its row in the ledger (`analysis/experiments.csv`), so the record keeps itself current.

This is C18's last step (D15's pattern: an outcome recorded each time, a scheduled read, a rule set in advance). The ledger and its reader are already live (merged today); nothing else changes.

## What the ledger says today

Backfilled from the product plan and git: 60 rules, 39 read, 18 waiting, 3 dropped before any read.

- **Most reads had no date to be late against.** Only 9 of the 39 had a due date; 8 of those 9 were read on time.
- **A keep rarely shows the change worked.** Of 7 keeps, 1 measured a gain bigger than its test could detect: the background-clip library, +22% against 11% (its videos also ran about 2 seconds longer). Opening on the question read +20% against 13%, but the product plan already says not to credit it, since that lead was mostly longer videos. v6 was inside its limit (+10% against 12%). Four had no limit recorded.
- **The one revert did not stand.** On 21 September the b-roll library read −39% on views and the rule said revert. The next day the rule was changed to watch time, which kept it. The views rule was firing on noise, but the rule changed after its answer was known.
- **Three releases were judged by rules set after they shipped** (v5, v6, the b-roll library). Opening on the question (v7) was the first with its rule set beforehand.
- **Next reads:** the subreddit test on 2 November can see about an 18% difference; the capitals test on 23 November about 82% on views. Bet 1's rules are due by upload count, not date.

## Why it matters for revenue

Every bet in the plan is judged by a rule like these. If the rules mostly come out "keep" inside their own detection limits, a bet that does nothing looks the same as one that works, and the quarter's planning spends a slot on it. The quarterly read is where you would see that.

## Recommendation

Approve: label this issue approved. It costs about five minutes of a quarterly prep and spends nothing. A keep/change/stop rule for the experiment process itself is not proposed here: the backfilled rows are already seen, so a rule written now would be written knowing its answer. The first quarterly prep proposes one, judged only on rules set after it.

## Recommendation

Approve: label this issue approved. It adds a quarterly read of the ledger and keeps the ledger current; it spends nothing.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*