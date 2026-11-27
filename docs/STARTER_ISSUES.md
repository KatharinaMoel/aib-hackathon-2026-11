# Starter issues

<!-- Ten first tasks, written before the day, so each person can claim one at the start instead of inventing
work. Copy each into a GitHub issue with the "Task" form (or ask your agent to). A proposal: the team changes
or drops any of them after reading the task details. See docs/FILES.md. -->

Order matters: **#1 merges first, by 16:00** – a walking skeleton that already runs end to end with stubs.
Everything else plugs into it and can run in parallel. #8 waits for Stackgini's labelled examples.

| # | Title | Done when (command → result) | Files | Lane |
|---|---|---|---|---|
| 1 | `task: walking skeleton – URL → fetch → signals → judge → verdict (JSON + Markdown)` | `uv run --env-file .env python -m <pkg> https://acme-crm.example` → a schema-valid JSON verdict and a readable Markdown verdict, with one stub signal and a stub judge | `src/<pkg>/`, `tests/test_cli.py`, `pyproject.toml`/`uv.lock` (package config and all runtime deps: e.g. httpx, the LLM SDK, jsonschema – one place, so later PRs need not touch them) | quick (skeleton phase) |
| 2 | `task: shared fetch helper – timeout, User-Agent, cache, page limit, URL guard` | `uv run pytest tests/test_fetch.py` → passes without network | `src/<pkg>/fetch.py`, tests | two-views (`second-opinion`) |
| 3 | `task: signal "others talk about it" – Tavily search → fetch → verified quote; record empty searches (MVP)` | test with saved search results: a found page gives a quote fact, no results give a measurement fact | `src/<pkg>/signals/outside.py`, tests | two-views (`second-opinion`) |
| 4 | `task: signal "product still alive" – dates in changelog, docs, blog, status page, sitemap (MVP)` | test with fixtures: newest date found, or `not_checked` | `src/<pkg>/signals/alive.py`, tests | standard |
| 5 | `task: signal domain age – RDAP + Wayback vs "since 20xx" (MVP)` | test with saved JSON answers, no network | `src/<pkg>/signals/domain_age.py`, tests | standard |
| 6 | `task: verifier – drop a fact whose quote is not on the fetched page` | test: exact and normalized match kept, changed quote dropped | `src/<pkg>/verify.py`, tests | two-views (`second-opinion`) |
| 7 | `task: judge – real LLM call, judge rules, examples with Stackgini's reasons` | test with a fake LLM: schema-valid verdict, always a call; bad JSON → `unclear`. Model name, endpoint and key come from `.env` (proposal: `JUDGE_MODEL`, `JUDGE_BASE_URL`, `JUDGE_API_KEY`), so switching the provider (e.g. to Nebius Token Factory) changes only `.env`; test: the judge uses the values from a fake environment, and a missing key stops with a clear error | `src/<pkg>/judge.py`, `.env.example`, tests | two-views (`second-opinion`) |
| 8 | `task: eval – two error counts on the labelled set` | `…` → prints hollow-called-solid and solid-called-hollow (`eval/README.md`) | `eval/` | standard |
| 9 | `task: run on a list → verdict file in the 19:45 format + one Markdown verdict per product` | `… products.txt` → one file with all verdicts; a timeout gives `unclear`, never a crash; under 3 min per product | `src/<pkg>/batch.py`, tests | standard |
| 10 | `task: more signals, one PR each – copyright year, dead links, social links, chatbot leftovers, provably fake urgency` | one test per signal with a fixture | `src/<pkg>/signals/…` | standard |

`<pkg>` is the package name; issue #1 picks it. Signals and their pitfalls: `docs/SIGNALS.md`.
The Markdown verdict is what a person reads: the call, 3–5 reasons each with its link, and "what we could not
check". The judges read reasons by hand (brief, p. 3), and the top three run one product live.
