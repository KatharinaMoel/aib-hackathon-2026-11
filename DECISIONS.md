# Decisions log

<!-- Evidence for the Norma track: DEFENCE.md is written from it at 18:15. Rows are copied in from the PRs' pr-norma blocks at 17:30. See docs/FILES.md. -->

One line per decision or Norma finding. Authors write their findings in the PR's `pr-norma` block; the Norma
owner copies them here in one PR at 17:30, so parallel branches do not clash on this table. Do not rewrite old
lines. At 18:15 we write `DEFENCE.md` from this log. The first row is the `baseline`: the first Norma check after
the first code PR (score and open findings).

Kinds: `baseline` (first check: score and open findings) · `fixed` · `accepted` (we leave it, with a reason) · `conflict` (two authors or agents clashed) ·
`candidate` (seen, not decided yet).
"Check before → after": the Norma result for this rule before and after the change.

| time | kind | rule ID | severity | file:line | authors (person + agent) | PR | what | reason | check before → after |
|---|---|---|---|---|---|---|---|---|---|
