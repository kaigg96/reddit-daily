#!/usr/bin/env python3
"""The pre-push gate: a push publishes, so nothing private goes out in one.

The repo is public: whatever a push carries is published the moment it lands,
history and commit metadata included. The old check ("Secrets still ignored",
guardrails.yml) confirmed that three file names were gitignored, after the push.
It never read what a commit says or who it says made it. This runs before the
push, on exactly the commits the push would publish, and refuses it if any:

  1. names its author or committer by anything but a noreply address;
  2. adds (on a diff line, or in its message) the value of a secret this
     session holds: .env, the OAuth client files, ~/.aws/credentials, any
     secret-named environment variable, and .git/info/private-values, one
     value a line: the owner's addresses and identifiers, kept on the machine
     that knows them and never pushed;
  3. adds a private email address or an AWS account ID (the same two rules CI
     applies from .github/workflows/gitleaks.toml);
  4. adds a credential shape: gitleaks with that config when both are present,
     otherwise the shapes the shift trace redacts.

It never prints what it found, only where and which rule: its output lands in a
session transcript, and a shift's in a public log.

`.githooks/pre-push` runs it, once `core.hooksPath` points there. The
SessionStart hook in .claude/settings.json does that for every Claude session
(local, Actions or cloud), and its PreToolUse hook refuses `--no-verify` and
hooksPath overrides. A person can still bypass it, and CI checks the same rules
after the push.

    prepush_check.py hook <remote> [url]    git's pre-push; refs on stdin
    prepush_check.py range <rev-args...>    by hand, e.g. origin/main..HEAD
    prepush_check.py install [--check]      point git at .githooks
    prepush_check.py guard                  Claude Code PreToolUse (stdin JSON)
"""
import configparser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shift_trace  # noqa: E402  (the shapes and rules, kept in one place)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS_DIR = ".githooks"
GITLEAKS_CONFIG = ".github/workflows/gitleaks.toml"
# Made-up credentials that prove the trace redactor catches each shape
# (tests/test_no_committed_secrets.py exempts the same file). gitleaks, when it
# runs, exempts them by exact value instead.
FIXTURE_PATHS = {"tests/test_shift_trace.py"}
NOREPLY = re.compile(r"(?:@users\.noreply\.github\.com|^noreply@github\.com)$", re.I)
SECRET_NAME = re.compile(r"(?:^|_)(?:KEY|SECRET|TOKEN|PASSWORD|CREDENTIALS?)(?:_|$)")
OAUTH_FILES = ("client_secret.json", "token.json")
OAUTH_FIELDS = {"client_id", "client_secret", "project_id", "refresh_token", "token", "access_token"}
AWS_FIELDS = ("aws_access_key_id", "aws_secret_access_key", "aws_session_token")
MIN_VALUE = 8   # shorter values match too much to mean anything

CREDENTIAL = re.compile(shift_trace.CREDENTIAL_SHAPES)
EMAIL = re.compile(shift_trace.PRIVATE_EMAIL)
NOT_A_PERSON = re.compile("|".join(shift_trace.NOT_A_PERSON))
ACCOUNT = re.compile(shift_trace.AWS_ACCOUNT_ID)
PLACEHOLDER = re.compile("|".join(shift_trace.PLACEHOLDER_ACCOUNTS))

Problem = namedtuple("Problem", "commit where rule")


def git(*args, cwd=None, check=True):
    r = subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=cwd,
                       capture_output=True, text=True, errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"git {args[0]} failed: {r.stderr.strip()[:300]}")
    return r.stdout


# --- what this session holds ----------------------------------------------

def _common_dir(cwd):
    return git("rev-parse", "--path-format=absolute", "--git-common-dir", cwd=cwd).strip()


def checkouts(cwd=None):
    """This worktree's top level, and the main checkout's (which holds .env)."""
    tops = [git("rev-parse", "--show-toplevel", cwd=cwd).strip()]
    common = _common_dir(cwd)
    if os.path.basename(common) == ".git":
        tops.append(os.path.dirname(common))
    return list(dict.fromkeys(tops)), common


def _dotenv(path):
    out = {}
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    out[k.strip()] = v
    except OSError:
        pass
    return out


def _json_fields(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and k in OAUTH_FIELDS:
                yield k, v
            else:
                yield from _json_fields(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _json_fields(v)


def held_values(env=None, home=None, tops=(), common=None, global_email=None):
    """{value: label} for every secret or private value this session can see.
    The label names where it came from, never what it is."""
    env = os.environ if env is None else env
    home = os.path.expanduser("~") if home is None else home
    vals = {}

    def add(label, value):
        value = (value or "").strip().strip("\"'")
        if len(value) >= MIN_VALUE:
            vals.setdefault(value, label)

    for name in sorted(env):
        if name in shift_trace.SECRET_VARS or SECRET_NAME.search(name):
            add(f"environment variable {name}", env[name])
    for top in tops:
        for k, v in _dotenv(os.path.join(top, ".env")).items():
            add(f".env {k}", v)
        for fn in OAUTH_FILES:
            try:
                with open(os.path.join(top, fn), encoding="utf-8") as f:
                    for k, v in _json_fields(json.load(f)):
                        add(f"{fn} {k}", v)
            except (OSError, ValueError):
                pass
    creds = configparser.ConfigParser(interpolation=None)
    try:
        creds.read(os.path.join(home, ".aws", "credentials"))
    except configparser.Error:
        pass
    for section in creds.sections():
        for field in AWS_FIELDS:
            add(f"~/.aws/credentials {field}", creds[section].get(field))
        for account in re.findall(r"(?<!\d)\d{12}(?!\d)", section):
            add("an AWS account ID named in ~/.aws/credentials", account)
    if common:
        try:
            with open(os.path.join(common, "info", "private-values"), encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    if line.strip() and not line.lstrip().startswith("#"):
                        add(f"line {n} of .git/info/private-values", line)
        except OSError:
            pass
    if global_email is None:
        global_email = git("config", "--global", "user.email", check=False).strip()
    if global_email and not NOREPLY.search(global_email):
        add("your global git user.email", global_email)
    return vals


# --- what a push would publish --------------------------------------------

def _is_zero(sha):
    return set(sha) == {"0"}


def ranges_from_hook(lines, remote, cwd=None):
    """git's pre-push stdin -> one rev-list argument list per pushed ref."""
    remotes = git("remote", cwd=cwd, check=False).split()
    not_public = [f"--remotes={remote}"] if remote in remotes else ["--remotes"]
    out = []
    for line in lines:
        parts = line.split()
        if len(parts) != 4:
            continue
        _, local, _, remote_sha = parts
        if _is_zero(local):          # deleting a remote ref publishes nothing
            continue
        known = (not _is_zero(remote_sha)
                 and subprocess.run(["git", "cat-file", "-e", f"{remote_sha}^{{commit}}"],
                                    cwd=cwd, capture_output=True).returncode == 0)
        out.append([f"{remote_sha}..{local}"] if known else [local, "--not", *not_public])
    return out


_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def commits(rev_args, cwd=None):
    """Yield (sha, author, committer, message, [(path, line_no, text), ...]) for
    each commit, its added lines only: what it publishes that was not public."""
    out = git("log", "-p", "--unified=0", "--no-color", "--no-ext-diff",
              "--diff-merges=first-parent", "--format=%x00%x01%H%x00%ae%x00%ce%x00%B%x00",
              *rev_args, "--", cwd=cwd)
    for chunk in out.split("\x00\x01")[1:]:
        sha, author, committer, message, diff = (chunk.split("\x00", 4) + [""] * 5)[:5]
        added, path, n = [], None, 0
        for line in diff.splitlines():
            if line.startswith("+++ "):
                target = line[4:].strip('"')
                path = None if target == "/dev/null" else target[2:] if target.startswith("b/") else target
            elif line.startswith("@@"):
                m = _HUNK.match(line)
                n = int(m.group(1)) if m else 0
            elif line.startswith("+") and path is not None:
                added.append((path, n, line[1:]))
                n += 1
        yield sha, author, committer, message, added


# --- the rules --------------------------------------------------------------

def _rules(text, values, shapes):
    """The rule names text breaks. Values compare case-insensitively: an address
    is the same address in any case, and a secret never collides by accident."""
    low = text.lower()
    found = [label for value, label in values.items() if value.lower() in low]
    if any(not NOT_A_PERSON.search(m.group()) for m in EMAIL.finditer(text)):
        found.append("private-email")
    if any(not PLACEHOLDER.search(m.group(1)) for m in ACCOUNT.finditer(text)):
        found.append("aws-account-id")
    if shapes and CREDENTIAL.search(text):
        found.append("credential shape")
    return found


def check(rev_args_list, values, cwd=None, shapes=True):
    problems = []
    seen = set()
    for rev_args in rev_args_list:
        for sha, author, committer, message, added in commits(rev_args, cwd):
            if sha in seen:
                continue
            seen.add(sha)
            short = sha[:9]
            for who, email in (("author", author), ("committer", committer)):
                if not NOREPLY.search(email.strip()):
                    problems.append(Problem(short, "commit metadata", f"{who} is not a noreply address"))
            for rule in _rules(message, values, shapes):
                problems.append(Problem(short, "commit message", rule))
            for path, n, text in added:
                for rule in _rules(text, values, shapes and path not in FIXTURE_PATHS):
                    problems.append(Problem(short, f"{path}:{n}", rule))
    return problems


def gitleaks(rev_args_list, cwd=None):
    """gitleaks' credential rules with the shared config, or None when either is
    missing. Its two private-identifier rules are checked above already."""
    top = git("rev-parse", "--show-toplevel", cwd=cwd).strip()
    config = os.path.join(top, GITLEAKS_CONFIG)
    exe = shutil.which("gitleaks")
    if not exe or not os.path.exists(config):
        return None
    problems = []
    for rev_args in rev_args_list:
        with tempfile.TemporaryDirectory() as tmp:
            report = os.path.join(tmp, "r.json")
            r = subprocess.run([exe, "git", "--no-banner", "--redact", "--log-level", "error",
                                "--config", config, "--log-opts", " ".join(rev_args),
                                "--report-format", "json", "--report-path", report,
                                "--exit-code", "0", top], capture_output=True, text=True)
            if r.returncode:
                problems.append(Problem("-", "gitleaks", f"could not run (exit {r.returncode})"))
                continue
            try:
                with open(report, encoding="utf-8") as f:
                    findings = json.load(f) or []
            except (OSError, ValueError):
                findings = []
            for x in findings:
                if x.get("RuleID") not in ("private-email", "aws-account-id"):
                    problems.append(Problem(x.get("Commit", "")[:9], f"{x.get('File')}:{x.get('StartLine')}",
                                            f"gitleaks {x.get('RuleID')}"))
    return problems


FIX = """\
What was found is not shown: this output is a transcript, and a shift's is a public log.
To fix, rewrite the commits before pushing (nothing has been published yet):
  author/committer: git config user.email <id>+<login>@users.noreply.github.com
                    git rebase <upstream> --exec 'git commit --amend --no-edit --reset-author'
  content:          remove it, then rewrite the commits that added it
                    (git reset --soft <upstream>, recommit). A secret that reached any
                    remote, log or issue must also be rotated.
Bypassing this is refused in Claude sessions, and CI checks the same rules after a push."""


def report(problems, out=sys.stderr):
    commits_hit = sorted({p.commit for p in problems})
    print(f"pre-push: refused, nothing was pushed. {len(problems)} problem(s) in "
          f"{len(commits_hit)} commit(s):", file=out)
    for p in problems:
        print(f"  {p.commit}  {p.where}  {p.rule}", file=out)
    print(FIX, file=out)


def run(rev_args_list, cwd=None, values=None):
    if not rev_args_list:
        return 0
    if values is None:
        tops, common = checkouts(cwd)
        values = held_values(tops=tops, common=common)
    leaks = gitleaks(rev_args_list, cwd)
    problems = check(rev_args_list, values, cwd, shapes=leaks is None) + (leaks or [])
    if problems:
        report(problems)
        return 1
    return 0


# --- installing it, and keeping it installed ---------------------------------

def install(check_only=False, cwd=ROOT):
    try:
        current = git("config", "core.hooksPath", cwd=cwd, check=False).strip()
    except OSError:
        return 0
    if current == HOOKS_DIR:
        if check_only:
            print(f"pre-push gate installed (core.hooksPath = {HOOKS_DIR})")
        return 0
    if check_only:
        print(f"pre-push gate NOT installed: core.hooksPath is {current or 'unset'}; "
              f"run python3 scripts/prepush_check.py install")
        return 1
    git("config", "core.hooksPath", HOOKS_DIR, cwd=cwd, check=False)
    return 0


_SEGMENT = re.compile(r"[;&|\n]+")
# Setting or unsetting it (`git -c core.hooksPath=…`, `git config [--unset] core.hooksPath …`,
# or git's config environment variables). Reading it, or grepping for it, is fine.
_SETS_HOOKS = re.compile(
    r"(?i)\bgit\b.*(?:-c\s*core\.hookspath\s*="
    r"|\bconfig\b(?!.*--get).*\bcore\.hookspath\s+[^\s#]"
    r"|\bconfig\b.*--(?:unset|unset-all|replace-all|add)\b.*\bcore\.hookspath\b)"
    r"|\bGIT_CONFIG_(?:PARAMETERS|KEY_\d+)\s*=.*core\.hookspath")
_GIT_PUSH = re.compile(r"\bgit\b.*\bpush\b")
_NO_VERIFY = re.compile(r"(?:^|\s)--no-verify\b")


def refusal(command):
    """Why a shell command would switch the gate off, or None."""
    for seg in _SEGMENT.split(command or ""):
        if _SETS_HOOKS.search(seg):
            return "it changes core.hooksPath, which switches off the pre-push gate"
        if _GIT_PUSH.search(seg) and _NO_VERIFY.search(seg):
            return "--no-verify skips the pre-push gate"
    return None


def guard(stdin=sys.stdin):
    try:
        call = json.load(stdin)
    except ValueError:
        return 0
    if call.get("tool_name") != "Bash":
        return 0
    why = refusal((call.get("tool_input") or {}).get("command", ""))
    if why:
        print(f"Refused: {why}. If the gate refused a push, fix what it names "
              "(scripts/prepush_check.py explains how); it never blocks a clean one.", file=sys.stderr)
        return 2
    return 0


def main(argv):
    cmd = argv[0] if argv else ""
    if cmd == "hook":
        remote = argv[1] if len(argv) > 1 else "origin"
        return run(ranges_from_hook(sys.stdin.read().splitlines(), remote))
    if cmd == "range" and len(argv) > 1:
        return run([argv[1:]])
    if cmd == "install":
        return install(check_only="--check" in argv)
    if cmd == "guard":
        return guard()
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
