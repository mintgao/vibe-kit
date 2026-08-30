# Vibe Kit v0.7.0 — resilient upgrades and first-class prerelease publication

- ID: `20260831-v0-7-resilient-upgrades-publication`
- Size: `L`
- Status: complete
- Created: 2026-08-31

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: L work changes permissions and failure consistency, cross-file transaction/rollback and crash recovery, project-owned onboarding compatibility migration, closed result/protocol compatibility, public source trust language, and consent-bound GitHub writes.
- Decision owner: read-only Tech Lead author for the v0.7.0 upgrade/publication boundary
- Governing decision: Accepted ADRs [0010](../../decisions/0010-recoverable-upgrade-transaction.md) and [0011](../../decisions/0011-exact-source-and-publication-boundary.md), composed with [0001](../../decisions/0001-managed-vs-project-owned.md), [0004](../../decisions/0004-reproducible-release-contract.md), [0007](../../decisions/0007-agent-first-adoption-contract.md), [0008](../../decisions/0008-technical-decision-readiness-gate.md), and [0009](../../decisions/0009-post-upgrade-takeover.md).
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: a distinct native read-only Tech Lead reviewed the exact persisted ADR/work-item boundary through three changes-required passes, independently recomputed the historical identity hashes, and approved the final files on 2026-08-31. After QA exposed the final-leaf syscall gap, the author supplied the lossless hard-link/exchange amendment and the same distinct reviewer required one closure pass for the alias-removed crash substate and canonical digest inputs, then approved the persisted ADR 0010 amendment with no remaining architecture, recovery, compatibility, security/privacy, ownership, publication, or product-choice blocker.
- Material product decisions: resolved by the user's 2026-08-31 request accepting issues #1-#5 and authorizing design, implementation, verification, and a new release. The shaped target is v0.7.0 GitHub Pre-release; direct support is preserved through 0.6.x; only an authenticated audited v0.2-v0.4 pre-onboarding family may receive create-only `pending`, while missing v0.5/v0.6 onboarding is state loss and blocks before writes; transaction guarantees are scoped to one Vibe Kit `upgrade`; exact/pinned selection plus verified digest does not imply platform-enforced immutability.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-08-30T19:11:22Z`
- Confirmation basis: Accepted ADR 0010 now composes the approved lossless existing-parent leaf protocol with the approved adjacent prepared-directory unit protocol for absent parent chains. Exact intent/prepared/commit schemas, parent capability and identity checks, no-clobber publication, rollback, private cleanup and crash recovery are closed; the distinct reviewer approved the persisted composition with no remaining blocker.
- Readiness history: `2026-08-31 — request classified L; PM shaping and repository evidence established decision triggers. A read-only Tech Lead authored ADR 0010/0011; a distinct reviewer required and verified three rounds of corrections, then approved. The orchestrator confirmed implementation-ready before the first application/shared implementation code edit. During implementation, RD found that three closeout intent child objects were declared closed without exact fields; affected work paused and readiness reopened. The author closed the omitted shapes, the distinct reviewer approved the amendment, and the orchestrator reconfirmed the gate before resume. Independent QA later proved a remaining final-leaf race after CAS validation; the orchestrator blocked publication and reopened only the atomic leaf-mutation boundary. The author supplied a lossless atomic leaf protocol; the distinct reviewer required one crash/digest closure pass and approved the exact persisted amendment; the orchestrator reconfirmed the valid decision-accepted + implementation-ready pair at 2026-08-30T18:53:24Z after correcting a persisted enum-position error before RD resumed code edits. RD then identified, before further shared code edits, that the new release skill requires an absent installation parent not covered by the file-leaf transaction protocol; the orchestrator reopened the exact directory boundary at 2026-08-30T18:55:28Z. The author supplied the adjacent prepared-directory unit protocol; the distinct reviewer required two closure passes and approved the exact persisted composition; the orchestrator reconfirmed decision-accepted + implementation-ready at 2026-08-30T19:11:22Z.`

## Goal

Ship Vibe Kit v0.7.0 as a verifiable GitHub Pre-release whose declared predecessor range can upgrade without an onboarding deadlock, whose managed upgrade path is transaction- and recovery-aware under permission/write/crash failures, whose source trust language is precise, and whose own publication uses a first-class dry-run-first Agent workflow. Close issues #1-#5 only after criterion-to-evidence verification and public read-back.

## Context

- [Issue #1](https://github.com/mintgao/vibe-kit/issues/1) requests a first-class GitHub prerelease publication workflow.
- [Issue #2](https://github.com/mintgao/vibe-kit/issues/2) exposed permission failures during managed upgrade. Tracebacks are now contained, but whole-upgrade transaction and rollback remain explicitly unfinished.
- [Issue #3](https://github.com/mintgao/vibe-kit/issues/3) is implemented by ADR 0008 and the readiness workflow; this release supplies closure evidence rather than new readiness behavior.
- [Issue #4](https://github.com/mintgao/vibe-kit/issues/4) identifies an inaccurate equivalence between an exact Release/tag reference and platform-enforced immutability.
- [Issue #5](https://github.com/mintgao/vibe-kit/issues/5) is reproducible from the official v0.3.0 tag: target plan is safe and apply succeeds, but the first v0.6.0 doctor reports blocking `onboarding-state-missing`.
- Product and architecture context describe an offline, dependency-free Python 3.9 CLI, Agent/host-owned networking and credentials, project-owned onboarding, repository-pinned managed runtime, and manual-fallback-only current activation.

## Scope

- In: missing-onboarding compatibility behavior for every directly supported predecessor contract family, including exact official v0.3.0 and current v0.6.0 evidence.
- In: one-upgrade transaction, rollback, interrupted-state detection and explicit recovery for framework-managed files, the managed AGENTS block, tool-maintained install state, and only the create-only onboarding state introduced by that upgrade.
- In: versioned text/JSON result, maintenance bridge, doctor, takeover and release-contract changes required by the accepted failure semantics.
- In: exact/pinned source selection, verified digest, mutable tag/Release risk and platform-enforced immutability as separate trust concepts across normative and user-facing current contracts.
- In: a dry-run-first Vibe release workflow that keeps network and GitHub credentials in the Agent/host boundary, performs idempotent read-before-write/read-back publication, public re-download validation and durable evidence.
- In: v0.7.0 version/protocol/Plugin/release documentation, reproducible packaging, independent QA, GitHub Pre-release publication and evidence-backed closure of issues #1-#5.
- Out: Stable promotion, public Plugin Directory, automatic updater, package managers, telemetry, publisher signatures or external provenance attestation.
- Out: transaction guarantees for `init`, `adopt`, arbitrary business files, unrelated project-owned files, or unauthenticated/unsupported predecessors.
- Out: automatic deletion or rewrite of an existing remote tag/Release, blind retry after uncertain remote state, or expansion of current live reload/automatic handoff claims.

## Acceptance criteria

- [x] AC-1 — Supported onboarding bridge: every declared direct predecessor has a read-only safe plan leading to a first target doctor without blocking `onboarding-state-missing`, or blocks before any control/project write. Only the audited historical v0.2 fixture and exact official v0.3/v0.4 contract families may receive create-only `pending`; missing v0.5/v0.6 onboarding is rejected as state loss, and no bridge fabricates `complete`.
- [x] AC-2 — Onboarding preservation: existing valid onboarding remains byte-identical; malformed, conflicting, wrong-type or raced state fails closed before overwrite. A failed/rolled-back upgrade does not leave newly created onboarding as false success evidence.
- [x] AC-3 — Handled upgrade failure consistency: permission/write failure injected at every externally visible mutation point produces no traceback and no success/healthy/ready claim. When rollback succeeds, every scoped managed/tool-maintained byte and onboarding absence/presence matches the pre-upgrade snapshot.
- [x] AC-4 — Interrupted recovery: process interruption and rollback failure leave bounded, integrity-checked but untrusted detectable state with an independently durable commit marker. Subsequent plan/upgrade/doctor fail closed with one deterministic action; fd-relative recovery refuses unknown paths, symlinks, tampered evidence and third-party divergence, and distinguishes recoverable `recovery-required` from unclassifiable `unknown-partial`.
- [x] AC-5 — Upgrade regression boundary: managed conflicts, local preservation, predecessor complete-set authentication, source trust, AGENTS merge, stale-path handling, symlink/race protection and project-owned preservation continue to pass in text and JSON interfaces.
- [x] AC-6 — Precise trust contract: current normative and user-facing language distinguishes exact/pinned selection, SHA-256 content verification, mutable repository refs/assets and platform-enforced immutability. CLI behavior continues to accept the same exact SemVer/tag/Release URL/commit shapes without calling them immutable.
- [x] AC-7 — Trust regression evidence: contract tests prevent stronger immutable claims from returning, and public v0.7.0 verification records GitHub's observed immutable metadata without contradicting the release note or trust contract.
- [x] AC-8 — Reviewable publication dry run: one documented Agent entry point produces a no-write canonical intent containing exact repository, expected-old/target commits, annotated tag object identity, Release title/body/state, the exact sorted five-asset set and digests, local gates, remote observations/ordered operations, authorization boundary and recovery rules.
- [x] AC-9 — Consent-bound idempotent publication: failed local gates or missing two-layer authorization perform no remote writes; authorized publication fast-forwards `main` under lease and creates or verifies the exact annotated tag/Pre-release/five-asset set, treats identical state as success, divergent or extra state as blocking, and always reads back and publicly hashes uncertain operations before retrying.
- [x] AC-10 — Public artifact verification: canonical GitHub downloads match local sizes and SHA-256, pass outer/nested checksums and `validate-release`, and pass fresh direct install/doctor, Plugin-bundled smoke and critical historical/current upgrade scenarios.
- [x] AC-11 — Offline/privacy boundary: local package, validation, install and upgrade remain Python 3.9 standard-library/offline capable. Tokens, environment values, raw host output and goal/conversation data are absent from release plans, receipts, transaction evidence and artifacts.
- [x] AC-12 — Readiness closure: ADR 0008, focused workflow-contract tests, an unhinted permission/recovery L scenario, and this work item's author/reviewer/gate/RD/QA chain prove issue #3 remains satisfied without expanding its feature scope.
- [x] AC-13 — Exact candidate quality: v0.7.0 version/protocol/Plugin/Agent contracts/context/changelog/release note align; full configured tests, default structured verify, doctor, JSON parsing, diff check, bytecode compilation and actual Python 3.9 pass. Two clean prerelease builds are byte-identical and independently valid.
- [x] AC-14 — Public release and closure: annotated `v0.7.0` has the frozen tag-object identity and points to the accepted clean commit; GitHub exposes one exact non-draft Pre-release and five-asset set; remote read-back/public-download smoke pass; then one canonical closeout intent idempotently posts marker-bound evidence comments and closes exactly #1-#5, with final receipt proving every comment and closed state.

## Design and technical notes

- Keep one implementation writer after the readiness gate is confirmed; QA remains independent.
- Existing Accepted ADRs continue to govern ownership, deterministic local packaging, Agent-first offline materialization, readiness and host-owned takeover. A new or amended Accepted decision must explicitly join their transaction, onboarding exception, result/protocol and publication boundaries.
- A narrower direct-support range, weaker handled-failure rollback promise, Stable release, or mandatory platform immutability would change the shaped external behavior and must return to the user.
- Public writes are authorized only for the accepted exact v0.7.0 Pre-release payload after all local/QA gates pass. Destructive Release/tag rollback remains separately authorized.

## Risks and open decisions

- Crash consistency across multiple fixed repository paths cannot be strict simultaneous filesystem atomicity; the decision must define observable command and recovery guarantees precisely.
- Rollback can fail under changing permissions or external mutation; unknown/tampered state must remain fail-closed rather than overwrite newer user content.
- Creating missing onboarding is a narrow project-owned exception and must not generalize upgrade ownership.
- Remote GitHub create/upload/push responses can be uncertain; idempotent read-back is mandatory before retry.
- The current worktree contains three pre-existing project-context changes. They must be preserved and reviewed explicitly when selecting the release commit boundary.
