---
name: exploration-dashboard-synthesizer
description: Transform unstructured notes, transcripts, articles, meeting fragments, or AI conversation history into a BM-style Exploration Dashboard with Big Ideas, typed Sessions, assumptions, unresolved questions, key points, and next suggestions. Use when the user asks to synthesize, create, initialize, or build an Exploration Dashboard from raw material, especially before ongoing dashboard governance begins.
---

# Exploration Dashboard Synthesizer

## Purpose

Use this skill to turn messy exploration material into an initial BM-style Exploration Dashboard. The Dashboard is a cognitive coordination artifact, not a narrative summary: prefer faithful structuring, visible uncertainty, and actionable exploration units.

Use `$dashboard-governance` instead when a repository already has a Dashboard and the task is to maintain task state, mark sessions complete, record decisions, or identify emergent next sessions after project work.

## Workflow

1. Identify the input scope: meeting notes, brainstorming fragments, docs, article text, AI conversation history, or mixed material.
2. Extract major themes and cluster them into Big Ideas. Use multiple Big Ideas when directions are meaningfully different.
3. Convert concrete fragments into Sessions under the relevant Big Idea. Set a new candidate to lifecycle Status `todo` only when projecting into a governed repository; use `decision-needed` only for a real pending choice and reference its Decision.
4. Classify each Session as `Exploration`, `Knowledge`, or `Proposed`.
5. Summarize supported insights under Key Points and future options under Next Suggestions.
6. Preserve uncertainty with Assumptions and Unresolved Questions instead of inventing conclusions.
7. Keep the output concise enough to become a working Dashboard.

## Session Types

- `Exploration`: a real exploration activity that already happened.
- `Knowledge`: an existing knowledge artifact, method, metric, concept, or reusable module.
- `Proposed`: a suggested exploration topic that could become a future Session.

Only `Exploration` Sessions contribute to Big Idea Length. Use `Unknown` when a length or coverage estimate is not supported by the input. Use `-` or `N/A` for Knowledge and Proposed Session length.

## Output Format

```markdown
# Exploration Dashboard

## Big Idea: [short name; bilingual label optional]
- Big Idea Length: [sum of Exploration Session lengths, or Unknown]
- Coverage: [estimated exploration progress, or Unknown]
- Key Points:
  - [major insights already supported by the input]
- Next Suggestions:
  - [possible future exploration topics]

### Sessions
| Session ID | Session Type | Topic | Scope | Purpose | Length (minutes) | Key Points |
|------------|--------------|-------|-------|---------|-------------------|------------|
| B1-E1 | Exploration | ... | ... | ... | Unknown | ... |

### Assumptions
- [Only include assumptions needed to interpret ambiguous material. Use "None" if not needed.]

### Unresolved Questions
- [Questions that should not be invented into conclusions. Use "None" if not needed.]
```

## Accuracy Rules

- Do not fabricate events, insights, participants, decisions, or outcomes unsupported by the input.
- If material is ambiguous, prefer a Proposed Session or an Unresolved Question.
- Do not force bilingual labels; use them only when the input or user context makes them useful.
- Do not merge unrelated directions into a single Big Idea for neatness.
- Use stable, readable Session IDs such as `B1-E1`, `B1-K1`, and `B1-P1`.
- Keep Session Type separate from lifecycle Status: `Proposed` is a Session Type, not a Status value.
- Keep standalone synthesis portable and omit a Status column unless the user or target format requests one.
- Before projecting into a governed repository Dashboard, discover and read that project's Dashboard governance contract. Use its Status enum as authority and preserve separate state axes.
- For a governed projection, give each new candidate lifecycle Status `todo`. Use `decision-needed` only when a real choice is pending and include a reference to the governing Decision.
- Never emit `active`, `proposed`, `partial`, or `bounded-*` as lifecycle Status values. If the repository has no discoverable governance contract, retain the standalone output and do not claim governed conformance.

## Optional HTML projection

The Markdown Dashboard is the primary output. When an interactive panorama is requested, save the Markdown output and run the bundled `scripts/render_dashboard.py` with the Markdown path and an HTML output path. For richer relationships, statuses, phase tags, and source metadata, provide the JSON shape described in [`references/html-renderer.md`](references/html-renderer.md). The generated single-file page includes overview, Big Idea, Stage Plan, and Session views, keyword/field filters, sorting, pagination, URL-hash state, and a detail drawer. It is a derived read model and must not be treated as canonical Dashboard truth or an approval receipt.

## References

Read `references/core-concepts.md` when the task needs deeper BM Dashboard semantics, field meanings, or examples of Big Idea and Session distinctions.

Source project: https://github.com/buccaneermethodology/ExplorationDashboardSynthesizer
