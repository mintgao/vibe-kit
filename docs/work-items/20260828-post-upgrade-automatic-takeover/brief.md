# Post-upgrade automatic takeover

- ID: `20260828-post-upgrade-automatic-takeover`
- Size: `L`
- Status: compatibility-repair
- Created: 2026-08-28
- Completed: 2026-08-28

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: real-project release acceptance exposed a new migration, compatibility, managed-ownership and trust-boundary decision for authenticating predecessor files that become managed in 0.6.0
- Decision owner: Tech Lead perspective; authenticated-predecessor compatibility amendment accepted on 2026-08-28
- Governing decision: Accepted amended ADR 0009, with Accepted ADRs 0005, 0007 and 0008 as inherited boundaries
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: the distinct independent reviewer recomputed the registry, predecessor-installation and contract-set digests; required and re-reviewed symlink-free AGENTS/path-chain authentication, predecessor-source exclusion, exact closed mirror paths/shapes and a matching normative maintenance-bridge object; final verdict approved
- Material product decisions: resolved by the user in this task — one exact-version confirmation, automatic post-upgrade adaptation and original-goal resumption, truthful unsupported-host degradation, and ready language only after activation/readiness/verification
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: 2026-08-28T06:16:42Z
- Confirmation basis: Workflow orchestrator checked the Accepted ADR 0009 compatibility amendment, independent digest evidence and approved review, exact official v0.5.0 complete-set boundary, fail-closed partial/mixed/symlink/race behavior, additive schema-1 evidence, cross-channel mirror requirements, manual-fallback truthfulness, project ownership, Python 3.9 and atomic-upgrade separation, with `Open blockers: none`
- Readiness history: 2026-08-28 — classified L; PM and UX read-only shaping completed; shared lifecycle/protocol/compatibility/host/recovery triggers required a technical decision; read-only Tech Lead authored ADR 0009; independent review requested two rounds of changes; the exact resolved ADR was approved and accepted; Workflow orchestrator confirmed implementation-ready before shared implementation edits. After implementation, independent QA returned Not ready: the only claimed manual fallback lacked installed normative contracts, schema 2 could not execute the normative invariants, and required controlled takeover scenarios were static assertions. Readiness reopened as `decision-required + blocked` before repair edits. The Tech Lead authored an ADR 0009 amendment; independent review required deterministic activation normalization, installed-contract authentication, complete nested validation, custody history and registry identity corrections before approval. The amended ADR was accepted and the Workflow orchestrator reconfirmed implementation-ready before repair edits. Real-project release acceptance then exposed that the official v0.5.0 source checkout already contains both newly managed Agent-install contracts outside its managed manifest, so 0.6.0 safely but incompatibly blocks plan. The gate reopened again as `decision-required + blocked` before compatibility repair edits. The Tech Lead authored a closed authenticated-predecessor migration; independent review verified all digests and required two correction rounds covering symlink-free paths, predecessor-source exclusion and exact mirror/bridge shapes. The amendment was accepted and the Workflow orchestrator reconfirmed implementation-ready at 2026-08-28T06:16:42Z before compatibility code edits.

## Goal

Make an explicitly confirmed Vibe Kit version upgrade one continuous Agent-owned
experience: verify the exact trusted version, preview and apply the safe upgrade,
activate the new repository rules, adapt project context when needed, re-evaluate
and resume the originating development request, verify the resulting state, and
only then report that development may continue.

The developer must not need to issue a second confirmation, invoke internal
commands or Skills, request onboarding or verification, or repeat the original
goal.

## Context

The product already provides trusted version selection, read-only upgrade
planning, managed/project-owned boundaries, structured upgrade results, conflict
evidence and `doctor`. The missing contract is between “managed files were
written” and “the target-version rules are active and the project is ready.”

Current evidence:

- `bin/vibe upgrade` proves an apply result but cannot prove that a running Agent
  loaded the new repository instructions.
- `doctor` separates installation health from onboarding readiness; a healthy
  installation may still be pending project understanding.
- the maintenance Plugin stops after apply, doctor and conditionally relevant
  verification; it does not close activation, adaptation or original-goal
  resumption.
- ADR 0007 provides a one-new-task fallback and explicitly avoids assuming
  portable hot reload or automatic task creation.

## Observable states

- **Upgraded:** target-version managed files and installation state were applied
  consistently, and the installed target-version doctor is not `broken`.
- **Activated:** the current or successor Agent task has positive host evidence
  that target-version repository instructions and Skills govern execution.
- **Adapted:** onboarding is complete or evidence shows no refresh is needed;
  material repository/context contradictions remain blocking.
- **Re-evaluated:** the unfinished original request was classified and routed
  under target-version rules before further shared implementation work.
- **Verified:** required installed health and applicable project checks passed;
  executed and skipped checks are reported truthfully.
- **Ready:** every applicable state above is satisfied. Only this state permits
  unconditional “升级完成，可以继续开发.”
- **Degraded/blocked:** at least one stage is incomplete; report the last completed
  stage, write state, one concrete reason, and one safe next action or material
  decision.

## Scope

### In

- Exact-version confirmation, trusted source verification and read-only planning.
- Safe apply without a redundant conversational confirmation.
- Versioned separation of upgraded, activated, adapted, verified and ready.
- Same-task activation when supported; automatic successor-task handoff when
  supported and required; one-action manual fallback otherwise.
- Preservation and transfer of the original development request across takeover.
- Evidence-backed onboarding/refresh without template-regenerating project facts.
- Target-version re-evaluation before further application/shared implementation.
- Installed doctor, applicable configured verification and truthful final reports.
- Cross-channel human/machine contracts and scenario coverage.

### Out

- Silent version discovery, moving refs, silent pre-release selection or network
  resolution inside the offline CLI.
- Silent conflict resolution, permission expansion or uncertain project-fact
  overwrite.
- Application migrations caused solely by a Vibe Kit upgrade.
- Pretending to provide host hot reload or automatic task creation where the host
  has no such capability.
- Whole-upgrade filesystem atomicity, which remains owned by
  `20260827-permission-safe-atomic-upgrade`.
- New compatibility claims for unverified Agent adapters or release publication.

## Acceptance criteria

- [x] **AC-1 — Single confirmation:** Given an exact target version and project
  confirmed once, the Agent verifies the trusted source, reports current/target
  versions and does not request another upgrade confirmation after a safe plan.
- [x] **AC-2 — Read-only plan:** Planning changes no project, conflict-evidence,
  onboarding, handoff or installation-state files.
- [x] **AC-3 — Safe ownership:** Apply preserves current managed-conflict,
  project-ownership, source, permission and no-silent-resolution guarantees.
- [x] **AC-4 — Honest stages:** Apply and installation version changes can prove
  upgraded only; they can never by themselves produce activated or ready.
- [x] **AC-5 — Same-task activation:** A capable host supplies positive evidence
  that a target-version-only rule governs the same task before adaptation or
  resumed implementation proceeds, without further user input.
- [x] **AC-6 — Automatic handoff:** A capable host that cannot live-reload passes
  the exact project, target version and original goal to a successor task, which
  continues without user recreation, Skill vocabulary or request repetition.
- [x] **AC-7 — Portable degradation:** A host supporting neither path reports
  files upgraded but activation incomplete, does not assume target-rule execution,
  does not say ready, and gives one non-CLI new-task action.
- [x] **AC-8 — Evidence-backed adaptation:** Pending, missing, stale or
  contradicted onboarding triggers automatic evidence review. Existing context is
  preserved unless evidence supports an update; invalid or unresolved states block.
- [x] **AC-9 — New-rule re-evaluation:** Before further application/shared edits,
  the unfinished original request is routed under target-version rules and resumes
  unless those rules expose a material user decision or valid readiness blocker.
- [x] **AC-10 — Closed verification:** The installed target-version doctor and all
  applicable configured checks run; executed, unconfigured, skipped and failed
  outcomes are explicit, and required skipped/failed checks prevent ready.
- [x] **AC-11 — Truthful success:** Success states exact version/source,
  activation path, adaptation outcome, verification evidence and original-goal
  status; unconditional ready language appears only after every gate passes.
- [x] **AC-12 — Truthful incomplete states:** Source failure, blocked plan,
  conflict, `unknown-partial`, activation failure, invalid onboarding, failed
  verification and host limitations each report true write state, last completed
  stage and one safe next action or material decision.
- [ ] **AC-13 — Scenario coverage:** Automated and controlled Agent scenarios cover
  maintenance-only upgrade, same-task activation, automatic handoff, unsupported
  host fallback, onboarding refresh, new-rule readiness discovery, verification
  failure and existing upgrade safety regressions.
- [x] **AC-14 — Cross-channel identity:** Direct release, Plugin payload and
  marketplace human/machine contracts stay synchronized; validation rejects
  lifecycle, protocol or behavior drift.

## Design and technical notes

- User-visible semantics are defined in `design.md`.
- A maintenance-only request ends ready without inventing application work. When
  upgrade is a prerequisite inside an unfinished development request, successful
  takeover resumes that exact request.
- Host permission prompts remain authoritative; the product confirmation does not
  broaden source, credentials, network or filesystem scope.
- Existing onboarding state remains project-owned. Upgrade materialization does not
  rewrite it; evidence-backed onboarding owns any justified refresh.
- Unknown schema, lifecycle enum, warning classification or activation outcome
  fails closed rather than being coerced into success.

## Risks and open decisions

- Define positive activation evidence and host capability negotiation without
  letting the offline CLI claim host behavior.
- Define original-goal transfer without persisting sensitive conversation content
  into the repository or duplicating work across tasks.
- Evolve result schema/protocol/version compatibility without reusing the published
  immutable 0.5.0 release.
- Compose takeover stages with `unknown-partial` and the separate atomic-upgrade
  work without conflicting writers or inconsistent recovery claims.
- Define machine-readable verification and warning readiness semantics.
