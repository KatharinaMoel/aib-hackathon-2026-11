#!/usr/bin/env python3
"""Decide which lane a pull request is in, and check what that lane needs (CONTRIBUTING.md, section 4).

Lanes, so small PRs stay fast and risky PRs get a second look:
- fast:      only Markdown files, and none of them a rule file -> needs only the pr-summary block;
             no issue, no review marker (the person who merges is the second pair of eyes).
- standard:  everything else -> all required blocks, "Closes #n", review A (correctness/security).
- two-views: label `norma` or `second-opinion`, or a change to rules, CI, agent config, tools or schema
             -> standard plus review B (consistency/Norma).
- quick:     label `quick`, only until the skeleton (#1) is merged and in emergency mode (docs/TEAM.md)
             -> pr-summary, pr-test, pr-norma, review A (may be given at the table).

Used by CI (.github/workflows/pr.yml and review-gate.yml) and by tests/test_pr_lane.py. Run by hand:
  FILES="README.md" LABELS="" BODY="..." TITLE="docs: ..." python3 tools/pr_lane.py blocks
  FILES="src/a.py" LABELS="" AUTHOR=kat REVIEWS='[{"user":"bo","body":"<!-- review:correctness -->"}]' \
      python3 tools/pr_lane.py reviews
"""

import json
import os
import re
import sys

# Files and folders whose change affects every author or agent: they always get two views.
RULE_FILES = {
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CLAUDE.md",
    "CODEOWNERS",
    "pyproject.toml",
    "uv.lock",
}
RULE_DIRS = (".github/", ".claude/", "tools/", "schema/")
RISK_LABELS = {"norma", "second-opinion"}
ALL_BLOCKS = ["pr-summary", "pr-issue", "pr-test", "pr-norma", "pr-ai"]
# Squash-merge turns the PR title into the commit on main, so the title follows the commit rule.
TITLE = re.compile(r"^(feat|fix|docs|test|chore|refactor): .+")


def lane(files, labels):
    """Return the lane name and what it needs: blocks, whether an issue link is needed, review views."""
    files = [f for f in files if f]
    rule_change = any(f in RULE_FILES or f.startswith(RULE_DIRS) for f in files)
    if files and all(f.endswith(".md") for f in files) and not rule_change:
        return {"lane": "fast", "blocks": ["pr-summary"], "issue": False, "reviews": []}
    # quick: skeleton phase and emergency mode (docs/TEAM.md) - fewer blocks, view A only, no issue needed.
    if "quick" in labels:
        blocks = ["pr-summary", "pr-test", "pr-norma"]
        return {"lane": "quick", "blocks": blocks, "issue": False, "reviews": ["correctness"]}
    reviews = ["correctness"]
    if rule_change or RISK_LABELS & set(labels):
        reviews.append("consistency")
    name = "two-views" if len(reviews) == 2 else "standard"
    return {"lane": name, "blocks": ALL_BLOCKS, "issue": True, "reviews": reviews}


def missing_blocks(body, need, title):
    """List the problems in the PR description and title; empty list = all good."""
    problems = []
    for name in need["blocks"]:
        m = re.search(rf"<!-- {name}:start -->(.*?)<!-- {name}:end -->", body or "", re.S)
        text = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip() if m else ""
        if not text or "…" in text:
            problems.append(f"{name}: empty, missing or still contains '…'")
    if need["issue"] and not re.search(r"(?i)\b(closes|fixes|resolves) #\d+", body or ""):
        problems.append("pr-issue: no 'Closes #n'")
    if not TITLE.match(title or ""):
        problems.append(
            "title: must read '<type>: <summary>', type feat/fix/docs/test/chore/refactor"
        )
    return problems


def missing_reviews(reviews, need, author):
    """List the review views that are still missing.

    View A (correctness) must come from a person other than the author. View B (consistency) may be posted
    from the author's account, because it is usually a fresh agent session; its first lines say so.
    """

    def found(view):
        allowed = [r for r in reviews if view != "correctness" or r.get("user") != author]
        return any(f"<!-- review:{view} -->" in (r.get("body") or "") for r in allowed)

    return [v for v in need["reviews"] if not found(v)]


def main():
    files = os.environ.get("FILES", "").split()
    labels = [x for x in os.environ.get("LABELS", "").split(",") if x]
    need = lane(files, labels)
    print(
        f"Lane: {need['lane']} ({len(files)} changed file(s); labels: {', '.join(labels) or 'none'})"
    )
    if sys.argv[1:] == ["blocks"]:
        problems = missing_blocks(os.environ.get("BODY", ""), need, os.environ.get("TITLE", ""))
    elif sys.argv[1:] == ["reviews"]:
        reviews = json.loads(os.environ.get("REVIEWS", "[]"))
        missing = missing_reviews(reviews, need, os.environ.get("AUTHOR", ""))
        problems = [f"missing review view: {v} (first line `<!-- review:{v} -->`)" for v in missing]
    else:
        sys.exit(
            "usage: pr_lane.py blocks|reviews (inputs via environment variables, see docstring)"
        )
    for p in problems:
        print(f"  FAIL  {p}")
    print(f"{len(problems)} problem(s) - see CONTRIBUTING.md, sections 3 and 4.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
