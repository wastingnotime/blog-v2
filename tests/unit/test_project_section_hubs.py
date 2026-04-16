from src.app.application.use_cases.project_narrative_navigation import (
    project_arc_views,
    project_saga_views,
)
from src.app.application.use_cases.project_section_hubs import project_sagas_index
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Saga


def test_project_sagas_index_uses_first_episode_as_start_reading() -> None:
    catalog = _catalog()
    arc_views = project_arc_views(catalog)
    saga_views = project_saga_views(catalog, arc_views)

    sagas_index = project_sagas_index(saga_views, arc_views)

    assert sagas_index.sagas[0].title == "HireFlow"
    assert (
        sagas_index.sagas[0].start_permalink
        == "/sagas/hireflow/the-origin-blueprint/the-first-brick/"
    )


def _catalog() -> ContentCatalog:
    return ContentCatalog(
        pages=(),
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
            ),
        ),
    )
