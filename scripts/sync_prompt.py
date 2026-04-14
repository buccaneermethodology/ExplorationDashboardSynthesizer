#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    prompt = (ROOT / "prompt.md").read_text(encoding="utf-8").rstrip("\n")
    skill_path = ROOT / "skill.json"
    skill = json.loads(skill_path.read_text(encoding="utf-8"))
    skill["prompt_template"] = prompt
    skill_path.write_text(json.dumps(skill, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("synced prompt.md -> skill.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
