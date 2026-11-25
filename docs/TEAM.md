# Team

<!-- For the people on the team: how we decide, who owns what, the plan for the day, what we hand in.
See docs/FILES.md for the other files. -->

## Agreement (2 minutes – this worked for me, change anything)

1. One person, the "caller", decides what we build and what we cut. After 5 minutes of disagreement, the caller
   decides.
2. A working version end to end by 16:15; ugly is fine. After that, only changes that raise the eval score.
3. Small PRs, one topic each; one issue in progress and one PR waiting per person – while it waits, review. Someone else merges when every check
   is green – incl. the review for the PR's lane (`CONTRIBUTING.md`, section 4). Only a `Bug:` blocks.
4. No reason without a fetched link. Data and keys stay out of git and chat.
5. Freeze at 18:45. After that, only fixes for crashes.

## Roles (3–5 people)

| Role | Owns |
|---|---|
| Caller | what we build and cut, tie-breaks |
| Pipeline | fetching pages (rate limit, page limit, cache), evidence |
| Judgement | prompt, verdict logic, output file |
| Eval + blind run | eval script, score after each change, hold-out set, the 19:00 run; plus a backup who can run it from a fresh clone |
| Norma + video | Norma setup, `DECISIONS.md` → `DEFENCE.md`, video of at most 2 minutes |

## Timebox

| Time | What | Checkpoint |
|---|---|---|
| before 15:00 | Owner: invite everyone's GitHub handle, install the Norma GitHub App. Everyone: accept the invite, `uv sync`, `tools/check`, sign in to Norma | everyone can clone and `tools/check` says `0 must fix` |
| 15:00–15:10 | Intros: tool, strength, what each of us wants to learn; team channel named | caller named |
| 15:10–15:30 | Agreement, roles, picks from `docs/PROPOSALS.md`, commands in `AGENTS.md`, output format; Norma MCP, link the repo in the Norma workspace, compare `get_rulesets` with the house rules in `AGENTS.md`, **first Norma check → `baseline` row in `DECISIONS.md`**; each person claims one starter issue (`docs/STARTER_ISSUES.md`) | Norma not working by 15:45 → caller keeps or drops it |
| 15:30–16:15 | First working version: one site → verdict → eval; **≥ 2 small PRs from different authors merged** (Norma entry condition) | 16:15: 5-minute sync; not running → everyone helps |
| 16:15–17:30 | Improve in parallel, post the score every 30 min; first Norma finding fixed by 17:00 | 17:00: drop any signal that does not raise the score; 17:30: 5-minute sync |
| 17:30–18:15 | Sweep 1: Norma owner copies the `pr-norma` blocks into `DECISIONS.md` (one PR). With 4 people, the caller takes Norma and video from now | 18:15: write `DEFENCE.md` from `DECISIONS.md`; sweep 2 (PRs merged after 17:30) inside the `DEFENCE.md` PR |
| 18:15–18:45 | Full run on the hold-out set; timeout → verdict `unclear`; record the video | freeze 18:45 |
| 18:45–19:00 | Backup runs it from a fresh clone | |
| 19:00–19:30 | Blind run – no manual research (brief, page 3); at most one rerun | |
| 19:30–19:45 | Submit; verdict file sent by 19:40 | |

## Fallbacks

- **No labelled set by 15:45:** the caller writes a list of 8 well-known products (none of the live ones) with
  the call we expect, in `data/fallback.txt`. "Raises the score" then means: no new mistake on that list.
- **Norma down or not set up by 15:45:** the caller decides to drop it. PRs write `live_check ran: no, because
  Norma down`; the label `norma` is not used.

## Emergency mode

**Starts at 18:15**, or when end to end still does not run at 17:30, or on any crash during the blind run.
The caller says it out loud.

- Only `fix:` PRs for crashes, timeouts or the output format, with label `hotfix`.
- Required blocks: `pr-summary`, `pr-test`, `pr-norma` (honest, e.g. "live_check ran: no, because hotfix at
  19:12"). `pr-ai` may be one line.
- View A may be given at the table and recorded as one review:
  `<!-- review:correctness -->` / `Review A by @x (person, at the table, 19:12): ran <cmd> → ok`. No view B.
- `lint-test` must still be green. Never remove code to make a finding go away.
- The blind run may run from the fix branch; the PR merges afterwards. Hotfix rows go into the sweep-2.

## Submission checklist

- [ ] Verdict file for the blind cases (Stackgini) + the standard AIB submission (link: given at kickoff; not
      published yet)
- [ ] GitHub link: ≥ 2 merged PRs from different authors, checked by the Norma GitHub App
- [ ] `DEFENCE.md`: fixed / accepted / conflict, each with rule, file, reason
- [ ] Video, at most 2 minutes, at least 30 seconds on the conflict between authors
- [ ] Norma workspace named after the team
- [ ] Afterwards: remove collaborators or keep the repo private, uninstall the Norma app, rotate keys

Sources: [Stackgini brief](https://aiagentsberlin.xyz/ah3-brief-stackgini-agents-with-taste.pdf),
[Norma brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf).
