<!-- About 3 minutes. See CONTRIBUTING.md, section 3.
Each block sits between two markers. Keep the markers: a person or an agent can then fill or replace exactly one block.
Write only what the diff and the checks cannot show: no list of changed files, no test counts.
If a block does not apply, delete its text and keep its markers.
CI (pr / blocks-filled) fails while pr-summary, pr-issue, pr-test, pr-norma or pr-ai is empty or still contains "…". -->

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
Good: `uv run python -m taste https://acme-crm.example` → verdict with 3 reasons, each with a URL -->
- `…` → …
<!-- pr-test:end -->

<!-- pr-norma:start -->
<!-- From the Norma check on this branch (live_check while working, GitHub App comment on this PR).
One line per finding: rule ID, severity, file:line, what you did.
Accepted = left on purpose, with the reason a judge should believe. Conflict = your code and another author's code disagree or repeat a mistake.
Every line here also goes into DECISIONS.md before the merge. Write "no findings" only if the Norma check shows none. -->
- fixed: …
- accepted, because: …
- conflict with: …
- live_check ran: yes (model: …) / no, because …
- DECISIONS.md rows added: yes / no
<!-- pr-norma:end -->

<!-- pr-ai:start -->
<!-- Who wrote it with which agent and model. Keep "I ran" (command + what you saw) apart from "I only read".
Name every assumption and what it rests on (code read, page fetched, told by a teammate). -->
Written by … with … .
- Assumptions: …
- I ran: …
- I only read / did not test: …
<!-- pr-ai:end -->

<!-- pr-review:start -->
<!-- Who does the two reviews (CONTRIBUTING.md, section 4). Neither is the session that wrote this code.
View A: a person (@handle). View B: a person or "separate <agent> session, posted by @handle".
Set the label second-opinion if this PR touches fetched text, keys, shell or network. -->
- A – correctness/security: …
- B – consistency/Norma: …
<!-- pr-review:end -->

<!-- pr-open:start -->
<!-- Only if it applies, else delete the text: what this PR does not solve, or what you found on the way.
Each point that is work gets an issue: "#n". -->
<!-- pr-open:end -->
