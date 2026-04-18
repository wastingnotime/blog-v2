from src.app.application.use_cases.project_narrative_navigation import (
    project_arc_views,
    project_saga_views,
)
from src.app.application.use_cases.project_publication_metadata import (
    project_publication_metadata,
)
from src.app.application.use_cases.project_topic_catalog import project_topic_catalog
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga


def test_project_publication_metadata_limits_feed_entries_by_recency() -> None:
    catalog = _catalog()
    arc_views = project_arc_views(catalog)
    saga_views = project_saga_views(catalog, arc_views)
    topic_catalog = project_topic_catalog(catalog)

    metadata = project_publication_metadata(
        catalog,
        saga_views,
        arc_views,
        topic_catalog.pages,
        feed_limit=2,
    )

    assert tuple(entry.title for entry in metadata.feed_entries) == (
        "Third Iteration",
        "Second Iteration",
    )


def test_project_publication_metadata_projects_sitemap_last_modified_dates() -> None:
    catalog = _catalog()
    arc_views = project_arc_views(catalog)
    saga_views = project_saga_views(catalog, arc_views)
    topic_catalog = project_topic_catalog(catalog)

    metadata = project_publication_metadata(
        catalog,
        saga_views,
        arc_views,
        topic_catalog.pages,
    )
    sitemap_by_permalink = {
        entry.permalink: entry.last_modified for entry in metadata.sitemap_entries
    }

    assert sitemap_by_permalink["/"] == "2026-04-14"
    assert sitemap_by_permalink["/archives/"] == "2026-04-14"
    assert sitemap_by_permalink["/library/"] == "2026-04-14"
    assert sitemap_by_permalink["/sagas/hireflow/"] == "2026-04-14"
    assert sitemap_by_permalink["/sagas/hireflow/the-origin-blueprint/"] == "2026-04-14"
    assert sitemap_by_permalink["/studio/"] is None


def _catalog() -> ContentCatalog:
    return ContentCatalog(
        pages=(
            Page(
                title="About",
                slug="about",
                summary="About the publication.",
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
            Episode(
                title="Third Iteration",
                slug="third-iteration",
                summary="Latest work.",
                date="2026-04-14",
                saga_slug="hireflow",
                saga_title="HireFlow",
                arc_slug="the-origin-blueprint",
                arc_title="The Origin Blueprint",
                number=3,
                body_markdown="Latest episode body.",
                tags=("architecture",),
            ),
        ),
    )
