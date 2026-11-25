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


GLOBAL_V6 = ipaddress.ip_network("2000::/3")  # the only IPv6 range used on the public internet
NAT64 = ipaddress.ip_network(
    "64:ff9b::/96"
)  # well-known prefix: the IPv4 address is the last 32 bits
LOCAL_NAT64 = ipaddress.ip_network("64:ff9b:1::/48")  # site-specific layout: refused, not decoded


def _not_public(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    """True unless the address is clearly public. Fails closed: when in doubt, refuse.

    IPv6 forms that carry an IPv4 address (IPv4-mapped, 6to4, Teredo, NAT64) are judged by that IPv4 address.
    """
    if isinstance(ip, ipaddress.IPv6Address):
        embedded = ip.ipv4_mapped or ip.sixtofour or (ip.teredo[1] if ip.teredo else None)
        if ip in LOCAL_NAT64:
            return True
        if embedded is None and ip in NAT64:
            embedded = ipaddress.IPv4Address(int(ip) & 0xFFFFFFFF)
        if embedded is not None:
            ip = embedded
        elif ip not in GLOBAL_V6:
            return True
    return (
        not ip.is_global
        or ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_unspecified
        or ip.is_reserved
        or ip.is_multicast
    )


def check_url(url: str) -> None:
    """Refuse URLs that could reach our own machine or network: only public http(s) hosts.

    DNS can change between this check and the connection ("DNS rebinding"), so `fetch` checks the address it
    actually connected to again before it reads the page. Accepted limit: the GET request itself is already
    sent by then; only its answer is never read. Closing this fully needs a transport that connects to the
    checked IP – too much for a one-day agent whose URLs come from the organisers (decision 25 Nov 2026).
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


def _peer_is_public(response: httpx.Response) -> bool:
    """Check the address we really connected to (guards against DNS rebinding). Unknown = mock transport = ok."""
    stream = response.extensions.get("network_stream")
    peer = stream.get_extra_info("server_addr") if stream is not None else None
    if not peer:
        return True
    return not _not_public(ipaddress.ip_address(str(peer[0]).split("%")[0]))


def _read_capped(response: httpx.Response, started: float) -> bytes:
    """Read at most MAX_BYTES of the raw body and stop when the overall deadline has passed.

    We ask for uncompressed pages and refuse compressed ones, so a small compressed answer cannot expand
    into gigabytes in memory ("decompression bomb").
    """
    encoding = response.headers.get("content-encoding", "identity").strip().lower()
    if encoding not in ("", "identity"):
        raise FetchError(f"{response.url}: compressed answer ({encoding}) refused")
    body = bytearray()
    try:
        for chunk in response.iter_raw():
            body += chunk[: MAX_BYTES - len(body)]
            if len(body) >= MAX_BYTES:
                break
            if time.monotonic() - started > DEADLINE:
                raise FetchError(f"{response.url}: took longer than {DEADLINE:.0f} s")
    except httpx.StreamConsumed:  # test responses (mock transport) arrive already read
        return bytes(response.content[:MAX_BYTES])
    return bytes(body)


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
                headers={"User-Agent": USER_AGENT, "Accept-Encoding": "identity"},
                timeout=TIMEOUT,
                follow_redirects=False,
            ) as response:
                if not _peer_is_public(response):
                    raise FetchError(f"{current}: connected to a non-public address")
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
