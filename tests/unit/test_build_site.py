from src.app.application.use_cases.build_site import build_homepage
from src.app.domain.models.site_config import AnalyticsConfig, SiteConfig


def test_build_homepage_omits_same_origin_api_when_analytics_disabled() -> None:
    config = SiteConfig(
        title="Example",
        description="Static site",
        base_url="https://example.com/",
    )

    html = build_homepage(config)

    assert "/api/event" not in html
    assert 'src="https://plausible.io/js/script.js"' not in html


def test_build_homepage_renders_direct_plausible_configuration() -> None:
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

    html = build_homepage(config)

    assert 'src="https://plausible.example.com/js/script.js"' in html
    assert 'data-api="https://plausible.example.com/api/event"' in html
    assert 'data-domain="example.com"' in html
    assert "https://example.com/api/event" not in html
