"""The Telegram side of the gift bot: commands in the group, pledges in private, the list on /idealo.

What for: collects observations and pledges and posts the list. It decides nothing about products or money
(docs/GIFT_BOT.md, "Three parts, one contract"): facts come from agent.py, verdicts from rules.py.
Who reads it: whoever changes a command; __main__.py starts it.
How to change: keep handlers thin; put logic in state.py or wishlist.py, where tests can reach it.

Commands (privacy mode stays on, so in a group the bot sees only commands):
  group:   /gift <name> <YYYY-MM-DD> · /idea <observation> · /pledge · /idealo (or /wishlist) · /help
  private: /start (from the pledge button) · then the amount, e.g. "50"

After the list, /idealo posts the gift plan of plan.py: what to buy with the pot, and when to order.
"""

import asyncio
import logging
from datetime import UTC, datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    TypeHandler,
    filters,
)

from giftbot.agent import AgentError, run_agent
from giftbot.plan import build_plan, format_plan
from giftbot.rules import format_eur
from giftbot.state import (
    Store,
    parse_amount_cents,
    parse_pledge_payload,
    parse_round_args,
    pledge_payload,
)
from giftbot.wishlist import changes_note, decide_round, format_wishlist, split_message

log = logging.getLogger(__name__)

HELP = (
    "I turn what you noticed about a person into a checked gift list.\n\n"
    "1. /gift Lena 2026-12-05 – start a round\n"
    "2. /idea her headphones are ancient – one observation per command\n"
    "3. /pledge – tell me in private the most you would chip in \n"
    "4. /idealo – I check every idea on idealo, post the list and a gift plan"
)
_PENDING = "pledge_chat_id"  # key in user_data: the group a private pledge is for


def _name(update: Update) -> str:
    user = update.effective_user
    return user.first_name if user and user.first_name else "someone"


def _args(context: ContextTypes.DEFAULT_TYPE) -> str:
    return " ".join(context.args or [])


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(HELP)


async def gift(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    parsed = parse_round_args(_args(context))
    if parsed is None:
        await update.effective_message.reply_text("Usage: /gift <name> <YYYY-MM-DD>")
        return
    person, birthday = parsed
    organizer = _name(update)
    context.bot_data["store"].start(update.effective_chat.id, person, birthday, organizer)
    await update.effective_message.reply_text(
        f"New round for {person}, birthday {birthday.isoformat()}. {organizer} places the order.\n"
        "Add ideas with /idea <what you noticed>, then /pledge."
    )


async def idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    store: Store = context.bot_data["store"]
    if store.get(update.effective_chat.id) is None:
        await update.effective_message.reply_text(
            "No round yet. Start one with /gift <name> <date>."
        )
        return
    observation = store.add_observation(update.effective_chat.id, _name(update), _args(context))
    if observation is None:
        await update.effective_message.reply_text("Usage: /idea <what you noticed>")
        return
    await update.effective_message.reply_text(f"Noted as idea {observation.id}.")


async def pledge(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.bot_data["store"].get(update.effective_chat.id) is None:
        await update.effective_message.reply_text(
            "No round yet. Start one with /gift <name> <date>."
        )
        return
    link = f"https://t.me/{context.bot.username}?start={pledge_payload(update.effective_chat.id)}"
    button = InlineKeyboardMarkup([[InlineKeyboardButton("Pledge in private", url=link)]])
    await update.effective_message.reply_text(
        "Tell me in private the most you would chip in. The group sees only the total.",
        reply_markup=button,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = parse_pledge_payload(_args(context))
    round_ = context.bot_data["store"].get(chat_id) if chat_id is not None else None
    if round_ is None:
        await update.effective_message.reply_text(HELP)
        return
    context.user_data[_PENDING] = chat_id
    await update.effective_message.reply_text(
        f"Gift for {round_.person}: what is the most you would chip in, in euros? (e.g. 50)"
    )


async def private_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = context.user_data.get(_PENDING)
    if chat_id is None:
        await update.effective_message.reply_text(HELP)
        return
    cents = parse_amount_cents(update.effective_message.text or "")
    if cents is None:
        await update.effective_message.reply_text("Please send an amount in euros, e.g. 50")
        return
    store: Store = context.bot_data["store"]
    round_ = store.pledge(chat_id, update.effective_user.id, _name(update), cents)
    if round_ is None:
        await update.effective_message.reply_text(
            "That round is gone. Ask the group for a new link."
        )
        return
    del context.user_data[_PENDING]
    await update.effective_message.reply_text(f"Saved: up to {format_eur(cents)}. Thank you!")
    await context.bot.send_message(
        chat_id,
        f"{len(round_.pledges)} pledged so far · pot {format_eur(round_.pot_cents)}",
    )


async def idealo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    round_ = context.bot_data["store"].get(chat_id)
    if round_ is None or not round_.observations:
        log.info("idealo stopped in chat %s: no round or no idea", chat_id)
        await update.effective_message.reply_text(
            "First /gift <name> <date>, then at least one /idea."
        )
        return
    if round_.pot_cents == 0:
        log.info("idealo stopped in chat %s: the pot is empty", chat_id)
        await update.effective_message.reply_text("The pot is still empty. Use /pledge first.")
        return
    running: set[int] = context.bot_data["running"]
    if chat_id in running:
        log.info("idealo stopped in chat %s: a run is already going", chat_id)
        await update.effective_message.reply_text("I am already checking this list.")
        return
    running.add(chat_id)
    try:
        await update.effective_message.reply_text(
            f"Checking {len(round_.observations)} idea(s) on idealo. This can take a few minutes."
        )
        await context.bot.send_chat_action(chat_id, "typing")
        settings = context.bot_data["settings"]
        checked = round_.snapshot()  # ideas and pledges sent while the run goes do not change it
        output = await asyncio.to_thread(
            run_agent,
            checked.agent_input(),
            timeout_s=settings["timeout_s"],
            model=settings["model"],
        )
        text = format_wishlist(checked, output)
        note = changes_note(checked, round_)
        if note:
            text += "\n\n" + note
        for part in split_message(text):
            await context.bot.send_message(chat_id, part, disable_web_page_preview=True)
        read_on = datetime.now(UTC).date()  # the day the agent read the offers
        # The plan uses the same snapshot as the list: the ideas and the pot the search used.
        plan = build_plan(checked, decide_round(checked, output), read_on)
        if plan is not None:
            for part in split_message(format_plan(checked, plan, read_on)):
                await context.bot.send_message(chat_id, part, disable_web_page_preview=True)
    except AgentError as err:
        log.warning("agent run failed for chat %s: %s", chat_id, err)
        await update.effective_message.reply_text(f"Sorry, the idealo check failed: {err}")
    finally:
        running.discard(chat_id)


async def group_only(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_text(
        "This command works in a group. Add me to a group, then send it there.\n\n" + HELP
    )


async def log_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log what arrives: chat, chat type and the command word. Never the text people wrote."""
    message, chat = update.effective_message, update.effective_chat
    if message is None or chat is None:
        log.info("update %s without a message", update.update_id)
        return
    text = message.text or ""
    kind = text.split()[0] if text.startswith("/") else ("text" if text else "other")
    log.info("update: chat %s (%s), %s", chat.id, chat.type, kind)


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    log.error("update failed", exc_info=context.error)


def build_application(token: str, timeout_s: float, model: str | None) -> Application:
    """Wire the handlers. Updates run concurrently, so a slow /idealo does not block other chats."""
    app = Application.builder().token(token).concurrent_updates(True).build()
    app.bot_data.update(
        store=Store(), running=set(), settings={"timeout_s": timeout_s, "model": model}
    )
    groups, private = filters.ChatType.GROUPS, filters.ChatType.PRIVATE
    app.add_handler(TypeHandler(Update, log_update), group=-1)  # runs first, for every update
    app.add_handler(CommandHandler("gift", gift, filters=groups))
    app.add_handler(CommandHandler("idea", idea, filters=groups))
    app.add_handler(CommandHandler("pledge", pledge, filters=groups))
    app.add_handler(CommandHandler(["idealo", "wishlist"], idealo, filters=groups))
    app.add_handler(CommandHandler("start", start, filters=private))
    app.add_handler(CommandHandler("help", help_cmd))
    group_commands = ["gift", "idea", "pledge", "idealo", "wishlist"]
    app.add_handler(CommandHandler(group_commands, group_only, filters=private))
    app.add_handler(MessageHandler(private & filters.TEXT & ~filters.COMMAND, private_text))
    app.add_error_handler(on_error)
    return app
