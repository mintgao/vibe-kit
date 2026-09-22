# Raise the Hermes host label to verified and refresh the Codex conformance record under the schema-4 contract

- ID: `20260922-host-label-raise`
- Size: `M`
- Status: shaping
- Created: 2026-09-22

## Technical decision readiness

- Outcome: `covered-by-accepted-decision`
- Trigger evidence: the change updates the content of a durable shared contract — the per-host conformance label and its evidence references in the agent-install host registry — whose label semantics, evidence rule and raise condition are already owned by an Accepted decision, so the trigger is real but introduces no new durable choice
- Decision owner: Tech Lead perspective on this host: ADR 0019 owns the per-host label rule; this work item applies it and introduces no new architecture, boundary, schema, migration, recovery or security decision
- Governing decision: `docs/decisions/0019-host-adapters.md`
- No-new-decision rationale: none
- Review mode: `sequential-perspective`
- Review result: `approved`
- Review evidence: `docs/work-items/20260922-host-label-raise/technical-review.md#Review pass — approved`
- Material product decisions: resolved by the product owner: on 2026-09-21 (iteration 0.10.0, decision C) the Hermes label stays `supported-unverified` until its five-stage conformance record is complete, and the raise then follows as the recorded execution of that decision; on 2026-09-22 the product owner accepted the work-item plan and asked to start it, with the release that carries the change remaining a separate release-preparation step
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator, Hermes session 2026-09-22
- Confirmed at: 2026-09-22T16:15:35+08:00
- Confirmation basis: ADR 0019 owns the change, reads `Status: Accepted`, and its raise condition is met by the completed five-stage Hermes record (`docs/work-items/20260921-host-adapters/conformance.md`, commit `503f1a4`); the sequential review pass returned `approved` with three non-blocking notes; the material product decisions (decision C on 2026-09-21 and the start instruction on 2026-09-22) are resolved; `Open blockers: none`; every copy of the label and every affected test is enumerated in the brief
- Readiness history: 2026-09-22 the trigger scan found the durable shared-contract touch (host registry content) and cited ADR 0019 as the governing Accepted decision; the sequential review pass (`docs/work-items/20260922-host-label-raise/technical-review.md#Review pass — approved`; capability limitation: identity-isolated independent reviewer unavailable) returned `approved` with three non-blocking notes; the gate owner then confirmed `implementation-ready` after checking the decision, the review, the resolved material product decisions and the empty blocker list

## Goal

The contract tells the truth about both declared hosts: Hermes reads `verified`
because its five-stage conformance record is complete and recorded, and the
Codex record is refreshed under the schema-4 contract so both hosts' labels rest
on current, symmetric, citable evidence.

## Context

- The Hermes five-stage record landed on 2026-09-22: a genuinely new Hermes task
  admitted this repository's existing installation through the manual-new-task
  path, its schema-2 takeover object passed `validate-takeover` (`valid`, no
  errors, `manual_transfer_status: valid`), and
  `docs/work-items/20260921-host-adapters/conformance.md` now carries all five
  stages with command results and artifact digests (commit `503f1a4`).
- ADR 0019 owns the label rule: `verified` only where a host's record is
  complete and its evidence grade matches; labels change only with recorded
  evidence, never by assertion. The conformance record changed first, satisfying
  that precondition.
- Current declarations to change: `bin/vibe` `HOST_REGISTRY.hermes.conformance`
  (`label: supported-unverified`, `evidence: []`), its mirror
  `agent-install.json#hosts.hermes.conformance`, the guide table row in
  `AGENT_INSTALL.md`, the prose in `README.md` (two places), and the living
  context in `docs/context/product.md`; tests pin the old label in
  `tests/test_workflow_contract.py` and the guide row in
  `tests/test_host_adapters.py`.
- The label is descriptive: the only readers are the mirror-coherence check in
  the contract-shape validator and the tests; no operation is gated by it, and
  the fail-closed rules for unknown hosts stay untouched.
- The Codex schema-4 five-stage re-run remains a tracked follow-up
  (conformance.md, Codex section); no `codex` host is available in this
  environment, so the deliverable here is a runbook plus a host-neutral driver
  the Codex environment can execute, with the limitation recorded rather than
  hidden.
- The 0.10.0 release is frozen and its historical records (release note, ADRs,
  CHANGELOG entry, closed work items) describe the state at their time; they are
  not rewritten.

## Scope

- In: the Hermes conformance label and evidence references in the registry and
  every copy (contract mirror, guide table, README prose, living context doc,
  the conformance record's own label-raise wording); the release-identity
  regeneration for the touched payload files in the same change; regression
  tests pinning the new label, the evidence references and the mirror
  coherence; a Codex refresh runbook plus host-neutral driver recorded under
  this work item; this work item's records and the work-items index entry.
- Out: the release itself and its version bump; any schema, protocol, shape or
  behavior change; changing the label semantics or the fail-closed rules; the
  Codex run itself (performed in the Codex environment); other hosts.

## Acceptance criteria

- [ ] AC-1: The registry declares the Hermes label `verified` with an evidence
  reference to the completed conformance record, and every copy agrees after
  regeneration: the `agent-install.json` mirror, the `AGENT_INSTALL.md` table
  row, the `README.md` prose and the living context doc all read `verified` for
  Hermes, while the guide's general rule text for hosts without a complete
  record stays intact.
- [ ] AC-2: No behavior change: the label gates no operation, unknown hosts and
  incoherent selections still fail closed, and the only test edits are the
  assertions that pin the changed values (plus the new regression assertions).
- [ ] AC-3: Release identity: `payload_tree_sha256`, `activation_set_sha256`,
  the installed manifest and the plugin payload mirror are regenerated in the
  same change; `package` and `validate-release` pass on a frozen candidate and
  the repository's own `doctor` stays healthy.
- [ ] AC-4: Regression tests (standard-library `unittest`) pin the new label,
  the non-empty Hermes evidence references and the registry/contract mirror
  equality for `conformance`, and keep the fail-closed host-selection coverage.
- [ ] AC-5: The Codex refresh runbook and host-neutral driver exist under this
  work item, state exactly what ran where, and record that the Codex-side run is
  handed off to the Codex environment rather than claimed here.
- [ ] AC-6: For the frozen final candidate, the default lane passes on CPython
  3.13 and 3.9, `doctor` is healthy, and `validate-readiness` is valid for this
  brief.

## Design and technical notes

- Change set, all in one commit: `bin/vibe` `HOST_REGISTRY.hermes.conformance`
  (label plus `["docs/work-items/20260921-host-adapters/conformance.md"]` as the
  evidence reference), the `agent-install.json` mirror, the `AGENT_INSTALL.md`
  row `| \`hermes\` | 1 | none | verified |`, the two `README.md` statements, the
  `docs/context/product.md` sentence, and the conformance record's closing
  paragraph (raise pending, then raised).
- Leave historical records untouched: `docs/releases/0.10.0.md`,
  `docs/decisions/0019-host-adapters.md` and `0020`, the `CHANGELOG.md` 0.10.0
  entry, and closed work-item records keep their point-in-time wording.
- Regenerate identity with the repository's own procedure (the mirror rebuild
  script used for the previous work items) after the content edits, then prove
  with `package` plus `validate-release` and with the repository's own `doctor`.
- Test updates: `tests/test_workflow_contract.py` label assertion;
  `tests/test_host_adapters.py::test_guide_publishes_host_registry` row
  assertion; extend `test_registry_mirrors_stay_coherent` to also compare the
  `conformance` entry between the registry and the contract; add a small
  regression asserting the Hermes evidence reference is non-empty and points at
  the conformance record.
- Codex refresh: reuse the Hermes exercise shape (driver generates receipts,
  authors host-side artifacts, builds the schema-2 object, validates with
  `validate-takeover`) with one change — the successor task id is supplied by
  the host task (an argument) instead of being resolved from a Hermes-specific
  store — and document the runbook steps for a Codex-owned task. Evidence stays
  host-side; only the record update returns to the repository, following the
  same record-changes-first rule.
- Review runs as `sequential-perspective` on this host (analysis-shaped
  subagent review is not relied on; the limitation is recorded).

## Risks and open decisions

- Mirror cascade: every copy of the label must move together or the shape
  validator and the packaging tests fail closed; the rebuild script plus the
  full lane are the proof.
- Do not rewrite history: the 0.10.0 records and the 0.10.0-era decision text
  describe their time and stay as published; only living documents change.
- The Codex-side run depends on the product owner's Codex environment and may
  land later; the work item closes with the runbook delivered and the handoff
  recorded, and the Hermes label raise does not depend on it.
- Release routing (a patch release versus the next feature release) is a
  release-preparation decision and stays out of scope here.
