# 0011: Separate exact-source trust from platform immutability and orchestrate publication at the Agent/host boundary

- Status: Accepted
- Date: 2026-08-31
- Decision owner: read-only Tech Lead author
- Review: approved by a distinct read-only Tech Lead on 2026-08-31 after exact asset/publication/closeout schemas and recovery branches were closed; a narrow implementation-discovered closeout child-schema amendment was independently approved the same day

## Context

The current contract describes an exact tag/Release URL as selecting an
“immutable version.” Exact selection, artifact digest and GitHub platform-enforced
immutability are different facts. A maintainer with authority may move/delete a
tag or replace Release state unless live platform metadata proves otherwise.

Vibe Kit already builds and validates deterministic local candidates, but v0.3–
v0.6 GitHub publication used ad hoc Agent commands. v0.7.0 needs a first-class,
dry-run-first, consent-bound and read-before-write/read-back workflow while keeping
credentials/network outside the CLI and Plugin.

## Decision

### Trust vocabulary

Current normative and user-facing contracts distinguish:

- **exact/pinned selection** — exact SemVer tag, canonical Release/tag URL or
  commit digest selected for this operation;
- **verified content identity** — transferred SHA-256, release manifest, nested
  checksums, payload tree and cross-channel validation pass; and
- **platform-enforced immutability** — reported only when live GitHub metadata
  positively proves it, otherwise false or unknown.

Canonical wording is:

> An exact canonical tag or Release URL selects a specific published version. It
> does not by itself prove that the tag or Release is platform-immutable. Trust
> transferred bytes only after their SHA-256 and nested release validation pass.

Accepted exact-ref shapes and version/digest/moving-ref behavior remain compatible.
Internal help/error vocabulary changes from `immutable_ref` to `exact_ref`. A
digest proves verified bytes, not publisher identity.

### Component boundary

The product exposes one Agent-facing Vibe Kit release workflow:

1. a repository Agent Skill owns readiness/QA, plan presentation, exact-payload
   authorization binding, host operation ordering, one-next-action and durable
   verification;
2. the offline CLI supplies `publication-plan` and `validate-publication`; and
3. the Agent/host GitHub capability owns authentication, network, Git/ref/Release/
   issue read/write and live read-back.

`bin/vibe` gains no credential, implicit network resolver or updater. The host may
use `gh`, GitHub API or an equivalent adapter but must produce the same closed
receipt. The bootstrap Plugin gains no MCP, hook, app, publisher, background
process or network authority.

### Five-asset release declaration

Release manifest schema 2 is an inner declaration of direct ZIP, Plugin ZIP,
payload, marketplace and protocol identities. It contains no digest for itself,
`SHA256SUMS` or the distribution ZIP. `SHA256SUMS` covers exactly:

```text
release-manifest.json
vibe-kit-0.7.0.zip
vibe-kit-plugin-0.7.0.zip
marketplace/marketplace.json
marketplace/plugins/vibe-kit/**    # every allowlisted regular file
```

Every covered file appears once as lowercase 64-hex, two ASCII spaces, a safe
POSIX relative path and LF, sorted by UTF-8 path bytes. Directories, symlinks,
`SHA256SUMS` and the distribution ZIP are excluded. Missing, extra, duplicate,
unsafe or mismatched lines fail.

The distribution ZIP contains exactly:

```text
vibe-kit-0.7.0/SHA256SUMS
vibe-kit-0.7.0/<every exact SHA256SUMS-covered path>
```

It never contains itself. ADR 0004 normalized path/mode/timestamp/compression/order
rules remain. After this ZIP is final, `publication-plan` binds the five public
assets:

```text
SHA256SUMS
release-manifest.json
vibe-kit-0.7.0.zip
vibe-kit-distribution-0.7.0.zip
vibe-kit-plugin-0.7.0.zip
```

Each entry has exact name, role, size and SHA-256, sorted by UTF-8 name bytes.
`asset_set_sha256` hashes the canonical array. This intent is the sole outer
closure. The four corresponding public/inner distribution members are byte-
identical. The public Release list must be the exact five-name set; missing,
extra, duplicate or same-name/different-byte state conflicts except for the
authorized missing-object branch.

### Publication intent schema 1

The canonical intent omits its own digest; the CLI envelope and authorization
reference its SHA-256. Every object below has `additionalProperties: false`, every
listed field is required, and types are strict JSON string/integer/boolean/array/
object unless a field explicitly permits null. Top-level fields are exactly:

```text
schema_version = 1
kind = vibe-kit-publication
repository
version
source_commit
main
tag
release
assets
asset_set_sha256
local_gates
remote_snapshot
operations
authorization_scope
issue_closeout_policy
recovery_policy
```

Nested shapes are exact:

```text
repository: owner, name, canonical_url
main: branch, expected_old_oid, target_oid, policy=fast-forward-cas-only
tag: name, object_type=tag, expected_tag_object_oid, target_commit,
     tagger_name, tagger_email, tagger_timestamp, tagger_timezone,
     message_sha256
release: title, body_sha256, body_source_path, draft=false, prerelease=true,
         generated_notes=false, platform_immutability_required=false
asset item: name, role, size, sha256
local_gates: source_clean, source_commit_verified, qa_passed,
             package_a_sha256, package_b_sha256, byte_identical,
             validate_release_passed
remote_snapshot: observed_at, main_oid, tag_state, tag_oid,
                 release_state, release_id, asset_set
operation item: sequence, operation_id, kind, natural_key,
                expected_precondition, max_write_attempts=2
authorization_scope: repository, version, release_kind, allowed_operations,
                     destructive_operations_allowed=false
issue_closeout_policy: issues=[1,2,3,4,5],
                       requires_public_verification=true,
                       requires_separate_closeout_intent=true,
                       requires_separate_closeout_authorization=true
recovery_policy: read_back_before_retry=true, delete=false, replace=false,
                 force=false
```

Strings containing OIDs/digests are lowercase 40-hex Git SHA-1 or 64-hex SHA-256
as declared; sizes/sequences are non-negative integers and timestamps are ISO-8601.
Asset roles are exactly `checksum`, `manifest`, `direct`, `distribution`, and
`plugin`, one each. `remote_snapshot.tag_state` and `release_state` are
`absent|present`; their OID/ID is null iff absent. A remote asset observation is
exactly `name`, non-negative `size`, nullable `sha256`, nullable integer `id` and
nullable `download_url`; SHA is required once an existing asset is publicly
downloaded. Operation kind is one member of the authorized-operation set and
`expected_precondition` is a closed `kind`, `identity_sha256` object. All gate
flags are booleans and all gate digest fields are 64-hex.

Repository is exactly `mintgao/vibe-kit`, version/tag are `0.7.0`/`v0.7.0`, and
the source commit is full-length. Tag identity is precomputed without writing a
ref. Release body bytes come from one fixed accepted-candidate path; remote body is
LF-normalized before hash comparison. Any bound-field change produces a new
intent and invalidates prior authorization.

### Two-layer authorization

The user's 2026-08-31 request authorizes the exact v0.7.0 Pre-release scope, not an
unbounded GitHub mutation. The executable authorization record binds:

```text
authorization_id
repository
version
release_kind
allowed_operations
publication_intent_sha256
host_operation_id
```

The closed allowed-operation set is:

```text
fast-forward-main
create-or-confirm-annotated-tag
create-or-confirm-prerelease
upload-or-confirm-five-assets
read-back-publication
download-and-verify-public-assets
conditionally-comment-and-close-issues-1-through-5
```

Changing repository, version, release status, accepted commit, tag identity,
Release body/title, assets, operation set, destructive behavior or issue set needs
new authorization.

### Executable publication graph

The closed graph is:

```text
host remote read
  -> offline publication-plan --phase publish
  -> frozen publication intent
  -> exact authorization
  -> host apply/reconcile
  -> public metadata read-back and asset download
  -> offline validate-publication
  -> publication/verification receipt
  -> offline publication-plan --phase issue-closeout
  -> frozen closeout intent
  -> host issue reconciliation
  -> final receipt
```

The CLI is offline. It validates structures, hashes and declared observations; it
does not claim GitHub authenticity merely because a receipt is well formed.

Remote reconciliation is exact and non-destructive:

- `main` advances only under the intent's expected-old-OID compare-and-swap/lease
  and only as a fast-forward; force push is forbidden;
- a missing tag is created from the frozen annotated-tag object, while an existing
  tag must match ref OID, tag object and peeled commit exactly;
- an existing Release-by-tag must match exact title/body/state;
- the full remote asset list is read before uploads; missing authorized assets may
  be uploaded, but extra/duplicate/divergent assets block;
- every timeout/uncertain response triggers exact read-back and, for assets,
  public download/hash before any retry; and
- final reconciliation rereads main/tag/Release/assets and downloads all assets.

Each operation permits at most two write attempts. Definite write success still
requires read-back. Timeout/transport uncertainty never triggers an immediate
retry; the closed read-back classification is:

```text
match               -> confirmed-after-uncertain; no retry
divergent           -> conflict; no retry
positively-absent   -> one retry only when attempts < 2, then mandatory read-back
still-unknown       -> uncertain; no retry and one read-back next action
```

For a branch update, positively-absent means the exact expected preimage is still
observed; for create/upload it means the exact natural-key object is proven absent.
After the second attempt, positively-absent becomes
`absent-after-bounded-retry`/confirmed-partial and never gets a third write.
Permission/auth failure has no retry. Any extra/duplicate asset conflicts before
this invocation performs an asset write.

No branch force, tag move, object delete, asset replacement, Release rewrite or
stable/draft transition is automatic. Divergence blocks with one next action.

Remote write state is `none`, `confirmed-partial`, `confirmed-complete`, or
`uncertain`. Verification is `not-run`, `passed`, `failed`, or `uncertain`.
Published-but-unverified remains public and is never announced as verified.

### Publication receipt schema 1

Every object has `additionalProperties: false`; every listed field is required and
strictly typed, with explicit null only where the remote object has not yet been
created/observed. Top-level fields are exactly:

```text
schema_version = 1
kind = vibe-kit-publication-receipt
intent_sha256
authorization_id
host_operation_id
repository
remote_write_state
verification_state
main
tag
release
assets
operations
downloads
validate_release
smokes
limitations
issue_closeout
error
```

The `main`, `tag`, `release` and asset items carry their intent identity plus
observed public state with these exact fields:

```text
main: branch, expected_old_oid, target_oid, observed_oid, write_state, read_back
tag: name, expected_tag_object_oid, observed_ref_oid, peeled_commit,
     write_state, read_back
release: id, url, tag, title, body_sha256, draft, prerelease,
         immutable, write_state, read_back
asset item: name, role, size, sha256, id, url, write_state, read_back
download item: name, size, sha256, matched
validate_release: status, receipt_sha256
smoke item: name, status, evidence_sha256
error: code, message, next_action
```

Nullable remote IDs/URLs/OIDs are permitted only before observation; successful
confirmation requires them. `immutable` is `true|false|unknown`.
`validate_release.status` is `valid|invalid|error`; smoke status is
`passed|failed|error`; `error` and `issue_closeout` alone may be top-level null.
`write_state` in remote object/item shapes uses the receipt's remote write enum and
`read_back` is boolean. Each operation receipt is
exactly `sequence`, `operation_id`, `kind`, `natural_key`, `write_attempts`,
`initial_response`, `read_back_result`, `outcome`, nullable `remote_object_id` and
nullable `error`. Outcomes are:

```text
not-attempted | read-matched | created | uploaded |
confirmed-after-uncertain | conflict | permission-denied |
absent-after-bounded-retry | uncertain
```

`initial_response` is `not-attempted|definite-success|timeout|transport-unknown|
permission-denied`; `read_back_result` is
`not-run|match|divergent|positively-absent|still-unknown`. Limitations is an array
of bounded strings; assets/downloads/operations/smokes are arrays of the exact
items above.

Remote write state is `none`, `confirmed-partial`, `confirmed-complete`, or
`uncertain`; verification is `not-run`, `passed`, `failed`, or `uncertain`.
Receipts contain allowlisted public/sanitized facts only and exclude credentials,
headers, environment, raw output and goal/conversation content.

`validate-publication` returns valid only when remote write is confirmed-complete,
all five public downloads match the intent, the distribution member graph is
exact, inner `validate-release` is valid and every required smoke passes.

### Issue #1–#5 closeout transaction

Issue closeout is a post-publication, idempotent remote-write phase. It cannot
start until release write state is `confirmed-complete`, public verification is
`passed`, and criterion-to-evidence verification covers all five issues.

The stable ID is computed before comment bytes or closeout-intent digest:

```text
closeout_id = SHA256(canonical JSON of {
  "schema_version": 1,
  "repository": "mintgao/vibe-kit",
  "version": "0.7.0",
  "parent_publication_intent_sha256": "<digest>",
  "issues": [1,2,3,4,5]
})
```

Each marker uses that stable ID:

```text
<!-- vibe-kit:v0.7.0:issue-<n>:<closeout_id> -->
```

The exact comment bytes and hashes are then formed, so no digest is self-
referential. Closeout intent schema 1 has `additionalProperties:false` at every
level and exactly these required top-level fields:

```text
schema_version=1
kind=vibe-kit-issue-closeout
closeout_id
parent_publication_intent_sha256
publication_receipt_sha256
verification_receipt_sha256
repository
issues
remote_snapshot
operations
authorization_scope
```

Each issue item contains exactly `issue_number`, `marker`, `comment_body_sha256`,
`observed_state`, nullable `observed_matching_comment_id`, `desired_state=closed`
and `criterion_evidence_sha256`.

The remaining closeout-intent child objects are closed as follows. No field below
is nullable unless explicitly stated, and every object has
`additionalProperties:false`.

`remote_snapshot` contains exactly `observed_at` and `issues`. `observed_at` is an
ISO-8601 timestamp. `issues` is exactly five items ordered `[1,2,3,4,5]`; each
contains exactly:

```text
issue_number
state
marker_state
matching_comment_id
matching_comment_body_sha256
```

`issue_number` is an integer, never a boolean. `state` is `open|closed` and
`marker_state` is `absent|exact`. With `absent`, both matching fields are null.
With `exact`, comment ID is a positive integer and body SHA is lowercase 64-hex
equal to the corresponding issue item's `comment_body_sha256`. Snapshot state/ID
must equal the top-level issue observation. A safe intent permits only
`open+absent`, `open+exact`, or `closed+exact`; mismatch, duplicate exact comments,
or `closed+absent` blocks planning before an executable digest exists.

`operations` is exactly ten items, in issue order, comment then close. Each item
contains exactly:

```text
sequence
operation_id
issue_number
kind
natural_key
expected_precondition
max_write_attempts
```

Sequence is integer `0..9`; issue `n` comment/close uses `2*(n-1)` and the next
integer. Kind is `create-exact-evidence-comment|close-issue`; operation ID is
`issue-<n>-comment|issue-<n>-close`; natural key is
`issue:<n>:marker:<closeout_id>` or `issue:<n>:state:closed`; maximum attempts is
integer `2`.

`expected_precondition` contains exactly `kind`, `initial_snapshot_sha256` and
`allowed_observations`. Kind is `issue-closeout-monotonic-resume`; SHA is lowercase
64-hex over that issue's canonical snapshot item. Allowed observations, in order,
are exactly:

```text
comment: [open-absent, open-exact, closed-exact]
close:   [open-exact, closed-exact]
```

The executor rereads issue state and all exact-marker comments before each
operation. It reuses exact observations; close is forbidden until the exact
comment has been read back.

Intent `authorization_scope` contains exactly `repository`, `issues`,
`allowed_operations`, `destructive_operations_allowed` and
`requires_separate_closeout_authorization`, with exact values:

```text
repository = mintgao/vibe-kit
issues = [1,2,3,4,5]
allowed_operations = [create-exact-evidence-comment, close-issue]
destructive_operations_allowed = false
requires_separate_closeout_authorization = true
```

Names are strings, issue values are integers (never booleans), and policy fields
are booleans. This scope is declarative, not executable authorization. Separate
authorization must contain exactly `closeout_authorization_id`, `repository`,
`issues`, `allowed_operations`, `closeout_intent_sha256` and
`destructive_operations_allowed=false`; scope fields must equal the intent and
the digest must equal canonical closeout intent SHA-256.

Each operation makes at most two writes. It reads before the first write and after
every definite or uncertain response. Read-back classification is exact:

```text
exact desired -> read-matched or confirmed-after-uncertain; no retry
divergent/closed-absent/body-mismatch/duplicate -> conflict; no retry
positively absent after attempt 1 -> one retry, then mandatory read-back
positively absent after attempt 2 -> absent-after-bounded-retry; no third write
still unknown -> uncertain; no retry
permission/auth failure -> permission-denied; no retry
```

For comment creation, positively absent means open without an exact marker. For
close, it means open with one confirmed exact comment. Conflict/uncertainty stops
the current and all later operations; earlier confirmed items remain reusable. A
later invocation with the same intent and authorization rereads and resumes from
the first non-terminal operation without duplicating comment or close.

Before any issue write, a distinct closed authorization binds
`closeout_authorization_id`, repository, exact `[1,2,3,4,5]`, allowed operations
`[create-exact-evidence-comment, close-issue]`, `closeout_intent_sha256` and
`destructive_operations_allowed=false`. Conditional publication scope permits
planning/review but does not replace this executable binding. The current user
request authorizes this exact scope; changed issue set, comment bytes, desired
state or operation scope needs new authorization.

Resume behavior is exact:

| Current issue state | Exact marker/body | Action |
|---|---|---|
| open | absent | create exact comment, read back, then close |
| open | exact | reuse comment and close only |
| closed | exact | idempotent complete; no write |
| uncertain comment, exact now exists | exact | reuse, then continue close |
| uncertain close, now closed | exact | confirmed-after-uncertain |
| closed | absent | conflict; do not comment on a closed issue |
| any | marker exists but body differs | conflict |
| any | duplicate exact comments for one closeout ID | conflict and stop writes |

An exact terminal closed issue is never rejected merely because its current state
differs from the first open snapshot. Issues execute in numeric order. On conflict
or uncertainty, earlier confirmed issues stay complete and current/later issues
receive no more writes; the next invocation uses the same intent/authorization and
reuses exact terminal state. The host never reopens, deletes or edits.

Final receipt `issue_closeout` contains exactly `closeout_id`,
`closeout_intent_sha256`, `closeout_authorization_id`, `overall_state` and `items`.
Overall state is `not-run`, `confirmed-partial`, `confirmed-complete`, `uncertain`
or `conflict`. Every item retains issue number, expected initial state, comment
hash/ID/URL, comment/close write states, observed post-state, read-back and error.
Only five exact-marker/body closed and read-back-confirmed items yield
confirmed-complete.

### Public verification

The workflow downloads from canonical public Release URLs and verifies metadata/
intent parity, the exact five-asset set, all five outer SHA-256 values, nested
distribution checksums, target `validate-release`, fresh direct init/doctor,
downloaded Plugin smoke, and critical exact historical/current upgrades including
v0.3, v0.5 and v0.6. GitHub's live `immutable` metadata is recorded but is not a
v0.7 gate.

### Joint v0.7 contract matrix

| Contract | Version |
|---|---:|
| Kit | `0.7.0` |
| Core protocol | `5` |
| Codex adapter protocol | `5` |
| Agent-install schema | `3` |
| Agent-install protocol | `3` |
| CLI result schema | `2` |
| Takeover schema | `2` |
| Maintenance bridge schema | `2` |
| Compatibility migration registry | `2` |
| Release manifest schema | `2` |
| Transaction journal schema | `1` |
| Commit marker schema | `1` |
| Publication intent schema | `1` |
| Publication receipt schema | `1` |
| Issue closeout intent schema | `1` |

Installed manifest `1`, onboarding `1`, feedback protocol `2` and activation v2
remain. Release/Plugin/marketplace, compiled constants and Agent-install/core/
release mirrors agree exactly. Old consumers fail closed on unknown schema or
protocol; target v0.7 contracts are the interpretation authority.

## Alternatives considered

- Put GitHub API calls and credentials inside `bin/vibe`: rejected because it
  combines network authority with the deterministic local engine.
- Continue ad hoc `gh` commands: rejected because they lack canonical intent,
  exact authorization and idempotent reconciliation.
- Make GitHub Actions the sole publisher: rejected because it adds a secret/CI
  dependency and does not replace the local/host contract.
- Hash the release manifest into itself or put distribution outer hashes inside
  an archive it hashes: rejected as self-referential.
- Close issues as part of initial publication writes: rejected because closure
  must depend on completed public verification.

## Compatibility, versioning and supersession

For v0.7 and later this decision supersedes:

- ADR 0007 and ADR 0009 wording that calls an exact hosted ref/Release immutable;
- ADR 0004 wording that a release manifest or `SHA256SUMS` can declare every final
  transferred digest, especially its own and the final distribution archive's;
  and
- ADR 0004's self/distribution outer-closure construction.

ADR 0004 deterministic build, normalized payload and nested validation rules
remain. The v0.7 outer closure is the publication intent. ADR 0002's “immutable
payload” means digest-fixed bytes. ADR 0005 and ADR 0009 credential, host and
activation boundaries remain.

Local package/validate/install/upgrade remain Python 3.9 standard-library and
offline. Stable promotion, public Plugin Directory, signing/provenance and other
host-platform claims remain outside scope.

## Recovery

- Local candidate/intent failure rebuilds unpublished output from the accepted
  commit.
- Remote partial/uncertain state rereads and reconciles only exact authorized
  missing objects under the same intent.
- Divergent remote state blocks without mutation.
- Published but unverified state remains public as `published-unverified`.
- Issue closeout resumes only by its exact intent and never duplicates an exact
  marker/comment.
- Source rollback is Git revert; public delete/replace/force move is never
  automatic recovery.

## Verification

Verification covers no-write plans; canonical intent/tag/body/asset identity;
authorization invalidation; clean/dirty/version/manifest gates; fresh/identical/
partial/divergent remote main/tag/Release/assets; timeouts and read-back;
permissions; exact asset-set conflicts; public downloads; observed immutable
metadata; closeout pre-state/marker/comment/close/uncertain/idempotency branches;
receipt schemas/redaction; network-disabled CLI tests; cross-channel contract
parity; full/default/Python 3.9/two-build parity; and the actual v0.7 publication
and issue closeout receipts.

## Open decisions

None. Stable promotion, mandatory platform immutability, changed issue set,
narrowed compatibility, network inside CLI, automatic remote rollback or a generic
third-party publisher requires a new material product decision.
