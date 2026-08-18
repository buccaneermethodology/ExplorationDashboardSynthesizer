# HTML Renderer

`scripts/render_dashboard.py` converts the Skill's standard Markdown output or a richer JSON Dashboard into a self-contained HTML file. The page runs without a server or external assets and provides the same interaction pattern as the Semx full-cycle panorama: overview, Big Idea, Stage Plan and Session views; keyword and field filters; sorting; pagination; URL-hash state; detail drawer; and reset.

## Usage

```bash
python3 scripts/render_dashboard.py examples/dashboard.json /tmp/exploration-dashboard.html
python3 scripts/render_dashboard.py examples/meeting-notes.dashboard.md /tmp/meeting-notes.html
```

The renderer does not mutate the source Dashboard. It is a derived read model.

## JSON shape

The minimal input is:

```json
{
  "title": "Exploration Dashboard",
  "subtitle": "A derived, offline view",
  "big_ideas": [{"id": "B1", "topic": "...", "key_points": [], "next_suggestions": []}],
  "sessions": [{
    "id": "B1-E1", "type": "Exploration", "topic": "...",
    "scope": "...", "purpose": "...", "length": "Unknown",
    "key_points": ["..."], "big_ideas": ["B1"],
    "status": "todo", "phase_tags": []
  }]
}
```

`stage_plans`, `recommendations`, and `source_manifest` are optional. Extra fields are preserved and shown in the detail drawer. A Markdown input is parsed using the standard table emitted by the Skill; JSON is recommended when status, relationships, or source metadata matter.

## Claim boundary

The HTML is a portable, offline, human-readable projection. It is not a canonical source of truth, approval receipt, semantic correctness verdict, or production-readiness evidence. When used in a governed repository, keep the repository's Dashboard/registry as the authority and publish the HTML alongside a source pointer.
