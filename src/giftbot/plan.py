"""Build the gift plan the bot posts after the list: what to buy, what is left over, when to order.

What for: the list shows every idea with ✔ or ✘. The plan picks from the ✔ entries, so the group gets one
proposal instead of a vote. The idea comes from the gift-pot draft (comment by rmohn-dev on PR #14,
27 Nov 2026): explicit wishes first, total prices with shipping, an order-by date, the money left over.
Who reads it: whoever changes how the plan is picked or shown; bot.py posts its output.
How to change: the pick is in build_plan(), the text in format_plan(). Every rule has a test in
tests/test_giftbot_plan.py. No network and no model here.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from giftbot.config import RuleConfig
from giftbot.rules import Offer, format_day, format_eur
from giftbot.state import Observation, Round
from giftbot.wishlist import Decided

# The kind the skill `observation-to-gift` gives to a wish the person said out loud. These go first.
EXPLICIT_WISH = "said"
_LINK_STARTS = ("https://", "http://")


@dataclass(frozen=True)
class PlanItem:
    """One product on the plan, with the offer rules.decide_entry() picked for it."""

    observation: Observation
    product_name: str
    offer: Offer
    offer_count: int  # how many offers the agent copied; 1 means the price rests on one merchant


@dataclass(frozen=True)
class GiftPlan:
    """What the group buys with the pot. All amounts are whole cents."""

    items: tuple[PlanItem, ...]
    pot_cents: int
    total_cents: int
    needed_by: date
    order_by: date

    @property
    def left_over_cents(self) -> int:
        return self.pot_cents - self.total_cents


def _kind(entry: dict | None) -> object:
    return entry.get("kind") if isinstance(entry, dict) else None


def _offer_count(entry: dict | None) -> int:
    offers = entry.get("offers") if isinstance(entry, dict) else None
    return len(offers) if isinstance(offers, list) else 0


def build_plan(
    round_: Round, decided: list[Decided], read_on: date, config: RuleConfig | None = None
) -> GiftPlan | None:
    """Pick the ✔ entries the pot pays for together. None if no entry is on the list.

    Order: explicit wishes (`kind` "said") first, then the order of the observations. An entry joins the plan
    while the sum of the total prices stays within the pot; an entry that does not fit is left out.

    Order-by date: the offers were read on `read_on` and promise arrival by their late delivery date. Between
    the latest of these dates and the day the gift is needed lie some spare days. The group can wait that many
    days before it orders. This holds only if a merchant's delivery time stays the same on a later day, which
    we could not verify (docs/GIFT_BOT.md, "Not verified"); the text of the plan says so.
    """
    config = config or RuleConfig()
    passing = [d for d in decided if d.verdict is not None and d.verdict.ok and d.verdict.offer]
    passing.sort(key=lambda d: _kind(d.entry) != EXPLICIT_WISH)  # stable: keeps the given order

    items: list[PlanItem] = []
    total = 0
    for d in passing:
        offer = d.verdict.offer
        cost = offer.total_cents
        if cost is None or offer.late_delivery is None or total + cost > round_.pot_cents:
            continue
        name = d.verdict.product_name or "Product without a name"
        items.append(PlanItem(d.observation, name, offer, _offer_count(d.entry)))
        total += cost
    if not items:
        return None

    needed_by = round_.birthday - timedelta(days=config.arrival_buffer_days)
    latest_arrival = max(item.offer.late_delivery for item in items)
    spare_days = max((needed_by - latest_arrival).days, 0)
    return GiftPlan(
        items=tuple(items),
        pot_cents=round_.pot_cents,
        total_cents=total,
        needed_by=needed_by,
        order_by=read_on + timedelta(days=spare_days),
    )


def _item_lines(number: int, item: PlanItem) -> list[str]:
    offer = item.offer
    shop = offer.shop_name or "a merchant without a name"
    lines = [
        f"{number}. {item.product_name} at {shop}, {format_eur(offer.total_cents)} with shipping, "
        f"arrives by {format_day(offer.late_delivery)}"
    ]
    # Text from idealo is data: only a web link is posted as a link.
    if offer.url and offer.url.startswith(_LINK_STARTS):
        lines.append(f"   {offer.url}")
    if item.offer_count == 1:
        lines.append("   only one merchant found for this product")
    return lines


def format_plan(round_: Round, plan: GiftPlan, read_on: date) -> str:
    """The plan as one chat message. Every number comes from the offers read on `read_on`."""
    lines = [
        f"🎁 Gift plan for {round_.person}",
        f"Pot: {format_eur(plan.pot_cents)}",
        "",
        "Buying:",
    ]
    for number, item in enumerate(plan.items, start=1):
        lines += _item_lines(number, item)
    lines += [
        "",
        f"Left over: {format_eur(plan.left_over_cents)}",
        f"Must arrive by: {format_day(plan.needed_by)}",
        f"Order by: {format_day(plan.order_by)} (if the delivery time stays as stated today)",
    ]
    if round_.organizer:
        lines.append(
            f"{round_.organizer}, you place the order. I collect no money and order nothing."
        )
    lines.append(f"Prices from idealo, {format_day(read_on)} {read_on.year}.")
    return "\n".join(lines)
