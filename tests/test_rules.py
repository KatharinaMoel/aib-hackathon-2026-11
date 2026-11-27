"""Tests for src/giftbot/rules.py: price parsing and the verdict per observation.

What for: every rule that decides about money or dates is checked here without network or model (AGENTS.md,
rule 12). Shops, products and prices below are made up.
How to change: a new rule in rules.py gets a test here that fails without the rule.
"""

from datetime import date

import pytest

from giftbot.config import RuleConfig
from giftbot.rules import (
    check_offer,
    decide_entry,
    format_day,
    format_eur,
    offer_from_contract,
    offer_from_mcp,
    parse_day,
    parse_eur_cents,
)

BIRTHDAY = date(2026, 12, 5)


def offer(price="20,00 €", shipping="4,00 €", late="2026-12-02", rating=4.6, name="Shop A"):
    """One offer in the contract format (docs/GIFT_BOT.md); every argument can be overridden."""
    return {
        "price_text": price,
        "shipping_text": shipping,
        "late_delivery_date": late,
        "shop_name": name,
        "shop_rating": rating,
        "is_marketplace": False,
        "payments": ["PP", "INV"],
        "url": "https://example.invalid/offer",
    }


def entry(*offers, **extra):
    """One entry of an agent run with the given offers."""
    base = {
        "observation_id": 1,
        "kind": "does",
        "mode": "type_search",
        "query": "Chalkbag",
        "skipped_reason": None,
        "product": {"name": "Example Chalk Bag", "productRef": "ref-1"},
        "offers": list(offers),
        "price_stats": {"low_text": "18,50 €", "low_date": "2026-11-20"},
    }
    return base | extra


@pytest.mark.parametrize(
    ("text", "cents"),
    [
        ("1.059,00 €", 105900),
        ("10,19 €", 1019),
        ("0,00 €", 0),
        ("12 €", 1200),
        ("12,5 €", 1250),
        (f"1.234.567,89{chr(0xA0)}€", 123456789),
        ("kostenlos", None),
        ("1,059.00", None),
        ("", None),
        (None, None),
        (1019, None),
    ],
)
def test_parse_eur_cents(text, cents):
    assert parse_eur_cents(text) == cents


def test_format_eur_and_day():
    assert format_eur(105900) == "€1,059.00"
    assert format_eur(5) == "€0.05"
    assert format_day(date(2026, 12, 3)) == "3 Dec"


def test_parse_day_reads_date_and_timestamp():
    assert parse_day("2026-12-03") == date(2026, 12, 3)
    assert parse_day("2026-12-03T10:00:00Z") == date(2026, 12, 3)
    assert parse_day("next week") is None
    assert parse_day(None) is None


def test_total_is_price_plus_shipping_and_unknown_stays_unknown():
    assert offer_from_contract(offer()).total_cents == 2400
    assert offer_from_contract(offer(shipping=None)).total_cents is None


def test_offer_from_mcp_reads_the_nested_idealo_fields():
    raw = {
        "price": "10,19 €",
        "minShippingCost": "3,99 €",
        "shop": {"name": "Shop A", "rating": {"count": 12, "avg": 4.4}, "isMarketplace": False},
        "payments": [{"costCode": "INV", "name": "Rechnung"}, {"costCode": "PP", "name": "PayPal"}],
        "delivery": {"lateDeliveryDate": "2026-12-03"},
        "relocatorUrl": "https://example.invalid/go",
    }
    parsed = offer_from_mcp(raw)
    assert parsed.total_cents == 1418
    assert parsed.late_delivery == date(2026, 12, 3)
    assert parsed.shop_rating == 4.4
    assert parsed.payments == ("INV", "PP")
    assert offer_from_mcp({}).total_cents is None


def test_check_offer_reasons():
    config = RuleConfig()
    assert check_offer(offer_from_contract(offer()), BIRTHDAY, config) is None
    assert check_offer(offer_from_contract(offer(price=None)), BIRTHDAY, config) == "price unknown"
    assert (
        check_offer(offer_from_contract(offer(shipping="?")), BIRTHDAY, config)
        == "shipping cost unknown"
    )
    assert (
        check_offer(offer_from_contract(offer(late=None)), BIRTHDAY, config) == "no delivery date"
    )
    assert (
        check_offer(offer_from_contract(offer(late="2026-12-04")), BIRTHDAY, config)
        == "arrives by 4 Dec, needed by 3 Dec"
    )
    assert (
        check_offer(offer_from_contract(offer(rating=1.4)), BIRTHDAY, config)
        == "merchant rated 1.4 of 5, minimum is 4"
    )


def test_arrival_exactly_on_the_buffer_day_passes():
    assert (
        check_offer(offer_from_contract(offer(late="2026-12-03")), BIRTHDAY, RuleConfig()) is None
    )


def test_unrated_merchant_passes():
    assert check_offer(offer_from_contract(offer(rating=None)), BIRTHDAY, RuleConfig()) is None


def test_cheapest_passing_offer_wins_over_cheaper_bad_ones():
    verdict = decide_entry(
        entry(
            offer(price="10,00 €", rating=1.4, name="Cheap but badly rated"),
            offer(price="11,00 €", late="2026-12-12", name="Cheap but late"),
            offer(price="20,00 €", name="Good"),
            offer(price="25,00 €", name="Good but dearer"),
        ),
        BIRTHDAY,
        pot_cents=6000,
    )
    assert verdict.ok
    assert verdict.offer.shop_name == "Good"
    assert verdict.offer.total_cents == 2400
    assert verdict.product_low_cents == 1850
    assert verdict.product_name == "Example Chalk Bag"


def test_over_the_pot_is_dropped_with_the_missing_amount():
    verdict = decide_entry(entry(offer(price="236,00 €")), BIRTHDAY, pot_cents=18000)
    assert not verdict.ok
    assert verdict.missing_cents == 6000
    assert verdict.reason == (
        "cheapest offer that passes costs €240.00, the pot is €180.00 (€60.00 missing)"
    )


def test_total_equal_to_the_pot_passes():
    assert decide_entry(entry(offer()), BIRTHDAY, pot_cents=2400).ok


def test_no_passing_offer_names_the_reason_of_the_cheapest():
    verdict = decide_entry(
        entry(offer(price="10,00 €", late="2026-12-12"), offer(price="30,00 €", rating=2.0)),
        BIRTHDAY,
        pot_cents=6000,
    )
    assert not verdict.ok
    assert verdict.reason == "no offer passes; the cheapest one: arrives by 12 Dec, needed by 3 Dec"


def test_skipped_and_empty_entries():
    skipped = decide_entry(
        entry(skipped_reason="needs her shoe size", product=None, offers=[]), BIRTHDAY, 6000
    )
    assert not skipped.ok
    assert skipped.reason == "not searched: needs her shoe size"
    assert decide_entry(entry(), BIRTHDAY, 6000).reason == "no offer found"
    assert decide_entry({}, BIRTHDAY, 6000).reason == "no offer found"


def test_missing_price_stats_gives_no_price_position():
    assert decide_entry(entry(offer(), price_stats=None), BIRTHDAY, 6000).product_low_cents is None


def test_threshold_comes_from_the_config():
    strict = RuleConfig(arrival_buffer_days=5, min_shop_rating=4.8)
    assert not decide_entry(entry(offer()), BIRTHDAY, 6000, strict).ok


# Offers shaped like `get_product_offers` on idealo.it (27 Nov 2026): most shops have
# shop.rating {count: null, avg: null}; some offers have deliveryStatus "UNKNOWN" and both dates null.
# Shop names and prices are made up.
def mcp_offer(
    price="39,20 €", shipping="0,00 €", avg=None, status="SHORT", late="2026-12-02", early=None
):
    count = None if avg is None else 25
    return {
        "price": price,
        "minShippingCost": shipping,
        "shop": {"name": "Shop IT", "rating": {"count": count, "avg": avg}, "isMarketplace": True},
        "payments": [{"costCode": "PP"}],
        "delivery": {
            "deliveryStatus": status,
            "earlyDeliveryDate": early,
            "lateDeliveryDate": late,
        },
        "relocatorUrl": "https://example.invalid/go",
    }


def test_null_rating_is_kept_and_marked_unrated_when_allowed():
    parsed = offer_from_mcp(mcp_offer(avg=None))
    assert parsed.shop_rating is None
    assert check_offer(parsed, BIRTHDAY, RuleConfig(allow_unrated_merchants=True)) is None


def test_null_rating_is_dropped_when_not_allowed():
    parsed = offer_from_mcp(mcp_offer(avg=None))
    config = RuleConfig(allow_unrated_merchants=False)
    assert check_offer(parsed, BIRTHDAY, config) == "merchant has no rating"


@pytest.mark.parametrize(
    ("avg", "reason"), [(3.6, "merchant rated 3.6 of 5, minimum is 4"), (4.5, None)]
)
def test_rating_below_the_minimum_is_dropped(avg, reason):
    assert check_offer(offer_from_mcp(mcp_offer(avg=avg)), BIRTHDAY, RuleConfig()) == reason


def test_unknown_delivery_with_null_dates_is_dropped_not_crashed():
    parsed = offer_from_mcp(mcp_offer(status="UNKNOWN", late=None, early=None))
    assert parsed.late_delivery is None
    assert check_offer(parsed, BIRTHDAY, RuleConfig()) == "no delivery date"


def test_arrival_uses_the_late_date_not_the_early_one():
    parsed = offer_from_mcp(mcp_offer(early="2026-12-01", late="2026-12-04"))
    assert check_offer(parsed, BIRTHDAY, RuleConfig()) == "arrives by 4 Dec, needed by 3 Dec"


def test_unknown_delivery_only_offer_drops_the_idea():
    verdict = decide_entry(entry(offer(late=None)), BIRTHDAY, pot_cents=8000)
    assert not verdict.ok
    assert verdict.reason == "no offer passes; the cheapest one: no delivery date"


def test_rated_passing_offer_is_chosen_over_a_cheaper_unrated_one():
    verdict = decide_entry(
        entry(
            offer(price="15,00 €", rating=None, name="Cheap unrated"),
            offer(price="20,00 €", rating=4.5, name="Rated"),
        ),
        BIRTHDAY,
        pot_cents=8000,
    )
    assert verdict.ok
    assert verdict.offer.shop_name == "Rated"


def test_unrated_offer_is_chosen_when_no_rated_offer_passes():
    verdict = decide_entry(
        entry(
            offer(price="15,00 €", rating=None, name="Unrated"),
            offer(price="12,00 €", rating=3.6, name="Badly rated"),
        ),
        BIRTHDAY,
        pot_cents=8000,
    )
    assert verdict.ok
    assert verdict.offer.shop_name == "Unrated"
    assert verdict.offer.shop_rating is None


def test_total_with_shipping_decides_not_the_price():
    verdict = decide_entry(
        entry(
            offer(price="39,20 €", shipping="17,54 €", name="Low price, high shipping"),
            offer(price="47,33 €", shipping="0,00 €", name="Free shipping"),
        ),
        BIRTHDAY,
        pot_cents=8000,
    )
    assert verdict.ok
    assert verdict.offer.shop_name == "Free shipping"
    assert verdict.offer.total_cents == 4733
