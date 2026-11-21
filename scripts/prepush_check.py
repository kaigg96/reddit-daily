#!/usr/bin/env python3
"""The pre-push gate: a push publishes, so nothing private goes out in one.

The repo is public: whatever a push carries is published the moment it lands,
history and commit metadata included. The old check ("Secrets still ignored",
guardrails.yml) confirmed that three file names were gitignored, after the push.
It never read what a commit says or who it says made it. This runs before the
push, on exactly what the push would publish that no remote ref already holds,
and refuses it if any commit, tag or ref:

  1. names its author, committer or tagger by anything but a noreply address;
  2. carries (in a line it adds, a binary file, a file path, its message, a
     person's name, a tag or a ref name) the value of a secret this session
     holds: .env, the OAuth client files, ~/.aws/credentials and config, any
     secret-named environment variable, and .git/info/private-values, one
     value a line: the owner's addresses and identifiers, kept on the machine
     that knows them and never pushed;
  3. carries a private email address or an AWS account ID (the rules the
     gitleaks config, .github/workflows/gitleaks.toml, also carries);
  4. carries a credential shape: gitleaks with that config checks added lines
     when both are present; the shapes the shift trace redacts check the rest.

It never prints what it found, only where and which rule: its output lands in a
session transcript, and a shift's in a public log.

`.githooks/pre-push` runs it, once `core.hooksPath` points there. The
SessionStart hook in .claude/settings.json does that for every Claude session
(local, Actions or cloud), and its PreToolUse hook refuses `--no-verify` and
hooksPath overrides. It is the only check before a push, and a person can
still bypass it.

    prepush_check.py hook <remote> [url]    git's pre-push; refs on stdin
    prepush_check.py range <rev-args...>    by hand, e.g. origin/main..HEAD
    prepush_check.py install [--check]      point git at .githooks
    prepush_check.py guard                  Claude Code PreToolUse (stdin JSON)
"""
import configparser
import json
import os
import re
import shlex
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
WITHHELD = "(a path, withheld: the path itself is flagged)"

CREDENTIAL = re.compile(shift_trace.CREDENTIAL_SHAPES)
EMAIL = re.compile(shift_trace.PRIVATE_EMAIL)
NOT_A_PERSON = re.compile("|".join(shift_trace.NOT_A_PERSON))
ACCOUNT = re.compile(shift_trace.AWS_ACCOUNT_ID)
PLACEHOLDER = re.compile("|".join(shift_trace.PLACEHOLDER_ACCOUNTS))
TWELVE_DIGITS = re.compile(r"(?<!\d)\d{12}(?!\d)")

Problem = namedtuple("Problem", "commit where rule")
Commit = namedtuple("Commit", "sha author_name author committer_name committer message added paths binaries")


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
    The label names where it came from, never what it is. Every .env value
    counts: this project's .env holds only credentials and identifiers."""
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
    # Account IDs live in section names, role_arn and sso_account_id.
    for fn in ("credentials", "config"):
        aws = configparser.ConfigParser(interpolation=None)
        try:
            aws.read(os.path.join(home, ".aws", fn))
        except configparser.Error:
            continue
        for section in aws.sections():
            for field in AWS_FIELDS:
                add(f"~/.aws/{fn} {field}", aws[section].get(field))
            for text in (section, *aws[section].values()):
                for account in TWELVE_DIGITS.findall(text or ""):
                    add(f"an AWS account ID in ~/.aws/{fn}", account)
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


def _pushed(lines):
    """git's pre-push stdin -> (local sha, remote ref, remote sha) for each ref
    that publishes something (not a deletion, not already there)."""
    for line in lines:
        parts = line.split()
        if len(parts) == 4 and not _is_zero(parts[1]) and parts[1] != parts[3]:
            yield parts[1], parts[2], parts[3]


def ranges_from_hook(lines, remote, cwd=None):
    """One rev-list argument list per pushed ref: what it reaches that no ref
    of that remote does. Excluding the remote's refs, not only the ref's old
    value, keeps a branch rebased onto main (or merged with it) from re-checking
    main's commits, which are public already."""
    remotes = git("remote", cwd=cwd, check=False).split()
    not_public = [f"--remotes={remote}"] if remote in remotes else ["--remotes"]
    out = []
    for local, _, remote_sha in _pushed(lines):
        known = (not _is_zero(remote_sha)
                 and subprocess.run(["git", "cat-file", "-e", f"{remote_sha}^{{commit}}"],
                                    cwd=cwd, capture_output=True).returncode == 0)
        out.append([local, "--not", *([remote_sha] if known else []), *not_public])
    return out


def pushed_tags(lines, cwd=None):
    """The annotated tag objects a push carries (a tag of a tag included)."""
    out = []
    for local, _, _ in _pushed(lines):
        sha = local
        for _ in range(5):
            if git("cat-file", "-t", sha, cwd=cwd, check=False).strip() != "tag":
                break
            out.append(sha)
            m = re.search(r"^object (\S+)", git("cat-file", "tag", sha, cwd=cwd), re.M)
            sha = m.group(1) if m else ""
    return list(dict.fromkeys(out))


_HUNK = re.compile(r"^@@ -\d+(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def _unquote(path):
    return path[1:-1] if len(path) > 1 and path[0] == path[-1] == '"' else path


def _strip_prefix(path):
    path = _unquote(path)
    return path[2:] if path[:2] in ("a/", "b/") else path


def _header_path(line):
    """`diff --git a/P b/P` -> P, when the two halves agree (no rename)."""
    s = line[len("diff --git a/"):]
    n = (len(s) - 3) // 2
    return s[:n] if n > 0 and s[n:n + 3] == " b/" and s[n + 3:] == s[:n] else None


def commits(rev_args, cwd=None):
    """Yield a Commit for each commit in range: the lines it adds, every path it
    publishes, its binary files. A merge shows only what it adds beyond the
    automatic merge of its parents (remerge): what it brings in from each
    side is the side's own commits, checked as themselves."""
    out = git("log", "-p", "--unified=0", "--no-color", "--no-ext-diff", "--diff-merges=remerge",
              "--format=%x00%x01%H%x00%an%x00%ae%x00%cn%x00%ce%x00%B%x00", *rev_args, "--", cwd=cwd)
    for chunk in out.split("\x00\x01")[1:]:
        sha, an, ae, cn, ce, message, diff = (chunk.split("\x00", 6) + [""] * 7)[:7]
        added, paths, binaries = [], [], []
        path, n, old_left, new_left = None, 0, 0, 0
        for line in diff.splitlines():
            if old_left > 0 or new_left > 0:
                # Inside a hunk the counts say what each line is, so a content
                # line that looks like a header ("++ x" shows as "+++ x") is content.
                if line.startswith("+"):
                    if path is not None:
                        added.append((path, n, line[1:]))
                    n += 1
                    new_left -= 1
                elif line.startswith("-"):
                    old_left -= 1
                continue
            if line.startswith("diff --git "):
                path = None
                header = _header_path(line)
                if header:
                    paths.append(header)
            elif line.startswith(("rename to ", "copy to ")):
                paths.append(_unquote(line.split(" to ", 1)[1]))
            elif line.startswith("+++ "):
                target = _unquote(line[4:])
                path = None if target == "/dev/null" else _strip_prefix(target)
                if path is not None:
                    paths.append(path)
            elif line.startswith("Binary files ") and line.endswith(" differ"):
                target = line[len("Binary files "):-len(" differ")].rsplit(" and ", 1)[-1]
                if _unquote(target) != "/dev/null":
                    binaries.append(_strip_prefix(target))
                    paths.append(binaries[-1])
            elif line.startswith("@@"):
                m = _HUNK.match(line)
                if m:
                    old_left = int(m.group(1) if m.group(1) is not None else 1)
                    n = int(m.group(2))
                    new_left = int(m.group(3) if m.group(3) is not None else 1)
        yield Commit(sha, an, ae, cn, ce, message, added, list(dict.fromkeys(paths)), binaries)


def _blob_texts(sha, path, cwd=None):
    """A binary file's bytes as text the rules can read: as-is, and with NULs
    dropped (UTF-16 text, which git calls binary). None if it cannot be read."""
    r = subprocess.run(["git", "cat-file", "blob", f"{sha}:{path}"], cwd=cwd, capture_output=True)
    if r.returncode:
        return None
    return [r.stdout.decode("latin-1"), r.stdout.replace(b"\x00", b"").decode("latin-1")]


# --- the rules --------------------------------------------------------------

def _rules(text, values, shapes=True):
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


def _identity(short, where, who, name, email, values):
    problems = []
    if not NOREPLY.search(email.strip()):
        problems.append(Problem(short, where, f"{who} is not a noreply address"))
    for rule in _rules(name, values):
        problems.append(Problem(short, where, f"{who} name: {rule}"))
    return problems


def check(rev_args_list, values, cwd=None, shapes=True):
    """Everything the commits in range publish. `shapes` covers added text
    lines only: gitleaks, when it runs, checks those instead. Messages, names,
    paths and binary files are never in a patch gitleaks reads."""
    problems = []
    seen = set()
    for rev_args in rev_args_list:
        for c in commits(rev_args, cwd):
            if c.sha in seen:
                continue
            seen.add(c.sha)
            short = c.sha[:9]
            problems += _identity(short, "commit metadata", "author", c.author_name, c.author, values)
            problems += _identity(short, "commit metadata", "committer", c.committer_name, c.committer, values)
            for rule in _rules(c.message, values):
                problems.append(Problem(short, "commit message", rule))
            flagged = set()
            for path in c.paths:
                for rule in _rules(path, values):
                    flagged.add(path)
                    problems.append(Problem(short, "a file path", rule))
            for path, n, text in c.added:
                place = WITHHELD if path in flagged else f"{path}:{n}"
                for rule in _rules(text, values, shapes and path not in FIXTURE_PATHS):
                    problems.append(Problem(short, place, rule))
            for path in c.binaries:
                place = WITHHELD if path in flagged else f"{path} (binary)"
                texts = _blob_texts(c.sha, path, cwd)
                if texts is None:
                    problems.append(Problem(short, place, "binary file could not be read"))
                    continue
                for rule in dict.fromkeys(r for t in texts for r in _rules(t, values)):
                    problems.append(Problem(short, place, rule))
    return problems


def check_tags(tags, values, cwd=None):
    problems = []
    for sha in tags:
        head, _, message = git("cat-file", "tag", sha, cwd=cwd).partition("\n\n")
        short = sha[:9]
        m = re.search(r"^tagger (.*?) <([^>]*)>", head, re.M)
        if m:
            problems += _identity(short, "tag metadata", "tagger", m.group(1), m.group(2), values)
        name = re.search(r"^tag (.*)$", head, re.M)
        for rule in _rules(name.group(1) if name else "", values):
            problems.append(Problem(short, "tag name", rule))
        for rule in _rules(message, values):
            problems.append(Problem(short, "tag message", rule))
    return problems


def check_refs(lines, values):
    """A pushed ref's name is published too."""
    return [Problem("-", "a pushed ref's name", rule)
            for _, ref, _ in _pushed(lines) for rule in _rules(ref, values)]


def gitleaks(rev_args_list, values, cwd=None):
    """gitleaks' credential rules over added lines, with the shared config, or
    None when either is missing. Its two private-identifier rules are checked
    above already."""
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
                if x.get("RuleID") in ("private-email", "aws-account-id"):
                    continue
                path = str(x.get("File"))
                place = WITHHELD if _rules(path, values) else f"{path}:{x.get('StartLine')}"
                problems.append(Problem(x.get("Commit", "")[:9], place, f"gitleaks {x.get('RuleID')}"))
    return problems


FIX = """\
What was found is not shown: this output is a transcript, and a shift's is a public log.
The commits named are on no remote yet. Rewrite them before pushing:
  author/committer: git config user.email <id>+<login>@users.noreply.github.com
                    git rebase <upstream> --exec 'git commit --amend --no-edit --reset-author'
  content or path:  remove it, then rewrite the commits that added it
                    (git reset --soft <upstream>, recommit)
  a tag:            delete it (git tag -d <name>) and make it again
A secret that reached any remote, log or issue must also be rotated.
Bypassing this is refused in Claude sessions."""


def report(problems, out=sys.stderr):
    commits_hit = sorted({p.commit for p in problems})
    print(f"pre-push: refused, nothing was pushed. {len(problems)} problem(s) in "
          f"{len(commits_hit)} commit(s):", file=out)
    for p in problems:
        # The trace's redactor too, in case a place names something private.
        print(f"  {p.commit}  {shift_trace.redact(p.where)}  {p.rule}", file=out)
    print(FIX, file=out)


def run(rev_args_list, cwd=None, values=None, tags=(), refs=()):
    if not rev_args_list and not tags and not refs:
        return 0
    if values is None:
        tops, common = checkouts(cwd)
        values = held_values(tops=tops, common=common)
    leaks = gitleaks(rev_args_list, values, cwd) if rev_args_list else None
    problems = (check(rev_args_list, values, cwd, shapes=leaks is None) + (leaks or [])
                + check_tags(tags, values, cwd) + check_refs(refs, values))
    if problems:
        report(problems)
        return 1
    return 0


# --- installing it, and keeping it installed ---------------------------------

def install(check_only=False, cwd=ROOT):
    """Point git at .githooks. The setting is shared by every worktree, and a
    worktree on a branch from before the gate has no .githooks/pre-push, so the
    check needs both."""
    try:
        current = git("config", "core.hooksPath", cwd=cwd, check=False).strip()
        top = git("rev-parse", "--show-toplevel", cwd=cwd, check=False).strip()
    except OSError:
        return 0
    present = bool(top) and os.access(os.path.join(top, HOOKS_DIR, "pre-push"), os.X_OK)
    if check_only:
        if current == HOOKS_DIR and present:
            print(f"pre-push gate installed (core.hooksPath = {HOOKS_DIR})")
            return 0
        why = (f"core.hooksPath is {current or 'unset'}; run python3 scripts/prepush_check.py install"
               if current != HOOKS_DIR else
               f"this checkout has no executable {HOOKS_DIR}/pre-push (a branch from before "
               "the gate: rebase it onto main)")
        print(f"pre-push gate NOT installed: {why}")
        return 1
    if current != HOOKS_DIR:
        git("config", "core.hooksPath", HOOKS_DIR, cwd=cwd, check=False)
    return 0


# --- the guard: a Claude session never switches the gate off -------------------
# A speed bump for an honest agent, not a sandbox: it reads each simple command
# the way the shell would split it, so text a commit message, a PR body or a
# heredoc carries is data, and only a git command that skips or repoints the
# hook is refused.

NO_VERIFY = "--no-verify skips the pre-push gate"
REPOINTS = "it changes core.hooksPath, which switches off the pre-push gate"
_HEREDOC = re.compile(r"<<(-?)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")
_ASSIGN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
_CONFIG_ENV = re.compile(r"^GIT_CONFIG_(?:PARAMETERS|KEY_\d+)=", re.I)
_WRAPPERS = {"env", "command", "exec", "nohup", "time", "nice", "sudo"}
_WRAPPER_ARGS = {"-u", "--unset", "-C", "--chdir", "-g", "--group", "-n"}   # options that take one
_SHELLS = {"sh", "bash", "zsh", "dash"}
_GIT_ARGS = {"-C", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--attr-source"}
_CONFIG_ARGS = {"-f", "--file", "--blob", "--type", "--default", "--comment", "--value"}
_CONFIG_READS = {"--get", "--get-all", "--get-regexp", "--get-urlmatch", "-l", "--list",
                 "--get-color", "--get-colorbool", "-e", "--edit", "--rename-section", "--remove-section"}


def _segments(command):
    """A shell command split into its simple commands: at unquoted ; & | ( ) `
    $( and newlines, with comments and heredoc bodies left out."""
    segs, cur, quote, pending, i, n = [], [], None, [], 0, len(command)
    while i < n:
        c = command[i]
        if quote:
            cur.append(c)
            if c == "\\" and quote == '"' and i + 1 < n:
                cur.append(command[i + 1])
                i += 1
            elif c == quote:
                quote = None
            i += 1
            continue
        if c == "\\" and i + 1 < n:
            if command[i + 1] != "\n":            # an escaped newline joins lines
                cur += [c, command[i + 1]]
            i += 2
            continue
        if c in "'\"":
            quote = c
        elif c == "#" and (not cur or cur[-1].isspace()):
            j = command.find("\n", i)
            i = n if j < 0 else j
            continue
        elif command.startswith("<<", i) and not command.startswith("<<<", i):
            m = _HEREDOC.match(command, i)
            if m:
                pending.append((m.group(3), m.group(1) == "-"))
                cur.append(m.group(0))
                i = m.end()
                continue
        elif c in ";&|()`\n" or command.startswith("$(", i):
            segs.append("".join(cur))
            cur = []
            if c == "$":
                i += 1
            if c == "\n":
                for word, dash in pending:        # skip each body to its delimiter
                    while i < n:
                        j = command.find("\n", i + 1)
                        line = command[i + 1:n if j < 0 else j]
                        i = n if j < 0 else j
                        if (line.lstrip("\t") if dash else line) == word:
                            break
                pending = []
            i += 1
            continue
        cur.append(c)
        i += 1
    segs.append("".join(cur))
    return [s for s in segs if s.strip()]


def _words(segment):
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def _repoints(kv):
    """`core.hooksPath=<value>` that sets anything but .githooks."""
    key, _, value = kv.partition("=")
    return key.strip().lower() == "core.hookspath" and value != HOOKS_DIR


def _config_refusal(args):
    mode = None
    if args and args[0] in ("set", "unset"):
        mode, args = args[0], args[1:]
    elif args and args[0] in ("get", "list", "edit", "rename-section", "remove-section"):
        return None
    flags, positional, i = set(), [], 0
    while i < len(args):
        a = args[i]
        if a in _CONFIG_ARGS:
            i += 2
            continue
        if a.startswith("-"):
            flags.add(a.split("=", 1)[0])
        else:
            positional.append(a)
        i += 1
    if not positional or positional[0].lower() != "core.hookspath":
        return None
    if mode == "unset" or flags & {"--unset", "--unset-all"}:
        return REPOINTS
    if flags & _CONFIG_READS or len(positional) < 2:
        return None
    return REPOINTS if positional[1] != HOOKS_DIR else None


def _git_refusal(args):
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-c":
            if i + 1 < len(args) and _repoints(args[i + 1]):
                return REPOINTS
            i += 2
        elif a.startswith("--config-env"):
            kv = a.split("=", 1)[1] if "=" in a else (args[i + 1] if i + 1 < len(args) else "")
            if kv.lower().startswith("core.hookspath="):
                return REPOINTS
            i += 1 if "=" in a else 2
        elif a in _GIT_ARGS:
            i += 2
        elif a.startswith("-"):
            i += 1
        else:
            break
    if i >= len(args):
        return None
    sub, rest = args[i], args[i + 1:]
    if sub == "push":
        # git takes any unambiguous abbreviation of a long option.
        if any(len(a) >= len("--no-veri") and "--no-verify".startswith(a) for a in rest):
            return NO_VERIFY
    elif sub == "config":
        return _config_refusal(rest)
    return None


def _command_refusal(words, depth):
    i = 0
    while i < len(words):
        w = words[i]
        if _ASSIGN.match(w):
            if _CONFIG_ENV.match(w) and "core.hookspath" in w.lower():
                return REPOINTS
            i += 1
        elif os.path.basename(w) in _WRAPPERS:
            i += 1
            while i < len(words) and words[i].startswith("-"):
                i += 2 if words[i] in _WRAPPER_ARGS else 1
        else:
            break
    if i >= len(words):
        return None
    cmd, args = os.path.basename(words[i]), words[i + 1:]
    if cmd in ("export", "declare", "typeset"):
        return next((REPOINTS for a in args if _CONFIG_ENV.match(a) and "core.hookspath" in a.lower()), None)
    if cmd in _SHELLS and "-c" in args and depth < 3:
        k = args.index("-c")
        return refusal(args[k + 1], depth + 1) if k + 1 < len(args) else None
    if cmd == "eval" and depth < 3:
        return refusal(" ".join(args), depth + 1)
    return _git_refusal(args) if cmd == "git" else None


def refusal(command, depth=0):
    """Why a shell command would switch the gate off, or None."""
    for seg in _segments(command or ""):
        why = _command_refusal(_words(seg), depth)
        if why:
            return why
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
        lines = sys.stdin.read().splitlines()
        return run(ranges_from_hook(lines, remote), tags=pushed_tags(lines), refs=lines)
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
