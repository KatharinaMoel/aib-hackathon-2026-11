# Gift bot – Telegram side

The idea and the contract: `docs/GIFT_BOT.md`. This file: how to run it, test it and change it.

```text
Telegram group ──► bot.py ──► agent.py: `claude -p` + skill gift-wishlist ──► idealo MCP
                     ▲                         │ facts as JSON
                     └── wishlist.py, plan.py ◄── rules.py, split.py
```

| File | Does |
|---|---|
| `bot.py` | Telegram commands; thin handlers, no logic |
| `state.py` | rounds, observations, pledges (in memory) |
| `agent.py` | starts one `claude -p` run; only the skill and the four idealo tools are allowed |
| `wishlist.py` | writes the list from the verdicts of `rules.py` |
| `plan.py` | picks the gift plan from the ✔ entries: what to buy with the pot, what is left over, order by |
| `rules.py`, `split.py`, `config.py` | money, dates, merchant checks, shares |

## Run it

1. Create a bot: chat with `@BotFather`, send `/newbot`, copy the token.
2. Add to `.env`: `TELEGRAM_BOT_TOKEN=<token>`. Optional: `GIFTBOT_AGENT_TIMEOUT_SECONDS=600`,
   `GIFTBOT_CLAUDE_MODEL=sonnet`.
3. Connect idealo once in Claude Code on this machine: `claude mcp add --transport http idealo
   https://mcp.idealo.com/mcp`, then `/mcp` → `idealo` → Authenticate. The bot uses this login.
4. The skills must be in `.claude/skills/` (branch `kat/gift-skills-skeleton` until it is merged).
5. Start: `PYTHONPATH=src uv run --env-file .env python -m giftbot`. You should see `gift bot starting`.

## Try it

In a group with the bot (privacy mode stays on: the bot sees only commands):

1. `/gift Lena 2026-12-05` → "New round for Lena".
2. `/idea she started climbing` → "Noted as idea 1".
3. `/pledge` → a button. Press it, press Start in the private chat, send `60` → the group sees
   "Got it: pot €60.00, 1 answered." Send `0` instead if you are not chipping in: you count as answered.
4. `/idealo` (or `/wishlist`) → after a few minutes, the list: ✔ or ✘ per idea, with the reason. Then the gift
   plan: the ✔ entries the pot pays for together (a wish the person said out loud first), the money left over,
   the order-by date, and who places the order (the person who sent `/gift`).

Every run's raw answer is saved in `data/runs/` (git-ignored). Read it when a number looks wrong.

## Test it

`uv run pytest` – no Telegram, no Claude, no network. `agent.py` is tested with a fake runner.

## Change it

- Follow `CONTRIBUTING.md`: branch `<name>/<topic>`, `tools/check` → `0 must fix`, small PR.
- A new command: a handler in `bot.py`, its logic in `state.py` or `wishlist.py` with a test.
- A rule about money or dates goes into `rules.py` with a test, never into the bot or a skill.
- What the agent searches: the skills in `.claude/skills/`. Their output format is the contract in
  `docs/GIFT_BOT.md`; tell the team before you change a field.

## Limits

- State lives in memory: a restart forgets all rounds.
- Anyone who finds the bot can use it and spend the idealo quota (500 calls per day, trial).
- A full run with a real `claude -p` and idealo is not verified yet.
- With two pledges, each person can work out the other's limit from the pot (`docs/GIFT_BOT.md`, open point).
- The order-by date assumes that a merchant's delivery time stays the same on a later day. Not verified.
- From the gift-pot draft (comment on PR #14), not built: who is in and reminders, exclusions ("she already
  has X"), objections and rejected products, add-ons for the money left over, solo mode, free-text messages.
