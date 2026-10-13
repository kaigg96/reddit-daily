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
