# Product context

## Product purpose

Provide a reusable, lightweight development operating system for personal vibe-coding projects.

## Primary users

- A developer using Codex to create or continue software projects.

## Current capabilities

- Project-level PM, UX, read-only Tech Lead, RD, QA, and Investigator roles.
- Repository-scoped onboarding, feature, design, implementation, verification, and debugging workflows.
- Size-aware technical-decision readiness before implementation: M trigger scans, explicit L outcomes, Accepted decision/review evidence for durable or high-risk choices, and sequential-perspective fallback disclosure when identity-isolated review is unavailable.
- `init` for new projects and conservative `adopt` for existing projects.
- Read-only `plan init|adopt|upgrade` before project writes.
- Hash-checked `upgrade` with conflict candidates and no partial managed-file update when a conflict is found.
- `doctor` with three-source installed/manifest/core version integrity, configurable `verify`, and work-item generation commands.
- Mode-aware `vibe-feedback-flow` plus `feedback mode/close/draft/list/review/revise/check/submit/dismiss` for evidence-backed framework improvement. `ask` proactively presents new/material candidates once, while every GitHub submission to `mintgao/vibe-kit` remains exact-payload consent-bound and deduplicated.
- Deterministic local release/Plugin packaging, SHA-256 manifest validation, expanded marketplace output, and artifact-based offline install checks.
- Agent-first adoption from the canonical GitHub link through packaged human/machine contracts, structured install-critical CLI results, source provenance, and automatic onboarding readiness routing.
- Shallow stack and command detection for common Node.js, Python, Rust, Go, and Swift projects.

## Non-goals and boundaries

- v0.5.0 is the latest GitHub Pre-release. Stable promotion, a public Plugin Directory entry, and automatic network updates remain out of scope.
- It does not collect telemetry or silently submit feedback. The central feedback repository is configured, but every outbound payload still requires adjacent, unambiguous approval bound to its report, repository and current hash.
- The accepted distribution uses channel-neutral releases, repository-pinned installations, a bootstrap-only Codex Plugin, generated thin adapters, and a validated GitHub Release bundle.
- It does not replace framework-specific project generators.
- It does not infer deep product or architecture truth during CLI installation; the onboarding workflow performs evidence-based enrichment afterward.
- Ordinary users are not expected to learn `init`, `adopt`, `doctor`, or internal Skill names; those remain Agent/maintainer interfaces and may surface for troubleshooting.
- Ordinary users are not expected to request an ADR or recognize an architecture phase. They decide only technical options that materially change product scope, observable behavior, promised risk/cost, irreversible state, or external compatibility.

## Product principles

- Lightweight by default, rigorous when risk demands it.
- Existing projects are preserved during adoption.
- Framework-owned and project-owned files remain distinguishable.
- Verification results must distinguish executed evidence from assumptions or skipped checks.
