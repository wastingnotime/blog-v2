from src.app.application.use_cases.project_homepage_surface import (
    project_homepage_surface,
)
from src.app.application.use_cases.project_narrative_navigation import (
    project_arc_views,
    project_saga_views,
)
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga


def test_project_homepage_surface_limits_recent_entries_deterministically() -> None:
    catalog = _catalog()
    arc_views = project_arc_views(catalog)
    saga_views = project_saga_views(catalog, arc_views)

    homepage = project_homepage_surface(
        catalog,
        saga_views,
        arc_views,
        recent_limit=3,
    )

    assert tuple(entry.title for entry in homepage.recent_entries) == (
        "Third Iteration",
        "Second Iteration",
        "The First Brick",
    )
    assert all(entry.kind == "episode" for entry in homepage.recent_entries)


def test_project_homepage_surface_summarizes_saga_status() -> None:
    catalog = _catalog()
    arc_views = project_arc_views(catalog)
    saga_views = project_saga_views(catalog, arc_views)

    homepage = project_homepage_surface(catalog, saga_views, arc_views)

    assert homepage.saga_summaries[0].title == "HireFlow"
    assert homepage.saga_summaries[0].episode_count == 3
    assert homepage.saga_summaries[0].last_release_date == "2026-04-14"
    assert homepage.saga_summaries[0].status == "in-progress"


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
            Page(
                title="Notes",
                slug="notes",
                summary="Standalone note.",
                date="2026-04-15",
                body_markdown="Notes body.",
                tags=("writing",),
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
                tags=("architecture",),
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
                summary="Another follow-up.",
                date="2026-04-14",
                saga_slug="hireflow",
                saga_title="HireFlow",
                arc_slug="the-origin-blueprint",
                arc_title="The Origin Blueprint",
                number=3,
                body_markdown="Even more episode body.",
                tags=("architecture",),
            ),
        ),
    )
