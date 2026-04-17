from src.app.application.use_cases.project_entry_metadata import (
    project_episode_metadata,
    project_page_metadata,
)
from src.app.domain.models.content import Episode, Page


def test_project_page_metadata_derives_reading_time_and_tag_links() -> None:
    page = Page(
        title="About",
        slug="about",
        summary="About the publication.",
        date="2026-04-10",
        body_markdown=" ".join(["word"] * 210),
        tags=("architecture", "writing"),
    )

    metadata = project_page_metadata(page)

    assert metadata.publication_date == "2026-04-10"
    assert metadata.reading_time_minutes == 2
    assert tuple(tag.name for tag in metadata.tags) == ("architecture", "writing")
    assert tuple(tag.permalink for tag in metadata.tags) == (
        "/library/architecture/",
        "/library/writing/",
    )


def test_project_episode_metadata_defaults_to_one_minute_without_tags() -> None:
    episode = Episode(
        title="The First Brick",
        slug="the-first-brick",
        summary="Recent work.",
        date="2026-04-12",
        saga_slug="hireflow",
        saga_title="HireFlow",
        arc_slug="the-origin-blueprint",
        arc_title="The Origin Blueprint",
        number=1,
        body_markdown="brief body",
        tags=(),
    )

    metadata = project_episode_metadata(episode)

    assert metadata.publication_date == "2026-04-12"
    assert metadata.reading_time_minutes == 1
    assert metadata.tags == ()
