<!-- About 3 minutes. See CONTRIBUTING.md, section 3.
Each block sits between two markers. Keep the markers: a person or an agent can then fill or replace exactly one block.
Write only what the diff and the checks cannot show: no list of changed files, no test counts.
If a block does not apply, delete its text and keep its markers.
Title: "<type>: <summary>", type feat/fix/docs/test/chore/refactor (it becomes the commit on main).
FAST LANE – only Markdown files, none of them AGENTS.md, CONTRIBUTING.md or CLAUDE.md: fill pr-summary only, delete the rest.
Every other PR: CI (pr / blocks-filled) fails while pr-summary, pr-issue, pr-test, pr-norma or pr-ai is empty or still contains "…".
Lanes and reviews: CONTRIBUTING.md, section 4. -->

<!-- pr-summary:start -->
<!-- One sentence: what works after this PR that did not work before. No file names. -->
…
<!-- pr-summary:end -->

<!-- pr-issue:start -->
<!-- "Closes #n" for the task issue; GitHub closes it on merge. A second issue goes on its own line. -->
Closes #…
<!-- pr-issue:end -->

<!-- pr-test:start -->
<!-- One command per line and what the reviewer should see. It must work from a fresh clone after `uv sync` and with .env set.
Good: `uv run pytest tests/test_verify.py` → 4 passed
Good: `uv run --env-file .env python -m <pkg> https://acme-crm.example` → verdict with 3 reasons, each with a URL -->
- `…` → …
<!-- pr-test:end -->

<!-- pr-norma:start -->
<!-- From the Norma check on this branch (live_check while working, GitHub App comment on this PR).
One line per finding: rule ID, severity, file:line, what you did.
Accepted = left on purpose, with the reason a judge should believe. Conflict = your code and another author's code disagree or repeat a mistake.
The Norma owner copies these lines into DECISIONS.md at 17:30 – so write them complete. Write "no findings" only if the Norma check shows none.
If this PR fixes, accepts or causes a finding, set the label norma (adds review view B). -->
- fixed: …
- accepted, because: …
- conflict with: …
- live_check ran: yes (model: …) / no, because …
<!-- pr-norma:end -->

<!-- pr-ai:start -->
<!-- Who wrote it with which agent and model. Keep "I ran" (command + what you saw) apart from "I only read".
Name every assumption and what it rests on (code read, page fetched, told by a teammate). -->
Written by … with … .
- [ ] A person read the whole diff and can explain why it is correct.
- Assumptions: …
- I ran: …
- I only read / did not test: …
<!-- pr-ai:end -->

<!-- pr-review:start -->
<!-- Who reviews (CONTRIBUTING.md, section 4). Standard lane: view A only. Two-views lane (label norma or second-opinion,
or rules, CI, agent config, tools/, schema/ changed): A and B. Neither is the session that wrote this code.
View A: a person who is not the author (@handle). View B: a person or "separate <agent> session, posted by @handle".
Set the label second-opinion if this PR touches fetched text, keys, shell or network. -->
- A – correctness/security: …
- B – consistency/Norma (only two-views lane): …
<!-- pr-review:end -->

<!-- pr-open:start -->
<!-- Only if it applies, else delete the text: what this PR does not solve, or what you found on the way.
Each point that is work gets an issue: "#n". -->
<!-- pr-open:end -->
