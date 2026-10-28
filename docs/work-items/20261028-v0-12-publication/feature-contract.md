# Public feature contract: exact onboarding, real-entry evidence and read-only inspection

This document preserves the accepted F1-F3 semantics for the public 0.12.0 projection. [Brief](brief.md) AC-1 through AC-4 and [ADR0023](../../decisions/0023-readonly-run-inspection-and-entrypoint-evidence.md) govern feature behavior; [ADR0024](../../decisions/0024-v0-12-publication-and-separate-closeout.md) governs its later publication lifecycle. Fresh independent review and verification belong to this public candidate; no earlier local receipt is rebound.

## F1: one exact onboarding version predicate

Change the existing object/version guard only: a mapping with type(schema_version) exactly int and value 1 is supported. Reject true/false, 1.0, other floats, strings, null, missing version, 0/2 and non-object roots through the existing invalid_onboarding_state boundary. Keep the rest of pending/refresh-needed/complete rules. In particular complete still requires the existing date/evidence checks and missing state retains its existing review-required/legacy-bridge behavior.

All consumers continue calling onboarding_readiness: no separate doctor, upgrade or project-kind predicate. Exercise helper plus real doctor and read-only plan upgrade preflight. Invalid state bodies must not enter error output. The current decode error text exposes parser location rather than the JSON body; tests should use a distinctive private body marker and verify it is absent, without expanding this patch into unrelated parser/schema changes.

## F2: bounded affected-entry evidence

Add applicable guidance and one reusable example to implementation/verification Skills and the relevant handoff/verification template or documentation. For shared helper/adapter changes, the sender supplies this finite slice:

| Configured check | Actual default entry | Affected live caller/helper | Observed origin/arguments | Focused command/result | Preserved historical caller |
|---|---|---|---|---|---|
| test | project discovery/script | bounded project path/name | runtime observation | project command and evidence | path/assertion, or none |

Use only affected entry points and explain why the slice is sufficient. Static rg/import inspection assists discovery; actual focused execution supplies proof. The project owns imports, probes and assertions. No generic graph builder, launcher, new core configuration or mandatory S artifact is added. When no shared entry changes, mark the slice inapplicable without inventing a table. Historical callers/tests remain unchanged unless separately approved.

Python fixture: new helper direct unit test passes while a discovered live observer still imports the old helper. Execute the default discovery machinery with a bounded file pattern selecting the real observer; assert loaded origin and actual arguments, so it fails before full QA. Correct only the reviewed live import/adapter; direct helper, observer and unchanged historical tests then pass.

Node fixture: package.json has a real test script invoking the live adapter. Use the project's actual package-script dispatcher and focused arguments; a direct new-helper test passes while stale adapter origin/arguments fail. Correct only that adapter and rerun focused script plus preserved historical assertion. Use an existing Node runtime and its real package-script dispatcher; Node --run may execute the real package.json test script without installing npm. Test/runtime discovery may accept CODEX_TASK_WORKSPACE_NODE as an explicit portable selector and otherwise shutil.which('node'). No machine-specific runtime path belongs in shipped core. If no runtime or package dispatcher is available on another host, record that scenario not executed/Blocked; never count a skip as the required local Node acceptance Pass.

## F3: consumer pipeline and complete receipt profile

The command is inspect-run <target> --run-id <id> [--final-receipt <path>] with text/json format. Both identities are explicit; no locator/latest option is needed for this slice. Keep --final-receipt out of the generic output-receipt allowlist. The command never calls verify, doctor, observe_toolchain, subprocess, Git, project shell commands or network tools.

1. Validate the run grammar. Absolute-lexically normalize the explicit target and traverse every existing directory component with open_existing_directory_nofollow; reject a symlinked target or ancestor. Hold this root descriptor for all project reads. Factor the existing read_verify_execution snapshot read/strict-parse/schema/run-ID portion into a narrow shared internal helper accepting an already-open private store; keep the public wrapper behavior unchanged. Inspect uses that helper with a store anchored by a duplicate of its pinned root descriptor, without artifacts=True and without resolving the target through symlinks. Keep its bounded findings. Do not parse project.yaml or load project modules.
2. Choose one receipt: explicit input wins; otherwise only valid metadata's available project receipt path is eligible. An external receipt requires explicit input. A failed explicit read never falls back. Invalid/missing metadata cannot choose a receipt path but must not prevent independent validation of a supplied receipt.
3. Safely read at most 1,048,576 bytes and strict-parse JSON. Validate the complete CLI receipt profile below before projecting any fact. Retain raw byte SHA-256 and canonical root-relative envelope SHA-256 separately.
4. With valid metadata and receipt, normalize the envelope with root_relative_receipt against the captured lexical root, then call existing pure validate_verify_execution(snapshot, normalized_envelope) without re-resolving a filesystem root; verify any recorded available receipt raw hash. Match also selection, effective order, check outcomes and output.full references as the existing validator requires. A not-requested receipt has no recorded raw hash, but an explicitly supplied wrapper receipt can still bind through the canonical envelope hash. The output binding=matched means internal correspondence only. In explicit receipt mode, compare the selected explicit bytes against any recorded available raw hash but never reopen the metadata's original project receipt path. Report inspection-original-receipt-path-not-inspected when that project path exists in valid metadata; this is informational, not an integrity failure. A byte-identical safe explicit copy can bind even if the original slot is missing. Its existence/integrity is not claimed. When no explicit receipt is supplied, the selected metadata project path itself must be safely read and checked. Never fall back from a bad explicit receipt.
5. Select exactly one artifact set before any log read. A complete valid selected receipt owns the set, even if metadata is missing, invalid or unbound: inspect only that receipt's output.full references, at most one per selected check and four total, and report artifact_scope=receipt. Otherwise, valid metadata owns its available log references and artifact_scope=metadata; with neither valid source, use artifact_scope=none and an empty artifacts array. Never union sets or read a second identity for a conflicting check. A receipt/metadata reference disagreement is a binding mismatch: inspect the receipt-owned set, report inspection-metadata-artifacts-not-inspected, and leave metadata artifact integrity unclaimed. The independent receipt verdict depends only on its validated body and its selected verified logs, so it may remain passed while the run verdict is unverified and top-level status invalid/exit 1. If binding matches, references are identical and the one set verifies both. Verify the chosen set through bounded constant-memory hashing. Never dereference arbitrary unvalidated paths or external logs.
6. Compute coverage/verdicts independently, project safe facts, emit one bounded result, and close descriptors. Never create a file, directory, ignore rule or cache from this command. Do not repair/clean/trim evidence.

The new complete receipt validator is deliberately narrow: current CLI-produced complete verify schema-2 receipts under ADR0017/0022. It is not a general historical receipt migration or publication validator. Other historical/host shapes keep their meaning; unsupported shapes cannot establish an inspect-run pass.

Exact top-level receipt fields are schema_version, command, status, target, selection, producer, cli_invoked, default_order, toolchain, checks, summary. Require exact integer schema 2, command verify, producer cli, cli_invoked exactly true, and current status passed/failed/blocked/error. After existing root_relative_receipt normalization, target must be '.': a foreign absolute target is not accepted. A root-relative '.' is not origin attestation.

Validate default_order as the four unique known check names in effective order. selection is the existing exact mode/requested/coverage object: default/[]/all-configured or only/nonempty unique ordered known names/partial. checks must exactly match that ordered selection, not merely contain test. Each check has the current exact fields name, configured, applicability, required, outcome, exit_code, reason_code, provenance, output, plus environment only for environment-limited. configured/required are exact booleans and agree; applicability agrees with configured. Provenance is the existing CLI shape kind=cli, task_id=null, operation_id=null.

Allowed CLI combinations are unconfigured/false/null exit/not-configured; passed/true/0/null; failed/true/nonzero/null; environment-limited/true/nonzero/toolchain-mismatch plus existing environment details; skipped/true/null exit/process-start-failed or execution-interrupted. Exits are exact signed 64-bit integers, never bool. Output is the existing four tail/truncation fields plus optional full={path,sha256}; strings/booleans retain their types, full is only for complete process outcomes and uses the exact content-addressed project log path/digest. Never echo tails. toolchain has exactly python/node/pnpm with nonempty strings or null, and text values at most 4096 characters; environment retains exact expectations/observed maps over those tool names, expected/observed pairs and nonempty bounded expectation strings. Missing or unknown fields, wrong types and nonfinite/duplicate JSON fail closed.

summary has exactly passed/failed/unconfigured/skipped/environment-limited, each an exact integer 0..4 matching actual counts. passed status requires only passed/unconfigured outcomes; failed requires failed and no skipped/environment-limited. blocked is accepted with otherwise valid check combinations, including all observed passed outcomes, because terminal delivery interruption is valid existing behavior; its original blocked status is never promoted. error is never passing. The consumer does not invent a new producer invariant that rejects valid error/blocked terminal receipts.

## Public inspection result

The exact new command result is the common schema-2 header plus one nested object:

```text
{schema_version: 2, command: "inspect-run",
 status: "inspected" | "invalid" | "error",
 inspection: {
   schema_version: 1,
   run_id: valid requested run ID | null,
   metadata: {state, run_state, result_status, updated_at, metadata_sha256},
   receipt: {state, source, result_status, sha256, envelope_sha256},
   binding,
   coverage,
   artifact_scope: "receipt" | "metadata" | "none",
   artifacts: [{check, state, sha256, bytes}],
   historical_receipt_verdict,
   historical_run_verdict,
   candidate_applicability: "unproven",
   project_origin: "not-attested",
   liveness: "not-assessed",
   findings: [{code, path}],
   next_actions: [action code]
 }}
```

All listed fields are required; unknown fields are forbidden. metadata.state is valid/missing/invalid/unavailable. run_state is running/incomplete/finished/null. result_status is passed/failed/blocked/error/null. updated_at and metadata_sha256 are validated values only, otherwise null. No snapshot body, recorded receipt path or free-text field is copied.

receipt.state is valid/missing/not-supplied/invalid/unavailable. source is explicit/metadata-project/null. result_status is the fully validated original status or null; sha256 is the actual safely read receipt-byte digest or null; envelope_sha256 is the validated canonical root-relative envelope digest or null. Invalid bodies expose no status/content. A readable but invalid body may retain only its actual byte hash.

binding is matched/mismatch/unavailable. coverage is all-configured/partial/unknown, derived only from a complete valid receipt. artifact_scope identifies the single selected source as receipt/metadata/none under pipeline step 5; it does not assert both sources were inspected. artifacts contains at most four known check names in that source's validated effective selection order, one identity per check; a differing unselected metadata set is never read or represented as verified. state is verified/not-referenced/unavailable/invalid; sha256 is a validated digest or null and bytes is a nonnegative verified count or null. Available but oversized/unreadable artifacts are unavailable, never verified. Full-body metadata errors never expose input values through artifact records.

Each historical verdict is passed/not-passed/unverified. historical_receipt_verdict=passed requires a complete default/all-configured passed receipt with all configured outcomes passed, correct summary and every referenced log verified; metadata is not required for this independent historical fact. historical_run_verdict=passed additionally requires valid finished/passed metadata and binding=matched. Valid partial or non-passing evidence is not-passed for default acceptance. Missing, invalid, unbound or unfinished evidence is unverified; a matching incomplete blocked/error run is not-passed. No current-candidate pass exists in this result.

At most 64 findings contain fixed rule codes and fixed schema-field paths, never values, user key names, absolute paths or exceptions. Use existing execution-* findings for metadata, plus fixed inspection-* codes for run/target/receipt-shape/receipt-size/receipt-unavailable/receipt-binding/original-receipt-path-not-inspected/metadata-artifacts-not-inspected/artifact-size/artifact-integrity/coverage-partial/envelope-not-supplied/current-candidate-unproven/unsupported-filesystem/internal-error as applicable. A registry and drift tests freeze the actual chosen codes before final QA. next_actions is a deduplicated ordered array of at most eight fixed codes drawn from supply-final-receipt, recover-existing-evidence, inspect-evidence-finding, assess-current-candidate, review-nonpassing-result and await-owned-run-evidence. It never commands a rerun or process action.

Exit rules:

| Status / exit | Meaning |
|---|---|
| inspected / 0 | Valid metadata was inspected and the selected receipt/artifact scope has no integrity failure. Explicit mode does not attest the unselected original receipt slot; informational not-inspected findings do not fail this status. Missing optional final envelope, partial coverage and original failed/blocked/error runs remain explicit gaps/non-passes. |
| invalid / 1 | Invalid/missing required run metadata, invalid explicit receipt, mismatch, or missing/unreadable/oversized evidence within the selected receipt/artifact scope. A valid independent receipt is still separately reported. |
| error / 2 | Invalid/unopenable target, unsupported required filesystem primitives, or an internal processing failure prevents the safe inspection operation. |

Invalid run syntax produces invalid/1 with run_id=null. Normal argparse usage failures retain conventional exit 2; evidence parsing/read errors stay inside the bounded command handler and never reach generic raw-exception output. JSON emits exactly one result; text emits the same safe facts. The encoded result is at most 32768 bytes, with bounded arrays, projections and field lengths. Add current AGENT_COMMAND_STATUSES/agent-install.cli.command_statuses entries for inspected/invalid/error and a closed cli.inspect_run declaration: result_schema_version=2, inspection_schema_version=1, statuses=[inspected,invalid,error], authority=historical-evidence-only, side_effects=none. The existing verify declaration is byte-semantically unchanged.

## Safe read implementation bounds

Receipt maximum is 1 MiB, log maximum 64 MiB each, at most four logs, hash buffer 64 KiB. These caps bound inspection only; verify's configurable tails and retention are unchanged. A size limit is an evidence gap, not proof the historical execution failed and not an automatic rerun instruction.

Reuse ProjectRootFD directory traversal, VerifyPrivateStore private_object and existing no-follow primitives. Add only narrow pinned-descriptor support/shared internal reads needed to anchor this consumer; do not change existing callers' default semantics. Never perform a fresh path-based reopen of project evidence after pinning the root. A pathname replacement must not redirect later reads away from the pinned directory. If extending read_verify_project_receipt, add a keyword-only maximum=None and preserve callers' defaults. Inspect passes the explicit bound and checks both initial size and bytes as read. An explicit receipt lexically within the captured project root is read relative to the same pinned root descriptor. External explicit final-receipt paths use absolute lexical normalization plus open_existing_directory_nofollow; never resolve a symlink and then open its referent. Both readers require current owner, 0600 regular one-link leaf, O_RDONLY/O_NOFOLLOW/O_NONBLOCK, and stable device/inode/mode/uid/link/size/mtime/ctime before/after. Streaming log hashing uses the same pinned store/identity rules and compares bytes/count/digest; it does not return log bodies. Existing project-store parent mode rules remain. All descriptors close on every failure, including recursive/malformed JSON and MemoryError where reportable.


## Acceptance and deferred scope

Independent QA verifies the brief criteria through the production CLI and focused executable scenarios. Default/partial/blocked/error receipts, bounded selected artifacts, real interruption, genuinely different wrong-run evidence, no-follow/resource/privacy boundaries and explicit-copy original-slot non-read retain their separate verdicts. RD runs focused checks; QA owns the complete default run for each unchanged final candidate. Static evidence does not establish live host compliance, source applicability, copied-evidence provenance or descendant cancellation.

Issues #21 and #26 remain assessment-only; #24 and #25 remain deferred. No candidate-lineage, outcome-rollup, general output-policy or execution-profile feature is added. Historical producer and publication contracts retain their meaning.
