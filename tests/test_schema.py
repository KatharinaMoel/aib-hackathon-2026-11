"""The output contract loads and names the fields every verdict needs."""

import json
from pathlib import Path

SCHEMA = Path(__file__).parent.parent / "schema" / "verdict.schema.json"


def test_schema_is_valid_json_object():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    assert schema.get("type") == "object"
    assert {"product_url", "call", "reasons"} <= set(schema["required"])
