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
   Commands that need keys run as `uv run --env-file .env <command>`.
   Not the same as `.venv`: `.env` holds keys and settings (you write it), `.venv` holds the installed packages
   (`uv sync` writes it). Neither is committed.
4. Norma (see section 6): sign in at [norma.qualityclouds.com](https://norma.qualityclouds.com) with GitHub,
   join the team workspace, then connect your agent. Claude Code reads `.mcp.json` in this repo; for other agents
   see [Quality Clouds' setup page](https://github.com/qualityclouds/ai-summit-barcelona-2026/blob/main/examples/mcp-config.md).
5. Check: `tools/check` prints `0 must fix`.

Why uv: one lock file, so every author and every agent runs the same versions; `uv run` syncs before it runs.
([uv docs: project layout](https://docs.astral.sh/uv/concepts/projects/layout/))

## 2. From issue to merge

1. **Issue.** Code work starts from a GitHub issue made with the "Task" form: goal, done-when command, files
   allowed to change, owner. Docs-only changes (fast lane, section 4) need no issue.
2. **Claim it.** Assign yourself before you start, so nobody does the same work twice. Hold **at most one issue
   in progress and one PR waiting for review**. While your PR waits: review someone else's PR first, then start
   the next issue in its own branch. Fast-lane PRs do not count. Your agent may work on several files at once –
   but on one issue. Agents never open issues on their own.
3. **Branch.** `<name>/<topic>`, e.g. `kat/fetch-timeout`. One branch per person and task; two agents never
   share a checkout.
4. **Work.** Your agent runs the Norma check on every file it changes (section 6) and the tests before it says
   "done".
5. **Check.** `tools/check` must print `0 must fix`.
6. **PR.** Title `<type>: <summary>` (it becomes the commit on `main`). Fill the blocks your lane needs
   (sections 3 and 4).
7. **Review** for your lane (section 4). Only a `Bug:` blocks.
8. **Merge.** A person squash-merges when every check is green. The author may merge their own PR once another
   person approved it; GitHub does not count the author's own approval. Agents never merge.
   Delete the branch.

Small PRs: one topic, ideally under 200 changed lines. A big change becomes several issues.
Why the limit: with agents it is easy to start five things and finish none; under time pressure, merged work
counts, open work does not. Reviewing first keeps everyone's PRs moving (pattern from smolagents'
[CONTRIBUTING.md](https://github.com/huggingface/smolagents/blob/main/CONTRIBUTING.md)).

## 3. The PR description

`.github/pull_request_template.md` has blocks between markers, e.g. `<!-- pr-test:start -->` …
`<!-- pr-test:end -->`. Each block has a comment that says exactly what goes in.

- **Keep the markers.** A person or an agent can fill or replace exactly one block. Example prompt:
  "Fill only the block `pr-norma` of PR #12 from the Norma results of this branch. Change nothing else."
- **Write what the diff cannot show.** No list of changed files, no test counts.
- **Required blocks:** fast lane: only `pr-summary`. Standard and two-views: `pr-summary`, `pr-issue`,
  `pr-test`, `pr-norma`, `pr-ai`. CI job `pr / blocks-filled` fails while one of them is empty or still
  contains `…`, or while the title does not read `<type>: <summary>`.
- **"I ran" vs. "I only read".** In `pr-ai`, keep the two apart. A claim you did not run goes under "only read".

## 4. Review: lanes

Not every PR needs the same care. `tools/pr_lane.py` decides the lane from the changed files and labels; CI
uses it, so nobody has to decide by hand.

| Lane | When | Needs before the merge | Typical time |
|---|---|---|---|
| **fast** | only Markdown files, none of them a rule file (`AGENTS.md`, `CONTRIBUTING.md`, `CLAUDE.md`) and none under `.github/` or `.claude/` | block `pr-summary`; the person who merges reads the diff. No issue, no review marker | 2 min |
| **standard** | everything else, e.g. code in `src/` | all five blocks, `Closes #n`, **view A** | 10 min |
| **two-views** | label `norma` or `second-opinion`, or a change to rules, CI, agent config, `tools/`, `schema/` | standard plus **view B** | +5 min |
| **quick** | label `quick`: only until the walking skeleton (#1) is merged, and in emergency mode (`docs/TEAM.md`) | blocks `pr-summary`, `pr-test`, `pr-norma`; view A, which may be given at the table and recorded in one line | 5 min |

Set `second-opinion` when a PR touches fetched text, keys, shell or network. Set `norma` when it fixes,
accepts or causes a Norma finding.

| View | Who | Questions |
|---|---|---|
| **A – correctness/security** | a person who is not the author | 1. Does the `pr-test` command give the stated output? Did you run it? 2. Can text from an MCP response reach a prompt as instructions, or a shell, `eval` or a file path? 3. Any key, token, or file from `data/`, `out/`, `results/`? 4. Do a timeout, an MCP error or an empty answer end in a clear message, not a crash or a silently wrong number? 5. Does every number carry the logged MCP call it came from? |
| **B – consistency/Norma** | a fresh agent session (or a second person) that gets only the PR number and these questions; may be posted from the author's account. With label `second-opinion`, B also answers A-questions 2 and 4 | 1. Does the `pr-norma` block match the Norma GitHub App comment on this PR? 2. Is every finding listed in `pr-norma`? 3. Does it duplicate an existing helper or change a module someone else owns? 4. Does it follow the house rules in `AGENTS.md` (HTTP, errors, logging, config)? A clash is logged as `conflict`. 5. Would a judge believe the reason for each accepted finding? |

Prompt for a view-B session (paste as it is, nothing else):
"Review PR #<n> in this repo as view B, CONTRIBUTING.md section 4. Answer the five B-questions (with label
second-opinion also A-questions 2 and 4), one line each, with file:line. Run nothing that changes files.
Start your answer with `<!-- review:consistency -->`."

Each review is one GitHub review. Its first line is a marker, then who wrote it:

```
<!-- review:correctness -->
**Review A: correctness/security** by @handle (person)
Verdict: ok   (or: Bug: 2)
Ran: `uv run pytest tests/test_verify.py` → 4 passed      Only read: src/judge.py
1. … 2. … 3. … 4. … 5. …
```

For view B the first line is `<!-- review:consistency -->`, and the second says
"by <agent>, separate session, posted by @handle". CI job `review-gate` stays red until the markers the lane
needs are there. View A from the author's own account does not count.

An agent review posted from the author's own account is a "Comment" review; it never counts as an approval
(GitHub does not let authors approve their own PR). Say honestly who read what.

**Comments** start with their kind: `Bug:` (must be fixed before the merge – blocks), `Question:` (only the
author can answer; answer it, but it does not block), `Note:` (information). One clear sentence first, details after,
with `file:line`. If an AI drafted your comment, add "(drafted with <agent>)".

### Maintainers

Maintainers review changes to the rules (`AGENTS.md`, `CONTRIBUTING.md`), CI, agent config, `tools/` and
`schema/` – always someone who is not the author. After that approval, the author may merge. We name 2–3 maintainers at the start; anyone on the team
can be one. (On a personal GitHub repo every collaborator has the same write access, so "maintainer" is a team
role, not a GitHub setting.)

## 5. Labels

We sit at one table, so we use few labels:

| Label | Means | Set by |
|---|---|---|
| `task` | issue: one piece of work, one PR | the form |
| `second-opinion` | touches fetched text, keys, shell or network; adds view B | author or reviewer |
| `norma` | fixes, accepts or causes a Norma finding; adds view B | author or reviewer |
| `quick` | skeleton phase and emergency mode only: fewer blocks, view A at the table | announced out loud to the team |

Create them once: `tools/labels.sh` (needs `gh` with write access). Who is waiting for whom we say out loud.

## 6. Norma: the check inside the agent loop

Norma checks code against a fixed set of rules for our stack: "same file, same rules, same verdict every time"
([norma-mcp](https://github.com/qualityclouds/norma-mcp)). The GitHub App also comments on every PR.

Tools your agent gets over MCP (`https://api.qualityclouds.ai/mcp`, OAuth, no key):

| Tool | When |
|---|---|
| `get_rulesets`, `get_rules_for_ruleset` | once at the start: which rules apply, with ID, severity and fix guidance |
| `live_check` | when a file is finished (not after every edit), and once on all changed files before `tools/check` |
| `get_open_issues` | before a PR and before the 18:45 freeze |
| `register_applied_actions` | after a check: what was verified or fixed, and by which model |

The skill `.claude/skills/check-and-fix/` runs this loop in Claude Code (from Quality Clouds' workshop, MIT).
If `live_check` answers `unlinked`, the repo is not linked in the Norma workspace yet – tell the Norma owner.

Rules for findings:
1. **Fix the cause.** Never delete or bend code just to make a finding go away – the Norma brief scores that
   with zero. No suppress comments.
2. **Every finding goes into the `pr-norma` block** of its PR: rule ID, severity, file:line, fixed / accepted /
   conflict, reason, check before → after. The Norma owner copies all rows into `DECISIONS.md` in one PR at
   17:30. (Many branches appending to the same table at once would cause merge conflicts.) Only the
   `baseline` row (first check after the first code PR) goes in directly. A second sweep for PRs
   merged after 17:30 happens inside the `DEFENCE.md` PR at 18:15.
3. **Accept only with a reason a judge would believe**, tied to our task. Never accept a security HIGH.
4. **A conflict** is when two authors (or agents) do the same thing differently or repeat a mistake. Log it,
   then fix it once for everyone (a shared helper or a house rule in `AGENTS.md`).

## 7. Tests and style

- Tests live in `tests/`, fixtures (recorded or hand-written MCP responses) in `tests/fixtures/`. **No network in
  tests.** Pass the MCP client and the LLM client in as parameters, so tests can use fakes.
- Never commit recorded responses with real idealo data as fixtures – they go in `data/`. Fixtures use made-up
  products.
- **Tests never call an LLM, a paid API or the network.** A fixed bug gets a test that fails before the fix
  (pattern from browser-use's [AGENTS.md](https://github.com/browser-use/browser-use/blob/main/AGENTS.md)).
- Style is whatever `uv run ruff format` writes. Lint rules are in `pyproject.toml`; change them by PR.
- First tests worth writing: the MCP client turns a recorded response into our data model; an MCP error or an
  empty answer gives a clear message, not a crash; every number in the output keeps its MCP call reference;
  bad JSON from an LLM (if we use one) does not crash the run.

## 8. When CI fails

| Job | Run locally |
|---|---|
| `guard` | `git ls-files -z \| python3 tools/check_tracked.py --scan` |
| `pr / lint-test` | `uv run ruff format --check && uv run ruff check && uv run pytest` |
| `pr / blocks-filled` | read the job log: it names the lane, the empty block or the title problem; edit the PR description or title |
| `review-gate` | not a code problem: a review view for this lane is missing (section 4) |
| any of the two above, by hand | `FILES="src/a.py" TITLE="feat: x" BODY="$(cat body.md)" python3 tools/pr_lane.py blocks` |

On a private repo on GitHub Free, GitHub cannot enforce required checks or reviews
([GitHub plans](https://docs.github.com/en/get-started/learning-about-github/githubs-plans); our plan: not
verified). So it is a team rule: **merge only when every check is green.**
