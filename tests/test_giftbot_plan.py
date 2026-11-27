"""Tests for src/giftbot/plan.py: which ✔ entries make the gift plan, and the text the group sees.

Products, shops and prices are made up. No Telegram, no Claude, no network.
"""

from datetime import date

from giftbot.plan import build_plan, format_plan
from giftbot.state import Store
from giftbot.wishlist import decide_round

READ_ON = date(2026, 11, 27)


def make_round(*pledges_cents):
    store = Store()
    round_ = store.start(-10, "Lena", date(2026, 12, 5), organizer="Jonas")
    store.add_observation(-10, "Jonas", "she started climbing")
    store.add_observation(-10, "Mia", "she said she would love a record player")
    store.add_observation(-10, "Tom", "her coffee grinder annoys her")
    for user_id, cents in enumerate(pledges_cents, start=1):
        store.pledge(-10, user_id, f"Friend {user_id}", cents)
    return round_


def offer(price, late="2026-12-01", shop="Shop A", url="https://example.invalid/offer"):
    return {
        "price_text": price,
        "shipping_text": "0,00 €",
        "late_delivery_date": late,
        "shop_name": shop,
        "shop_rating": 4.6,
        "is_marketplace": False,
        "payments": ["PP"],
        "url": url,
    }


def entry(observation_id, kind, name, *offers):
    return {
        "observation_id": observation_id,
        "kind": kind,
        "skipped_reason": None,
        "product": {"name": name, "productRef": f"r{observation_id}"},
        "offers": list(offers),
        "price_stats": None,
    }


def plan_for(round_, *entries):
    return build_plan(round_, decide_round(round_, {"entries": list(entries)}), READ_ON)


def test_an_explicit_wish_comes_first_even_when_it_was_written_later():
    round_ = make_round(10000)
    plan = plan_for(
        round_,
        entry(1, "does", "Example Chalk Bag", offer("20,00 €"), offer("25,00 €")),
        entry(2, "said", "Example Record Player", offer("70,00 €"), offer("75,00 €")),
    )
    assert [item.product_name for item in plan.items] == [
        "Example Record Player",
        "Example Chalk Bag",
    ]
    assert plan.total_cents == 9000
    assert plan.left_over_cents == 1000


def test_an_entry_that_no_longer_fits_the_pot_is_left_out_and_a_smaller_one_still_joins():
    round_ = make_round(10000)
    plan = plan_for(
        round_,
        entry(1, "does", "Example Chalk Bag", offer("60,00 €")),
        entry(2, "said", "Example Record Player", offer("70,00 €")),
        entry(3, "complains", "Example Coffee Grinder", offer("30,00 €")),
    )
    # €70 first (explicit wish). €60 would make €130, over the pot of €100. €30 fits: €100.
    assert [item.product_name for item in plan.items] == [
        "Example Record Player",
        "Example Coffee Grinder",
    ]
    assert plan.left_over_cents == 0


def test_no_plan_when_nothing_is_on_the_list():
    round_ = make_round(1000)
    assert plan_for(round_, entry(1, "does", "Example Chalk Bag", offer("20,00 €"))) is None
    assert plan_for(round_) is None


def test_order_by_moves_the_reading_day_by_the_spare_days_of_the_slowest_offer():
    round_ = make_round(10000)
    plan = plan_for(
        round_,
        entry(1, "does", "Example Chalk Bag", offer("20,00 €", late="2026-11-30")),
        entry(2, "said", "Example Record Player", offer("70,00 €", late="2026-12-01")),
    )
    # Birthday 5 Dec, 2 buffer days: needed by 3 Dec. Slowest offer arrives by 1 Dec: 2 spare days.
    assert plan.needed_by == date(2026, 12, 3)
    assert plan.order_by == date(2026, 11, 29)


def test_order_by_is_the_reading_day_when_the_offer_has_no_spare_day():
    round_ = make_round(10000)
    plan = plan_for(
        round_, entry(1, "does", "Example Chalk Bag", offer("20,00 €", late="2026-12-03"))
    )
    assert plan.order_by == READ_ON


def test_a_pledge_of_zero_adds_nothing_to_the_pot_of_the_plan():
    round_ = make_round(5000, 0)
    plan = plan_for(round_, entry(1, "does", "Example Chalk Bag", offer("20,00 €")))
    assert plan.pot_cents == 5000
    assert plan.left_over_cents == 3000


def test_plan_text_names_pot_total_dates_organizer_and_the_day_of_the_prices():
    round_ = make_round(6000, 4000)
    plan = plan_for(
        round_,
        entry(
            2, "said", "Example Record Player", offer("70,00 €"), offer("75,00 €", shop="Shop B")
        ),
    )
    assert format_plan(round_, plan, READ_ON) == "\n".join(
        [
            "🎁 Gift plan for Lena",
            "Pot: €100.00",
            "",
            "Buying:",
            "1. Example Record Player at Shop A, €70.00 with shipping, arrives by 1 Dec",
            "   https://example.invalid/offer",
            "",
            "Left over: €30.00",
            "Must arrive by: 3 Dec",
            "Order by: 29 Nov (if the delivery time stays as stated today)",
            "Jonas, you place the order. I collect no money and order nothing.",
            "Prices from idealo, 27 Nov 2026.",
        ]
    )


def test_plan_text_says_when_a_price_rests_on_one_merchant_and_posts_only_web_links():
    round_ = make_round(10000)
    plan = plan_for(
        round_,
        entry(1, "does", "Example Chalk Bag", offer("20,00 €", url="javascript:alert(1)")),
    )
    text = format_plan(round_, plan, READ_ON)
    assert "only one merchant found for this product" in text
    assert "javascript" not in text


def test_plan_text_never_names_a_single_pledge():
    round_ = make_round(6000, 4000, 0)
    plan = plan_for(round_, entry(1, "does", "Example Chalk Bag", offer("20,00 €")))
    text = format_plan(round_, plan, READ_ON)
    assert "€60.00" not in text
    assert "€40.00" not in text
    assert "Friend" not in text
