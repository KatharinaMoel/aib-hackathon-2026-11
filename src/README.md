# src/taste – the agent

<!-- The agent's code. A walking skeleton prepared before the day on branch prep/skeleton: it runs end to end
with a stub signal and a stub judge. The team decides at the start whether to use it (and whether code from
before the day is allowed). See docs/FILES.md. -->

**Status:** walking skeleton (starter issue #1). Prepared by Katharina with Claude Code on 25 Nov 2026. Use it
only if the organisers allow code from before the day and the team agrees; otherwise rebuild it on the day.

```bash
uv sync
uv run --env-file .env python -m taste https://example.com --out out/try   # prints the Markdown verdict
uv run pytest tests/test_skeleton.py                                      # no network, no LLM
```

| File | What it does | Starter issue that grows it |
|---|---|---|
| `cli.py`, `__main__.py` | command line; writes `<out>/<host>.json` and `.md` | #9 (list of URLs → one verdict file) |
| `pipeline.py` | one product: fetch → signals → verify → judge → verdict dict; numbers facts `F1, F2 …`; drops reasons that cite unknown IDs or unverified quotes | – |
| `fetch.py` | the only network access: timeout, User-Agent, URL guard (no private addresses), HTML → visible text | #2 (cache, page limit) |
| `signals/` | one module per signal; `SIGNALS` lists them; today one stub (`homepage.py`) | #3, #4, #5, #10 |
| `verify.py` | is the quote really on the fetched page? `exact` / `normalized` / `absent` | #6 |
| `judge.py` | `stub_judge` (no LLM) and `llm_judge(complete)` with the judge rules; bad model JSON → `unclear` | #7 (model, examples) |
| `render.py` | the Markdown verdict a person reads | – |
| `models.py` | `Page`, `Fact`, `SignalResult` – shapes shared by all modules | – |

**Add a signal:** write `signals/<name>.py` with a function `(page, fetcher) -> SignalResult`, add it to
`SIGNALS`, add a test with a fixture in `tests/fixtures/`. Facts need a URL; outside sources get
`tier="independent"`. A source that fails goes to `not_checked`, never into a con.

**Not decided here (on purpose):** the model and its SDK, the search API, the verdict values (draft in
`schema/verdict.schema.json`), the format of the 19:45 file.
