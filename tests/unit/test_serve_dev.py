from __future__ import annotations

from http.server import ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
import threading
import urllib.request

from src.app.interfaces.cli.serve_dev import DevRequestHandler, ReloadState
from src.app.interfaces.cli import serve_dev


def test_current_repository_revision_marks_dirty_worktree(monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    calls: list[tuple[tuple[str, ...], Path]] = []

    def fake_run(command, cwd, check, capture_output, text):
        calls.append((tuple(command), cwd))
        if command == ["git", "rev-parse", "--short", "HEAD"]:
            return SimpleNamespace(stdout="abc1234\n")
        if command == ["git", "status", "--porcelain"]:
            return SimpleNamespace(stdout=" M src/app/interfaces/cli/serve_dev.py\n")
        raise AssertionError(command)

    monkeypatch.setattr(serve_dev.subprocess, "run", fake_run)

    assert serve_dev._current_repository_revision() == "abc1234-dirty"
    assert calls == [
        (("git", "rev-parse", "--short", "HEAD"), repo_root),
        (("git", "status", "--porcelain"), repo_root),
    ]


def test_dev_status_endpoint_reports_commit_and_reload_version(tmp_path: Path) -> None:
    output_dir = tmp_path / "dist"
    output_dir.mkdir()
    (output_dir / "404.html").write_text("<!doctype html>", encoding="utf-8")

    reload_state = ReloadState()
    reload_state.bump()

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        lambda *args, **kwargs: DevRequestHandler(
            *args,
            directory=str(output_dir),
            reload_state=reload_state,
            repository_revision="abc1234",
            **kwargs,
        ),
    )
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        port = server.server_address[1]
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}/__dev_status__",
            timeout=5,
        ) as response:
            payload = response.read().decode("utf-8")

        assert response.status == 200
        assert "commit=abc1234" in payload
        assert "reload=1" in payload
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
