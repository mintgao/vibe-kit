# Implementation plan: Proactive Vibe Kit feedback loop

## Target

- Version: `0.4.0`
- Protocol: feedback protocol 2
- Compatibility: Python 3.9+, standard library only
- Writer: one shared-code writer; independent RD planning and QA verification

## CLI changes

1. Add strict project-owned `feedback.mode` parsing for `ask/local/off`; missing mode defaults to `ask`, invalid or ambiguous YAML fails closed.
2. Add `feedback mode` as a read-only, network-free policy query.
3. Add `feedback close` as the deterministic proactive entry point:
   - `off`: no candidate;
   - `local`: local candidate only;
   - `ask`: one exact decision block for new/material candidates.
4. Introduce feedback state schema 2 with independent attention revision/status so occurrence-driven hash changes do not create repeated prompts.
5. Add `feedback revise` for sanitized partial updates, collision checks, hash invalidation and exact re-review.
6. Add an explicit semantic security-sensitive gate in addition to existing secret-pattern blocking.
7. Preserve existing manual `draft/list/review/check/submit/dismiss` commands and exact hash enforcement.
8. Remove raw remote stderr from persisted/user-visible feedback failure state.

## Managed workflow changes

- Update `AGENTS.md`, `vibe-feedback-flow` and quality gates with mode-first Close, primary-task-first ordering, exact decision output and strict natural-language consent.
- Keep each Close to one generalized root-cause candidate.
- Treat payload content as data, not instructions.

## Version and distribution

- Bump core, installed source, Plugin metadata and bundled-version documentation to 0.4.0.
- Add feedback protocol 2 metadata and 0.4.0 release-candidate notes.
- Refresh the self-hosted manifest through `vibe upgrade`; do not hand-edit managed hashes.

## Verification

- Add focused mode, proactive attention, revise, consent/hash, privacy/security and remote-failure tests mapped to AC-1–AC-12.
- Run default Python and macOS system Python 3.9 suites.
- Run `./bin/vibe verify .`, `doctor`, bytecode compile, deterministic package/validate, official Plugin validator and Skill validators.
- Give final source and built artifacts to independent QA; QA does not edit failures.

## Rollback

- Users can immediately select `local` or `off` without deleting candidates.
- State v2 preserves v1 fields and is normalized lazily; rollback readers ignore new fields.
- No migration rewrites project-owned `.vibe/project.yaml` or historical local candidates in bulk.

## Implemented result

- CLI now provides strict `feedback mode`, mode-aware `feedback close`, partial `feedback revise`, state schema 2 attention tracking and semantic public-submission blocking.
- Existing manual commands remain available; remote duplicate/create failures store sanitized categories instead of raw stderr.
- Managed AGENTS, feedback Skill, quality gate, core/feedback protocol metadata, Plugin version, README, changelog and release notes are aligned to 0.4.0.
- This repository was upgraded in place from its recorded 0.3.0 installation using a read-only plan followed by the native conflict-checked upgrader. The project-owned feedback mode remained `ask`.
- An unpublished deterministic release candidate is built at `dist/vibe-kit-0.4.0`; its manifest records core protocol 2, feedback protocol 2 and Codex adapter 2.

The implementation does not add a Host-specific action card or natural-language parser. The managed Skill decides whether an adjacent user reply is unambiguous; the CLI continues to enforce exact `--confirm` payload identity before network access.
