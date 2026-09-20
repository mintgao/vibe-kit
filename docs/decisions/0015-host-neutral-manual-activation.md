# 0015: The manual new-task activation path is host-neutral, and managed contract text follows the installed contract

- Status: Accepted
- Date: 2026-09-21
- Decision owner: read-only Tech Lead author `vibe_tech_lead`
- Work item: `docs/work-items/20260921-host-neutral-manual-activation/brief.md`
- Evidence: feedback issues #10 and #12, retrospective #13 finding F1, and the receiving host's accepted `validate-takeover` result

## Context and applicable decisions

A real receiving host (Hermes) completed the manual new-task path after a 0.3.0 to 0.9.0 migration, produced a takeover object that installed `bin/vibe validate-takeover` accepted with `status: valid`, `host_evidence_authenticated: false` and `ready_claim: false`, and filed feedback issues #10 and #12 plus retrospective #13. Finding F1 of #13 is decisive: the contract never states whether a non-Codex host may use the manual path, so the only completed end-to-end activation rests on an unstated permission. Issue #12 is the mechanical defect: the managed `AGENTS.md` block tells readers to follow the installed contract for `takeover schema 1` while the installed `agent-install.json` declares `takeover.schema_version: 2`.

The installed contract already describes the manual path without naming a host: `activation.current_repository_capability` is `manual-fallback-only`; `adapter.capabilities.manual_new_task` is `supported` with required receipt `manual-task-start`; `same_task_reload` and `automatic_successor_handoff` are `conditional` with `current_claim: false`. Only `adapter.name: codex` reads as host-restrictive.

ADR 0001 continues to govern managed/project ownership; ADR 0008 governs readiness authority; ADR 0010 governs installation transaction and recovery unchanged; ADR 0011 governs host-owned network operations and exact-source trust; ADR 0012 governs bounded handoffs and verification ownership; ADR 0014 governs managed documentation boundaries and authenticated managed regions.

## Decision: the manual new-task path is host-neutral

Any host that can start a new task in the same project may own the successor task and supply the `manual-task-start` receipt. `adapter` metadata and the activation fingerprint describe the host that installed or adopted the version; they do not restrict which host owns the successor task. The `codex` adapter name identifies the verified integration, not a runtime requirement on the successor. Every surface that states the manual fallback action (the managed `AGENTS.md` block, `AGENT_INSTALL.md` including its quoted Chinese message, `bin/vibe` instruction strings, both Plugin Skills and the `README.md` / `README.zh-CN.md` pair) states one host-neutral action and agrees with the others.

Host-neutrality changes who may use the manual path; it does not relax that path. A host that cannot recompute the installed identities must take the unchanged degraded stop (`reason_code=manual-new-task-required`, `next_action.code=create-new-project-task`) and must not supply a receipt. A structurally valid `validate-takeover` result is not authentication: `host_evidence_authenticated=false` and `ready_claim=false` remain explicit, and a fabricated or unverifiable receipt is a host failure, not a contract variant.

## Decision: managed contract text follows the installed contract

The managed `AGENTS.md` block references the takeover schema declared by the installed `agent-install.json` instead of a hard-coded number, and no managed surface declares a schema number that disagrees with the installed contract. The reference tracks the installed contract by construction of the text only: the block is authored text, not generated from the contract, and this decision adds no materialization step, CLI command, or validator change.

Enforcement is part of the decision: a regression test fails when a managed surface's declared takeover schema and the installed contract disagree; a second fails when a single host name is reintroduced on any manual-fallback surface; a third fails when the release payload digest and the identity mirrors disagree, which is the condition that left `main` failing `./bin/vibe package` while `doctor` still reported healthy.

## Consequences and boundaries

Unchanged: receipt content requirements (recompute the installed identities and validate any transfer identifier), the degraded stop with `reason_code=manual-new-task-required` and `next_action.code=create-new-project-task`, host-task-state-only custody, and the fail-closed rule for unknown capability. Same-task reload and automatic successor handoff stay `conditional` and unclaimed for every host until positive live conformance evidence exists. The compatibility claim is unchanged: the Codex adapter remains the only verified Agent integration, so host-neutrality widens permission on the manual path, not the compatibility claim.

Projects already installed at 0.9.0 keep their installed managed block, including its Codex-scoped action sentence and its `takeover schema 1` reference, until they adopt a newer version. This decision requires no in-place rewrite, no migration, and no `validate-takeover` change; the clarified permission and the corrected reference reach an installed project only with the next version's managed block, and the next release preparation carries the release section for this change.

This change is prose and scope only: no schema, protocol, enum, validator, receipt, custody or CLI-result change. `agent-install.json` keeps its closed top-level field set and adapter capability claims; only its regenerated activation mirror changes. Release identity mirrors (the Plugin payload digest and the manifest source payload digest and activation mirrors) must be regenerated in the same change. No version or protocol bump occurs in this change.

## Follow-ups out of scope

- Publishing the takeover object schema (F2).
- A receipt-writing helper (F7).
- A minimal manual transfer payload (F12).
- Recording host capability limitations when subagent budgets cannot finish the verification lane (F10).
- An environment-limited check state (F11).
- Configured-check ordering (issue #9).
