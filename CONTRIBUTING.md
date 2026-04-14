# Contributing

Thank you for improving Exploration Dashboard Synthesizer.

## Good Contributions

Useful pull requests usually improve one of these areas:

- prompt clarity
- output structure
- examples
- Dashboard methodology references
- validation scripts
- portability to other AI skill runtimes

## Development Workflow

1. Edit `prompt.md` when changing the prompt.
2. Run `python3 scripts/sync_prompt.py` to update `skill.json`.
3. Add or update examples when prompt behavior changes.
4. Run `python3 scripts/validate_repo.py` before committing.

## Pull Request Checklist

- [ ] `python3 scripts/validate_repo.py` passes.
- [ ] `skill.json` is valid JSON.
- [ ] `prompt.md` and `skill.json` are synchronized.
- [ ] README links still resolve.
- [ ] Examples are updated if output semantics changed.
- [ ] The change does not encourage unsupported invention by the model.

## Prompt Design Principles

- Prefer faithful structuring over creative summarization.
- Preserve uncertainty explicitly.
- Use Proposed Sessions for ambiguous future directions.
- Do not force estimates when the input does not support them.
- Keep generated Dashboards easy to review and edit.
