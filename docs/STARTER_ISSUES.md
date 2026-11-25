# Starter issues

<!-- Ten first tasks, written before the day, so each person can claim one at 15:10–15:30 instead of
inventing work. Copy each into a GitHub issue with the "Task" form (or ask your agent to). See docs/FILES.md. -->

Order matters: **#1 merges first** (the shape everyone builds on). #2–#6 can then run in parallel.
#7 needs #1 and #6. #8 waits for Stackgini's labelled examples. #9 needs #2–#7; #10 needs #9.

| # | Title | Done when (command → result) | Files | Lane |
|---|---|---|---|---|
| 1 | `task: skeleton – package, Fact type, CLI with a fake judge, all runtime dependencies` | `uv run --env-file .env python -m <pkg> https://acme-crm.example` → a verdict that matches the schema | `src/<pkg>/`, `tests/test_cli.py`, `pyproject.toml`/`uv.lock` (package config and all runtime deps: e.g. httpx, the LLM SDK, jsonschema – one place, so later PRs need not touch them) | two-views (`pyproject.toml`) – merge by 16:00 |
| 2 | `task: shared fetch helper – timeout, User-Agent, cache, page limit, URL guard` | `uv run pytest tests/test_fetch.py` → passes without network | `src/<pkg>/fetch.py`, tests | two-views (`second-opinion`) |
| 3 | `task: signal copyright year (MVP)` | `uv run pytest tests/test_signal_copyright.py` → passes | `src/<pkg>/signals/copyright.py`, tests | standard |
| 4 | `task: signal dead help/docs links, max 20 (MVP)` | test with a fixture: 404 counts, 403 goes to `not_checked` | `src/<pkg>/signals/links.py`, tests | standard |
| 5 | `task: signal domain age – RDAP + Wayback vs "since 20xx" (MVP)` | test with saved JSON answers, no network | `src/<pkg>/signals/domain_age.py`, tests | standard |
| 6 | `task: verifier – drop a fact whose quote is not on the fetched page` | test: exact and normalized match kept, changed quote dropped | `src/<pkg>/verify.py`, tests | two-views (`second-opinion`) |
| 7 | `task: judge – facts → schema-valid verdict; bad LLM JSON → unclear` | test with a fake LLM; judge rules from `docs/SIGNALS.md` | `src/<pkg>/judge.py`, tests | two-views (`second-opinion`) |
| 8 | `task: eval – two error counts on the labelled set, hold-out split` | `…` → prints hollow-called-solid and solid-called-hollow | `eval/` | standard |
| 9 | `task: wire fetch → signals → verify → judge into the CLI` | one real run on a made-up or well-known site → schema-valid verdict with verified reasons; by 17:00 | `src/<pkg>/cli.py`, `src/<pkg>/pipeline.py` | standard |
| 10 | `task: run on a list → verdict file in the 19:45 format` | `… products.txt` → one file with all verdicts; a timeout gives `unclear`, never a crash | `src/<pkg>/batch.py`, tests | standard |

`<pkg>` is the package name; issue #1 picks it (by 15:30, `AGENTS.md`, "Stack and commands"). Signals and their pitfalls: `docs/SIGNALS.md`.
Whether to create these on GitHub before the day: owner decides (they are visible to the whole team).
