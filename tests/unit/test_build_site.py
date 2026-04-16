from src.app.application.use_cases.build_site import build_static_site
from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga
from src.app.domain.models.site_config import AnalyticsConfig, SiteConfig


def test_build_static_site_omits_same_origin_api_when_analytics_disabled() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert "/api/event" not in html
    assert 'src="https://plausible.io/js/script.js"' not in html


def test_build_static_site_renders_direct_plausible_configuration() -> None:
    config = SiteConfig(
        title="Example",
        description="Static site",
        base_url="https://example.com/",
        analytics=AnalyticsConfig(
            provider="plausible",
            domain="example.com",
            script_url="https://plausible.example.com/js/script.js",
            api_host="https://plausible.example.com",
        ),
    )

    html = build_static_site(config, _catalog())["index.html"]

    assert 'src="https://plausible.example.com/js/script.js"' in html
    assert 'data-api="https://plausible.example.com/api/event"' in html
    assert 'data-domain="example.com"' in html
    assert "https://example.com/api/event" not in html


def test_build_static_site_orders_recent_content_by_date_desc() -> None:
    html = build_static_site(_site_config(), _catalog())["index.html"]

    assert html.index("[episode] Second Iteration") < html.index("[page] About")


def test_build_static_site_renders_arc_page_and_episode_navigation() -> None:
    pages = build_static_site(_site_config(), _catalog())

    arc_html = pages["sagas/hireflow/the-origin-blueprint/index.html"]
    first_episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/the-first-brick/index.html"
    ]
    second_episode_html = pages[
        "sagas/hireflow/the-origin-blueprint/second-iteration/index.html"
    ]

    assert "[Ep 01] The First Brick" in arc_html
    assert "[Ep 02] Second Iteration" in arc_html
    assert "HireFlow</a> /" in first_episode_html
    assert "Ep 02 Second Iteration" in first_episode_html
    assert "Ep 01 The First Brick" in second_episode_html


def test_build_static_site_generates_library_and_topic_pages() -> None:
    pages = build_static_site(_site_config(), _catalog())

    library_html = pages["library/index.html"]
    topic_html = pages["library/architecture/index.html"]

    assert "Topics" in library_html
    assert "architecture" in library_html
    assert "[page] About" in topic_html
    assert "[episode] Second Iteration" in topic_html
    assert "HireFlow / The Origin Blueprint" in topic_html


def test_build_static_site_generates_section_hub_pages() -> None:
    pages = build_static_site(_site_config(), _catalog())

    sagas_html = pages["sagas/index.html"]
    studio_html = pages["studio/index.html"]

    assert "Active sagas" in sagas_html
    assert "HireFlow" in sagas_html
    assert "start reading" in sagas_html
    assert "/library/" in studio_html
    assert "/sagas/" in studio_html


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
