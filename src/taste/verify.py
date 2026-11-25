"""Check that a quoted fact really is on the page we fetched. Code sets `verification`, never the LLM."""

import re
import unicodedata

from taste.models import Fact, Page


def _normalize(text: str) -> str:
    """Same text, other spelling: Unicode form, non-breaking spaces, line breaks, case."""
    text = unicodedata.normalize("NFKC", text).replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip().casefold()


def verify(fact: Fact, pages: dict[str, Page]) -> str:
    """Return exact | normalized | measured | absent. A reason with `absent` is dropped."""
    if fact.kind == "measurement":
        return "measured"
    page = pages.get(fact.url)
    if page is None or not fact.quote:
        return "absent"
    if fact.quote in page.text:
        return "exact"
    if _normalize(fact.quote) in _normalize(page.text):
        return "normalized"
    return "absent"
