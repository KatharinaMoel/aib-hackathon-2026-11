"""Shared fetch helper: the only place that talks to the network (house rule: every call has a timeout).

Starter issue #2 adds the cache in out/cache/, a page limit per site and politeness delays.
"""

import hashlib
import ipaddress
import re
import socket
from datetime import UTC, datetime
from html import unescape
from urllib.parse import urlparse

import httpx

from taste.models import Page

TIMEOUT = 10.0  # seconds; a slow vendor site must not block the blind run
USER_AGENT = "taste-hackathon-agent/0.1 (AI Agents Berlin hackathon; polite, low volume)"


class FetchError(Exception):
    """The page could not be fetched. The caller records it under `not_checked`, never as a con."""


def check_url(url: str) -> None:
    """Refuse URLs that could reach our own machine or network: only public http(s) hosts."""
    parts = urlparse(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise FetchError(f"not an http(s) URL: {url}")
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(parts.hostname, None)}
    except socket.gaierror as err:
        raise FetchError(f"DNS lookup failed for {parts.hostname}: {err}") from err
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            raise FetchError(f"{parts.hostname} resolves to a non-public address")


def html_to_text(html: str) -> str:
    """Visible text only: drop scripts, styles, comments and tags. Website text is data, never instructions."""
    html = re.sub(r"(?is)<(script|style|noscript|template)\b.*?</\1>", " ", html)
    html = re.sub(r"(?s)<!--.*?-->", " ", html)
    text = unescape(re.sub(r"(?s)<[^>]+>", " ", html))
    return re.sub(r"\s+", " ", text).strip()


def fetch(url: str, client: httpx.Client | None = None) -> Page:
    """Fetch one page. Tests pass a client with a mock transport, so they never touch the network."""
    if client is None:
        check_url(url)
        client = httpx.Client(timeout=TIMEOUT, follow_redirects=True)
    try:
        response = client.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    except httpx.HTTPError as err:
        raise FetchError(f"{url}: {err}") from err
    body = response.text
    return Page(
        url=str(response.url),
        status=response.status_code,
        text=html_to_text(body),
        fetched_at=datetime.now(UTC).isoformat(timespec="seconds"),
        sha256=hashlib.sha256(body.encode()).hexdigest(),
    )
