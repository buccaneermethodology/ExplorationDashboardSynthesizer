# Exploration Dashboard Synthesizer

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Exploration Dashboard Synthesizer** is an OpenClaw skill that transforms unstructured information (meeting notes, brainstorming fragments, documentation excerpts, etc.) into a structured **Exploration Dashboard**. This dashboard helps teams:

- Understand major exploration directions
- Track progress
- Align shared understanding
- Organize future work

The principles of synthesizing emphasizes faithful structuring over creativity, and treats the dashboard as a cognitive coordination artifact, not a narrative summary.

## ✨ Features

- Extracts themes and clusters them into **Big Ideas** (long-lived exploration directions).
- Identifies **Sessions** (exploration units) and classifies them as:
  - `Exploration` – activities that already happened.
  - `Knowledge` – existing artifacts or conceptual modules.
  - `Proposed` – suggested future topics.
- Summarizes key insights and suggests next steps for each Big Idea.
- Outputs a clean, human-readable Markdown table structure.

## 🚀 Quick Start

### Prerequisites
- [OpenClaw](https://github.com/openclaw) environment (or any platform that can execute the skill's prompt template).
- A large language model (e.g., GPT-4, Claude) with good structured output capabilities.

### Installation
1. Clone this repository:
```bash
git clone https://github.com/yourusername/exploration-dashboard-synthesizer.git
```

2. Import skill.json into your OpenClaw instance (or copy the prompt template manually).

Usage via OpenClaw CLI

```bash
openclaw run exploration-dashboard-synthesizer \
  --input "path/to/your/unstructured/text.txt" \
  --output dashboard.md
```

Usage via Direct Prompt

If you are not using OpenClaw, you can paste the prompt template (from skill.json) into a chat with a compatible LLM, then append your unstructured information.

### 📖 Reference

For a detailed explanation of the core concepts (Big Ideas, Sessions, Session Types) and the structuring process, please see reference.md.

### 🧪 Example

Input

```
Meeting notes:
- Alice: We tried using knowledge graphs for fault diagnosis, but accuracy is only 70%.
- Bob: I think we need higher quality knowledge, maybe extract rules from expert experience.
- Carol: Let's form a task force and start a pilot next month, target accuracy >85%.
```

Output

```markdown
# Exploration Dashboard

## Big Idea: Fault Diagnosis with Knowledge Graph (基于知识图谱的故障诊断)
- Big Idea Length: 0 minutes
- Coverage: 0%
- Key Points:
  - Current knowledge graph diagnosis accuracy is only 70%, unstable.
  - Need to incorporate expert experience rules to improve quality.
- Next Suggestions:
  - Form a task force and plan a pilot.
  - Research methods to integrate expert rules into the graph.

### Sessions
| Session ID | Session Type | Topic                         | Scope               | Purpose                                            | Length (minutes) | Key Points                          |
|------------|--------------|-------------------------------|---------------------|----------------------------------------------------|------------------|-------------------------------------|
| B1-K1      | Knowledge    | Current fault diagnosis status| Fault diagnosis     | Document the current state and pain points        | -                | Accuracy 70%, unstable.             |
| B1-P1      | Proposed     | Incorporate expert rules      | Knowledge graph enhancement | Explore how to extract rules from expert experience | -                | May improve diagnosis quality.       |
| B1-P2      | Proposed     | Form task force & pilot       | Organization & plan | Define responsibilities and timeline for pilot     | -                | Launch next month, target 85%+.      |
```

### 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements, bug fixes, or additional features.

· Optimize the prompt – improve clarity or output quality.
· Support more input formats – e.g., direct audio transcription.
· Add multi-language support – generate dashboards in other languages.

### 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

### 📬 Contact

Maintainer: Tai Xiaomei buccaneermethodology@gmail.com
GitHub: @buccanneermethodology

---

Happy exploring! 🧭

```
