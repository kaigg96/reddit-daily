"""Every dependency is pinned to an exact version.

The video workflow resolves requirements.txt against PyPI on every run, so
an unpinned line takes whatever was released that morning. Two of them decide
what ships: better-profanity's bundled word list filters posts and comments,
and emoji decides which host lines are dropped. A new release would change
the live selection with no commit to point at (TECH_DEBT, 2026-10-13).
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
# name[extras]==1.2.3, with any environment marker after ";" ignored, so
# `foo; python_version == "3.12"` and `foo==1.*` do not pass as pinned.
PINNED = re.compile(r"^[A-Za-z0-9._\-]+(\[[^\]]*\])?\s*===?\s*[^\s*,;]+$")


def _requirements(name):
    for line in (ROOT / name).read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            yield line


@pytest.mark.parametrize("name", ["requirements.txt", "requirements-dev.txt"])
def test_every_requirement_is_pinned_to_an_exact_version(name):
    unpinned = [r for r in _requirements(name)
                if not PINNED.match(r.split(";", 1)[0].strip())]
    assert not unpinned, f"{name}: pin these with ==: {unpinned}"


# The weekly snapshot job named its packages unpinned (TECH_DEBT, 2026-10-14);
# its fix is a workflow patch only the owner can land, so the line it replaces
# is the one exception until then. A broken release on a Monday would lose that
# week's snapshot for good: there is no backfill.
_UNPINNED_UNTIL_PATCHED = {
    ("weekly-analytics.yml",
     "pip install google-api-python-client google-auth google-auth-httplib2"),
}


def test_workflows_install_only_from_the_pinned_files():
    named = []
    for wf in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
        for line in wf.read_text().splitlines():
            cmd = line.split("#", 1)[0].strip()
            cmd = cmd[len("run:"):].strip() if cmd.startswith("run:") else cmd
            if "pip install" not in cmd or (wf.name, cmd) in _UNPINNED_UNTIL_PATCHED:
                continue
            words = cmd.split("pip install", 1)[1].split()
            # Every word is a flag, a requirements file after -r, or pip itself.
            loose = [w for i, w in enumerate(words)
                     if not w.startswith("-") and w != "pip"
                     and not (i and words[i - 1] == "-r")]
            if loose:
                named.append(f"{wf.name}: {cmd}")
    assert not named, f"install from requirements*.txt, not by name: {named}"
