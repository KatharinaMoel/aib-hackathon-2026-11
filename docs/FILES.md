# What is this file?

One entry per file or folder: **What** it is · **Why** we have it · **Read by** (a person, a coding agent, CI or
GitHub) · **Change** (when and how). The one-screen map of the repo is in `README.md`, "Repo map".

Where a list changes on the day (steps, fields, rules), this page points to the file that holds it instead of
copying it. "CI" (continuous integration) means the checks GitHub runs on every push and pull request (PR); they
live in `.github/workflows/`.

## Start here

**`README.md`** – the task (idealo challenge), what the brief says, what is still open, the repo map, how to run.
Why: the first page GitHub shows. Read by: everyone, judges (submission notes at the end). Change: by PR when we
learn something; fill "For the submission" at 18:15.

**`docs/FILES.md`** (this page) – what every file is for. Why: keep the overview without opening every file.
Read by: people, agents looking for where something lives. Change: in the PR that adds, removes or renames a
file.

**`docs/TEAM.md`** – agreement (a proposal), roles, the checkpoints other files refer to, fallbacks, skeleton
phase and emergency mode, submission checklist. The detailed minute plan stays with the facilitator, outside the
repo. Why: 3–5 strangers need one shared frame. Read by: people. Change: at the start when the team agrees;
later by PR.

**`docs/INTRO.md`** – how the repo came about: principles, the steps and sources it was built from, what is
prepared and what the team decides together at the start, and a one-page cheat sheet.
- **Why:** strangers join at 15:00 and need to know what is already done and why.
- **Read by:** everyone at the start; the owner for the intro talk.
- **Change:** by PR (fast lane) when a decision changes.

**`docs/PROPOSALS.md`** – practices that may help; not rules. Why: background for the decisions at the start. Read by:
people. Change: cross out what we don't want; move a picked practice into `AGENTS.md` or `CONTRIBUTING.md` by
PR.

**`src/README.md`** – placeholder for the code. Why: git does not track empty folders; the code is built on the
day, once the team has picked the idea. Read by: people, agents. Change: once code exists.

**`eval/README.md`** – how we check the prototype on a fixed case list. Empty until the idea is picked. Why: we
measure every change the same way. Read by: the eval owner and their agent. Change: by PR; the eval command goes
into `AGENTS.md`, "Stack and commands".

## Rules for people and agents

**`AGENTS.md`** – the one rule file: numbered rules, how we write, house rules for code, commands, output
contract, where things are, git flow. Why: every author – person or agent – follows the same rules; Norma scores
that consistency. Read by: Codex, Cursor, Copilot directly ([agents.md](https://agents.md)); Claude Code through
`CLAUDE.md`; people. Change: by PR only; a maintainer who is not the author reviews (`CONTRIBUTING.md`, "Maintainers"). Always the two-views lane.

**`CLAUDE.md`** – a header comment and `@AGENTS.md`. The `@` line makes Claude Code load `AGENTS.md`. Why:
Claude Code reads `CLAUDE.md`, not `AGENTS.md` ([Claude Code: memory](https://code.claude.com/docs/en/memory)).
Read by: Claude Code at session start. Change: never add rules here; put them in `AGENTS.md`.

**`CONTRIBUTING.md`** – the steps from issue to merge: setup, claim rule, PR description, the three review lanes,
labels, the Norma loop, tests, what to do when CI fails. Why: `AGENTS.md` has the short rules, this file the
steps. Read by: people and agents before their first task. Change: by PR; if it disagrees with `AGENTS.md`, fix
one of them in the same PR.

**`DECISIONS.md`** – one row per decision or Norma finding (kinds and columns are explained at the top of the
file). Why: Norma scores fixed findings and accepted trade-offs; this log is our evidence and the source for
`DEFENCE.md`. Read by: the Norma owner, people. Change: authors write findings in their PR's `pr-norma` block;
the Norma owner copies them here in one PR at 17:30, so parallel branches do not clash on one table. Never
rewrite old rows.

**`DEFENCE.md`** – the draft of the Norma note for the submission form: fixed, accepted and conflict, each with
rule, file and reason, plus the policy. Why: 60 of 100 Norma points depend on that note. Read by: the person who
submits. Change: write it at 18:15 from `DECISIONS.md`.

## Code and tests

**`pyproject.toml`** – the project settings: Python version, dependencies, dev tools and the ruff and pytest
config. Ruff does formatting and "lint" (an automatic check for mistakes and banned patterns); several of its
rules mirror Norma rules, explained in comments in the file. Read by: uv, ruff, pytest. Change: packages with
`uv add <package>` (dev tools: `uv add --dev`), never by hand or with pip; lint rules by PR.

**`uv.lock`** – the "lock file": the exact version and checksum of every package. Why: `pyproject.toml` says
"pytest 9 or newer", the lock file says which one, so everyone and CI run the same code. Read by: uv; CI runs
`uv sync --locked`, which fails if the lock file does not match `pyproject.toml`. Change: **never by hand** –
`uv add`, `uv remove` or `uv lock` regenerate it. Commit it with `pyproject.toml`.

**`.python-version`** – one line, `3.12`; uv uses it for `.venv`. No comment in the file, to keep it a plain
value. Change: only with a team OK, together with `requires-python` in `pyproject.toml` and `python-version` in
`.github/workflows/pr.yml`.

**`.env.example`, `.env`, `.venv`** –
- `.env.example` (tracked): the key names with empty values, one comment per key. Add a name when code needs a new
  key; never a value.
- `.env` (not tracked; you write it with `cp .env.example .env`): your real keys. Commands that need them run as
  `uv run --env-file .env <command>`. Claude Code may not read it (`.claude/settings.json`).
- `.venv` (not tracked; `uv sync` writes it): the "virtual environment", the installed packages for this project
  only. If it breaks, delete it and run `uv sync`.

**`tests/`** – pytest tests: for now only `test_pr_lane.py` (below). `tests/fixtures/README.md` sets the rules
for fixtures ("fixture" = fixed test input; here recorded or hand-written idealo MCP responses about made-up
products). Not covered: product code, which does not exist yet; `CONTRIBUTING.md`, section 7 lists the first
tests worth writing. Read by: pytest, CI `pr / lint-test`. Change: add a test with every module; tests never call
an LLM, a paid API or the network.

**`src/giftbot/`** – the gift bot. `src/giftbot/README.md` says how to run, try, test and change the Telegram
side (`bot.py`, `state.py`, `agent.py`, `wishlist.py`); `docs/GIFT_BOT.md` holds the idea and the contract.
Read by: everyone who works on the bot, and their agents. Change: by PR, with a test in `tests/test_giftbot_*.py`.

**`tests/test_pr_lane.py`** – tests for `tools/pr_lane.py`: which files make a PR fast, standard or two-views;
the block and title checks; that review A from the author never counts while review B may. Why: CI uses the same
functions, so a green test means CI applies these rules. Change: with every change to `tools/pr_lane.py`.

## Checks and CI

**`tools/check`** – run before every PR: `tools/check`. It changes nothing and prints each step before it runs
it (the steps are in the script). Each line ends as one of three results:
- **ok** – the step passed.
- **to look at** (`LOOK`) – a reminder, not a failure (e.g. you are on `main`, or `origin/main` is missing). Read
  it and decide.
- **must fix** (`FAIL`) – a hard failure (private file, token-like string, ruff or pytest). The script exits
  with code 1. Open the PR only when it ends `0 must fix`.

Read by: people and agents (rule 7: done means a command passed). Change: by PR; keep its private-path patterns
in step with `tools/check_tracked.py` and `.gitignore`.

**`tools/pr_lane.py`** – decides a PR's lane (fast / standard / two-views / quick) from its changed files and labels,
then checks what that lane needs: title, description blocks, `Closes #n`, review markers. Why: small PRs stay
fast, risky ones get a second look, and nobody decides the lane by hand. Read by: CI (`pr / blocks-filled`,
`review-gate`), `tests/test_pr_lane.py`; you can run it by hand (usage in its docstring). The lane rules for
people: `CONTRIBUTING.md`, section 4. Change: by PR, with tests, and update section 4 in the same PR.

**`tools/check_tracked.py`** – the private-file check as a separate script; with `--scan` it also searches every
tracked file for token-like strings. Why: CI `guard` runs it on every push, so a leak is caught even if
`tools/check` was skipped. Run locally: `git ls-files -z | python3 tools/check_tracked.py --scan`.

**`tools/labels.sh`** – creates the labels from `CONTRIBUTING.md`, section 5, in one step. Needs `gh` (the
GitHub command line tool) logged in with write access. Safe to run again (`--force`). Change: together with the
label table in `CONTRIBUTING.md`.

**`.github/workflows/`** – the CI jobs. When one is red, `CONTRIBUTING.md`, section 8 says what to run locally.
- `guard.yml` – no private path or token-like string is tracked. Red: remove the file from git
  (`git rm --cached <file>`); if it was a key, rotate the key – it is in the git history now.
- `pr.yml` – `lint-test`: format, lint and tests with the exact versions from `uv.lock`. `blocks-filled`: title
  and required blocks for the PR's lane (`tools/pr_lane.py blocks`). Red: the log names the problem; fix the code,
  or edit the PR title or description (editing re-runs the job).
- `review-gate.yml` – the review markers the lane needs (`tools/pr_lane.py reviews`). Red is not a code problem:
  a review is missing. It checks only that markers exist, not that a review is newer than the last push.

Change: by PR (two-views lane); a maintainer who is not the author reviews.

## GitHub templates

**`.github/pull_request_template.md`** – the text in every new PR description: blocks between markers such as
`<!-- pr-test:start -->`, each with a comment saying what goes in. Why: reviewers get the same information from
every author, an agent can fill exactly one block, CI checks the blocks. Change: by PR; if you rename a block,
change `ALL_BLOCKS` in `tools/pr_lane.py` too.

**`.github/ISSUE_TEMPLATE/`** – the new-issue page. `task.yml`: the "Task" form (goal, done-when command, files,
owner, risk). `norma-finding.yml`: one Norma finding the team must decide on. `config.yml`: no blank issues, plus
a link to `CONTRIBUTING.md`. Why: every issue has a goal and a done-when command an agent can work from. Read by:
GitHub, people, agents. Change: by PR.

## Agent config

**`.mcp.json`** – tells coding agents which MCP servers this project uses. MCP (Model Context Protocol) is a
standard way to give a coding agent extra tools from a server. Here one server, `norma`, whose tools check code
against the Norma rules while the agent works (`CONTRIBUTING.md`, section 6). No key in the file: each person
signs in to Norma through OAuth (a browser login with GitHub) the first time their agent uses it, after joining
the team workspace at [norma.qualityclouds.com](https://norma.qualityclouds.com). Read by: Claude Code (it asks
once before using a project server). Other agents have their own config file – see
[Quality Clouds' setup page](https://github.com/qualityclouds/ai-summit-barcelona-2026/blob/main/examples/mcp-config.md).
Change: by PR. JSON has no comments, so the explanation lives here.

**`.claude/settings.json`** – Claude Code permissions (JSON, no comments):
- deny `Read(./.env)`, `Read(./.env.*)` – Claude Code may not read your keys, so they cannot reach a prompt or a
  log. This also blocks `.env.example`, which holds no secrets.
- deny `Bash(git push --force*)`, `Bash(git push -f*)` – no force-push, which would overwrite others' commits.
- deny `Bash(gh pr merge*)` – agents never merge (`AGENTS.md`, rule 4).
- ask `Bash(git push*)` – any other push needs a person's yes.

Why: text rules can be ignored; deny rules are enforced by Claude Code
([best practices](https://code.claude.com/docs/en/best-practices)). Other agents do not read this file; for them
`AGENTS.md` applies. Change: by PR; a maintainer who is not the author reviews.

**`.claude/skills/check-and-fix/SKILL.md`** – a Claude Code "skill" (instructions the agent loads when needed)
that runs the Norma loop: `live_check` each changed file → fix → re-check → record. Why: makes `AGENTS.md` rule 5
a routine. Change: **do not edit** – Quality Clouds' text (MIT), copied unchanged; our additions go into
`CONTRIBUTING.md`.

## Other files

**`.gitignore`** – paths git must never pick up: keys, event data (`data/`, `out/`, `results/`, `*.labels.*`),
caches, `.venv/`. Why: `AGENTS.md`, rule 1. Change: by PR; a new private folder also goes into the patterns in
`tools/check` and `tools/check_tracked.py`. `.pytest_cache/` and `.ruff_cache/` are not listed because pytest and
ruff put their own `.gitignore` inside them.

## Generated or private – do not edit by hand

| Path | Made by | Tracked? |
|---|---|---|
| `uv.lock` | `uv add`, `uv remove`, `uv lock` | yes – commit it, never edit it |
| `.venv/` | `uv sync` | no |
| `.pytest_cache/`, `.ruff_cache/`, `__pycache__/` | pytest, ruff, Python | no |
| `.env` | you, from `.env.example` | no – never |
| `data/`, `out/`, `results/` | event material, cache (`out/cache/`), our results | no – never |
