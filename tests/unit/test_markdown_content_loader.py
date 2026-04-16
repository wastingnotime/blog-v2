from pathlib import Path

import pytest

from src.app.infrastructure.content.markdown_content_loader import MarkdownContentLoader


def test_markdown_content_loader_maps_frontmatter_to_typed_records(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    _write(
        content_root / "pages" / "about.md",
        """---
title: "About"
type: "page"
summary: "About this site."
date: "2026-04-10"
---

Hello world.
""",
    )
    _write(
        content_root / "sagas" / "hireflow" / "index.md",
        """---
title: "HireFlow"
type: "saga"
summary: "Saga summary."
status: "in-progress"
date: "2026-04-11"
---
""",
    )
    _write(
        content_root / "sagas" / "hireflow" / "the-origin-blueprint" / "index.md",
        """---
title: "The Origin Blueprint"
type: "arc"
summary: "Arc summary."
date: "2026-04-11"
---
""",
    )
    _write(
        content_root
        / "sagas"
        / "hireflow"
        / "the-origin-blueprint"
        / "the-first-brick.md",
        """---
title: "The First Brick"
type: "episode"
arc: "The Origin Blueprint"
summary: "Episode summary."
number: 1
date: "2026-04-12"
---

### The First Brick
""",
    )

    catalog = MarkdownContentLoader().load(content_root)

    assert catalog.pages[0].title == "About"
    assert catalog.sagas[0].title == "HireFlow"
    assert catalog.arcs[0].title == "The Origin Blueprint"
    assert catalog.episodes[0].arc_title == "The Origin Blueprint"
    assert catalog.episodes[0].permalink == (
        "/sagas/hireflow/the-origin-blueprint/the-first-brick/"
    )


def test_markdown_content_loader_rejects_missing_required_frontmatter(
    tmp_path: Path,
) -> None:
    content_root = tmp_path / "content"
    _write(
        content_root / "pages" / "about.md",
        """---
title: "About"
type: "page"
date: "2026-04-10"
---

Hello world.
""",
    )

    with pytest.raises(ValueError, match="summary"):
        MarkdownContentLoader().load(content_root)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
