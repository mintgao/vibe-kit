# Publish Vibe Kit v0.5.0 GitHub prerelease

- ID: `20260827-v0-5-publication`
- Size: `L`
- Status: implementation
- Created: 2026-08-27

## Technical decision readiness

- Outcome: `covered-by-accepted-decision`
- Trigger evidence: L external publication spanning immutable Git refs, release assets, integrity metadata, channel status, public compatibility claims, and rollback boundaries.
- Decision owner: Release orchestrator applying existing Accepted decisions
- Governing decision: [ADR 0004](../../decisions/0004-reproducible-release-contract.md), [ADR 0007](../../decisions/0007-agent-first-adoption-contract.md), and [ADR 0008](../../decisions/0008-technical-decision-readiness-gate.md)
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: Independent Tech Lead review on 2026-08-27 confirmed that Accepted ADRs 0004, 0007, and 0008 cover clean committed deterministic packaging, immutable refs, the five-asset GitHub Pre-release flow, Agent-install/result/onboarding/provenance boundaries, remote read-back, isolated download validation, and the shared 0.5.0/protocol 3 target. The established v0.3/v0.4 mechanics introduce no new durable decision. The review also required truthful disclosure of unverified Linux/host evidence and the still-unimplemented permission-safe atomic-upgrade boundary.
- Material product decisions: resolved; the user explicitly authorized integrating the completed concurrent task and publishing public v0.5.0, while stable promotion remains unauthorized and unsupported by current evidence, so this work publishes a Pre-release.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-08-27T15:38:06Z`
- Confirmation basis: Explicit user publication authorization, Accepted ADRs 0004/0007/0008, approved independent Tech Lead coverage review, Pre-release limitation, and no remaining decision blocker.
- Readiness history: `2026-08-27 — publication requested; existing Accepted release, Agent-install, and readiness decisions identified; covered-by-accepted-decision review opened before remote writes; independent review approved the coverage and corrected the product-decision record to resolved; orchestrator confirmed implementation-ready before self-upgrade or remote publication writes.`

## Goal

Publish the integrated Agent-first adoption and Technical Decision Readiness Gate as a verifiable GitHub Pre-release so an Agent can resolve, validate, install, and use the exact `0.5.0` payload without relying on the development checkout or exposing the internal CLI workflow to a human.

## Context

- `20260827-agent-first-adoption` targets `0.5.0`, core/Codex protocol 3, and Agent-install protocol 1.
- `20260827-architecture-decision-readiness-gate` is complete and independently verified; it shares the same unpublished `0.5.0` / protocol 3 candidate.
- The separate `20260827-permission-safe-atomic-upgrade` work item is shaped but not implemented and must not be described as part of this release.
- The established v0.4.0 publication contract uses a clean commit, annotated tag, five GitHub assets, and isolated re-download verification.

## Scope

- In: final integrated QA, controlled source-checkout self-upgrade, publication-facing documentation, a clean release commit, annotated `v0.5.0` tag, GitHub Pre-release, and five validated assets.
- In: release ZIP, Plugin ZIP, distribution ZIP, release manifest, SHA256SUMS, and cross-channel Agent-contract identity.
- In: isolated GitHub re-download, checksums, release validation, install/adopt/doctor/Plugin smoke tests, and durable publication evidence.
- Out: stable promotion, public Plugin Directory, package managers, automatic updates, Linux certification, non-Codex compatibility claims, signatures/attestations, and permission-safe whole-upgrade transactions.

## Acceptance criteria

- [ ] AC-1: source, protocol, Plugin, changelog, release notes, and durable context identify `0.5.0` consistently and describe both completed capabilities without claiming the separate atomic-upgrade work.
- [ ] AC-2: independent QA passes the configured suite, `verify`, bytecode compilation, diff validation, unpublished packaging, release validation, and isolated GitHub/Plugin install paths; skipped host/platform checks are explicit.
- [ ] AC-3: controlled self-upgrade updates only Vibe Kit installation state after a safe JSON plan, then source-checkout doctor reports healthy with valid onboarding readiness.
- [ ] AC-4: a clean committed tree produces a reproducible `prerelease` distribution bound to the release commit with kit 0.5.0, core/Codex protocol 3, Agent-install protocol 1, feedback protocol 2, and byte-identical Agent contracts across channels.
- [ ] AC-5: annotated tag `v0.5.0` resolves to the accepted release commit and remote `main` contains that commit.
- [ ] AC-6: GitHub Release `v0.5.0` is public, non-draft, marked Pre-release, and exposes exactly the five intended assets.
- [ ] AC-7: remote asset sizes and SHA-256 digests match the local publication files and uploaded state is confirmed by read-back.
- [ ] AC-8: a fresh isolated download passes outer and nested checksums, `validate-release`, read-only plan, installation/adoption, installed doctor, Plugin smoke, and Agent-contract identity checks.
- [ ] AC-9: publication evidence records exact refs, URL, digests, checks, limitations, skipped gates, and a non-destructive recovery/rollback boundary.

## Design and technical notes

- Follow ADR 0004: build only from a clean committed release source and never upload the dirty-tree unpublished candidate.
- Publish as Pre-release. Linux, real non-Codex hosts, and stronger provenance are not verified, so stable claims remain blocked.
- Upload exactly five user-facing assets and verify the canonical GitHub download rather than trusting command intent.
- On an uncertain remote write, inspect remote state before retrying. Do not delete or rewrite a remote Release/tag without a separate destructive decision.
- GitHub authentication is an execution prerequisite, not a product decision; the current host must be re-authorized before remote writes.

## Risks and open decisions

- GitHub tag identity and SHA-256 provide integrity signals but not an external publisher signature or provenance attestation.
- Agent-install provenance is caller/host-attested at the CLI boundary; publication evidence must not overstate local validation as publisher authentication.
- Real Linux, Python 3.9, Codex task handoff, and Plugin host behavior may remain incomplete; the release stays Pre-release and records every skipped check.
- If authentication, push, tag creation, Release creation, or upload is uncertain, stop and read remote state before any retry.
