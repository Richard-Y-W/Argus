from __future__ import annotations

from dataclasses import dataclass

from .biospace_reconstruction import (
    SitemapEntry,
    candidate_entries,
    parse_sitemap,
    polite_fetch,
)


SITEMAP = b"""<?xml version='1.0'?>
<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>
  <url><loc>https://www.biospace.com/a-phase-iii-trial-fails</loc><lastmod>2019-01-02</lastmod></url>
  <url><loc>https://www.biospace.com/company-hires-a-ceo</loc></url>
  <url><loc>https://www.biospace.com/positive-phase-3-topline-results</loc></url>
</urlset>"""


def test_parse_and_filter_sitemap() -> None:
    entries = parse_sitemap(SITEMAP)
    assert len(entries) == 3
    candidates = candidate_entries(entries)
    assert [entry.slug for entry in candidates] == [
        "a-phase-iii-trial-fails",
        "positive-phase-3-topline-results",
    ]
    assert candidates[0].last_modified == "2019-01-02"


@dataclass
class FakeResponse:
    status_checked: bool = False

    def raise_for_status(self) -> None:
        self.status_checked = True


def test_polite_fetch_respects_one_second_delay() -> None:
    sleeps: list[float] = []
    clocks = iter([10.25, 11.0])
    response = FakeResponse()

    result, requested_at = polite_fetch(
        "https://example.com/article",
        previous_request_at=10.0,
        get=lambda *args, **kwargs: response,
        clock=lambda: next(clocks),
        sleeper=sleeps.append,
    )

    assert result is response
    assert requested_at == 11.0
    assert sleeps == [0.75]
    assert response.status_checked


def test_candidate_filter_does_not_treat_generic_phase_page_as_event() -> None:
    entries = [SitemapEntry("https://www.biospace.com/phase-iii-explainer", None)]
    assert candidate_entries(entries) == []
