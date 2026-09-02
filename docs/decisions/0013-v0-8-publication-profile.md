# 0013: Publish v0.8.0 through a closed schema-2 profile without Issue closeout

- Status: Accepted
- Date: 2026-09-02
- Decision owner: read-only Tech Lead author `/root/v08_release_tl_author`
- Review: approved by distinct read-only Tech Lead `/root/v08_release_tl_review`
  after two changes-required rounds; final approval 2026-09-02

## Context

ADR 0011 defines a safe host-owned publication transaction, but its persisted
schemas and implementation are deliberately exact to v0.7.0:

- intent and receipt schema 1 hard-code version/tag/release-note paths and asset
  names;
- the authorization set includes conditional Issue #1–#5 closeout;
- `issue_closeout_policy` requires those five Issues and a separate closeout
  transaction; and
- `publication-plan`, `validate-publication`, the release Skill, and tests
  enforce those exact values.

The accepted v0.8 work item requires the same exact-source, five-asset,
authorization, read-back, and recovery safety properties, but explicitly
excludes every Issue operation. Reinterpreting schema 1 to accept v0.8 or
encoding no-closeout through empty schema-1 values would weaken the historical
closed contract.

The current v0.8 worktree is not yet a releasable source identity. Publication
remains blocked until this decision is accepted and reviewed, implementation
lands, fresh release QA passes, and one exact clean commit is frozen.

## Decision

### ADR 0011 applicability

ADR 0011 continues to govern these shared invariants:

- exact selection, verified bytes, and platform-enforced immutability are
  distinct facts;
- packaging/publication remain offline-CLI plus host-owned-network components;
- publication binds one clean source commit, annotated-tag object, Release bytes,
  and exact five-asset closure;
- remote writes are read-before-write, CAS-bound, non-destructive, and read back;
- uncertain writes never receive an immediate retry;
- public verification and live-host evidence are required before a verified
  claim; and
- credentials, headers, environment values, raw host output, conversations, and
  hidden reasoning are excluded from durable evidence.

ADR 0011 remains the sole exact definition of v0.7 schema-1 publication and
Issue #1–#5 closeout. It is not rewritten or generalized in place.

### Closed publication profiles

Implementation uses a closed, compiled profile table with exactly two entries:

| Profile | Version | Intent/receipt | Issue behavior |
|---|---|---|---|
| Historical v0.7 | `0.7.0` | schema `1` / `1`; no persisted profile field | Existing exact #1–#5 closeout contract |
| v0.8 Pre-release | `0.8.0`, `v0.8.0` | schema `2` / `2`; profile `vibe-kit-v0.8.0-prerelease` | No Issue operation or closeout phase |

The table is an internal closed dispatch mechanism, not a generic SemVer
publisher, configuration file, or extension API. Unknown versions, profiles, or
schema/profile combinations fail closed. Future releases require an explicit
new profile or separately reviewed general publication contract.

Shared validation helpers may be reused, but every version-specific value comes
from the resolved exact profile rather than interpolation from untrusted input.

### v0.8 publication intent schema 2

Schema 2 retains the schema-1 publication fields and adds required:

```text
profile = vibe-kit-v0.8.0-prerelease
```

The profile fixes:

- repository `mintgao/vibe-kit`;
- version/tag `0.8.0` / annotated `v0.8.0`;
- release title `Vibe Kit v0.8.0`;
- release body path `docs/releases/0.8.0.md`;
- `draft=false`, `prerelease=true`, `generated_notes=false`;
- `platform_immutability_required=false`;
- the exact five v0.8 asset names and roles;
- the exact six-operation publication graph;
- required public smoke names; and
- no Issue-closeout branch.

The exact v0.8 `issue_closeout_policy` is:

```json
{
  "mode": "none",
  "issues": [],
  "allowed_operations": []
}
```

No schema-1 closeout booleans are reused with empty values. Schema 2 rejects any
non-empty Issue list, Issue operation, separate-closeout requirement, or
closeout authorization.

The exact authorization and intent operation set is:

```text
fast-forward-main
create-or-confirm-annotated-tag
create-or-confirm-prerelease
upload-or-confirm-five-assets
read-back-publication
download-and-verify-public-assets
```

It contains no conditional Issue operation. `publication-plan --phase
issue-closeout` remains a v0.7/schema-1-only interface and cannot be selected by
the v0.8 Skill branch.

### Closed remote snapshot and operation preconditions

Schema-2 `remote_snapshot` has exactly `observed_at`, `main`, `tag`, `release`,
`asset_list_complete`, and `assets`. Every object is closed with
`additionalProperties:false`.

```text
main: branch, observed_oid
tag: state, ref_oid, object_type, tag_object_oid, peeled_commit,
     tagger_name, tagger_email, tagger_timestamp, tagger_timezone,
     message_sha256
release: state, id, url, tag, title, body_sha256, draft, prerelease,
         immutable
asset item: id, name, size, sha256, download_url
```

`main.branch=main`; `observed_oid` is lowercase 40-hex and equals either the
intent's expected-old OID or target OID. Tag and Release state is
`absent|present`. Every tag field after `state` is null iff absent; a present tag
is annotated and its complete identity equals the intent. Every Release field
after `state` is null iff absent; a present Release has a positive ID, canonical
URL, LF-normalized body digest, and `immutable=true|false|unknown`.

`asset_list_complete=true` asserts that all GitHub pagination completed.
`assets` is the complete Release asset list, sorted by UTF-8 name bytes then
numeric ID so duplicates remain representable and rejectable. Every listed
asset has a positive ID, safe name, non-negative size, canonical public URL, and
non-null SHA-256 obtained by public download. An unavailable or unhashable
existing asset blocks planning. An absent Release requires `assets=[]`. Extra,
duplicate, or divergent assets block before an executable intent digest exists.

Schema 2 adds required top-level `remote_snapshot_sha256`, the SHA-256 of UTF-8
canonical JSON of `remote_snapshot` with sorted keys, no ASCII escaping, and
separators `(",", ":")`; arrays retain contract order.

Every high-level operation precondition contains exactly `kind`,
`remote_snapshot_sha256`, and `identity_sha256`. The snapshot digest equals the
top-level value. `identity_sha256` hashes canonical JSON containing the schema,
profile, operation kind, natural key, snapshot digest, and that operation's exact
initial observed object. Any snapshot or precondition change invalidates the
intent and authorization.

### Closed operation receipt ledgers

The authorization still exposes exactly six high-level operation kinds.
Schema-2 receipt top-level `operations` contains exactly six high-level receipts
in intent order. Every high-level operation receipt has exactly:

```text
sequence
operation_id
kind
natural_key
precondition_sha256
initial_observation
attempts
final_observation
outcome
remote_object_id
asset_receipts
error
```

Outcome is exactly one of:

```text
not-attempted | read-matched | updated | created | uploaded |
confirmed-after-uncertain | verified | conflict | permission-denied |
definite-failure | absent-after-bounded-retry | uncertain | error
```

Successful terminal outcomes are `read-matched|updated|created|uploaded|
confirmed-after-uncertain|verified`. `error` is null only for a successful
terminal outcome; all other outcomes carry exactly non-empty bounded `code`,
`message`, and `next_action`.

Main, tag, and Release operations require non-null initial/final observations,
zero to two attempts, and `asset_receipts=[]`. Upload requires null high-level
observations, `attempts=[]`, and exactly five asset receipts. Read-back and
download operations require null observations, no attempts, empty asset
receipts, and outcome `verified`, `not-attempted`, or `error`.

Every write attempt contains exactly:

```text
attempt_number
pre_write_observation
response
read_back_observation
```

Response is `definite-success|timeout|transport-unknown|permission-denied|
definite-failure|execution-error`. Attempt numbers are consecutive from one.
Every attempt has a fresh read before the write and a read after its response.
Attempt two is permitted only when attempt one's read-back is the kind-specific
positive-absence state: main `preimage`, or tag, Release, and asset `absent`.
Permission denial, definite failure, execution error, divergence, or unknown
state never permits attempt two.

A main observation has exactly `observed_at`, `state`, and `oid`; state is
`preimage|target|divergent|unknown`, and OID is null iff unknown. Target yields
`read-matched`, `updated`, or `confirmed-after-uncertain`; preimage after attempt
two yields `absent-after-bounded-retry`.

A tag observation has exactly:

```text
observed_at, state, ref_oid, object_type, tag_object_oid, peeled_commit,
tagger_name, tagger_email, tagger_timestamp, tagger_timezone, message_sha256
```

State is `absent|match|divergent|unknown`. All identity fields are null for
absent/unknown and complete for match/divergent. Match yields `read-matched`,
`created`, or `confirmed-after-uncertain`.

A Release observation has exactly:

```text
observed_at, state, id, url, tag, title, body_sha256, draft, prerelease,
immutable
```

State is `absent|match|divergent|unknown`. All remote fields are null for
absent/unknown and complete for match/divergent. Match yields `read-matched`,
`created`, or `confirmed-after-uncertain`.

`upload-or-confirm-five-assets` remains one authorization boundary, not one
aggregate write. Its schema-2 intent operation contains `asset_operations`,
exactly five children sorted by UTF-8 asset name; every other high-level intent
operation has `asset_operations=[]`. Each asset child has exactly:

```text
sequence, operation_id, natural_key, name, role, size, sha256,
expected_precondition, max_write_attempts = 2
```

The natural key is
`mintgao/vibe-kit:release:v0.8.0:asset:<exact-name>`. The child precondition
canonically binds the parent operation, complete snapshot digest, intended asset
identity, and the matching initial remote item or canonical absent observation.

Intent asset children exist only in `operations[3].asset_operations`; receipt
asset ledgers exist only in `operations[3].asset_receipts`. The receipt's
top-level `assets` remains the final exact five public asset identities and is
not an attempt ledger.

Each item in `operations[3].asset_receipts` has exactly:

```text
sequence, operation_id, natural_key, name, role, expected_size,
expected_sha256, precondition_sha256, initial_observation, attempts,
final_observation, outcome, remote_asset_id, error
```

An asset observation has exactly `observed_at`, `state`, `id`, `size`, `sha256`,
and `download_url`. State is `absent|match|divergent|unknown`; remote fields are
null for absent/unknown and complete for match/divergent. Asset outcomes use the
complete high-level enum, but valid asset successes are only
`read-matched|uploaded|confirmed-after-uncertain`. Later children after a stop
are present with `not-attempted` and an upstream-stop error.

The high-level upload outcome is derived: all five successful children yield
`uploaded`, `read-matched`, or `confirmed-after-uncertain` according to the child
outcomes; any conflict, permission, failure, absence, unknown, or error yields
the corresponding first non-terminal outcome; later children remain
`not-attempted`. The same attempt-ledger rules apply uniformly to main, tag,
Release, and every asset natural key, proving positive absence before a second
write. Resume uses the same intent, authorization, and host operation ID,
rereads every natural key, reuses terminal matches, and starts at the first
non-terminal child without duplicate upload.

### Structural v0.7 closeout-parent isolation

The historical command invocation and request field shape remain unchanged:

```text
publication-plan --phase issue-closeout --request <json>
```

No `--parent-intent` argument is added. The current v0.8 CLI's compiled
historical profile contains the exact published v0.7 parent anchor:

```text
schema_version = 1
repository = mintgao/vibe-kit
version = 0.7.0
publication_intent_sha256 =
  1914fe1761cae16224a94e6f96c9dd71ecff9f2a4179848295ece1cef418a175
```

After unchanged schema-1 closeout request validation, planning requires its
`parent_publication_intent_sha256` to equal that exact anchor. A schema-2/v0.8
intent digest cannot pass absent a SHA-256 collision.

This intentionally narrows the current v0.8 CLI from accepting arbitrary
synthetic 64-hex v0.7 parent digests to the one actually published v0.7 parent.
The tagged v0.7 CLI, command invocation, actual historical request, markers,
closeout intent, and authorization remain unchanged. Synthetic fixture tests
use the pinned parent or test child-shape helpers directly. This narrowing is
authorized by AC-10's exact historical preservation and cross-profile rejection
requirement; it introduces no new user-visible publication capability.

### Two-phase evidence and exact prepublication receipts

Publication has two evidence phases. `prepublication-ready` proves the exact
source, tooling, and candidates are safe to authorize.
`postpublication-accepted` proves live public acceptance after publication. A
prepublication receipt never claims that live criteria passed.

The independent prepublication QA receipt contains AC-1 through AC-12 in numeric
order with this exact mapping:

| Criterion | Required prepublication state |
|---|---|
| AC-1 | `passed` |
| AC-2 | `tooling-pass-live-pending` |
| AC-3 | `passed` |
| AC-4 | `not-runnable-before-publication` |
| AC-5 | `tooling-pass-live-pending` |
| AC-6 | `tooling-pass-live-pending` |
| AC-7 | `tooling-pass-live-pending` |
| AC-8 | `tooling-pass-live-pending` |
| AC-9 | `not-runnable-before-publication` |
| AC-10 | `passed` |
| AC-11 | `tooling-pass-live-pending` |
| AC-12 | `not-runnable-before-publication` |

`passed` means wholly decidable locally. `tooling-pass-live-pending` means the
local contract/scenarios passed but live execution remains pending.
`not-runnable-before-publication` is not a pass. The prepublication gate accepts
only this exact mapping plus successful local receipts and a safe final plan; it
never derives final product acceptance. Only a later postpublication receipt may
map all criteria to passed and permit “published and verified.”

Every canonical command item has exactly:

```text
sequence, command_id, argv, exit_code, status, result, result_sha256
```

`argv` is a non-empty string array using `$SOURCE`, `$CANDIDATE_A`, and
`$CANDIDATE_B` aliases instead of local absolute paths. Status is
`passed|failed|blocked|error`. `result` has exactly `status`, `passed_count`,
`failed_count`, and `skipped_count`; counts are non-negative integers and
`result_sha256` is the canonical SHA-256 of this exact object. `exit_code` is an
integer when a process started and null only for blocked/error before start.
Passed requires exit code zero, result status passed, and failed count zero.
Every receipt's `error` is null when passed; otherwise it contains exactly
non-empty bounded `code`, `message`, and `next_action`.

The QA receipt has exactly:

```text
schema_version = 1
kind = vibe-kit-v0.8-prepublication-qa
execution_id
executor_role = independent-qa
started_at
finished_at
repository = mintgao/vibe-kit
version = 0.8.0
profile = vibe-kit-v0.8.0-prerelease
source_commit
source_tree_oid
asset_set_sha256
commands
criterion_mapping
status
error
```

Each criterion item has exactly `criterion_id`, `state`,
`evidence_command_sequences`, and `postpublication_requirement`.
`criterion_id` is AC-1 through AC-12 in order. State is
`passed|tooling-pass-live-pending|not-runnable-before-publication|failed|
blocked`. Evidence sequences are ordered, unique command references and may be
empty only for `not-runnable-before-publication`. Postpublication requirement is
`none|live-read-back|public-download|public-smoke|
offline-publication-validation|final-claim-gate`. QA status is passed only when
all commands pass and the exact required mapping exists; it does not mean all
product criteria passed.

The configured-check receipt has exactly:

```text
schema_version = 1
kind = vibe-kit-v0.8-configured-checks
execution_id
executor_role
started_at
finished_at
repository
version
profile
source_commit
source_tree_oid
commands
checks
status
error
```

`commands` contains exactly one canonical `./bin/vibe verify . --format json`
command item. `checks` contains exactly `lint`, `typecheck`, `test`, and `build`
in that order. Each item has exactly `name`, `configured`, `status`, `exit_code`,
and `result_sha256`. Status is
`passed|failed|not-configured|blocked|error`. `configured=false` requires
`not-configured` and null exit/result digest. Configured checks require a
non-null exit code and result digest unless blocked before start. Overall passed
requires every configured check passed and every unconfigured check explicitly
`not-configured`.

The Python receipt has exactly:

```text
schema_version = 1
kind = vibe-kit-v0.8-python-3.9
execution_id
executor_role
started_at
finished_at
repository
version
profile
source_commit
source_tree_oid
interpreter
commands
status
error
```

`interpreter` has exactly `implementation=CPython`, `major=3`, `minor=9`,
`patch`, `platform`, and `executable_name`; patch is non-negative and the final
two values are sanitized non-empty strings. Commands contain exactly, in order:

```text
python39-default-verify
python39-publication-focused-tests
python39-package-a
python39-validate-release-a
python39-package-b
python39-validate-release-b
```

All must pass. The final plan and final `validate-publication` result envelopes
separately record their actual CPython 3.9 execution identity and time.

Each clean-build receipt has exactly:

```text
schema_version = 1
kind = vibe-kit-v0.8-clean-build
execution_id
executor_role = release-build-host
started_at
finished_at
repository
version
profile
source_commit
source_tree_oid
build_id
checkout_id
output_id
source_clean
interpreter
package_command
assets
asset_set_sha256
validate_release_command
validate_release_result_sha256
status
error
```

`build_id` is exactly A or B; interpreter has the exact Python fields above;
`source_clean=true`; package and validate commands use the complete canonical
command schema. `assets` contains exactly five UTF-8-name-sorted items, each
with exactly `name`, `role`, `size`, and `sha256`, with one role each of
checksum, manifest, direct, distribution, and plugin. A and B require distinct
execution, checkout, and output IDs; identical source commit/tree and exact
asset items; equal asset-set digests; and separately valid validation results.

The release-gate bundle has exactly:

```text
schema_version = 1
kind = vibe-kit-v0.8-release-gate-evidence
repository
version
profile
source_commit
source_tree_oid
generated_at
qa
configured_checks
python_3_9
builds
receipt_sha256s
```

`builds` is exactly `[A,B]`. `receipt_sha256s` has exactly `qa`,
`configured_checks`, `python_3_9`, `build_a`, and `build_b`; each digest is
recomputed over the corresponding complete child receipt, which contains no
self-digest. Schema-2 `local_gates.release_gate_evidence_sha256` hashes the
complete bundle. Every digest therefore has a closed persisted preimage.

All objects are closed; times are ISO-8601 with finish not before start; every
receipt binds the same exact repository, profile, source commit, and tree.
`publication-plan` validates the bundle, recomputes every child digest, confirms
identities and results, computes both candidates directly, and rejects mismatch.
It requires the canonical candidate and a distinct comparison candidate,
verifies both are clean 0.8.0 prerelease builds from the same source, computes
both five-asset sets, requires byte identity, and validates each candidate.
Independent QA remains the authenticity owner.

After offline `validate-publication` succeeds, independent QA creates a separate
postpublication acceptance receipt with exactly:

```text
schema_version = 1
kind = vibe-kit-v0.8-postpublication-acceptance
execution_id
executor_role = independent-qa
started_at
finished_at
repository
version
profile
source_commit
source_tree_oid
publication_intent_sha256
authorization_id
host_operation_id
validate_publication_result_sha256
criteria
status
error
```

`criteria` contains AC-1 through AC-12 in order. Each item has exactly
`criterion_id`, `state`, and `evidence_refs`; state is
`passed|failed|blocked`. Each evidence reference has exactly `kind` and
`sha256`, where kind is `local-gate-receipt|publication-receipt|live-read-back|
public-download|public-smoke|validate-publication`. Final status is passed only
when all twelve criteria pass. This receipt is produced after validation and
does not participate in or create a validation digest cycle.

Release-specific full verification and publication scenarios run on actual
Python 3.9. This is a valid specialized rerun under ADR 0012 because publication
tooling changes the candidate and the release gate independently requires it.

### Five-asset closure

Release-manifest schema 2 and ADR 0011's non-self-referential closure remain.
The exact public set is:

```text
SHA256SUMS
release-manifest.json
vibe-kit-0.8.0.zip
vibe-kit-distribution-0.8.0.zip
vibe-kit-plugin-0.8.0.zip
```

There is exactly one role each: checksum, manifest, direct, distribution, and
plugin. The canonical sorted array of name, role, size, and SHA-256 produces
`asset_set_sha256`.

For v0.8, `SHA256SUMS` covers exactly:

```text
release-manifest.json
vibe-kit-0.8.0.zip
vibe-kit-plugin-0.8.0.zip
marketplace/marketplace.json
marketplace/plugins/vibe-kit/**  # every packaged allowlisted regular file
```

The recursive marketplace set includes the generated v0.8 Plugin descriptor,
packaged Skill files, and `payload/<every canonical managed-source file>` from
the expanded marketplace build. Every covered regular file appears exactly once
as a safe POSIX relative path; directories and symlinks are forbidden. Lines are
lowercase 64-hex, two ASCII spaces, relative path, and LF, sorted by UTF-8 path
bytes. `SHA256SUMS` does not cover itself, the distribution ZIP is excluded, and
no member is added through an implicit outer-artifact wildcard.

The distribution archive contains exactly
`vibe-kit-0.8.0/SHA256SUMS` plus
`vibe-kit-0.8.0/<every exact SHA256SUMS-covered path>`. It never contains itself.
The publication intent is the sole outer closure over all five public assets.
Missing, extra, duplicate, unsafe, or divergent content blocks.

### Source, main, and annotated-tag identity

The release source commit `C` is a full-length clean commit containing:

- the Accepted decision and review/gate evidence;
- v0.8 publication implementation and tests;
- exact release-note bytes;
- the implementation report and pre-final-QA status; and
- no unrelated or secret material.

`C` does not contain the final exact-commit QA receipt, public verification, or
future publication evidence. Final QA runs from a clean checkout of exact `C`
and retains the canonical release-gate evidence bundle outside that checkout.
Release candidates are also outside the checkout.

There is no tracked evidence-only exception before publication. Any tracked
change after `C` invalidates final QA, configured checks, Python 3.9 checks, both
builds, the remote snapshot, publication intent, and authorization. External
evidence is non-candidate state only because it is not tracked and every receipt
is bound to the exact commit and tree by canonical digest.

The initial remote snapshot binds `main`'s expected-old OID. The target OID
equals the source commit. The host verifies ancestry and advances `main` only
through expected-old-OID fast-forward CAS. A changed preimage blocks and
requires a new snapshot, intent, and authorization.

The annotated tag object is precomputed without creating the remote ref. Its
target commit, tagger name/email/time/timezone, exact message SHA-256, and
resulting Git object OID are frozen in the intent. Existing tag state is reusable
only when the ref OID, annotated object, and peeled commit all match.

The Release body is the exact LF-preserved bytes of `docs/releases/0.8.0.md`
from the source commit. Existing Release state is reusable only on exact tag,
title, body hash, draft/prerelease, and generated-notes parity.

### Exact executable authorization

The current publication request authorizes preparation, not an unfrozen GitHub
mutation.

After the two builds and remote snapshot are frozen, `publication-plan` emits
canonical schema-2 intent JSON and its SHA-256. Before any remote write, the user
must approve an executable record binding exactly:

```text
authorization_id
repository = mintgao/vibe-kit
version = 0.8.0
release_kind = prerelease
allowed_operations = exact six-operation set
publication_intent_sha256
host_operation_id
```

The same `host_operation_id` is retained across read-back and same-intent
recovery. Any change to commit, snapshot, tag object, Release bytes/state, asset
set, operation set, or recovery policy invalidates authorization.

For schema 2, `validate-publication` also receives the sanitized authorization
record and checks its structural equality with the intent and receipt. This
proves binding, not that the host genuinely obtained user consent.

### Remote reconciliation and recovery

Before each write, the host rereads the natural-key state. Existing exact state
is reused. Divergent, extra, or duplicate state blocks before mutation.

After every response, including permission denial, definite failure, and
execution error, the host performs exact read-back and records the closed
attempt ledger. Classification remains:

```text
match              -> confirmed; no retry
divergent          -> conflict; no retry
positively-absent  -> at most one retry, then mandatory read-back
still-unknown      -> uncertain; no retry
permission-denied  -> stop; no retry
definite-failure   -> stop; no retry
execution-error    -> stop; no retry
```

After the second write attempt, positive absence becomes
`absent-after-bounded-retry` and `confirmed-partial`; there is no third attempt.

Recovery reuses only the same intent, authorization, and host operation ID. It
rereads all relevant state and resumes from the first non-terminal operation.
Changed bound state requires a new intent and authorization.

No recovery path force-pushes, moves a tag, rewrites a Release,
replaces/deletes an asset, or performs an Issue operation. Partial public state
remains public. A published but unverified release is reported only as
`published-unverified`.

### Receipt schema 2 and public verification

Receipt schema 2 adds exact `profile` and `version` fields.
`issue_closeout` is required to be `null`; any Issue or closeout claim is
invalid.

The required smoke set is closed and contains exactly:

```text
public-direct-init-doctor
public-plugin-bundled-plan-init-doctor
public-upgrade-v0.3-to-v0.8
public-upgrade-v0.5-to-v0.8
public-upgrade-v0.6-to-v0.8
public-upgrade-v0.7-to-v0.8
```

Completion requires:

- authenticated live main/tag/Release/complete-asset-list read-back;
- five canonical unauthenticated public downloads matching sizes and SHA-256;
- exact nested distribution/checksum validation;
- valid target `validate-release`;
- all exact smokes passed;
- exact terminal operation receipts;
- `remote_write_state=confirmed-complete`;
- `verification_state=passed`;
- no receipt error; and
- offline `validate-publication` success.

The offline validator reports `host_evidence_authenticated=false`. Structural
validity never substitutes for retained live GitHub evidence.

GitHub's live `immutable` value is recorded as `true`, `false`, or `unknown`.
False or unknown does not fail v0.8 because platform immutability is not
promised. No tag, digest, or Release URL is described as a publisher signature,
provenance attestation, or platform immutability guarantee.

### Release evidence commit

The annotated tag continues to point to the frozen source commit. It is never
amended to include facts that exist only after publication.

After public verification, the orchestrator persists only sanitized public
facts, hashes, receipt/authorization identifiers, limitations, and criterion
mappings in the work-item evidence, then creates a descendant publication-
evidence commit. It does not amend or retag the source commit.

Publication explicitly does not authorize pushing this causally later commit.
Remote `main` ends at `C`, and the six-operation publication intent contains no
second main update. The final report records the release source as `C`, remote
`main` as `C`, the local evidence commit as its OID or `none`, and
`evidence_pushed=false`. Pushing an evidence commit is a new, separately shaped
exact-CAS task outside this decision and cannot reuse the publication intent.

## Alternatives considered

- Extend schema 1 with v0.8 values: rejected because it changes a historically
  exact closed schema.
- Encode no closeout as empty schema-1 Issues and false prerequisites: rejected
  because false can mean ungated rather than forbidden.
- Duplicate a separate v0.8 implementation: rejected because authorization,
  read-back, and recovery behavior would drift.
- Create a generic configurable SemVer publisher: rejected because it expands
  compatibility and trust scope beyond one release.
- Reuse the current user request as executable authorization: rejected because
  no exact intent digest exists yet.
- Include live publication evidence in the tagged source commit: impossible
  without circular or fabricated evidence.
- Amend or move the tag after evidence exists: rejected as destructive identity
  rewriting.
- Roll back partial GitHub state by delete/replace/force: rejected because
  recovery is monotonic and non-destructive.

## Consequences

- v0.7 schema-1 publication, closeout markers, receipts, Skill semantics, and
  historical evidence remain exact.
- v0.8 has an unambiguous no-Issue contract and smaller authorization set.
- Publication intent and receipt schemas advance to 2.
- Profile dispatch and dual-candidate validation add implementation/test surface.
- Existing v0.8 candidate QA becomes stale after publication tooling changes;
  fresh release QA is mandatory.
- Future versions are not implicitly supported.
- GitHub credentials and authenticity remain host responsibilities.
- Public state may remain partial or published-unverified after external
  failure; automatic destructive cleanup remains unavailable.

## Compatibility and versioning

| Contract | Value |
|---|---:|
| Kit | `0.8.0` |
| Core protocol | `6` unchanged |
| Codex adapter protocol | `6` unchanged |
| Publication intent schema | `2` |
| Publication receipt schema | `2` |
| Issue closeout intent schema | `1`, v0.7-only |
| Release manifest schema | `2` unchanged |
| CLI result schema | `2` unchanged |
| Agent-install schema/protocol | `3` / `3` unchanged |
| Takeover schema | `2` unchanged |
| Maintenance bridge schema | `2` unchanged |
| Transaction journal/commit schemas | `1` / `1` unchanged |

Current compiled and packaged protocol mirrors declare publication schemas 2.
The v0.8 CLI retains explicit historical schema-1 validation. Older consumers
fail closed on schema 2.

No core/Codex protocol bump is needed: protocol 6 remains the accepted v0.8
managed-workflow generation, while separately versioned publication schemas
carry the changed outer contract.

## Rollback and recovery

Before remote writes, rollback is Git revert plus deletion/rebuild of disposable
candidates.

After `main` advances, source correction uses a new descendant or revert commit;
never force-reset remote history.

After tag, Release, or asset creation, recovery is same-intent reconciliation
only. Divergent or uncertain state blocks. Public objects are not automatically
removed or rewritten.

A faulty publication-evidence commit is corrected by a new descendant. The
release tag and assets remain bound to the original source commit.

## Verification

Required evidence includes:

- exact v0.7 schema-1 plan/receipt/closeout regression tests;
- prepublication QA rejection when AC-4, AC-9, or AC-12 is marked passed;
- proof that AC-2/5/6/7/8/11 pending states cannot become final acceptance,
  and only a later twelve-pass postpublication receipt permits the final claim;
- missing/extra child fields, wrong order, invalid nullability, unknown enums,
  and digest/preimage mismatch rejection for every exact receipt shape;
- configured/not-configured exit-code and result-digest nullability tests;
- distinct A/B execution, checkout, and output identity tests;
- complete remote-snapshot pagination, closed nullability, canonical snapshot
  hashing, and per-operation precondition-digest tests;
- extra, duplicate, divergent, incomplete, and unhashable remote-asset cases;
- proof that top-level `assets`, upload `asset_operations`, and upload
  `asset_receipts` cannot substitute for one another;
- five ordered per-asset ledgers, partial-stop, and same-intent resume tests;
- rejection of main, tag, Release, and asset second attempts unless attempt-one
  read-back is the exact kind-specific positive-absence state;
- complete not-attempted, permission, definite-failure, execution-error,
  uncertain, conflict, and bounded-absence one-next-action evidence;
- acceptance of the original v0.7 closeout invocation/request only with the
  pinned historical parent, and rejection of arbitrary schema-1 and every
  schema-2/v0.8 parent digest;
- v0.7 archive/Skill/release-note/marker preservation;
- valid v0.8 schema-2 plan and receipt;
- cross-profile/schema/version rejection in both directions;
- rejection of every v0.8 Issue field or operation;
- exact five-asset and profile-specific name/role validation;
- malformed, cross-commit, duplicate-execution, non-CPython-3.9, and mismatched
  release-gate evidence rejection;
- invalidation after every tracked post-QA change;
- exact checksum line grammar, covered-path set, and distribution member set;
- dirty source, wrong commit, wrong note, A/B mismatch, and either-candidate
  validation failure;
- authorization/intent/receipt mismatch and digest invalidation;
- tag/Release/asset absent, exact, divergent, duplicate, and extra-state cases;
- timeout, bounded retry, permission, and still-unknown receipt branches;
- exact public download, nested checksum, and smoke-set validation;
- `immutable=true|false|unknown` honesty cases;
- network-disabled and credential-redaction tests;
- actual Python 3.9 configured checks, two clean builds, and dual validation;
- independent public main/tag/Release/assets/download/smoke verification; and
- evidence-commit ancestry, absence of an evidence-push publication operation,
  and explicit `evidence_pushed=false` reporting.

## Open decisions

None. The future exact publication authorization is a runtime gate, not an
unresolved architecture/product choice. Evidence-commit push is outside this
publication task and decision.
