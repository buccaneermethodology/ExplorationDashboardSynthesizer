# Exploration Dashboard

## Big Idea: AI-Assisted Exploration Continuity
- Big Idea Length: Unknown
- Coverage: Unknown
- Key Points:
  - Context loss across AI sessions is a recurring problem.
  - A Dashboard can separate long-running directions from bounded work sessions.
  - Decisions need their own explicit surface when they affect multiple future steps.
- Next Suggestions:
  - Test whether AI can update the Dashboard after each non-trivial task.
  - Define status and decision rules before relying on automated updates.

### Sessions
| Session ID | Session Type | Topic | Scope | Purpose | Length (minutes) | Key Points |
|------------|--------------|-------|-------|---------|-------------------|------------|
| B1-E1 | Exploration | Context continuity issue | AI session handoff | Capture the problem caused by losing context between sessions | Unknown | Session switching causes project-state loss. |
| B1-K1 | Knowledge | Dashboard separation model | Project state structure | Preserve the distinction between long-running directions and bounded sessions | - | Big Ideas and Sessions should not be collapsed. |
| B1-K2 | Knowledge | Decision visibility | Cross-session decision management | Keep multi-session choices outside task notes | - | Decisions affect future steps and need explicit tracking. |
| B1-P1 | Proposed | AI dashboard update experiment | End-of-task workflow | Test whether AI can maintain Dashboard state after meaningful work | - | The next experiment is to automate Dashboard updates after tasks. |

### Assumptions
- The fragments describe a project workflow problem, not a completed implementation.

### Unresolved Questions
- What fields should be mandatory for each Dashboard row?
- What quality gate should decide whether AI-generated Dashboard updates are acceptable?

### Governed Projection Note

This standalone example intentionally omits a Status column. If it is projected into a governed repository whose Dashboard contract permits `todo`, `B1-P1` keeps Session Type `Proposed` and receives lifecycle Status `todo`. It uses `decision-needed` only if a real choice is pending and then references the governing Decision; `active`, `proposed`, `partial`, and `bounded-*` are not lifecycle Status values.
