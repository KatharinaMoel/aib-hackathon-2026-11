"""The Markdown verdict a person reads (judges read reasons by hand, brief p. 3)."""

ICON = {"pro": "+", "con": "−"}


def to_markdown(verdict: dict) -> str:
    """Call, reasons with their links, and what we could not check."""
    lines = [
        f"## {verdict['product_url']}",
        "",
        f"**Call:** {verdict['call']} · evidence: {verdict['evidence_strength']}",
        "",
    ]
    for r in verdict["reasons"]:
        source = (
            f"“{r['quote']}”" if r["kind"] == "quote" else f"measured: {r['measurement']['value']}"
        )
        lines.append(
            f"- {ICON[r['direction']]} {r['claim']} — {source} — <{r['url']}> ({r['fact_id']})"
        )
    if verdict["not_checked"]:
        lines += ["", "**Could not check:**"]
        lines += [f"- {n['signal']}: {n['why']}" for n in verdict["not_checked"]]
    return "\n".join(lines) + "\n"
