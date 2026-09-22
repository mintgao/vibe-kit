# 0020: Publish exact v0.10.0 — the advanced maintenance-bridge bound, the closed schema-4 publication profile, and the #8–#13 issue closeout

- Status: Accepted
- Date: 2026-09-22
- Decision owner: read-only Tech Lead author (Hermes subagent, dispatched 2026-09-22)
- Work item: `docs/work-items/20260922-v0-10-0-publication/brief.md`
- Evidence: that brief's accepted criteria; the verification records of `20260921-readiness-naming-grammar`, `20260921-host-neutral-manual-activation`, `20260921-verify-contract-closure`, `20260921-takeover-admission` and `20260921-host-adapters`; and the publication, maintenance-bridge and predecessor-migration surfaces in `bin/vibe`, `agent-install.json` and `.vibe/core/protocol.json`
- Review: approved by the orchestrator as a distinct sequential-perspective Tech Lead reviewer on 2026-09-22 after one material addendum and two editorial notes; the host's 600 s subagent budget is the recorded review limitation

## Context and applicable decisions

Iteration 0.10.0 closed five work items on this repository — `20260921-readiness-naming-grammar`, `20260921-host-neutral-manual-activation`, `20260921-verify-contract-closure`, `20260921-takeover-admission` and `20260921-host-adapters` — and the iteration is verified at `d5fa87a`, the commit that records the host adapters verification evidence. The takeover-admission record freezes candidate `bc7ac542…` and the host-adapters record freezes candidate `d65e2dd…`; both were re-run independently on their frozen candidates, and the earlier candidates that moved are recorded as stale rather than as valid evidence. Their per-criterion evidence covers the six feedback issues this release closes: #8 and issue #13's findings F2, F7 and F12 in takeover admission; #9 and the findings F6, F10 and F11 in verify contract closure; #11 and the findings F8 and F9 in readiness naming grammar; the host-neutral and manual-activation findings in host-neutral manual activation; and the remaining #10, #12 and #13 findings across the same items.

The source still carries kit version `0.9.0` (`.vibe/core/version`, `.vibe/version`) and the maintenance bridge still bounds installs at `maximum_installed_kit_version_exclusive` `0.9.0`, so a v0.9.0 install cannot yet upgrade into the candidate. `v0.9.0` is the latest published non-draft GitHub Pre-release; its publication profile is schema 3 and its #6/#7 closeout is schema 2.

ADR 0004 governs deterministic packaging; ADR 0008 governs readiness authority; ADR 0010 governs installation transaction and recovery; ADR 0011 governs the exact-source trust model and the closeout transaction this record inherits; ADR 0012 governs capability honesty in the operating model; ADR 0013 governs the historical v0.8 publication contract whose field sets the later profiles inherit; ADR 0014 governs the v0.9 profile (schema 3) and its schema-2 closeout, whose section shape and level of exactness this record mirrors; ADRs 0015 through 0019 are the iteration's closed decisions this release publishes. This record changes none of them, and it is the version boundary the release tooling and its tests are held to.

## Version and compatibility identity

Select Kit version `0.10.0`. Every mirror of the kit version advances in the same change: `.vibe/core/version`, `.vibe/version`, the installed contract's `kit_version`, `agent-install.json#kit_version`, the Plugin metadata, and every generated release identity, with `doctor` healthy and the recorded identity equal to a fresh recomputation.

Every recorded protocol and schema constant stays exactly as it is except the two this release introduces:

- core protocol `7` — unchanged;
- Codex adapter protocol `7` — unchanged;
- Hermes adapter protocol `1` — unchanged, published first-class with `supported-unverified` under ADR 0019;
- agent-install schema `4` and agent-install protocol `4` — unchanged;
- takeover schema `2` — unchanged;
- maintenance bridge schema `2` — unchanged;
- compatibility migration registry schema `2` — unchanged; its compiled digest moves while its schema does not;
- release manifest schema `2`, transaction journal and commit schemas `1`, CLI result schema `2` — unchanged;
- publication profile schema `4` and publication intent/receipt schema `4` — new, exclusively for `vibe-kit-v0.10.0-prerelease`;
- issue-closeout intent schema `3` — new, exclusively for the #8–#13 closeout.

A schema or protocol constant changes only with an independently required shape change. This release changes no shape: it moves the version boundary, adds the closed v0.10.0 publication profile and the schema-3 closeout shape, and regenerates every release-identity mirror in the same change.

## Maintenance bridge and predecessor migration

The maintenance bridge admits exactly one versioned range. `maximum_installed_kit_version_exclusive` advances `0.9.0` → `0.10.0`, which is what lets a healthy recorded `0.9.0` install upgrade into the candidate. `minimum_installed_kit_version` stays `0.2.0`; `supported_installed_manifest_schemas` stays `[1]`; `supported_installed_agent_protocols` stays `[0, 1, 2, 3]` so older installed protocols stay upgradeable; `target_agent_install_schema` and `target_agent_install_protocol` stay `4`; `target_cli_result_schema` stays `2`; the bridge schema stays `2` and its operations stay `plan-upgrade`, `upgrade`, `recover-upgrade`, `doctor`.

The `v0.5.0-unmanaged-agent-contracts-v1` registry entry moves with the version. Its `target.framework_version` advances `0.9.0` → `0.10.0`. Its `predecessor` block does not move — `adapter_name` `codex`, `adapter_protocol` `3`, `agent_install_protocol` `1`, `agent_install_schema` `1`, `core_protocol` `3`, `framework_version` `0.5.0`, `install_identity_sha256` `70dd0eac…`, `manifest_schema` `1` — and its `paths` and path digests stay byte-exact.

The rationale is ownership: the v0.5.0-unmanaged-adoption path is executed by the installing CLI, so its target bound is the running source version. The bound must move with the version in the same change, or a healthy v0.5.0 install would be stranded with no eligible adopter.

Because the entry text changes, the compiled registry digest `PREDECESSOR_MIGRATION_REGISTRY_SHA256` is recomputed over the canonical JSON (sorted keys, compact separators) and its checked literal `EXPECTED_PREDECESSOR_MIGRATION_REGISTRY_SHA256` moves with it. Its two mirrors move in the same change and stay byte-equal to each other: `.vibe/core/protocol.json#predecessor_migrations` and `agent-install.json#maintenance_bridge.predecessor_migrations`, each exactly `schema_version` `2`, the new `registry_sha256`, `authority` `target-cli-compiled`, and `modes` `["create-pending-onboarding-if-absent", "replace-and-adopt-complete-set"]`.

The target-CLI self-check that binds the migration to the running source version moves to `0.10.0`: it already refuses any target whose framework version is not the running source version, and its rejection names the supported target. No aliasing, version substitution or input rewriting is introduced.

## Exact v0.10.0 publication profile

Use a closed internal profile definition and the parameterized shared validation helpers extracted for v0.8 and v0.9. Historical entry points and their regression fixtures stay; profile-specific identities and criterion sets are explicit constants. Do not rewrite JSON or source text, substitute version strings, or pretend v0.10.0 evidence is v0.9 evidence.

The profile `vibe-kit-v0.10.0-prerelease` (schema `4`) fixes:

- repository `mintgao/vibe-kit`;
- version `0.10.0`, annotated tag `v0.10.0`;
- title `Vibe Kit v0.10.0`;
- release body `docs/releases/0.10.0.md`;
- non-draft Pre-release, no generated notes, no platform-immutability promise;
- exactly five asset roles with exact v0.10.0 names: `SHA256SUMS` (checksum), `release-manifest.json` (manifest), `vibe-kit-0.10.0.zip` (direct), `vibe-kit-distribution-0.10.0.zip` (distribution), `vibe-kit-plugin-0.10.0.zip` (plugin);
- the same six publication operations as v0.8 and v0.9, with their ordered per-asset ledgers unchanged: `fast-forward-main`, `create-or-confirm-annotated-tag`, `create-or-confirm-prerelease`, `upload-or-confirm-five-assets`, `read-back-publication`, `download-and-verify-public-assets`; closeout is never a seventh publication operation;
- publication intent/receipt schema `4` and issue-closeout intent schema `3`.

`agent-install.json#publication` mirrors the profile: `intent_schema` `4`, `receipt_schema` `4`, `issue_closeout_intent_schema` `3`; `public_asset_roles` stays exactly `checksum`, `manifest`, `direct`, `distribution`, `plugin`; `commands`, `network_credentials_owner` (`agent-host`) and `cli_network_authority` (`false`) stay unchanged. `.vibe/core/protocol.json` carries the same three schema values.

The inherited field sets are ADR 0013's schema-2 intent, receipt and authorization shapes as ADR 0014 restated them for schema 3, with these v0.10.0 identity changes:

1. Version, profile, tag, title, body path and the five versioned asset names are exactly those fixed above.
2. The six publication operations keep ADR 0013's field sets, operation preconditions, per-asset ledgers, attempt classification, outcome enums, bounded retry and read-back/recovery semantics unchanged.
3. Intent `issue_closeout_policy` is exactly `{"mode": "after-public-verification", "issues": [8, 9, 10, 11, 12, 13], "allowed_operations": ["create-exact-evidence-comment", "close-issue"]}`.
4. Publication receipt `issue_closeout` remains exactly `null`. Closeout results are a separate receipt; publication validation never waits for issue closure.
5. Local evidence receipt schemas remain `1`, with exactly the v0.10.0 kinds replacing the v0.9 kinds: `vibe-kit-v0.10-prepublication-qa`, `vibe-kit-v0.10-configured-checks`, `vibe-kit-v0.10-python-3.9`, `vibe-kit-v0.10-clean-build`, `vibe-kit-v0.10-release-gate-evidence`, `vibe-kit-v0.10-postpublication-acceptance`.
6. The publication authorization retains ADR 0013's seven fields — `authorization_id`, `repository`, `version`, `release_kind`, `allowed_operations`, `publication_intent_sha256`, `host_operation_id` — and adds exactly `authorization_source_ref` and `bound_at`. The former is a nonempty sanitized host reference to existing authorization; the latter is ISO-8601. These prove structural binding, not consent authenticity, and no later user-message requirement is inherited.
7. ADR 0013's historical closeout-parent exception remains v0.7-only and cannot validate a v0.10.0 parent.

Historical profiles schema `1` (v0.7), schema `2` (v0.8) and schema `3` (v0.9) keep byte-exact semantics: their entry points, acceptance sets, markers and fixtures are unchanged, a v0.10.0 candidate must not pass them, unknown profiles fail closed, and cross-profile combinations fail closed. Shared helpers receive a resolved compiled profile; input rewriting and version aliasing are prohibited.

### Prepublication criteria and smokes

The prepublication QA receipt's `criterion_mapping` lists the brief's criteria, in order:

| Criterion | Required prepublication state | Postpublication requirement |
|---|---|---|
| AC-1 | passed | none |
| AC-2 | passed | none |
| AC-3 | passed | none |
| AC-4 | passed | none |
| AC-5 | passed | none |
| AC-6 | passed | none |
| AC-7 | not-runnable-before-publication | live-read-back |
| AC-CLOSE.1 | not-runnable-before-publication | issue-closeout |

Neither pending criterion may be reported passed before its phase. AC-7's live read-back references the live tag, commit and Release metadata, the five unauthenticated asset downloads, distribution validation, the complete smoke set and successful offline publication validation.

The required public smoke set is exactly:

```text
public-direct-init-doctor
public-plugin-bundled-plan-init-doctor
public-upgrade-v0.3-to-v0.10
public-upgrade-v0.5-to-v0.10
public-upgrade-v0.6-to-v0.10
public-upgrade-v0.7-to-v0.10
public-upgrade-v0.8-to-v0.10
public-upgrade-v0.9-to-v0.10
```

Each upgrade smoke starts from a healthy authenticated install of the named predecessor and verifies successful target installation and doctor; it claims no host activation. Postpublication acceptance contains exactly AC-1 through AC-7, all `passed`, and this passing receipt authorizes entering the already-authorized closeout phase.

## Issue closeout for #8–#13

Use closeout-intent schema `3` for exactly the issues this iteration verified as fixed, in this order: `[8, 9, 10, 11, 12, 13]`.

The product owner's standing standard is that an issue may be closed only when its fix is confirmed by verification. All six are covered by the closed work items `20260921-readiness-naming-grammar`, `20260921-host-neutral-manual-activation`, `20260921-verify-contract-closure`, `20260921-takeover-admission` and `20260921-host-adapters`, whose verification records carry the per-criterion evidence; issue #13's findings F1–F12 map onto those same items.

Inherit ADR 0011's "Issue #1–#5 closeout transaction" top-level and child field sets, types, observations, authorization scope, operation preconditions, bounded retry, duplicate rejection and monotonic resume, with precisely these differences:

- Issues are exactly `[8, 9, 10, 11, 12, 13]`, in that order.
- The closeout ID preimage uses `schema_version: 3`, version `0.10.0`, repository `mintgao/vibe-kit`, the v0.10.0 parent publication-intent digest, and `[8, 9, 10, 11, 12, 13]`.
- Markers are exactly `<!-- vibe-kit:v0.10.0:issue-<n>:<closeout_id> -->`.
- Twelve operations execute in order — comment then close, for each issue in ascending order — with sequences `0..11`. Existing operation ID and natural-key grammar remains unchanged.
- `publication_receipt_sha256` binds the validated schema-4 publication receipt; `verification_receipt_sha256` binds the passing v0.10.0 postpublication acceptance receipt. Both must bind the same parent intent, source, profile and authorization.
- Scope issues become `[8, 9, 10, 11, 12, 13]`; allowed operations remain comment and close; destructive operations remain false. `requires_separate_closeout_authorization=true` means a distinct executable record, not a new user confirmation.
- The closeout authorization has ADR 0011's six exact fields plus `authorization_source_ref` and `bound_at`, with the same semantics as above.
- At most two writes per operation remain allowed; uncertainty, permission failure, mismatch, duplicate matching comments, and closed-without-exact-comment block further writes. An exact closed issue is reusable on resume.

No closeout write may begin before a validated schema-4 publication receipt with `remote_write_state` `confirmed-complete` and `verification_state` `passed`, plus a passing postpublication acceptance receipt. The closeout authorization is read before the first write; each issue's exact comment freezes its original-problem/fix/regression/public-version mapping; markers give exact idempotency; every operation is read back; divergence stops the transaction. Unrelated issues are never edited, and nothing is closed before verification.

The standalone closeout receipt has exactly:

```text
schema_version = 3
kind = vibe-kit-issue-closeout-receipt
closeout_id
closeout_intent_sha256
closeout_authorization_id
overall_state
items
```

`overall_state` retains ADR 0011's enum (`not-run`, `confirmed-partial`, `confirmed-complete`, `uncertain`, `conflict`). `items` is exactly `[8, 9, 10, 11, 12, 13]`; each item has exactly:

```text
issue_number
expected_initial_state
comment_body_sha256
comment_id
comment_url
comment_write_state
close_write_state
observed_post_state
read_back
error
```

States are `open|closed`; `observed_post_state` may be null before observation. Comment ID and URL may be null before confirmation; otherwise the ID is positive and the URL is the canonical matching GitHub issue-comment URL. Write states use ADR 0011's operation-outcome enum. `read_back` is boolean; `error` is null or its closed `code,message,next_action` shape. Complete requires both exact comments and closed states read back, valid IDs and URLs, successful terminal operation states, and no errors.

AC-CLOSE.1 is completed only by this validated standalone closeout receipt plus its issue-to-fix/regression/version evidence; final task completion requires both receipts.

## Release notes, homepage review and the managed-guide drift check

`CHANGELOG.md` and `docs/releases/0.10.0.md` describe the iteration honestly and may claim only what the closed evidence supports:

- the readiness grammar widening (ADR 0016);
- the verification-contract closure: declared check order, preserved failure output, environment-limited verdicts, and the constrained-QA path (ADR 0017);
- takeover admission: the published takeover object, `--receipt` artifacts, the minimal manual-transfer payload, and the `existing-install-admission` receipt (ADR 0018);
- host adapters: the per-host registry, the schema-4 agent-install contract, and the first-class Hermes entry recorded `supported-unverified` (ADR 0019).

The notes must not raise or imply a Hermes conformance label, claim live host activation, claim a measured token reduction, or claim automatic reload or automatic successor handoff. The Codex five-stage re-run under the schema-4 contract stays a tracked follow-up, and no host's label moves without an equivalent record.

Both homepages (`README.md`, `README.zh-CN.md`) are reviewed for version, links, installation commands, capabilities and limitations. Changed facts must agree across both; unchanged sections receive a reasoned review record; both states are frozen before final candidate QA.

The managed guide `AGENT_INSTALL.md` carries version literals that no check binds to the framework version today — the opening identification line, the activation-notice text, and the publication-boundary paragraph naming the closed v0.9.0 schema-3 Pre-release and the #6/#7 closeout plan. The release adds a drift check that fails when the guide's version literals diverge from `.vibe/core/version`, pinned by a regression test, and the guide's publication paragraph presents the closed v0.10.0 schema-4 profile and the #8–#13 closeout under it.

## Ownership, recovery and verification

One RD writer owns implementation. Independent QA owns the complete default lane on the unchanged final candidate. The release gate additionally requires the default lane on CPython 3.13 and 3.9, `doctor`, `validate-readiness`, `package`, `validate-release`, and two independent clean builds from the same commit proving byte-identical five-asset sets.

Required scenarios:

1. Version and mirror coherence: `0.10.0` in every named mirror, the recorded release identities equal to a fresh recomputation, and `doctor` healthy.
2. A healthy authenticated `0.9.0` install upgrades into the candidate through the maintenance bridge with its files, recorded host selection and identity preserved.
3. A fresh candidate install is doctor-healthy for a `codex`, a `hermes` and a combined selection, and the per-host payload partition holds.
4. The `v0.5.0-unmanaged-agent-contracts-v1` migration authenticates a healthy v0.5.0 install under target `0.10.0`, and a source CLI of any other version refuses it.
5. The v0.10.0 profile accepts its exact intent and receipt and rejects a wrong version, tag, title, body hash, asset name, asset count or operation set.
6. Historical acceptance and rejection: the schema-1, schema-2 and schema-3 entry points behave exactly as recorded, a v0.10.0 candidate fails them, and an unknown profile or cross-profile combination fails closed.
7. Guide drift: a divergent version literal in `AGENT_INSTALL.md` fails the drift check, and the pinned literal passes.
8. Release gate: the dual-lane configured checks, the packaged artifacts, `validate-release`, and two byte-identical independent clean builds.
9. Public verification: tag, commit and Release read-back, all five unauthenticated asset hashes, the complete smoke set, and the #8–#13 closeout read-back under a separate authorization.

Before publication, recovery is git revert plus a disposable candidate rebuild; installation recovery remains ADR 0010. After remote writes, use same-intent reconciliation only — never force push, move the tag, replace assets, or delete the Release — and uncertain or partial state remains explicitly incomplete. Changed candidate bytes invalidate the frozen intent and evidence: rebuild and rebind within the authorized scope; a changed destination, version, operation scope, destructive behavior or other material commitment requires a new user decision.

No GitHub write happens in this work item. The public completion claim "v0.10.0 published and verified" is available only from `confirmed-complete` remote state plus passed public verification under a separate executable authorization bound to the frozen intent digest. The host capability limitation is recorded honestly where the record requires it, in the machine-checkable form of the constrained path; credentials and raw host output stay out of durable evidence.

## Alternatives and trade-offs

- Holding `maximum_installed_kit_version_exclusive` at `0.9.0`, or advancing it past the kit version. Rejected: the first strands a healthy v0.9.0 install, and the second admits an out-of-range predecessor.
- Advancing the bridge bound without moving the `v0.5.0-unmanaged-agent-contracts-v1` target. Rejected: that adoption path is owned by the installing CLI, so its bound must move with the version or a healthy v0.5.0 install is stranded.
- Reusing publication schema 3 for the new profile. Rejected: the version identity, the versioned asset names, the issue policy and the closeout shape all changed, and aliasing would let a v0.9 receipt validate a v0.10.0 publication.
- Rewriting, migrating or aliasing the historical schema-1, schema-2 and schema-3 profiles or their receipts. Rejected: historical contracts keep byte-exact semantics.
- Closing #8–#13 as a group without the per-issue verification mapping. Rejected: the product owner's standard requires confirmed verification for each issue.
- Raising or implying the Hermes conformance label, or claiming live activation. Rejected: labels follow recorded evidence, and the Codex five-stage re-run under schema 4 remains tracked.
- A prose-only guide review with no binding check. Rejected: prose version literals drift silently, which is how the guide still carries an unbound version paragraph.
- Copying the v0.9 publisher, or writing a generic configurable publisher. Rejected: share the checked helpers with explicit closed profiles rather than duplicating the trust surface or widening the accepted compatibility boundary.

No unresolved product choice remains within this accepted scope.

## Review addendum: schema-4 helper parity and the closeout graph

Recorded by the orchestrator as the distinct sequential-perspective Tech Lead reviewer on 2026-09-22. This host does have native subagents, but analysis-shaped review packets exceed its 600 s session budget, so the review is a sequential-perspective pass and that capability limitation is recorded rather than hidden. The decision above is accepted as written; this addendum binds three implementation details the record must not leave implicit.

1. Shared-helper parity (material). The publication helpers this record inherits were parameterized for schema 3 and must admit schema 4 without changing schema-1/2/3 behavior. Four places carry a schema-3 (or schema-2/3) condition today — the authorization field set and its source-reference/time validation, the exact asset-name closure, the operation natural-key grammar, and the `validate_publication_intent` schema dispatch. A schema-4 profile must receive every one of those checks; a schema-3 profile must keep receiving exactly them and nothing more.
2. Closeout authorization parity (material). `validate_profile_closeout_authorization` adds `authorization_source_ref` and `bound_at` only for schema 2 today. The schema-3 closeout inherits the same two fields under the same validation, per the authorization paragraph above.
3. Closeout graph prose (editorial). The shared closeout builder's failure text names "issues 1 through 5" and a ten-operation graph. Under the schema-3 closeout the messages must state the actual ordered issue set and the actual operation count (twelve, sequences 0..11): a fail-closed message that misstates the graph misleads the host it stops.

Editorial note: the version-identity section names `agent-install.json#kit_version` twice, once as the installed contract's `kit_version`. The duplication is harmless and the decision is unchanged.
