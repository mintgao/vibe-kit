# 0024: Publish exact v0.12.0 from a reviewed public PR and close completed issues separately

- Status: Accepted
- Date: 2026-10-28
- Decision owner: read-only vibe_tech_lead decision author
- Work item: docs/work-items/20261028-v0-12-publication/brief.md
- Public feature contract: docs/work-items/20261028-v0-12-publication/feature-contract.md
- Technical review: docs/work-items/20261028-v0-12-publication/technical-review.md; exact persisted inputs independently approved.

## Context and adopted feature boundary

Publish only F1/#20 exact onboarding integer validation, F2/#22 affected-entry focused evidence guidance, and F3/#23 bounded read-only historical verification inspection. Issues #21/#26 are assessed only; #24/#25 remain deferred. ADR0011 governs offline CLI and host publication ownership; ADR0017 configured verification; ADR0018 takeover and host-only custody; ADR0021 exact profiles and existing-authorization binding; ADR0022 private diagnostics, result persistence and separate publication/closeout acceptance.

Local feature acceptance is not evidence for the new public source identity. Project accepted files onto the public baseline, preserve private history separately, and perform fresh technical review, independent source QA and exact merged-source release QA. The sanitized ADR0023 and feature-contract.md retain accepted semantics while replacing unshipped/private references. Earlier local hashes, review identities and receipts are never relabelled as public-candidate evidence.

F1 accepts only exact integer 1 as onboarding schema version. Boolean, float, string, null, missing and unsupported versions retain existing invalid-state semantics without repair or rewriting. The shared predicate remains authoritative in real doctor and upgrade-plan preflight.

F2 connects the configured check, actual default entry, affected live helper/adapter, observed origin/arguments, focused execution and intentionally historical callers. Actual Python discovery and Node package-script execution establish wiring; static searches and direct helper tests alone do not. No general graph system, mandatory S ceremony or transfer of canonical full QA to RD is added.

F3 is inspect-run <target> --run-id <verify-id> [--final-receipt <path>] --format json. Preserve the complete command-specific result schema 2 / inspection schema 1 in feature-contract.md: metadata, complete receipt validity, binding, coverage, single selected artifact set and independent historical receipt/run verdicts remain distinct. Origin is not-attested, applicability unproven and liveness not-assessed. Inspected is never a current-candidate pass.

Preserve strict complete-receipt validation, component-wise pinned no-follow reads, input-only explicit receipt selection, explicit-copy original-slot non-read, independent receipt meaning when metadata is absent/mismatched, 1 MiB receipt cap, four logs, 64 MiB per log, 64 KiB hash buffer and 32 KiB result cap. Inspection starts no checks, probes, subprocess, Git or network and performs no repair, resume, signal, write or cache creation. Interrupted/unfinished/partial/mismatched run evidence remains non-passing. Consistent copied evidence cannot attest provenance; negative isolation uses genuinely different evidence.

This decision changes exact publication/closeout profiles, not accepted F1-F3, producer defaults, execution/verify schemas, upgrade transaction or activation protocol.

## Public projection and PR-first source identity

The public branch starts from observed public main. Project the accepted allowlist; never merge/cherry-pick unrelated private history. Preserve original commits and installed-state before-images. New public commits, notes, comments, assets and summaries exclude private machine paths, execution identities, environment values, raw logs, credentials, goal/custody and unshipped references. Select the public commit/tag identity deliberately.

H is the final independently reviewed PR head; M is the actual server-produced merged commit and tree read back after merge; E is a later publication-evidence/homepage-fact commit. Independent source QA/privacy review applies to H and cannot claim M has passed.

Push the sanitized branch, create a normal draft PR, review H, assess actual checks/protections, mark it ready and merge through the server-enforced path with expected head SHA. No admin bypass, force, protection changes or direct source push to main. Recheck head, rules, checks and mergeability immediately before governed mutations. Absent CI/approval rules are absent, not passed. Do not fabricate self-approval; retain independent exact-head review and satisfy actual server requirements.

The release source is M even if its tree equals H. Unexpected head, tree or main divergence blocks. After merge freeze clean M/tree, release-note bytes and managed identities. Gate evidence is private, outside the tracked source; do not change M while constructing its release.

Independent QA owns exactly one complete default verification of unchanged M as a distinct postmerge release gate; record the new-source reason before execution. H/earlier receipts keep their identities. Require actual CPython 3.9, all configured checks passing with no skips/environment limits, focused publication/feature checks, two clean prerelease builds from M in distinct checkouts/output locations, identical five-asset sets and explicit target validate-release for both.

One actual CPython 3.9 default execution may support QA/configured/Python receipt views truthfully. Canonical configured argv is exactly ./bin/vibe verify . --format json and must describe actual invocation. Do not repeat the full matrix to populate another view. Build manifests identify M, tree_state=clean, status=prerelease; build/checkout/output IDs are distinct. Changed source/managed/notes/build bytes invalidate affected gates. Corrected same-version/scope intents bind existing authorization without a new conversational approval.

## Version and compatibility

Kit/source/Plugin/Agent-install version is 0.12.0. Advance publication intent/receipt schemas to 7 and closeout profile to 5 only. Preserve core/Codex protocol 7, Hermes 1, Agent-install schema/protocol 4/4, CLI result 2, inspect inspection 1, takeover 2, execution 1, maintenance bridge/migration registry 2, release manifest 2, transaction journal/commit 1/1, installed manifest/onboarding 1 and feedback 2.

Preserve accepted bridge upper-bound 0.12.0 and exact current v0.5 target retargeting without changing predecessor eligibility/hashes; regenerate compiled digest/mirrors. After the last managed edit regenerate activation v2 using existing normalization. Content identity is not live activation. Never hand-edit installation manifest/version to manufacture health.

## Exact publication schema 7

The exclusive compiled profile is:
    schema: 7
    profile: vibe-kit-v0.12.0-prerelease
    repository: mintgao/vibe-kit
    version: 0.12.0
    tag: v0.12.0
    title: Vibe Kit v0.12.0
    body_path: docs/releases/0.12.0.md
    direct: vibe-kit-0.12.0.zip
    distribution: vibe-kit-distribution-0.12.0.zip
    plugin: vibe-kit-plugin-0.12.0.zip

Non-draft Pre-release, generated_notes=false, platform_immutability_required=false. Exact five assets sorted by UTF-8 name bytes:
    SHA256SUMS: checksum
    release-manifest.json: manifest
    vibe-kit-0.12.0.zip: direct
    vibe-kit-distribution-0.12.0.zip: distribution
    vibe-kit-plugin-0.12.0.zip: plugin

Inherit closed intent/receipt/observation/ledger/local-receipt field sets and result-persistence rules. Schema is exact integer 7; float/string/bool/unknown/cross-profile input fails closed. Publication receipt issue_closeout stays null.

Six ordered operations and natural keys:
    publish-0 fast-forward-main: mintgao/vibe-kit:main
    publish-1 create-or-confirm-annotated-tag: mintgao/vibe-kit:tag:v0.12.0
    publish-2 create-or-confirm-prerelease: mintgao/vibe-kit:release:v0.12.0
    publish-3 upload-or-confirm-five-assets: mintgao/vibe-kit:release:v0.12.0:assets
    publish-4 read-back-publication: mintgao/vibe-kit:publication:v0.12.0:read-back
    publish-5 download-and-verify-public-assets: mintgao/vibe-kit:release:v0.12.0:public-assets

asset-0 through asset-4 follow asset order, with natural keys mintgao/vibe-kit:release:v0.12.0:asset:<exact-name>. Preserve snapshot-bound precondition hashes, child ledgers, exact read-back and max two writes; read-only operations have zero attempts.

After PR merge main ordinarily already equals M. Freeze that snapshot and use read-matched main with no write. If main no longer equals frozen M, stop without moving it backward or substituting another source.

Issue policy is exactly mode=after-public-verification, issues=[20,22,23], allowed_operations=[create-exact-evidence-comment,close-issue]. This policy is not a seventh publication operation.

### Exact acceptance and receipt-kind constants

Prepublication QA is constructed only after frozen M passes its postmerge gate. Ordered states are AC-1 through AC-8 passed, then AC-9, AC-10, AC-11, AC-12 not-runnable-before-publication. Ordered requirements are AC-1 through AC-8 none; AC-9 live-read-back; AC-10 public-smoke; AC-11 issue-closeout; AC-12 project-upgrade.

project-upgrade is a schema-7-only profile constant, compared to the selected profile by the existing validator. It introduces no global enum or historical-profile meaning. post_criteria is exactly ordered AC-1 through AC-10, all passed; AC-11/12 are excluded.

Local receipt schemas remain 1. Kind mappings are exactly:
    prepublication-qa: vibe-kit-v0.12.0-prepublication-qa
    configured-checks: vibe-kit-v0.12.0-configured-checks
    python-3.9: vibe-kit-v0.12.0-python-3.9
    clean-build: vibe-kit-v0.12.0-clean-build
    release-gate-evidence: vibe-kit-v0.12.0-release-gate-evidence
    postpublication-acceptance: vibe-kit-v0.12.0-postpublication-acceptance

Every receipt retains the source/execution identity actually observed.

### Closed public smoke set

Exactly seventeen ordered names:
    public-direct-init-doctor
    public-plugin-bundled-plan-init-doctor
    public-upgrade-v0.3-to-v0.12.0
    public-upgrade-v0.5-to-v0.12.0
    public-upgrade-v0.6-to-v0.12.0
    public-upgrade-v0.7-to-v0.12.0
    public-upgrade-v0.8-to-v0.12.0
    public-upgrade-v0.9-to-v0.12.0
    public-upgrade-v0.10.0-to-v0.12.0
    public-upgrade-v0.10.1-to-v0.12.0
    public-upgrade-v0.11.0-to-v0.12.0
    public-repeat-upgrade-v0.12.0
    public-onboarding-exact-integer-entrypoints
    public-focused-entry-evidence-python-node
    public-inspect-run-evidence-separation
    public-inspect-run-interruption-readonly
    public-inspect-run-wrong-run-isolation

All use fresh downloaded/hash-validated public target bytes. Direct/Plugin prove read-only plan, install and installed doctor including shipped reference/declaration. Each predecessor starts healthy/authenticated, preserves project-owned content/host selection, commits target and leaves no active transaction. Repeat performs two actual same-version upgrades with truthful transaction results/healthy doctor/no active residue.

Onboarding uses actual doctor/upgrade-plan in Python/Node contexts for exact1 and invalid types/values, unchanged bytes and no state-body echo. Focused-entry executes actual Python discovery/Node package script: direct helper pass, stale-origin/wrong-argument failures, reviewed live fix pass and historical assertions preserved; static inspection/skipped Node is insufficient.

Evidence-separation creates actual verify evidence and covers default pass, partial/nonpassing, explicit receipt selection and artifact gaps; fixed origin/applicability/liveness limitations and no extra check start are observed. Interruption covers owned running, handled interruption and abrupt/no-final-body via real bounded checks; inspection remains read-only/nonpassing and process cleanup is fixture-owned, not an inspection capability or descendant-cancellation claim. Wrong-run uses genuinely different run/project evidence, mismatched explicit receipts with/without selected logs, independent receipt meaning and explicit-copy original-slot non-read. Consistent copied evidence cannot attest provenance.

## Authorization and acyclic evidence graph

Publication authorization retains exactly authorization_id, repository, version, release_kind, allowed_operations, publication_intent_sha256, host_operation_id, authorization_source_ref, bound_at. Bind existing human scope to the frozen intent; source_ref is sanitized and bound_at is executor binding time, not invented later consent. PR lifecycle uses separately recorded existing authorization, outside the six-op intent.

Acyclic graph: M/tree -> actual QA/configured/Python/build receipts -> gate bundle G -> intent I binding G/notes/tag/assets/snapshot -> exact authorization A -> host receipt R -> offline validation V -> independent acceptance P -> separate closeout intent C -> closeout authorization -> closeout receipt.

R binds I/auth/executor. P binds I,V,identities and actual local/public references. C also binds exact R/P digests. Later E records public facts without becoming M. No CLI network authority or credential is added; structural validation authenticates neither GitHub, consent, execution, applicability nor host activation.

## Public verification, reconciliation and completion

Read complete paginated tag/Release/assets; reject extra/duplicate/divergent/incomplete/unhashable state before writes. Read back each definite/uncertain write before proceeding/retry. A timeout is not absence. Second write only after positive original branch preimage or absent create/upload natural key. Denial/definite failure/execution error/divergence/still-unknown gets no retry; after attempt2 read back; no attempt3.

Never force, move tags, delete, replace assets, rewrite Release or promote stable. Freshly download all five canonical public assets, compare size/hash with I, verify corresponding inner/public members, nested checksums and distribution closure. Execute downloaded target validate-release against downloaded release and all17 smokes. Run final validate-publication on actual CPython3.9; receipt input stays read-only and optional distinct result stays create-only under ADR0022.

Claim publication only with confirmed-complete remote writes, passed public verification, valid V and independent P with AC1-10 all passed. Published-unverified is incomplete. Record immutable true/false/unknown from observed metadata; no signing/provenance/immutability inference.

## Exact separate closeout schema 5

Exclusive intent/receipt schema5, mintgao/vibe-kit, version0.12.0, parent publication schema7, ordered issues[20,22,23]. Inherit closed request/intent fields: schema_version,kind,closeout_id,parent_publication_intent_sha256,publication_receipt_sha256,verification_receipt_sha256,repository,issues,remote_snapshot,operations,authorization_scope.

closeout_id hashes canonical JSON of exactly schema_version=5, repository, version=0.12.0, parent_publication_intent_sha256 and issues=[20,22,23]. Exact marker for each is <!-- vibe-kit:v0.12.0:issue-<number>:<closeout-id> -->.

Six ordered operations: issue-20-comment/create-exact-evidence-comment, issue-20-close/close-issue, issue-22-comment/create-exact-evidence-comment, issue-22-close/close-issue, issue-23-comment/create-exact-evidence-comment, issue-23-close/close-issue. Inherit fields/natural keys/snapshot preconditions/max2/read-back and monotonic open-absent/open-exact/closed-exact. Close permits only open-exact/closed-exact; read back exact comment before close, then closed state.

Authorization retains exactly closeout_authorization_id,repository,issues,allowed_operations,closeout_intent_sha256,destructive_operations_allowed,authorization_source_ref,bound_at. Exact operation allowlist above; destructive=false. Bind separately authorized existing closeout scope to C.

Receipt fields remain schema_version,kind,closeout_id,closeout_intent_sha256,closeout_authorization_id,overall_state,items, with exact integer schema5 and inherited closed item/outcome sets. Parent requires exact7 I/R/A, complete/pass remote/public, matching valid V and independent P AC1-10; AC11/12 never gate parent.

criterion_evidence_sha256 binds a separate sanitized semantic record:
- #20: AC1 plus public-onboarding-exact-integer-entrypoints.
- #22: AC2 plus public-focused-entry-evidence-python-node, shipped reference and preserved QA ownership.
- #23: AC3 plus all3 public-inspect-run smokes and origin/applicability/interruption limitations.
The digest alone does not authenticate semantic truth; host checks actual mapped evidence.

A completed pair proves only that issue. AC11 passes after all3 exact comment/closed-state read-backs. Partial/uncertain unfinished items remain nonpassing. No operation or implemented claim for21/26/24/25.

## Mirrors, dispatch and historical preservation

Move current bin constants PUBLICATION_INTENT_SCHEMA/PUBLICATION_RECEIPT_SCHEMA/ISSUE_CLOSEOUT_INTENT_SCHEMA to7/7/5, .vibe/core/protocol.json matching fields, agent-install.json#publication matching fields, generated release manifest expectations, current AGENT_INSTALL guide/release Skill, current identity/guide/activation fixtures.

Add PUBLICATION_PROFILES[7]. Audit all applicable schema-conditioned sites: authorization source_ref/bound_at, exact5names, operation/child natural keys, intent dispatch and plan comparison/gate/Python branch, receipt/validation dispatch, existing schema6 exact-int guards extended to7, closeout authorization fields/source binding extended2-4 to2-5, parent dispatch7 to new v0.12 builder/receipt validator.

Use resolved compiled profiles, never version substitution/JSON rewriting/aliases. Historical publication1-6 and closeout1-4 retain exact identities, criteria, markers and verdicts. Schema6 remains exclusivelyv0.11. Current mirrors move; historical fixtures stay fixed. Unknown schema7 sentinels move to still-unknown values while retaining negative tests. Reject unknown/cross-profile/wrong-parent/order/assets/markers/malformed input without changing historical entry-point semantics.

## Release documentation and later evidence

Review README.md and README.zh-CN.md together before H QA and when finalizing M facts: capabilities/examples/install/upgrade/defaults/limits/candidate status agree. Before live completion retain latest verified published version and label0.12 candidate. Frozen notes do not predict publication/issue closure. After confirmed completion update homepages/context in E and read back without moving tag or rewriting body/assets.

Public audit summaries are this workitem's implementation.md,verification.md,postpublication.md,closeout.md: allowlisted facts/URLs/hashes, no raw logs/custody or new receipt fields. Decision/workitem indexes and all public references resolve.

## Separate development-project upgrade and activation boundary

AC12 follows public validation and is outside publication/closeout-parent acceptance. Use real downloaded validated target for official plan/upgrade/target doctor. Preserve local commits/project-owned context/install beforeimages until official upgrade legitimately changes state.

Inspect official planner behavior for pre-existing paths absent from old manifest; do not assume equality grants ownership. Never delete/relocate/overwrite unknown data to force success. If needed, review local Git alignment of proven tracked/framework-owned content preserving history/beforeimages; exact managed bytes match downloaded target. No fabricated ownership, hand manifest edits or conflict bypass. Failed plan remains exact path/ownership blocker.

After successful upgrade require healthy target doctor and no active transaction. Source task stops at upgraded health, validates takeover structurally with installed target CLI, and absent positive conforming reload/successor evidence gives exactly the installed manual action: create a new task in the same project. Only activated successor inspects/refreshes onboarding, adapts, runs final default verification, re-evaluates unfinished work and claims ready. Transfer stays host-owned.

## Verification, alternatives and recovery

Require schema7 positive/negative profile checks, exact17smokes, schema5 closeout order/markers/mapping/digests, already-target main/no-write, uncertainty/read-back/retry rules, create-only results, cross-profile rejection and unchanged historical positives/negatives. Preserve F1-F3 privacy/defaults/oldconfigs/Python3.9/std-lib/offline/predecessor migration/repeat recovery/installed ownership.

Static tests do not establish live model compliance, host isolation, arbitrary-secret detection, descendant cancellation or measured efficiency. Rejected: repurpose6,publishH before merge,relabel receipts,direct-main source push,closeout inside publication,publication depending on realproject upgrade,destructive recovery,manual install-state edits.

Before public writes correct/review/rebuild candidate. After writes reconcile same exact intent/natural keys and read back uncertainty; denial/divergence stops affected action with independent completed stages retained. Failed public validation preserves public objects as published-unverified with diagnosis/owner. No definition proves publication/closure/upgrade/activation/readiness. Implementation stays blocked until distinct exact review, Accepted decision, orchestrator gate and validate-readiness pass.
