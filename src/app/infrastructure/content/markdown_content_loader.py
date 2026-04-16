from __future__ import annotations

from pathlib import Path

from src.app.domain.models.content import Arc, ContentCatalog, Episode, Page, Saga


class MarkdownContentLoader:
    def load(self, content_root: Path) -> ContentCatalog:
        pages = []
        sagas = []
        arcs = []
        episodes = []
        arc_titles: dict[tuple[str, str], str] = {}

        pages_root = content_root / "pages"
        if pages_root.exists():
            for path in sorted(pages_root.glob("*.md")):
                frontmatter, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
                _require_type(path, frontmatter, expected="page")
                page = Page(
                    title=_require_string(frontmatter, "title", path),
                    slug=path.stem,
                    summary=_require_string(frontmatter, "summary", path),
                    date=_require_string(frontmatter, "date", path),
                    body_markdown=body.strip(),
                )
                pages.append(page)

        sagas_root = content_root / "sagas"
        if sagas_root.exists():
            for saga_dir in sorted(path for path in sagas_root.iterdir() if path.is_dir()):
                saga_index = saga_dir / "index.md"
                if not saga_index.exists():
                    raise ValueError(f"missing saga index: {saga_index}")

                frontmatter, body = _parse_frontmatter(
                    saga_index.read_text(encoding="utf-8"),
                )
                _require_type(saga_index, frontmatter, expected="saga")
                saga = Saga(
                    title=_require_string(frontmatter, "title", saga_index),
                    slug=saga_dir.name,
                    summary=_require_string(frontmatter, "summary", saga_index),
                    date=_require_string(frontmatter, "date", saga_index),
                    status=_require_string(frontmatter, "status", saga_index),
                )
                sagas.append(saga)
                _ = body

                for arc_dir in sorted(path for path in saga_dir.iterdir() if path.is_dir()):
                    arc_index = arc_dir / "index.md"
                    if not arc_index.exists():
                        raise ValueError(f"missing arc index: {arc_index}")

                    arc_frontmatter, arc_body = _parse_frontmatter(
                        arc_index.read_text(encoding="utf-8"),
                    )
                    _require_type(arc_index, arc_frontmatter, expected="arc")
                    arc = Arc(
                        title=_require_string(arc_frontmatter, "title", arc_index),
                        slug=arc_dir.name,
                        summary=_require_string(arc_frontmatter, "summary", arc_index),
                        date=_require_string(arc_frontmatter, "date", arc_index),
                        saga_slug=saga.slug,
                        saga_title=saga.title,
                    )
                    arcs.append(arc)
                    arc_titles[(saga.slug, arc_dir.name)] = arc.title
                    _ = arc_body

                    for episode_path in sorted(arc_dir.glob("*.md")):
                        if episode_path.name == "index.md":
                            continue
                        frontmatter, body = _parse_frontmatter(
                            episode_path.read_text(encoding="utf-8"),
                        )
                        _require_type(episode_path, frontmatter, expected="episode")
                        episodes.append(
                            Episode(
                                title=_require_string(frontmatter, "title", episode_path),
                                slug=episode_path.stem,
                                summary=_require_string(
                                    frontmatter,
                                    "summary",
                                    episode_path,
                                ),
                                date=_require_string(frontmatter, "date", episode_path),
                                saga_slug=saga.slug,
                                saga_title=saga.title,
                                arc_slug=arc_dir.name,
                                arc_title=arc_titles.get(
                                    (saga.slug, arc_dir.name),
                                    _require_string(frontmatter, "arc", episode_path),
                                ),
                                number=_require_int(frontmatter, "number", episode_path),
                                body_markdown=body.strip(),
                            ),
                        )

        return ContentCatalog(
            pages=tuple(sorted(pages, key=lambda page: page.slug)),
            sagas=tuple(sorted(sagas, key=lambda saga: saga.slug)),
            arcs=tuple(sorted(arcs, key=lambda arc: (arc.saga_slug, arc.slug))),
            episodes=tuple(
                sorted(
                    episodes,
                    key=lambda episode: (episode.date, episode.number, episode.slug),
                    reverse=True,
                ),
            ),
        )


def _parse_frontmatter(document: str) -> tuple[dict[str, object], str]:
    if not document.startswith("---\n"):
        raise ValueError("expected YAML frontmatter delimited by ---")

    try:
        _, remainder = document.split("---\n", 1)
        frontmatter_block, body = remainder.split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("frontmatter block is not terminated") from exc

    return _parse_simple_yaml(frontmatter_block), body.lstrip("\n")


def _parse_simple_yaml(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list_key: str | None = None
    current_list: list[object] = []

    for line in raw.splitlines():
        if not line.strip():
            continue

        if line.startswith("  - "):
            if current_list_key is None:
                raise ValueError("list item declared before a key")
            current_list.append(_parse_scalar(line[4:]))
            continue

        if current_list_key is not None:
            data[current_list_key] = current_list
            current_list_key = None
            current_list = []

        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")

        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not value:
            current_list_key = key
            current_list = []
            continue
        data[key] = _parse_scalar(value)

    if current_list_key is not None:
        data[current_list_key] = current_list

    return data


def _parse_scalar(value: str) -> object:
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def _require_type(path: Path, frontmatter: dict[str, object], *, expected: str) -> None:
    actual = _require_string(frontmatter, "type", path)
    if actual != expected:
        raise ValueError(f"{path} declares type {actual!r}, expected {expected!r}")


def _require_string(frontmatter: dict[str, object], key: str, path: Path) -> str:
    value = frontmatter.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} is missing a non-empty string for {key!r}")
    return value.strip()


def _require_int(frontmatter: dict[str, object], key: str, path: Path) -> int:
    value = frontmatter.get(key)
    if not isinstance(value, int):
        raise ValueError(f"{path} is missing an integer for {key!r}")
    return value
