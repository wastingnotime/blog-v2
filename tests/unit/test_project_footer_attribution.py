from src.app.application.use_cases.project_footer_attribution import (
    project_footer_attribution,
)
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga
from src.app.domain.models.site_config import SiteConfig


def test_project_footer_attribution_uses_latest_publication_year() -> None:
    attribution = project_footer_attribution(_site_config(), _catalog())

    assert attribution.year == "2026"
    assert attribution.site_name == "example.com"
    assert attribution.tagline == "built with custom python static renderer"


def test_project_footer_attribution_falls_back_when_catalog_is_empty() -> None:
    attribution = project_footer_attribution(
        _site_config(),
        ContentCatalog(pages=(), sagas=(), arcs=(), episodes=(), section_pages=()),
    )

    assert attribution.year == "1970"


def _site_config() -> SiteConfig:
    return SiteConfig(
        title="Example",
        description="Static site",
        base_url="https://example.com/",
    )


def _catalog() -> ContentCatalog:
    return ContentCatalog(
        pages=(
            Page(
                title="About",
                slug="about",
                summary="Why this site exists and how the work is published in public.",
                date="2026-04-10",
                body_markdown="About body.",
            ),
        ),
        sagas=(
            Saga(
                title="HireFlow",
                slug="hireflow",
                summary="Architecture in public.",
                date="2026-04-11",
                status="in-progress",
            ),
        ),
        arcs=(
            Arc(
                title="The Origin Blueprint",
                slug="the-origin-blueprint",
                summary="How the saga starts.",
                date="2026-04-11",
                saga_slug="hireflow",
                saga_title="HireFlow",
            ),
        ),
        episodes=(
            Episode(
                title="Second Iteration",
                slug="second-iteration",
                summary="Follow-up work.",
                date="2026-04-13",
                saga_slug="hireflow",
                saga_title="HireFlow",
                arc_slug="the-origin-blueprint",
                arc_title="The Origin Blueprint",
                number=2,
                body_markdown="More episode body.",
            ),
        ),
        section_pages=(),
    )
