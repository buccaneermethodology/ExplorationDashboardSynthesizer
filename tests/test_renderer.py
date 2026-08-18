from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_dashboard.py"


def test_json_render() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "dashboard.html"
        subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "examples/dashboard.json"), str(output)], check=True)
        page = output.read_text(encoding="utf-8")
        assert '<select id="status">' in page
        assert "data-view=\"session\"" in page
        assert "dashboard-data" in page
        assert "B1-K1" in page
        assert "URLSearchParams" in page


def test_markdown_render() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "dashboard.html"
        subprocess.run([sys.executable, str(SCRIPT), str(ROOT / "examples/meeting-notes.dashboard.md"), str(output)], check=True)
        page = output.read_text(encoding="utf-8")
        assert "Exploration Dashboard" in page
        assert "dashboard-data" in page


def test_json_is_embedded_safely() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "input.json"
        source.write_text(json.dumps({"title": "<safe>", "big_ideas": [], "sessions": []}), encoding="utf-8")
        output = Path(tmp) / "dashboard.html"
        subprocess.run([sys.executable, str(SCRIPT), str(source), str(output)], check=True)
        page = output.read_text(encoding="utf-8")
        assert "\\u003c" in page
        assert "<safe>" not in page
