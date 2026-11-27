"""Decide which gift candidates the group can buy: total price, arrival, merchant, pot.

What for: the agent run returns facts copied from idealo (docs/GIFT_BOT.md, "The contract"). This module turns
them into one verdict per observation. No network and no model here, so every rule has a test in
tests/test_rules.py.
Who reads it: whoever changes a rule, and the bot code that calls decide_entry().
How to change: thresholds live in config.py. A new rule gets its own reason text and a test.
Words: an "offer" is one merchant selling the product; the "pot" is the sum of what the friends would chip in.
"""

import re
from dataclasses import dataclass
from datetime import date, timedelta

from giftbot.config import RuleConfig

# idealo writes prices as German text: "1.059,00 €" (dot for thousands, comma for cents).
_EUR_TEXT = re.compile(r"^\s*(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d{1,2}))?\s*(?:€|EUR)?\s*$")
# Some price texts use a no-break space before the euro sign.
_NO_BREAK_SPACE = chr(0xA0)
_MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


def parse_eur_cents(text: object) -> int | None:
    """Turn "1.059,00 €" into 105900 cents. Anything we cannot read is None, never a guess."""
    if not isinstance(text, str):
        return None
    match = _EUR_TEXT.match(text.replace(_NO_BREAK_SPACE, " "))
    if match is None:
        return None
    euros = int(match.group(1).replace(".", ""))
    cents = int((match.group(2) or "0").ljust(2, "0"))
    return euros * 100 + cents


def format_eur(cents: int) -> str:
    """Turn 105900 cents into "€1,059.00" for the English list."""
    return f"€{cents // 100:,}.{cents % 100:02d}"


def parse_day(text: object) -> date | None:
    """Read "2026-12-03" (a longer time stamp works too). Unreadable text is None."""
    if not isinstance(text, str):
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def format_day(day: date) -> str:
    """Turn a date into "3 Dec". Written by hand so the result does not depend on the computer's language."""
    return f"{day.day} {_MONTHS[day.month - 1]}"


def _number(value: object) -> float | None:
    """Accept a rating like 4.6; True and False are not numbers here."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


@dataclass(frozen=True)
class Offer:
    """One merchant's offer with only the fields the rules use. A missing fact is None."""

    price_cents: int | None
    shipping_cents: int | None
    late_delivery: date | None
    shop_name: str | None
    shop_rating: float | None
    is_marketplace: bool
    payments: tuple[str, ...]
    url: str | None

    @property
    def total_cents(self) -> int | None:
        """Price plus shipping: what the group really pays. None while one of the two is unknown."""
        if self.price_cents is None or self.shipping_cents is None:
            return None
        return self.price_cents + self.shipping_cents


def offer_from_contract(raw: dict) -> Offer:
    """Read one offer in the format of docs/GIFT_BOT.md, "Output of one agent run"."""
    payments = raw.get("payments")
    return Offer(
        price_cents=parse_eur_cents(raw.get("price_text")),
        shipping_cents=parse_eur_cents(raw.get("shipping_text")),
        late_delivery=parse_day(raw.get("late_delivery_date")),
        shop_name=raw.get("shop_name") if isinstance(raw.get("shop_name"), str) else None,
        shop_rating=_number(raw.get("shop_rating")),
        is_marketplace=raw.get("is_marketplace") is True,
        payments=tuple(p for p in payments if isinstance(p, str))
        if isinstance(payments, list)
        else (),
        url=raw.get("url") if isinstance(raw.get("url"), str) else None,
    )


def offer_from_mcp(raw: dict) -> Offer:
    """Read one offer exactly as `get_product_offers` returns it, so no model has to retype the numbers."""
    shop = raw.get("shop") if isinstance(raw.get("shop"), dict) else {}
    rating = shop.get("rating") if isinstance(shop.get("rating"), dict) else {}
    delivery = raw.get("delivery") if isinstance(raw.get("delivery"), dict) else {}
    payments = raw.get("payments") if isinstance(raw.get("payments"), list) else []
    return offer_from_contract(
        {
            "price_text": raw.get("price"),
            "shipping_text": raw.get("minShippingCost"),
            "late_delivery_date": delivery.get("lateDeliveryDate"),
            "shop_name": shop.get("name"),
            "shop_rating": rating.get("avg"),
            "is_marketplace": shop.get("isMarketplace"),
            "payments": [p.get("costCode") for p in payments if isinstance(p, dict)],
            "url": raw.get("relocatorUrl"),
        }
    )


def check_offer(offer: Offer, birthday: date, config: RuleConfig) -> str | None:
    """Return why this offer is out, or None if it passes. The pot is checked later, on the best offer only."""
    if offer.price_cents is None:
        return "price unknown"
    if offer.shipping_cents is None:
        return "shipping cost unknown"
    # The latest date the merchant states, never the earliest. With deliveryStatus "UNKNOWN" it is null.
    if offer.late_delivery is None:
        return "no delivery date"
    needed_by = birthday - timedelta(days=config.arrival_buffer_days)
    if offer.late_delivery > needed_by:
        return f"arrives by {format_day(offer.late_delivery)}, needed by {format_day(needed_by)}"
    if offer.shop_rating is None:
        return None if config.allow_unrated_merchants else "merchant has no rating"
    if offer.shop_rating < config.min_shop_rating:
        return f"merchant rated {offer.shop_rating:g} of 5, minimum is {config.min_shop_rating:g}"
    return None


@dataclass(frozen=True)
class Verdict:
    """The result for one observation: on the list (ok) or dropped, with the reason and the facts to show."""

    observation_id: object
    ok: bool
    reason: str | None
    product_name: str | None
    offer: Offer | None
    missing_cents: int | None
    # The product's lowest price in idealo's price history (all shops), not a fact about the chosen offer.
    product_low_cents: int | None


def _sort_key(offer: Offer) -> tuple[bool, int]:
    """Cheapest total first; offers without a known total go last."""
    total = offer.total_cents
    return (total is None, total or 0)


def _best_key(offer: Offer) -> tuple[bool, int]:
    """Among offers that pass: rated merchants first, then the lowest total."""
    return (offer.shop_rating is None, offer.total_cents or 0)


def decide_entry(
    entry: dict, birthday: date, pot_cents: int, config: RuleConfig | None = None
) -> Verdict:
    """Pick the best offer that arrives in time from an accepted merchant, then compare it with the pot.

    Best: a rated merchant before an unrated one, then the lowest total (price + shipping).
    """
    config = config or RuleConfig()
    product = entry.get("product") if isinstance(entry.get("product"), dict) else {}
    name = product.get("name") if isinstance(product.get("name"), str) else None

    def dropped(reason: str, offer: Offer | None = None, missing: int | None = None) -> Verdict:
        return Verdict(entry.get("observation_id"), False, reason, name, offer, missing, None)

    skipped = entry.get("skipped_reason")
    if isinstance(skipped, str) and skipped.strip():
        return dropped(f"not searched: {skipped.strip()}")

    raw_offers = entry.get("offers") if isinstance(entry.get("offers"), list) else []
    offers = sorted(
        (offer_from_contract(raw) for raw in raw_offers if isinstance(raw, dict)), key=_sort_key
    )
    if not offers:
        return dropped("no offer found")

    passing = [offer for offer in offers if check_offer(offer, birthday, config) is None]
    if not passing:
        return dropped(
            f"no offer passes; the cheapest one: {check_offer(offers[0], birthday, config)}"
        )

    best = min(passing, key=_best_key)
    total = best.total_cents
    if total > pot_cents:
        missing = total - pot_cents
        reason = (
            f"cheapest offer that passes costs {format_eur(total)}, "
            f"the pot is {format_eur(pot_cents)} ({format_eur(missing)} missing)"
        )
        return dropped(reason, best, missing)

    stats = entry.get("price_stats") if isinstance(entry.get("price_stats"), dict) else {}
    low_cents = parse_eur_cents(stats.get("low_text"))
    return Verdict(entry.get("observation_id"), True, None, name, best, None, low_cents)
