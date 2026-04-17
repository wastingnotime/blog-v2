from __future__ import annotations

from pathlib import Path
import shutil

from src.app.application.use_cases.build_site import build_static_site
from src.app.domain.models.content import ContentCatalog
from src.app.domain.models.site_config import SiteConfig


class StaticSiteBuilder:
    def __init__(self, output_dir: Path, identity_assets_dir: Path) -> None:
        self._output_dir = output_dir
        self._identity_assets_dir = identity_assets_dir

    @property
    def identity_asset_filenames(self) -> tuple[str, ...]:
        return (
            "favicon.ico",
            "favicon-16x16.png",
            "favicon-32x32.png",
            "apple-touch-icon.png",
            "social-preview.png",
        )

    def build(self, config: SiteConfig, catalog: ContentCatalog) -> list[Path]:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        written_paths: list[Path] = []

        for relative_path, html in build_static_site(config, catalog).items():
            output_path = self._output_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")
            written_paths.append(output_path)

        for filename in self.identity_asset_filenames:
            source_path = self._identity_assets_dir / filename
            if not source_path.exists():
                raise FileNotFoundError(
                    f"missing identity asset: {source_path}"
                )
            output_path = self._output_dir / filename
            shutil.copyfile(source_path, output_path)
            written_paths.append(output_path)

        return sorted(written_paths)
