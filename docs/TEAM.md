# Team

<!-- How we work together on the day: a proposal the team agrees on or changes at the start. The detailed
minute plan stays with the facilitator (not in the repo); here are only the points other files refer to.
See docs/FILES.md. -->

## Agreement (a proposal – change anything at the start)

1. One person, the "caller", decides what we build and what we cut after 5 minutes of disagreement. Anyone can
   be the caller; we pick one at the start.
2. First a walking skeleton end to end, ugly is fine. After that, only changes that make the demo better.
3. Small PRs, one topic each; one issue in progress and one PR waiting per person – while it waits, review.
   Someone else merges when every check is green, incl. the review for the PR's lane (`CONTRIBUTING.md`,
   section 4). Only a `Bug:` blocks.
4. Every number comes from a logged idealo MCP call (`AGENTS.md`, rule 2). Data and keys stay out of git and
   chat.
5. Every idea is welcome. If it does not fit now, it goes on the parking list (a GitHub issue with label
   `task`), not lost.

## Roles (3–5 people, a suggestion)

| Role | Owns |
|---|---|
| Caller | what we build and cut, tie-breaks, time |
| Data | the idealo MCP client (login, rate limit, cache, logged calls), recorded responses for tests |
| Domain logic | the rules and numbers the result rests on (e.g. our finance experts, paired with one coder); prompt if any |
| Demo + eval | the case list, score after each change, the demo; plus a backup who can run it from a fresh clone |
| Norma + submission | Norma workspace and policy, findings log (`DECISIONS.md`), the note for the submission form; the captain who submits |

## Checkpoints (other files refer to these)

Proposal after the review of 27 Nov, 15:40. The idea comes before the admin steps, because idealo's creativity
criterion depends on what the MCP tools can do.

| Time | Checkpoint |
|---|---|
| 15:45 | teammates invited; everyone checked in at `/hackathons/build/checkin`; team name agreed |
| 15:50 | in parallel: idealo tool list (`docs/IDEALO_TOOLS.md`) · Norma workspace named after the team, everyone's MCP connected |
| 16:05 | idea decided (the caller decides) |
| 16:15 | PR #9 merged; old Stackgini PRs closed; Norma policy created |
| 16:45 | walking skeleton merged (author A); the skeleton phase (label `quick`) ends |
| 17:00 | second code PR merged (author B); first Norma check → `baseline` row in `DECISIONS.md` |
| 17:45 | at least one finding fixed, one accepted with a reason |
| 18:15 | feature freeze; draft the Norma note and the pitch; emergency mode starts |
| 18:45 | rehearsal: one demo run from a fresh clone, as in the pitch |
| 19:15 | last Norma check; write down the Production-Ready Score |
| 19:30 | the captain submits at `/hackathons/build/submit` (deadline 19:45) |
| 20:00 | selected teams pitch live (event) |

## Fallbacks

- **No idealo login by 16:00:** record MCP responses through any teammate's working login into `data/`
  (git-ignored) and build on those; ask the idealo team onsite.
- **Norma down or not set up by 15:45:** the caller decides to drop it. PRs write `live_check ran: no, because
  Norma down`; the label `norma` is not used.

## Skeleton phase and emergency mode (label `quick`)

**Skeleton phase:** from the start until the walking skeleton is merged. **Emergency mode:** from 18:15, or when end to end
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

Sources: event page (check-in, submit), idealo brief, Norma brief ("What to submit").

- [ ] Every builder checked in once at `/hackathons/build/checkin` (event page)
- [ ] One captain submits at `/hackathons/build/submit` by 19:45 (event page)
- [ ] GitHub link: ≥ 2 merged PRs from different authors, each checked by the Norma GitHub App
- [ ] Norma workspace name = team name; the policy lives there
- [ ] The Norma note in the submission form (a few sentences): the accepted finding with rule and file and why;
      how the policy kept authors consistent, with one clash between two authors or one agent repeating
      another's mistake. Draft it in `DEFENCE.md`.
- [ ] Pitch ready for 20:00 (if selected): problem, who it helps, how the idealo data drives it, live demo
- [ ] Afterwards: remove collaborators or keep the repo private, uninstall the Norma app, rotate keys

Sources: [idealo brief](https://aiagentsberlin.xyz/ah3-brief-idealo.pdf),
[Norma brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf).
