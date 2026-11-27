# Intro – how this repo came about, and a cheat sheet

<!-- For the 15:00 intro and for anyone who joins later: what was prepared before the day, on what basis,
what is decided and what we decide together. The last section is a one-page cheat sheet. See docs/FILES.md. -->

Katharina (repo owner) prepared this repo on 25 Nov 2026 with Claude Code and several review agents. **No agent
code exists yet** – that is built together on the day. What exists is the ground we build on: the task, the
rules and the checks.

**27 Nov: we switched from Stackgini to the idealo challenge.** The Stackgini material (task, signals,
research, starter issues, verdict schema) was removed; it stays in the git history (`git show c25c4bf:<path>`).
The rules, checks and the Norma setup were kept – they do not depend on the challenge.

## 1. Principles behind it

1. **Every claim can be checked.** A number needs the MCP call that produced it; model knowledge is never
   data. The same goes for our docs: facts from outside have a link, guesses say "not verified".
2. **Same rules for every author – person or agent.** One rule file (`AGENTS.md`) that every coding agent
   reads; the same checks locally (`tools/check`) and in CI. That is also what the Norma track scores.
3. **Fast where it is safe, careful where it matters.** Docs-only PRs go through the fast lane; code needs a
   review by a person; rules, CI and risky code get a second view (`CONTRIBUTING.md`, section 4).
4. **Explainable for a junior developer.** Every file says what it is for (`docs/FILES.md`, repo map in the
   README).
5. **Keep it simple.** First one working version end to end, then only changes that raise the score.

## 2. How it was built (25 Nov)

| Step | What was done | Result in the repo |
|---|---|---|
| Read the briefs | all four public challenge briefs (Stackgini, Norma, idealo, Affinidi) | `README.md` (task, what we know, what we don't) |
| Choose the challenge | first Stackgini; on 27 Nov switched to idealo. Norma stacks on top ("any project you submit with a GitHub link can enter", Norma brief p. 1) | `README.md`, "How idealo and Norma fit together" |
| Expert reviews (agents) | senior/OSS developer, project manager, eval engineer, hackathon juror, security; later Python maintainer, GitHub admin, Norma analyst, technical writer | `AGENTS.md`, `CONTRIBUTING.md`, PR template, CI, `docs/FILES.md` |
| Compare with 6 open-source agent repos | OpenHands, crewAI, smolagents, browser-use, gpt-researcher, deer-flow – what their contribution rules, agent files and evals do | claim rule, accountability line in PRs, rules 11–13 |
| Stress test under time pressure | the day simulated in 15-minute steps with 4 people | lanes incl. `quick`, "review first while you wait", fallbacks, emergency mode |

## 3. What is prepared, what we decide together at the start

**Prepared – a proposal, change any of it:** uv + ruff + pytest; CI checks (`guard`, `pr`, `review-gate`);
PR template in blocks; issue forms; 4 labels; lanes; house rules that mirror Norma rule IDs; Norma MCP config
and check-and-fix skill.

**We decide together at the start:**
- what we keep, change or drop from this proposal – after everyone has read the task details;
- **the idea** – what we build with the idealo MCP;
- who is caller, data, domain logic, demo + eval, Norma/video (`docs/TEAM.md`, roles), and 2–3 maintainers;
- package name, run command and the first issues (once the idea is picked);
- the model, if the idea needs one;
- which proposals from `docs/PROPOSALS.md` we keep.

**Still open:** how our code gets an idealo token (see `README.md`, "What is still open").

## 4. Cheat sheet

**Setup (once):** `uv sync` · `cp .env.example .env` (add keys) · `tools/check` → `0 must fix`

**Every task:**

| Step | Command / action |
|---|---|
| Claim | assign yourself the issue; max. 1 issue in progress + 1 PR waiting |
| Branch | `git switch -c <name>/<topic>` |
| Run | `uv run --env-file .env <command>` |
| Check | `tools/check` (ruff, pytest, private files, tokens) |
| PR | title `feat: …` / `fix: …` / `docs: …`; fill the blocks your lane needs |
| While waiting | review someone else's PR, then start the next issue |

**Lanes:** fast (only non-rule `.md`) → summary only · standard (code) → all blocks + review A by a person ·
two-views (label `norma`/`second-opinion`, or rules/CI/tools/schema) → + review B · quick (until the skeleton is merged,
and in emergency mode) → three blocks + review A at the table.

**Comments:** `Bug:` blocks · `Question:` answer it, does not block · `Note:` information.

**Never:** keys or event data in git or chat · agents merging · deleting code to hide a Norma finding ·
tests that call an LLM or the network.

**Checkpoints** (`docs/TEAM.md`): 16:00 walking skeleton merged · 16:15 two code PRs from different authors ·
17:30 Norma sweep 1 + video script · 18:15 DEFENCE + emergency mode · 18:30 demo rehearsal · 18:45 freeze ·
19:40 submission sent · 20:00 pitch.

**Where to look:** task → `README.md` · rules → `AGENTS.md` · how to merge → `CONTRIBUTING.md` · plan →
`docs/TEAM.md` · any file → `docs/FILES.md`.
