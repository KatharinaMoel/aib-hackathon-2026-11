#!/usr/bin/env python3
"""Fail if private material is tracked: `git ls-files -z | python3 tools/check_tracked.py [--scan]`.

Paths are read NUL-separated (`-z`), so git does not quote names with spaces or non-ASCII characters
and they cannot slip past the patterns. `--scan` also searches tracked files for token-like strings;
a file that cannot be read counts as a failure, not as clean.

Run by CI job `guard` (.github/workflows/guard.yml); `tools/check` does the same path check locally.
See docs/FILES.md.
"""

import re
import subprocess
import sys

# Same patterns as PRIVATE and TOKEN in tools/check; change both together. Explained there.
DENY = [
    r"^data/",
    r"^out/",
    r"^results/",
    r"^local/",
    r"(^|/)\.env($|\.)(?!example$)",
    r"\.labels\.",
]
TOKEN = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|tvly-[A-Za-z0-9]{20,})")


def split_nul(raw):
    # surrogateescape: a file name that is not valid UTF-8 is kept, not dropped.
    return [x.decode("utf-8", "surrogateescape") for x in raw.split(b"\0") if x]


paths = split_nul(sys.stdin.buffer.read())
bad = [p for p in paths if any(re.search(d, p) for d in DENY)]
for p in bad:
    print(f"  ! tracked private path: {p}")

problems = []
if "--scan" in sys.argv:
    for p in split_nul(subprocess.run(["git", "ls-files", "-z"], capture_output=True).stdout):
        try:
            with open(p, encoding="utf-8", errors="ignore") as fh:
                if TOKEN.search(fh.read()):
                    problems.append(f"token-like string in: {p}")
        except OSError as err:
            problems.append(f"cannot read {p}: {err}")
    for msg in problems:
        print(f"  ! {msg}")

sys.exit(1 if bad or problems else 0)
