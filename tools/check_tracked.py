#!/usr/bin/env python3
"""Fail if private material is tracked: `git ls-files | python3 tools/check_tracked.py`."""
import re
import sys

DENY = [r"^data/", r"^out/", r"^results/", r"(^|/)\.env($|\.)(?!example$)", r"\.labels\."]
TOKEN = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|tvly-[A-Za-z0-9]{20,})")

bad = [p for p in (l.strip() for l in sys.stdin) if p and any(re.search(d, p) for d in DENY)]
for p in bad:
    print(f"  ! tracked private path: {p}")
leaks = []
if "--scan" in sys.argv:
    import subprocess
    for p in subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split():
        try:
            if TOKEN.search(open(p, encoding="utf-8", errors="ignore").read()):
                leaks.append(p)
        except OSError:
            pass
    for p in leaks:
        print(f"  ! token-like string in: {p}")
sys.exit(1 if bad or leaks else 0)
