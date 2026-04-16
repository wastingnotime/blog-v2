from pathlib import Path

from src.app.interfaces.cli.run_scenario import load_site_config
from src.app.infrastructure.builders.static_site_builder import StaticSiteBuilder


def test_static_site_builder_writes_index_html(tmp_path: Path) -> None:
    output_dir = tmp_path / "dist"
    builder = StaticSiteBuilder(output_dir=output_dir)

    homepage_path = builder.build(load_site_config())

    assert homepage_path == output_dir / "index.html"
    assert homepage_path.exists()
    html = homepage_path.read_text(encoding="utf-8")
    assert "GitHub Pages static files" in html
    assert "/api/event" not in html
