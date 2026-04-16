from src.app.application.use_cases.build_site import build_static_site
from src.app.domain.models.content import ContentCatalog, Episode, Page, Saga
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

    assert html.index("[episode] New Episode") < html.index("[page] About")


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
        episodes=(
            Episode(
                title="New Episode",
                slug="new-episode",
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
