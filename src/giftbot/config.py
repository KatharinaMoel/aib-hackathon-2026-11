"""The numbers the team decides: how early a gift must arrive and which merchants we accept.

What for: one place for the defaults of rules.py, so a rule change is one line and needs no search.
Who reads it: the team when it sets a threshold; rules.py imports it.
How to change: edit a default below by PR and adjust the test in tests/test_rules.py that names it.
These defaults are a proposal (docs/GIFT_BOT.md, "Rules the code applies").
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleConfig:
    """Thresholds for one wishlist run. Frozen: a run cannot change them halfway."""

    # The latest delivery date the merchant states must be at least this many days before the birthday.
    arrival_buffer_days: int = 2
    # Lowest accepted average merchant rating. idealo's scale goes up to 5 (seen in an offers response,
    # 27 Nov 2026).
    min_shop_rating: float = 4.0
    # Most offers on idealo.it carry `shop.rating` {count: null, avg: null} (seen 27 Nov 2026). True: keep such
    # offers and show them as "unrated shop"; a rated offer that passes is still preferred. False: drop them.
    allow_unrated_merchants: bool = True
