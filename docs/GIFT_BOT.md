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

## How a round runs

From the gift-pot draft (comment by `rmohn-dev` on PR #14, 27 Nov 2026). Its goal: remove the usual group-gift
chaos. The bot decides and asks as little as possible.

| Step | What happens | Part |
|---|---|---|
| 1. Setup | The bot asks once, and only for what is missing: who the gift is for and the occasion, who is in (names), the deadline (the latest day the gift may arrive) and the organizer (the person who orders; default: the person who started the round). | bot |
| 2. Collect | Each person gives a pledge and, if they like, hints about the person. A pledge of €0 is an answer: it does not block the pot, and that person's hints count in full. After each input the bot confirms in one line: "Got it: pot €40, 4 of 6 answered." | bot |
| 3. Remind | While someone has not answered, the bot ends its reply by tagging that person once. | bot |
| 4. Close | The pot closes when every named person has answered, or when the organizer writes "close the pot". The bot posts "Pot closed: €60. Working on ideas." | bot |
| 5. Research | One agent run checks the hints on idealo, the strongest hint first. | skills |
| 6. Plan | The code builds the gift plan: what fits the pot, the total prices, the order date, the money left over. | rules |
| 7. Post | The bot posts the plan. An objection changes the plan. A product the group rejected never comes back. | bot |

- **Solo mode.** One person with a budget runs the same steps. The pot closes when that person has given a
  budget and hints.
- **Who gave what stays private.** The group sees the total and how many people pledged. It never sees who gave
  how much or who gave nothing.
- **The person who gets the gift sees nothing:** not the pot, not the hints, not the plan. If that person seems
  to be in the chat, the bot says so and stops posting details.
- **What the bot remembers in a round:** every pledge, every hint and exclusion ("she already has X"), every
  product it proposed and every objection.
- **No hints at all.** The bot asks once for the person's age and the relationship (colleague, uncle, best
  friend). The agent then searches product types that fit almost anyone: coffee and tea, care products, sweets,
  kitchen helpers, plants, cosy home items. This is a case where the idea does not come from a friend (see
  "Open for the team").

## How the bot talks

From the gift-pot draft.

- Casual, friendly, short. Chat-sized messages, no walls of text.
- Default language: English. If a person writes in German, the bot answers that person in German. In a mixed
  group the summaries stay in English.
- At most one emoji per message.
- The bot handles no payment and no order. It never says that money was collected or that an order was placed.
- The organizer orders with their own address. The bot does not ask for an address and stores none.
- When a result rests on thin data (only one merchant found), the bot says so.

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

The gift-pot draft ends with a gift plan instead of a list (made-up numbers):

```
🎁 Gift plan for Lena
Pot: €180.00

Buying:
1. Headphones, newer generation at <merchant>, €169.00 with shipping, arrives by 2 Dec
   <link>

Left over: €11.00 → 3 small ideas that fit
Order by: 28 Nov · must arrive by: 3 Dec
Jonas, you place the order.
Prices from idealo, 27 Nov 2026.
```

The draft writes "delivery x days". idealo states a date (`late_delivery_date`), so the plan shows the date.
Whether the group gets the list, the plan or both: see "Open for the team".

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
| **Bot** (`src/giftbot/bot.py`, `telegram.py`, `state.py`, `agent.py`) | runs the round (setup, pledges, hints, reminders, closing the pot), starts the agent run, posts the list and the plan | decide anything about products or money |
| **Skills** (`.claude/skills/idealo-lookup/`, `observation-to-gift/`, `gift-wishlist/`) | turn an observation into a search, call the MCP, copy idealo's fields unchanged | compute sums, compare dates, rank, advise |
| **Rules** (`src/giftbot/rules.py`, `split.py`) | total price, arrival check, merchant check, ✔ or ✘ with a reason, shares | call the network or a model |

Who owns which part: see the assigned issues.

Principle: **the agent finds facts, the code decides.** That keeps money and dates testable without network
(AGENTS.md, rule 12) and every number traceable to an MCP response (rule 2).

The gift-pot draft tells the agent "you decide yourself". We keep that towards the group: the bot decides, the
group does not vote on every step. Inside the bot the split above stays: the agent reads texts and finds facts,
the code does the sums and the dates.

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

### Proposed additions from the gift-pot draft (not built)

None of these is in the skills (PR #14) or in `rules.py` (PR #13) yet. Each one needs a team OK first, because
three parts depend on the contract.

| Where | Field | Values | For |
|---|---|---|---|
| input | `occasion` | text | setup: "birthday", "farewell" |
| input | `deadline` | date | the latest day the gift may arrive; would replace `birthday`, so the bot works for any occasion |
| input | `exclusions[]` | texts | "she already has X", "he hates Y": the agent never searches these |
| input | `rejected[]` | `productRef` values | products the group rejected: the agent never returns them again |
| input | `age`, `relationship` | text | only when there is no hint at all |
| output | `fetched_at` per entry | time of the MCP call | the line "Prices from idealo, 27 Nov 2026" (AGENTS.md, rule 2). idealo also sends a time stamp per offer, `freshness` (`docs/IDEALO_TOOLS.md`) |

The draft names four kinds of hint. Two of them are not a `kind` yet:

| In the draft | `kind` here | Note |
|---|---|---|
| explicit need: "she said she needs headphones" | `said` | highest weight: these entries come first in the plan |
| interest: "likes coffee, plants, running" | new: `likes` | close to `does`, but names a taste, not an activity |
| experience: "wants to go to the Christmas market" | new: `wants_to_do` | the agent names products that fit: insulated mug, warm gloves |
| exclusion: "she already has X", "he hates Y" | none | not an observation; goes into `exclusions[]` |
| – | `owns_old`, `complains` | in this file, not in the draft |

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

### Rules from the gift-pot draft

The table above already covers four rules of the draft: total price with shipping, offers that arrive too late
are dropped, nothing goes over the pot, 2 buffer days. New, and not in `rules.py` yet:

| Rule | Proposal | Part |
|---|---|---|
| Gift plan | one main gift, or a combination of ✔ entries within the pot; `said` entries first | rules |
| Several items | prefer offers from the same merchant, to save shipping | rules |
| Order by | the day the offers were read, plus the days between `late_delivery_date` and the deadline minus 2 days. The bot proposes the date and asks for an OK. If someone names another date, the code checks it and the bot warns if the gift would be late | rules, bot |
| Left over | pot minus the total of the plan, shown as "€8.11 left". Then 3 small add-ons within that amount, and a button "Show 20 more ideas" | rules, skills, bot |
| Close early | the deadline is less than 7 days away and answers are missing: the bot suggests to the organizer to close the pot now | rules, bot |
| Re-check | right before the final post, the bot reads the chosen offers again. If a price or the availability changed, the code builds the plan again first | bot, rules |
| Conflicting hints | a concrete statement beats a vague one; the majority beats a single voice; a real tie: drop the theme and say so in one line; ask the group only if the top pick depends on it, as one yes/no question | skills |
| Need without a model | "needs headphones": the draft picks a solid mid-range model and gives the reason in one sentence. This clashes with "do not rank, do not advise" (see "Open for the team") | skills |

Limits: "Show 20 more ideas" with total price, merchant and link needs one `get_product_offers` call per
product, so 20 calls, and two searches (one search returns 10 results). We allow 4 calls per observation, and the
trial has 500 calls per day (`docs/IDEALO_TOOLS.md`, "Limits", not checked). The search price alone is not a
price someone can pay.

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
| A bot cannot list the members of a group, so it has to ask who is in (gift-pot draft) | [available methods](https://core.telegram.org/bots/api#available-methods) |
| How the bot tags a person who has no username | [MessageEntity](https://core.telegram.org/bots/api#messageentity), type `text_mention` |
| A button under a message, for "Show 20 more ideas" | [InlineKeyboardMarkup](https://core.telegram.org/bots/api#inlinekeyboardmarkup) |
| The delivery time of an offer stays the same when the order is placed some days later; the rule "Order by" depends on it | no source found; ask idealo |
| Which idealo field says that an offer is in stock | `docs/IDEALO_TOOLS.md` lists the search filter `availableOnly` and `delivery.deliveryStatus`; a stock field per offer: not seen |

## Open for the team

- With two pledges, each person can work out the other's limit from the pot. Show the pot from two pledges, or
  only from three?
- Which merchant rating is the minimum?
- The vote on the list: Telegram poll, or nothing?

From the gift-pot draft (comment on PR #14, 27 Nov 2026):

- Who reads the chat? The draft is one agent that understands free text ("I'm in for 10", "ich geb nichts") and
  answers in the person's language. This file has one agent run per round; how the bot understands free text is
  not decided. Proposal: a fourth skill reads one chat message and returns JSON (pledge, hint, exclusion,
  objection), and the code keeps the ledger. Cost: one model call per message.
- Pledge in private (this file) or as a message in the group (draft)? A message in the group shows everyone who
  gave how much. The draft wants to avoid exactly that.
- List, plan or both? This file shows every hint with ✔ or ✘ and lets the group choose. The draft lets the bot
  choose one plan and then takes objections.
- May the agent bring its own ideas? The draft does so in three places: no hints (product types that fit almost
  anyone), experiences (products that fit), add-ons for the money left over. This file says the idea comes from
  a friend.
- Which product for a need without a model: the draft's "solid mid-range model", or a fixed rule such as "the
  first product with at least 3 offers" (`idealo-lookup` in PR #14, line marked TEAM)?
- `birthday` or `deadline` as the field name?
- One skill file for the whole flow (`gift-pot-agent`, as drafted) or the three skills of PR #14?
