# Publish and verify Vibe Kit 0.12.0 Pre-release

- ID: `20261028-v0-12-publication`
- Size: `L`
- Status: implementation-ready
- Created: 2026-10-28

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: New exact publication and issue-closeout schemas, irreversible public GitHub state, public-source privacy, version compatibility and postpublication project upgrade.
- Decision owner: vibe_tech_lead read-only publication decision author
- Governing decision: `docs/decisions/0023-readonly-run-inspection-and-entrypoint-evidence.md`, `docs/decisions/0024-v0-12-publication-and-separate-closeout.md`
- No-new-decision rationale: none
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: `docs/work-items/20261028-v0-12-publication/technical-review.md`
- Material product decisions: Publish the accepted F1/#20, F2/#22 and F3/#23 scope as exact 0.12.0 Pre-release in mintgao/vibe-kit; close only completed #20/#22/#23 after public verification; then perform the official target-version upgrade for the authorized development project, stopping at the required activation boundary.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: 2026-10-28T04:46:51.746876+00:00
- Confirmation basis: Distinct exact-hash technical approval of ADR0023/0024, feature contract and scoped brief; governing ADRs Accepted; resolved authorized scope and no open blocker.
- Readiness history: 2026-10-28 decision-required/blocked before implementation; different-instance exact persisted review approved; administrative ADR acceptance and orchestrator implementation-ready confirmation only, with reviewed technical content preserved.

## Goal and scope

Publish an independently accepted, sanitized 0.12.0 source candidate through the repository's offline intent and host-owned GitHub workflow. Preserve historical release contracts and existing project state. The public candidate starts at upstream main and contains only reviewed feature and publication changes; unrelated local history is excluded.

In scope: F1 exact onboarding integer validation; F2 bounded actual-entry focused evidence guidance and managed example; F3 safe read-only historical run inspection; exact new publication/closeout profiles; bilingual release documentation; normal draft PR, review/check assessment and merge; annotated tag, non-draft Pre-release and exactly five assets; fresh public downloads and independent acceptance; separately authorized evidence-bound #20/#22/#23 closeout; later publication-fact evidence; official downloaded-target upgrade and healthy doctor before the activation boundary.

Out of scope: implementation or closure of #21/#26 (assessment only) and #24/#25 (deferred); stable promotion; force, deletion, tag movement or asset replacement; protection bypass; runtime activation without host evidence; public private logs or host custody; credentials, global configuration or other repositories; claims of signing, universal secret detection, measured efficiency or live-model compliance.

## Acceptance criteria

- AC-1: F1/#20 accepts exact integer 1 only, rejects invalid onboarding versions without rewriting state, and is verified through real entry paths.
- AC-2: F2/#22 documents the bounded configured/default entry, loaded helper origin/arguments, focused Python discovery and Node script evidence, while preserving historical callers and QA ownership.
- AC-3: F3/#23 is discoverable, read-only and bounded; distinguishes metadata, receipt, coverage, binding, artifacts and historical verdict from unattested origin/unproven applicability; interruption and wrong-run evidence remain non-passing.
- AC-4: Existing receipt/producer defaults, predecessor upgrades, offline Python 3.9+ standard-library operation and historical publication/closeout semantics remain compatible.
- AC-5: An Accepted exact decision, different-instance technical review, readiness validation and one RD writer govern the public candidate. Independent source/privacy QA applies to H; distinct postmerge release QA applies to M. Required configured checks pass; absent CI/approval rules are absent, not passed.
- AC-6: The new public source projection/history/documents/assets exclude private machine paths, local identities, raw logs and unshipped references. Both homepages agree on capabilities/limits and observed latest-published status; completion facts change only in later E.
- AC-7: Clean actual merged source M has actual CPython 3.9 evidence, distinct independent release QA, two byte-identical prerelease builds from distinct clean M checkouts and successful target validate-release. Earlier receipts keep their identities; private gates remain outside source.
- AC-8: A normal draft PR receives independent exact-head H review and required check/protection assessment, is marked ready and merged with expected H through server enforcement without bypass/direct-main source push. M and tree are read back as the release source.
- AC-9: The exact schema-7 intent and existing authorization are bound to the merged source, frozen notes, annotated identity and current remote snapshot; six non-destructive operations produce a non-draft 0.12.0 Pre-release with exactly five identity-verified assets and truthful immutable metadata.
- AC-10: All five public artifacts are freshly downloaded and hashed, nested distribution and downloaded-target validation pass, and the exact seventeen ADR0024 independent public smokes verify F1-F3 and predecessor/same-version maintenance compatibility before publication is claimed complete.
- AC-11: A separate exact schema-5 closeout intent permits only ordered [20,22,23] with ADR0024 evidence mapping and separate authorization, with comment identity read-back before close and closed-state read-back afterward; other open issues retain their disposition.
- AC-12: The authorized development project preserves existing local work and uses the real public validated target for official plan/upgrade/doctor. Inspect official planner behavior for existing paths absent from the old manifest; never delete/move unknown data or edit installation state to force success. The source task stops after upgraded health with no active transaction; activation/adaptation/final reliability checks belong to a real successor task.

## Ownership and verification

The workflow orchestrator owns classification, gate, remote authorization and operation reconciliation. A read-only Tech Lead authors the exact contract; a different instance reviews the persisted decision. One RD owns shared implementation. Independent QA owns each unchanged final candidate's complete default verification once, with explicit reasons for any new-candidate or distinct postmerge/publication gate. An independent privacy reviewer audits the public projection before push.

The public release acceptance graph must distinguish source checks, remote publication, public verification, closeout and project upgrade. A source-only pass cannot close the whole outcome. Private evidence remains outside the release source tree; only bounded public facts and hashes may be committed. Recovery before publication is a reversible local candidate correction/rebuild; after writes reconcile the same intent and natural keys without destructive mutation. Uncertain writes require read-back before retry; denial, divergence or still-unknown state stops the affected operation.

Publication acceptance is exactly AC-1 through AC-10. AC-11 closeout and AC-12 project upgrade are later independent stages of the authorized overall outcome and never prerequisites of publication or closeout-parent validation. H/M/E and the exact closed profiles/smokes are defined by ADR0024.
