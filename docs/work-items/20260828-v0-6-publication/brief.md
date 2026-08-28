# Publish Vibe Kit v0.6.0 GitHub prerelease

- ID: `20260828-v0-6-publication`
- Size: `L`
- Status: release-readiness
- Created: 2026-08-28

## Technical decision readiness

- Outcome: `covered-by-accepted-decision`
- Trigger evidence: L external publication spanning immutable Git refs, public release assets, integrity metadata, exact predecessor compatibility, activation claims, platform evidence, and rollback boundaries.
- Decision owner: Release orchestrator applying existing Accepted decisions
- Governing decision: [ADR 0004](../../decisions/0004-reproducible-release-contract.md), [ADR 0007](../../decisions/0007-agent-first-adoption-contract.md), [ADR 0008](../../decisions/0008-technical-decision-readiness-gate.md), and [ADR 0009](../../decisions/0009-post-upgrade-takeover.md)
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: Independent Tech Lead review on 2026-08-28 approved the corrected boundary after requiring exact official-v0.5 versus real-current-project verification semantics, readiness-only blockers, the five named assets, commit-tree exclusion of unrelated atomic-upgrade work, and removal of a stale fixture count. The reviewer confirmed coverage by Accepted ADRs 0004/0007/0008/0009 for Pre-release status, actual Python 3.9 execution, truthful Linux/manual-host limitations, clean isolated builds, public re-download, and inspect-before-retry recovery.
- Material product decisions: resolved; the user explicitly authorized the recommended publication flow on 2026-08-28. Stable promotion remains unsupported, so the authorized public form is a GitHub Pre-release.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-08-28T08:00:31Z`
- Confirmation basis: Explicit user publication authorization, Accepted ADRs 0004/0007/0008/0009, approved independent Tech Lead coverage review, corrected acceptance semantics, Pre-release limitation, and no remaining decision blocker.
- Readiness history: `2026-08-28 — user authorized publication after the authenticated v0.5.0 predecessor repair passed real-current-project upgrade acceptance and independent QA; existing Accepted release, Agent-install, readiness, and takeover decisions identified; independent coverage review opened before release-facing shared edits or remote publication writes. First review returned changes-required for old-project test truthfulness, readiness blocker scope, exact assets, unrelated-work exclusion, and stale fixture count. The brief was corrected; the distinct reviewer approved it; the Workflow orchestrator confirmed implementation-ready before release-facing shared edits or remote writes.`

## Goal

Publish the independently accepted Vibe Kit 0.6.0 upgrade/takeover candidate as a verifiable GitHub Pre-release only after this repository itself proves a real 0.5.0-to-0.6.0 upgrade, all required runtime and artifact gates pass, and the public assets are downloaded and revalidated from GitHub.

## Context

- The unpublished 0.6.0 candidate passed AC-1 through AC-14 in `20260828-post-upgrade-automatic-takeover`.
- The exact official v0.5.0 predecessor-contract compatibility defect is repaired and fail-closed outside the authenticated complete-set boundary.
- A real current-project fixture preserved all project/application-owned files byte-for-byte and passed target doctor/default verification.
- The current Codex capability is manual-new-task continuation only. Same-task hot reload and automatic successor handoff must not be claimed.
- The separate `20260827-permission-safe-atomic-upgrade` work item is unrelated, incomplete user work and must not enter the release commit or claims.

## Scope

- In: exact 0.6.0 candidate changes and their accepted design, implementation, verification, release note, context, tests, and publication record.
- In: actual Python 3.9 execution, current-host verification, clean committed source, deterministic prerelease packaging, annotated tag, five GitHub assets, remote read-back, and isolated public-download validation.
- In: a fresh official v0.5.0-to-public-v0.6.0 upgrade smoke and a fresh install/Plugin smoke from downloaded artifacts.
- Out: stable promotion, public Plugin Directory, automatic network updater, publisher signatures/attestations, Linux certification when no Linux runtime is available, hot reload, automatic task creation, and permission-safe whole-upgrade transactions.

## Acceptance criteria

- [ ] AC-1: release-facing source, protocol, Plugin, changelog, release note, context, and docs identify 0.6.0 consistently without claiming stable status, automatic takeover, atomic upgrade, or unverified hosts/platforms.
- [ ] AC-2: independent QA passes the focused predecessor suite, full configured suite, default `verify`, doctor, diff/JSON/bytecode checks, and negative migration/trust/race/symlink cases on the exact candidate.
- [ ] AC-3: the official v0.5.0 and real-current-project upgrade acceptances remain reproducible and preserve all project-owned bytes; manual-new-task continuation remains the only positive live host claim.
- [ ] AC-4: an actual Python 3.9 runtime passes compilation, the full suite, default verification, doctor, package, and release validation on the candidate. Linux is either executed or disclosed as an unverified Pre-release limitation rather than a product failure.
- [ ] AC-5: a clean committed release source excludes `docs/work-items/20260827-permission-safe-atomic-upgrade/**` and its pending work-item index entry while leaving that unrelated development-checkout work untouched, then produces two byte-identical `prerelease` builds with validated direct, Plugin, distribution, manifest, and checksum outputs bound to the release commit.
- [ ] AC-6: annotated tag `v0.6.0` resolves to the accepted release commit and remote `main` contains that commit.
- [ ] AC-7: GitHub Release `v0.6.0` is public, non-draft, marked Pre-release, and exposes exactly `vibe-kit-0.6.0.zip`, `vibe-kit-plugin-0.6.0.zip`, `vibe-kit-distribution-0.6.0.zip`, `release-manifest.json`, and `SHA256SUMS`.
- [ ] AC-8: remote asset state, size, and SHA-256 match the local publication files after read-back.
- [ ] AC-9: fresh isolated public downloads pass outer and nested checksums and `validate-release`; the intact official v0.5.0 source checkout passes read-only plan, apply, target doctor, and project-byte preservation while its four known old project-test incompatibilities remain truthfully reported; the real-current-project fixture passes target default verification; fresh init/doctor, Plugin install smoke, and cross-channel identity checks pass.
- [ ] AC-10: durable evidence records exact refs, URL, digests, checks, platform/host limitations, skipped gates, and the inspect-before-retry/non-destructive recovery boundary.

## Design and technical notes

- Follow ADR 0004: package only from a clean committed source. The dirty development checkout is never an upload source.
- Follow ADR 0009: actual Python 3.9 execution is required for release confidence; activation/ready claims remain host-owned and manual-fallback-only without positive live receipts.
- Publish as a Pre-release. Linux absence is disclosed separately and does not become an inferred compatibility claim.
- Upload exactly five files and verify canonical GitHub downloads rather than trusting command intent.
- On uncertain Git or GitHub writes, read back remote state before retrying. Do not delete or rewrite a public Release/tag without a separate destructive decision.

## Risks and recovery

- Git tag identity and SHA-256 provide integrity signals, not an external publisher signature or provenance attestation.
- Keep unrelated dirty user work unstaged and outside the release commit; build from an isolated clean checkout of the accepted commit.
- If authentication, push, tag creation, Release creation, or upload is uncertain, stop and inspect exact remote state before any retry.
- Rollback requires a separately authorized exact Release/tag operation; never rewrite unrelated history or discard the public release commit.
