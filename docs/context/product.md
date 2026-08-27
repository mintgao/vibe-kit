# Product context

## Product purpose

Provide a reusable, lightweight development operating system for personal vibe-coding projects.

## Primary users

- A developer using Codex to create or continue software projects.

## Current capabilities

- Project-level PM, UX, RD, QA, and Investigator roles.
- Repository-scoped onboarding, feature, design, implementation, verification, and debugging workflows.
- `init` for new projects and conservative `adopt` for existing projects.
- Read-only `plan init|adopt|upgrade` before project writes.
- Hash-checked `upgrade` with conflict candidates and no partial managed-file update when a conflict is found.
- `doctor` with three-source installed/manifest/core version integrity, configurable `verify`, and work-item generation commands.
- Local-first `vibe-feedback-flow` plus `feedback draft/list/review/check/submit/dismiss` for evidence-backed framework improvement. Drafting and review are offline; GitHub submission is per-payload consent-bound and deduplicated.
- Deterministic local release/Plugin packaging, SHA-256 manifest validation, expanded marketplace output, and artifact-based offline install checks.
- Shallow stack and command detection for common Node.js, Python, Rust, Go, and Swift projects.

## Non-goals and boundaries

- This version publishes a GitHub Pre-release but does not fetch or apply updates over the network.
- It does not collect telemetry or submit feedback automatically. No central feedback repository is configured in the source distribution yet.
- The accepted distribution direction uses channel-neutral releases, repository-pinned installations, a bootstrap-only Codex Plugin, and generated thin adapters. v0.3 begins implementing release-ready local artifacts; public channel publication remains a separate authorized action.
- It does not replace framework-specific project generators.
- It does not infer deep product or architecture truth during CLI installation; the onboarding workflow performs evidence-based enrichment afterward.

## Product principles

- Lightweight by default, rigorous when risk demands it.
- Existing projects are preserved during adoption.
- Framework-owned and project-owned files remain distinguishable.
- Verification results must distinguish executed evidence from assumptions or skipped checks.
