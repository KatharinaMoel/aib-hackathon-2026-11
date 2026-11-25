"""Stub signal for the skeleton: the homepage answered, and its title. Replace or extend on the day."""

import re

from taste.models import Fact, Page, SignalResult


def homepage(page: Page, fetcher) -> SignalResult:
    """Two facts from the vendor's own homepage: it answered, and what it calls itself."""
    result = SignalResult()
    result.facts.append(
        Fact(
            claim=f"The homepage answered with HTTP {page.status}.",
            axis="looks",
            direction="pro" if page.status == 200 else "con",
            kind="measurement",
            url=page.url,
            tier="vendor_self",
            fetched_at=page.fetched_at,
            measurement={"method": "HTTP GET", "value": page.status},
        )
    )
    first_words = " ".join(page.text.split()[:12])
    if first_words:
        result.facts.append(
            Fact(
                claim="The homepage describes the product (vendor's own words).",
                axis="looks",
                direction="pro",
                kind="quote",
                url=page.url,
                tier="vendor_self",
                fetched_at=page.fetched_at,
                quote=re.sub(r"\s+", " ", first_words),
            )
        )
    return result
