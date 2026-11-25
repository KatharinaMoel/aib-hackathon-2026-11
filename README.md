# Agents with Taste – team repo

<!-- Start page for people, coding agents and judges: the task, what we know, how to run.
What every other file is for: docs/FILES.md. -->

Our team repo for the [AI Agents Berlin hackathon](https://aiagentsberlin.xyz/agentic-hackathon), Fri 27 Nov 2026,
14:00–21:00, The Delta Campus. Main task: the Stackgini challenge "Agents with Taste"
([brief, 3 pages](https://aiagentsberlin.xyz/ah3-brief-stackgini-agents-with-taste.pdf)). Side challenge on the same
code: Norma by Quality Clouds ([brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf)).

> **Status 25 Nov:** everything below comes from the public briefs. Details follow: Stackgini sends labelled
> examples and a scoring script to registered builders (the brief says "on Nov 23"; not received by us yet).
> When they arrive, we update "What we don't know yet".

**New here? 5 minutes:**
0. `docs/INTRO.md`: how this repo came about, what is decided, and a one-page cheat sheet.
1. This README up to "Good and bad reasons" (2 min).
2. `docs/TEAM.md`: agreement and timebox (1 min).
3. `AGENTS.md`: rules 1–13 (2 min). `CONTRIBUTING.md`: how a change gets merged.
4. `docs/FILES.md` when you ask "what is this file for?": one entry per file.

## Repo map

```text
README.md            – the task, what we know, how evidence is weighed, how to run (this file)
AGENTS.md            – rules 1–13 for people and agents, house rules for code, commands, output contract
CLAUDE.md            – one line that makes Claude Code load AGENTS.md
CONTRIBUTING.md      – how a change gets merged: claim rule, PR blocks, lanes, reviews, labels, Norma loop
DECISIONS.md         – log of decisions and Norma findings (filled from pr-norma blocks at 17:30)
DEFENCE.md           – Norma submission: fixed / accepted / conflict, written at 18:15
CODEOWNERS           – who reviews changes to rules, agent config and CI
docs/TEAM.md         – agreement, roles, timebox for the day, submission checklist
docs/SIGNALS.md      – signals the agent can check, free sources, pitfalls, rules for the judge
docs/STARTER_ISSUES.md – ten first tasks to claim, and the order they merge in
docs/INTRO.md        – how the repo came about, principles, what is decided, cheat sheet
docs/RESEARCH.md     – what research says about spotting fake sites: 11 rules with sources
docs/research/       – the four full literature reviews behind RESEARCH.md
docs/PROPOSALS.md    – optional practices; only what the team picks becomes a rule
docs/FILES.md        – what every file is for, who reads it, how to change it
src/                 – the agent: fetch → judge → verify (built on the day)
eval/README.md       – eval protocol: hold-out split, the two error counts
schema/verdict.schema.json – draft output contract for one verdict
tests/               – pytest, no network; fixtures/ holds hand-written pages of made-up products
tools/check          – run before every PR; must end "0 must fix"
tools/pr_lane.py     – decides a PR's lane and what it needs; used by CI
tools/check_tracked.py – private-file and token check, used by CI
tools/labels.sh      – creates the four labels once (incl. `hotfix`)
pyproject.toml, uv.lock, .python-version – dependencies, exact versions, Python 3.12
.env.example         – names of the keys; copy to .env (never committed)
.gitignore           – keys, event data and caches git must never pick up
.mcp.json            – connects coding agents to the Norma MCP server
.claude/             – Claude Code permissions and the Norma check-and-fix skill
.github/             – PR template, issue forms, CI workflows (guard, pr, review-gate)
```

Details per file: `docs/FILES.md`.

## The task in one paragraph

We build an agent that gets the website of a software product and returns a verdict a buyer can act on: **is the
product real and alive, and would you trust the company behind it with your data and money?** Every reason comes
with a link a person can open and check. The hard part: a polished website is now free to make, and an old-looking
site can belong to a solid vendor. "An agent that believes everything fails. So does an agent that doubts
everything." (brief, p. 1)

## What we know (from the brief)

| Topic | What the brief says | Page |
|---|---|---|
| Input | the website of a software product the agent has never seen | 2 |
| Output | a verdict + reasons; every reason points to a page, a record or an archived snapshot | 2 |
| Done | (1) unseen product → verdict with reasons; (2) every reason checkable; (3) flags hollow products without trashing solid ones | 2 |
| Material | labelled examples (real products, Stackgini's call + reasons) and a small script that compares our calls with theirs | 2 |
| 19:00 | every team gets the same few new products | 2 |
| 19:45 | submissions close: a file with our agent's verdicts, next to the standard AIB submission | 2 |
| Judging | **calls count most**. If we disagree with Stackgini and our reasons hold up, the call counts; finding something they missed gives a bonus. Then: evidence – each source must say what the agent claims | 2–3 |
| Final | top 3 teams run one more product live, picked on the spot | 3 |
| Rules | no researching the live products by hand; don't hammer vendor sites; don't contact vendors; keep the data inside the event; team of max. 5 | 3 |
| Judge | David Mente, CTO and co-founder of Stackgini; Stackgini team onsite until 19:45 | 3 |

Signals the brief names (p. 2) – a starting point, not a checklist:

| Kind | Examples from the brief |
|---|---|
| Looks | design age, copyright year, dead links, a help center that goes nowhere, screenshots that don't match the product |
| Substance | claims that check out in docs or a partner marketplace, customers who confirm, a company register entry, a team with a track record |
| Risk | breaches, lawsuits, an acquisition that froze the product, what the founders did before |

What still means something, according to the brief (p. 1): signals that take time or need someone else –
customers who name the vendor on their own sites, a domain older than last month, a team with a history, a press
report the vendor didn't write.

## What we don't know yet

- The exact verdict values (e.g. `solid` / `hollow` / something in between?). `schema/verdict.schema.json` is a
  draft until we see the labelled examples.
- The format of the verdict file for 19:45 and of the labelled examples.
- How many live products there are, and how the scoring script counts.
- Whether Tavily keys, Nebius compute and n8n licences come by email or onsite ("the other partners bring search,
  compute and n8n", p. 2).

Ask Stackgini at the kickoff (14:00) if the material has not arrived by then.

## Our goal

1. **Both sides right.** On the labelled set, count two numbers: hollow products we called solid, and solid
   products we called hollow. ("Solid" and "hollow" are the brief's words; our draft schema uses `trust` /
   `caution` / `hollow` / `unclear` until we see Stackgini's labels.) We try to bring both down, not only one.
2. **No reason without a source we fetched.** A reason counts only if our pipeline fetched the URL and the quoted
   text is on that page (`AGENTS.md`, rule 2). Better three checked reasons than ten guesses.
3. **Say when we are unsure.** If the evidence is thin, the verdict says so and names what is missing. (Our
   proposal; whether the format allows an "unsure" value: not known yet.)
4. **Runs on a new product in minutes**, without a person looking anything up.

## How evidence is weighed

1. Independent sources (company register, customers' own sites, press the vendor didn't write, web archive) –
   count as evidence.
2. The vendor's own site – counts only for how the site looks (copyright year, dead links), not for claims about
   customers or features.
3. Search snippets and model knowledge – never count as evidence. They may suggest where to look.

## Good and bad reasons

The products below are **made up** (`.example` domains). They show the form, not real companies.

| | Reason | Why |
|---|---|---|
| Bad | "The company seems trustworthy and well established." | no source, no fact, nothing to check |
| Bad | "Used by Siemens and BMW." – link: `acme-crm.example/customers` | the vendor's own claim; says nothing about whether the customers agree |
| Good | "A customer names the product on its own site: 'We run our field service on Acme CRM since 2019.'" – link: `bigcustomer.example/case-study` | independent source, the quote is on the page |
| Good | "The help center links to 14 articles; 9 return 404 (checked 27 Nov, 16:10)." – link: `acme-crm.example/help` | a looks signal we measured, with the time of the check |
| Good | "The domain was first archived in March 2025, the site says 'since 2008'." – link: `web.archive.org/web/2025*/acme-crm.example` | a claim tested against an outside record |
| Bad | "Hollow: the website looks old." | old-looking is not the same as dead; the brief warns about this case |

A good verdict in short: the call, 3–5 reasons like the good rows above, and one line on what we could not
check. More examples go into `docs/VERDICTS.md` once we have the labelled set. Which signals we can check, and the
free sources we tested: `docs/SIGNALS.md`.

## How Stackgini and Norma fit together

- **Stackgini** is *what* we build: the agent and its verdicts. Judged on the calls and the evidence.
- **Norma** is *how* we build it: every author – person or coding agent – works under the same quality rules,
  checked by Norma through MCP and a GitHub App on each pull request. It wants at least two merged PRs from
  different authors, at least one fixed finding, and `DEFENCE.md` (fixed / accepted with a reason / conflict).
  Most points go to consistency across authors and to trade-offs we accepted with a reason (Norma brief).
- Same repo, same PRs: Norma costs us little extra if we work through small PRs anyway. See `CONTRIBUTING.md`.

## Run

```bash
git clone git@github.com:KatharinaMoel/aib-hackathon-2026-11.git && cd aib-hackathon-2026-11
uv sync                # needs uv: https://docs.astral.sh/uv/getting-started/installation/
cp .env.example .env   # add your keys
tools/check            # must end with "0 must fix"
uv run --env-file .env <run command> https://acme-crm.example   # set by 15:30, see AGENTS.md "Stack and commands"
```

## For the submission (fill in at 18:15)

- **Sample verdict:** <one verdict with two reasons and their links>
- **Result on the labelled set:** <the two numbers from "Our goal" – no data from the set itself>
- **Team, agents:** <names and which coding agent each used> · Norma workspace `<team name>` · `DEFENCE.md`
- **Limits:** <what it cannot do yet>
