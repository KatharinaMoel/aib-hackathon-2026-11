# Decisions log

Add one line per decision or Norma finding, at the latest when the PR merges. Do not rewrite old lines.
At 18:15 we write `DEFENCE.md` from this log.

Kinds: `fixed` · `accepted` (we leave it, with a reason) · `conflict` (two authors or agents clashed) ·
`candidate` (seen, not decided yet).
"Check before → after": the Norma result for this rule before and after the change.

| time | kind | rule | file:line | authors (person + agent) | PR | what | reason | check before → after |
|---|---|---|---|---|---|---|---|---|
| 16:40 | fixed | *example:* no bare `except` | `src/fetch.py:31` | Kat + Claude Code | #4 | catch only `httpx.TimeoutException` | a bare except hid a 403 as "site dead" | 1 finding → 0 |
