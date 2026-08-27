# 0001: Separate framework files, installation state, and project context

- Status: Accepted
- Date: 2026-08-27

## Decision

Vibe Kit uses three ownership classes:

1. Framework-managed files may be replaced by a safe upgrade: files recorded in the manifest plus the marked Vibe Kit block in `AGENTS.md`.
2. Tool-maintained installation state is written by the CLI but is not incoming framework content: `.vibe/manifest.json`, `.vibe/version`, and `.vibe/conflicts/` candidates.
3. Project-owned context is never overwritten by upgrade: project configuration, project rules, context, work items, and decision records.

Before updating a managed file, the CLI compares its current hash with the hash recorded at installation. If both the local file and the incoming framework file changed, the upgrade aborts without applying managed-file changes and writes incoming candidates under `.vibe/conflicts/`.

## Consequences

- Existing projects can adopt the workflow without merging Git histories.
- Local edits to managed files are detected rather than silently lost.
- Project-specific changes belong in project-owned files or outside the managed block.
- Installation state should be inspected through CLI diagnostics rather than edited as project configuration.
