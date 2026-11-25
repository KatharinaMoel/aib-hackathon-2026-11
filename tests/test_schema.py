"""The output contract loads and names the fields every verdict needs.

It checks that schema/verdict.schema.json is valid JSON and requires product_url, call and reasons.
It does not check allowed values or that a real verdict matches; see docs/FILES.md.
"""

import json
from pathlib import Path

SCHEMA = Path(__file__).parent.parent / "schema" / "verdict.schema.json"


def test_schema_is_valid_json_object():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema.get("type") == "object"
    assert {"product_url", "call", "reasons"} <= set(schema["required"])
