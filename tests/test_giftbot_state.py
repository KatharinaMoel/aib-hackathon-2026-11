"""Tests for src/giftbot/state.py: command arguments, amounts, pledge links and the round store.

No Telegram, no network. Names and amounts are made up.
"""

from datetime import date

import pytest

from giftbot.state import (
    Store,
    parse_amount_cents,
    parse_pledge_payload,
    parse_round_args,
    pledge_payload,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Lena 2026-12-05", ("Lena", date(2026, 12, 5))),
        ("Lena Maria 2026-12-05", ("Lena Maria", date(2026, 12, 5))),
        ("Lena", None),
        ("Lena 5.12.2026", None),
        ("", None),
    ],
)
def test_parse_round_args(text, expected):
    assert parse_round_args(text) == expected


@pytest.mark.parametrize(
    ("text", "cents"),
    [
        ("50", 5000),
        ("50,5", 5050),
        ("50.50", 5050),
        ("€50", 5000),
        ("50 €", 5000),
        ("0", None),
        ("-5", None),
        ("fifty", None),
        ("99999", None),
    ],
)
def test_parse_amount_cents(text, cents):
    assert parse_amount_cents(text) == cents


def test_pledge_payload_round_trip_for_negative_group_id():
    payload = pledge_payload(-1001234567890)
    assert len(payload) <= 64
    assert parse_pledge_payload(payload) == -1001234567890


@pytest.mark.parametrize("payload", ["", "pledge_", "pledge_abc", "other_123"])
def test_parse_pledge_payload_rejects_other_text(payload):
    assert parse_pledge_payload(payload) is None


def test_store_collects_observations_and_pledges():
    store = Store()
    store.start(-10, "Lena", date(2026, 12, 5))
    assert store.add_observation(-10, "Jonas", "  her headphones are ancient ").id == 1
    assert store.add_observation(-10, "Mia", "she started climbing").id == 2
    store.pledge(-10, 1, "Jonas", 5000)
    store.pledge(-10, 2, "Mia", 3000)
    store.pledge(-10, 1, "Jonas", 6000)  # a second pledge replaces the first

    round_ = store.get(-10)
    assert round_.pot_cents == 9000
    assert round_.agent_input() == {
        "person": "Lena",
        "birthday": "2026-12-05",
        "pot_eur": 90,
        "country": "DE",
        "observations": [
            {"id": 1, "from": "Jonas", "text": "her headphones are ancient"},
            {"id": 2, "from": "Mia", "text": "she started climbing"},
        ],
    }


def test_store_without_round_or_text_adds_nothing():
    store = Store()
    assert store.add_observation(-10, "Jonas", "anything") is None
    assert store.pledge(-10, 1, "Jonas", 5000) is None
    store.start(-10, "Lena", date(2026, 12, 5))
    assert store.add_observation(-10, "Jonas", "   ") is None


def test_same_first_names_keep_separate_limits():
    store = Store()
    store.start(-10, "Lena", date(2026, 12, 5))
    store.pledge(-10, 1, "Alex", 5000)
    store.pledge(-10, 2, "Alex", 3000)
    assert sorted(store.get(-10).limits_cents().values()) == [3000, 5000]
