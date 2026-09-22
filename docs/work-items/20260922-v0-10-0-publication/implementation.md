# Implementation: Publish Vibe Kit v0.10.0

Plan, explicit before any edit (single writer, this work item). Frozen decisions: `docs/decisions/0020-v0-10-0-publication.md` (approved by the orchestrator as a distinct sequential-perspective Tech Lead reviewer on 2026-09-22, with one material review addendum). Readiness gate: `implementation-ready` before the first edit.

## Edit sequence (one change; mirrors last)

1. Version identity (`bin/vibe` head and the identity files): the framework version constant, `.vibe/core/version` and `.vibe/version` move `0.9.0 → 0.10.0`; `agent-install.json#kit_version` and the Plugin metadata follow in the same change.
2. Maintenance bridge: `maximum_installed_kit_version_exclusive` `0.9.0 → 0.10.0` while `minimum_installed_kit_version` stays `0.2.0` and `supported_installed_agent_protocols` keeps `[0, 1, 2, 3]`, so every install the v0.9.0 bridge admitted stays upgradeable.
3. Predecessor-migration registry: the target entry moves to `0.10.0`; `PREDECESSOR_MIGRATION_REGISTRY_SHA256` and its two mirrors (`.vibe/core/protocol.json#predecessor_migrations`, `agent-install.json#maintenance_bridge.predecessor_migrations`) are recomputed in the same change.
4. Publication profile: a new closed schema-4 profile for `v0.10.0` (annotated tag `v0.10.0`, Release title, body path `docs/releases/0.10.0.md`, exactly five assets, the six-operation allowlist, the issue policy for `[8, 9, 10, 11, 12, 13]`, the seven post criteria, the six evidence kinds and the eight public smokes); the schema-2 and schema-3 profile entries keep byte-exact semantics.
5. Closeout: a schema-3 issue-closeout graph for the v0.10.0 profile — six evidence comments plus six closes (twelve operations), each with a monotonic-resume precondition and a `v0.10.0` marker, dispatched from the parent publication intent's schema; `V100_CLOSEOUT_ISSUES` and the `validate_v100_*` helpers pin it.
6. Validators: `validate_publication_intent`, `validate_profile_intent`, the receipt/authorization validators and the closeout validator accept schema 4 with schema-3 closeout and refuse anything else with an actionable message; the helper parity the review addendum required is closed (the schema-4 path reuses the shared helper set rather than a private copy).
7. Contract mirrors: `agent-install.json#publication` records `intent_schema 4 / receipt_schema 4 / issue_closeout_intent_schema 3`; `.vibe/core/protocol.json` mirrors the same triple and the registry digest; the Plugin manifest drops the redundant `kit_version` key the review addendum flagged.
8. Documentation: `CHANGELOG.md` gains the 0.10.0 entry; `docs/releases/0.10.0.md` is the Release body and the payload file; both homepages are synchronized (version literals, the latest-published link, the upgrade commands, the contract/protocol sentences, the compatibility exception, the release-notes link) and the Codex-only verification claim becomes the per-host statement; `AGENT_INSTALL.md`'s three version literals move with the framework version; `docs/context/architecture.md` and `docs/context/product.md` record the v0.10.0 iteration facts.
9. Tests (`tests/`, standard-library `unittest`): the version pins in `test_workflow_contract.py`, `test_host_adapters.py` and `test_readiness_doc_gates.py` move with the identity; the new `tests/test_v010_publication.py` pins the closed schema-4 profile, its intent/receipt/authorization acceptance, the historical profiles' rejection of a v0.10.0 candidate, the twelve-operation closeout graph with its rejection matrix, the mirrored schemas and identity, the advanced bridge bound and registry digest, and the managed-guide drift check.
10. Mirrors: the `rebuild-mirrors.py` skill script converged the activation identity, payload tree, manifest and Plugin mirrors; `doctor` healthy; re-running the script leaves the identity stable (63 recorded checks equal a fresh recomputation).
11. Records and commits: this file, then the implementation commit, then the verification record after the independent run.

## Review addendum carried into the change

The orchestrator's review of the decision record found one material gap and two editorial notes, all closed here before the freeze:

- Helper parity: the schema-4 publication path originally duplicated the helper set; it now shares the canonical helpers, so a future profile cannot drift from the validators that judge it.
- The Plugin manifest carried a redundant `kit_version` key outside the closed contract shape; removed.
- The decision record's review line and the closeout-graph rationale were corrected to name the reviewer and the ordering rule exactly.

## Deferred by design (not skipped)

- No GitHub write: no push, tag, Release, asset upload or issue mutation happens in this work item. Publication and the #8–#13 closeout are planned, validated and receipted by the CLI but executed only under a separate authorization bound to the frozen publication-intent digest.
- No conformance-label raise: Hermes stays `supported-unverified`; the release notes claim no live reload or automatic successor handoff.
- No stable promotion: this is the non-draft Pre-release candidate only.

## Evidence at the freeze

Frozen candidate `ef5b9b57f87ffa4eca255966ef706cf23f670cfc` (working tree clean). Activation identity `7454b02243494b9f78fe8d48314d59a50ae828ef070b80c688aeb01b3185d14f`; payload tree `a6dcffe27d8ef9c7d61a70609412e9189a7f74279715aa5284f517f21c10e4fd`. 117 tests green on CPython 3.13.9 and 3.9.6 (107 before this work item); `doctor` healthy with zero diagnostics; `validate-readiness` valid; `inspect-managed-agents` valid; 63/63 mirrors equal a fresh recomputation; `package` plus `validate-release` valid with 36 payload files and no network use; two independent clean builds byte-identical across all five assets.
