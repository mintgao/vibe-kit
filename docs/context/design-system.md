# Interaction context

This version is a command-line and documentation scaffold with no graphical design system.

## CLI conventions

- Commands are non-interactive and accept an explicit target path.
- Successful operational summaries are written to standard output.
- User-facing errors and failed verification summaries are written to standard error.
- Exit code `0` means success, `1` means verification or diagnostic failure, and `2` means a usage, installation, or managed-file conflict prevented the operation.
- Potentially destructive ambiguity stops the operation and leaves an inspectable conflict candidate instead of overwriting content.

## Documentation conventions

- Durable project truth belongs in `docs/context/`.
- Bounded requirements and evidence belong in `docs/work-items/`.
- Decisions with consequences beyond one work item belong in `docs/decisions/`.
