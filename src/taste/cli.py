"""Command line: `uv run --env-file .env python -m taste <url> [--out out/]`.

Prints the Markdown verdict and writes `<out>/<host>.json` and `<out>/<host>.md`. A list of URLs for the blind
run (one file, the 19:45 format) is starter issue #9.
"""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from taste.pipeline import run
from taste.render import to_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="taste", description="Judge a software product's website."
    )
    parser.add_argument("url", help="the product's website, e.g. https://acme-crm.example")
    parser.add_argument(
        "--out", default="out", help="folder for the JSON and Markdown verdict (git-ignored)"
    )
    args = parser.parse_args(argv)

    verdict = run(args.url)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    host = urlparse(args.url).hostname or "product"
    (out / f"{host}.json").write_text(json.dumps(verdict, indent=2, ensure_ascii=False) + "\n")
    markdown = to_markdown(verdict)
    (out / f"{host}.md").write_text(markdown)
    sys.stdout.write(markdown)
    return 0
