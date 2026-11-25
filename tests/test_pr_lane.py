"""tools/pr_lane.py decides the PR lane and what it needs (CONTRIBUTING.md, section 4).

Covers: which files make a PR fast, standard or two-views; block and title checks; that review A by the
author never counts, while review B may come from the author's account (a fresh agent session). CI uses the same functions, so a green test here means CI applies the same rules.
"""

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "pr_lane", Path(__file__).parent.parent / "tools" / "pr_lane.py"
)
pr_lane = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pr_lane)

FILLED = (
    "\n".join(f"<!-- {b}:start -->\ntext\n<!-- {b}:end -->" for b in pr_lane.ALL_BLOCKS)
    + "\nCloses #3"
)


def test_docs_only_is_fast():
    assert pr_lane.lane(["README.md", "docs/SIGNALS.md"], [])["lane"] == "fast"


def test_rule_file_is_never_fast():
    assert pr_lane.lane(["AGENTS.md"], [])["lane"] == "two-views"
    assert pr_lane.lane([".github/workflows/pr.yml"], [])["lane"] == "two-views"


def test_code_is_standard_unless_labelled():
    assert pr_lane.lane(["src/fetch.py"], [])["lane"] == "standard"
    assert pr_lane.lane(["src/fetch.py"], ["second-opinion"])["lane"] == "two-views"


def test_fast_lane_needs_only_summary_and_title():
    need = pr_lane.lane(["README.md"], [])
    body = "<!-- pr-summary:start -->\nFix a typo.\n<!-- pr-summary:end -->"
    assert pr_lane.missing_blocks(body, need, "docs: fix typo") == []
    assert pr_lane.missing_blocks(body, need, "Fix typo") != []


def test_standard_lane_needs_all_blocks_and_issue():
    need = pr_lane.lane(["src/fetch.py"], [])
    assert pr_lane.missing_blocks(FILLED, need, "feat: fetch helper") == []
    assert pr_lane.missing_blocks(FILLED.replace("Closes #3", ""), need, "feat: x") != []
    assert pr_lane.missing_blocks(FILLED.replace("text", "…", 1), need, "feat: x") != []


def test_author_review_does_not_count():
    need = pr_lane.lane(["src/fetch.py"], [])
    own = [{"user": "kat", "body": "<!-- review:correctness -->"}]
    other = [{"user": "bo", "body": "<!-- review:correctness -->"}]
    assert pr_lane.missing_reviews(own, need, "kat") == ["correctness"]
    assert pr_lane.missing_reviews(other, need, "kat") == []


def test_view_b_may_come_from_the_authors_account():
    need = pr_lane.lane(["AGENTS.md"], [])
    reviews = [
        {"user": "bo", "body": "<!-- review:correctness -->"},
        {"user": "kat", "body": "<!-- review:consistency -->\nby Claude Code, separate session"},
    ]
    assert pr_lane.missing_reviews(reviews, need, "kat") == []


def test_quick_lane_needs_view_a_and_three_blocks():
    need = pr_lane.lane(["src/fetch.py", "AGENTS.md"], ["quick"])
    assert need["lane"] == "quick"
    assert need["reviews"] == ["correctness"]
    assert need["blocks"] == ["pr-summary", "pr-test", "pr-norma"]
