# <project name>

<One sentence: what the agent does.>
Built at the [AI Agents Berlin hackathon](https://aiagentsberlin.xyz/agentic-hackathon), 27 Nov 2026, for the
Stackgini challenge "Agents with Taste"
([brief](https://aiagentsberlin.xyz/ah3-brief-stackgini-agents-with-taste.pdf)) and the Norma track
([brief](https://aiagentsberlin.xyz/ah3-brief-norma.pdf)).

**New here? 5 minutes:**
1. `docs/TEAM.md`: agreement and timebox (2 min).
2. `AGENTS.md`: rules 1–10 (3 min).
3. `docs/PROPOSALS.md` is optional. We pick from it at 15:10.

Team channel: `<set at 15:10>`.

## Run

```bash
git clone <repo URL> && cd <repo>
cp .env.example .env   # add your keys
<install command>
<run command> https://example-vendor.com
```

## Sample verdict

<one verdict with two reasons and their links>

## How evidence is checked

Every reason carries a URL our pipeline fetched and a quote that is on that page. Sources have three levels:
1. Independent sources (company register, customers' own sites, press, web archive) – count as evidence.
2. The vendor's own site – counts only for how the site looks (copyright year, dead links), not for claims
   about customers or features.
3. Search snippets and model knowledge – never count as evidence.

## Result on the labelled set

<two numbers: hollow products we called solid, solid products we called hollow – no data from the set>

## Team, agents, governance

<names and which coding agent each used> · Norma workspace: `<team name>` · see `DEFENCE.md` and merged PRs.

## Limits

<what it cannot do yet>
