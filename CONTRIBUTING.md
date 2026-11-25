# Contributing

How a change gets from an issue into `main`. It applies the same way to people and to coding agents – that is
what the Norma track scores as "consistency across authors". `AGENTS.md` holds the short rules; this file
holds the steps. If the two disagree, fix one of them by PR.

Reading time: 5 minutes. Point your agent at this file and at `AGENTS.md` before its first task.

## 1. Setup (once, 5 minutes)

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if `uv --version` fails:
   `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `pipx install uv`).
2. `uv sync` – creates `.venv` with the exact versions from `uv.lock`, including ruff and pytest.
3. `cp .env.example .env` and add your keys. Never paste a key into chat, an issue or a PR.
4. Norma (see section 6): sign in at [norma.qualityclouds.com](https://norma.qualityclouds.com) with GitHub,
   join the team workspace, then connect your agent. Claude Code reads `.mcp.json` in this repo; for other agents
   see [Quality Clouds' setup page](https://github.com/qualityclouds/ai-summit-barcelona-2026/blob/main/examples/mcp-config.md).
5. Check: `tools/check` prints `0 must fix`.

Why uv: one lock file, so every author and every agent runs the same versions; `uv run` syncs before it runs.
([uv docs: project layout](https://docs.astral.sh/uv/concepts/projects/layout/))

## 2. From issue to merge

1. **Issue.** Every piece of work is a GitHub issue made with the "Task" form: goal, done-when command, files
   allowed to change, owner. No issue, no PR – except a typo fix.
2. **Branch.** `<name>/<topic>`, e.g. `kat/fetch-timeout`. One branch per person and task; two agents never
   share a checkout.
3. **Work.** Your agent runs the Norma check on every file it changes (section 6) and the tests before it says
   "done".
4. **Check.** `tools/check` must print `0 must fix`.
5. **PR.** Fill the template block by block (section 3). Link the issue with `Closes #n`. Label `needs-review`.
6. **Two reviews** (section 4). Only a `Bug:` blocks.
7. **Merge.** A person who is not the author squash-merges when CI is green and both reviews are there.
   Agents never merge. Delete the branch.

Small PRs: one topic, ideally under 200 changed lines. A big change becomes several issues.

## 3. The PR description

`.github/pull_request_template.md` has blocks between markers, e.g. `<!-- pr-test:start -->` …
`<!-- pr-test:end -->`. Each block has a comment that says exactly what goes in.

- **Keep the markers.** A person or an agent can fill or replace exactly one block. Example prompt:
  "Fill only the block `pr-norma` of PR #12 from the Norma results of this branch. Change nothing else."
- **Write what the diff cannot show.** No list of changed files, no test counts.
- **Required blocks:** `pr-summary`, `pr-issue`, `pr-test`, `pr-norma`, `pr-ai`. CI job `pr / blocks-filled`
  fails while one of them is empty or still contains `…`.
- **"I ran" vs. "I only read".** In `pr-ai`, keep the two apart. A claim you did not run goes under "only read".

## 4. Review: two independent views

Every PR gets two reviews before the merge. Neither comes from the session that wrote the code.

| View | Who | Questions |
|---|---|---|
| **A – correctness/security** | a person who is not the author (also merges) | 1. Does the `pr-test` command give the stated output? Did you run it? 2. Can text from a fetched page reach a prompt as instructions, or a shell, `eval` or a file path? 3. Any key, token, or file from `data/`, `out/`, `results/`? 4. Do a timeout, 403 or empty page end in verdict `unclear`, not a crash or a silently dropped reason? 5. Does every reason carry a fetched URL and a quote that is on that page? |
| **B – consistency/Norma** | a fresh agent session (or a second person) that gets only the PR number and these questions | 1. Does the `pr-norma` block match the Norma GitHub App comment on this PR? 2. Does every finding have a `DECISIONS.md` row? 3. Does it duplicate an existing helper or change a module someone else owns? 4. Does it follow the house rules in `AGENTS.md` (HTTP, errors, logging, config)? A clash is logged as `conflict`. 5. Would a judge believe the reason for each accepted finding? |

Each review is one GitHub review. Its first line is a marker, then who wrote it:

```
<!-- review:correctness -->
**Review A: correctness/security** by @handle (person)
Verdict: ok   (or: Bug: 2)
Ran: `uv run pytest tests/test_verify.py` → 4 passed      Only read: src/judge.py
1. … 2. … 3. … 4. … 5. …
```

For view B the first line is `<!-- review:consistency -->`, and the second says
"by <agent>, separate session, posted by @handle". CI job `review-gate` stays red until both markers are there.

An agent review posted from the author's own account is a "Comment" review; it never counts as an approval
(GitHub does not let authors approve their own PR). Say honestly who read what.

**Comments** start with their kind: `Bug:` (must be fixed before the merge – blocks), `Question:` (only the
author can answer; answer before the merge), `Note:` (information). One clear sentence first, details after,
with `file:line`. If an AI drafted your comment, add "(drafted with <agent>)".

## 5. Labels

| Label | Means | Set by |
|---|---|---|
| `task` | issue: one piece of work, one PR | the form |
| `needs-review` | PR ready; a reviewer is next | author |
| `author-turn` | a `Bug:` or `Question:` is open; after the fix, click "Re-request review" | reviewer |
| `second-opinion` | touches fetched text, keys, shell or network; view A must be a person | anyone |
| `blocked` | waits for a decision; the comment says from whom | anyone |
| `norma` | has a Norma finding to fix, accept or log as conflict | anyone |

Create them once: `tools/labels.sh` (needs `gh` with write access).

## 6. Norma: the check inside the agent loop

Norma checks code against a fixed set of rules for our stack: "same file, same rules, same verdict every time"
([norma-mcp](https://github.com/qualityclouds/norma-mcp)). The GitHub App also comments on every PR.

Tools your agent gets over MCP (`https://api.qualityclouds.ai/mcp`, OAuth, no key):

| Tool | When |
|---|---|
| `get_rulesets`, `get_rules_for_ruleset` | once at the start: which rules apply, with ID, severity and fix guidance |
| `live_check` | after each file the agent creates or changes, before it moves on |
| `get_open_issues` | before a PR and before the 18:45 freeze |
| `register_applied_actions` | after a check: what was verified or fixed, and by which model |

The skill `.claude/skills/check-and-fix/` runs this loop in Claude Code (from Quality Clouds' workshop, MIT).
If `live_check` answers `unlinked`, the repo is not linked in the Norma workspace yet – tell the Norma owner.

Rules for findings:
1. **Fix the cause.** Never delete or bend code just to make a finding go away – the Norma brief scores that
   with zero. No suppress comments.
2. **Every finding gets one row in `DECISIONS.md`** before the merge: rule ID, severity, file:line, fixed /
   accepted / conflict, reason, check before → after.
3. **Accept only with a reason a judge would believe**, tied to our task. Never accept a security HIGH.
4. **A conflict** is when two authors (or agents) do the same thing differently or repeat a mistake. Log it,
   then fix it once for everyone (a shared helper or a house rule in `AGENTS.md`).

## 7. Tests and style

- Tests live in `tests/`, fixtures (hand-written HTML) in `tests/fixtures/`. **No network in tests.** Pass the
  fetcher and the LLM client in as parameters, so tests can use fakes.
- Never use pages from the labelled set or the live products as fixtures – that is event data (`data/`).
- Style is whatever `uv run ruff format` writes. Lint rules are in `pyproject.toml`; change them by PR.
- First tests worth writing: the verifier accepts a quote that is on the page (also with `&nbsp;`, line breaks,
  other case) and drops one that is not; HTML to text drops `<script>`; a verdict from a fake LLM matches
  `schema/verdict.schema.json`; bad JSON from the LLM gives `unclear`, not a crash.

## 8. When CI fails

| Job | Run locally |
|---|---|
| `guard` | `git ls-files -z \| python3 tools/check_tracked.py --scan` |
| `pr / lint-test` | `uv run ruff format --check && uv run ruff check && uv run pytest` |
| `pr / blocks-filled` | read the job log: it names the empty block; edit the PR description |
| `review-gate` | not a code problem: a review view is missing (section 4) |

On a private repo on GitHub Free, GitHub cannot enforce required checks or reviews
([GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans); our plan: not
verified). So it is a team rule: **merge only when every check is green.**
