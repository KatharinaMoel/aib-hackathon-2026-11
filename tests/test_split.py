"""Tests for src/giftbot/split.py: who pays how much.

What for: the shares must add up to the price to the cent, and nobody may pay more than their limit. Names and
amounts are made up.
How to change: a new split rule gets its own tests here, including the edge cases at the bottom.
"""

from itertools import product

from giftbot.split import pot_cents, split_shares


def test_pot_is_the_sum_of_the_limits():
    assert pot_cents({"a": 5000, "b": 15000}) == 20000
    assert pot_cents({"a": 5000, "b": -100}) == 5000
    assert pot_cents({}) == 0


def test_shares_follow_the_limits():
    assert split_shares(10000, {"a": 5000, "b": 15000}) == {"a": 2500, "b": 7500}


def test_left_over_cents_are_spread_one_each():
    shares = split_shares(1000, {"a": 1000, "b": 1000, "c": 1000})
    assert shares == {"a": 334, "b": 333, "c": 333}


def test_small_and_large_limit_at_full_pot():
    assert split_shares(20500, {"a": 500, "b": 20000}) == {"a": 500, "b": 20000}


def test_price_above_the_pot_gives_no_split():
    assert split_shares(20501, {"a": 500, "b": 20000}) is None


def test_no_pledges_or_only_zero_pledges_give_no_split():
    assert split_shares(1000, {}) is None
    assert split_shares(1000, {"a": 0}) is None


def test_someone_with_limit_zero_pays_nothing():
    assert split_shares(999, {"a": 0, "b": 1000, "c": 1000}) == {"a": 0, "b": 500, "c": 499}


def test_free_gift_costs_nobody_anything():
    assert split_shares(0, {"a": 500, "b": 700}) == {"a": 0, "b": 0}


def test_every_split_adds_up_and_respects_the_limits():
    amounts = (1, 333, 500, 1999, 20000)
    for limits in product(amounts, repeat=3):
        named = dict(zip("abc", limits, strict=True))
        pot = sum(limits)
        for total in (t for t in (1, 7, 100, 1001, pot - 1, pot) if t <= pot):
            shares = split_shares(total, named)
            assert sum(shares.values()) == total
            assert all(shares[name] <= named[name] for name in named)
