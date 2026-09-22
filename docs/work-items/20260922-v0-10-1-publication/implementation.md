# Implementation: Publish Vibe Kit v0.10.1

Plan, explicit before any edit (single writer, this work item). Frozen decision:
`docs/decisions/0021-v0-10-1-publication.md` (Accepted), reviewed by a distinct
sequential-perspective Tech Lead pass recorded in `technical-review.md` with one
editorial correction applied. Readiness gate: `implementation-ready`
(`validate-readiness` `valid`) before the first edit.

## Edit sequence (one change; mirrors last)

1. Version identity: `.vibe/core/version`, `.vibe/version`,
   `agent-install.json#kit_version` and the Plugin metadata move
   `0.10.0 → 0.10.1`.
2. Maintenance bridge: `maximum_installed_kit_version_exclusive`
   `0.10.0 → 0.10.1`, with `minimum_installed_kit_version` `0.2.0`,
   `supported_installed_manifest_schemas` `[1]`, `supported_installed_agent_protocols`
   `[0, 1, 2, 3]`, the target schemas and the four operations unchanged.
3. Predecessor-migration registry: the
   `v0.5.0-unmanaged-agent-contracts-v1` entry's `target.framework_version`
   advances to `0.10.1` with its predecessor block and path digests byte-exact;
   `PREDECESSOR_MIGRATION_REGISTRY_SHA256` is recomputed
   (`cf0b7a15… → 7cedd9fb…`) and written into the checked literal and both
   mirrors (`.vibe/core/protocol.json#predecessor_migrations`,
   `agent-install.json#maintenance_bridge.predecessor_migrations`).
4. Upgrade-path audit: `validate_target_predecessor_migration_contract`'s
   framework-version guard and its rejection message, plus the two
   `version == ...` plan/upgrade branches, move to `0.10.1` in the same change.
   No aliasing, version substitution or input rewriting is introduced.
5. Publication schema 5: `PUBLICATION_INTENT_SCHEMA`/`PUBLICATION_RECEIPT_SCHEMA`
   become `5`; `PUBLICATION_PROFILES[5]` is added as the closed
   `vibe-kit-v0.10.1-prerelease` profile (version, tag, title, body path, five
   exact asset names, the six operations, the nine-smoke set, AC-1…AC-6 with
   AC-6 `not-runnable-before-publication`/`live-read-back`, the six
   `vibe-kit-v0.10.1-*` evidence kinds, the authorization fields and issue policy
   `{"mode": "none", "issues": [], "allowed_operations": []}`).
   `ISSUE_CLOSEOUT_INTENT_SCHEMA` stays `3` and no schema-5 closeout exists.
6. Shared-helper parity: every schema-4-bearing condition admits `5` — the
   authorization field set and its source-reference/binding-time validation, the
   exact asset-name closure, the operation natural-key grammar, the intent
   dispatch, the publication-plan schema selection and the validate-publication
   command dispatch — while schema 1/2/3/4 behavior and their fail-closed
   messages stay unchanged.
7. Contract mirrors: `agent-install.json#publication` records `intent_schema 5 /
   receipt_schema 5 / issue_closeout_intent_schema 3` and
   `.vibe/core/protocol.json` mirrors the same triple plus the registry digest.
8. Self-hosted install record: this repository's own `.vibe/manifest.json`
   advances `framework_version` and `source.ref` to `0.10.1`. Verified against a
   disposable `init --host codex,hermes` of the candidate: those two fields were
   the only differences, and the activation identity was already equal.
9. Documentation: `CHANGELOG.md` gains the 0.10.1 entry; `docs/releases/0.10.1.md`
   is the Release body and a payload file; both homepages are synchronized
   (latest-published link, adoption prompts, contract/protocol paragraph with
   publication schema 5, the `validate-release` example, the release-notes link
   and the limitations bullet); `AGENT_INSTALL.md`'s three version literals move
   with the framework version under the existing `ManagedGuideDriftTests` check;
   `.agents/skills/vibe-release/SKILL.md` presents the schema-5 profile;
   `docs/context/architecture.md` and `docs/context/product.md` record the
   v0.10.1 iteration facts including ADR0021.
10. Tests: the source-version pins in `test_v010_publication.py`,
    `test_workflow_contract.py`, `test_host_adapters.py` and
    `test_readiness_doc_gates.py` move with the identity; the schema-4 profile
    and closeout fixtures stay byte-exact; the new `tests/test_v011_publication.py`
    pins the closed schema-5 profile, its intent/receipt/authorization acceptance,
    its rejection matrix, the historical profiles' rejection of a v0.10.1
    candidate, the mirrored schemas and the published Hermes label, the release
    note's honesty, the absent schema-5 closeout, and the migration/bridge
    boundary.
11. Mirrors: the `rebuild-mirrors.py` skill script converged the activation
    identity, payload tree, manifest and Plugin mirrors (63 checks, none failed);
    re-running it leaves the identity stable; `doctor` is `healthy`.
12. Records and commits: this file, then the implementation commit, then the
    verification record after the independent run.

## Homepage review (reasoned record)

Both homepages were re-read end to end and synchronized for version, links,
installation commands, capabilities and limitations. Changed facts: the
latest-published line and its link, the two adoption prompts, the
contract/protocol paragraph (`publication schema 5 with a separate closeout
schema 3`), the `validate-release dist/vibe-kit-0.10.1` example, the release-notes
link and the selected-Pre-release limitations bullet — nine replacements per
language, identical facts in both. Reviewed and deliberately unchanged, with
reasons: the trust-contract section (the recognized repository and exact-tag
rules do not move), the takeover and manual-fallback wording (this release ships
no takeover or activation change), the upgrade/conflict section (no upgrade
semantics change beyond the advanced bound), and the logo/feature sections. The
Hermes `verified` statement was already present and correct from the label-raise
work item, so it needed no edit.

## Deferred by design (not skipped)

- No GitHub write: no push, tag, Release, asset upload or issue mutation happens
  in this work item. Publication is planned, validated and receipted by the CLI
  but executed only under a separate authorization bound to the frozen
  publication-intent digest.
- No issue closeout and no product change: #14 and #15 stay open tracked
  defects; the Codex five-stage refresh stays a delivered handoff.
- No stable promotion, signing, provenance or platform-immutability claim.

## Evidence at the freeze

Candidate commit at the implementation commit (working tree clean). Kit version
`0.10.1`; activation identity
`d418a177c0f9c1cf3f9d84256a6549986187050408859685e62a8e7ea68afd64`; payload tree
`b828663d3d056b9c3122fed8d686089e134fb758accd23f8e80b4302332d2b88`; migration
registry digest `7cedd9fbabd84ab1b51b029a5e679765a1e79efd2d09d5edaa42f9ccf2e47bd3`;
127 tests green on CPython 3.13.9 and 3.9.6 (118 before this work item, including
the 9 new schema-5 tests); `doctor` `healthy` with zero diagnostics and a matching
activation set; 63/63 mirrors equal a fresh recomputation;
`validate-readiness` `valid` for the brief. The prepublication AC-4 harness
(`.vibe/local/v0-10-1-gate/upgrade-scenarios.py`, host-side, gitignored) ran
40/40 checks: a recorded `0.10.0` install and a recorded `0.9.0` install each
upgraded into the candidate with project-owned bytes and the recorded host
selection preserved; fresh `codex`, `hermes` and combined installs were
doctor-healthy with the installed Hermes label reading `verified` and a
`hermes`-only install carrying no Codex payload; the
`v0.5.0-unmanaged-agent-contracts-v1` migration planned and applied under the
advanced target. Raw output:
`.vibe/local/v0-10-1-gate/upgrade-scenarios.out.txt`.