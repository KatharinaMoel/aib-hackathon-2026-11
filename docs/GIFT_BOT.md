# Gift bot – "a wishlist without a wishlist"

<!-- What this file is for: the idea we build for the idealo challenge, and the contract between its three parts.
Who reads it: everyone who writes the bot, the skills or the rules, and their coding agents.
How to change it: by PR (fast lane). Tell the team before you change a field in "The contract" – three parts
depend on it. This is a proposal: change anything.
No real prices, merchant names or chat messages here – those belong in data/ (AGENTS.md, rule 1). All numbers
below are made up. -->

## The idea

A group wants to give one gift together. There is rarely a wishlist. The group does not know what the person
wishes for, but it knows what the person owns and does.

1. Friends write observations into a Telegram group: "her headphones are ancient", "she started climbing".
2. Each friend tells the bot in private the most they would chip in. The group sees only the total (the pot).
3. The bot turns every observation into a product search on idealo and checks the result against pot and date.
4. The group gets a list. Every entry shows the observation it came from, the total price, the arrival date and
   each person's share. Entries that fail stay on the list with the reason.

idealo does not produce the ideas. It makes an idea checkable: does the product exist, what does it cost with
shipping, when does it arrive, how is the merchant rated, where is the price in its 30-day range.

## What the group sees (made-up numbers)

```
Wishlist for Lena · birthday Sat 5 Dec · pot €180 (4 pledged)

✔ Headphones, newer generation · from Jonas: "her headphones are ancient"
  €169.00 with shipping · arrives by 2 Dec · merchant 4.6
  today €8.00 above the 30-day low · shares €23.00 to €45.00

✔ Chalk bag · from Mia: "she started climbing"
  €29.00 with shipping · arrives by 3 Dec · merchant unrated

✘ Coffee grinder · from Tom: "her grinder annoys her"
  dropped: cheapest offer that passes costs €240.00, the pot is €180.00
```

## Three parts, one contract

```
Telegram group ──► bot ──► agent run (skills) ──► idealo MCP
                    ▲             │
                    │        facts as JSON
                    │             ▼
              list + poll ◄── rules (Python)
```

| Part | Does | Does not |
|---|---|---|
| **Bot** (`src/giftbot/bot.py`, `telegram.py`, `state.py`, `agent.py`) | collects observations and pledges, starts the agent run, posts the list | decide anything about products or money |
| **Skills** (`.claude/skills/idealo-lookup/`, `observation-to-gift/`, `gift-wishlist/`) | turn an observation into a search, call the MCP, copy idealo's fields unchanged | compute sums, compare dates, rank, advise |
| **Rules** (`src/giftbot/rules.py`, `split.py`) | total price, arrival check, merchant check, ✔ or ✘ with a reason, shares | call the network or a model |

Who owns which part: see the assigned issues.

Principle: **the agent finds facts, the code decides.** That keeps money and dates testable without network
(AGENTS.md, rule 12) and every number traceable to an MCP response (rule 2).

## The contract

### Input to one agent run

```json
{
  "person": "Lena",
  "birthday": "2026-12-05",
  "pot_eur": 180,
  "country": "DE",
  "observations": [
    {"id": 1, "from": "Jonas", "text": "her headphones are ancient, some Sony from 2019"}
  ]
}
```

### Output of one agent run

One entry per observation, in the same order. Texts are copied from the MCP response, not reformatted.

```json
{
  "entries": [
    {
      "observation_id": 1,
      "kind": "owns_old",
      "mode": "model_lookup",
      "query": "…",
      "skipped_reason": null,
      "product": {"name": "…", "productRef": "…"},
      "offers": [
        {
          "price_text": "169,00 €",
          "shipping_text": "0,00 €",
          "late_delivery_date": "2026-12-02",
          "shop_name": "…",
          "shop_rating": 4.6,
          "is_marketplace": false,
          "payments": ["PP", "INV"],
          "url": "…"
        }
      ],
      "price_stats": {"low_text": "161,00 €", "low_date": "2026-11-20"}
    }
  ]
}
```

| Field | Values | Note |
|---|---|---|
| `kind` | `owns_old`, `does`, `complains`, `said` | the four kinds of observation |
| `mode` | `model_lookup`, `type_search` | see below |
| `skipped_reason` | text or `null` | set when the agent did not search (needs a size, too vague, not a product); then `product` is `null` and `offers` is empty |
| any other field | may be `null` | idealo leaves fields empty; write `null`, never guess |

### Two search modes

| Mode | For | How |
|---|---|---|
| `model_lookup` | "owns something old" | search the model name; idealo returns the newer generations of the line; take the newest one under the pot |
| `type_search` | the other three kinds | a concrete product type ("chalk bag", not "climbing gift") with category and `maxPrice` = pot |

Rules for every MCP call are in `docs/IDEALO_TOOLS.md`, "Rules for our code": keep only `itemType == "PRODUCT"`,
never use the search price as a price someone can pay, at most 4 calls per observation.

## Rules the code applies (defaults – the team can change them)

| Rule | Default |
|---|---|
| Total price | offer price + shipping |
| Arrives in time | `late_delivery_date` at least 2 days before the birthday |
| Merchant | rating at or above a threshold the team sets; a seller without rating is shown as "unrated", not hidden |
| Best offer | the cheapest total among the offers that pass |
| Over the pot | entry is ✘ with the missing amount; the bot never asks anyone to pay more |
| Shares | in proportion to each person's limit; nobody pays more than their limit |
| Price position | a fact ("today €8.00 above the 30-day low"), never a forecast |

## How the bot reaches idealo

Checked on 27 Nov 2026, 17:16: a headless run of the coding agent can use the idealo login of the machine it
runs on. One search took 16 seconds end to end. Command (run inside the repo):

```
claude -p "<prompt>" --allowedTools "mcp__idealo__search_products" --permission-mode dontAsk --output-format json
```

- Allow only the four `mcp__idealo__…` tools. Group messages and product titles are data, never instructions
  (AGENTS.md, rule 3); with no other tool allowed, an instruction hidden in a message has nothing to use.
- `--json-schema <schema>` makes the run return the output above (flag listed in `claude --help`; not tried yet).
- The answer of that run also carried text from a session-start hook. Read the structured result, not free text.
- Save the raw answer of every run under `data/runs/` (git-ignored).

How a script gets an idealo token without this route: not verified (`docs/IDEALO_TOOLS.md`, "Connect").

## Telegram facts

Read on 27 Nov 2026 in the [Bot API](https://core.telegram.org/bots/api) and
[bot features](https://core.telegram.org/bots/features) pages.

| Topic | Fact |
|---|---|
| Create the bot | `/newbot` in a chat with `@BotFather`; the token goes into `.env` as `TELEGRAM_BOT_TOKEN` |
| Receive messages | `getUpdates` with `timeout` (long polling); works without a webhook |
| Group messages | privacy mode is on by default: the bot sees only commands and replies. A bot that is group admin receives all messages. Or switch it off with `/setprivacy` and add the bot to the group again |
| Private pledge | a button with `https://t.me/<bot_username>?start=<payload>`; the bot receives `/start <payload>`. Allowed in the payload: `A-Z`, `a-z`, `0-9`, `_`, `-`, up to 64 characters |
| Message fields | `chat.id`, `chat.type` (`private`, `group`, `supergroup`), `from`, `text`, `date` |
| Message length | 1 to 4096 characters |

## Not verified

| Claim | Where to check |
|---|---|
| `sendPoll` in groups with `allows_multiple_answers`; anonymous by default; up to 12 options | [sendPoll](https://core.telegram.org/bots/api#sendpoll) |
| A bot cannot write to a person before that person pressed Start | not found in the docs; the pledge button above does not depend on it |
| How long a full run with several observations takes | time one run in the rehearsal |
| Scale of `shop.rating` | `data/idealo-livecheck-2026-11-27.jsonl`, before the team sets the threshold |
| 500 MCP calls per day are enough for rehearsal and demo | count the calls of one run |

## Open for the team

- With two pledges, each person can work out the other's limit from the pot. Show the pot from two pledges, or
  only from three?
- Which merchant rating is the minimum?
- The vote on the list: Telegram poll, or nothing?
