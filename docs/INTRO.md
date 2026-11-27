# Intro – the 10-minute walk-through, and a cheat sheet

<!-- For the team intro and for anyone who joins later: the task, how we work, the plan until 20:00.
It follows the slides used in the intro. See docs/FILES.md. -->

Katharina prepared this repo on 25 Nov 2026 with Claude Code and several review agents. On 27 Nov the team
switched from the Stackgini challenge to the **idealo challenge**. The Stackgini material is gone from the tree
and stays in the git history (`git show c25c4bf:<path>`). The rules, the checks and the Norma setup stayed: they
do not depend on the challenge. **No product code exists yet, and the idea is still open.**

## 1. The task: idealo

"Build Something We Didn't Expect" ([idealo brief](https://aiagentsberlin.xyz/ah3-brief-idealo.pdf)): a
prototype that needs idealo's commerce data – catalogue, categories, current and historical prices,
availability, merchants, offers – to solve a real problem. Judged on four questions:

| Criterion | Question from the brief |
|---|---|
| Creativity | Does the project use the idealo MCP in an unexpected way? |
| Meaningfulness | What real problem does it solve, and for whom? |
| Use of the data | How do product, price, availability, merchant or category signals drive the result? |
| Execution | Does the working prototype make the idea and its potential tangible? |

Submit by 19:45; selected teams pitch from 20:00. MCP details: `README.md`, "The idealo MCP".

## 2. On top: Norma

From the [Norma brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf), "What your build must show":

1. Every author runs the same checks: Norma MCP in each coding agent, checks while the code is written.
2. At least 2 PRs from different authors, each checked by the Norma GitHub App (merged, for the submission).
3. At least one finding fixed; a later check shows it gone.
4. One Norma policy in the team workspace, with the rules the team agrees on.

Scoring (100): policy and consistency 30 · the trade-off we accepted 30 · findings fixed 20 · Production-Ready
Score at submission 20. **60 points depend on a short note in the submission form** – we draft it in
`DEFENCE.md`. The workspace is named after the team. An empty repo scores zero; so does deleting code to make
a finding disappear.

## 3. Our rules (`AGENTS.md`, the five that matter most today)

1. **No keys or data in git or chat.** Keys in `.env`; real idealo responses in `data/`.
2. **Every number has a source:** a logged idealo MCP call, never model knowledge.
3. **Small PRs, agents never merge.** One topic per PR; another person merges when everything is green.
4. **Norma in the loop.** `live_check` on each finished file; fix the cause; never delete code to hide a
   finding.
5. **Done means a command passed** (`tools/check` → `0 must fix`), and tests never call an LLM or the network.

## 4. From issue to merge

Issue → branch `<name>/<topic>` → build with your agent, with a test → Norma `live_check` → `tools/check` → PR
with the template's blocks → **another person approves** → a person merges (the author may). While your PR waits, review someone else's.
Details: `CONTRIBUTING.md`.

**Review lanes** (set by `tools/pr_lane.py`): fast (Markdown only) · standard (code: review A) · two-views (rules,
CI, tools, dependencies: reviews A and B) · quick (skeleton phase and emergency mode: three blocks, review A at
the table). Only a comment starting with `Bug:` blocks a merge.

**Proposal for today, to decide in the intro** (from the review on 27 Nov): with about four hours left, work in
the `quick` lane until 18:15, with one review A at the table; review B only for changes to `AGENTS.md`; no
issue required for small fixes. Note: `uv add` changes `pyproject.toml` and `uv.lock`, which always puts a PR
into the two-views lane.

## 5. Roles

Caller (decides after 5 minutes of disagreement, keeps time) · Data (idealo MCP client, logged calls, recorded
responses) · Domain logic (the rules and numbers behind the result – our finance experts, paired with one
person who codes) · Demo + eval (case list, demo, backup who can run it from a fresh clone) · Norma + submission
(workspace, policy, findings log, the note, the captain who submits) · 2–3 maintainers. Details: `docs/TEAM.md`.

## 6. The plan until 20:00

| Time | What |
|---|---|
| 15:45 | invite teammates; everyone checks in; team name |
| 15:50 | in parallel: idealo tool list · Norma workspace + everyone's MCP |
| 16:05 | idea decided (the caller decides) |
| 16:15 | PR #9 merged; old PRs closed; Norma policy created |
| 16:45 | walking skeleton merged (author A) |
| 17:00 | second code PR merged (author B); first Norma check |
| 17:45 | one finding fixed, one accepted with a reason |
| 18:15 | feature freeze; draft the Norma note and the pitch |
| 18:45 | rehearsal from a fresh clone |
| 19:15 | last Norma check; note the score |
| 19:30 | the captain submits (deadline 19:45) |
| 20:00 | pitch, if selected |

The source of these times is `docs/TEAM.md`, "Checkpoints".

**Still open:** how our code gets an idealo token (`README.md`, "What is still open"). Help onsite: Nuno Silva
at the Quality Clouds table (Norma), the idealo team (MCP).

## 7. Cheat sheet

**Setup (once):** `uv sync` · `cp .env.example .env` (add keys) · `tools/check` → `0 must fix`

**Connect your agent:** `claude mcp add --transport http idealo https://mcp.idealo.com/mcp`, then `/mcp` →
`idealo` → Authenticate, and `/mcp` → `norma` → Authenticate (with the account in the team workspace).

| Step | Command / action |
|---|---|
| Branch | `git switch -c <name>/<topic>` |
| Run | `uv run --env-file .env <command>` |
| Check | `tools/check` (ruff, pytest, private files, tokens) |
| PR | title `feat: …` / `fix: …` / `docs: …`; fill the blocks your lane needs |
| While waiting | review someone else's PR, then start the next task |

**Comments:** `Bug:` blocks · `Question:` answer it, does not block · `Note:` information.

**Never:** keys or event data in git or chat · agents merging · deleting code to hide a Norma finding ·
tests that call an LLM or the network.

**Where to look:** task → `README.md` · rules → `AGENTS.md` · how to merge → `CONTRIBUTING.md` · plan →
`docs/TEAM.md` · any file → `docs/FILES.md`.
