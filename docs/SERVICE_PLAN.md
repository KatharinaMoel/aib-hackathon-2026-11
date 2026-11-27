# Plan: from skills to a service

<!-- What this file is for: a proposal to move the idealo part of the gift bot from Claude Code skills into
Python code, so the bot follows the skills' rules every time. Written 27 Nov 2026, after the hackathon demo.
Who reads it: whoever continues the gift bot, and their coding agents.
How to change it: by PR (fast lane). Nothing here is built yet; each step below becomes its own PR. -->

**Status:** proposal, not built. The bot works today as described in "Where we are". Change nothing before the
team agrees.

## Where we are

There is no separate service. Everything runs on the laptop of the person who starts the bot.

```text
Telegram ──► bot (Python) ──► `claude -p` + skills ──► idealo MCP
                 ▲                    │ JSON "entries"
                 └── rules.py, plan.py ◄┘
```

1. On `/idealo`, `src/giftbot/agent.py` starts `claude -p` (Claude Code) with the skill `gift-wishlist`.
2. Claude reads the skills, calls the idealo MCP, and returns the `entries` JSON (`docs/GIFT_BOT.md`, "The contract").
3. `rules.py` decides ✔ or ✘ per idea; `plan.py` builds the gift plan; the bot posts both.

It depends on three things on that laptop: the Claude Code login, the idealo login inside Claude Code, and the
skills in `.claude/skills/`.

Measured on 27 Nov 2026 (two real rounds, model `sonnet`, raw answers in `data/runs/`):

| Round | Ideas | Time | Steps | Cost |
|---|---|---|---|---|
| 18:23 | 2 | 69 s | 15 | $1.21 |
| 19:04 | 3 | 84 s | 15 | $1.30 |

### What is guaranteed today, and what is not

| Rule | Guaranteed by | Today |
|---|---|---|
| Only the skill and the four idealo tools can run | `--allowedTools` in `agent.py` | code |
| The answer has the `{"entries": [...]}` shape | `extract_json_object()` in `agent.py` | code |
| Money, dates, merchant checks, the plan | `rules.py`, `split.py`, `plan.py` | code, with tests |
| Every idealo call is logged with tool, arguments, time | `data/runs/<time>.calls.json` (PR #26) | code |
| Search with `maxPrice` = pot and `availableOnly: true` | text in `idealo-lookup` | **instruction only** |
| Keep only `itemType == "PRODUCT"`; pick one product | text in `idealo-lookup` | **instruction only** |
| At most 4 idealo calls per idea | text in `idealo-lookup`; the log warns afterwards | **instruction only** |
| Copy prices and dates unchanged, never from memory | text in `idealo-lookup` | **instruction only** |
| Skip ideas that need a size or name no product | text in `observation-to-gift` | **instruction only** |

"Instruction only" means Claude should do it, but nothing forces it. The call log shows afterwards whether it did.

## The three skills

| Skill | What it does | Needs judgement? |
|---|---|---|
| `gift-wishlist` | loops over the ideas, uses the other two skills, returns `{"entries": [...]}` | no – it only coordinates |
| `observation-to-gift` | turns an idea ("she started climbing") into one German product-type query ("Chalkbag") and a `kind`, or a reason to skip it | **yes** – it reads people's words |
| `idealo-lookup` | search → keep `PRODUCT` → pick one → offers → price history → copy the fields; at most 4 calls | no – fixed steps |

## Proposal

Move the fixed steps into Python. Keep one small model call for the part that needs judgement.

```text
Telegram ──► bot ──► ideas.py: one Claude API call, no tools ──► {kind, mode, query} or skipped_reason
                 └─► lookup.py: Python ──► idealo.py: MCP client ──► idealo MCP
                 └─► rules.py, plan.py (unchanged)
```

| Today | Proposed | Why |
|---|---|---|
| `idealo-lookup` (skill) | `src/giftbot/lookup.py` + `src/giftbot/idealo.py` (code) | fixed steps: in code they always hold, are tested without network, and cost no model tokens |
| `gift-wishlist` (skill) | a loop in `lookup.py` (code) | it only coordinates |
| `observation-to-gift` (skill) | `src/giftbot/ideas.py`: one Claude API call per round, all ideas at once, JSON output | the only part that needs a model; the skill text becomes the prompt |

The output stays the `entries` JSON of `docs/GIFT_BOT.md`. So `rules.py`, `wishlist.py`, `plan.py` and the bot's
messages do not change.

### What we expect (estimates, not measured)

- A round takes seconds instead of about 80 s, and costs cents instead of about $1.30.
- The search rules hold on every run, not only when the model follows them.
- The bot no longer needs Claude Code on the machine, so it can run on a server.

## Steps

Each step is one PR with its own check (AGENTS.md, rule 7).

| # | Step | Done when |
|---|---|---|
| 0 | **Spike: idealo login from Python.** Use the `mcp` Python SDK ([repo](https://github.com/modelcontextprotocol/python-sdk)) with its OAuth client. Store the token in `data/` (git-ignored). | A script lists the four idealo tools, and still works after a restart without a browser. **If this fails, stop here** and keep the `claude -p` route. |
| 1 | `src/giftbot/idealo.py`: one function per MCP tool; timeout; at most 3 calls per second; every call logged (tool, arguments, time) to `data/runs/`. | Tests with hand-written responses of made-up products in `tests/fixtures/` pass without network. |
| 2 | `src/giftbot/lookup.py`: the steps of `idealo-lookup` in code, at most 4 calls per idea, and the pick rule the team chose. | Tests: only `PRODUCT` kept; offers and history use the same `productRef`; a failed call gives `product: null`, not a crash. |
| 3 | `src/giftbot/ideas.py`: one Claude API call with structured JSON output; prompt from `observation-to-gift`. Needs `ANTHROPIC_API_KEY` in `.env`. | Tests with a fake client: every idea gets a query or a `skipped_reason`; bad JSON gives a clear error. |
| 4 | Wire it in behind the same `run_agent()` call. A setting `GIFTBOT_ENGINE=cli` / `service` keeps the old route until the new one passed a real round. | One real group round with `service` gives a list and a plan. |
| 5 | Compare both engines on 5 fixed rounds (`eval/`); switch the default when the new one is not worse. | The two lists match, or each difference has a reason. |

Step 0 comes first because everything else depends on it.

## Facts this plan rests on

| Fact | Source |
|---|---|
| The idealo MCP offers dynamic client registration, PKCE (S256), refresh tokens and the `client_credentials` grant | `https://mcp.idealo.com/.well-known/oauth-authorization-server`, read 27 Nov 2026 |
| Trial limits: 3 calls per second, 500 calls per day | [idealo MCP guide](https://github.com/idealo/mcp-server-guide), not checked by us |
| Tool names, filters and offer fields | `docs/IDEALO_TOOLS.md` (two live checks, 27 Nov 2026) |
| Time and cost of a round today | `data/runs/` of 27 Nov 2026 (table above) |

## Not verified

- That a Python script can log in to the idealo MCP and refresh the token without a browser (step 0).
- The field names inside `priceTrend.statistics` for the 30-day low (`.claude/skills/idealo-lookup/SKILL.md`).
- How to do `model_lookup` ("the newest generation of the line under the pot") without a model: it may need
  `ideas.py` to name the model.
- The time and cost estimates above.

## Open for the team

- Which product to pick from the search results (the line marked TEAM in `idealo-lookup`). Code needs one fixed
  rule. The skill's proposal: the first `PRODUCT` with at least 3 offers.
- Keep the three skills as the readable source of the rules, or delete them once the code exists?
- Which model for `ideas.py`, and who owns `idealo.py` (one owner per shared module, AGENTS.md rule 8).

### Options we did not pick

- **Keep `claude -p` and only audit the call log.** It shows mistakes afterwards; it does not prevent them.
- **Claude API with the MCP connector** (Anthropic calls the idealo MCP for us). The model still decides the
  steps, so the rules stay "instruction only", and our idealo token would go to Anthropic.
