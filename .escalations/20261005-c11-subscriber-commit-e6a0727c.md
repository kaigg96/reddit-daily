---
title: Apply a one-line patch so the weekly job saves the subscriber count
key: c11-subscriber-commit-e6a0727c
labels: needs-owner
raised_at: 2026-10-05T18:49:07+00:00
---

The weekly statistics job now records the channel's subscriber count in its own file (PLAN C11). No record held it before, and it is half of the Partner Program's bar. The workflow commits only the files it names, so this one-line patch is needed or the new file is written and dropped. Like the traffic file, it is added only if present, so a failed channel query cannot cost the per-video snapshot.

## The exact change

Applied automatically, exactly as shown, when you label this `approved`.

<!-- apply-patch -->
`````diff
diff --git a/.github/workflows/weekly-analytics.yml b/.github/workflows/weekly-analytics.yml
index 35d56ff..d8cf1f8 100644
--- a/.github/workflows/weekly-analytics.yml
+++ b/.github/workflows/weekly-analytics.yml
@@ -55,6 +55,8 @@ jobs:
         # path makes `git add` fail, and `set -e` would then kill the step before
         # the commit — losing the snapshot too. Same trap as run-reddit-video.yml.
         if [ -f analysis/traffic_sources.csv ]; then git add analysis/traffic_sources.csv; fi
+        # channel_stats.csv (PLAN C11, subscribers) is fail-soft the same way.
+        if [ -f analysis/channel_stats.csv ]; then git add analysis/channel_stats.csv; fi
         git commit -m "Weekly analytics snapshot" || echo "No changes to commit"
 
         # Retry, matching run-reddit-video.yml: the twice-daily video job can
`````
patch-sha256: e6a0727c2fda497ecc7a2f89bbb53aeaad0a3109bad18d609839cfd0fe2c93f3

## Recommendation

Approve: the change is one line, fails soft, and is the only way the subscriber count reaches the record.

---

*Raised automatically by a `/shift` run — it could not make this call itself. Close this issue once decided; if the decision changes a standing rule, it belongs in `CLAUDE.md` too.*