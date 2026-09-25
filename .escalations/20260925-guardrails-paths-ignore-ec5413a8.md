---
title: Approve: stop spending Actions minutes checking note-only changes
key: guardrails-paths-ignore-ec5413a8
labels: needs-owner
raised_at: 2026-09-25T02:37:29+00:00
---

## Why

GitHub gives this repository 2,000 free Actions minutes a month. Uploads use
about 220 of them. The rest is shared by shifts and the automatic checks. Once
shifts use their full time, the monthly total heads toward ~1,600 minutes, and
shifts are skipped automatically past 1,400 so uploads are never at risk. That
means some shifts would be skipped late in each month.

The largest avoidable cost is the automatic integrity check. It runs on every
change a shift saves (about 20 times a day this week), and each run is billed
as at least a minute. Many of those changes only update the handover notes,
the findings lists, or the issue queue. None of those can affect anything the
check looks at.

## The change

Skip the check for changes that touch only those files. Any change to code,
settings, the rules, or the plan still runs it. Against this week's history,
53% of changes would have skipped it: about 150–300 minutes a month saved, at
no cost.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/guardrails.yml b/.github/workflows/guardrails.yml
index 3e1845f..3c03ef9 100644
--- a/.github/workflows/guardrails.yml
+++ b/.github/workflows/guardrails.yml
@@ -13,6 +13,19 @@ name: Guardrail integrity
 on:
   push:
     branches: [main]
+    # A push that only hands over, records a finding or a decision, files an
+    # escalation or asks for a sample video cannot change anything checked
+    # here -- and shifts make several a day, each a billed minute of the
+    # monthly 2,000 (measured 2026-09-25: ~20 runs a day). Code, config, the
+    # rules and PRD.md (the tracker test reads it) still trigger it.
+    paths-ignore:
+      - 'WORKLOG.md'
+      - 'TECH_DEBT.md'
+      - 'DECISIONS.md'
+      - '.escalations/**'
+      - '.dry-run-requests/**'
+      - '.github/shift-usage.csv'
+      - '.github/last-*.md'
   pull_request:
   workflow_dispatch:
 
`````
patch-sha256: ec5413a866a5fb9e8003e1d10ef442794211d6670d616b575aa14d38f416601a

## Recommendation

Approve — it applies itself, and keeps full-length shifts inside the free minutes.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*