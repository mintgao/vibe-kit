# Exact v0.13.0 publication contract

- Status: Accepted specification; runtime acceptance and publication remain unverified
- Scope: publication of the accepted four-module 0.13 feature candidate
- Source acceptance: original N01–N36 remains mandatory; this document adds release criteria only

## Exact identities and unchanged versions

Publication intent schema 8 and publication receipt schema 8 select exactly:

| Field | Value |
|---|---|
| repository | mintgao/vibe-kit |
| version | 0.13.0 |
| profile | vibe-kit-v0.13.0-prerelease |
| tag | v0.13.0 |
| title | Vibe Kit v0.13.0 |
| body_path | docs/releases/0.13.0.md |
| direct | vibe-kit-0.13.0.zip |
| distribution | vibe-kit-distribution-0.13.0.zip |
| plugin | vibe-kit-plugin-0.13.0.zip |

Release fields: draft=false, prerelease=true, generated_notes=false, platform_immutability_required=false. Exact integer schema 8 is required; bool, float, string, unknown and cross-profile inputs fail closed.

Publication mirror values are 8/8/5: closeout schema remains 5. Preserve kit/Plugin 0.13.0, Agent-install schema/protocol 4/5, core/Codex 7/7, Hermes 1, takeover 2, CLI result 2, inspection 1, execution 1, release manifest 2, maintenance bridge/migration registry 2, transaction journal/commit 1/1, installed manifest/onboarding 1 and feedback 2.

Historical publication 1–7 and closeout 1–5 retain their existing exact semantics. Schema 7 remains exclusively 0.12.0; closeout 5 remains exclusively its historical parent. No new closeout profile or schema-8 closeout dispatch is permitted.

## Assets and six-operation graph

Exactly five assets, sorted by UTF-8 name bytes:

| Name | Role |
|---|---|
| SHA256SUMS | checksum |
| release-manifest.json | manifest |
| vibe-kit-0.13.0.zip | direct |
| vibe-kit-distribution-0.13.0.zip | distribution |
| vibe-kit-plugin-0.13.0.zip | plugin |

The ordered publication operations and natural keys are:

| ID | Kind | Natural key |
|---|---|---|
| publish-0 | fast-forward-main | mintgao/vibe-kit:main |
| publish-1 | create-or-confirm-annotated-tag | mintgao/vibe-kit:tag:v0.13.0 |
| publish-2 | create-or-confirm-prerelease | mintgao/vibe-kit:release:v0.13.0 |
| publish-3 | upload-or-confirm-five-assets | mintgao/vibe-kit:release:v0.13.0:assets |
| publish-4 | read-back-publication | mintgao/vibe-kit:publication:v0.13.0:read-back |
| publish-5 | download-and-verify-public-assets | mintgao/vibe-kit:release:v0.13.0:public-assets |

asset-0 through asset-4 follow the exact asset order with natural keys mintgao/vibe-kit:release:v0.13.0:asset:<exact-name>. Inherit all closed field sets, canonical precondition hashes and child ledgers. Write operations allow at most two attempts; read-only operations have zero. After merge, main equals M and publish-0 is read-matched without a write. Drift blocks.

Issue policy is exactly {"mode":"none","issues":[],"allowed_operations":[]}; publication receipt issue_closeout is null. Issue comments and closes are neither a publication operation nor an implied later phase.

## Acceptance and local receipt kinds

The ordered criterion lists contain AC-1 through AC-10, with meanings defined in brief.md. Prepublication states are eight passed followed by two not-runnable-before-publication. Requirements are eight none values, then live-read-back for AC-9 and public-smoke for AC-10. post_criteria contains exactly ordered AC-1 through AC-10, all passed for completion.

The local receipt schemas remain 1, retaining existing closed fields:

| Kind | Exact receipt kind |
|---|---|
| prepublication-qa | vibe-kit-v0.13.0-prepublication-qa |
| configured-checks | vibe-kit-v0.13.0-configured-checks |
| python-3.9 | vibe-kit-v0.13.0-python-3.9 |
| clean-build | vibe-kit-v0.13.0-clean-build |
| release-gate-evidence | vibe-kit-v0.13.0-release-gate-evidence |
| postpublication-acceptance | vibe-kit-v0.13.0-postpublication-acceptance |

Prepublication QA is constructed after actual M gates pass. Preserve the real source and execution identity for every receipt. QA evaluates the full product evidence and its target applicability; criterion mappings and hashes alone do not prove host execution. Do not add project-upgrade or issue-closeout requirements to schema 8.

## Closed public smoke set

Exactly twenty ordered names:

```text
public-direct-init-doctor
public-plugin-bundled-plan-init-doctor
public-upgrade-v0.3-to-v0.13.0
public-upgrade-v0.5-to-v0.13.0
public-upgrade-v0.6-to-v0.13.0
public-upgrade-v0.7-to-v0.13.0
public-upgrade-v0.8-to-v0.13.0
public-upgrade-v0.9-to-v0.13.0
public-upgrade-v0.10.0-to-v0.13.0
public-upgrade-v0.10.1-to-v0.13.0
public-upgrade-v0.11.0-to-v0.13.0
public-upgrade-v0.12.0-to-v0.13.0
public-repeat-upgrade-v0.13.0
public-onboarding-exact-integer-entrypoints
public-focused-entry-evidence-python-node
public-inspect-run-evidence-separation
public-inspect-run-interruption-readonly
public-inspect-run-wrong-run-isolation
public-extension-contract-templates-python-node
public-upgrade-compatibility-readonly-python-node
```

Every target invocation uses freshly downloaded, hash-validated 0.13 public bytes. Direct/Plugin tests perform real plan, install and installed doctor. Each predecessor starts from authenticated official public assets with a healthy known installation, preserves project ownership/host selection and commits target without active transaction residue. The existing public 0.12 release supplies that predecessor; missing, changed or unverifiable source blocks rather than triggering a historical re-release. Repeat performs two actual same-version upgrades.

Retain ADR0024's substantive onboarding, actual Python/Node entry wiring and three inspect-run scenarios: exact integer rejection, preserved assertions, independently meaningful receipt/run evidence, read-only interruption and genuinely distinct wrong-run isolation. Retain origin not-attested, applicability unproven and liveness not-assessed. Skipped Node or static string checks cannot pass actual execution requirements.

The template smoke executes the shipped real Python discovery and Node package-script dispatchers against the production validator. Include complete/default and partial controls, missing-check with consistent-summary rejection, a separate summary counterexample, stale origin/wrong argument, legal output-semantic versus invalid integrity variants and absent/generated doctor lifecycle. No relaxed helper or stub runtime is accepted.

The compatibility smoke exercises authenticated direct and Plugin bundled payload entrypoints, with the Plugin preflight calling the bundled CLI directly and proving the old wrapper was not invoked. Cover missing/disabled declarations, exact allowed/rejected target identities, malformed and reserved-unsupported rules, binding/source-drift negatives and zero writes during the complete read-only call. Preserve original install-plan conflicts separately and source_authentication=not-attested. An identity mismatch is not proof of API incompatibility.

F3/F4 are shipped guidance and host-owned behavior, not new aggregate CLI commands. Product N01–N36 includes their genuine final-target host scenarios before publication. Public package/activation identity and installed-contract checks prove the shipped bytes; neither these checks nor the public smokes fabricate a new host activation or replace those live criteria.

## Authorization, persistence and completion

Reuse existing publication authorization fields including authorization_source_ref and bound_at, bound to exact repository/version/six-operation intent and one host operation. Do not include private host data in public summaries. The offline CLI authenticates neither consent, GitHub state, host execution nor current applicability.

Read complete remote state before planning; read before each natural-key write and after every response. Unknown is not absence. A second eligible write requires positive absence and unchanged applicable precondition; denial, definite execution failure, divergence or still-unknown state stops that operation. Never force, delete, replace, promote stable or move a tag.

Final validation requires fresh public downloads of all five assets, nested checksum/distribution validation, downloaded-target validate-release, all twenty smokes, and actual CPython 3.9 validate-publication. Receipt input is read-only; optional result persistence is distinct and create-only. Independent later acceptance binds the actual result and requires ten passes. Only then record observed publication facts in E; no tag/body/asset rewrite or issue operation follows.
