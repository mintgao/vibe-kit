# Publish Vibe Kit v0.4.0 GitHub prerelease

- ID: `20260827-v0-4-publication`
- Size: `L`
- Status: complete
- Created: 2026-08-27

## Goal

Publish the completed proactive-feedback capability as a verifiable GitHub Pre-release so another host or user can download, validate and install the exact 0.4.0 payload without relying on this development checkout.

## Context

- `20260827-proactive-feedback-loop` completed implementation and independent QA for 0.4.0.
- The final unpublished candidate passed 21 tests on the workspace Python and macOS Python 3.9.6, `doctor`, release validation and official Skill/Plugin validation.
- The established v0.3.0 publication contract uses a clean commit, annotated tag, five GitHub assets and isolated re-download verification.
- The user explicitly requested release 0.4.0; the repository supports prerelease status only until Linux CI and stronger provenance gates exist.

## Scope

- In: publication-facing documentation, final source verification, a clean release commit, annotated `v0.4.0` tag, GitHub Pre-release and five validated assets.
- In: isolated re-download, checksum/release validation, install smoke test and durable publication evidence.
- Out: stable promotion, Linux CI, signatures/provenance attestations, Plugin Directory, package managers and automatic updates.

## Acceptance criteria

- [x] AC-1: release-facing documentation consistently identifies 0.4.0 as the current GitHub Pre-release and does not claim stable or Plugin Directory publication.
- [x] AC-2: all configured tests, Python 3.9 compatibility, `doctor`, bytecode compilation and official Skill/Plugin validators pass on the release source.
- [x] AC-3: a clean committed tree produces a `prerelease` manifest bound to the release commit, with core 2, feedback 2 and Codex adapter 2.
- [x] AC-4: annotated tag `v0.4.0` resolves to the accepted release commit; remote `main` contains that commit and may advance only with the publication-evidence commit.
- [x] AC-5: GitHub Release `v0.4.0` is public, non-draft, marked Pre-release and exposes the release ZIP, Plugin ZIP, distribution ZIP, manifest and checksums.
- [x] AC-6: remotely reported asset sizes and digests match local publication artifacts.
- [x] AC-7: a fresh isolated download passes outer checksum parity, nested checksums, `validate-release`, read-only install planning, installation and installed `doctor`.
- [x] AC-8: publication evidence records exact refs, URLs, digests, limitations, skipped checks and recovery/rollback boundaries.

## Design and technical notes

- Follow the existing reproducible release contract in ADR 0004; no new durable architecture decision is introduced.
- Build from the release commit with `./bin/vibe package --status prerelease`; never republish the dirty-tree unpublished candidate.
- Upload exactly five user-facing assets and verify the canonical GitHub download rather than trusting upload intent.
- On an uncertain remote write, inspect remote state before any retry. Rollback is limited to drafting/deleting the exact Release and removing the exact tag after separate confirmation.

## Risks and open decisions

- Linux execution remains absent, so the release must stay Pre-release.
- GitHub SHA-256 digests and the annotated tag provide integrity signals but not an external publisher signature or provenance attestation.
- The local feedback candidate is unrelated release state and remains ignored; Issue submission is handled only under its own exact-payload authorization.
