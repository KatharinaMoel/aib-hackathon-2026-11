"""Data shapes shared by every module. They mirror schema/verdict.schema.json."""

from dataclasses import dataclass, field


@dataclass
class Page:
    """One fetched page. `text` is the visible text; scripts and styles are removed."""

    url: str
    status: int
    text: str
    fetched_at: str
    sha256: str


@dataclass
class Fact:
    """One thing a signal found, with the link a person can open. The judge cites it by `fact_id`."""

    claim: str
    axis: str  # looks | substance | risk
    direction: str  # pro | con
    kind: str  # quote | measurement
    url: str
    tier: str  # independent | vendor_self
    fetched_at: str
    quote: str = ""
    measurement: dict | None = None
    fact_id: str = ""  # set by the pipeline: F1, F2, …
    verification: str = ""  # set by code: exact | normalized | measured | absent


@dataclass
class SignalResult:
    """What one signal returns: facts, and what it tried but could not check."""

    facts: list[Fact] = field(default_factory=list)
    not_checked: list[dict] = field(default_factory=list)  # {"signal": …, "why": …}
