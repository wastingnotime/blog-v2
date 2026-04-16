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
        output_dir / "about" / "index.html",
        output_dir / "library" / "index.html",
        output_dir / "library" / "architecture" / "index.html",
        output_dir / "sagas" / "hireflow" / "index.html",
        output_dir / "sagas" / "hireflow" / "the-origin-blueprint" / "index.html",
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
    saga_html = (
        output_dir / "sagas" / "hireflow" / "index.html"
    ).read_text(encoding="utf-8")
    arc_html = (
        output_dir / "sagas" / "hireflow" / "the-origin-blueprint" / "index.html"
    ).read_text(encoding="utf-8")
    about_html = (output_dir / "about" / "index.html").read_text(encoding="utf-8")
    episode_html = (
        output_dir
        / "sagas"
        / "hireflow"
        / "the-origin-blueprint"
        / "the-first-brick"
        / "index.html"
    ).read_text(encoding="utf-8")

    assert "Recent" in homepage_html
    assert 'href="https://wastingnotime.org/about/"' in homepage_html
    assert 'href="https://wastingnotime.org/library/"' in homepage_html
    assert (output_dir / "sagas" / "hireflow" / "index.html").exists()
    assert "/api/event" not in homepage_html
    assert "Topics" in library_html
    assert "architecture" in library_html
    assert "[page] About" in topic_html
    assert "[episode] Second Iteration" in topic_html
    assert "Timeline" in saga_html
    assert "The Origin Blueprint" in saga_html
    assert "Episodes" in arc_html
    assert "[Ep 01] The First Brick" in arc_html
    assert "Why this site exists" in about_html
    assert "HireFlow / The Origin Blueprint" in episode_html
    assert "Ep 02 Second Iteration" in episode_html
    assert "/api/event" not in episode_html
