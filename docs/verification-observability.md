# Local verification observability

This describes local verification in the unpublished Vibe Kit 0.12.0 source candidate. Execution metadata is diagnostic;
independent acceptance still requires the complete applicable verification result.

## Settings and final results

```yaml
checks:
  requires:
    test: ["lint"]
  output_limit_bytes: 16384
  log_policy: "failures"
  progress: true
```

Missing diagnostic settings resolve to `failures` and `true`. Policies are exactly
`failures` and `all-configured`; progress accepts only JSON-style booleans.
Duplicate declarations, unknown keys/values and dependency cycles fail before
checks start. Use independent overrides:

```text
./bin/vibe verify . --format json --log-policy all-configured --no-progress
./bin/vibe verify . --format json --progress --receipt verification.json
```

`--receipt` explicitly persists the bounded result; no automatic `result.json` or
other envelope copy exists. Serialization uses UTF-8, ensure_ascii=False, sorted
keys, indent=2 and one terminal LF. Equal root-relative envelope values produce
equal bytes; changing process output/toolchain/transaction evidence can change
receipts. Progress IDs and timestamps never enter final schema-2 envelopes.

| Progress | Log policy | Persistence |
| --- | --- | --- |
| true | failures | Metadata; complete failed/environment-limited logs |
| true | all-configured | Metadata; complete successful/failed/environment-limited logs |
| false | failures | Complete failed/environment-limited logs; no runs or locator |
| false | all-configured | Complete configured logs; no runs or locator |

Capture remains in memory until a complete process result. Exact UTF-8 log bytes
are `"=== stdout ===\n" + sanitize(stdout) + "\n=== stderr ===\n" + sanitize(stderr)`.
No trimming or chronological interleaving is implied. SHA-256 H identifies
`.vibe/local/verify/logs/sha256/<H>.log`; verified references keep existing
`check.output.full={path,sha256}`. Concurrent identical producers may reuse only
exact safe bytes. Never-started/interrupted captures do not create complete logs.

Sanitization processes complete streams before logs and tails, strips unsafe
controls/ANSI, replaces invalid UTF-8, redacts supported credentials and entire
recognized private-key blocks, including unterminated blocks through end of
stream, and rewrites root aliases. It does not discover every secret and does not
read environment values. Logs remain private and are not public feedback evidence.

## Discovery and safe consumption

Startup stderr identifies the caller's `verify-<32 lowercase hex>` run and
progress path, or disabled/unavailable state, plus effective policy. Selected log
notices contain bounded availability/identity only. Every notice is at most 2048
UTF-8 bytes; completed stdout delivery contains one final JSON result.

Snapshots are `.vibe/local/verify/runs/<run-id>/progress.json`. The bounded
`latest.json` locator points to the run whose locator write was last successfully
published, which may differ from start-time order. It never implies current
liveness, completion or acceptance. Use your startup run ID when tracking your own
invocation.

Use the explicit public consumer for an existing run:

```text
./bin/vibe inspect-run . --run-id verify-<startup-id> --format json
./bin/vibe inspect-run . --run-id verify-<startup-id> --final-receipt .vibe/local/verify/receipts/qa-unique.json --format json
```

Target and startup run ID are required. There is no implicit latest lookup,
rerun, repair, process control or liveness probe. `--final-receipt` is read-only
input; relative explicit paths follow the invocation working directory. Without
it, only an available project receipt selected by valid metadata is read.
External receipts always require an explicit path. A bad explicit input never
falls back. The original metadata receipt path is not reopened in explicit mode:
a safe byte-identical copy can bind even if the original slot is gone, and the
informational `inspection-original-receipt-path-not-inspected` finding discloses
that limit. The original slot's existence/integrity is not attested.

A complete valid selected receipt owns the only artifact set. Otherwise valid
metadata owns its available logs; otherwise the set is empty. `artifact_scope`
is `receipt`, `metadata` or `none`. At most four references in selected check
order are hashed, without reading a second conflicting identity. Conflicting
metadata references produce a binding mismatch and
`inspection-metadata-artifacts-not-inspected`. The independent receipt verdict
can still pass after its own logs verify; the run verdict remains unverified.

The schema-2 result has exactly `schema_version`, `command`, `status`,
`inspection`. Its nested schema 1 has exactly: `schema_version`, `run_id`,
`metadata`, `receipt`, `binding`, `coverage`, `artifact_scope`, `artifacts`,
`historical_receipt_verdict`, `historical_run_verdict`, `candidate_applicability`,
`project_origin`, `liveness`, `findings`, `next_actions`.

- Metadata projects only state, last run state, original result status, validated
  update time and metadata digest. Receipt projects only state/source, original
  status, actual byte digest and canonical root-relative envelope digest.
- Binding is matched/mismatch/unavailable, coverage all-configured/partial/unknown.
  Artifacts project check/state/digest/verified byte count only; bodies and paths
  are absent. Historical verdicts are passed/not-passed/unverified.
- A historical receipt pass needs a complete CLI schema-2 default/all-configured
  passed receipt, exact summary and every referenced log verified. A run pass also
  needs valid finished/passed metadata and matched binding. Partial coverage and
  original failed/blocked/error results remain non-passing. Missing/invalid or
  unbound evidence remains unverified.
- `candidate_applicability=unproven`, `project_origin=not-attested` and
  `liveness=not-assessed` are unconditional. Hash binding is correspondence, not
  provenance: copying an identical consistent root-relative evidence set cannot
  be detected. Current source changes do not acquire a historical pass.

| Status / exit | Meaning |
|---|---|
| inspected / 0 | Valid metadata and no selected evidence integrity failure; optional missing envelope and partial/non-passing original results remain explicit gaps. |
| invalid / 1 | Required metadata missing/invalid, selected evidence unavailable/invalid, or binding/integrity mismatch. Independent receipt facts remain separate. |
| error / 2 | Unsafe/unopenable target, unsupported filesystem primitives or internal safe-processing failure. |

Inspection pins the lexical root using component-wise no-follow traversal; all
project reads retain that root descriptor. Receipt inputs are at most 1 MiB;
logs at most 64 MiB each, hashed in 64 KiB chunks. Declared and observed bounds
are enforced. Private regular one-link 0600 leaves require current ownership and
stable device/inode/mode/owner/link/size/mtime/ctime. Project-store parent rules
remain unchanged. Symlinks and unsafe types/modes/owners fail closed. No parent,
ignore rule, cache or evidence is created or modified. These are consumer limits;
producer retention and receipt behavior are unchanged. Unsupported/oversized
input is a gap, never proof the historical execution failed or an instruction to
rerun checks.

Complete receipts use strict UTF-8 JSON without duplicate keys or nonfinite
numbers. Unknown/missing fields, bool-as-integer versions/exits/counts, invalid
selection/order/outcome/provenance/environment/output or summary fail closed.
Valid error and terminal-delivery blocked receipts keep their original status.
The old `read_verify_execution`, `validate_verify_execution` and locator APIs
remain available with their existing defaults; their optional artifact reads are
not the bounded public inspection interface.

Findings are at most 64 fixed codes/field paths; output is at most 32768 UTF-8
bytes and never contains tails, commands, exceptions, user keys, absolute paths,
toolchain free text or bodies. Existing `execution-*` codes describe metadata.
The closed new registry is:

```text
inspection-run, inspection-target, inspection-receipt-shape,
inspection-receipt-size, inspection-receipt-unavailable,
inspection-receipt-binding, inspection-original-receipt-path-not-inspected,
inspection-metadata-artifacts-not-inspected, inspection-artifact-size,
inspection-artifact-integrity, inspection-coverage-partial,
inspection-envelope-not-supplied, inspection-current-candidate-unproven,
inspection-unsupported-filesystem, inspection-internal-error
```

Next actions are at most eight deduplicated fixed codes from
`supply-final-receipt`, `recover-existing-evidence`, `inspect-evidence-finding`,
`assess-current-candidate`, `review-nonpassing-result`, `await-owned-run-evidence`.
They never request a process action or an automatic rerun.

For a long owned QA invocation, first establish an existing symlink-free private
receipt directory (0700), with the project's ignore coverage (for example a
private `.gitignore` containing `*` and `!.gitignore`). Use a new filename for each
invocation; verify does not create receipt parents. Then, when QA already owns
the authorized canonical run:

```text
./bin/vibe verify . --progress --log-policy all-configured --receipt .vibe/local/verify/receipts/qa-unique.json --format json
./bin/vibe inspect-run . --run-id verify-<startup-id> --final-receipt .vibe/local/verify/receipts/qa-unique.json --format json
```

Progress, complete success logs and explicit receipt persistence are independent
choices. This example does not add an RD full-matrix pre-run. Keep all logs and
receipts private. Checksums detect inconsistency, not a malicious writer with the
same OS principal.

`available` logs have exact path/bytes/digest. Other availability states carry
null identity: pending, not-selected, not-applicable, unavailable, incomplete.
Storage-error reasons are permission-denied, unsafe-path, unsafe-object,
unsupported-filesystem, resource-exhausted or io-error.

## Interruption, privacy and limits

Running records the last observation. Finished means terminal result production,
including failed/blocked/error results. A handled interruption keeps completed
earlier checks, marks started work interrupted and remaining configured work
not-started, and binds only blocked/error output if a result was produced.
Available explicitly requested blocked receipts are allowed; the run remains
incomplete. SIGKILL/crash/power loss may leave running/null-result evidence.

A handled signal during terminal JSON delivery/flush stops the owned output
operation and returns exit 2. Escaped bytes cannot be retracted: stdout can remain
partial/unusable, and no second JSON document is appended. The canonical
interrupted result stays blocked/error in memory, is written only to a safely
available explicit receipt, and can be bound by incomplete progress metadata.
Already completed checks keep their observed outcomes. A stale finished snapshot
or escaped prefix is not complete invocation evidence. Write/flush completion
does not prove downstream receipt or acceptance; no atomic multi-sink delivery or
consumer acknowledgement is promised. A signal after the owned operation has
completed does not retroactively rewrite its evidence.

Scoped SIGINT/SIGTERM handling restores prior handlers, requests termination of
the direct shell, waits at most one second, then requests kill and waits at most
one further second. Reaped proves a successful direct-child wait only. Descendants
remain `not-proven`; inherited pipes never force indefinite interruption cleanup.
Ordinary project checks have no added timeout or process-group manipulation.

New directories are 0700 and evidence files 0600; runs/logs have nested Git
ignores. Unsafe ownership/modes, symlinks, hard links and wrong types are refused.
Optional storage failure leaves check verdicts intact, permits later independent
checks, reports unavailable and never elevates or falls back outside the project.
Progress resource exhaustion during initialization or later publication closes
owned resources and disables that channel; logs and explicit receipts remain
independent. This containment is not a guarantee that a globally exhausted
process can allocate every result or diagnostic message.
Explicit receipt write failure returns schema-2 verify error/exit 2 without a
fallback or recursive write. No automatic expiry, deletion or quota cleanup is
added. Complete capture consumes memory; selected logs can consume disk.

A structurally valid snapshot alone is diagnostic. Even matching passed output
must satisfy the existing full/default configured-check acceptance rules. Missing,
disabled, stale, unavailable or invalid metadata does not invalidate an
independently complete valid verification receipt. Metadata never promotes
missing, partial, interrupted or non-passing evidence to Pass.
