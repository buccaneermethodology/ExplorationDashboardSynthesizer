#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "skill.json",
    "prompt.md",
    "docs/core-concepts.md",
    "docs/bm-dashboard.md",
    "examples/meeting-notes.input.txt",
    "examples/meeting-notes.dashboard.md",
    "examples/ai-conversation.input.txt",
    "examples/ai-conversation.dashboard.md",
]
REQUIRED_SKILL_FIELDS = [
    "name",
    "version",
    "description",
    "author",
    "license",
    "repository",
    "inputs",
    "outputs",
    "prompt_template",
]


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_skill(errors: list[str]) -> None:
    skill_path = ROOT / "skill.json"
    try:
        skill = json.loads(skill_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"skill.json is invalid JSON: {exc}", errors)
        return

    for field in REQUIRED_SKILL_FIELDS:
        if field not in skill:
            fail(f"skill.json missing required field: {field}", errors)

    if skill.get("name") != "exploration-dashboard-synthesizer":
        fail("skill.json name should be exploration-dashboard-synthesizer", errors)
    if skill.get("license") != "MIT":
        fail("skill.json license should be MIT", errors)
    if not isinstance(skill.get("inputs"), list) or not skill.get("inputs"):
        fail("skill.json inputs must be a non-empty list", errors)
    if not isinstance(skill.get("outputs"), list) or not skill.get("outputs"):
        fail("skill.json outputs must be a non-empty list", errors)

    prompt = (ROOT / "prompt.md").read_text(encoding="utf-8").rstrip("\n")
    if skill.get("prompt_template") != prompt:
        fail("skill.json prompt_template is not synchronized with prompt.md", errors)


def validate_required_files(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"required file missing: {rel}", errors)


def validate_markdown_links(errors: list[str]) -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for md_path in ROOT.rglob("*.md"):
        if ".git" in md_path.parts:
            continue
        text = md_path.read_text(encoding="utf-8")
        for raw_link in pattern.findall(text):
            link = raw_link.split("#", 1)[0].strip()
            if not link or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
                continue
            target = (md_path.parent / unquote(link)).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"{md_path.relative_to(ROOT)} links outside repository: {raw_link}", errors)
                continue
            if not target.exists():
                fail(f"{md_path.relative_to(ROOT)} has broken local link: {raw_link}", errors)


def main() -> int:
    errors: list[str] = []
    validate_required_files(errors)
    if (ROOT / "skill.json").exists() and (ROOT / "prompt.md").exists():
        validate_skill(errors)
    validate_markdown_links(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
