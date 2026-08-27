# 0008: Gate implementation on technical decision readiness

- Status: Accepted
- Date: 2026-08-27
- Decision owner: Tech Lead perspective
- Review: Independent Tech Lead review approved on 2026-08-27

## Context

Vibe Kit separates product shaping from implementation and asks L work to record important architectural decisions, but the lifecycle, Skills, Agent roles, and work-item template do not currently form a complete handoff. Feature work can move from PM/UX directly to an RD writer, and direct implementation or debug-to-fix work has no required check for unresolved durable or high-risk technical choices.

The `permission-safe-atomic-upgrade` work item exposed the gap. Permissions, multi-file consistency, rollback failure, recovery, and crash boundaries should trigger a technical decision before implementation even when the user or PM does not explicitly request an ADR.

## Decision

Vibe Kit establishes a mandatory **Technical Decision Readiness** gate between Shape/Investigation and the first code edit.

The normative policy is defined once in `.vibe/core/technical-decision-readiness.md`. The operating model, quality gates, workflow Skills, Agent definitions, and work-item template reference that contract rather than redefining independent variants.

The Codex adapter adds a read-only `vibe_tech_lead` role. A Tech Lead pass may author a proposed technical decision or perform a technical review, but the same native subagent instance must not perform both required passes. The orchestrator persists read-only specialist output, verifies readiness evidence, and confirms the gate. One `vibe_rd` writer implements only after the gate is ready.

Per-work-item readiness state remains project-owned Markdown. Vibe Kit does not add a CLI-owned workflow state machine in this iteration. CLI packaging, installation, and doctor continue to distribute and validate managed files; they do not decide whether a work item is implementation-ready.

This contract is core protocol 3 and Codex adapter version 3. These values are conformance metadata, not runtime enforcement. Prompt routing, workflow instructions, recorded evidence, and review provide the gate behavior.

## Readiness state contract

### Applicability

- A normal S task does not require a readiness block. If a trigger scan finds a durable or high-risk boundary, the task must be reclassified to M or L before code editing.
- Every M work item completes a trigger scan before implementation.
- Every L work item contains an explicit readiness block and outcome before implementation.
- An active M/L work item that has not entered implementation is subject to this contract immediately.
- A work item already implementing when this contract is adopted is not paused merely because its historical brief lacks the block. It reopens the gate if a new unresolved durable/high-risk boundary is discovered.
- Complete historical work items are not migrated.

### Required fields

An applicable readiness block contains:

- `Outcome`
- `Trigger evidence`
- `Decision owner`
- `Governing decision`
- `Review mode`
- `Review result`
- `Review evidence`
- `Material product decisions`
- `Open blockers`
- `Gate`
- `Gate owner`
- `Confirmed at`
- `Confirmation basis`
- `Readiness history`

A field with no applicable value contains the explicit value `none`; an empty field is missing evidence.

### Outcome enum

`Outcome` is exactly one of:

- `not-assessed`
- `decision-required`
- `covered-by-accepted-decision`
- `no-new-durable-decision`
- `decision-accepted`

`not-assessed` is an initialization value, not a successful readiness outcome.

### Gate enum

`Gate` is exactly one of:

- `blocked`
- `implementation-ready`

There is no implicit, blank, or inferred gate state.

### Review enums

`Review mode` is exactly one of:

- `not-required`
- `independent-agent`
- `sequential-perspective`

`Review result` is exactly one of:

- `not-required`
- `pending`
- `changes-required`
- `approved`

### Valid combinations

| Outcome | Allowed gate | Release conditions |
|---|---|---|
| `not-assessed` | `blocked` only | None |
| `decision-required` | `blocked` only | None |
| `covered-by-accepted-decision` | `blocked` or `implementation-ready` | Every governing ADR is Accepted; applicability is explained; required review is approved; product decisions and blockers are resolved; gate confirmation exists |
| `no-new-durable-decision` | `blocked` or `implementation-ready` | Rationale explains why remaining choices are local, reversible, and do not change a shared contract; required review is approved; blockers are resolved; gate confirmation exists |
| `decision-accepted` | `blocked` or `implementation-ready` | The new or updated governing ADR is Accepted; required review is approved; product decisions and blockers are resolved; gate confirmation exists |

`not-assessed + implementation-ready` and `decision-required + implementation-ready` are invalid. A successful outcome may remain blocked while required review, product resolution, or gate confirmation is pending.

### Fail-closed rules

For work subject to this contract, any of the following means `Gate: blocked`:

- a missing readiness block;
- a missing required field;
- an unknown enum value;
- an invalid Outcome/Gate combination;
- a referenced decision that is absent or not `Status: Accepted`;
- required review without approved evidence;
- an unresolved material product decision;
- any non-empty open blocker; or
- missing gate confirmation evidence.

The Agent must not edit application or shared implementation code while any of these conditions holds. It first repairs the readiness artifact or routes the missing decision/review.

`covered-by-accepted-decision` and `decision-accepted` may reference only decision records whose current status is exactly `Accepted`. A Proposed, Draft, Rejected, or Superseded ADR cannot release the gate. Existing Accepted ADRs remain valid without retrospective author/reviewer metadata, but their applicability to new L or triggered M work still receives current review.

## Trigger boundary and review policy

The readiness scan includes durable/shared contracts, cross-system boundaries, schema/protocol/version compatibility, migration, authentication, permissions, security, privacy, trust boundaries, rollback, recovery, crash/failure consistency, irreversible state, and alternatives with material long-term trade-offs.

Local, reversible implementation choices that do not change a shared contract remain RD planning decisions and do not require an ADR.

### S

A normal S task requires no independent technical review. If a trigger causes reclassification, the resulting M/L policy applies.

### M without a trigger

An untriggered M records `Outcome: no-new-durable-decision`, a concise trigger-scan rationale, `Review mode: not-required`, and `Review result: not-required`. No ADR or independent technical review is required. The gate owner may confirm readiness when no blockers remain.

### Triggered M

A triggered M requires technical decision-owner evidence and technical review whether it creates a new decision, relies on an existing Accepted decision, or concludes that no new durable decision is needed. `Review result: approved` is required before release.

### L

Every L readiness outcome requires technical review, including `covered-by-accepted-decision` and `no-new-durable-decision`. For L no-new-decision, the reviewer checks that the rationale is not hiding an unresolved architecture, recovery, compatibility, security, migration, or ownership trade-off.

The implementation writer must not be the source of the only decision, review, and gate evidence.

## State transitions and confirmation

1. A new M/L readiness block starts as `Outcome: not-assessed` and `Gate: blocked`.
2. Trigger scan produces `decision-required + blocked`, `covered-by-accepted-decision + blocked`, or `no-new-durable-decision + blocked`.
3. A new or updated ADR may move `decision-required` to `decision-accepted` only after the ADR itself is `Status: Accepted`.
4. Required review is recorded separately. A successful outcome remains blocked while review is pending or requests changes.
5. The gate owner moves the gate to `implementation-ready` only after checking all release conditions.
6. Implementation discovery of a new schema, protocol, compatibility, ownership, recovery, migration, security, or other durable/high-risk choice immediately moves the state to `decision-required + blocked`.
7. Reopening invalidates the previous current confirmation. The prior outcome, confirmation, timestamp, and reopen reason are appended to `Readiness history`; they are not silently overwritten.
8. After the new or updated decision and review are complete, the gate is confirmed again through the normal transition.

An implementation-ready state records the gate-owner perspective or Agent, an ISO-8601 confirmation timestamp, the current work-item reference, governing Accepted ADRs or no-new-decision rationale, required review evidence, resolution references for material product decisions, and `Open blockers: none`. Confirmation states what evidence was checked; it does not authorize the gate owner to invent or alter the technical decision.

## Specialist execution semantics

### Read-only author

`vibe_tech_lead` is read-only. It returns a proposed ADR or applicability/no-new-decision artifact to the orchestrator. The orchestrator may persist that output and make formatting-only adjustments. Substantive architecture changes are returned to the decision owner for revision.

### Native-subagent host

For L and triggered M work:

1. one read-only Tech Lead instance authors the decision evidence;
2. the orchestrator persists the proposal;
3. a separate native Tech Lead/reviewer instance reviews the exact persisted proposal;
4. the orchestrator persists review evidence and resolves the gate;
5. one RD writer implements after readiness.

The author and reviewer are different native subagent instances. The implementation writer's self-review cannot satisfy required technical review.

### Sequential-perspective host

A host without independent subagents may run separate sequential passes: technical-decision author, critical technical review, gate confirmation, and implementation writer. The review pass is separately recorded, does not edit code, and returns `approved`, `changes-required`, or `blocked`.

A successful fallback records `Review mode: sequential-perspective`, `Review result: approved`, review evidence, and `Capability limitation: identity-isolated independent reviewer unavailable`. This degraded mode may release the gate after all other conditions are met so non-subagent hosts retain the same blocking semantics. It must not be described as `independent-agent` review or used as evidence of identity-isolated independence.

## Work-item readiness record

New work items include this project-owned block:

```md
## Technical decision readiness

- Outcome: `not-assessed`
- Trigger evidence: none
- Decision owner: none
- Governing decision: none
- Review mode: `not-required`
- Review result: `not-required`
- Review evidence: none
- Material product decisions: none
- Open blockers: none
- Gate: `blocked`
- Gate owner: Workflow orchestrator
- Confirmed at: none
- Confirmation basis: none
- Readiness history: none
```

## Alternatives considered

### Reuse `vibe_rd` as an architecture mode

Rejected for the initial Codex adapter. The existing RD role has write access and combines planning with implementation. Adding a mode protocol would leave author/writer separation and automatic routing ambiguous.

### Add a CLI-enforced work-item state machine

Deferred. A Markdown parser and transition command would add schema and migration complexity without preventing an Agent from directly editing code. The managed workflow contract is normatively blocking but not mechanically enforced. A read-only checker may be reconsidered if repeated state drift is observed.

### Duplicate gate rules in each Skill

Rejected. A shared core contract avoids semantic drift; Skills and role prompts apply it rather than restating competing versions.

## Protocol and release alignment

Core protocol 3 and Codex adapter version 3 declare that the distributed workflow supports the readiness state contract, Tech Lead author/reviewer mapping, pre-implementation blocking across feature, debug-to-fix, and direct implementation, and native/sequential capability semantics.

These metadata values do not cause the CLI to parse work items, enforce transitions, or prevent writes. `doctor` validates installed managed files, hashes, and Agent/Skill structure; it does not certify implementation readiness.

A protocol-3 canonical payload must not reuse the already published immutable 0.4.0 version. This decision joins the repository's already accepted, unpublished 0.5.0 development candidate from ADR 0007 and does not create a second version or channel decision. `.vibe/core/version`, Plugin metadata, release notes, and immutable artifacts must remain aligned to 0.5.0. Promotion from `release-candidate-unpublished` to a GitHub prerelease or stable release remains a separate, explicitly authorized release operation.

Ephemeral conformance fixtures may use an explicitly non-publishable fixture version. They must not be presented as canonical release candidates or public release evidence.

## Consequences

- Product shaping and implementation readiness become separate observable states.
- L work incurs an explicit readiness and review pass even when no new ADR is needed.
- Untriggered M work incurs only a concise trigger-scan rationale and gate confirmation.
- Codex gains one additional read-only specialist role.
- Capability-degraded hosts can continue, but their evidence discloses the absence of identity-isolated review.
- Work-item state remains human-readable, project-owned, normatively blocking, and not mechanically enforced by the CLI.
- Protocol metadata advertises conformance but does not provide runtime enforcement.
- The already selected unpublished 0.5.0 development candidate carries the protocol-3 contract; publication remains separately gated.
- CLI state enforcement remains a possible later iteration only if evidence shows the Markdown/prompt contract is insufficient.

## Compatibility and adoption

- Active M/L work that has not entered implementation adopts the gate at its next handoff.
- In-progress work pauses only when a new unresolved durable/high-risk boundary is found.
- Completed historical work is not retrofitted.
- Existing Accepted ADRs remain valid; a new work item records why they apply rather than manufacturing historical reviewer metadata.
- New template fields affect newly created work items only; upgrades never overwrite existing project-owned briefs.
- Older Vibe Kit versions ignore the added Markdown fields. Protocol 3 is a conformance boundary, not technical proof of host behavior.

## Verification

- Installation, adoption, upgrade, doctor, and release payload scenarios cover the new core contract and Tech Lead role.
- Contract tests verify that feature, debug-to-fix, and direct implementation paths apply the shared readiness contract and block unresolved work.
- Role tests verify read-only Tech Lead behavior and non-conflicting PM, Tech Lead, RD, orchestrator, and QA authority.
- Scenario verification covers permission/recovery L work without an ADR hint, accepted-decision release, direct implementation, debug-to-fix, S/M negative cases, gate reopening, and sequential-host limitations.
- Agent behavior that cannot be deterministically executed in the current test harness is recorded as independent QA evidence rather than replaced by string assertions.
- Actual non-Codex host runtime conformance remains unverified until a compatible adapter exists.

## Rollback and recovery

### Exact repository rollback

Git revert of the reviewed implementation commits is the exact source-tree rollback. It restores tracked managed files and removes newly tracked files introduced by those commits. Project-owned evidence is reverted only when included in the selected commits and intentionally rolled back.

### Semantic installed-project rollback

Upgrade with an older trusted payload restores the older payload's governing managed content and protocol semantics, but it is not an exact filesystem rollback. Existing removed-managed-file policy may retain newer-only files, including the readiness core or Tech Lead role, for manual review.

The rollback report must describe semantic rollback with retained stale files, not byte-for-byte restoration. Retained paths are reviewed explicitly before manual removal; stale-file deletion is outside this work item's scope and must not be folded into the separate atomic-upgrade decision.

## Open decisions

None. ADR 0007 already fixes the current development target as an unpublished 0.5.0 candidate; this work introduces no publication action.
