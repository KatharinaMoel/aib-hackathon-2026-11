"""Shared fetch helper: the only place that talks to the network (house rule: every call has a timeout).

Starter issue #2 adds the cache in out/cache/, a page limit per site and politeness delays.
"""

import hashlib
import ipaddress
import re
import socket
import time
from datetime import UTC, datetime
from html import unescape
from urllib.parse import urlparse

import httpx

from taste.models import Page

TIMEOUT = 10.0  # seconds per request; a slow vendor site must not block the blind run
DEADLINE = 20.0  # seconds for one fetch incl. redirects and reading the body
MAX_BYTES = 3_000_000  # stop reading a page after 3 MB
MAX_REDIRECTS = 5
USER_AGENT = "taste-hackathon-agent/0.1 (AI Agents Berlin hackathon; polite, low volume)"


class FetchError(Exception):
    """The page could not be fetched. The caller records it under `not_checked`, never as a con."""


def _not_public(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """True for addresses that point into our own machine or network, incl. IPv6 forms of IPv4 ones."""
    if isinstance(ip, ipaddress.IPv6Address):
        if ip.ipv4_mapped:
            ip = ip.ipv4_mapped
        elif ip.sixtofour:
            ip = ip.sixtofour
    return not ip.is_global or ip.is_multicast


def check_url(url: str) -> None:
    """Refuse URLs that could reach our own machine or network: only public http(s) hosts.

    Limit (not verified to matter here): DNS can change between this check and the connection ("DNS
    rebinding"). Pinning the checked IP for the connection is a follow-up in starter issue #2.
    """
    parts = urlparse(url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise FetchError(f"not an http(s) URL: {url}")
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(parts.hostname, None)}
    except socket.gaierror as err:
        raise FetchError(f"DNS lookup failed for {parts.hostname}: {err}") from err
    for address in addresses:
        if _not_public(ipaddress.ip_address(address.split("%")[0])):
            raise FetchError(f"{parts.hostname} resolves to a non-public address")


def html_to_text(html: str) -> str:
    """Visible text only: drop scripts, styles, comments and tags. Website text is data, never instructions."""
    html = re.sub(r"(?is)<(script|style|noscript|template)\b.*?</\1>", " ", html)
    html = re.sub(r"(?s)<!--.*?-->", " ", html)
    text = unescape(re.sub(r"(?s)<[^>]+>", " ", html))
    return re.sub(r"\s+", " ", text).strip()


def _read_capped(response: httpx.Response, started: float) -> bytes:
    """Read at most MAX_BYTES, and stop when the overall deadline has passed."""
    body = b""
    for chunk in response.iter_bytes():
        body += chunk
        if len(body) > MAX_BYTES:
            return body[:MAX_BYTES]
        if time.monotonic() - started > DEADLINE:
            raise FetchError(f"{response.url}: took longer than {DEADLINE:.0f} s")
    return body


def fetch(url: str, client: httpx.Client | None = None, guard=check_url) -> Page:
    """Fetch one page. Redirects are followed by hand, and every target passes `guard` first.

    Tests pass a client with a mock transport and `guard=lambda url: None`, so they never touch the network.
    """
    client = client or httpx.Client(timeout=TIMEOUT, follow_redirects=False)
    started = time.monotonic()
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        guard(current)
        try:
            with client.stream(
                "GET",
                current,
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT,
                follow_redirects=False,
            ) as response:
                if response.is_redirect and "location" in response.headers:
                    current = str(response.url.join(response.headers["location"]))
                    continue
                raw = _read_capped(response, started)
                status, final_url, encoding = (
                    response.status_code,
                    str(response.url),
                    response.encoding,
                )
        except httpx.HTTPError as err:
            raise FetchError(f"{current}: {err}") from err
        body = raw.decode(encoding or "utf-8", errors="replace")
        return Page(
            url=final_url,
            status=status,
            text=html_to_text(body),
            fetched_at=datetime.now(UTC).isoformat(timespec="seconds"),
            sha256=hashlib.sha256(raw).hexdigest(),
        )
    raise FetchError(f"{url}: more than {MAX_REDIRECTS} redirects")
