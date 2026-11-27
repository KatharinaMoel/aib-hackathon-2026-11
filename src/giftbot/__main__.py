"""Start the gift bot: `PYTHONPATH=src uv run --env-file .env python -m giftbot`.

What for: reads the settings from the environment (.env) and runs the bot with long polling, so no public URL
is needed. How to run and test: src/giftbot/README.md.
"""

import logging
import os
import sys

from giftbot.agent import DEFAULT_MAX_BUDGET_USD
from giftbot.bot import build_application

log = logging.getLogger("giftbot")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    # At INFO, httpx logs every request URL, and Telegram URLs contain the bot token.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        log.error("TELEGRAM_BOT_TOKEN is not set; add it to .env (src/giftbot/README.md)")
        sys.exit(1)
    timeout_s = float(os.environ.get("GIFTBOT_AGENT_TIMEOUT_SECONDS", "600"))
    model = os.environ.get("GIFTBOT_CLAUDE_MODEL", "").strip() or None
    max_budget_usd = float(
        os.environ.get("GIFTBOT_MAX_BUDGET_USD", "").strip() or DEFAULT_MAX_BUDGET_USD
    )
    log.info(
        "gift bot starting (agent timeout %g s, budget $%g per run)", timeout_s, max_budget_usd
    )
    build_application(token, timeout_s, model, max_budget_usd).run_polling()


if __name__ == "__main__":
    main()
