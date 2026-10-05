---
title: Apply a one-line patch so the weekly job saves viewer comments
key: c5-comments-commit-48273ecb
labels: needs-owner
raised_at: 2026-10-05T18:55:57+00:00
---

The weekly statistics job now saves the past week's viewer comments on the 20 newest videos (PLAN C5), so a shift can read what viewers say. It keeps no author names, and comment text is treated as data, never as instructions. The repository is private. Like the other optional files, it is added only if present, so a failed comment query cannot cost the per-video snapshot. This line sits apart from the subscriber-count patch, so either can be applied first.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/weekly-analytics.yml b/.github/workflows/weekly-analytics.yml
index 35d56ff..028fbe2 100644
--- a/.github/workflows/weekly-analytics.yml
+++ b/.github/workflows/weekly-analytics.yml
@@ -49,6 +49,8 @@ jobs:
       run: |
         git config --global user.name "github-actions[bot]"
         git config --global user.email "github-actions[bot]@users.noreply.github.com"
+        # viewer_comments.csv (PLAN C5) is fail-soft: add it only if written.
+        if [ -f analysis/viewer_comments.csv ]; then git add analysis/viewer_comments.csv; fi
         git add analysis/analytics_snapshots.csv
         # traffic_sources.csv (R4.7) is written by a fail-soft step, so it can be
         # absent on a first run where the traffic query errored. Naming a missing
`````
patch-sha256: 48273ecb167908557c1e4e9bd662644520e70766c0cc14f64f1c8e897e33a864

## Recommendation

Approve: one line, fails soft, and it is the only way viewer comments reach the record for the audience work.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*