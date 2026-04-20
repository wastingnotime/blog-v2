from __future__ import annotations

from datetime import date
from urllib.parse import urlparse

from src.app.domain.models.content import ContentCatalog, FooterAttribution
from src.app.domain.models.site_config import SiteConfig


def project_footer_attribution(
    config: SiteConfig,
    catalog: ContentCatalog,
) -> FooterAttribution:
    publication_dates = (
        tuple(page.date for page in catalog.pages)
        + tuple(saga.date for saga in catalog.sagas)
        + tuple(arc.date for arc in catalog.arcs)
        + tuple(episode.date for episode in catalog.episodes)
    )
    latest_date = max((date for date in publication_dates if date), default="1970-01-01")
    current_year = str(date.today().year)
    year = latest_date[:4] if latest_date == "1970-01-01" else max(latest_date[:4], current_year)
    return FooterAttribution(
        year=year,
        site_name=_site_name_from_base_url(config.base_url),
        tagline="built with custom python static renderer",
    )


def _site_name_from_base_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    netloc = parsed.netloc or base_url.rstrip("/")
    if "wastingnotime.org" in netloc:
        return "wastingnotime.org"
    return netloc
