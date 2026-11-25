"""One product end to end: fetch → signals → verify → judge → verdict dict (schema/verdict.schema.json)."""

import subprocess
from collections.abc import Callable

from taste.fetch import FetchError, fetch
from taste.judge import stub_judge
from taste.models import Fact, Page
from taste.signals import SIGNALS
from taste.verify import verify


def run_id() -> str:
    """git SHA of the code that made the verdict (model and prompt hash are added by #7)."""
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return sha.stdout.strip() or "unknown"


def evidence_strength(facts: list[Fact]) -> str:
    """strong = at least two verified facts of different kinds, at least one independent."""
    kinds = {f.kind for f in facts}
    independent = any(f.tier == "independent" for f in facts)
    return "strong" if len(facts) >= 2 and len(kinds) >= 2 and independent else "thin"


def run(
    url: str,
    fetcher: Callable[[str], Page] = fetch,
    signals=None,
    judge: Callable[[list[Fact]], dict] = stub_judge,
) -> dict:
    """Return a verdict dict. A failed fetch gives 'unclear' with the reason in not_checked."""
    signals = SIGNALS if signals is None else signals
    verdict = {"product_url": url, "not_checked": [], "run_id": run_id()}
    try:
        home = fetcher(url)
    except FetchError as err:
        verdict.update(call="unclear", reasons=[], evidence_strength="thin")
        verdict["not_checked"].append({"signal": "homepage", "why": str(err)})
        return verdict

    pages = {home.url: home}
    facts: list[Fact] = []
    for signal in signals:
        result = signal(home, fetcher)
        facts.extend(result.facts)
        verdict["not_checked"].extend(result.not_checked)

    for number, fact in enumerate(facts, start=1):
        fact.fact_id = f"F{number}"
        fact.verification = verify(fact, pages)
    verified = [f for f in facts if f.verification != "absent"]
    for f in facts:
        if f.verification == "absent":
            verdict["not_checked"].append(
                {"signal": f.fact_id, "why": "quote not found on the fetched page"}
            )

    decision = judge(verified)
    by_id = {f.fact_id: f for f in verified}
    reasons = []
    for r in decision.get("reasons", []):
        fact = by_id.get(r.get("fact_id"))
        if fact is None:  # the judge cited an ID we do not have: drop the reason
            continue
        reasons.append(reason_dict(fact, r))
    verdict.update(
        call=decision["call"],
        reasons=reasons,
        evidence_strength=evidence_strength([by_id[r["fact_id"]] for r in reasons]),
    )
    return verdict


def reason_dict(fact: Fact, said: dict) -> dict:
    """A reason in schema form: the judge's sentence and direction, everything else from the verified fact."""
    reason = {
        "fact_id": fact.fact_id,
        "claim": said.get("claim") or fact.claim,
        "axis": fact.axis,
        "direction": said.get("direction")
        if said.get("direction") in ("pro", "con")
        else fact.direction,
        "kind": fact.kind,
        "url": fact.url,
        "fetched_at": fact.fetched_at,
        "tier": fact.tier,
        "verification": {"status": fact.verification},
    }
    if fact.kind == "quote":
        reason["quote"] = fact.quote[:300]
    else:
        reason["measurement"] = fact.measurement or {"method": "unknown", "value": None}
    return reason
