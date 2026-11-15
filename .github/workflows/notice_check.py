#!/usr/bin/env python3
"""What a workflow change may do when it lands by notice, with nobody looking.

Since D16 (2026-11-14) a shift's change to a workflow file applies itself
after NOTICE_DAYS with no objection (apply-approved.yml). The owner's one wall
is money, and the workflows are where the paid and upload keys are wired, so a
notice may not reach:

  - any secret a shift's own job is not given (SHIFT_HOLDS): the Polly keys
    spend money, the YouTube keys change the channel, APPLY_TOKEN pushes here;
  - a widened GITHUB_TOKEN: `actions: write` dispatches the upload job, which
    holds every key, so permissions are an allowlist and must be declared;
  - the money checks (MONEY_CHECKS) or this machinery (LOCKED), ever.

The first review of the notice path (2026-11-15) found a text regex misses
what YAML resolves: "secr\\x65ts.X" is `secrets.X` once parsed, `secrets:
"inherit"` is `secrets: inherit`. So a YAML file is parsed and every string in
it is checked, as well as the raw text; a file that cannot be parsed is
refused. Whatever `secrets` appears as, other than `secrets.<a key the shift
holds>`, counts as reaching every secret. Comments count too: a refusal costs
one owner label, a miss could cost money.

One copy of these rules: apply-approved.yml runs this before a notice lands,
protect-process.yml re-runs it on what reaches main, and scripts/escalate.py
imports it to word the issue. Refusing is always the safe answer, so any
error here is a refusal.

    python3 .github/workflows/notice_check.py --name <published path> [FILE]

reads FILE (or stdin), prints a JSON list of reasons to refuse, and exits 1
if there are any, 0 if none, 2 if it could not run.
"""
import argparse
import json
import re
import sys

NOTICE_DAYS = 3
# The keys shift.yml gives a shift. tests/test_apply_approved.py checks that
# file against this list, so it cannot grow unnoticed.
SHIFT_HOLDS = frozenset({"GEMINI_API_KEY", "GROQ_API_KEY", "AWS_READONLY_ACCESS_KEY_ID",
                         "AWS_READONLY_SECRET_ACCESS_KEY", "CLAUDE_CODE_OAUTH_TOKEN"})
# Never changed by this machinery, even on the owner's label: they land by hand.
LOCKED = (".github/workflows/protect-process.yml", ".github/workflows/apply-approved.yml",
          ".github/workflows/notice_check.py")
# Out of a notice's reach; the owner's label may change them.
MONEY_CHECKS = (".github/workflows/guardrails.yml",)
# What a notice-landed workflow may ask of GITHUB_TOKEN. A shift's own job
# has exactly these (shift.yml); `actions: write` is the one that reaches
# the keyed jobs, by dispatching them.
ALLOWED_PERMISSIONS = {"contents": {"read", "write", "none"}, "issues": {"read", "write", "none"},
                       "actions": {"read", "none"}, "id-token": {"read", "write", "none"}}

_SECRETS = re.compile(r"\bsecrets\b(?:\s*\.\s*([A-Za-z0-9_]+))?", re.I)
_ESCAPE = re.compile(r"\\[xuUN]")


def _text_reasons(text, where):
    out = []
    for m in _SECRETS.finditer(text):
        name = m.group(1)
        if name and name.upper() in SHIFT_HOLDS:
            continue
        out.append(f"{where} reaches secrets.{name}" if name
                   else f"{where} reaches every secret (`secrets` used other than as secrets.<name>)")
    if _ESCAPE.search(text):
        out.append(f"{where} contains an escaped character (\\x, \\u, \\U or \\N), which can spell a key")
    return out


def _walk(node, where, out):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str):
                out.extend(_text_reasons(k, where))
                if k.lower() == "secrets" and isinstance(v, str):
                    out.append(f"{where} passes every secret to a called workflow (secrets: {v})")
            _walk(v, where, out)
    elif isinstance(node, list):
        for v in node:
            _walk(v, where, out)
    elif isinstance(node, str):
        out.extend(_text_reasons(node, where))


def _permission_reasons(perm, where):
    if perm is None:
        return []
    if isinstance(perm, str):
        return [] if perm == "read-all" else [f"{where} grants {perm} to GITHUB_TOKEN"]
    if not isinstance(perm, dict):
        return [f"{where} permissions could not be read"]
    out = []
    for scope, level in perm.items():
        allowed = ALLOWED_PERMISSIONS.get(str(scope))
        if allowed is None or str(level) not in allowed:
            out.append(f"{where} grants {scope}: {level} to GITHUB_TOKEN")
    return out


def reasons(text, name, raw_only=False):
    """Why a notice may not land `text` as the workflow file `name`; [] if it may."""
    out = _text_reasons(text, name)
    if raw_only or not name.endswith((".yml", ".yaml")):
        return _dedupe(out)
    try:
        import yaml
        doc = yaml.safe_load(text)
    except Exception as err:                      # any failure to read is a refusal
        return _dedupe(out + [f"{name} could not be read as YAML ({type(err).__name__})"])
    if not isinstance(doc, dict):
        return _dedupe(out + [f"{name} is not a workflow (no mapping at the top)"])
    _walk(doc, name, out)
    if "permissions" not in doc:
        out.append(f"{name} declares no permissions, so the repository's default applies")
    else:
        out.extend(_permission_reasons(doc["permissions"], name))
    jobs = doc.get("jobs")
    if isinstance(jobs, dict):
        for job_name, job in jobs.items():
            if isinstance(job, dict) and "permissions" in job:
                out.extend(_permission_reasons(job["permissions"], f"{name} job {job_name}"))
    return _dedupe(out)


def _dedupe(items):
    seen, out = set(), []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="the file's published path")
    ap.add_argument("file", nargs="?", help="the content to check (default: stdin)")
    args = ap.parse_args(argv)
    try:
        text = open(args.file, encoding="utf-8").read() if args.file else sys.stdin.read()
        found = reasons(text, args.name)
    except Exception as err:                      # noqa: BLE001 - refusing is the safe answer
        print(json.dumps([f"{args.name} could not be checked ({type(err).__name__}: {err})"]))
        return 2
    print(json.dumps(found))
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
