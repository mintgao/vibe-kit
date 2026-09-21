# Verification contract closure: declared check order, preserved failure output, constrained-QA evidence and environment-limited states

- ID: `20260921-verify-contract-closure`
- Size: `L`
- Status: shaping
- Created: 2026-09-21

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: the change alters the verify receipt's closed contract (a recordable environment-limited verdict plus the toolchain fields the receipt carries) and the derivation of the effective check order that publication and closeout consume, so it is durable, cross-system and compatibility-relevant work at size L; it also changes the operating model's rule for who may own the complete default verification on a budget-limited host
- Decision owner: Tech Lead author, `vibe_tech_lead` perspective (Hermes subagent, dispatched 2026-09-21), which authored `docs/decisions/0017-verification-contract-closure.md`
- Governing decision: `docs/decisions/0017-verification-contract-closure.md`
- No-new-decision rationale: none
- Review mode: `sequential-perspective`
- Review result: `approved`
- Review evidence: `docs/work-items/20260921-verify-contract-closure/technical-review.md#Pass 2 — approved`
- Material product decisions: resolved by the product owner on 2026-09-21 (iteration 0.10.0) — (a) issue #9 is fixed by an explicit check-dependency declaration in `.vibe/project.yaml`, with the effective order written into the receipt and the contract prose; (b) the F10 path is recorded in the operating model as orchestrator-runs-the-complete-lane plus an independent focused re-run by a bounded subagent plus a recorded capability limitation; (c) environment-limited verdicts get a recordable state instead of a misleading failure; (d) failure output preservation is configurable and does not downgrade by default; (e) each work item in this iteration delivers brief, implementation plan, technical review and verification records
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator, Hermes session 2026-09-21
- Confirmed at: 2026-09-21T11:59:26+08:00
- Confirmation basis: ADR 0017 at revision 2 was reviewed against the brief's acceptance criteria; Pass 1 returned changes-required on one blocking attribution defect (the context section mislabeled #9/F6/F10/F11 and contradicted its own evidence bullet), the author's revision corrected it, and Pass 2 approved with two non-blocking notes carried into `implementation.md` §3 and §5 (the environment-limited classification trigger and the constrained-QA record form); the review ran as a separate sequential pass because the host's subagent channel timed out on every analysis-shaped review task at its 600 s budget
- Readiness history: 2026-09-21 the trigger scan found the compatibility and schema trigger above and the record started `decision-required + blocked` with no application or shared implementation code edited; the Tech Lead author (subagent) then wrote `docs/decisions/0017-verification-contract-closure.md`; review Pass 1 required one attribution fix, revision 2 landed, and Pass 2 approved it as `docs/work-items/20260921-verify-contract-closure/technical-review.md#Pass 2 — approved` recording `Capability limitation: identity-isolated independent reviewer unavailable`; the gate then moved to `implementation-ready`

## Goal

A repository can declare the order and dependencies of its configured checks so a clean tree does not misreport; a failing lane leaves enough output to diagnose the failure from the receipt; a host whose subagent budget is smaller than the lane has a sanctioned, recorded QA path; and a verdict that depends on the host environment can be recorded truthfully — all without weakening fail-closed coverage for publication and closeout.

## Context

- Issue [#9](https://github.com/mintgao/vibe-kit/issues/9): the default order is hardcoded `lint → typecheck → test → build`, so a repository whose `test` consumes build artifacts fails on a tree without a fresh full build. The reported attribution was later corrected by evidence: the mechanism that actually failed was an environment-dependent exemption predicate, which is also finding F11.
- Issue [#13](https://github.com/mintgao/vibe-kit/issues/13) finding F6: each check's captured output is truncated to a 16 KB tail, so per-file verdicts of a failing check were not recoverable from the receipt and the investigation had to re-run parts of the suite outside the lane.
- Finding F10: the operating model makes independent QA the canonical owner of the complete default `verify` run, but this host's subagent sessions are capped at 600 seconds while the lane takes 3–10 minutes; both QA attempts timed out after running the lane but before reporting, and the documented fallback covers only hosts without subagents, not hosts whose subagents cannot finish the work.
- Finding F11: when a failing check depended on which Node line the host shell resolved (Node 22 versus the project's documented Node 24), the only recordable outcome was `verification-failed → fix-configured-check`; there is no state for "this verdict depends on the host environment".
- Existing surface: `VERIFY_ORDER` is the hardcoded tuple in `bin/vibe`; the verify receipt already carries `default_order` and a per-check truncation flag; the installed contract declares a closed verify shape (statuses, default order, outcomes `passed/failed/unconfigured/skipped`, and skipped reasons) that validation compares exactly.
- Applicable decisions: ADR 0008 governs readiness authority; ADR 0014 governs the readiness evidence grammar and the verify additions of 0.9.0; ADR 0002 and 0011 govern the repo-pinned offline trust model, which this work changes nowhere; ADR 0016 governs decision-file naming. This work adds a new decision record for the verify contract.

## Scope

- In: the verify implementation in `bin/vibe` (configuration parsing, order derivation, receipt fields, output-preservation policy, the environment-limited outcome, toolchain recording); the additive `.vibe/project.yaml` declaration; the closed verify contract declaration in `agent-install.json`; the operating model's QA-ownership rule for budget-limited hosts; the verify contract prose; regression tests in `tests/`; the new decision record; this work item's records; the release-identity mirrors (same change).
- Out: publication and closeout profile/schema versions and the release itself (the release work item owns those); the takeover object, receipts and admission path (work item 3); host adapters and per-host payloads (work item 4); splitting the CLI (deferred); moving or rewriting any historical profile boundary; any change to the trust model.

## Acceptance criteria

- [ ] AC-1: `.vibe/project.yaml` may declare check dependencies or order, the effective order is derived deterministically and recorded in the receipt, and a repository whose `test` consumes build artifacts no longer misreports on a clean tree; the declaration is validated fail-closed (unknown check names, unknown keys, or dependency cycles fail with actionable messages).
- [ ] AC-2: Per-check output preservation is configurable and does not silently downgrade; when a check fails, its per-file verdicts are recoverable either from the receipt or from a referenced full-output artifact on disk, and a regression test proves that recovery.
- [ ] AC-3: The operating model defines and requires the compliant path for a host whose subagent budget is smaller than the lane — the orchestrator runs the complete default verification, an independent bounded subagent re-runs a focused subset, and the work item records the host capability limitation — with a machine-checkable record form.
- [ ] AC-4: A verdict that depends on the host environment is recordable as an environment-limited state distinct from passed, failed and skipped; the receipt records the toolchain versions that produced the verdict; publication and closeout treat environment-limited coverage as not passing.
- [ ] AC-5: The closed verify contract in `agent-install.json` matches the new order and outcome semantics, validation keeps rejecting unknown statuses, outcomes and skipped reasons, and historical 0.7–0.9 receipts keep their recorded semantics.
- [ ] AC-6: Compatibility and recovery are explicit: a repository with no declaration keeps the current effective order; the change is revertible without migration (additive fields, defaults restorable); no published profile boundary moves; and the work item states the rollback path.
- [ ] AC-7: For the frozen final candidate the default verification lane passes, `doctor` is healthy, `validate-readiness` is valid for this brief, and every behavior change has a regression test in `tests/` using the standard library only.

## Design and technical notes

- Order derivation: prefer an explicit declaration in `.vibe/project.yaml` (product decision) over guessing from file names; the receipt must keep describing the effective order so a reader never has to infer it, and the declaration must not be able to hide a genuinely broken configured check.
- Environment-limited state: extend the outcome vocabulary rather than reusing `skipped`, require a reason plus the observed toolchain, and make every readiness consumer treat it as not passing.
- Output preservation: keep the default at least as informative as today, allow a configured bound, and prefer writing full output to a project-local artifact that the receipt references by path and digest.
- Constrained QA: prose plus a record shape only; the kit's own lane is roughly 40 seconds, so this repository can demonstrate the compliant record immediately.
- Release identity: this change edits release-payload files, so the payload and activation mirrors must be regenerated in the same change using the recorded procedure.
- Deliverables for this work item: `brief.md`, `implementation.md` (explicit plan), `technical-review.md`, `verification.md`.

## Risks and open decisions

- Schema ripple: the verify receipt is consumed by publication and closeout; keep changes additive, document the compatibility rule, and leave version and profile bumps to the release work item.
- Loophole risk: environment-limited could become a way to avoid a real failure; publication treats it as not passing, and the state requires an explicit reason and the toolchain that produced it.
- Order declaration could mask a broken check: fail-closed validation plus a self-describing receipt keep the effective order auditable.
- Recovery: removing the declaration restores the default order, and the new receipt fields are additive, so the change reverts without data migration; historical receipts are never rewritten.