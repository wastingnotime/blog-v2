from pathlib import Path

from src.app.application.use_cases.load_content_catalog import load_content_catalog
from src.app.interfaces.cli.run_scenario import load_site_config
from src.app.infrastructure.builders.static_site_builder import StaticSiteBuilder
from src.app.infrastructure.content.markdown_content_loader import MarkdownContentLoader


def test_static_site_builder_generates_static_routes_from_markdown(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "dist"
    content_root = Path(__file__).resolve().parents[2] / "content"
    builder = StaticSiteBuilder(output_dir=output_dir)
    catalog = load_content_catalog(
        loader=MarkdownContentLoader(),
        content_root=content_root,
    )

    written_paths = builder.build(load_site_config(), catalog)

    expected_paths = {
        output_dir / "index.html",
        output_dir / "feed.xml",
        output_dir / "sitemap.xml",
        output_dir / "about" / "index.html",
        output_dir / "library" / "index.html",
        output_dir / "library" / "architecture" / "index.html",
        output_dir / "sagas" / "index.html",
        output_dir / "sagas" / "hireflow" / "index.html",
        output_dir / "sagas" / "hireflow" / "the-origin-blueprint" / "index.html",
        output_dir / "studio" / "index.html",
        output_dir
        / "sagas"
        / "hireflow"
        / "the-origin-blueprint"
        / "the-first-brick"
        / "index.html",
    }

    assert expected_paths.issubset(set(written_paths))

    homepage_html = (output_dir / "index.html").read_text(encoding="utf-8")
    library_html = (output_dir / "library" / "index.html").read_text(encoding="utf-8")
    topic_html = (
        output_dir / "library" / "architecture" / "index.html"
    ).read_text(encoding="utf-8")
    sagas_index_html = (
        output_dir / "sagas" / "index.html"
    ).read_text(encoding="utf-8")
    saga_html = (
        output_dir / "sagas" / "hireflow" / "index.html"
    ).read_text(encoding="utf-8")
    arc_html = (
        output_dir / "sagas" / "hireflow" / "the-origin-blueprint" / "index.html"
    ).read_text(encoding="utf-8")
    about_html = (output_dir / "about" / "index.html").read_text(encoding="utf-8")
    feed_xml = (output_dir / "feed.xml").read_text(encoding="utf-8")
    sitemap_xml = (output_dir / "sitemap.xml").read_text(encoding="utf-8")
    studio_html = (
        output_dir / "studio" / "index.html"
    ).read_text(encoding="utf-8")
    episode_html = (
        output_dir
        / "sagas"
        / "hireflow"
        / "the-origin-blueprint"
        / "the-first-brick"
        / "index.html"
    ).read_text(encoding="utf-8")

    assert "In Public" in homepage_html
    assert "This site tracks architecture decisions" in homepage_html
    assert 'class="active">Home</a>' in homepage_html
    assert 'href="https://wastingnotime.org/about/"' in homepage_html
    assert 'href="https://wastingnotime.org/library/"' in homepage_html
    assert 'href="https://wastingnotime.org/sagas/"' in homepage_html
    assert "3 recent entries shown" in homepage_html
    assert "2 episodes · last release 2025-11-15 · in-progress" in homepage_html
    assert (output_dir / "sagas" / "hireflow" / "index.html").exists()
    assert "/api/event" not in homepage_html
    assert "Deployment target:" not in homepage_html
    assert "<rss version=\"2.0\">" in feed_xml
    assert "<link>https://wastingnotime.org/sagas/hireflow/the-origin-blueprint/second-iteration/</link>" in feed_xml
    assert "<title>About</title>" in feed_xml
    assert "/api/event" not in feed_xml
    assert "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" in sitemap_xml
    assert "<loc>https://wastingnotime.org/</loc>" in sitemap_xml
    assert "<loc>https://wastingnotime.org/library/architecture/</loc>" in sitemap_xml
    assert "<lastmod>2025-11-15</lastmod>" in sitemap_xml
    assert "Topics" in library_html
    assert 'class="active">Library</a>' in library_html
    assert "architecture" in library_html
    assert "[page] About" in topic_html
    assert "[episode] Second Iteration" in topic_html
    assert "Active sagas" in sagas_index_html
    assert 'class="active">Sagas</a>' in sagas_index_html
    assert "start reading" in sagas_index_html
    assert "Timeline" in saga_html
    assert 'class="active">Sagas</a>' in saga_html
    assert "The Origin Blueprint" in saga_html
    assert "Episodes" in arc_html
    assert "[Ep 01] The First Brick" in arc_html
    assert "Why this site exists" in about_html
    assert 'class="active">About</a>' in about_html
    assert "/sagas/" in studio_html
    assert "/library/" in studio_html
    assert 'class="active">Studio</a>' in studio_html
    assert "HireFlow / The Origin Blueprint" in episode_html
    assert "Ep 02 Second Iteration" in episode_html
    assert "/api/event" not in episode_html
