# Verification: Architecture decision readiness gate

- Verified: 2026-08-27
- QA perspective: independent `vibe_qa`
- Evaluated state: shared uncommitted working tree based on `064aefd`, including the separately Accepted `0.5.0` / core protocol 3 Agent-first adoption work
- Conclusion: **Pass for the current Codex adapter contract and controlled Codex routing scenarios; no readiness-specific defect found.** Non-Codex and real sequential-host execution remain unverified and are not inferred from static artifacts.

## Readiness and accepted-boundary audit

- The work item is L and records all fields required by `.vibe/core/technical-decision-readiness.md`: `decision-accepted`, Accepted ADR 0008, `independent-agent` review approved with concrete evidence, no material product decision, no blockers, an explicit `implementation-ready` gate, gate-owner perspective, ISO-8601 confirmation time, confirmation basis, and state history.
- [ADR 0008](../../decisions/0008-technical-decision-readiness-gate.md) is `Status: Accepted` and fixes the implementation boundary: one normative core contract, project-owned Markdown readiness state, read-only Tech Lead author/reviewer passes, orchestrator confirmation, one post-gate RD writer, Codex adapter/core protocol 3, and no CLI-owned workflow state machine or file-write lock.
- A distinct Tech Lead reviewer approved the exact persisted ADR before the gate record was released; the implementation writer was a separate agent. No evidence showed QA being used to create or waive readiness evidence.
- The accepted boundary reuses the separately Accepted, unpublished `0.5.0` / protocol 3 decision from ADR 0007. QA did not treat concurrent Agent-first adoption files as readiness regressions or authorize publication.
- The persisted readiness history records the pre-implementation blocked, review-changes-required, Accepted, and gate-confirmed transitions. Because the implementation is an uncommitted shared working tree, Git cannot independently reconstruct the wall-clock order of every file edit; no contradictory or bypass evidence was observed.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | `.vibe/core/operating-model.md`, `.vibe/core/technical-decision-readiness.md`, `.codex/agents/vibe-pm.toml`, `.codex/agents/vibe-tech-lead.toml`, `.codex/agents/vibe-rd.toml`, and feature guidance consistently assign product contract to PM, durable technical choices to Tech Lead, and implementation inside the accepted boundary to RD. Repository-wide contradiction search found no instruction requiring PM to choose architecture or migration/recovery details. | Pass |
| AC-2 | The operating lifecycle now inserts Technical Decision Readiness before Plan/Implement. Feature, debug-to-fix, and direct implementation Skills reference the same core contract and stop application/shared code edits while blocked. `WorkflowContractTests.test_implementation_entry_points_apply_one_canonical_contract` passed. A fresh Codex RD dry-run also returned `decision-required + blocked` before implementation for the L permission/recovery case. | Pass |
| AC-3 | The core contract and operating model define lightweight S, trigger-scanned M, and explicit-outcome/reviewed L. L can cite an applicable Accepted ADR or reviewed no-new-decision rationale rather than manufacturing a new ADR. Controlled scenario reasoning allowed copy-only/local reversible S, required a concise confirmed record but no ADR/review for untriggered M, and reclassified a nominal S that introduced authentication. | Pass |
| AC-4 | `.vibe/core/technical-decision-readiness.md` lists durable/shared contract, cross-component/system, schema/protocol/version/API/compatibility, migration/irreversibility, auth/permissions/security/privacy/trust, rollback/recovery/crash/failure consistency, and material long-term trade-offs; it excludes local reversible choices. `test_static_trigger_vocabulary_covers_high_risk_boundaries` passed. | Pass |
| AC-5 | `.vibe/core/templates/work-item-brief.md` initializes all 14 required fields as `not-assessed + blocked`; the current brief demonstrates `decision-accepted + implementation-ready` with governing decision, review, blockers, confirmation, and history. `test_work_item_template_initializes_all_fields_blocked` and the generated-work-item CLI scenario passed. | Pass |
| AC-6 | The core Roles and authority section plus PM/Tech Lead/RD/QA prompts define product owner, decision author, independent reviewer, orchestrator gate owner, writer stop/reopen behavior, and the material-product-choice boundary. Fresh dogfood reasoning correctly kept internal transaction/recovery choices with Tech Lead and did not ask the user. | Pass |
| AC-7 | The core and ADR require different native Tech Lead instances for author and reviewer, prevent the writer from being the sole author/reviewer/approver, and define a separately disclosed non-writing `sequential-perspective` fallback. The Tech Lead role is read-only and has mutually exclusive author/reviewer modes. Static role and host-semantics tests passed; actual non-Codex/sequential-host execution was not available and is recorded below. | Pass |
| AC-8 | `.agents/skills/vibe-implementation-flow/SKILL.md` preflights size, risks, open decisions, architecture, governing decision, review, blockers, and confirmation even for a direct implementation request. In a fresh controlled Codex RD prompt with no ADR/architecture hint, the L permission-safe atomic-upgrade request was not authorized for edits and was routed to a read-only Tech Lead decision pass. This proves current Codex routing reasoning, not a mechanical file-write lock. | Pass |
| AC-9 | `.agents/skills/vibe-debug-flow/SKILL.md` says confirmed root cause alone does not release implementation. A fresh controlled Codex debug-to-fix prompt classified an M fix adding persistent recovery state and changing older-client interpretation as `decision-required + blocked`, routed Tech Lead author/reviewer before RD, and correctly returned the unspecified observable compatibility promise to product/user authority. | Pass |
| AC-10 | Fresh Codex RD dogfood prompt contained L size, permissions, multi-file atomicity, rollback/recovery, rollback failure, crashes, ownership, and compatibility, but no `ADR` or architecture-stage hint. It refused application/shared edits, produced `decision-required + blocked`, identified transaction/recovery/crash consistency as blocking, routed Tech Lead author then a distinct reviewer, and required no user decision for internal choices. The prompt was read-only, so this is controlled live routing evidence rather than write-enforcement evidence. | Pass |
| AC-11 | In a follow-up on the same dogfood scenario, the fresh RD received an Accepted decision covering transaction/recovery/crash/compatibility, approved distinct review, no material product decisions/blockers, and complete orchestrator confirmation. It returned `decision-accepted + implementation-ready`, handed off to one RD writer, did not ask PM/user to approve internal implementation details, and listed new durable/high-risk discoveries as reopen triggers. | Pass |
| AC-12 | Controlled Codex scenario reasoning allowed a copy-only S and a local reversible known-cause S fix without ADR/review; required an untriggered M to record `no-new-durable-decision` and explicit gate confirmation but no ADR/review; and stopped/reclassified a nominal S that introduced authentication. | Pass |
| AC-13 | The core contract invalidates prior confirmation, appends prior state/time/reason to history, and moves a newly discovered schema/compatibility/ownership/recovery/security choice to `decision-required + blocked`. Controlled Codex reasoning stopped the affected edit and required new Accepted decision, approved review, and fresh gate confirmation before resuming. | Pass |
| AC-14 | The core and ADR apply the gate to active M/L work before its next implementation handoff, pause in-progress work only for a newly discovered unresolved durable/high-risk boundary, and do not retrofit completed history. The shaped `permission-safe-atomic-upgrade` item remains pre-implementation; its next handoff must fail closed because its legacy brief lacks the new canonical readiness block. Templates/upgrades do not overwrite existing project-owned briefs. | Pass |
| AC-15 | This verification maps AC-2 through AC-14 to the no-hint dogfood block, accepted-decision release, direct implementation, debug-to-fix, S/M negative, reclassification, reopen, adoption, and sequential-host cases. Deterministic artifact/distribution results are separated from controlled Codex reasoning; unavailable non-Codex/sequential runtime evidence is explicit. | Pass |

## Automated checks

| Check | Result | Evidence |
|---|---|---|
| Focused workflow contract | Pass | `python3 -m unittest tests.test_workflow_contract -v` — 7/7 passed. These are deterministic artifact assertions and do not certify live Agent behavior. |
| Focused init/work-item and upgrade | Pass | `test_init_doctor_and_work_item` and `test_upgrade_updates_managed_files_and_preserves_project_files` passed. Generated M work item contained the complete blocked readiness block; upgrade preserved project-owned state. |
| Focused adopt/package/plan/conflict upgrade | Pass | Corrected invocation of `test_adopt_preserves_existing_project_and_detects_stack`, `test_release_package_is_reproducible_installable_and_tamper_evident`, `test_plan_is_read_only_for_init_adopt_upgrade_and_conflict`, and `test_upgrade_is_atomic_when_managed_file_conflicts` — 4/4 passed. Release/Plugin/fresh install included the readiness core and Tech Lead role, fresh doctor passed, and historical upgrade installed both files. |
| Initial focused selector | Corrected | Two valid selected tests passed; two mistyped, nonexistent test method names produced unittest loader errors. The exact existing test names were then discovered and the intended scenarios passed above. This was a QA command-selection error, not a product failure. |
| Full project verification | Pass | `./bin/vibe verify` — 29/29 tests passed in 21.755s. |
| Diff whitespace validation | Pass | `git diff --check` produced no output. |
| Source-checkout doctor | Environment limitation | `./bin/vibe doctor . --format json` returned 1/`broken`: installed `.vibe/version` and manifest remain `0.4.0`, while the shared unpublished source candidate is `0.5.0`; managed working files are therefore reported modified. Fresh 0.5.0 install and historical-upgrade doctor scenarios passed. QA did not mutate installation metadata. |

## Controlled Agent scenarios

| Scenario | Observed current Codex behavior | Boundary |
|---|---|---|
| Direct L permission/recovery request without decision hint | Refused edits; `decision-required + blocked`; Tech Lead author/reviewer handoff; no internal-choice user prompt. | Fresh `vibe_rd` reasoning pass; no attempted code write. |
| Same L request with Accepted ADR/review/confirmation | `decision-accepted + implementation-ready`; one RD writer may begin; reopen on new durable/high-risk choice. | Fresh follow-up reasoning using supplied complete evidence; no persisted permission-upgrade ADR was manufactured. |
| Debug-to-fix M with persistent recovery marker and old-client behavior | Root cause did not release code; `decision-required + blocked`; technical mechanics to Tech Lead, unspecified observable compatibility promise to user/product. | Fresh Codex reasoning pass; no implementation. |
| Copy S, local reversible fix, untriggered M, risky nominal S | Normal S cases proceed without ADR; untriggered M needs concise rationale/confirmation only; auth boundary reclassifies and gates. | Fresh `vibe_rd` scenario-matrix reasoning; not an end-to-end host run. |
| Reopen | Affected edit stops; prior confirmation is retained in history; new decision/review/confirmation required. | Fresh `vibe_rd` scenario-matrix reasoning plus deterministic contract text. |
| Sequential host | Separate author, non-writing critical review, gate confirmation, writer; capability limitation must be recorded and cannot be called independent-agent. | Contract and controlled reasoning only. No real sequential-only or non-Codex host was available. |

## Defects

No readiness-specific defect was found in the reviewed working tree.

The source-checkout doctor result is not classified as a readiness regression: it is the expected mismatch between the repository's installed 0.4.0 metadata and the concurrent, unpublished 0.5.0 development payload. It remains a release-state limitation until the owning workflow intentionally updates installation state.

## Limitations and residual risk

- The readiness gate is a prompt/role/evidence contract. Per Accepted ADR 0008, the CLI does not parse work-item readiness or mechanically prevent file writes. Compliance therefore depends on the Agent loading and following the distributed instructions.
- Controlled fresh Codex passes verified trigger classification, routing, release reasoning, false-positive boundaries, and reopening. They were explicitly read-only QA scenarios, so they do not prove that every future Agent will resist an attempted write under adversarial or stale instructions.
- A real host without native subagents was unavailable. The sequential fallback is verified statically and by current Codex reasoning only; identity-isolated review must not be claimed for that mode.
- No non-Codex adapter/runtime was exercised. Protocol 3 metadata is conformance declaration, not runtime proof.
- The shared working tree is uncommitted and also contains the accepted Agent-first 0.5.0/protocol 3 iteration. QA verified compatibility boundaries and did not evaluate that separate work item's full product acceptance.
