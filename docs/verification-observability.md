# Local verification observability

This describes local verification in Vibe Kit 0.11.0. Execution metadata is diagnostic;
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

The CLI exposes one pure `validate_verify_execution` validator and safe
`read_verify_execution`/`read_verify_locator` readers for maintainers and tests.
For an explicitly persisted result, a trusted local consumer can use:

```python
import json
from pathlib import Path
import runpy

api = runpy.run_path("bin/vibe")
root = Path(".").resolve()
locator, locator_errors = api["read_verify_locator"](root)
if locator_errors:
    raise ValueError("Progress discovery is unavailable")
# Prefer the caller's startup ID when supplied, rather than this discovery locator.
run_id = locator["run_id"]
envelope = json.loads(Path("verification.json").read_bytes())
snapshot, errors = api["read_verify_execution"](
    root, run_id, envelope, artifacts=True
)
if errors:
    raise ValueError("Diagnostic evidence is unavailable or invalid")
```

The safe reader checks private objects without following symlinks, owner/modes,
single-link regular-file identity, 64 KiB snapshot/2 KiB locator bounds, strict
JSON without duplicates/nonfinite values, closed fields/enums/combinations,
numeric major.minor.patch versions without leading-zero components,
calendar-valid UTC microsecond timestamps, metadata checksum, supplied envelope
selection/order/check binding, and requested log/receipt bytes/digests. External
receipt paths are never persisted; pass `external_receipt=<authorized bytes>` to
verify one when supplied. Errors expose bounded rule IDs and field paths only.
Checksums detect inconsistent changes, not a malicious same-OS-principal writer.

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
