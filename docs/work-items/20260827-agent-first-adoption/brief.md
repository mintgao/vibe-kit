# Agent-first Vibe Kit adoption

- ID: `20260827-agent-first-adoption`
- Size: `L`
- Status: verified-with-limitations
- Created: 2026-08-27

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: L change to a durable Agent adoption contract, acquisition/runtime trust boundary, CLI result and onboarding schemas, core/Codex protocol versions, project-owned readiness ownership, compatibility, failure recovery, and release validation.
- Decision owner: Read-only Tech Lead author perspective (`agent_first_tech_author`)
- Governing decision: [ADR 0007 — Accepted](../../decisions/0007-agent-first-adoption-contract.md)
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: Independent Tech Lead reviewer (`agent_first_tech_review`) approved the exact persisted ADR 0007 revision on 2026-08-27 after confirming the rejected prose-parsing and hot-reload alternatives, closed result/onboarding/write-state enums and fail-closed evolution rules, caller-attested provenance boundary, truthful partial-write recovery, ownership, compatibility, and task-handoff constraints. The reviewer also confirmed that this approval does not rewrite the truthful late-adoption history.
- Material product decisions: none; the unresolved items are internal trust, state, compatibility, and recovery contracts inside the accepted product scope.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator (`/root` perspective)
- Confirmed at: `2026-08-27T15:24:03Z`
- Confirmation basis: Accepted product brief and design, Accepted ADR 0007, exact-revision approval from an independent Tech Lead reviewer, no material product decision, and no remaining readiness blocker.
- Readiness history: `2026-08-27 — Work started before the technical-decision readiness gate landed concurrently. PM/UX shaping and ADR 0007 preceded implementation, but no pre-implementation Tech Lead review or implementation-ready record existed. Independent QA identified the timing gap. The active work adopted the new gate honestly at QA, froze further shared code changes, and moved to decision-required/blocked; no retroactive pre-implementation claim is made. Late-adoption Tech Lead author required a targeted ADR amendment. The first independent review returned changes-required for missing alternatives, ambiguous closed-enum/schema evolution, and mixed readiness/implementation blockers; the persisted decision and readiness text were revised without resuming shared code. The independent reviewer then approved the exact revision; ADR 0007 was accepted and the orchestrator confirmed implementation-ready before repair work resumed.`

## Goal

Make Vibe Kit an Agent-first project operating protocol. A developer gives Codex the canonical GitHub link, a target/new-project intent, and a development goal; Codex owns release selection, verification, safe installation, health checks, first-run project understanding, and later workflow routing. The developer does not need to download archives, choose `init` versus `adopt`, run Vibe CLI commands, or name internal Skills.

## Context

- The current public path exposes a two-layer release bundle, absolute CLI paths, `plan`, `init`/`adopt`, `doctor`, an explicit onboarding Skill, and a new-task requirement in the primary README flow.
- Vibe Kit already has the correct trust primitives: immutable release payloads, SHA-256 metadata, repository-pinned runtime files, read-only plans, managed/project-owned boundaries, and a bootstrap-only Plugin.
- The product and architecture contexts identify Codex as the only verified adapter and forbid silent network updates or following `main`.
- Durable design is recorded in [ADR 0007](../../decisions/0007-agent-first-adoption-contract.md). Interaction states are recorded in [design.md](design.md).

## Scope

- In: a root, release-packaged Agent installation guide plus a machine-readable adoption contract discoverable from a normal GitHub repository link.
- In: exact-tag/release selection, stable-by-default bare-repository policy, one explicit pre-release decision when no stable release exists, scoped source/target trust, and no fallback to `main` or an unverified payload.
- In: non-interactive structured output for the install-critical CLI paths (`plan`, `init`/`adopt`, `doctor`, release validation, and upgrade where shared code makes it coherent), while preserving existing text output and exit behavior.
- In: project-owned onboarding readiness state, automatic first-run onboarding, resumption of the original development request, and natural-language routing through the existing repository Skills.
- In: Plugin bootstrap/maintenance instructions and README information architecture that keep commands internal to Agent and maintainer flows.
- In: source provenance in the installed manifest/receipt when the invoking Agent supplies the selected channel, immutable ref, and artifact digest.
- In: release and scenario tests proving contract discovery, cross-channel payload equality, structured results, project-owned preservation, onboarding behavior, and existing safety boundaries.
- Out: a network resolver or updater inside `bin/vibe`, `curl | sh`, automatic tracking of `main`, silent pre-release adoption, public Plugin Directory publication, package-manager publication, release publication, automatic Git commits, or telemetry.
- Out: automatic task creation in hosts that do not expose it, arbitrary GitHub forks as trusted canonical sources, non-Codex compatibility claims, or replacement of framework-specific project generators.
- Out: silently resolving managed-file conflicts, overwriting project-owned context, or making whole-install permission failure atomic; the latter remains tracked by the separate permission-safe atomic upgrade work item.

## Acceptance criteria

- [x] AC-1: The README first screen presents only Agent-oriented natural-language examples for adopting an existing project and creating a new project, then tells the user to continue with ordinary development language; manual CLI material is clearly secondary maintenance/troubleshooting documentation.
- [x] AC-2: `AGENT_INSTALL.md` and `agent-install.json` define a versioned, Codex-scoped state machine for source selection, target/mode choice, plan, apply, doctor, handoff, onboarding, success, and blocking states. A bare canonical repo selects stable only; an exact pre-release tag is honored; a bare repo with no stable requires one user decision.
- [x] AC-3: The Agent contract, direct release ZIP, Plugin bundled payload, and expanded marketplace contain byte-identical installation guidance, and release validation rejects a missing, malformed, version-drifted, or channel-drifted contract.
- [x] AC-4: Install-critical commands support versioned JSON results without changing their default human-readable output or established exit codes. Safe/blocked plans, successful install, structured errors, healthy/warning/broken doctor states, and release validation results are machine distinguishable without parsing prose.
- [x] AC-5: An install can record validated source type, immutable ref, and artifact SHA-256 in `.vibe/manifest.json` and the JSON receipt. Invalid digest/ref inputs fail before project writes. Existing invocations remain supported with an explicit local-payload source classification.
- [x] AC-6: Fresh `init` and `adopt` create a project-owned `.vibe/onboarding.json` in `pending`; an existing file is preserved byte-for-byte. Missing state remains compatible with older installations, while malformed state is diagnosable.
- [ ] AC-7: The managed `AGENTS.md` automatically routes ordinary requests, runs onboarding internally when state/context requires it, and resumes the original request. The onboarding Skill marks readiness complete only after evidence-backed context is updated. Users are never required to name `$vibe-project-onboarding` or another internal flow.
- [ ] AC-8: The bootstrap Plugin keeps plan/apply/doctor internal, does not request redundant confirmation after a scoped install request and safe plan, and degrades to one non-CLI new-task handoff when repository instructions cannot be reloaded in the current task.
- [x] AC-9: Existing business files, project-owned configuration/context, repository-specific AGENTS content, offline installation, conflict failure, version integrity, and release/Plugin tamper rejection retain regression coverage.
- [x] AC-10: The implementation is packaged as the next unpublished development version with synchronized core, protocol, Plugin, changelog, release note, and durable product/architecture context. It passes the configured test suite, `doctor`, release validation, Python bytecode compilation, and independent QA; unsupported host/Linux checks are reported rather than inferred.

## Design and technical notes

- CLI commands are implementation tools for Agents and maintainers, not the primary human product surface.
- Remote resolution remains an Agent/host responsibility. The local CLI accepts only a selected local payload and never gains implicit network authority.
- The first implementation trusts only `https://github.com/mintgao/vibe-kit` as canonical. A fork or alternative repository requires a separately explicit source decision.
- Repository-pinned files remain the runtime source of truth. Plugin and GitHub are acquisition channels only.
- A new Codex task remains the reliable activation boundary. Hosts may automate the handoff; the portable fallback is one instruction to open a task in the project and state the development goal normally.

## Risks and open decisions

- GitHub release/tag identity plus asset digests remain the publisher trust signal; signatures and external provenance are not yet available.
- A plan and later apply remain separate operations, so filesystem changes between them are re-preflighted but not bound by a plan token.
- Installation uses atomic file replacement but is not a whole-directory transaction on interruption or permission failure.
- The repository can define a task handoff contract but cannot force every Agent host to hot-load new repository instructions or create a task automatically.
- This work prepares an unpublished `0.5.0` candidate; stable or pre-release publication is a separate explicitly authorized release operation.
