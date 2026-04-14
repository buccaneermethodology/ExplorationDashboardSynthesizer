# Exploration Dashboard Synthesizer

[![validate](https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer/actions/workflows/validate.yml/badge.svg)](https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer/actions/workflows/validate.yml)
[![GitHub release](https://img.shields.io/github/v/release/buccaneermethodology/ExplorationDashboardSynthesizer)](https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer/releases)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Exploration Dashboard Synthesizer** is an OpenClaw skill that transforms unstructured exploration material into a structured **Exploration Dashboard**.

It is designed for notes, conversations, brainstorming fragments, research discussions, and AI collaboration traces where the goal is still emerging. The skill turns raw material into Big Ideas, Sessions, key points, next suggestions, assumptions, and unresolved questions.

The synthesis principle is simple: preserve structure faithfully. The Dashboard is a cognitive coordination artifact, not a narrative summary.

## What It Does

- Extracts major themes and clusters them into **Big Ideas**.
- Converts concrete fragments into **Sessions**.
- Classifies Sessions as `Exploration`, `Knowledge`, or `Proposed`.
- Separates supported insights from assumptions and unresolved questions.
- Produces a Markdown Dashboard that can be reviewed, edited, and evolved.
- Keeps unsupported ideas out of conclusions and places ambiguous material into Proposed Sessions or Unresolved Questions.

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

### 2. Use with OpenClaw

Import [skill.json](skill.json) into your OpenClaw environment.

Example CLI usage:

```bash
openclaw run exploration-dashboard-synthesizer \
  --input "examples/meeting-notes.input.txt" \
  --output dashboard.md
```

### 3. Use as a direct prompt

If you are not using OpenClaw, copy the prompt from [prompt.md](prompt.md), paste it into a capable LLM, and replace `{{input_text}}` with your material.

### 4. Review the output

Treat the generated Dashboard as a working artifact. Review unsupported assumptions, rename Big Ideas if needed, and adjust Session boundaries before using it for coordination.

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
| [prompt.md](prompt.md) | Human-readable source for the prompt template. |
| [docs/core-concepts.md](docs/core-concepts.md) | Concept definitions and output structure. |
| [docs/bm-dashboard.md](docs/bm-dashboard.md) | BM Dashboard methodology article. |
| [examples/](examples/) | Sample inputs and expected Dashboard outputs. |
| [scripts/validate_repo.py](scripts/validate_repo.py) | Repository validation script used by CI. |
| [scripts/sync_prompt.py](scripts/sync_prompt.py) | Syncs `prompt.md` into `skill.json`. |

## Relationship To Dashboard Governance

This repository creates an initial Exploration Dashboard from unstructured material.

For ongoing project-state maintenance after a Dashboard exists, use [dashboard-governance-skill](https://github.com/buccaneermethodology/dashboard-governance-skill). The two repositories are complementary:

| Repository | Role |
| --- | --- |
| `ExplorationDashboardSynthesizer` | Synthesizes the initial Dashboard from raw material. |
| `dashboard-governance-skill` | Maintains Big Ideas, Sessions, Decisions, status, and emergent next steps during ongoing work. |

## Validate

Run the repository validator:

```bash
python3 scripts/validate_repo.py
```

The validator checks:

- required repository files
- `skill.json` structure
- `prompt.md` and `skill.json` prompt synchronization
- local Markdown links

If you edit [prompt.md](prompt.md), sync it into [skill.json](skill.json):

```bash
python3 scripts/sync_prompt.py
python3 scripts/validate_repo.py
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
