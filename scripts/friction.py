#!/usr/bin/env python3
"""The friction log: what made each finished item hard, and whether fixing it
worked (DECISIONS.md D15).

NOT BUILT YET. This docstring is the spec; a shift builds it (PLAN.md C17) on
branch `gm/friction-log`, which already carries the skill and ORG.md wording
that call it and the seed data below.

Shifts wrote "Friction:" notes in the work log from 09-25 to 10-07, about 18
distinct ones, several recurring. From 10-08 there were none. The work log is
the owner's email, with no slot for them, a word budget, and its oldest
entries deleted, so a recurrence could never be counted. This gives the notes
a home that lasts, a weekly reader, and a rule that says whether it works.

Every finished item logs one row as it finishes, not at the end of the shift:
a merge, an answered question, an escalation, a candidate dropped, an attempt
abandoned.

    venv/bin/python scripts/friction.py add --function engineering \\
        --task "..." --outcome done --category allowance \\
        --hardest "..." --helped "..." --minutes 15 [--fixes G3] [--group G1]
    venv/bin/python scripts/friction.py add --function data --task "..." \\
        --outcome done --category none        # nothing notable: a real answer
    venv/bin/python scripts/friction.py groups     # open groups, to tag a repeat
    venv/bin/python scripts/friction.py report     # weekly review: ungrouped rows,
                                                   # groups by leverage
    venv/bin/python scripts/friction.py evaluate   # D15's rule, then its checks
    venv/bin/python scripts/friction.py gaps       # shifts since START with no row

FILES

.github/friction.csv, append-only, one row per item:
    id            F1, F2, ...
    timestamp_utc when `add` ran
    run_id        GITHUB_RUN_ID, else "local"; "backfill" for the seed rows
    function      an ORG.md short name (strategy, gm, market, audience,
                  distribution, monetization, product, editorial, engineering,
                  reliability, data, finance, legal, security)
    task          one line
    outcome       done | partial | abandoned
    fixes         the group this item fixed, else blank
    category      see below
    hardest       one concrete line; blank only for "none"
    helped        one line; a moonshot is allowed
    minutes_lost  an integer, or "blocked"; blank only on backfill rows
    group         blank until sorted (the writer may tag an obvious repeat)

.github/friction-groups.csv, one row per group, written by the weekly review:
    group, title, status (open | queued | fixed | wontfix | parked),
    item (the queue id or commit that answers it), opened,
    resolved (the date its fix shipped; recurrence is counted after it), note

CATEGORIES
    docs       missing or misleading documentation
    access     no visibility or access: logs, YouTube data, a web page
    allowance  an external allowance: Gemini, a render slot, the clock
    owner      waiting on the owner
    tool       a tool's bug or false alarm
    rules      rules in conflict, or a rule that did not fit
    rederived  re-derived something already recorded
    mistake    my own mistake
    none       nothing notable

WHAT THE BUILD MUST KEEP
- `add` refuses an unknown function, category or outcome, and a non-"none"
  row without hardest, helped and minutes.
- START, the day this lands, is a constant here. Rows before it (the
  2026-10-27 backfill) are never in an evaluation.
- D15's thresholds are constants here, and a test checks that D15 states the
  same numbers, so the rule and the code cannot drift apart.
- `evaluate` prints D15's decision rule verbatim from DECISIONS.md before any
  number, then each check (a)-(h) with its value, threshold and pass / fail /
  not yet, then the verdict (keep, change, stop, not yet). Check (c) is
  judgement: print 10 random non-"none" rows for the reviewer. Check (g)
  counts rows with `fixes` set against all rows in the window.
- `gaps` matches rows to shifts by time: a shift in .github/shift-usage.csv
  logged if a row falls inside [end - duration - 5 min, end + 5 min].
- `context_budget.py --health` calls `gaps`. Three silent shifts in a row
  queue `process-friction-silent` to the owner; it is not SHIFT_OWNED,
  because a silent stop is exactly what happened to the work-log notes.
- Leverage, for `report`, per group: rows x median minutes ("blocked" counts
  as 60) x distinct functions. A fixed group with a row after `resolved` is
  flagged RECURRED.
- Tests in tests/test_friction.py, like the other scripts'.
"""
import sys

sys.exit("friction.py: not built yet; the docstring is the spec (PLAN.md C17)")
