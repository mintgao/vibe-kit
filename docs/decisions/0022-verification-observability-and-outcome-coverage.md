# 0022: Preserve publication inputs and upgrade recovery while adding local verification observability and prospective outcome coverage

- Status: Accepted
- Date: 2026-10-11
- Decision owner: read-only Tech Lead author
- Work item: `docs/work-items/20261010-feedback-closure/brief.md`
- Source baseline: `ac549fa69319ef92ba859bd7a43d3607ec226e43` — Vibe Kit 0.10.1
- Review: Baseline design-only approval: `docs/work-items/20261010-feedback-closure/technical-review-prior.md` (review SHA-256 `45b59c9b0c0326d95ced3f7a71f8c2739fad383a3e63e6f46c771faa7d8e329b`, reviewed Proposed ADR SHA-256 `97adc3490910de7c47767e499c5a127702f12443d1de6d261fdf6d285989cc10`); a distinct review of this persisted adoption revision is required and recorded in the brief before implementation release.

## Context and evidence

This is source-distribution development following a synchronized Git baseline. It is not an installed application's Kit upgrade or takeover, and changes no downstream project.

The five accepted targets are public issues #14 and #15 and the three approved suggestions now published as #16 (L01: complete sanitized success logs), #17 (L02: persistent verification execution progress), and #18 (L03: prospective multi-stage outcome coverage). L01–L03 remain traceability aliases for those exact published issues; no new feedback submission is part of this work.

The following gaps are confirmed by source inspection:

1. `bin/vibe#main` assigns `RECEIPT_CONTEXT` for every parsed `--receipt`. `validate-publication` uses that option as an input, while `print_json` treats the context as an output destination. Validation therefore overwrites its input receipt.
2. `transaction_installation_state_project` compares each current image with its preimage before its postimage. An equal preimage/postimage is classified only as pre. Upgrade always stages manifest/version entries, so an already-current `.vibe/version` can prevent target validation.
3. `verify` captures complete output but writes complete artifacts only for failed or environment-limited checks. Successful checks retain bounded tails.
4. `verify` executes checks synchronously, with no durable before/after-check execution record. JSON is printed only at the end.

L03 has medium-confidence framework attribution. Existing operating-model and implementation instructions already require truthful completion boundaries, follow-ups, contradiction resolution and independent QA. The new guidance supplies a reusable cross-stage expression of those obligations; it does not establish that the framework caused every observed omission or wait.

ADR0010 continues to govern lossless final-leaf mutation, inode-pair recovery, prepared directory units and fail-closed transactions. ADR0011 continues to govern offline CLI operation and host-owned publication. ADR0012 continues to govern readiness, capability honesty, one implementation writer and independent verification. ADR0017 continues to govern check order, bounded diagnostics and non-passing environment-limited coverage. ADR0018 continues to govern receipt artifacts and host-only goal/custody state. ADR0021 remains the exact historical 0.10.1 publication decision.

## Decision boundary

Implement five bounded changes:

- separate publication input receipts from result persistence;
- make transaction image equality satisfy both the predecessor and target predicates;
- add opt-in complete sanitized success output;
- add local metadata-only before/after-check execution progress and honest incomplete evidence;
- add prospective, lightweight outcome coverage guidance for applicable multi-stage M/L work.

Do not add a scheduler, backend, telemetry, streaming raw-output spool, implicit network operation, new permission bypass, automatic host activation, downstream migration or reduced independent QA.

## Publication input and result ownership

### Command interface

`validate-publication --receipt <path>` remains exclusively an input option.

Add:

```text
validate-publication ... --result-receipt <new-path>
```

This explicitly persists the final validation envelope and implies JSON output. With no `--result-receipt`, validation writes no result artifact.

The input receipt must remain byte-identical after valid, invalid and error results. Existing publication profile verdict rules are unchanged.

### Dispatch and write ordering

Replace attribute-based receipt dispatch with an explicit output-option allowlist:

- existing output `--receipt` semantics remain for plan, upgrade, doctor, verify and validate-takeover;
- validate-publication never installs its input `--receipt` in generic output context;
- its optional result artifact is written explicitly, once, after constructing the final validation result.

Reset generic receipt context before argument parsing and clear it in a finally boundary covering parsing failures, returns, SystemExit and exceptional exits. Repeated calls to main in one process must not inherit an earlier output destination.

Nested validators, including the captured `validate-release` call, must not persist an intermediate result through the publication output option. Artifact persistence belongs to the outer command boundary.

### Alias and destination checks

Before any output write, protect the intent, input receipt, optional authorization, and candidate directory.

Reject:

- lexical aliases after absolute-path and `.`/`..` normalization;
- resolved aliases, including input symlink referents;
- existing same-file aliases identified by device/inode, including hard links;
- any output inside the candidate directory;
- output symlinks, symlinked output-parent components, nonregular existing leaves, or an unavailable parent.

The output parent must already exist. This command does not create arbitrary parent directories.

`--result-receipt` is create-only: any existing destination is refused. This removes the dangerous check-then-overwrite race even when an unrelated process creates an alias after preflight.

Use a pinned parent directory and an exclusive no-follow temporary, mode 0600. Write and fsync the complete bytes, publish without replacing an existing final leaf, fsync the parent, and clean only the exact temporary owned by this operation. If required safe publication primitives are unavailable, report output persistence unavailable and exit nonzero; do not fall back to overwriting.

Input symlinks need not acquire a new blanket rejection rule when historical read-only validation accepted them. Output operations must never follow them.

Alias rejection occurs before a result file or temporary is created. Validation failures and write failures must not trigger a second generic artifact write from an error handler.

## Equality-aware upgrade validation

### Image predicates

For each transaction item, calculate independently:

```text
matches_pre  = current image equals recorded preimage
matches_post = current image equals recorded postimage
```

Image equality includes the existing state, content identity and mode.

An equal preimage/postimage may satisfy both predicates. It must not be forced into only pre or only post.

Consumers use the predicate required by their operation:

- forward commit requires every target/postimage predicate;
- verified rollback requires every predecessor/preimage predicate;
- recovery with a valid commit marker requires target predicates and the existing committed-pair proof;
- recovery without a valid commit marker follows the existing rollback/prepared-pair rules, even when bytes satisfy both predicates.

Mixed genuinely pre-only and post-only entries remain recovery-required. A scoped image satisfying neither remains unknown and preserves evidence.

### Preserve recovery authority

Byte equality does not replace object identity.

Keep unchanged:

- preimage and prepared postimage device/inode binding;
- final/private pair checks;
- no-clobber/exchange mutation;
- compensating exchange limits;
- absent-preimage rollback;
- directory-unit recovery;
- valid commit-marker requirements;
- tamper, active-transaction and unsupported-filesystem rejection.

A byte-identical third-party replacement remains a race when its inode fails the recorded pair proof.

Do not introduce a version-string shortcut that returns success without the existing source, manifest, path, conflict and identity checks. Same-version does not mean same content.

### Repeat semantics

The smallest fix retains the existing transaction representation and equal manifest/version entries. An already-current repeat may commit a maintenance transaction whose logical managed content is unchanged.

It must honestly report its actual transaction and write state. It must not claim `writes_performed: false` if it exchanged state leaves or wrote transaction control.

Its summary may state that already-current content was validated and a maintenance transaction committed. It must not claim runtime activation or readiness.

A true zero-write fast path, elimination of equal journal entries, or a new transaction outcome is outside this iteration. Those would require additional race and compatibility decisions.

## Complete sanitized output and receipt identity

### Configuration

Extend the strict checks declaration with:

```yaml
checks:
  log_policy: "failures"
  progress: true
```

Accepted log_policy values are exactly:

- failures — default; retain complete output for failed and environment-limited checks;
- all-configured — additionally retain complete output for successful configured checks that obtained a complete process result.

Progress is a strict JSON-style boolean true or false. Missing values resolve to failures and true.

Add verify --log-policy failures|all-configured and mutually exclusive --progress / --no-progress overrides. Each override affects only its corresponding setting.

Keep requires and output_limit_bytes and the existing 16384-byte minimum. Reject unknown keys, policies, duplicate declarations, malformed values and dependency cycles before running checks. Do not rewrite old configurations.

### Orthogonal behavior

| Progress | Log policy | Durable behavior |
|---|---|---|
| enabled | failures | Metadata-only execution snapshots; complete failed/environment-limited logs |
| enabled | all-configured | Metadata-only execution snapshots; complete successful and failed/environment-limited logs |
| disabled | failures | No run snapshots or locator; complete failed/environment-limited logs |
| disabled | all-configured | No run snapshots or locator; complete successful and failed/environment-limited logs |

Neither progress setting authorizes successful output retention. Successful complete-log retention requires all-configured. Existing explicit --receipt independently requests persistence of the bounded final envelope, including its sanitized tails.

Never automatically create result.json or another copy of the final result body. Default progress stores neither successful tails nor complete output bodies.

### Log format and location

Capture output in memory until a complete process result. Do not create raw output spools or live streaming logs.

Define layout stdout-stderr-v1 as the exact UTF-8 concatenation:

```text
"=== stdout ===\n" + sanitize(stdout) +
"\n=== stderr ===\n" + sanitize(stderr)
```

The labels and added separator are literal; do not normalize or trim the sanitized stream text. This preserves both streams but does not claim chronological interleaving.

Let H be lowercase SHA-256 of those exact bytes. Store the complete artifact at:

```text
.vibe/local/verify/logs/sha256/<H>.log
```

The path is project-root-relative and depends only on sanitized content and layout, not timestamp, run ID or check name.

Keep the final verification field shape:

```text
check.output.full = { path, sha256 }
```

The path is the content-addressed path above; sha256 is H. Add no new schema-2 final-result field. Byte count, layout and availability are diagnostic metadata.

Publish complete artifacts exclusively without replacing an existing final leaf. Concurrent producers of identical content may reuse the same artifact only after independently checking its exact bytes, digest, regular-file type, owner, mode and single-link identity. A mismatching, unsafe or unreadable existing object is unavailable, never overwritten or silently repaired.

A selected artifact is referenced only after publication/reuse validation succeeds. Empty streams can produce a complete labeled artifact. Unconfigured, never-started and interrupted checks do not produce a complete process-output artifact.

Historical timestamped logs and their receipts remain untouched.

### Sanitization

Sanitize complete captured streams before disk publication and before deriving bounded tails. A supported credential split across process writes is therefore inspected as one complete stream.

Cover existing credential patterns, entire recognized private-key blocks, recognized unterminated private-key blocks through end of stream, project-root aliases, ANSI escape sequences, DEL/C1 and other unsafe controls, and invalid UTF-8 through deterministic replacement.

Strip unsafe controls before credential matching. Preserve ordinary text, newline and tab. Sanitization of the complete artifact and tails must use the same policy.

Known-pattern sanitization is not universal secret detection. Do not collect environment values to manufacture that guarantee. Private logs are not authorized for public submission.

### Availability, failure and retention

Log availability is one of:

- pending;
- not-selected;
- not-applicable;
- available;
- unavailable;
- incomplete.

Not-selected means a completed successful check under failures. Not-applicable means no complete process output exists because the check was unconfigured or never started. Incomplete means a started check was interrupted without a complete capture.

Available requires an exact path, byte count and digest. All other states have null artifact identity fields. Never claim a partial file is complete.

A full-log or progress storage failure does not alter the project's observed exit code or verdict, stop later independent checks, trigger elevation, or move evidence outside the project. Report unavailable through writable metadata and bounded sanitized stderr diagnostics. Omit output.full when no complete verified artifact exists.

The existing explicit --receipt request retains its nonzero-on-write-failure contract. If that requested write fails, emit a normal schema-2 verify error result with exit code 2 when JSON reporting remains possible, without a fallback file or recursive receipt write. Preserve already observed per-check outcomes in available metadata. This is distinct from an optional log/progress failure.

No automatic expiry, quota deletion or background cleanup is added. Artifacts remain until explicitly removed. Do not truncate an artifact claimed complete; resource exhaustion means unavailable. Full-memory capture and potentially substantial opt-in disk usage remain limitations.

### Receipt stability amendment

This decision narrowly amends the unqualified same-tree/cross-parent byte-stability statement in ADR0018 and AGENT_INSTALL.md.

The serialization guarantee is:

> For the same result-envelope values after project-root-relative rewriting, receipt serialization produces identical bytes. Actual process output, toolchain observations, transaction identities and other runtime evidence can differ between invocations. Receipt writing does not make executions deterministic.

Use the existing receipt serialization: UTF-8 JSON, ensure_ascii=False, sorted keys, indent=2 and one terminal LF. A receipt's cited SHA-256 is over its actual serialized file bytes.

The baseline's timestamped failure-log references already prevent a general execution byte-stability guarantee. Historical receipts retain their recorded meaning and bytes; this amendment does not retroactively normalize them.

For new complete logs, fixed sanitized content and layout produce the same path and digest. With fixed final-envelope values, fixed settings and fixed observed toolchain, repeated verify receipts must be byte-identical, including all-configured success references. Progress run IDs and timestamps must never enter the final verification envelope.

Update the current managed guide to state this qualified guarantee. No result schema or protocol bump is required for correcting the promise and using the existing reference shape.

## Metadata-only execution progress

### Location and discovery

When enabled and safe storage is available, use:

```text
.vibe/local/verify/runs/<run-id>/progress.json
.vibe/local/verify/runs/latest.json
```

Run ID grammar is exactly:

```text
verify-<32 lowercase hexadecimal characters>
```

Create each run directory exclusively using a randomly generated ID. Concurrent runs never share snapshots.

latest.json identifies the run whose locator write was last successfully published. Concurrent starts may publish out of start-time order. A caller’s own startup notice identifies its run ID and progress path. The locator is discovery-only, not liveness, completion or acceptance evidence.

When progress is disabled, create no run directory, snapshot or locator. Selected logs still use the independent private content-addressed log directory. There is no logs-only run directory.

Emit a bounded startup stderr notice containing the run ID when created, progress availability/path or disablement/unavailability, and the effective log policy. Emit a bounded per-check stderr availability notice for selected complete logs, including available identity or an enum reason. Each notice is at most 2048 UTF-8 bytes and excludes raw exception text, command arguments and output bodies.

JSON stdout remains one final verification result. Diagnostic notices never enter it.

### Types and common rules

Execution schema 1 is local diagnostic evidence, separate from CLI result schema 2, takeover and acceptance receipts.

Reject duplicate JSON keys, nonfinite numbers, unknown keys, missing keys, unknown schemas/enums and booleans where integers are required.

All digests are exactly 64 lowercase hexadecimal characters without a prefix. All integers are signed 64-bit values unless further restricted. Byte counts are nonnegative. Check names are exactly lint, typecheck, test or build.

All paths are safe POSIX project-root-relative paths, at most 1024 characters: no absolute prefix, backslash, empty component, dot/dot-dot component or control character.

Timestamps are UTC strings in exact YYYY-MM-DDTHH:MM:SS.ffffffZ form. Validate calendar values. started_at <= updated_at; ended_at, when nonnull, lies between them. Check times lie within the run observation interval, with start <= end. Writer timestamps must not move backward; clamp a backward wall-clock observation to the previous recorded timestamp. These are observation times, not timing or performance proofs.

A snapshot is at most 65536 UTF-8 bytes. It contains at most four checks. No unbounded free-text field exists.

### Exact snapshot shape

progress.json contains exactly:

```text
schema_version
kind
run_id
kit_version
state
started_at
updated_at
ended_at
selection
effective_order
log_policy
current_check
checks
interruption
result
metadata_sha256
```

Values:

- schema_version: integer 1;
- kind: vibe-verify-execution;
- kit_version: current strict SemVer;
- state: running | incomplete | finished;
- current_check: null or a known selected check name;
- log_policy: failures | all-configured;
- interruption/result: null or the closed objects below.

effective_order is the four unique check names in the validated effective order.

selection contains exactly mode, requested, coverage:

- default: requested=[], coverage=all-configured;
- only: nonempty unique requested names in effective order, coverage=partial.

checks is exactly the selected ordered list: all four effective-order names for default, or requested for only.

metadata_sha256 is SHA-256 of canonical JSON of every other snapshot field. Canonical JSON means ensure_ascii=False, sort_keys=True, separators=(",", ":"), UTF-8, without terminal LF. Snapshot storage may use the receipt-style pretty serialization; its integrity digest still uses the defined canonical object.

This checksum detects inconsistent or changed metadata unless recomputed. It does not authenticate a malicious same-OS-principal writer.

### Exact check and log objects

Each check contains exactly:

```text
name
configured
state
started_at
ended_at
outcome
exit_code
reason_code
log
```

configured is a boolean. Check state is pending | running | finished | not-started | interrupted | unconfigured.

Allowed combinations:

| State | Required combination |
|---|---|
| pending | configured=true; times/outcome/exit/reason null; log pending |
| running | configured=true; start nonnull, end/outcome/exit/reason null; log pending |
| finished | configured=true; both times nonnull; passed/0/null reason, failed/nonzero/null reason, or environment-limited/nonzero/toolchain-mismatch |
| not-started | configured=true; start null, end nonnull; skipped/null exit; reason process-start-failed or execution-interrupted; log not-applicable |
| interrupted | configured=true; both times nonnull; skipped/null exit/execution-interrupted; log incomplete |
| unconfigured | configured=false; both times null; unconfigured/null exit/not-configured; log not-applicable |

Exit codes may be negative signal values; zero is forbidden for failed/environment-limited. The final envelope retains its existing environment details; progress does not duplicate them.

Each log contains exactly:

```text
availability
reason
layout
path
bytes
sha256
```

layout is always stdout-stderr-v1.

- available: reason=null; path is exactly the content-addressed log path derived from sha256; bytes is nonnegative; digest is nonnull;
- pending: reason/path/bytes/digest null;
- not-selected: reason=policy-failures; other identity fields null; allowed only for a finished passed check under failures;
- not-applicable: reason=not-configured for unconfigured, or not-started for not-started; identity fields null;
- incomplete: reason=execution-interrupted; identity fields null;
- unavailable: reason is permission-denied | unsafe-path | unsafe-object | unsupported-filesystem | resource-exhausted | io-error; identity fields null.

Finished failed/environment-limited checks, and finished passed checks under all-configured, require available or unavailable logs. No configured complete check may remain pending in a terminal snapshot.

### Exact interruption and final-result binding

interruption contains exactly:

```text
reason
requested_at
direct_child
descendants
```

- reason: sigint | sigterm | runner-error;
- requested_at: a timestamp within the run observation interval;
- direct_child: not-started | reaped | unconfirmed;
- descendants: exactly not-proven.

Do not persist process IDs, signal exception text or descendant lists. Reaped means the direct child was observed through a successful wait; it does not establish descendant termination.

result contains exactly:

```text
status
exit_code
envelope_sha256
receipt
```

status is passed | failed | blocked | error. Exit code is 0 for passed, 1 for failed and 2 for blocked/error.

envelope_sha256 is SHA-256 of canonical JSON of the final envelope after the existing project-root-relative transformation. Compute it in memory. Its body is not persisted by progress.

receipt contains exactly:

```text
availability
scope
path
sha256
reason
```

- not-requested: scope/path/digest/reason null;
- available: scope=project or external, digest over the actual receipt file bytes, reason=null;
- unavailable: scope=project or external, path/digest null, reason from the storage-error enum above.

For available project receipts, path is safe project-root-relative. For available external receipts, path is null: the caller already supplied the destination; progress does not persist its absolute location. An external receipt can be checked only when the caller supplies its bytes or authorized file reference.

No receipt is created unless the user explicitly supplied --receipt. An available interrupted blocked receipt is permitted; the run remains incomplete.

### Run state combinations

- running: ended_at/interruption/result null; at most one running check, exactly named by current_check. With no running check, current_check is null. Completed earlier checks remain recorded; all-finished checks may briefly coexist with running while final result construction is pending.
- finished: ended_at/result nonnull; interruption/current_check null; no pending, running or interrupted check. not-started is allowed only for process-start-failed. Finished describes completed result production, including failed, blocked or error results; it is not Pass.
- incomplete: ended_at/interruption nonnull, current_check null; no pending or running checks in the handled terminal snapshot. Preserve completed earlier checks; convert the active started check to interrupted and remaining configured checks to not-started/execution-interrupted. Unconfigured checks retain unconfigured. result is null or blocked/error with exit code 2.

An interruption near completion may leave all process outcomes observed; the invocation still reports blocked/error if interrupted before producing its terminal result. Do not erase an observed complete process outcome to manufacture a skipped count.

### Durable transitions and interrupted execution

After configuration/order validation, persist running metadata before external checks. Persist current check and start time before starting it, then its observed result and log availability after complete capture.

Construct the final bounded envelope in memory. Persist terminal metadata binding its digest, then emit the envelope. If --receipt was requested, perform that explicit write and record its actual availability before final metadata. Never persist an automatic envelope copy.

A crash between terminal metadata and stdout delivery may leave a constructed-result digest with no delivered body. The snapshot alone still cannot establish acceptance.

Use a small capture runner preserving shell/cwd semantics and imposing no normal project-check timeout. Install scoped SIGINT/SIGTERM handling and restore prior handlers.

On handled interruption, stop starting further configured checks, preserve observed outcomes, and report incomplete/blocked evidence when possible. Request termination of the direct shell; wait up to one second; if needed request kill and wait up to one further second. Record reaped only after a successful wait, otherwise unconfirmed. Do not manipulate process groups, assert all descendants stopped, or wait indefinitely on inherited descendant pipes.

Do not publish the interrupted capture as a complete log. Close owned capture resources; retain completed earlier artifacts.

SIGKILL, process crash and power loss cannot promise a terminal update. The last snapshot may remain running with null result. Running is a last observation, not proof of current liveness; without a terminal result body/binding it is incomplete evidence.

### Reader validation

Implement one bounded pure schema validator plus a safe snapshot reader, used by producer checks, tests and documented consumers. No scheduler or general state engine is added.

The reader:

1. opens the derived run/snapshot path without following symlinks;
2. checks private ownership, modes, regular-file type, single-link identity and size;
3. strictly parses JSON and validates every closed field, bound, enum and combination;
4. verifies metadata_sha256;
5. checks any supplied result envelope against envelope_sha256 and corresponding selection/order/check metadata;
6. when artifact evidence is requested, safely reads project-relative available logs/receipts and verifies their actual size/digest.

External receipt bytes are checked only when supplied. Unknown or malformed input returns bounded rule IDs and field paths, without echoing values.

A structurally valid snapshot without a matching final envelope is diagnostic only. A matching passed envelope must still pass the existing default/full-coverage and configured-check acceptance rules; progress does not waive them.

Missing, disabled, stale, unavailable or invalid progress does not invalidate an otherwise complete independently valid verification receipt. Conversely, progress never upgrades missing, partial, interrupted or non-passing verification to Pass.

Artifacts that cannot be read or whose digest/type/mode changed are unavailable/tampered evidence, not trusted references.

### Locator and storage security

latest.json is at most 2048 bytes and contains exactly schema_version=1, kind=vibe-verify-locator, run_id, progress_path and started_at. progress_path must equal the derived run path. It is discovery-only and never promises the latest snapshot digest.

The locator follows last-successfully-published order, not run-start order; concurrent publication requires no additional ordering guarantee.

New tool-owned directories are 0700 and regular evidence files 0600, enforced on opened objects. Pin the project root, traverse without following symlinks, use exclusive publication for blobs, and atomically replace only operation-owned private metadata with file and parent fsync.

Reject wrong types, unsafe ownership/modes, unexpected hard links and symlinked tool-state components. Do not chmod unrelated project parents or rewrite historical artifacts. Install nested ignore rules for both runs and logs.

Progress and log stores fail independently. If progress becomes unavailable, report it and stop relying on that sidecar; its last snapshot remains a last observation. Complete checks and selected logs may continue. If the common parent is unsafe, neither channel falls back elsewhere. Intentional disablement is reported as disabled, never as a storage error.

No diagnostic storage failure authorizes elevation or unsafe filesystem fallbacks.

## Prospective outcome coverage

Add a short optional section to the new brief template and Close guidance, used only when an M/L task delivers part of a larger approved outcome.

Use existing Markdown:

```text
Approved outcome / AC reference | This stage covers | State | Evidence |
Next action | Role owner | Blocker / waiting condition
```

Use explicit Pass, Fail, Blocked, Unverified or Not applicable states. Unverified is a planning/coverage state, not a new QA result enum; QA retains its existing four result states.

References point to approved project artifacts. Do not copy host goal text, transfer payloads or custody into repository documents.

For source Pass, external API Blocked and export Unverified, Close may claim the source stage completed. It must not claim overall delivery complete.

A failed result with an already-authorized actionable diagnosis receives that next action and an owner, and execution continues within the existing authorization. A genuine external permission blocker records the waiting condition and owner. The table neither grants permissions nor repeats settled product approvals.

S work receives no new required artifact. Completed historical documents are not retrofitted. The guidance preserves existing technical review, gate authority and independent QA.

Static scenarios can verify the template and rule presence; they cannot prove that a live model followed the guidance or delivered a measured efficiency improvement.

## Version, protocol and publication strategy

Select unpublished Kit candidate 0.11.0.

Retain:

- core protocol 7;
- Codex adapter protocol 7;
- Hermes adapter protocol 1;
- Agent-install schema/protocol 4/4;
- CLI result schema 2;
- takeover schema 2;
- maintenance bridge schema 2;
- compatibility migration registry schema 2;
- release manifest schema 2;
- transaction journal/commit schemas 1/1;
- feedback protocol 2.

Execution metadata has independent schema 1. Final verification retains existing statuses, outcomes, skipped reasons and output.full shape. Progress timestamps/run IDs never enter final envelopes. The corrected receipt guarantee is an explicit documentation amendment, not an unversioned new schema-2 field.

Reopen readiness if implementation needs a new final-result field, enum, Agent-install shape, host responsibility or recovery mode.

Advance current Kit/version mirrors together. Move the bridge's exclusive upper bound to 0.11.0, retarget only the existing exact v0.5 predecessor migration and regenerate its compiled digest/mirrors. Preserve eligibility and predecessor hashes. Historical records remain fixed.

### Exact publication schema 6

The compiled profile is exclusively:

```text
schema: 6
profile: vibe-kit-v0.11.0-prerelease
repository: mintgao/vibe-kit
version: 0.11.0
tag: v0.11.0
title: Vibe Kit v0.11.0
body_path: docs/releases/0.11.0.md
direct: vibe-kit-0.11.0.zip
distribution: vibe-kit-distribution-0.11.0.zip
plugin: vibe-kit-plugin-0.11.0.zip
```

Use a non-draft Pre-release, no generated notes and exactly five assets: SHA256SUMS/checksum, release-manifest.json/manifest, direct, distribution and plugin.

Keep the six ordered publication operations exactly:

1. fast-forward-main;
2. create-or-confirm-annotated-tag;
3. create-or-confirm-prerelease;
4. upload-or-confirm-five-assets;
5. read-back-publication;
6. download-and-verify-public-assets.

Their existing authorization, precondition, ledger, retry, uncertainty and reconciliation semantics remain. Closeout is not a publication operation.

The exact issue policy is:

```json
{
  "mode": "after-public-verification",
  "issues": [14, 15, 16, 17, 18],
  "allowed_operations": ["create-exact-evidence-comment", "close-issue"]
}
```

Publication receipt issue_closeout remains null.

### AC-10 phase mapping and exact acceptance constants

Split only the evidence mapping of the existing combined AC-10:

- AC-10.1: local review, final QA, Python/release gates, deterministic builds and both homepage reviews;
- AC-10.2: confirmed publication, live read-back, five public downloads, release validation, exact public smokes and final offline publication validation;
- AC-10.3: subsequent separately scoped #14–#18 issue closeout, with each issue closed only after its mapped improvement and the parent publication have been verified.

This does not expand product scope. Overall work-item AC-10 is complete only when all applicable parts pass. Publication acceptance deliberately excludes AC-10.3.

The schema-6 states mapping has this exact insertion order:

```json
{
  "AC-1": "passed",
  "AC-2": "passed",
  "AC-3": "passed",
  "AC-4": "passed",
  "AC-5": "passed",
  "AC-6": "passed",
  "AC-7": "passed",
  "AC-8": "passed",
  "AC-9": "passed",
  "AC-10.1": "passed",
  "AC-10.2": "not-runnable-before-publication",
  "AC-10.3": "not-runnable-before-publication"
}
```

The requirements mapping has the same insertion order:

```json
{
  "AC-1": "none",
  "AC-2": "none",
  "AC-3": "none",
  "AC-4": "none",
  "AC-5": "none",
  "AC-6": "none",
  "AC-7": "none",
  "AC-8": "none",
  "AC-9": "none",
  "AC-10.1": "none",
  "AC-10.2": "live-read-back",
  "AC-10.3": "issue-closeout"
}
```

post_criteria is exactly:

```json
["AC-1", "AC-2", "AC-3", "AC-4", "AC-5", "AC-6",
 "AC-7", "AC-8", "AC-9", "AC-10.1", "AC-10.2"]
```

Receipt-kind mapping is exactly:

```json
{
  "prepublication-qa": "vibe-kit-v0.11.0-prepublication-qa",
  "configured-checks": "vibe-kit-v0.11.0-configured-checks",
  "python-3.9": "vibe-kit-v0.11.0-python-3.9",
  "clean-build": "vibe-kit-v0.11.0-clean-build",
  "release-gate-evidence": "vibe-kit-v0.11.0-release-gate-evidence",
  "postpublication-acceptance": "vibe-kit-v0.11.0-postpublication-acceptance"
}
```

These local receipt schemas remain 1 and inherit their existing closed fields. Prepublication QA does not claim the two future phases passed. Postpublication acceptance requires precisely the eleven post_criteria passes and their actual evidence.

The exact ordered public smoke set is:

```text
public-direct-init-doctor
public-plugin-bundled-plan-init-doctor
public-upgrade-v0.3-to-v0.11.0
public-upgrade-v0.5-to-v0.11.0
public-upgrade-v0.6-to-v0.11.0
public-upgrade-v0.7-to-v0.11.0
public-upgrade-v0.8-to-v0.11.0
public-upgrade-v0.9-to-v0.11.0
public-upgrade-v0.10.0-to-v0.11.0
public-upgrade-v0.10.1-to-v0.11.0
public-repeat-upgrade-v0.11.0
```

The repeat smoke initializes from the public 0.11.0 payload, performs two same-version upgrades and checks truthful successful transaction results, healthy doctor and no active residue. Upgrade smokes prove installation behavior, never activation.

### Publication authorization and historical profiles

Schema-6 publication authorization retains the exact nine fields inherited by schema 5: authorization_id, repository, version, release_kind, allowed_operations, publication_intent_sha256, host_operation_id, authorization_source_ref and bound_at.

authorization_source_ref binds existing user authorization. bound_at records the executor's subsequent binding. Structural validation does not authenticate consent. Do not add a requirement for a later conversational reapproval when existing authorization already covers the exact operation. A changed material scope still requires the applicable decision.

The earlier rejected feedback egress is historical and is not retried by this release. The exact approved suggestion bodies are already published as #16–#18. Release and issue-closeout authorization remain separately bound; neither creates another feedback submission.

Publication intent/receipt schemas become 6 in current mirrors; historical profiles 1–5 retain exact identities, acceptance sets and verdicts. Audit all profile-conditioned authorization, asset, natural-key, release-gate and dispatcher checks. Unknown/cross-profile inputs fail closed. No string rewriting, version aliasing or historical-profile repurposing is permitted.

### Exact separate closeout schema 4

Add a new closeout profile, not a reuse of an historical graph:

```text
intent/receipt schema: 4
repository: mintgao/vibe-kit
version: 0.11.0
parent publication schema: 6
ordered issues: [14, 15, 16, 17, 18]
```

The intent retains the current closed field set: schema_version, kind, closeout_id, parent_publication_intent_sha256, publication_receipt_sha256, verification_receipt_sha256, repository, issues, remote_snapshot, operations and authorization_scope.

The closeout ID is canonical JSON SHA-256 of exactly schema_version=4, repository, version=0.11.0, parent_publication_intent_sha256 and issues=[14,15,16,17,18].

Use exact markers:

```text
<!-- vibe-kit:v0.11.0:issue-14:<closeout-id> -->
<!-- vibe-kit:v0.11.0:issue-15:<closeout-id> -->
<!-- vibe-kit:v0.11.0:issue-16:<closeout-id> -->
<!-- vibe-kit:v0.11.0:issue-17:<closeout-id> -->
<!-- vibe-kit:v0.11.0:issue-18:<closeout-id> -->
```

The ordered ten operations are:

```text
0: issue-14-comment — create-exact-evidence-comment
1: issue-14-close   — close-issue
2: issue-15-comment — create-exact-evidence-comment
3: issue-15-close   — close-issue
4: issue-16-comment — create-exact-evidence-comment
5: issue-16-close   — close-issue
6: issue-17-comment — create-exact-evidence-comment
7: issue-17-close   — close-issue
8: issue-18-comment — create-exact-evidence-comment
9: issue-18-close   — close-issue
```

Carry forward the existing closed per-operation fields, monotonic observations, natural-key construction, max_write_attempts=2 and exact read-back/idempotency behavior, parameterized by the new identity. Destructive operations remain false.

Authorization fields are exactly closeout_authorization_id, repository, issues, allowed_operations, closeout_intent_sha256, destructive_operations_allowed, authorization_source_ref and bound_at. Allowed operations are exactly create-exact-evidence-comment and close-issue. Bind existing authorization covering that separate scope; ordinary publication authorization alone does not widen to it.

The receipt fields remain exactly schema_version, kind, closeout_id, closeout_intent_sha256, closeout_authorization_id, overall_state and items, with schema_version=4 and the inherited closed item field sets/outcomes.

Parent validation requires the exact schema-6 intent/receipt/authorization, confirmed-complete public writes, passed publication verification, valid matching validate-publication result and passed postpublication acceptance over post_criteria. Bind all referenced canonical digests and executor identities. It never requires AC-10.3 before closeout.

Issue #14 evidence binds AC-1; #15 binds AC-2 and the published repeat smoke; #16 binds AC-3/AC-4; #17 binds AC-5/AC-6; #18 binds AC-7/AC-8. The #18 evidence remains bounded static contract/scenario evidence and makes no live-model compliance claim. Execute each exact evidence comment and then its issue closure only after checking that issue's mapped evidence and the validated parent publication. A completed pair records only that issue as closed; unfinished or uncertain items remain non-passing. Complete closeout requires exact comment identities and closed-state read-back for all five ordered issues. Record AC-10.3 only afterward.

Keep historical closeout schemas 1–3, issue lists, parent bindings and markers unchanged. Update current issue-closeout schema mirrors to 4 and add an explicit schema-6 parent dispatch; reject cross-parent/schema combinations.

Record AC-10.2 publication acceptance in `docs/work-items/20261010-feedback-closure/postpublication.md` and AC-10.3 issue closure separately in `docs/work-items/20261010-feedback-closure/closeout.md`. The closeout record maps each of the five issues to its verified criterion evidence, exact authorized comment identity, and closed-state read-back, and references the bound intent/authorization/receipt digests. These Markdown records are audit summaries, not new receipt fields or schemas; public summaries do not copy private logs or host goal/custody payloads.

After remote writes, reconcile only the same exact authorized intent; divergence blocks. Defining these profiles is not a claim that publication or issue closure occurred.

## Alternatives

- Globally comparing postimage first: rejected because equal images also satisfy rollback's predecessor obligation; consumers need expectation-specific predicates.
- Filtering equal journal entries or returning early on version equality: deferred because it changes race observation and transaction evidence beyond the necessary fix.
- Reusing --receipt for both publication directions: rejected because input ownership remains ambiguous.
- Allowing publication result overwrite after alias preflight: rejected because a competing create can defeat a check-then-overwrite guard.
- Increasing only the tail limit: rejected as the success-log solution because it remains a bounded summary.
- Always retaining complete successful output: rejected because it changes default privacy and disk retention.
- Streaming to raw temporary logs: rejected because it creates a new raw-evidence persistence boundary and requires a separate streaming sanitizer design.
- Treating progress or an exited shell as acceptance/cancellation proof: rejected because neither proves completed checks or stopped descendants.
- A scheduler or retrospective rewrite of all work items: rejected as unnecessary scope expansion.
- Reusing the 0.10.1 publication profile: rejected because exact version, tag, assets and issue policy differ.

## Verification required

These are required scenarios, not reported results:

1. AC-1: valid, invalid and malformed publication receipts remain byte-identical. Test no-output and distinct create-only output, relative/resolved/symlink/hard-link/case-insensitive aliases, candidate descendants, competing final creation, parsing failures, repeated main calls and nested validators.
2. AC-2: repeated same-version and mixed changed/equal upgrades, mode drift, byte-identical inode replacement, genuine divergence, failure before commit and interrupted cleanup after durable commit. Preserve the existing predecessor rollback and committed-pair proofs.
3. AC-3: more than 16 KiB of successful stdout/stderr retains first/last evidence only when selected; failures/environment-limited remain retained. Verify complete layout bytes, byte count, digest, content-addressed reuse and concurrent publication.
4. AC-4/R1/R3/R5: all four progress/log-policy combinations; default successful runs leave no output body on disk; disabled progress creates no runs/locator; selected logs remain available with progress off. Test explicit receipt selection/failure separately. Compare fixed-output receipts across runs/project parents. Exercise unsafe/read-only/full destinations, permissive umask, modes, hard links, Git exclusion, controls, private keys and secrets split across writes.
5. AC-5: silent and output-producing slow checks expose before-check metadata; concurrent runs remain distinct; stdout is one final JSON result. Validate locator grammar, last-successfully-published ordering under reversed concurrent publications, caller-specific startup discovery, and stale-discovery semantics.
6. AC-6/R2: process-start failure, handled SIGINT/SIGTERM, runner error, SIGKILL, completed earlier checks and never-started remaining checks. Test incomplete runs both without and with an explicitly persisted blocked receipt, and surviving descendants without a cancellation claim.
7. AC-7/AC-8: synthetic source Pass/API Blocked/export Unverified coverage includes references, next actions, role owners and waiting conditions. Preserve S/history, readiness/QA and host custody boundaries; do not claim live-model compliance.
8. AC-9/R2: unknown/duplicate fields, invalid enums/nullability/bounds/timestamps/paths, invalid metadata checksum, mismatching supplied envelope and changed artifact digests fail closed. Missing or disabled metadata does not invalidate an independently complete existing verification receipt. Preserve historical publication/closeout acceptance and rejection and Python 3.9/offline boundaries.
9. AC-10.1: revised decision approval, one writer's focused checks, independent final-candidate default QA, justified specialized Python/release gates, two clean deterministic builds and both homepage reviews.
10. AC-10.2: exact schema-6 acceptance constants, all eleven public smokes, live publication/read-back/downloads and final offline validation. Demonstrate that publication acceptance is obtainable without closeout.
11. AC-10.3: exact schema-4 ordered [14,15,16,17,18] graph, per-issue AC evidence mapping, parent/digest authorization binding, wrong-parent/issue/order/marker rejection, uncertain/idempotent resume, honest partial closeout and separate complete closeout evidence.

The orchestrator's supplied baseline onboarding verification is source-baseline evidence, not final-candidate QA.

## Migration, rollback and remaining risk

No project configuration, historical receipt or historical evidence is migrated. New diagnostic data is ignored local state and can remain after a source rollback without becoming acceptance evidence.

Before publication, revert the source change and rebuild disposable unpublished candidates. Projects opting into new config keys must remove those keys before using an older parser; older binaries must continue rejecting unknown declarations.

Installation rollback and interrupted upgrades continue under ADR0010. Old binaries may retain the same-version classification defect; this change does not retroactively repair them.

After remote publication writes, reconcile only the same exact authorized intent. Never force-push, move tags, replace assets or delete a Release as automatic recovery. Changed bytes invalidate frozen candidate evidence.

Residual limits are complete-output memory/disk cost, pattern-based sanitization, unavailable diagnostic storage, unhandled crash finalization, and unproven descendant cancellation. None authorizes a passing acceptance claim without its required evidence.

No unresolved material product choice remains within this decision. Implementation remains blocked until this exact persisted adoption revision is independently reviewed, accepted, and the orchestrator confirms readiness. Publication acceptance and complete issue closeout remain separately evidenced later phases.
