# Vibe Kit 0.13 publication implementation plan

- Status: Approved plan; execution requires the applicable stage gate
- Owner: vibe_tech_lead decision author
- Governing decision: docs/decisions/0026-v0-13-publication.md
- Gate: docs/work-items/20261029-v0-13-publication/brief.md#technical-decision-readiness

## Stage 0: decision and authoritative evidence

1. Review this exact four-document packet with a different read-only Tech Lead. The author does not approve the proposal.
2. Re-review the now-materialized public projections of ADR0025 and the historical local-delivery scope, brief and technical-review, together with the byte-unchanged N01–N36 matrix. R1 supplies these dependencies; R2 clarifies historical acceptance and durable host requirements. Preserve original local-only scope and feature semantics, retain original identities separately, and approve the exact revised bytes rather than inferring approval from the historical Accepted header.
3. Resolve review findings, record Accepted governing decisions and approved independent review, then let the orchestrator confirm readiness and run ./bin/vibe validate-readiness . --brief docs/work-items/20261029-v0-13-publication/brief.md --format json. Nonzero blocks all implementation.
4. Evidence authoring is permitted while blocked. At this stage do not edit implementation, version/protocol mirrors, README, Plugin, tests or old candidate/fixture files. Review onboarding/context against the public baseline and refresh only evidence-backed project facts when that work is properly owned; never treat context as proof of activation.

## Stage 1: one writer, one final public candidate

After release, one RD writer works only in the new publication source checkout. Preserve the earlier frozen source, stopped fixtures and receipts. Re-read public main; preserve observed baseline ancestry and explicitly resolve any drift before public projection.

Project only the accepted feature implementation allowlist onto that public baseline, not private commits or history. Check every projected file's ownership and public suitability. Import the applicable sanitized feature documentation with resolved public references. Do not copy private logs, fixtures, installation state, task data or historical publication drafts.

Implement the exact schema-8 profile and required current mirrors. Complete public document projection and both homepages' capability/default/limitation/version review before final identity freeze. Use observed 0.12 as the existing published Pre-release and 0.13 as the candidate until actual 0.13 completion. Notes must list exact assets and describe capabilities without predicting publication, issue closure or measured live compliance.

Minimal implementation surfaces:

| Path or surface | Required change |
|---|---|
| bin/vibe | Add PUBLICATION_PROFILES[8]; current publication constants 8/8 with closeout 5; extend publication-only dispatch, exact-int guards, authorization binding, precise asset/natural-key checks, gate/comparison-build paths and receipt validation. |
| .vibe/core/protocol.json and agent-install.json#publication | Current 8/8/5 mirrors; preserve accepted 0.13 Agent-install schema/protocol 4/5 and core/Codex 7/7. |
| AGENT_INSTALL.md and .agents/skills/vibe-release/SKILL.md | Current exact 0.13 workflow, ten ACs, twenty smokes, issue policy none, H/M/E and identity/activation boundaries; retain historical contracts. |
| Identity mirrors and Plugin manifest | Recompute canonical activation v2 and payload identities after the last relevant edit; update only dependent mirrors. Generate installation manifests through production disposable installs, never edit source installation state to manufacture health. |
| tests/test_v130_publication.py and affected historical/current tests | Exact new profile plus historical isolation, dispatch/negative/recovery/persistence cases; update current-mirror expectations while preserving historical objects and verdicts. |
| docs/releases/0.13.0.md, README.md, README.zh-CN.md, CHANGELOG.md and necessary indexes/context | Public, truthful and mutually consistent prepublication content, exact asset names and resolving accepted references. |

Do not add an external framework, automatic task creator, new host protocol, general reconciliation engine or new issue-closeout profile. Existing accepted feature code is projected, not redesigned.

## Stage 2: focused development checks and freeze H

RD runs focused publication, release-identity/distribution and directly affected feature regressions. Include exact schema type/cross-profile rejection; five distinct sorted assets; six operations/child ledgers; authorization digest/source binding; distinct clean-build identities; zero-write main read-match; unknown/denied/divergence behavior; optional create-only result output; schema-8 closeout rejection; unchanged historical publication 1–7/closeout 1–5; protocol and activation/payload/Plugin consistency; actual installed entrypoints.

Audit the explicit schema-conditioned branches in publication validators and dispatch. Avoid broad refactors that reinterpret old objects. Current-mirror assertions in historical test files may move to 8/8/5; old profile identities, accepted/rejected inputs and closeout mappings stay fixed.

Regenerate final identity mirrors after all managed/payload edits, including notes and README. Independently review the final public projection and diff. Commit the final local prospective PR head H only after that projection/privacy review; the commit itself is not an acceptance claim. Keep subsequent runtime outputs outside the tracked source. Freeze H/tree, CLI, payload and activation hashes and exact notes. Any further candidate-defining change gets a new identity and invalidates affected evidence.

## Stage 3: new final-target fixtures and local acceptance

The bounded [N13/N28 acceptance-execution plan](acceptance-execution-plan.md) is an additional Proposed case plan, not an approved procedure. A distinct reviewer must approve its exact cases and then the applicable harness bytes, target/input bindings, paths and finite operation counts before execution. N13 and N28 retain their original acceptance strength; this reference neither imports implementation nor starts any scenario. The plan remains separate from the source and fixture full-default budgets below.

Create independent project-local Python and Node fixture roots from authenticated predecessor assets; install the actual frozen H target through the official safe plan/upgrade/doctor sequence. Bind source and installed identities, ownership, transaction result and the source-task STOP before any successor operation. Do not alter the older B2 fixtures.

The host creates or identifies each genuine successor at its exact fixture root and reads back actual task/root/terminal state. An uncertain creation is reconciled before any retry or activation gate. If the host supports only a manual task path, require the genuine manual receipt; tool availability, a proposed task or a child sharing another root is not evidence. Open only the exact task's gate after proving the prior prompt did not already release it. Keep the host-specific mechanism and all task/receipt/custody data out of public documents.

The successor independently reads the target rules and recomputes actual manifest/activation identities. Only host-authenticated activation plus structural validation may release applicable onboarding or bounded maintenance. No active transaction, unknown installation or unresolved readiness may be bypassed. Use one maintenance writer and independent technical review as required by the feature contract; preserve guard strength, assertions, budgets and file ownership. Do not run a full default merely to manufacture a known compatibility failure.

Independent QA executes applicable final fixture checks and each fixture's candidate-bound complete default once; one real run may satisfy maintenance and takeover when all conditions are satisfied. Reconcile a disconnected original QA run through read-only evidence before considering another run. Complete all N01–N36 on the actual final target, with static/CLI/live evidence separately labelled. Missing genuine host capability remains Blocked.

Independent QA also owns the one complete source default for unchanged H. Use its actual identity and result; the earlier feature candidate's full QA is not relabelled or repeated. A changed source or failed/invalid evidence requires an explicit reason for a new run. Do not push while required local product acceptance, source privacy/review or H QA remains blocked.

## Stage 4: PR, M and distinct release gate

Push only the accepted public branch; create and attach a normal draft PR. Review the exact H and actual checks/protections. Satisfy required independent approvals without self-approval or bypass. Re-read head and merge conditions, mark ready and merge through the governed expected-head path.

Read back the server-created M/tree. Confirm approved source, public ancestry and payload/activation equality or explain any differences. Earlier receipts retain their actual identities. Review continued applicability of unchanged feature/host evidence explicitly; changed relevant runtime bytes require affected acceptance and genuine activation. Unexplained drift blocks.

Record the specialized postmerge gate reason, then independent QA executes one canonical complete ./bin/vibe verify . --format json on unchanged M using actual CPython 3.9. That run supplies truthful QA/configured/Python views; no duplicate full run to fill another view. RD does not own this gate. Require all configured checks passing with no skipped or limited environment.

Build twice from distinct clean M checkouts and output locations with actual CPython 3.9. Require identical five assets, clean source identity and target validate-release for both. Freeze source/notes/annotated tag and assemble the existing acyclic gate bundle. Keep all gate receipts outside the tracked source.

## Stage 5: exact publication and public verification

Re-read complete main/tag/Release/assets and hash any existing assets. Require exact compatible state; extra/duplicate/divergent or unhashable state blocks. Main already at M is read-matched with no write.

Construct publication-plan with both candidates and the actual release-gate bundle. Bind the existing scope authorization to the exact intent with its real binding time. Publish only the six-operation graph with per-natural-key precondition checks and after-response read-backs. Unknown outcomes are read back first; only positively absent eligible operations may receive their bounded second write. Denial, execution failure, divergence or unknown state stops; no destructive correction.

Freshly download all five public assets, hash them, validate nested distribution/checksums and downloaded-target validate-release, then execute the exact twenty public smokes in feature-contract.md. Actual public 0.12 predecessor assets are required; do not re-release history. Run validate-publication on CPython 3.9, then obtain the independent postpublication acceptance for all ten ACs.

Only confirmed-complete remote state, passed public validation and independent acceptance permit the completion claim. Update truthful homepage/context facts through later E and read back the governed result, leaving M/tag/body/assets fixed. No issue comment or close is scheduled or performed.

## Required independent review points and stop conditions

The reviewer must explicitly assess: whether this extends rather than reinterprets historical profiles; whether the twenty smokes cover shipped new executable entries; whether N01–N36 remains a prerequisite; whether public source/host privacy projection is complete; whether H/M/E and build identities are acyclic and actual; whether new target activation is genuine; whether old STOP/unknown operations are preserved; whether QA reuse is honest; and whether authorization/retry rules remain bounded.

Materialized feature artifacts with unresolved exact-byte review, Proposed decisions, unapproved review or failed readiness block implementation. The N13/N28 appendix remains execution-blocked until its separate required approval and applicable gates are satisfied. Missing live evidence blocks acceptance. Missing actual PR approval/protection compliance blocks merge. Main/tag/asset divergence blocks publication. Published but unverified remains incomplete. Report exact action, target, reason, completed scope and whether denied, pending or uncertain; do not turn an internal missing fact into a fabricated pass.
