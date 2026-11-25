# Decisions log

Add one line per decision or Norma finding, at the latest when the PR merges. Do not rewrite old lines.
At 18:15 we write `DEFENCE.md` from this log.

Kinds: `baseline` (first check: score and open findings) · `fixed` · `accepted` (we leave it, with a reason) · `conflict` (two authors or agents clashed) ·
`candidate` (seen, not decided yet).
"Check before → after": the Norma result for this rule before and after the change.

| time | kind | rule ID | severity | file:line | authors (person + agent) | PR | what | reason | check before → after |
|---|---|---|---|---|---|---|---|---|---|
| 15:25 | baseline | – | – | – | – | – | first Norma check on `main` | starting point | score …, … open findings |
| 16:40 | fixed | *example:* `py-maint-broad-except` | HIGH | `src/fetch.py:31` | Kat + Claude Code | #4 | catch only `httpx.TimeoutException` | a broad except hid a 403 as "site dead" | 1 finding → 0 |
