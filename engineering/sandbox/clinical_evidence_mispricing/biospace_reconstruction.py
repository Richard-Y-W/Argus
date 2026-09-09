"""BioSpace catalog discovery for an independent Phase III event reconstruction.

The collector respects BioSpace's published one-second crawl delay. Catalog
discovery is intentionally return-blind and does not classify outcomes from
subsequent price behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
import time
from typing import Callable
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

import requests


SITEMAP_URL = "https://www.biospace.com/news-sitemap-content.xml"
SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
PHASE_PATTERN = re.compile(r"(?:phase[- ]?(?:3|iii)|late[- ]stage)", re.IGNORECASE)
OUTCOME_PATTERN = re.compile(
    r"(?:fail|flop|miss|did-not-meet|positive|success|meet|topline|top-line|result)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SitemapEntry:
    url: str
    last_modified: str | None

    @property
    def slug(self) -> str:
        return urlparse(self.url).path.rstrip("/").rsplit("/", maxsplit=1)[-1]


def parse_sitemap(content: bytes) -> list[SitemapEntry]:
    root = ET.fromstring(content)
    entries = []
    for node in root.findall("s:url", SITEMAP_NS):
        location = node.find("s:loc", SITEMAP_NS)
        modified = node.find("s:lastmod", SITEMAP_NS)
        if location is None or not location.text:
            continue
        entries.append(
            SitemapEntry(
                url=location.text.strip(),
                last_modified=modified.text.strip()
                if modified is not None and modified.text
                else None,
            )
        )
    return entries


def candidate_entries(entries: list[SitemapEntry]) -> list[SitemapEntry]:
    return [
        entry
        for entry in entries
        if PHASE_PATTERN.search(entry.slug) and OUTCOME_PATTERN.search(entry.slug)
    ]


def fetch_catalog(
    *,
    get: Callable[..., requests.Response] = requests.get,
) -> list[SitemapEntry]:
    response = get(
        SITEMAP_URL,
        timeout=30,
        headers={"User-Agent": "Argus academic event-catalog reconstruction"},
    )
    response.raise_for_status()
    return parse_sitemap(response.content)


def polite_fetch(
    url: str,
    *,
    previous_request_at: float | None,
    get: Callable[..., requests.Response] = requests.get,
    clock: Callable[[], float] = time.monotonic,
    sleeper: Callable[[float], None] = time.sleep,
) -> tuple[requests.Response, float]:
    now = clock()
    if previous_request_at is not None:
        sleeper(max(0.0, 1.0 - (now - previous_request_at)))
    response = get(
        url,
        timeout=30,
        headers={"User-Agent": "Argus academic event-catalog reconstruction"},
    )
    response.raise_for_status()
    return response, clock()


def parse_iso_date(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
