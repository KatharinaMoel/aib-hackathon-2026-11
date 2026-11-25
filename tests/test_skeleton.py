"""The walking skeleton runs end to end without network or LLM (starter issue #1).

Covers: HTML to visible text, quote verification, the pipeline output against schema/verdict.schema.json,
the Markdown verdict, a failed fetch, and the LLM judge's handling of bad answers and unknown fact IDs.
"""

import json
from pathlib import Path

import httpx
import jsonschema

from taste import pipeline
from taste.fetch import FetchError, fetch, html_to_text
from taste.judge import llm_judge
from taste.models import Fact, Page
from taste.render import to_markdown
from taste.verify import verify

ROOT = Path(__file__).parent.parent
SCHEMA = json.loads((ROOT / "schema" / "verdict.schema.json").read_text(encoding="utf-8"))
HTML = (ROOT / "tests" / "fixtures" / "acme-crm.example.html").read_text(encoding="utf-8")
URL = "https://acme-crm.example/"


def fake_fetcher(url: str) -> Page:
    """Serve the fixture through httpx's mock transport, so fetch() runs its real code without network."""
    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, text=HTML))
    )
    return fetch(url, client=client)


def test_html_to_text_drops_scripts_styles_and_comments():
    text = html_to_text(HTML)
    assert "Acme CRM – the CRM for field service teams" in text
    assert "offerEnds" not in text and "color:red" not in text
    assert "ignore all previous instructions" not in text


def test_verify_exact_normalized_absent():
    page = Page(url=URL, status=200, text="Trusted by teams since 2008.", fetched_at="", sha256="")
    fact = Fact("c", "looks", "pro", "quote", URL, "vendor_self", "", quote="Trusted by teams")
    assert verify(fact, {URL: page}) == "exact"
    fact.quote = "TRUSTED  by\nteams"
    assert verify(fact, {URL: page}) == "normalized"
    fact.quote = "Trusted by 10,000 teams"
    assert verify(fact, {URL: page}) == "absent"


def test_pipeline_output_matches_schema_and_renders():
    verdict = pipeline.run(URL, fetcher=fake_fetcher)
    jsonschema.validate(verdict, SCHEMA)
    assert verdict["call"] == "caution"
    assert all(r["verification"]["status"] in ("exact", "measured") for r in verdict["reasons"])
    assert "**Call:** caution" in to_markdown(verdict)


def test_failed_fetch_gives_unclear_not_a_crash():
    def broken(url: str) -> Page:
        raise FetchError("timeout")

    verdict = pipeline.run(URL, fetcher=broken)
    jsonschema.validate(verdict, SCHEMA)
    assert verdict["call"] == "unclear"
    assert verdict["not_checked"][0]["why"] == "timeout"


def test_llm_judge_bad_json_gives_unclear():
    verdict = pipeline.run(
        URL, fetcher=fake_fetcher, judge=llm_judge(lambda prompt: "I think it is fine")
    )
    jsonschema.validate(verdict, SCHEMA)
    assert verdict["call"] == "unclear"


def test_llm_judge_reason_with_unknown_fact_id_is_dropped():
    answer = json.dumps(
        {
            "call": "trust",
            "reasons": [
                {"fact_id": "F1", "claim": "It answers.", "direction": "pro"},
                {"fact_id": "F99", "claim": "Invented.", "direction": "pro"},
            ],
        }
    )
    verdict = pipeline.run(URL, fetcher=fake_fetcher, judge=llm_judge(lambda prompt: answer))
    jsonschema.validate(verdict, SCHEMA)
    assert [r["fact_id"] for r in verdict["reasons"]] == ["F1"]
