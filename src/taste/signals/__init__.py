"""Signals: each module checks one thing and returns facts with links (docs/SIGNALS.md).

A signal is a function `(page, fetcher) -> SignalResult`. Add it to SIGNALS below; one signal per PR.
"""

from taste.signals.homepage import homepage

SIGNALS = [homepage]
