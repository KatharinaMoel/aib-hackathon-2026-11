"""Tests for src/giftbot/wishlist.py: the list text the group sees. Products and shops are made up."""

from datetime import date

from giftbot.state import Store
from giftbot.wishlist import changes_note, format_wishlist, header, split_message


def make_round():
    store = Store()
    round_ = store.start(-10, "Lena", date(2026, 12, 5))
    store.add_observation(-10, "Jonas", "her headphones are ancient")
    store.add_observation(-10, "Mia", "she started climbing")
    store.add_observation(-10, "Tom", "she is stressed")
    store.pledge(-10, 1, "Jonas", 5000)
    store.pledge(-10, 2, "Mia", 3000)
    return round_


def offer(price, shipping="0,00 €", late="2026-12-02", rating=4.6):
    return {
        "price_text": price,
        "shipping_text": shipping,
        "late_delivery_date": late,
        "shop_name": "Shop A",
        "shop_rating": rating,
        "is_marketplace": False,
        "payments": ["PP"],
        "url": "https://example.invalid/offer",
    }


AGENT_OUTPUT = {
    "entries": [
        {
            "observation_id": 1,
            "skipped_reason": None,
            "product": {"name": "Example Headphones 5", "productRef": "r1"},
            "offers": [offer("70,00 €")],
            "price_stats": {"low_text": "62,00 €", "low_date": "2026-11-20"},
        },
        {
            "observation_id": 2,
            "skipped_reason": None,
            "product": {"name": "Example Chalk Bag", "productRef": "r2"},
            "offers": [offer("70,00 €", shipping="20,00 €")],
            "price_stats": None,
        },
    ]
}


def test_header_shows_weekday_and_pot_but_no_single_pledge():
    assert (
        header(make_round()) == "Wishlist for Lena · birthday Sat 5 Dec · pot €80.00 (2 answered)"
    )


def test_list_has_one_block_per_observation_in_order():
    text = format_wishlist(make_round(), AGENT_OUTPUT)
    blocks = text.split("\n\n")
    assert len(blocks) == 4

    assert blocks[1].startswith('✔ Example Headphones 5 · from Jonas: "her headphones are ancient"')
    assert "€70.00 with shipping · arrives by 2 Dec · merchant 4.6" in blocks[1]
    assert "today €8.00 above the 30-day low" in blocks[1]
    # €70.00 split by limits €50 and €30: €43.75 and €26.25.
    assert "shares €26.25 to €43.75" in blocks[1]

    assert blocks[2].startswith("✘ Example Chalk Bag")
    assert "costs €90.00, the pot is €80.00 (€10.00 missing)" in blocks[2]

    assert (
        blocks[3] == '✘ from Tom: "she is stressed"\n  dropped: the agent returned nothing for it'
    )


def test_list_uses_the_round_as_it_was_when_the_run_started():
    # Bug seen on 27 Nov: an idea added during the run showed "the agent returned nothing for it",
    # and the verdicts used a pot that had grown during the run.
    round_ = make_round()
    checked = round_.snapshot()
    round_.observations.append(type(round_.observations[0])(4, "Ana", "she needs a coffee machine"))
    round_.pledges[3] = type(round_.pledges[1])("Ana", 2000)

    text = format_wishlist(checked, AGENT_OUTPUT)
    assert "coffee machine" not in text
    assert "pot €80.00 (2 answered)" in text
    note = changes_note(checked, round_)
    assert "1 idea(s) added during the check are not in this list" in note
    assert "the pot is now €100.00; this list used €80.00" in note
    assert changes_note(checked, checked.snapshot()) is None


def test_split_message_keeps_parts_under_the_limit():
    text = "\n".join(f"line {i:03d}" for i in range(100))
    parts = split_message(text, limit=50)
    assert all(len(p) <= 50 for p in parts)
    assert "\n".join(parts) == text
    assert split_message("x" * 120, limit=50) == ["x" * 50, "x" * 50, "x" * 20]
