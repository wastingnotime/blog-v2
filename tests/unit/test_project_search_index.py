import json

from src.app.application.use_cases.project_search_index import project_search_index
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga
from src.app.domain.models.site_config import SiteConfig


def test_project_search_index_projects_pages_and_narrative_content() -> None:
    index = project_search_index(_site_config(), _catalog())

    records = {entry.title: entry for entry in index.entries}

    assert tuple(entry.title for entry in index.entries) == (
        "Second Iteration",
        "The First Brick",
        "HireFlow",
        "The Origin Blueprint",
        "About",
    )
    assert records["About"].type == "page"
    assert records["About"].tags == ("architecture",)
    assert records["HireFlow"].type == "saga"
    assert records["HireFlow"].summary == "Architecture in public."
    assert records["The Origin Blueprint"].context == "HireFlow"
    assert records["Second Iteration"].context == "HireFlow · The Origin Blueprint"
    assert records["Second Iteration"].tags == ("architecture",)


def test_project_search_index_uses_absolute_urls_from_site_config() -> None:
    index = project_search_index(_site_config(), _catalog())

    serialized_urls = json.dumps([entry.url for entry in index.entries])

    assert "https://example.com/about/" in serialized_urls
    assert (
        "https://example.com/sagas/hireflow/the-origin-blueprint/second-iteration/"
        in serialized_urls
    )
    assert "/api/" not in serialized_urls


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
                tags=("architecture",),
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
                title="The First Brick",
                slug="the-first-brick",
                summary="Recent work.",
                date="2026-04-12",
                saga_slug="hireflow",
                saga_title="HireFlow",
                arc_slug="the-origin-blueprint",
                arc_title="The Origin Blueprint",
                number=1,
                body_markdown="Episode body.",
                tags=("architecture", "writing"),
            ),
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
                tags=("architecture",),
            ),
        ),
    )
