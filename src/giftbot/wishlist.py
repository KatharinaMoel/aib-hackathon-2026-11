"""Turn a round and the agent's facts into the list the group sees (docs/GIFT_BOT.md, "What the group sees").

What for: one verdict per observation comes from rules.decide_entry(); this module only writes it as text.
Who reads it: whoever changes how the list looks; bot.py posts its output.
How to change: text only. A rule about money or dates belongs in rules.py, with a test.
"""

from dataclasses import dataclass

from giftbot.config import RuleConfig
from giftbot.rules import Verdict, decide_entry, format_day, format_eur
from giftbot.split import split_shares
from giftbot.state import Observation, Round

_WEEKDAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
TELEGRAM_LIMIT = 4096


@dataclass(frozen=True)
class Decided:
    """One observation with the agent's entry for it and the verdict of rules.decide_entry()."""

    observation: Observation
    entry: dict | None
    verdict: Verdict | None


def decide_round(
    round_: Round, agent_output: dict, config: RuleConfig | None = None
) -> list[Decided]:
    """One verdict per observation, in the order of the observations. The list and the plan both use it."""
    entries = {
        e.get("observation_id"): e for e in agent_output.get("entries", []) if isinstance(e, dict)
    }
    decided = []
    for observation in round_.observations:
        entry = entries.get(observation.id)
        verdict = decide_entry(entry, round_.birthday, round_.pot_cents, config) if entry else None
        decided.append(Decided(observation, entry, verdict))
    return decided


def header(round_: Round) -> str:
    """ "Wishlist for Lena · birthday Sat 5 Dec · pot €180.00 (4 pledged)" """
    day = f"{_WEEKDAYS[round_.birthday.weekday()]} {format_day(round_.birthday)}"
    pot = f"pot {format_eur(round_.pot_cents)} ({len(round_.pledges)} pledged)"
    return f"Wishlist for {round_.person} · birthday {day} · {pot}"


def _source(observation: Observation) -> str:
    return f'from {observation.author}: "{observation.text}"'


def _product_low(verdict: Verdict) -> str | None:
    """The product's 30-day low across all shops: a fact about the product, not about the chosen offer."""
    if verdict.product_low_cents is None:
        return None
    return f"product 30-day low: {format_eur(verdict.product_low_cents)}"


def _shares(round_: Round, total_cents: int) -> str | None:
    shares = split_shares(total_cents, round_.limits_cents())
    if not shares:
        return None
    low, high = min(shares.values()), max(shares.values())
    if low == high:
        return f"shares {format_eur(low)} each"
    return f"shares {format_eur(low)} to {format_eur(high)}"


def format_entry(round_: Round, observation: Observation, verdict: Verdict | None) -> str:
    """One block of the list: ✔ with price, arrival, merchant and shares, or ✘ with the reason."""
    if verdict is None:
        return f"✘ {_source(observation)}\n  dropped: the agent returned nothing for it"
    name = verdict.product_name or "No product"
    if not verdict.ok or verdict.offer is None:
        return f"✘ {name} · {_source(observation)}\n  dropped: {verdict.reason}"
    offer = verdict.offer
    rating = f"merchant {offer.shop_rating:g}" if offer.shop_rating is not None else "unrated shop"
    lines = [
        f"✔ {name} · {_source(observation)}",
        f"  {format_eur(offer.total_cents)} with shipping · arrives by "
        f"{format_day(offer.late_delivery)} · {rating}",
    ]
    extra = [x for x in (_product_low(verdict), _shares(round_, offer.total_cents)) if x]
    if extra:
        lines.append("  " + " · ".join(extra))
    if offer.url:
        lines.append(f"  {offer.url}")
    return "\n".join(lines)


def format_wishlist(round_: Round, agent_output: dict, config: RuleConfig | None = None) -> str:
    """The whole list, in the order of the observations."""
    blocks = [header(round_)]
    for decided in decide_round(round_, agent_output, config):
        blocks.append(format_entry(round_, decided.observation, decided.verdict))
    return "\n\n".join(blocks)


def changes_note(checked: Round, now: Round) -> str | None:
    """Say what changed in the group while a run was going, so nobody thinks it was checked."""
    notes = []
    added = len(now.observations) - len(checked.observations)
    if added > 0:
        notes.append(f"{added} idea(s) added during the check are not in this list")
    if now.pot_cents != checked.pot_cents:
        notes.append(
            f"the pot is now {format_eur(now.pot_cents)}; "
            f"this list used {format_eur(checked.pot_cents)}"
        )
    if not notes:
        return None
    return "Note: " + "; ".join(notes) + ". Send /idealo again to include them."


def split_message(text: str, limit: int = TELEGRAM_LIMIT) -> list[str]:
    """Cut a long text into Telegram-sized parts, at line breaks where possible."""
    parts: list[str] = []
    current = ""
    for line in text.split("\n"):
        while len(line) > limit:
            if current:
                parts.append(current)
                current = ""
            parts.append(line[:limit])
            line = line[limit:]
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) > limit:
            parts.append(current)
            current = line
        else:
            current = candidate
    if current:
        parts.append(current)
    return parts
