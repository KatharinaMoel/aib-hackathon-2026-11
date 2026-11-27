"""Split the price of a gift between friends who each named a private limit.

What for: every friend tells the bot the most they would chip in. This module says who pays how much for one
gift, so that the shares add up to the price and nobody pays more than their limit.
Who reads it: whoever changes the split rule, and the bot code that shows the shares.
How to change: the rule is "in proportion to each limit". Another rule (for example equal shares with caps)
gets its own function and its own tests in tests/test_split.py.
All amounts are whole cents, so no rounding error can add or lose a cent.
"""


def pot_cents(limits_cents: dict[str, int]) -> int:
    """The pot: the sum of all limits. Negative entries count as zero."""
    return sum(max(limit, 0) for limit in limits_cents.values())


def split_shares(total_cents: int, limits_cents: dict[str, int]) -> dict[str, int] | None:
    """Share `total_cents` in proportion to each limit. None if the pot does not cover the total.

    Example: limits 50 € and 150 €, gift 100 € -> 25 € and 75 €.
    Cents that do not divide evenly go to the people with the largest remainder, one cent each.
    """
    limits = {name: max(limit, 0) for name, limit in limits_cents.items()}
    pot = sum(limits.values())
    if total_cents < 0 or pot == 0 or total_cents > pot:
        return None

    shares = {name: total_cents * limit // pot for name, limit in limits.items()}
    left_over = total_cents - sum(shares.values())
    # A person with remainder 0 never gets an extra cent, so no share can pass its limit.
    by_remainder = sorted(limits, key=lambda name: (-(total_cents * limits[name] % pot), name))
    for name in by_remainder[:left_over]:
        shares[name] += 1
    return shares
