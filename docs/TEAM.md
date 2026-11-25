# Team

## Agreement (2 minutes – this worked for me, change anything)

1. One person, the "caller", decides what we build and what we cut. After 5 minutes of disagreement, the caller
   decides.
2. A working version end to end by 16:15; ugly is fine. After that, only changes that raise the eval score.
3. Small PRs, one topic each. Someone else merges when checks are green. Only a `Bug:` blocks.
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
| 15:00–15:10 | Intros: tool, strength, what each of us wants to learn | caller named |
| 15:10–15:30 | Agreement, roles, picks from `docs/PROPOSALS.md`, commands in `AGENTS.md`, output format, team channel; Norma GitHub App + MCP, link the repo in the Norma workspace, compare `get_rulesets` with the house rules in `AGENTS.md`, **first Norma check → `baseline` row in `DECISIONS.md`**; `tools/labels.sh` | Norma not working by 15:45 → caller keeps or drops it |
| 15:30–16:15 | First working version: one site → verdict → eval | not running → everyone helps |
| 16:15–17:30 | Improve in parallel, post the score every 30 min | 17:00: drop any signal that does not raise the score |
| 17:30–18:15 | ≥ 2 PRs from different authors merged, ≥ 1 Norma finding fixed | 18:15: write `DEFENCE.md` from `DECISIONS.md` |
| 18:15–18:45 | Full run on the hold-out set; timeout → verdict `unclear`; record the video | freeze 18:45 |
| 18:45–19:00 | Backup runs it from a fresh clone | |
| 19:00–19:30 | Blind run – no manual research (brief, page 3); at most one rerun | |
| 19:30–19:45 | Submit; verdict file sent by 19:40 | |

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
