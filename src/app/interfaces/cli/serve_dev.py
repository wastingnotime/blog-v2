from __future__ import annotations

import argparse
from dataclasses import dataclass
import mimetypes
import os
from pathlib import Path
import threading
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import ClassVar
from urllib.parse import unquote, urlsplit

from src.app.application.use_cases.load_content_catalog import load_content_catalog
from src.app.interfaces.cli.run_scenario import load_site_config
from src.app.domain.models.site_config import SiteConfig
from src.app.infrastructure.builders.static_site_builder import StaticSiteBuilder
from src.app.infrastructure.content.markdown_content_loader import MarkdownContentLoader


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080
DEFAULT_BASE_URL = "http://localhost:8080/"
POLL_INTERVAL_SECONDS = 1.0
RELOAD_CHECK_PATH = "/__dev_reload__"
RELOAD_SCRIPT = """
<script>
(() => {
  const reloadUrl = "/__dev_reload__";
  let currentVersion = null;

  const poll = async () => {
    try {
      const response = await fetch(reloadUrl, { cache: "no-store" });
      const nextVersion = (await response.text()).trim();
      if (currentVersion === null) {
        currentVersion = nextVersion;
      } else if (nextVersion !== currentVersion) {
        window.location.reload();
        return;
      }
    } catch (error) {
      // Ignore transient rebuild or startup failures.
    }

    window.setTimeout(poll, 1000);
  };

  poll();
})();
</script>
""".strip()


@dataclass(frozen=True)
class DevServerConfig:
    output_dir: Path
    content_root: Path
    identity_assets_dir: Path
    host: str
    port: int


class ReloadState:
    def __init__(self) -> None:
        self._version = 0
        self._lock = threading.Lock()

    def bump(self) -> int:
        with self._lock:
            self._version += 1
            return self._version

    def current(self) -> int:
        with self._lock:
            return self._version


class DevRequestHandler(SimpleHTTPRequestHandler):
    directory: ClassVar[str]
    reload_state: ClassVar[ReloadState]

    def __init__(self, *args, directory: str, reload_state: ReloadState, **kwargs):
        self.directory = directory
        self.reload_state = reload_state
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self) -> None:  # noqa: N802
        if urlsplit(self.path).path == RELOAD_CHECK_PATH:
            payload = f"{self.reload_state.current()}\n".encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        self._serve_file()

    def _serve_file(self) -> None:
        request_path = urlsplit(self.path).path
        if request_path.endswith("/"):
            request_path += "index.html"
        elif "." not in Path(request_path).name:
            request_path += "/index.html"

        relative_path = unquote(request_path.lstrip("/"))
        file_path = Path(self.directory) / relative_path
        if not file_path.exists():
            file_path = Path(self.directory) / "404.html"
            status = HTTPStatus.NOT_FOUND
        else:
            status = HTTPStatus.OK

        data = file_path.read_bytes()
        content_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        if file_path.suffix == ".html":
            html = data.decode("utf-8")
            html = _inject_reload_script(html)
            data = html.encode("utf-8")
            content_type = "text/html; charset=utf-8"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Build and serve the site locally.")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--output-dir", default="dist")
    parser.add_argument("--content-root", default="content")
    parser.add_argument("--identity-assets-dir", default="assets/site/current")
    parser.add_argument("--base-url", default=os.getenv("SITE_BASE_URL", DEFAULT_BASE_URL))
    args = parser.parse_args(argv)

    config = DevServerConfig(
        output_dir=Path(args.output_dir),
        content_root=Path(args.content_root),
        identity_assets_dir=Path(args.identity_assets_dir),
        host=args.host,
        port=args.port,
    )

    site_config = load_site_config()
    if not os.getenv("SITE_BASE_URL"):
        site_config = SiteConfig(
            title=site_config.title,
            description=site_config.description,
            base_url=args.base_url,
            analytics=site_config.analytics,
        )

    builder = StaticSiteBuilder(
        output_dir=config.output_dir,
        identity_assets_dir=config.identity_assets_dir,
    )
    catalog = load_content_catalog(
        loader=MarkdownContentLoader(),
        content_root=config.content_root,
    )
    reload_state = ReloadState()
    builder.build(site_config, catalog)
    reload_state.bump()

    watch_targets = (
        config.content_root,
        Path("src/app"),
        config.identity_assets_dir,
    )

    stop_event = threading.Event()
    watcher = threading.Thread(
        target=_watch_for_changes,
        args=(builder, site_config, config, reload_state, watch_targets, stop_event),
        daemon=True,
    )
    watcher.start()

    handler_factory = lambda *handler_args, **handler_kwargs: DevRequestHandler(
        *handler_args,
        directory=str(config.output_dir),
        reload_state=reload_state,
        **handler_kwargs,
    )
    server = ThreadingHTTPServer((config.host, config.port), handler_factory)

    try:
        print(f"serving {config.output_dir} at http://{config.host}:{config.port}/")
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
        server.server_close()


def _watch_for_changes(
    builder: StaticSiteBuilder,
    site_config,
    config: DevServerConfig,
    reload_state: ReloadState,
    watch_targets: tuple[Path, ...],
    stop_event: threading.Event,
) -> None:
    previous_signature = _filesystem_signature(watch_targets)
    while not stop_event.wait(POLL_INTERVAL_SECONDS):
        current_signature = _filesystem_signature(watch_targets)
        if current_signature == previous_signature:
            continue
        catalog = load_content_catalog(
            loader=MarkdownContentLoader(),
            content_root=config.content_root,
        )
        builder.build(site_config, catalog)
        reload_state.bump()
        previous_signature = current_signature


def _filesystem_signature(paths: tuple[Path, ...]) -> tuple[tuple[str, int, int], ...]:
    entries: list[tuple[str, int, int]] = []
    for root in paths:
        if root.is_file():
            stat = root.stat()
            entries.append((str(root), int(stat.st_mtime_ns), int(stat.st_size)))
            continue
        if not root.exists():
            entries.append((str(root), 0, 0))
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file():
                stat = path.stat()
                entries.append((str(path), int(stat.st_mtime_ns), int(stat.st_size)))
    return tuple(entries)


def _inject_reload_script(html: str) -> str:
    if RELOAD_CHECK_PATH in html:
        return html
    if "</body>" in html:
        return html.replace("</body>", f"{RELOAD_SCRIPT}\n  </body>")
    return html + "\n" + RELOAD_SCRIPT


if __name__ == "__main__":
    main()
