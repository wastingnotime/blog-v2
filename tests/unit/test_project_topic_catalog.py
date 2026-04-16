from src.app.application.use_cases.project_topic_catalog import project_topic_catalog
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga


def test_project_topic_catalog_builds_sorted_tag_pages() -> None:
    catalog = _catalog()

    topic_catalog = project_topic_catalog(catalog)

    assert topic_catalog.tags == ("architecture", "writing")
    architecture_page = next(page for page in topic_catalog.pages if page.tag == "architecture")
    assert [entry.title for entry in architecture_page.entries] == [
        "Second Iteration",
        "The First Brick",
        "About",
    ]


def _catalog() -> ContentCatalog:
    return ContentCatalog(
        pages=(
            Page(
                title="About",
                slug="about",
                summary="What this site is about.",
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
        ),
    )
