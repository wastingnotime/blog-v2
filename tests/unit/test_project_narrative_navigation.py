from src.app.application.use_cases.project_narrative_navigation import (
    project_arc_views,
    project_saga_views,
)
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Saga


def test_project_arc_views_orders_episodes_and_builds_adjacent_navigation() -> None:
    catalog = _catalog()

    arc_view = project_arc_views(catalog)[("hireflow", "the-origin-blueprint")]

    assert [episode.number for episode in arc_view.episodes] == [1, 2]
    assert arc_view.previous_episode["the-first-brick"] is None
    assert arc_view.next_episode["the-first-brick"].title == "Second Iteration"
    assert arc_view.previous_episode["second-iteration"].title == "The First Brick"
    assert arc_view.next_episode["second-iteration"] is None


def test_project_saga_views_builds_timeline_descending_by_metadata() -> None:
    catalog = _catalog()
    arc_views = project_arc_views(catalog)

    saga_view = project_saga_views(catalog, arc_views)["hireflow"]

    assert [entry.title for entry in saga_view.timeline] == [
        "Second Iteration",
        "The First Brick",
    ]
    assert saga_view.arcs[0].title == "The Origin Blueprint"
    assert saga_view.arcs[0].episode_count == 2


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
