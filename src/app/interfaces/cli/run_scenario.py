from __future__ import annotations

import os
from pathlib import Path

from src.app.application.use_cases.load_content_catalog import load_content_catalog
from src.app.domain.models.site_config import SiteConfig
from src.app.infrastructure.builders.static_site_builder import StaticSiteBuilder
from src.app.infrastructure.content.markdown_content_loader import MarkdownContentLoader


def main() -> None:
    output_dir = Path(_getenv("OUTPUT_DIR", default="dist"))
    content_root = Path(_getenv("CONTENT_ROOT", default="content"))
    identity_assets_dir = Path(
        _getenv("IDENTITY_ASSETS_DIR", default="assets/site/current")
    )
    builder = StaticSiteBuilder(
        output_dir=output_dir,
        identity_assets_dir=identity_assets_dir,
    )
    catalog = load_content_catalog(
        loader=MarkdownContentLoader(),
        content_root=content_root,
    )
    written_paths = builder.build(load_site_config(), catalog)
    print(f"generated {len(written_paths)} files under {output_dir}")


def load_site_config() -> SiteConfig:
    return SiteConfig(
        title=_getenv("SITE_TITLE", default="Wasting No Time"),
        description=_getenv(
            "SITE_DESCRIPTION",
            default=(
                "blog-v2 starts from a simpler contract: static output, GitHub "
                "Pages deployment, and no first-party /api dependency."
            ),
        ),
        base_url=_getenv("SITE_BASE_URL", default="https://blog.wastingnotime.org/"),
    )


def _getenv(name: str, *, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip() or default


if __name__ == "__main__":
    main()
