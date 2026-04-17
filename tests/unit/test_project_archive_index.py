from src.app.application.use_cases.project_archive_index import project_archive_index
from src.app.domain.models.content import ContentCatalog, Episode, Page


def test_project_archive_index_orders_entries_reverse_chronologically() -> None:
    archive_index = project_archive_index(_catalog())

    assert tuple(entry.title for entry in archive_index.entries) == (
        "Second Iteration",
        "The First Brick",
        "About",
    )


def test_project_archive_index_projects_narrative_context_for_episodes() -> None:
    archive_index = project_archive_index(_catalog())

    episode_entry = archive_index.entries[0]

    assert episode_entry.kind == "episode"
    assert episode_entry.saga_title == "HireFlow"
    assert episode_entry.arc_title == "The Origin Blueprint"


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
        sagas=(),
        arcs=(),
    )
