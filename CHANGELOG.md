# Changelog

## 0.6.0 — 2026-08-28

- Added an evidence-gated post-upgrade takeover lifecycle that separates upgraded, activated, adapted, verified, re-evaluated, and ready states.
- Added Agent-install schema/protocol 2, maintenance bridge schema 1, takeover schema 1, core/Codex protocol 4, content-bound payload/activation identity, and fail-closed cross-channel validation.
- Added authoritative structured doctor diagnostics and additive `verify --format json` receipts with full configured-check coverage, bounded redacted output, and explicit failure/skip semantics while retaining CLI result schema 1.
- Installed `AGENT_INSTALL.md` and `agent-install.json` as activation-critical framework-managed files with collision/upgrade protection and broken doctor diagnostics when either contract is missing, modified, or invalid.
- Added activation-set algorithm v2 zero-sentinel normalization, a digest-authenticated compiled takeover registry, privacy-safe `validate-takeover --format json`, release-time canonical validator cases, and deterministic fake-host behavior scenarios.
- Added a compiled, digest-mirrored, complete-set migration for the exact healthy official v0.5.0 source-checkout Agent contracts, with normalized installation authentication, component-wise symlink rejection, independent apply reauthentication and fail-closed race handling; arbitrary untracked paths remain conflicts.
- Made exact-version consent single-use across safe plan/apply and defined same-task reload, automatic successor handoff, goal custody, and one-action manual new-task fallback contracts.
- Kept the repository and bootstrap Plugin manual-fallback-only until a running host supplies positive live conformance evidence.

## 0.5.0 — 2026-08-27

- Made Codex the primary adoption interface through a packaged `AGENT_INSTALL.md` and versioned `agent-install.json` contract.
- Added additive JSON results for install-critical plan, init/adopt, upgrade, doctor and release-validation paths while preserving default text output and exit codes.
- Added validated installation source provenance and project-owned onboarding readiness with automatic first-run routing that resumes ordinary user requests.
- Bumped the core and Codex adapter protocols to 3 and added Agent install protocol 1; kept the local CLI offline and repository-pinned.
- Updated the bootstrap Plugin, release validator, documentation and scenarios for Agent-first adoption.
- Added a size-aware technical-decision readiness gate, project-owned readiness record, read-only Tech Lead author/reviewer role, and fail-closed feature, debug-to-fix, and direct implementation handoffs.

## 0.4.0 — 2026-08-27

- Made `feedback.mode: ask` an observable, proactive Close behavior while keeping every GitHub write bound to adjacent approval of one exact payload.
- Added mode-aware `feedback close`, read-only `feedback mode`, sanitized `feedback revise`, attention state schema 2, material-resurface prompting and legacy-backlog suppression.
- Added semantic security-sensitive public-submission blocking and removed raw remote stderr from persisted feedback failure state.
- Bumped the core, feedback and Codex adapter protocols to version 2; refreshed repository and Plugin distribution metadata.
- Added mode, migration, prompt suppression, hash invalidation, privacy and remote-boundary regression coverage.

## 0.3.0 — 2026-08-27

- Added local-first, privacy-gated Vibe Kit feedback with stable deduplication, exact payload review hashes, dismissal/resurfacing, and optional consent-bound GitHub submission.
- Added read-only `plan init|adopt|upgrade` previews.
- Added deterministic offline release and bootstrap-only Codex Plugin packaging with SHA-256, protocol metadata, marketplace output, and cross-channel drift validation.
- Added artifact-based install/adopt/upgrade, tamper, unsafe ZIP, Plugin payload, and conflict regression coverage.
- Kept public GitHub/Plugin publication, signing, non-Codex adapters, and automatic remote updates out of scope.

## 0.2.0 — 2026-08-27

- Added three-way version integrity diagnostics and conservative self-upgrade validation.
- Strengthened adoption preservation and managed-file conflict evidence.

## 0.1.0 — 2026-08-27

- Established the repository-pinned operating model, PM/UX/RD/QA/Investigator roles, workflow Skills, project onboarding, and local installer.
