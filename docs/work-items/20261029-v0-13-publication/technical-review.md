# Vibe Kit 0.13 publication technical review

- Date: 2026-10-29
- Role: distinct independent vibe_tech_lead reviewer; implementation read-only
- Review mode: independent-agent
- Verdict: changes-required
- Implementation gate: blocked; this review does not confirm readiness
- Observed source baseline: e676446c661e717578b4dd114548cdfecb2b2437
- Review scope: exact persisted publication proposal and its applicable governing evidence; no product execution or remote publication assessment
- Transport limitation: transport context bounding unavailable; no prompt-isolation or efficiency claim

## Exact reviewed inputs

| Repository-relative artifact | SHA-256 |
|---|---|
| docs/decisions/0026-v0-13-publication.md | b7f3d24c02571784cf1914403fc55af1a106681fc8a6c153b6cf28f3ce789325 |
| docs/work-items/20261029-v0-13-publication/brief.md | 54b2634afb003cb99ea5e68bdd3e7b4eebc0e57f4588609cfe91d5a2cccaf6af |
| docs/work-items/20261029-v0-13-publication/feature-contract.md | a513c296992fdb5b6bb347c1d310b48e58863eed2d52bcf8fa44d31cb0f185a4 |
| docs/work-items/20261029-v0-13-publication/implementation-plan.md | cbfcfd0c872128c1debd57650b954dc6d960f7adf23ce8181aa19a6e2252db19 |
| docs/decisions/0025-upgrade-compatibility-and-maintenance-continuation.md | d4c93358dda898374908f1f1e72bd948159d444b0b74f2b1f56ee10dba3ec22d |
| docs/work-items/20261029-v0-13-local-delivery/acceptance-matrix.md | f88f432e0c645f86f0a63e5f32a72f6e5806c0f770acaff4a60668b94f008487 |

The review also read current AGENTS.md, project configuration/rules, operating model, technical-decision readiness, onboarding state, relevant product/architecture context, the vibe-release Skill, ADR0024, and the existing profile/validator and v0.12 publication-test surfaces. Those source surfaces remain the public 0.12 baseline. The copied feature decision and matrix establish proposed dependencies, not implemented 0.13 behavior or current acceptance.

## Required revisions

### R1: Finish the required accepted feature-governance projection before the implementation gate

ADR0026 Context and scope, publication brief Product dependency and current coverage, and implementation-plan Stage 0 all require the accepted feature scope at docs/work-items/20261029-v0-13-local-delivery/scope.md. That file is absent. ADR0025 also points to the absent local-delivery brief.md, and the acceptance matrix ends with the same unresolved brief reference. The full accepted scope cannot be established from the four-module summary alone.

Materialize the minimal sanitized accepted scope and the historical brief/review evidence needed to support and resolve these references. Preserve all N01–N36 criteria, the four-module boundary, the thirteen deferred items, and the original local-only stage. A concise public projection may replace private or unshipped references with accurate public governing references; it must disclose that transformation and preserve the accepted semantics. Do not import application code, private execution reports, raw QA output or unrelated history merely to satisfy this pre-edit gate. Preserve the original historical sources separately.

Update the publication packet's dependency statements to reflect the actual reviewed public materialization. Supply the exact new hashes for independent readback. This is a required evidence dependency, not a request for a new product choice or another full QA run.

### R2: Make the projected governing decision's status and host claims truthful

ADR0025 has an Accepted header, but Alternatives and remaining gate still describes the artifact as Proposed and says its independent review and acceptance are unfinished. Verification and actual host evidence also contains task-specific historical capability and execution-plan statements. Those passages cannot serve as current public-candidate authority without qualification.

In the public projection only, reconcile the closing status with the actual historical acceptance/review evidence. Distinguish accepted feature semantics from implementation and live acceptance that remain unverified for the publication candidate. Replace historical execution-host assertions with the durable host-evidence requirement or clearly bounded historical facts. Keep the requirement for a genuine same-root successor and authenticated target-content activation; do not replace it with structural validity, tool availability or an Agent claim. Resolve necessary public links, retaining only publishable facts.

The original accepted feature decision and historical receipts must retain their original identities. Re-read the changed projected decision and supporting scope/brief/review before approval; its current hash is not approval of future edited bytes.

## Technical assessment of the reviewed proposal

No architectural redesign is requested for the four exact proposal hashes above. Subject to R1/R2 and final exact-byte review:

- The implementation is a bounded extension of the existing offline profile machinery: exclusive schema 8, profile vibe-kit-v0.13.0-prerelease, five exact sorted assets, six operations, and inherited natural-key/ledger/persistence contracts. It adds no generalized release engine or network authority.
- Publication schemas 1–7 and closeout schemas 1–5 retain exact historical meanings. Current mirrors 8/8/5, issue policy none, null issue_closeout and schema-8 closeout rejection are coherent. Agent-install protocol 5 and the accepted 0.13 versions remain intact.
- The twenty smokes correctly add the v0.12 predecessor and two new executable-entry groups to the prior substantive set. The template and compatibility groups require real Python/Node dispatch and production validators. F3/F4 remain subject to the complete product matrix and genuine host evidence; public package checks cannot substitute for those requirements.
- Accepted feature implementation is projected by one writer only after readiness. Publication changes and public document projection precede the final payload/activation freeze and fresh final-target fixtures. Earlier source/fixture receipts remain historical; their STOP and unknown-operation boundaries are preserved.
- Local H acceptance and privacy review precede public push. A normal draft PR, independent exact-head review, actual checks/protections and expected-head merge govern public source changes. No self-approval substitute, direct-main source push or protection bypass is permitted.
- M is the actual server merge identity. Receipt identities are not relabelled even when trees agree. Explicit applicability assessment can reuse unchanged evidence; changed relevant target bytes require affected acceptance and real activation. E is a later governed publication-fact change, never a replacement release source.
- One independent complete default on unchanged H and one distinct postmerge release default on M have different applicable gates. The actual CPython 3.9 M run may support multiple truthful receipt views. Two clean M builds are separate evidence. There is no reason to rerun an unchanged superseded feature candidate or execute extra full matrices to populate receipts.
- The M-to-gate-to-intent-to-authorization-to-remote-receipt-to-validation-to-independent-acceptance sequence is acyclic. Existing consent is bound when the exact intent exists; binding time does not invent a later approval. Full remote snapshots, public downloads, nested validation and all twenty actual smokes remain future required evidence.
- Retry handling is bounded: read back every response; unknown is not absence; only an eligible positively absent natural key with its unchanged precondition permits a second write. Denial, definite failure, conflict or unresolved uncertainty stops. No destructive correction or automatic recovery guarantee is introduced.

## Final review and gate closure

The current Proposed artifacts and blocked brief are not approved for implementation. After R1/R2 are resolved, the author supplies the exact revised packet and dependency hashes. This distinct reviewer must read those persisted bytes and record an approved or changes-required result. Mere status substitution is insufficient while required governing evidence is absent.

Once substantive review succeeds, permitted administrative transitions are ADR0026 Proposed to Accepted; corresponding contract/plan acceptance status; brief outcome decision-required to decision-accepted; and truthful review-evidence/dependency fields. These changes must be read back and their actual final hashes recorded. No future Accepted hash is inferred here.

Only the workflow orchestrator may then record approved review, resolve the actual blockers, confirm implementation-ready with time/basis, and run the required validate-readiness command. A nonzero result blocks release. The final gate/readiness edits require exact readback before RD is released; any scope or technical change reopens review. The reviewer does not own gate confirmation.

The separately announced N13/N28 acceptance-execution plan was not a persisted input to this review and is not approved here. Its exact bytes require a separate bounded review before execution. It must not reduce the ten publication criteria, thirty-six product criteria or twenty smokes.

## Checks, limitations and remaining state

Performed: read-only document/source inspection, exact SHA-256 comparisons, and checks for the missing scope/brief and initially absent review record. No application, profile, protocol, README, fixture, installation-state or existing evidence edits were performed.

Not run: validate-readiness, source/default QA, product scenarios, builds, real activation, remote downloads, PR operations or publication. They are outside this review assignment and their actual prerequisite gates remain unmet. Onboarding/context retain historical latest-published claims; the assigned projection owner must refresh only verified public facts before the final candidate freeze. Metadata reported by the orchestrator was not independently re-fetched and is not asset verification.

Remaining action: document author completes R1/R2 and returns exact hashes; this reviewer performs final readback; orchestrator alone owns readiness release. The action is pending, not denied and not executed by this review. Implementation and publication remain blocked.


## Revision 2: governance closure and N13/N28 plan review

- Date: 2026-10-29
- Role/mode: distinct independent vibe_tech_lead / independent-agent
- Previous review record SHA-256: f0abe366170fca60496c92bbc33e041d7d557f43247923dc906d2cad6e40841f
- Verdict: changes-required; R1 and R2 resolved; one narrow R3 sequencing clarification remains
- Gate: blocked; no implementation or case execution released by this review

### Exact revision-2 inputs

| Repository-relative artifact | SHA-256 |
|---|---|
| docs/decisions/0026-v0-13-publication.md | 0e277b7f5bdbf13a2c780ad1c192bf2fd82ff233e10315445d1ff723b5f7df7b |
| docs/work-items/20261029-v0-13-publication/brief.md | 0c99e3228f031015a6d5ae32a6aee8af778e511550510c14c71ebee4c29301aa |
| docs/work-items/20261029-v0-13-publication/feature-contract.md | a513c296992fdb5b6bb347c1d310b48e58863eed2d52bcf8fa44d31cb0f185a4 |
| docs/work-items/20261029-v0-13-publication/implementation-plan.md | 910ce9ff2a7709c192d9ac9d3ceda0d6983f8b90944fdf413a5e29d4db28247d |
| docs/work-items/20261029-v0-13-publication/acceptance-execution-plan.md | 7819f383bc468eccd7b22c55d4158411ea8f04e09c689a2481c972ec0798a6dc |
| docs/decisions/0025-upgrade-compatibility-and-maintenance-continuation.md | 6b6b47d05156e89626c4c5c27fa2695c03872ea7dbb5375e06973cbff595bbf8 |
| docs/work-items/20261029-v0-13-local-delivery/scope.md | 14f0f85ede17e7e2a42f5129d1712aec35f19c53431cc0c3cd2015f0c5a19a71 |
| docs/work-items/20261029-v0-13-local-delivery/brief.md | d78de493edb1257102de5a0e3b4da780659c6b8cd4998f8bb62bf53d4a362aae |
| docs/work-items/20261029-v0-13-local-delivery/technical-review.md | 5a1736bf25f630a98a98bd74c24c158d127c570588983be7623346ea0bbf83c7 |
| docs/work-items/20261029-v0-13-local-delivery/acceptance-matrix.md | f88f432e0c645f86f0a63e5f32a72f6e5806c0f770acaff4a60668b94f008487 |

### R1 and R2 resolution

The required scope, historical brief and historical review now exist. The scope's product body after its opening projection section is byte-identical to the original; the complete matrix remains byte-identical. The new public Markdown references resolve. The historical brief and review retain their actual local-only authorization, original identities, initial findings and later technical approval, without treating historical implementation readiness as current candidate authority.

The historical Accepted ADR0025 has SHA-256 d4c93358dda898374908f1f1e72bd948159d444b0b74f2b1f56ee10dba3ec22d. Replacing only its Accepted status with Proposed recomputes the historical approved revision 93ea22d082e0422406ad6c474bcff18483c910b5127d2d0dcb823088c78a4fdd. The original scope/brief/review hashes match the public projection's cited provenance. The public ADR's bounded changes clarify that history, remove task-specific host-capability assertions, require actual same-root target-content activation, and correct its contradictory closing status. They preserve the accepted feature semantics. R1/R2 are resolved for the exact public bytes in this table.

The publication packet correctly keeps new implementation and acceptance unverified. The closed profile and previously assessed technical boundaries remain coherent. No feature redesign, premature source import, historical full-QA repeat or additional product decision is requested.

### N13/N28 substantive assessment

The appendix is within N13/N28 and does not change the 36 product criteria, ten publication criteria or twenty smokes. N13's two in-memory incomplete-evidence packets supplement only its missing-information group. They preserve original records, separate identity findings from semantic conclusions, require actual neutral Agent responses and independent QA, and add no default QA run. The identity-only and demonstrated-contract-change groups remain separately required.

N28's six owned shadows per language produce the seven required states using real A installs and production transactions. Five upgrades and five recoveries per language, zero shadow defaults and zero shadow successors are finite and consistent with the case list. Main-project negative and golden candidates retain distinct existing budgets. A production negative probe is separately authorized controlled test execution; it is not a maintenance Agent's permission to repair an unknown state.

Read-only source inspection confirms the proposed boundaries exist in the current public baseline: mutate_leaf_forward is inside the transaction loop; ordinary filesystem failure invokes production rollback; KeyboardInterrupt is outside the transaction's ordinary exception catch; the durable commit precedes commit-complete and cleanup; remove_transaction_control_project is called after rollback-complete; recover_upgrade checks invalid/absent state and target divergence before its normal recovery paths. These observations support the bounded design, not a claim that the future frozen target or unimplemented harness already passed.

The plan requires capture at the real fault and before cleanup, preserves production-generated journals and raw bytes, records genuinely absent data, keeps evidence copies separate from originals, and leaves unsupported or incomplete capture blocked. No fabricated journal, recovery implementation, host receipt, crash or denial claim is introduced. An injected Python exception remains a controlled test fault. Real main-target activation and the applicable maintenance gate remain prerequisites for N28; shadows cannot supply them.

The final harness still needs exact independent review of its actual dispatcher wiring, second-mutation prerequisite, one-shot injection restoration, capture-before-cleanup and capture-failure stop behavior, typed/no-follow snapshots, explicit resource bounds, counter semantics, owned paths and actual candidate bindings. This plan review does not approve unseen harness bytes, guarantee the expected runtime result or waive any execution prerequisite.

### R3: Separate preparation readiness from case-execution prerequisites

In acceptance-execution-plan.md, Orchestrator approval points and remaining gaps begins: "Before implementation or execution, the orchestrator must:". Its checklist requires exact harness bytes, final T_H identities and genuine target activation. Taken literally for implementation, this requires products of source/harness preparation before the preparation can start. It conflicts with the publication plan's source implementation, final freeze and later fixture sequence.

Clarify two stages without changing any technical safety condition: approval of the finite case design plus the publication implementation-readiness gate permits the named writer to prepare the accepted source and private harness; actual case execution remains blocked until the exact final harness, inputs, target identities, path/count bounds and applicable source-diagnostic or genuinely activated maintenance gate are independently reviewed and confirmed. The exact harness must be inspected after it exists and before it runs. Remove the ambiguous blanket application of the execution checklist to all implementation. Keep all case counts, no-write observations, activation, QA ownership and stop conditions intact.

This is the only new requested revision. It does not authorize execution, remove the pre-edit source gate or change the user-visible scope. Return the revised appendix hash for bounded readback. No harness or scenario was run to discover or resolve this wording issue.

### Revision-2 checks and remaining state

Performed read-only hash/provenance comparisons, scope/decision diffs, relative-link checks and inspection of the named production/test boundaries. Current AGENTS, project rules, operating model, readiness contract, release Skill, bin/vibe and the inspected tests still equal the public baseline. No code or runtime state changed.

R3 resolution and the final Accepted/status/gate-byte review remain pending. Publication and product acceptance remain unverified. No readiness validator, default QA, installation, recovery, real Agent case, remote operation or publication was executed by this reviewer. The only write is this appended review record; the initial record is preserved in full.


## Final review

- Date: 2026-10-30
- Role/mode: distinct independent vibe_tech_lead / independent-agent
- Review scope: final proposal semantics, R3 sequencing and the unchanged literal human-review requirement
- Previous complete review record SHA-256: ff81d289f2d2d4c82f55ca8a5abb8bbbd0160b8ba8cd2b782354045a95d46333
- Verdict: approved for the exact technical design below; no unresolved technical finding blocks subsequent source/profile preparation
- Implementation gate: not confirmed by this reviewer; Accepted/status readback, orchestrator confirmation and actual valid readiness remain required
- Execution, acceptance, merge and publication: not released by this review

This section is the current technical verdict. The initial review and Revision 2 remain intact as historical records of their exact inputs and findings. It neither overwrites those verdicts nor claims that later execution has occurred.

### Exact approved design inputs

| Repository-relative artifact | SHA-256 |
|---|---|
| docs/decisions/0026-v0-13-publication.md | 0e277b7f5bdbf13a2c780ad1c192bf2fd82ff233e10315445d1ff723b5f7df7b |
| docs/work-items/20261029-v0-13-publication/brief.md | 0c99e3228f031015a6d5ae32a6aee8af778e511550510c14c71ebee4c29301aa |
| docs/work-items/20261029-v0-13-publication/feature-contract.md | a513c296992fdb5b6bb347c1d310b48e58863eed2d52bcf8fa44d31cb0f185a4 |
| docs/work-items/20261029-v0-13-publication/implementation-plan.md | 910ce9ff2a7709c192d9ac9d3ceda0d6983f8b90944fdf413a5e29d4db28247d |
| docs/work-items/20261029-v0-13-publication/acceptance-execution-plan.md | c2a763034e98e79c877a59fdbd2de9df6b930292f1677956b6cd00d96c2fc959 |
| docs/decisions/0025-upgrade-compatibility-and-maintenance-continuation.md | 6b6b47d05156e89626c4c5c27fa2695c03872ea7dbb5375e06973cbff595bbf8 |
| docs/work-items/20261029-v0-13-local-delivery/scope.md | 14f0f85ede17e7e2a42f5129d1712aec35f19c53431cc0c3cd2015f0c5a19a71 |
| docs/work-items/20261029-v0-13-local-delivery/brief.md | d78de493edb1257102de5a0e3b4da780659c6b8cd4998f8bb62bf53d4a362aae |
| docs/work-items/20261029-v0-13-local-delivery/technical-review.md | 5a1736bf25f630a98a98bd74c24c158d127c570588983be7623346ea0bbf83c7 |
| docs/work-items/20261029-v0-13-local-delivery/acceptance-matrix.md | f88f432e0c645f86f0a63e5f32a72f6e5806c0f770acaff4a60668b94f008487 |

### Findings resolved without weakening later gates

R1 and R2 remain resolved for the unchanged projected governance bytes recorded in Revision 2 and confirmed above. Their historical acceptance and local-only scope are not current implementation or acceptance evidence for this publication candidate.

R3 is resolved for the exact acceptance-execution-plan.md hash above. Its Roles, review and execution gates and Orchestrator approval points now distinguish source/harness preparation from actual acceptance-case execution. Independent design approval plus applicable source readiness may release one named RD to prepare the accepted source/profile and private harness. Final T_H identities, exact prepared harness review and genuine corresponding main-fixture activation are later outputs and execution prerequisites; they no longer form a circular prerequisite for preparing those artifacts. N13 retains its authorized pre-apply read-only diagnostic path. N28 still requires actual corresponding final-target activation and the applicable maintenance gate. The finite cases, raw-capture rules, five-upgrade/five-recovery limits, zero shadow defaults and established main-candidate verification budgets are preserved.

The previously considered R4 wording change is withdrawn as unnecessary. ADR0026 remains unchanged and expressly requires "an explicit human review under the existing evidence rules" for H-to-M evidence applicability. This approval accepts that literal requirement. Human means an actual human reviewer; an Agent decision, structural validation, equality calculation or this technical review does not satisfy it. At the actual H-to-M gate, missing required human review keeps applicability blocked. Equality never changes receipt identities, authenticates a host or activates another target; changed relevant bytes still require affected acceptance and genuine activation.

The required human PR review and actual-PR approval also remain separate. They must concern the actual PR and applicable current head, with the required independence, real checks and protection compliance. General permission to publish, this design approval and a future readiness result cannot substitute for that approval. No self-approval, protection bypass or implied approval from absent rules is permitted.

No new architecture or scope change is needed to honor these later human gates while preparing the accepted local source/profile. Their future evidence is not claimed present. This conclusion does not enact the withdrawn wording change through interpretation.

### Bounded preparation and retained acceptance obligations

The previously reviewed closed schema-8 profile, five assets, six operations, twenty public smokes, issue policy none and historical schema preservation remain approved as design. There is no new recovery engine, host-authentication mechanism, source-history import or issue-closeout path.

After lawful source-readiness closure, one RD may project the accepted feature implementation and prepare the publication profile, public documents and private harness within the approved ownership boundary. This is preparation of a new candidate. Neither historical B2 results nor copied governance establish its implementation, activation or acceptance.

Before any final-target case runs, independently review the actual harness bytes, final target and predecessor bindings, inputs, owned paths, capture bounds, counters and applicable execution authority. Require real post-operation evidence and actual Agent judgments; installation health or restored bytes alone do not establish host readiness. Preserve the complete N01–N36 criteria, ten publication criteria and twenty smokes.

H and M have not been established by this review. Required final-target local acceptance, privacy review and independent H QA precede public push. The actual PR/head review and merge requirements precede M. The literal human applicability review, applicable final-target evidence, distinct independent M default, two clean builds and remaining prepublication gates precede publication. Actual remote readbacks, public downloads, smokes and independent acceptance precede a published-and-verified claim. Missing evidence at any applicable stage remains blocked.

### Permitted administrative closure and mandatory readback

The responsible decision author and workflow orchestrator may now make only the truthful administrative transitions corresponding to this approved design: ADR0026 Proposed to Accepted; current proposal/case-design status and review labels to accepted or approved; the brief's decision-required outcome to decision-accepted; and current review/dependency references to this final review. Historical status quotations and original identities remain historical. The human-review sentence and all substantive contracts remain unchanged.

The brief may record these technical findings as resolved while retaining unfulfilled case-execution, human, acceptance and publication obligations at their proper later gates. Source preparation must not be represented as case execution or final acceptance. Any substantive change beyond the approved design requires another independent review.

Only the workflow orchestrator owns the implementation gate, its truthful confirmation time and basis, and the actual validate-readiness invocation for this publication brief. This reviewer does not set implementation-ready. Before releasing RD, read back the exact final Accepted/status/gate bytes, record their real hashes, independently confirm that only the permitted administrative changes occurred, and inspect the actual successful readiness result. No future Accepted hash or readiness success is inferred here.

### Verification performed and limits

Performed: read-only examination of the exact current decision, brief, implementation sequence and review history; R3 gate readback; literal human/PR obligation review; and SHA-256 confirmation of all approved inputs above. The earlier substantive assessments remain applicable to those unchanged bytes.

Not performed: source/profile implementation, case/harness execution, readiness validation, full QA, installation, activation, builds, remote operations, PR approval or publication. This append is the only change made by the reviewer in this step. All earlier review bytes are preserved.
