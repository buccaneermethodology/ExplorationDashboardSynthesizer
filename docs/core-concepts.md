# Exploration Dashboard Core Concepts

This document defines the key concepts used in the Exploration Dashboard, serving as a reference for both human users and AI agents.

## 1. Dashboard Overview
An Exploration Dashboard is a structured artifact that organizes unstructured information (conversations, notes, ideas) into a map of an evolving exploration space. It helps teams:
- See the landscape of possible directions
- Track progress made
- Identify where to explore next

## 2. Core Concepts

### 2.1 Big Idea
A **Big Idea** is a long-lived exploration direction, a conceptual or engineering path that can host multiple Sessions over time.

**Characteristics:**
- Represents a coherent intellectual direction
- Can grow and evolve over time
- Should not collapse unrelated ideas into one
- Examples: "Knowledge Engineering Infrastructure", "Agent-Based Software Development", "Legacy System Capability Mining"

### 2.2 Session (Generalized)
A **Session** is a bounded exploration unit associated with a Big Idea. It may represent:
- An exploration activity that already happened
- An existing knowledge module (methodology, metric, framework)
- A proposed topic for future investigation

Sessions must be specific and actionable.

### 2.3 Session Types
Each Session must have one of the following types:

| Type         | Description                                                                 | Examples                                                                 |
|--------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------|
| Exploration  | A real exploration activity that already occurred.                          | A design discussion, a conceptual debate, an implementation planning session |
| Knowledge    | An existing knowledge artifact or conceptual module.                        | A methodology, a defined metric, a documented framework                  |
| Proposed     | A suggested exploration topic that could become a future Session.           | "Design a capability linter", "Build an M1 extractor CLI"                |

Session Type and lifecycle Status answer different questions. `Proposed` says what kind of Session it is; it must not be copied into a lowercase `proposed` Status value.

### 2.4 Governed Repository Projection

The default output is a standalone synthesis and does not require a Status column. When a user asks to project the result into an existing governed repository Dashboard:

1. Discover and read that project's Dashboard governance contract before choosing Status values.
2. Treat the contract's Status enum as authority and preserve any separate state axes.
3. Give a new candidate Session lifecycle Status `todo`.
4. Use `decision-needed` only when a real choice is pending, and reference the governing Decision.
5. Never use `active`, `proposed`, `partial`, or `bounded-*` as lifecycle Status values.

If no project contract is discoverable, keep the standalone synthesis and state that governed conformance was not established. Do not depend on a private repository path or assume one universal contract location.

## HTML projection

The Markdown Dashboard is the primary output. For a human-readable interactive view, `scripts/render_dashboard.py` can render either the standard Markdown output or the richer JSON shape into a self-contained offline HTML file. The projection offers overview, Big Idea, Stage Plan, and Session views, keyword and field filters, sorting, pagination, URL-hash state, and a detail drawer. It is a derived read model: it does not replace the Dashboard/registry source or authorize status changes. See [HTML renderer reference](../references/html-renderer.md).

## 3. Dashboard Structure

### 3.1 Header
Optional metadata (version, mode, input scope) can be included at the top.

### 3.2 Big Idea Tables
Each Big Idea appears as a separate table with the following fields:

| Field            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| Big Idea         | English name + Chinese conceptual abstraction (optional)                    |
| Big Idea Length  | Sum of durations of all Exploration Sessions under this Big Idea (minutes)  |
| Coverage (%)     | Estimated exploration progress (0-100%)                                     |
| Key Points       | Major insights already established                                           |
| Next Suggestions | Possible future exploration topics                                           |

### 3.3 Session Table
Each Big Idea contains a Session table with the following columns:

| Column          | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| Session ID      | Unique identifier (e.g., B1-E1, B2-K3)                                      |
| Session Type    | Exploration / Knowledge / Proposed                                          |
| Topic           | Session topic                                                               |
| Scope           | What area the Session covers                                                |
| Purpose         | Why this Session exists                                                     |
| Length (minutes)| Estimated duration (only for Exploration Sessions)                          |
| Key Points      | Concrete insights or expected outcomes                                      |

## 4. Structuring Process
When synthesizing a Dashboard from raw material, follow these steps:
1. **Theme Extraction** – Identify major conceptual directions → become **Big Ideas**.
2. **Idea Clustering** – Group related information under the same Big Idea.
3. **Exploration Unit Identification** – Convert information fragments into **Sessions**.
4. **Session Typing** – Assign each Session one of the three types.
5. **Knowledge Consolidation** – Summarize major insights under **Key Points** for each Big Idea.

## 5. Accuracy Rules
- Do not fabricate exploration events or insights unsupported by the material.
- If the material is ambiguous, prefer creating a Proposed Session instead of inventing conclusions.
- Multiple Big Ideas are expected; do not merge unrelated ideas.

## 6. Guiding Principle
The Dashboard is not a summary. It is a map of an evolving exploration space. Accuracy, stability, and structural clarity are more important than elegance.
