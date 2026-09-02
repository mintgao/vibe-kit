# Token Efficient Adaptive Workflow

- ID: `20260902-token-efficient-adaptive-workflow`
- Size: `M`
- Status: complete
- Created: 2026-09-02

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: Changes durable shared workflow contracts for task classification, specialist handoff context, and verification ownership.
- Decision owner: Read-only Tech Lead author `/root/token_tl_author`
- Governing decision: Accepted ADR 0012; Accepted ADR 0008 remains the safety floor
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: Distinct read-only Tech Lead `/root/token_tl_review` approved the exact persisted ADR 0012 on 2026-09-02 after two changes-required passes closed classification, exactly-once verification, platform-evidence, and rollback boundaries.
- Material product decisions: none
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-09-02T04:37:21Z`
- Confirmation basis: Workflow orchestrator checked the accepted scope and AC-1 through AC-11, Accepted ADRs 0008 and 0012, distinct approved review evidence, no material product decisions, and no open blockers.
- Readiness history: none

## Goal

Reduce avoidable token and context amplification in routine Vibe Kit delivery
without weakening the quality and safety controls that users value.

## Context

- The user reports that delivery quality improved after enabling Vibe Kit, while
  token consumption increased materially. The repository does not collect host
  token telemetry, so the magnitude and cause remain hypotheses rather than
  measured product facts.
- `.vibe/core/operating-model.md` currently allows multiple closely related
  files alone to move otherwise local, reversible work into M.
- The implementation and verification flows can both run configured/default
  verification for the same unchanged candidate.
- Current managed guidance does not require role-bounded specialist handoffs or
  exclude full conversation history and unrelated repository material by
  default.
- Relevant governing context: `docs/context/product.md`,
  `docs/context/architecture.md`, and ADR 0008.

## Scope

- In:
  - Make S/M/L classification risk-first: touching multiple tightly coupled
    implementation, test, or documentation files is not by itself an M trigger.
  - Define bounded specialist handoffs that name the role, task, minimum
    evidence, and expected output while excluding complete conversation history
    and unrelated files by default.
  - Make RD own focused development checks and independent QA own one complete
    default verification of the unchanged final M/L candidate.
  - Preserve all existing high-risk readiness triggers, triggered-M/L technical
    review, M/L independent QA, post-upgrade takeover, and release-specific
    verification requirements.
  - Add deterministic managed-contract and distribution scenario coverage.
  - Advance the source tree mechanically to an unpublished `0.8.0` development
    candidate with core/Codex protocol 6; this does not authorize publication.
- Out:
  - Token telemetry, billing integration, a public token-reduction percentage,
    model or reasoning-effort selection, and test-runtime optimization.
  - Changes to `verify` CLI semantics, release/publication behavior, upgrade
    recovery, compatibility, or host protocols.
  - Removing technical-decision readiness, specialist review, focused tests, or
    independent QA where current risk policy requires them.

## Acceptance criteria

- [x] AC-1: A clear, local, low-risk, reversible change with no readiness
  trigger may remain S even when it touches multiple tightly related files;
  file count alone never requires M.
- [x] AC-2: User-flow, shared contract/API, or unresolved acceptance changes
  remain M, while cross-system and high-risk work remains L.
- [x] AC-3: Authentication, permissions, security/privacy/trust, schema,
  protocol, version, API/compatibility, migration, irreversible state,
  rollback/recovery/crash, and failure-consistency triggers still invalidate S;
  triggered M and all L work remain blocked until their required decision and
  review evidence is complete.
- [x] AC-4: Every M/L implementation still receives independent QA with each
  criterion recorded as Pass, Fail, Blocked, or Not applicable.
- [x] AC-5: Each specialist handoff names the role, bounded task, minimum
  required evidence, and expected output; complete conversation history and
  unrelated files are excluded by default. Missing evidence is reported or
  requested rather than invented.
- [x] AC-6: The minimum handoff evidence remains role-correct: PM receives
  product context/work item; Tech Lead receives persisted scope, architecture,
  and readiness evidence; RD receives accepted scope and ready gate; QA receives
  acceptance criteria, final diff, and readiness/decision boundary.
- [x] AC-7: For an unchanged normal M/L final candidate, RD runs focused checks
  and independent QA runs the complete default
  `./bin/vibe verify . --format json` once. A later shared implementation change
  invalidates that QA evidence and permits a new complete run.
- [x] AC-8: Post-upgrade takeover, release, or another flow with an explicit
  complete-verification requirement retains its specialized contract; checks
  against different candidate states are not classified as duplicates.
- [x] AC-9: Source, installed managed contracts, and packaged output remain
  consistent, with positive classification/handoff/dedup scenarios and
  high-risk counterexamples covered by deterministic tests.
- [x] AC-10: Static contract and distribution checks are not reported as proof
  of a measured token reduction or of live host behavior; any later percentage
  claim requires comparable host telemetry.
- [x] AC-11: The unpublished source/package/install/Plugin candidate identifies
  itself consistently as Vibe Kit `0.8.0`, core/Codex protocol 6, with existing
  schemas unchanged, an ordinary offline v0.7-to-v0.8 upgrade scenario, and no
  tag, network, or publication side effect.

## Design and technical notes

- Apply `.vibe/core/technical-decision-readiness.md` and persist a new Accepted
  decision before editing shared managed contracts.
- ADR 0008 remains the safety floor: token efficiency may narrow ordinary work
  but cannot weaken the existing trigger or review boundary.
- ADR 0012 owns the adaptive execution, bounded handoff, verification ownership,
  host-capability honesty, and unpublished-candidate compatibility boundary.

## Risks and open decisions

- Over-classifying work as S could bypass required shaping or review; risk and
  uncertainty must outrank file count.
- Over-trimming a handoff could hide decisive evidence; each role needs an
  explicit minimum evidence set and a fail-closed request-for-context path.
- Moving full verification to QA can delay broad feedback; RD focused checks
  remain mandatory during implementation.
- Static prompt tests can prove distributed wording but not live host token
  behavior. The first iteration makes no numeric savings commitment.
