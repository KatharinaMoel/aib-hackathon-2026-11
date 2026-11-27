# Team

<!-- How we work together on the day: a proposal the team agrees on or changes at the start. The detailed
minute plan stays with the facilitator (not in the repo); here are only the points other files refer to.
See docs/FILES.md. -->

## Agreement (a proposal – change anything at the start)

1. One person, the "caller", decides what we build and what we cut after 5 minutes of disagreement. Anyone can
   be the caller; we pick one at the start.
2. First a walking skeleton end to end (the first issue once the idea is picked), ugly is fine. After that, only changes that raise
   the eval score.
3. Small PRs, one topic each; one issue in progress and one PR waiting per person – while it waits, review.
   Someone else merges when every check is green, incl. the review for the PR's lane (`CONTRIBUTING.md`,
   section 4). Only a `Bug:` blocks.
4. No reason without a fetched link. Data and keys stay out of git and chat.
5. Every idea is welcome. If it does not fit now, it goes on the parking list (a GitHub issue with label
   `task`), not lost.

## Roles (3–5 people, a suggestion)

| Role | Owns |
|---|---|
| Caller | what we build and cut, tie-breaks, time |
| Data | the idealo MCP client (login, rate limit, cache, logged calls), recorded responses for tests |
| Domain logic | the rules and numbers the result rests on (e.g. our finance experts, paired with one coder); prompt if any |
| Demo + eval | the case list, score after each change, the demo; plus a backup who can run it from a fresh clone |
| Norma + video | Norma setup, `DECISIONS.md` → `DEFENCE.md`, video script and recording (at most 2 minutes) |

## Checkpoints (other files refer to these)

| Time | Checkpoint |
|---|---|
| 16:00 | walking skeleton merged; the skeleton phase (label `quick`) ends |
| after the first code PR | first Norma check → `baseline` row in `DECISIONS.md` (on real code, so real findings exist) |
| 16:15 | ≥ 2 code PRs from different authors merged (Norma entry condition) |
| 17:00 | drop any signal that does not raise the score |
| 17:30 | Norma sweep 1 (`pr-norma` blocks → `DECISIONS.md`); video script written |
| 18:15 | `DEFENCE.md` + sweep 2; emergency mode starts |
| 18:30 | demo rehearsal: one run end to end from a fresh clone, as in the pitch |
| 18:45 | freeze |
| 19:40 | submission sent (deadline 19:45, event) |
| 20:00 | selected teams pitch live (event) |

## Fallbacks

- **No idealo login by 15:30:** record MCP responses through any teammate's working login into `data/`
  (git-ignored) and build on those; ask the idealo team onsite. "Raises the score" then means: no new mistake on
  our case list.
- **Norma down or not set up by 15:45:** the caller decides to drop it. PRs write `live_check ran: no, because
  Norma down`; the label `norma` is not used.

## Skeleton phase and emergency mode (label `quick`)

**Skeleton phase:** from the start until #1 is merged. **Emergency mode:** from 18:15, or when end to end
still does not run at 17:30, or on any crash during the demo rehearsal. The caller says it out loud.

- PRs with label `quick`; in emergency mode only `fix:` PRs for crashes, timeouts or the output format.
- Required blocks: `pr-summary`, `pr-test`, `pr-norma` (honest, e.g. "live_check ran: no, because quick fix at
  19:12"). `pr-ai` may be one line.
- View A may be given at the table and recorded as one review:
  `<!-- review:correctness -->` / `Review A by @x (person, at the table, 19:12): ran <cmd> → ok`. No view B.
- `lint-test` must still be green. Never remove code to make a finding go away.
- In emergency mode the demo may run from the fix branch; the PR merges afterwards. Its findings go into
  sweep 2.

## Submission checklist

- [ ] The standard AIB submission (link: given at kickoff; not published yet), with the notes from
      `README.md`, "For the submission"
- [ ] Pitch ready for 20:00 (if selected): problem, who it helps, how the idealo data drives it, live demo
- [ ] GitHub link: ≥ 2 merged PRs from different authors, checked by the Norma GitHub App
- [ ] `DEFENCE.md`: fixed / accepted / conflict, each with rule, file, reason
- [ ] Video, at most 2 minutes, at least 30 seconds on the conflict between authors
- [ ] Norma workspace named after the team
- [ ] Afterwards: remove collaborators or keep the repo private, uninstall the Norma app, rotate keys

Sources: [idealo brief](https://aiagentsberlin.xyz/ah3-brief-idealo.pdf),
[Norma brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf).
