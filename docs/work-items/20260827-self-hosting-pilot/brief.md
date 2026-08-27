# Self-hosting pilot

- ID: `20260827-self-hosting-pilot`
- Size: `M`
- Status: done
- Created: 2026-08-27

## Goal

Use the Vibe Kit repository as its own first adopted project and verify that installation, onboarding, work-item creation, and quality gates form a coherent self-hosted loop.

## Context

- The repository already contained the v0.1 managed source files and project context but had not created its own `.vibe/manifest.json` or `.vibe/version`.
- This pilot exercises the same-source/target adoption path; external target behavior remains covered by `tests/test_cli.py`.

## Scope

- In: run `./bin/vibe adopt .`, record installed state, refresh durable context from repository evidence, create this work item, run configured verification, and obtain an independent QA assessment.
- Out: publishing a package, adding network updates, changing workflow semantics, or refactoring the CLI.

## Acceptance criteria

- [x] AC-1: Self-adoption creates `.vibe/manifest.json` and `.vibe/version` without overwriting existing project-owned context.
- [x] AC-2: `./bin/vibe doctor .` reports no errors or warnings after onboarding changes are complete.
- [x] AC-3: `./bin/vibe verify .` passes the configured test suite on Python 3.9-compatible code.
- [x] AC-4: Product, architecture, and interaction context accurately describe observed v0.1 behavior rather than planned behavior.
- [x] AC-5: An independent QA pass maps every criterion to evidence and records limitations.

## Design and technical notes

- No application implementation is required. All pilot artifacts are project-owned except the generated installation manifest and version.
- The managed/project-owned boundary remains governed by `docs/decisions/0001-managed-vs-project-owned.md`.

## Risks and open decisions

- Self-adoption cannot prove cross-directory copying because the managed source and target paths resolve to the same files; the automated external-target tests remain necessary evidence.
- The repository has no initial commit, so preservation is evidenced by command behavior, manifest contents, targeted inspection, and scenario tests rather than a clean before/after Git diff.
