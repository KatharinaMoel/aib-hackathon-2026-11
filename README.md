# idealo challenge – team repo

<!-- Start page for people, coding agents and judges: the task, what we know, how to run.
What every other file is for: docs/FILES.md. -->

Our team repo for the [AI Agents Berlin hackathon](https://aiagentsberlin.xyz/agentic-hackathon), Fri 27 Nov 2026,
14:00–21:00, The Delta Campus. Main task: the idealo challenge "Build Something We Didn't Expect"
([brief, 1 page](https://aiagentsberlin.xyz/ah3-brief-idealo.pdf)). Side challenge on the same code: Norma by
Quality Clouds ([brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf)).

> **Status 27 Nov:** we switched from the Stackgini challenge to idealo. The Stackgini material is in the git
> history (`git show c25c4bf:<path>`). **The idea is still open** – the team decides it together.

**New here? Read only `docs/INTRO.md`** (5 minutes): how this repo came about, what is decided, and a one-page
cheat sheet. Everything else is reference – open it when you need it:
1. This README up to "What is still open" (2 min).
2. `docs/TEAM.md`: agreement, roles, checkpoints.
3. `AGENTS.md`: rules 1–13 (2 min). `CONTRIBUTING.md`: how a change gets merged.
4. `docs/FILES.md` when you ask "what is this file for?": one entry per file.

## Repo map

```text
README.md            – the task, what we know, how to run (this file)
AGENTS.md            – rules 1–13 for people and agents, house rules for code, commands
CLAUDE.md            – one line that makes Claude Code load AGENTS.md
CONTRIBUTING.md      – how a change gets merged: claim rule, PR blocks, lanes, reviews, labels, Norma loop
DECISIONS.md         – log of decisions and Norma findings (filled from pr-norma blocks at 17:30)
DEFENCE.md           – Norma submission: fixed / accepted / conflict, written at 18:15
docs/TEAM.md         – agreement, roles, checkpoints, fallbacks, emergency mode, submission checklist
docs/INTRO.md        – how the repo came about, principles, what is decided, cheat sheet
docs/PROPOSALS.md    – optional practices; only what the team picks becomes a rule
docs/FILES.md        – what every file is for, who reads it, how to change it
src/                 – the prototype (built on the day, once the idea is picked)
eval/README.md       – how we check the prototype on a fixed case list
tests/               – pytest, no network; fixtures/ holds recorded MCP responses of made-up products
tools/check          – run before every PR; must end "0 must fix"
tools/pr_lane.py     – decides a PR's lane and what it needs; used by CI
tools/check_tracked.py – private-file and token check, used by CI
tools/labels.sh      – creates the four labels once (incl. `quick`)
pyproject.toml, uv.lock, .python-version – dependencies, exact versions, Python 3.12
.env.example         – names of the keys; copy to .env (never committed)
.gitignore           – keys, event data and caches git must never pick up
.mcp.json            – connects coding agents to the Norma MCP server
.claude/             – Claude Code permissions and the Norma check-and-fix skill
.github/             – PR template, issue forms, CI workflows (guard, pr, review-gate)
```

Details per file: `docs/FILES.md`.

## The task in one paragraph

Build an application, agent, experience or prototype that uses idealo's commerce data to solve a real problem.
Through the idealo MCP we can work with the product catalogue, category relationships, current and historical
prices, product availability, merchants and offers. The data must be essential to what the prototype does. The
brief's examples: help someone decide whether to buy, wait, repair, rent or substitute; spot shortages from price
and availability signals; plan purchases around a budget. Ideas outside shopping are welcome if commerce data
makes them possible.

## What we know (from the brief)

| Topic | What the brief says |
|---|---|
| Award | "Most Creative Use of the idealo MCP" (€300 in vouchers, split among the winning team, per the event page) |
| Creativity | Does the project use the idealo MCP in an unexpected way? |
| Meaningfulness | What real problem does it solve, and for whom? |
| Use of the data | How do product, price, availability, merchant or category signals drive the result? |
| Execution | Does the working prototype make the idea and its potential tangible? |
| Deadline | Fri 27 Nov, 19:45, through the standard AI Agents Berlin submission |
| Pitch | selected teams pitch live from 20:00 |
| Team | up to five, at least one member on site; teams own their code |

## The idealo MCP (checked 27 Nov)

- Endpoint: `https://mcp.idealo.com/mcp` (HTTP transport). `https://mcp.idealo.com/com` answers 403.
- Login: OAuth 2 bearer token, scope `https://mcp.idealo.com/mcp/api.full-access`
  (from `https://mcp.idealo.com/.well-known/oauth-protected-resource`).
- Add it to your own Claude Code (local, not in this repo): `claude mcp add --transport http idealo
  https://mcp.idealo.com/mcp`, then `/mcp` → `idealo` → Authenticate.
- Tool names, parameters and limits: **not verified** yet – write them into `docs/IDEALO_TOOLS.md` after the
  first login.

## What is still open

- **The idea.** The team decides it at the start. It then sets the output format, the case list and the first
  issues.
- How our code gets an idealo token (OAuth from a script, or the MCP only through a coding agent). Ask idealo
  at the kickoff.
- Which model we use, if the idea needs one.

## How idealo and Norma fit together

- **idealo** is *what* we build: a prototype that uses the idealo MCP. Judged on creativity, meaning, use of the
  data and execution.
- **Norma** is *how* we build it: every author – person or coding agent – works under the same quality rules,
  checked by Norma through MCP and a GitHub App on each pull request. The brief asks for four things: Norma MCP
  in every coding agent; ≥ 2 PRs from different authors, checked by the GitHub App; ≥ 1 finding fixed; one Norma
  policy in the team workspace. Scoring: policy and consistency 30, the accepted trade-off 30, findings fixed 20,
  Production-Ready Score at submission 20. 60 points depend on a short note in the submission form; we draft
  it in `DEFENCE.md` ([Norma brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf)).
- Same repo, same PRs: Norma costs us little extra if we work through small PRs anyway. See `CONTRIBUTING.md`.

## Run

```bash
git clone git@github.com:KatharinaMoel/aib-hackathon-2026-11.git && cd aib-hackathon-2026-11
uv sync                # needs uv: https://docs.astral.sh/uv/getting-started/installation/
cp .env.example .env   # add your keys
tools/check            # must end with "0 must fix"
uv run --env-file .env <run command>   # set once the idea is picked, see AGENTS.md "Stack and commands"
```

## For the submission (fill in at 18:15)

- **Idea in one sentence:** <what it does, for whom>
- **How the idealo data drives it:** <which MCP tools, which signals>
- **Demo:** <link or command, one example run>
- **Team, agents:** <names and which coding agent each used> · Norma workspace `<team name>` · `DEFENCE.md`
- **Limits:** <what it cannot do yet>
