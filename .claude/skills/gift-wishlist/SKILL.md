---
name: gift-wishlist
description: Run one gift round – take a group's observations, the pot and the birthday, check each observation on idealo, and return the facts as JSON. Use when the gift bot asks for a wishlist.
---

# Gift wishlist

<!-- What this file is for: the full run the gift bot starts when a group asks for its wishlist.
Who reads it: the agent run the bot starts, and people who change the run.
How to change it: by PR. The input and output formats are the contract in docs/GIFT_BOT.md; tell the team before
you change a field there.
A skeleton: a proposal, change anything. -->

## Input

JSON as in `docs/GIFT_BOT.md`, "Input to one agent run": `person`, `birthday`, `pot_eur`, `country`,
`observations[]` with `id`, `from`, `text`.

## Steps

For each observation, in the order given:

1. Use the skill `observation-to-gift`: name the `kind`, choose the `mode`, build the query, or set
   `skipped_reason`.
2. If not skipped, use the skill `idealo-lookup`: search, pick one product, copy its offers and the 30-day low.
3. Write one entry.

## Output

Return only JSON as in `docs/GIFT_BOT.md`, "Output of one agent run": one entry per observation with
`observation_id`, `kind`, `mode`, `query`, `skipped_reason`, `product`, `offers`, `price_stats`.

- No text before or after the JSON.
- No ranking, no recommendation, no "best". The Python code decides what goes on the list
  (`src/giftbot/rules.py`), and the group decides what to buy.
- Do not compute totals or shares, and do not compare dates.

## Try it by hand

In a coding-agent session inside the repo, with the idealo MCP connected:

```
/gift-wishlist {"person": "Lena", "birthday": "2026-12-05", "pot_eur": 60, "country": "DE",
"observations": [{"id": 1, "from": "Mia", "text": "she started climbing this summer"}]}
```

You should see JSON with one entry, `mode` `type_search`, one product and up to 5 offers.
