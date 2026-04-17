from __future__ import annotations

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
    return FooterAttribution(
        year=latest_date[:4],
        site_name=_site_name_from_base_url(config.base_url),
        tagline="published as a static site",
    )


def _site_name_from_base_url(base_url: str) -> str:
    parsed = urlparse(base_url)
    return parsed.netloc or base_url.rstrip("/")
