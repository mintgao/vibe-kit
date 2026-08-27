# Implementation record

- Work item: `20260827-architecture-decision-readiness-gate`
- Size: `L`
- Result: `complete`
- Completed: 2026-08-27
- Governing decision: [ADR 0008](../../decisions/0008-technical-decision-readiness-gate.md)
- Feedback source: [GitHub issue #3](https://github.com/mintgao/vibe-kit/issues/3)

## Delivery flow

This iteration followed the gated path defined by the accepted work item:

1. PM shaping fixed the product problem, scope, observable behavior, and 15 acceptance criteria without choosing the implementation architecture.
2. A Tech Lead perspective authored ADR 0008. An independent technical reviewer requested changes, then approved the revised persisted decision.
3. The workflow orchestrator confirmed `implementation-ready` only after the accepted decision and review evidence were present.
4. One RD writer implemented the accepted boundary while preserving concurrent repository work.
5. Independent QA mapped every acceptance criterion to evidence and exercised positive, release, direct-implementation, debug, negative, and reopen scenarios.

## Implemented mechanism

- Added one normative technical-decision readiness contract covering trigger scanning, size policy, readiness outcomes, ownership, review separation, fail-closed behavior, adoption, and reopening.
- Separated `product-shaped` from `implementation-ready` in the operating model and quality gates.
- Added an explicit Tech Lead adapter and aligned PM, RD, and QA role boundaries.
- Added the pre-implementation scan and stop/reroute behavior to feature, direct implementation, debug-to-fix, and verification flows.
- Extended the work-item template with durable readiness evidence fields.
- Added executable workflow-contract tests, including the `permission-safe-atomic-upgrade` dogfood case without an explicit ADR hint.
- Updated project context and user-facing documentation to describe the new contract.

## Main artifacts

- Normative contract: `.vibe/core/technical-decision-readiness.md`
- Lifecycle and gates: `.vibe/core/operating-model.md`, `.vibe/core/quality-gates.md`
- Work-item evidence template: `.vibe/core/templates/work-item-brief.md`
- Host role adapter: `.codex/agents/vibe-tech-lead.toml`
- Flow adapters: `.agents/skills/vibe-feature-flow/SKILL.md`, `.agents/skills/vibe-implementation-flow/SKILL.md`, `.agents/skills/vibe-debug-flow/SKILL.md`, `.agents/skills/vibe-verification-flow/SKILL.md`
- Contract tests: `tests/test_workflow_contract.py`
- Independent evidence: `verification.md`

## Verification result

- Acceptance criteria: AC-1 through AC-15 passed.
- Workflow contract: 7/7 tests passed.
- Full repository verification: 29/29 tests passed.
- Patch hygiene: `git diff --check` passed.
- Controlled fresh-Codex scenarios passed for blocked detection, accepted-decision release, direct implementation, debug-to-fix routing, S/M false-positive boundaries, and readiness reopening.

## Known limitations

- A real non-Codex host that only supports sequential perspectives was not exercised; the normative fallback contract and persisted evidence requirements were reviewed, but that host capability remains unverified.
- Readiness is enforced through the normative workflow, managed Skills, role adapters, durable work-item evidence, and conformance tests. The CLI does not mechanically parse every work item and reject implementation commands.
- The current checkout's root `vibe doctor` remains unhealthy because installed metadata is still `0.4.0` while concurrent accepted development work targets unpublished `0.5.0` / protocol 3. Fresh-install and historical-upgrade fixtures pass; this iteration intentionally did not publish or rewrite shared release metadata.

## Close decision

The implementation satisfies the accepted ADR and all product acceptance criteria. No additional qualifying Vibe Kit gap was found during this iteration, so Close does not create a second feedback candidate. GitHub issue #3 remains the traceable source item; release and issue-closing actions are outside this iteration.
