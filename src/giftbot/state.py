"""What the bot remembers about each group's gift round: person, birthday, observations, private pledges.

What for: the Telegram handlers in bot.py read and write rounds only through this module, so the logic can be
tested without Telegram (tests/test_giftbot_state.py).
Who reads it: whoever changes a bot command; bot.py and wishlist.py import it.
How to change: keep it free of network and Telegram types. State lives in memory: a restart forgets all
rounds (docs/GIFT_BOT.md, "The contract", has no storage yet).
"""

import re
from dataclasses import dataclass, field
from datetime import date

# "50", "50,5", "50.50", "€50", "50 €" - a whole-euro or euro-and-cents amount.
_AMOUNT = re.compile(r"^\s*(?:€|EUR)?\s*(\d{1,5})(?:[.,](\d{1,2}))?\s*(?:€|EUR|eur|euro)?\s*$")
# The highest pledge we accept from one person, in cents (a typo guard, not a business rule).
MAX_PLEDGE_CENTS = 1_000_000
# Deep-link payload for a private pledge: "pledge_<group chat id>". Telegram allows A-Z a-z 0-9 _ - here.
_PLEDGE_PAYLOAD = re.compile(r"^pledge_(-?\d{1,20})$")


def parse_round_args(text: str) -> tuple[str, date] | None:
    """Read "/gift Lena 2026-12-05" arguments: a name (may contain spaces) and an ISO date at the end."""
    parts = text.split()
    if len(parts) < 2:
        return None
    try:
        birthday = date.fromisoformat(parts[-1])
    except ValueError:
        return None
    return " ".join(parts[:-1]), birthday


def parse_amount_cents(text: str) -> int | None:
    """Turn "50", "50,5" or "€50" into cents. Zero, negative, too large or unreadable is None."""
    match = _AMOUNT.match(text)
    if match is None:
        return None
    cents = int(match.group(1)) * 100 + int((match.group(2) or "0").ljust(2, "0"))
    if cents <= 0 or cents > MAX_PLEDGE_CENTS:
        return None
    return cents


def pledge_payload(group_chat_id: int) -> str:
    """The payload for the "pledge in private" button of one group."""
    return f"pledge_{group_chat_id}"


def parse_pledge_payload(payload: str) -> int | None:
    """Read the group chat id back from a /start payload; anything else is None."""
    match = _PLEDGE_PAYLOAD.match(payload.strip())
    return int(match.group(1)) if match else None


@dataclass(frozen=True)
class Observation:
    """One thing a friend noticed about the person, as written in the group."""

    id: int
    author: str
    text: str


@dataclass(frozen=True)
class Pledge:
    """The most one friend would chip in. Only the bot sees the amount; the group sees the pot."""

    name: str
    cents: int


@dataclass
class Round:
    """One gift round in one group chat."""

    chat_id: int
    person: str
    birthday: date
    country: str = "DE"
    observations: list[Observation] = field(default_factory=list)
    pledges: dict[int, Pledge] = field(default_factory=dict)  # key: Telegram user id

    @property
    def pot_cents(self) -> int:
        """The sum of all pledges."""
        return sum(p.cents for p in self.pledges.values())

    def limits_cents(self) -> dict[str, int]:
        """Each friend's limit by name, as split.split_shares() expects. Same names are made unique."""
        limits: dict[str, int] = {}
        for user_id, pledge in self.pledges.items():
            name = pledge.name if pledge.name not in limits else f"{pledge.name} ({user_id})"
            limits[name] = pledge.cents
        return limits

    def agent_input(self) -> dict:
        """The input of one agent run, as in docs/GIFT_BOT.md, "Input to one agent run"."""
        return {
            "person": self.person,
            "birthday": self.birthday.isoformat(),
            "pot_eur": self.pot_cents // 100,
            "country": self.country,
            "observations": [
                {"id": o.id, "from": o.author, "text": o.text} for o in self.observations
            ],
        }


class Store:
    """All open rounds, one per group chat."""

    def __init__(self) -> None:
        self.rounds: dict[int, Round] = {}

    def start(self, chat_id: int, person: str, birthday: date) -> Round:
        """Start a new round in a group. An older round in the same group is replaced."""
        self.rounds[chat_id] = Round(chat_id=chat_id, person=person, birthday=birthday)
        return self.rounds[chat_id]

    def get(self, chat_id: int) -> Round | None:
        return self.rounds.get(chat_id)

    def add_observation(self, chat_id: int, author: str, text: str) -> Observation | None:
        """Add an observation to the group's round. None if the group has no round or the text is empty."""
        round_ = self.rounds.get(chat_id)
        text = text.strip()
        if round_ is None or not text:
            return None
        observation = Observation(id=len(round_.observations) + 1, author=author, text=text)
        round_.observations.append(observation)
        return observation

    def pledge(self, chat_id: int, user_id: int, name: str, cents: int) -> Round | None:
        """Set (or replace) one friend's pledge in a group's round. None if that round does not exist."""
        round_ = self.rounds.get(chat_id)
        if round_ is None:
            return None
        round_.pledges[user_id] = Pledge(name=name, cents=cents)
        return round_
