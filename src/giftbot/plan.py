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


def _product_ref(entry: dict | None) -> object:
    product = entry.get("product") if isinstance(entry, dict) else None
    return product.get("productRef") if isinstance(product, dict) else None


def _one_line(text: str) -> str:
    """Text from idealo is data: a line break in a name must not write its own line into the plan."""
    return " ".join(text.split())


def _web_link(url: str | None) -> str | None:
    """Only a web address without any white space is posted as a link."""
    if not url or not url.startswith(_LINK_STARTS) or url != "".join(url.split()):
        return None
    return url


def build_plan(
    round_: Round, decided: list[Decided], read_on: date, config: RuleConfig | None = None
) -> GiftPlan | None:
    """Pick the ✔ entries the pot pays for together. None if no entry is on the list.

    Order: explicit wishes (`kind` "said") first, then the highest total price first, so the main gift is
    picked before the small ones. An entry joins the plan while the sum of the total prices stays within the
    pot; an entry that does not fit is left out, and so is a product that is already on the plan. This order
    is a proposal (docs/GIFT_BOT.md, "Rules from the gift-pot draft"); the team has not set it.

    An offer whose late delivery date lies before `read_on` is left out: that date is stale or mistyped.

    Order-by date: the offers were read on `read_on` and promise arrival by their late delivery date. Between
    the latest of these dates and the day the gift is needed lie some spare days. The group can wait that many
    days before it orders. This holds only if a merchant's delivery time stays the same on a later day, which
    we could not verify (docs/GIFT_BOT.md, "Not verified"); the text of the plan says so. No late delivery
    date on the plan lies before `read_on`, so the order-by date is never later than the day the gift is needed.
    """
    config = config or RuleConfig()
    passing = [d for d in decided if d.verdict is not None and d.verdict.ok and d.verdict.offer]
    # Stable sort: entries with the same key keep the order of the observations.
    passing.sort(
        key=lambda d: (_kind(d.entry) != EXPLICIT_WISH, -(d.verdict.offer.total_cents or 0))
    )

    items: list[PlanItem] = []
    total = 0
    seen_refs: set[str] = set()
    for d in passing:
        offer = d.verdict.offer
        cost = offer.total_cents
        if cost is None or offer.late_delivery is None or total + cost > round_.pot_cents:
            continue
        if offer.late_delivery < read_on:
            continue
        ref = _product_ref(d.entry)
        if isinstance(ref, str) and ref in seen_refs:
            continue
        if isinstance(ref, str):
            seen_refs.add(ref)
        name = _one_line(d.verdict.product_name or "") or "Product without a name"
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
    shop = _one_line(offer.shop_name or "") or "a merchant without a name"
    lines = [
        f"{number}. {item.product_name} at {shop}, {format_eur(offer.total_cents)} with shipping, "
        f"arrives by {format_day(offer.late_delivery)} if ordered today"
    ]
    link = _web_link(offer.url)
    if link:
        lines.append(f"   {link}")
    if item.offer_count == 1:
        lines.append("   only one offer found for this product")
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
    lines.append(f"Prices read from idealo on {format_day(read_on)} {read_on.year} (UTC).")
    return "\n".join(lines)
