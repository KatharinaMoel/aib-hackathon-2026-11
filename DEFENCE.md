# Defence

<!-- Draft of the Norma note for the submission form (a few sentences; 60 of 100 Norma points depend on it).
Write it at 18:15 from the rows in DECISIONS.md. See docs/FILES.md. -->

## Fixed
Rule:
File:
Why it mattered:

## Accepted
Rule:
File:
Why we left it:

## Conflict between authors
Authors:
What clashed:
How we resolved it:

## Policy
Name in Norma: not set yet – `<team name> – house rules` (the workspace is named after the team, `docs/TEAM.md`).

Rules it holds: the seven house rules from `AGENTS.md` ("House rules for code"), each mapped to a Norma rule ID.
IDs from `get_rules_for_ruleset` (python-norma-ruleset, secrets-norma-ruleset) on 2026-11-27.

| # | House rule | Norma rule ID | Severity | Also checked by |
|---|---|---|---|---|
| 1 | Every HTTP call has a timeout | `py-scal-requests-no-timeout-1.0` | MEDIUM | ruff `S113` |
| 1b | No timeout switched off (`timeout=None`, httpx) | `py-scal-http-no-deadline-1.0` | HIGH | – |
| 2 | No broad `except` | `py-maint-broad-except-1.0` | HIGH | ruff `BLE`/`E722` |
| 3 | Logging, not `print` | `py-maint-no-print-1.0` | MEDIUM | ruff `T20` |
| 4 | Timezone-aware times | `py-maint-naive-datetime-1.0` | MEDIUM | ruff `DTZ` |
| 5 | No secrets in code | `py-sec-hardcoded-secret-1.0` | MEDIUM | `tools/check`, CI `guard` |
| 5b | No AI provider key in code | `sec-ai-provider-key-1.0` | HIGH | – |
| 6 | No `eval`/`exec` | `py-sec-eval-exec-1.0` | HIGH | ruff `S102`/`S307` |
| 7 | TLS stays on | `py-sec-tls-verify-false-1.0` | HIGH | – |

1b and 5b are not in `AGENTS.md` yet: they cover httpx and the LLM key. Add them there by PR if the team agrees.

Optional, if the team agrees: `py-maint-logger-fstring-1.0` (goes with rule 3), `py-mng-open-no-encoding-1.0`
(recorded MCP responses in `data/`), `py-perf-http-client-per-call-1.0` (one shared fetch helper, `AGENTS.md` rule 8).

Planned exception: `py-maint-broad-except-1.0` at the per-site boundary, as `AGENTS.md` allows. Log it in
`DECISIONS.md` as accepted, with file and line. `print` in `tools/` and `tests/` is allowed; whether a Norma policy
can exclude paths is not verified – if not, log those findings as accepted.

Not verified: the form of a policy in the Norma app. Adapt these fields there.

How it kept authors consistent (one example):
