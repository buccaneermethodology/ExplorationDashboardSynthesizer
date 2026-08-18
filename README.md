# Exploration Dashboard Synthesizer

[![validate](https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer/actions/workflows/validate.yml/badge.svg)](https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer/actions/workflows/validate.yml)
[![GitHub release](https://img.shields.io/github/v/release/buccaneermethodology/ExplorationDashboardSynthesizer)](https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer/releases)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Exploration Dashboard Synthesizer** is an OpenClaw and Codex-compatible skill that transforms unstructured exploration material into a structured **Exploration Dashboard**.

It is designed for notes, conversations, brainstorming fragments, research discussions, and AI collaboration traces where the goal is still emerging. The skill turns raw material into Big Ideas, Sessions, key points, next suggestions, assumptions, and unresolved questions.

The synthesis principle is simple: preserve structure faithfully. The Dashboard is a cognitive coordination artifact, not a narrative summary.

## What It Does

- Extracts major themes and clusters them into **Big Ideas**.
- Converts concrete fragments into **Sessions**.
- Classifies Sessions as `Exploration`, `Knowledge`, or `Proposed`.
- Separates supported insights from assumptions and unresolved questions.
- Produces a Markdown Dashboard that can be reviewed, edited, and evolved.
- Optionally renders that Dashboard as a self-contained HTML panorama with interactive views, filters, sorting, pagination, URL state, and a detail drawer.
- Keeps unsupported ideas out of conclusions and places ambiguous material into Proposed Sessions or Unresolved Questions.
- Keeps Session Type separate from governed lifecycle Status when the output is projected into an existing repository Dashboard.

## When To Use It

Use this skill for:

- meeting notes from exploratory discussions
- brainstorming fragments
- research or strategy notes
- long AI conversation transcripts
- workshop notes
- early-stage product or methodology exploration
- scattered project knowledge that needs a first Dashboard structure

Do not use it as a replacement for:

- a normal task tracker when the work is already well-defined
- a final report or polished narrative article
- a formal requirements document
- an architecture decision record
- a bug tracker or implementation backlog

## Core Concepts

- **Big Idea**: a long-lived exploration direction that can contain multiple Sessions.
- **Session**: a bounded exploration unit associated with a Big Idea.
- **Exploration Session**: something that already happened.
- **Knowledge Session**: an existing artifact, method, metric, concept, or reusable module.
- **Proposed Session**: a suggested future exploration topic.
- **Coverage**: an estimated progress signal. Use `Unknown` when unsupported by the input.

See [docs/core-concepts.md](docs/core-concepts.md) for the full reference.

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer.git
cd ExplorationDashboardSynthesizer
```

### 2. Install as a Codex skill

Install the Codex-compatible skill path directly from GitHub:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo buccaneermethodology/ExplorationDashboardSynthesizer \
  --path skill/exploration-dashboard-synthesizer
```

Restart Codex after installation, then invoke it with `$exploration-dashboard-synthesizer`.

### 3. Use with OpenClaw

Import [skill.json](skill.json) into your OpenClaw environment.

Example CLI usage:

```bash
openclaw run exploration-dashboard-synthesizer \
  --input "examples/meeting-notes.input.txt" \
  --output dashboard.md
```

### 4. Use as a direct prompt

If you are not using OpenClaw, copy the prompt from [prompt.md](prompt.md), paste it into a capable LLM, and replace `{{input_text}}` with your material.

### 5. Review the output

Treat the generated Dashboard as a working artifact. Review unsupported assumptions, rename Big Ideas if needed, and adjust Session boundaries before using it for coordination.

### 6. Render an interactive HTML panorama

The Markdown file remains the primary output. To create a portable, offline HTML projection:

```bash
python3 scripts/render_dashboard.py examples/meeting-notes.dashboard.md /tmp/exploration-dashboard.html
```

For richer Big Idea/Stage Plan relationships, statuses, source locators, and phase tags, use the documented JSON shape:

```bash
python3 scripts/render_dashboard.py examples/dashboard.json /tmp/exploration-dashboard.html
```

The generated page includes overview, Big Idea, Stage Plan, and Session views; keyword and field filters; sorting; pagination; URL-hash state; and a detail drawer. See [HTML renderer reference](references/html-renderer.md). The page is a derived read model and does not mutate the source Dashboard.

## Examples

| Input | Expected Dashboard |
| --- | --- |
| [meeting-notes.input.txt](examples/meeting-notes.input.txt) | [meeting-notes.dashboard.md](examples/meeting-notes.dashboard.md) |
| [ai-conversation.input.txt](examples/ai-conversation.input.txt) | [ai-conversation.dashboard.md](examples/ai-conversation.dashboard.md) |

Minimal input:

```text
Meeting notes:
- Alice: We tried using knowledge graphs for fault diagnosis, but accuracy is only 70%.
- Bob: I think we need higher quality knowledge, maybe extract rules from expert experience.
- Carol: Let us form a task force and start a pilot next month, target accuracy above 85%.
```

Expected output shape:

```markdown
# Exploration Dashboard

## Big Idea: Fault Diagnosis with Knowledge Graph
- Big Idea Length: Unknown
- Coverage: Unknown
- Key Points:
  - The current knowledge graph diagnosis approach has unstable accuracy around 70%.
- Next Suggestions:
  - Explore methods for incorporating expert rules into the diagnosis knowledge graph.

### Sessions
| Session ID | Session Type | Topic | Scope | Purpose | Length (minutes) | Key Points |
|------------|--------------|-------|-------|---------|-------------------|------------|
| B1-K1 | Knowledge | Current diagnosis status | Knowledge graph based fault diagnosis | Capture the current baseline and pain point | - | Accuracy is around 70% and unstable. |
```

## Skill Files

| File | Purpose |
| --- | --- |
| [skill.json](skill.json) | OpenClaw skill package metadata and prompt template. |
| [skill/exploration-dashboard-synthesizer/SKILL.md](skill/exploration-dashboard-synthesizer/SKILL.md) | Codex-compatible skill entry point for installation from GitHub. |
| [prompt.md](prompt.md) | Human-readable source for the prompt template. |
| [docs/core-concepts.md](docs/core-concepts.md) | Concept definitions and output structure. |
| [docs/bm-dashboard.md](docs/bm-dashboard.md) | BM Dashboard methodology article. |
| [examples/](examples/) | Sample inputs, expected Dashboard outputs, and a renderer JSON example. |
| [scripts/render_dashboard.py](scripts/render_dashboard.py) | Generates a self-contained, filterable HTML projection from Markdown or JSON. |
| [scripts/validate_repo.py](scripts/validate_repo.py) | Repository validation script used by CI. |
| [scripts/sync_prompt.py](scripts/sync_prompt.py) | Syncs `prompt.md` into `skill.json`. |

## Relationship To Dashboard Governance

This repository creates an initial Exploration Dashboard from unstructured material.

For ongoing project-state maintenance after a Dashboard exists, use [dashboard-governance-skill](https://github.com/buccaneermethodology/dashboard-governance-skill). The two repositories are complementary:

| Repository | Role |
| --- | --- |
| `ExplorationDashboardSynthesizer` | Synthesizes the initial Dashboard from raw material. |
| `dashboard-governance-skill` | Maintains Big Ideas, Sessions, Decisions, status, and emergent next steps during ongoing work. |

### Governed Status Projection

Standalone synthesis does not require a Status column. If you ask the skill to write into an existing governed repository Dashboard, it first discovers and reads that project's Dashboard governance contract; the repository contract, not this portable skill, is the Status authority.

- A new candidate Session uses lifecycle Status `todo`.
- Use `decision-needed` only when a real choice is pending, and reference the governing Decision.
- `Proposed` remains a Session Type; it is not the lifecycle Status `proposed`.
- Never use `active`, `proposed`, `partial`, or `bounded-*` as lifecycle Status values.
- If no contract is discoverable, retain the standalone output and do not claim governed conformance.

No private repository path is required. Contract discovery is conditional on the target repository's capabilities.

## v1.3.1 Upgrade Notes

Version `1.3.1` keeps the governed-Status projection rules from `1.2.0` and the renderer from `1.3.0`, and bundles the renderer, reference, and example JSON inside the installable Codex Skill directory. Installing only `skill/exploration-dashboard-synthesizer` is now sufficient for complete HTML functionality. Existing Markdown synthesis remains the primary output and is backward compatible.

## Validate

Run the repository validator:

```bash
python3 scripts/validate_repo.py
python3 tests/test_renderer.py
```

The validator checks:

- required repository files
- `skill.json` structure
- `prompt.md` and `skill.json` prompt synchronization
- package version `1.3.1` and governed-Status markers across prompt, Codex Skill, references, README, and examples
- Codex-compatible `SKILL.md` path and metadata
- local Markdown links

If you edit [prompt.md](prompt.md), sync it into [skill.json](skill.json):

```bash
python3 scripts/sync_prompt.py
python3 scripts/validate_repo.py
```

If you have Codex's skill creator validator available, validate the installable skill path too:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skill/exploration-dashboard-synthesizer
```

## References

- [BM Dashboard methodology article](docs/bm-dashboard.md)
- [Original WeChat article](https://mp.weixin.qq.com/s/9XrmJUYoRppsLkl4JVnkBQ)
- [dashboard-governance-skill](https://github.com/buccaneermethodology/dashboard-governance-skill)

## Contributing

Issues and pull requests are welcome. Useful contributions include:

- clearer prompt wording
- additional examples
- output-format refinements
- portability notes for other agent environments
- validation improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).

## Maintenance

- Maintainer: Tai Xiaomei <buccaneermethodology@gmail.com>
- GitHub: [@buccaneermethodology](https://github.com/buccaneermethodology)
