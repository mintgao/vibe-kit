# 0021: Publish exact v0.10.1 — the advanced maintenance-bridge bound, the closed schema-5 publication profile, and the published Hermes verified label

- Status: Accepted
- Date: 2026-09-22
- Decision owner: read-only Tech Lead author (Hermes subagent, dispatched 2026-09-22)
- Work item: `docs/work-items/20260922-v0-10-1-publication/brief.md`
- Evidence: that brief's accepted criteria; the `20260922-host-label-raise` verification record (`docs/work-items/20260922-host-label-raise/verification.md`) and the five-stage record it cites (`docs/work-items/20260921-host-adapters/conformance.md`); and the publication, maintenance-bridge, predecessor-migration and host-registry surfaces in `bin/vibe`, `agent-install.json`, `.vibe/core/protocol.json`, `AGENT_INSTALL.md` and `README.md`
- Review: sequential-perspective Tech Lead review recorded at `docs/work-items/20260922-v0-10-1-publication/technical-review.md`; the host's subagent budget is the recorded review limitation

## Context and applicable decisions

The host-label raise landed on `main` at `3828071` with its verification record at `dc88d3f`: `HOST_REGISTRY.hermes.conformance.label` reads `verified` with the completed five-stage record as its evidence (`docs/work-items/20260921-host-adapters/conformance.md`), mirrored at `agent-install.json#hosts.hermes.conformance`, the `AGENT_INSTALL.md` registry table row, `README.md` and `docs/context/product.md`. The label is descriptive: no operation is gated by it, and the unknown-host and incoherent-selection rules stay fail-closed.

The published `v0.10.0` Pre-release (annotated tag `v0.10.0`, source commit `9628513`) is immutable — verified after publication and not to be rewritten — so the label can reach published artifacts only through a new version boundary. The source still carries kit version `0.10.0` (`.vibe/core/version`, `.vibe/version`), the maintenance bridge still bounds installs at `maximum_installed_kit_version_exclusive` `0.10.0`, and two upgrade branches plus the predecessor-migration target guard compare the target framework version literally against `0.10.0`.

ADR 0019 owns the per-host label rule this release publishes; ADR 0004 governs deterministic packaging; ADR 0008 governs readiness authority; ADR 0010 governs installation transaction and recovery; ADR 0011 governs the exact-source trust model and the publication boundary; ADR 0012 governs capability honesty; ADR 0013 governs the historical v0.8 publication contract whose field sets every later profile inherits; ADR 0014 governs the v0.9 profile; ADR 0020 governs the v0.10.0 profile (schema 4), its schema-3 #8–#13 closeout, and — in its review addendum — the shared-helper parity rule this record extends to schema 5. This record changes none of them, and it is the version boundary the release tooling and its tests are held to.

The `vibe-kit-v0.10.0-prerelease` profile (schema 4) and the schema-3 #8–#13 closeout are closed and keep exact semantics. Historical publication profiles are schema 1 (v0.7), schema 2 (v0.8), schema 3 (v0.9) and schema 4 (v0.10.0). The Codex five-stage conformance refresh remains a tracked follow-up: its runbook and host-neutral driver are delivered under `docs/work-items/20260922-host-label-raise/`, and no Codex execution is claimed. GitHub issues #14 and #15 stay open tracked defects.

## Version and compatibility identity

Select Kit version `0.10.1`. Every mirror of the kit version advances in the same change: `.vibe/core/version`, `.vibe/version`, the installed contract's `kit_version`, `agent-install.json#kit_version`, the Plugin metadata `distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json`, and every generated release identity, with `doctor` healthy and the recorded identity equal to a fresh recomputation.

Every recorded protocol and schema constant stays exactly as it is in `0.10.0` except the publication intent/receipt schema this release introduces:

- core protocol `7` — unchanged;
- Codex adapter protocol `7` — unchanged;
- Hermes adapter protocol `1` — unchanged;
- agent-install schema `4` and agent-install protocol `4` — unchanged;
- takeover schema `2` — unchanged;
- maintenance bridge schema `2` — unchanged;
- compatibility migration registry schema `2` — unchanged; its compiled digest moves while its schema does not;
- release manifest schema `2`, transaction journal and commit schemas `1`, CLI result schema `2`, feedback protocol `2` — unchanged;
- publication profile schema `5` and publication intent/receipt schema `5` — new, exclusively for `vibe-kit-v0.10.1-prerelease`;
- issue-closeout intent schema `3` — unchanged, and this release uses no closeout.

A schema or protocol constant changes only with an independently required shape change. The publication intent/receipt schema moves because the closed profile identity changes — version, tag, versioned asset names and issue policy — and a `0.10.0` receipt must not validate a `0.10.1` publication. Every other constant keeps its recorded shape, and every release-identity mirror is regenerated in the same change.

## Maintenance bridge and predecessor migration

The maintenance bridge admits exactly one versioned range. `maximum_installed_kit_version_exclusive` advances `0.10.0` → `0.10.1`, which is what lets a healthy recorded `0.10.0` install upgrade into the candidate. `minimum_installed_kit_version` stays `0.2.0`; `supported_installed_manifest_schemas` stays `[1]`; `supported_installed_agent_protocols` stays `[0, 1, 2, 3]` so older installed protocols stay upgradeable; `target_agent_install_schema` and `target_agent_install_protocol` stay `4`; `target_cli_result_schema` stays `2`; the bridge schema stays `2` and its operations stay `plan-upgrade`, `upgrade`, `recover-upgrade`, `doctor`.

The `v0.5.0-unmanaged-agent-contracts-v1` registry entry moves with the version. Its `target.framework_version` advances `0.10.0` → `0.10.1`. Its `predecessor` block does not move — `adapter_name` `codex`, `adapter_protocol` `3`, `agent_install_protocol` `1`, `agent_install_schema` `1`, `core_protocol` `3`, `framework_version` `0.5.0`, `install_identity_sha256` `70dd0eac…`, `manifest_schema` `1` — and its `paths` and path digests stay byte-exact.

The rationale is ownership: the v0.5.0-unmanaged-adoption path is executed by the installing CLI, so its target bound is the running source version. The bound must move with the version in the same change, or a healthy v0.5.0 install would be stranded with no eligible adopter.

Because the entry text changes, the compiled registry digest `PREDECESSOR_MIGRATION_REGISTRY_SHA256` is recomputed over the canonical JSON (`ensure_ascii=False`, `sort_keys=True`, compact separators) and its checked literal `EXPECTED_PREDECESSOR_MIGRATION_REGISTRY_SHA256` moves with it. Its two mirrors move in the same change and stay byte-equal to each other: `.vibe/core/protocol.json#predecessor_migrations` and `agent-install.json#maintenance_bridge.predecessor_migrations`, each exactly `schema_version` `2`, the new `registry_sha256`, `authority` `target-cli-compiled`, and `modes` `["create-pending-onboarding-if-absent", "replace-and-adopt-complete-set"]`.

The target-CLI self-check that binds the migration to the running source version moves to `0.10.1`: it already refuses any target whose framework version is not the running source version, and its rejection names the supported target. The two plan/upgrade branches that compare `version == "0.10.0"` before invoking that check move to `0.10.1` in the same change, so no path admits a stale target. No aliasing, version substitution or input rewriting is introduced.

## Exact v0.10.1 publication profile

Use a closed internal profile definition and the parameterized shared validation helpers extracted for v0.8 through v0.10.0. Historical entry points and their regression fixtures stay; profile-specific identities and criterion sets are explicit constants. Do not rewrite JSON or source text, substitute version strings, or pretend v0.10.0 evidence is v0.10.1 evidence.

The profile `vibe-kit-v0.10.1-prerelease` (schema `5`) fixes:

- repository `mintgao/vibe-kit`;
- version `0.10.1`, annotated tag `v0.10.1`;
- title `Vibe Kit v0.10.1`;
- release body `docs/releases/0.10.1.md`;
- non-draft Pre-release, no generated notes, no platform-immutability promise;
- exactly five asset roles with exact v0.10.1 names: `SHA256SUMS` (checksum), `release-manifest.json` (manifest), `vibe-kit-0.10.1.zip` (direct), `vibe-kit-distribution-0.10.1.zip` (distribution), `vibe-kit-plugin-0.10.1.zip` (plugin);
- the same six publication operations as v0.8, v0.9 and v0.10.0, in the same order and with their per-asset ledgers unchanged: `fast-forward-main`, `create-or-confirm-annotated-tag`, `create-or-confirm-prerelease`, `upload-or-confirm-five-assets`, `read-back-publication`, `download-and-verify-public-assets`; closeout is never a seventh publication operation;
- publication intent/receipt schema `5`.

`agent-install.json#publication` mirrors the profile: `intent_schema` `5`, `receipt_schema` `5`, `issue_closeout_intent_schema` `3`; `public_asset_roles` stays exactly `checksum`, `manifest`, `direct`, `distribution`, `plugin`; `commands`, `network_credentials_owner` (`agent-host`) and `cli_network_authority` (`false`) stay unchanged. `.vibe/core/protocol.json` carries the same three schema values.

The inherited field sets are ADR 0013's schema-2 intent, receipt and authorization shapes as ADR 0014 and ADR 0020 restated them for schema 3 and schema 4, with these v0.10.1 identity changes:

1. Version, profile, tag, title, body path and the five versioned asset names are exactly those fixed above.
2. The six publication operations keep ADR 0013's field sets, operation preconditions, per-asset ledgers, attempt classification, outcome enums, bounded retry and read-back/recovery semantics unchanged.
3. Intent `issue_closeout_policy` is exactly `{"mode": "none", "issues": [], "allowed_operations": []}`.
4. Publication receipt `issue_closeout` remains exactly `null`. Closeout results would be a separate receipt; publication validation never waits for issue closure.
5. Local evidence receipt schemas remain `1`, with exactly the v0.10.1 kinds replacing the v0.10.0 kinds: `vibe-kit-v0.10.1-prepublication-qa`, `vibe-kit-v0.10.1-configured-checks`, `vibe-kit-v0.10.1-python-3.9`, `vibe-kit-v0.10.1-clean-build`, `vibe-kit-v0.10.1-release-gate-evidence`, `vibe-kit-v0.10.1-postpublication-acceptance`.
6. The publication authorization retains ADR 0013's seven fields — `authorization_id`, `repository`, `version`, `release_kind`, `allowed_operations`, `publication_intent_sha256`, `host_operation_id` — and adds exactly `authorization_source_ref` and `bound_at`. The former is a nonempty sanitized host reference to existing authorization; the latter is ISO-8601. These prove structural binding, not consent authenticity, and no later user-message requirement is inherited.
7. ADR 0013's historical closeout-parent exception remains v0.7-only and cannot validate a v0.10.1 parent.

Shared-helper parity is the trap ADR 0020's addendum named, and this record extends the named set from four places to the seven sites — six grouped checks — that carry a schema-4 (or schema-2/3/4) condition in `bin/vibe` today. Each must admit schema `5` without changing schema-1/2/3/4 behavior, and a schema-5 profile must receive every one of these checks:

- the authorization field set and its source-reference/binding-time validation, conditioned today on `profile['schema'] in (3, 4)`;
- the exact asset-name closure over the profile's five asset names and roles;
- the operation natural-key grammar — the ordered `publish-<index>` and `asset-<index>` identities, the per-operation natural keys, and the child key `mintgao/vibe-kit:release:<tag>:asset:<name>`, all keyed off `profile['tag']` so the v0.10.1 tag is admitted;
- the intent dispatch and the publication-plan schema selection, including the profile-selected `expected_version`, the `docs/releases/<version>.md` body path, and the comparison-candidate/release-gate branch;
- the receipt dispatch;
- the `validate-publication` command dispatch, which today accepts `schema in (2, 3, 4)` and must accept `5` while still refusing anything else.

Historical profiles schema `1` (v0.7), schema `2` (v0.8), schema `3` (v0.9) and schema `4` (v0.10.0) keep byte-exact semantics: their entry points, acceptance sets, markers and fixtures are unchanged, a v0.10.1 candidate must not pass them, unknown profiles fail closed, and cross-profile combinations fail closed. Shared helpers receive a resolved compiled profile; input rewriting and version aliasing are prohibited. The closeout dispatch stays unchanged: it selects the v0.9 or v0.10.0 closeout builders from the parent intent schema, and no schema-5 closeout exists.

### Prepublication criteria and smokes

The prepublication QA receipt's `criterion_mapping` lists the brief's criteria, in order:

| Criterion | Required prepublication state | Postpublication requirement |
|---|---|---|
| AC-1 | passed | none |
| AC-2 | passed | none |
| AC-3 | passed | none |
| AC-4 | passed | none |
| AC-5 | passed | none |
| AC-6 | not-runnable-before-publication | live-read-back |

Neither pending criterion may be reported passed before its phase. AC-6's live read-back references the live tag, commit and Release metadata, the five unauthenticated asset downloads, distribution validation, the complete smoke set and successful offline publication validation. Postpublication acceptance contains exactly AC-1 through AC-6, all `passed`.

The required public smoke set is exactly nine names:

```text
public-direct-init-doctor
public-plugin-bundled-plan-init-doctor
public-upgrade-v0.3-to-v0.10.1
public-upgrade-v0.5-to-v0.10.1
public-upgrade-v0.6-to-v0.10.1
public-upgrade-v0.7-to-v0.10.1
public-upgrade-v0.8-to-v0.10.1
public-upgrade-v0.9-to-v0.10.1
public-upgrade-v0.10.0-to-v0.10.1
```

Each upgrade smoke starts from a healthy authenticated install of the named predecessor and verifies successful target installation and `doctor`; it claims no host activation.

## No issue closeout

This release closes no issue. GitHub issues #14 (`validate-publication --receipt` rewrites its input receipt with the result envelope) and #15 (re-running `upgrade` on an already-current install fails target postimage validation and rolls back) stay tracked defects, excluded by the product owner's resolved decision of 2026-09-22: the release contains no product change beyond the label raise and the version identity.

The issue-closeout intent schema stays `3`, and the schema-3 closeout graph stays exclusively the v0.10.0 one: no v0.10.1 closeout intent, authorization, receipt or operation exists, and the publication receipt's `issue_closeout` stays `null`. Publication validation never waits for issue closure, and no issue is commented or closed in this work item.

## Release notes, homepage review and the managed-guide drift check

`CHANGELOG.md` and `docs/releases/0.10.1.md` may claim exactly:

- the Hermes host label raise to `verified` on its completed five-stage conformance record under ADR 0019;
- the version-identity advance to `0.10.1`;
- that nothing else ships.

They must not claim or imply live host activation, a measured token reduction, automatic reload or automatic successor handoff, stable promotion, signing, provenance, platform immutability, a refreshed Codex record, or any fix for #14 or #15.

Both homepages (`README.md`, `README.zh-CN.md`) are reviewed for version, links, installation commands, capabilities and limitations. The literals that move are the latest-published tag line and its link, the two adoption prompts, the version/schema statement paragraph, the `validate-release` example, the release-notes link and the limitations bullet; changed facts must agree across both languages. Sections whose facts do not change — the trust contract, the takeover description, the manual-fallback wording — receive a reasoned unchanged record. Both states are frozen before final candidate QA.

The managed guide `AGENT_INSTALL.md` carries three version literals — the identification line, the activation-notice text, and the publication-boundary paragraph naming the closed v0.10.0 schema-4 Pre-release. Those three literals are already bound by `tests/test_v010_publication.py::ManagedGuideDriftTests`, which requires each literal to equal the framework version and the publication-boundary paragraph's schema number to equal `PUBLICATION_INTENT_SCHEMA`. The three literals move with the framework version under that existing check; no new drift check is added or needed.

## Ownership, recovery and verification

One RD writer owns implementation. Independent QA owns the complete default lane on the unchanged final candidate and runs it exactly once. The release gate additionally requires the default lane on CPython 3.13 and 3.9, `doctor`, `validate-readiness`, `package`, `validate-release`, and two independent clean builds from the same commit proving byte-identical five-asset sets.

Required scenarios:

1. Version and mirror coherence: `0.10.1` in every named mirror, the recorded release identities equal to a fresh recomputation, and `doctor` healthy.
2. The upgrade fixture covers both a healthy recorded `0.10.0` install and a pre-`0.10.0` recorded install upgrading into the candidate through the maintenance bridge with their files, recorded host selection and identity preserved.
3. The `v0.5.0-unmanaged-agent-contracts-v1` migration authenticates a healthy v0.5.0 install under target `0.10.1`, and a source CLI of any other version refuses it.
4. A fresh candidate install is doctor-healthy for a `codex`, a `hermes` and a combined selection, and the installed contract's Hermes label reads `verified`.
5. The v0.10.1 profile accepts its exact intent and receipt and rejects a wrong version, tag, title, body hash, asset name, asset count or operation set.
6. Historical acceptance and rejection: the schema-1, schema-2, schema-3 and schema-4 entry points behave exactly as recorded, a v0.10.1 candidate fails them, and an unknown profile or cross-profile combination fails closed.
7. Guide drift: the existing drift check passes with the three guide literals moved, and a divergent literal still fails it.
8. Release gate: the dual-lane configured checks, the packaged artifacts, `validate-release`, and two byte-identical independent clean builds.
9. Public verification: tag, commit and Release read-back, all five unauthenticated asset hashes, the complete nine-smoke set, and successful offline publication validation.

Before publication, recovery is git revert plus a disposable candidate rebuild; installation recovery remains ADR 0010. After remote writes, use same-intent reconciliation only — never force push, move the tag, replace assets, or delete the Release — and uncertain or partial state remains explicitly incomplete. Changed candidate bytes invalidate the frozen intent and evidence: rebuild and rebind within the authorized scope; a changed destination, version, operation scope, destructive behavior or other material commitment requires a new user decision.

No GitHub write happens in this work item. The public completion claim "v0.10.1 published and verified" is available only from `confirmed-complete` remote state plus passed public verification under a separate executable authorization bound to the frozen intent digest. Credentials and raw host output stay out of durable evidence.

## Alternatives and trade-offs

- Holding `maximum_installed_kit_version_exclusive` at `0.10.0`, or advancing it past the kit version. Rejected: the first strands a healthy recorded `0.10.0` install, and the second admits an out-of-range predecessor.
- Reusing publication schema 4 for the new profile. Rejected: the version identity, tag, versioned asset names and issue policy all changed, and aliasing would let a `0.10.0` receipt validate a `0.10.1` publication.
- Rewriting, migrating or aliasing the historical schema-1 through schema-4 profiles, their receipts or their fixtures. Rejected: historical contracts keep byte-exact semantics and a v0.10.1 candidate must fail them.
- Advancing the bridge bound without moving the `v0.5.0-unmanaged-agent-contracts-v1` target or its compiled digest. Rejected: that adoption path is owned by the installing CLI, so the target, the checked digest literal and both mirrors must move together or a healthy v0.5.0 install is stranded.
- Advancing the version files while leaving the two plan/upgrade branches and the migration target guard on the literal `0.10.0`. Rejected: the upgrade paths would still require a stale target and the guard's rejection would name the wrong supported target, so no healthy install could reach the candidate.
- Folding the label raise into a later feature release instead of a patch release. Rejected: the product owner resolved on 2026-09-22 that the completed record ships as `0.10.1`, and the published v0.10.0 is immutable.
- Fixing issue #14 or #15 in this release. Rejected: the product owner's resolved decision fixes the release contents to the label raise and the version identity, and each defect carries its own reproduction and regression obligations.
- Introducing a schema-5 closeout, or reusing the schema-3 closeout for a v0.10.1 parent. Rejected: this release closes no issue, and the schema-3 closeout graph is bound to the v0.10.0 parent intent.
- Adding a second guide drift check, or leaving the guide's version literals at `0.10.0`. Rejected: `ManagedGuideDriftTests` already binds all three literals to the framework version, so a duplicate check adds nothing while a stale literal fails the lane.
- Copying the v0.10.0 publisher, or widening the shared helpers into a generic configurable publisher. Rejected: share the checked helpers with explicit closed profiles rather than duplicating the trust surface or widening the accepted compatibility boundary.
- Claiming live host activation, stable promotion, signing, provenance, platform immutability or a refreshed Codex record alongside the label raise. Rejected: labels follow recorded evidence, and the Codex five-stage run is a handoff with no execution claimed.
- Recovering a partial remote write by force push, tag movement, asset replacement or Release deletion. Rejected: after remote writes only same-intent reconciliation is permitted, and changed candidate bytes invalidate the frozen intent and evidence.

No unresolved product choice remains within this accepted scope.
