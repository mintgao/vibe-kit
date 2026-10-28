# 0023: Inspect historical verification evidence read-only and check affected real entry points

- Status: Accepted
- Date: 2026-10-28
- Decision owner: read-only Tech Lead feature decision, adopted for public projection under ADR0024
- Work item: docs/work-items/20261028-v0-12-publication/brief.md
- Public detailed contract: docs/work-items/20261028-v0-12-publication/feature-contract.md
- Public adoption review: docs/work-items/20261028-v0-12-publication/technical-review.md (fresh public adoption independently approved)

## Context and governing decisions

The approved iteration implements F1/#20, F2/#22 and F3/#23 only. F4/#26 and F5/#21 receive assessment; F6/#24 and F7/#25 remain deferred. The public publication brief owns AC-1 through AC-4 for these adopted feature semantics.

ADR0017 preserves configured verification, effective order, non-passing environment limits and independent QA. ADR0018 owns explicit receipt artifacts and host-only goal/custody. ADR0022 owns execution schema 1, private evidence, complete opt-in logs, the qualified serialization guarantee and diagnostic/acceptance separation. Those decisions remain applicable. This decision adds a consumer; it does not migrate or extend their execution or verify result objects.

Production evidence in `bin/vibe` is decisive: onboarding_readiness uses equality without an exact integer type check; read_verify_execution validates metadata and optional binding but is not a complete final-envelope validator; its artifacts=True path reads logs without a maximum and skips an external receipt when no bytes were supplied. read_verify_project_receipt reads the entire file. A public wrapper cannot simply label that call's empty findings as complete acceptance.

## Decision and scope

Restore the existing onboarding schema-1 gate with `type(value.get("schema_version")) is int` and value 1. Keep one shared onboarding_readiness predicate, existing invalid_onboarding_state errors, persisted state semantics and byte-preserving behavior. Do not introduce a new onboarding schema or automatically repair state.

Make real-entry impact evidence an applicable handoff aid: configured command, actual default entry, affected live helper/adapter, origin and arguments, bounded focused command/result, and intentionally historical callers. Projects own the graph and assertions. A helper unit test or static search is insufficient proof that its default caller uses it. S work receives no mandatory table; RD still runs focused checks and independent QA still owns one complete default matrix per unchanged final candidate.

Add the first public consumer as:

```text
./bin/vibe inspect-run <target> --run-id <verify-id> [--final-receipt <path>] --format json
```

Target and run ID are explicit and required. There is no latest scan, output receipt option, retry, resume, launch, signal, subprocess, toolchain probe or network operation. The new option is input-only and never enters RECEIPT_CONTEXT. Relative explicit receipt paths follow the invocation working directory, as existing verify output destinations do. Recorded project receipt paths follow the explicit target. Text and JSON expose the same bounded facts.

## Result authority and versioned shape

Keep AGENT_RESULT_SCHEMA=2 and every existing verify schema-2 field/enum/serialization rule unchanged. The new command has its own closed command-specific shape, using the common schema-2 header and a nested inspection schema 1. The exact shape, enums, limits and exit rules are in feature-contract.md, Public inspection result. Add only the new command's statuses and a closed cli.inspect_run declaration to the current machine contract; publish that declaration and drift-test it. This is an explicitly versioned new command result, not optional fields added to old verify envelopes.

Report these separately: metadata validity and last state; complete receipt validity and its original status; receipt-to-snapshot binding; default or partial coverage; actual referenced artifact integrity; historical receipt/run verdict; and unproven current-candidate applicability. Top-level inspected never means passed. Missing or invalid progress cannot erase a complete independent receipt's historical meaning, and an independent receipt cannot claim linkage to a run whose metadata is missing or invalid.

A historical run can report passed only when valid finished/passed metadata binds a complete valid passed receipt, selection is default/all-configured, configured checks passed, summary agrees, and every referenced artifact is verified. A partial passed receipt never satisfies default coverage. Valid failed, blocked and error results remain their original non-passing results. Running is a last observation; finished is terminal result production. No final body is reconstructed from progress or a stdout prefix.

The existing data do not attest project origin or a source commit/tree. Inspection always reports project_origin=not-attested and candidate_applicability=unproven. Hash binding proves consistency of supplied evidence, not provenance, authentication or applicability. Equal root-relative receipt values can legitimately have equal bytes in different projects/runs. Copying an entire consistent evidence set is not detectable under these schemas. Tests must not pretend otherwise; wrong-run/cross-project negative cases use genuinely different evidence. No Git or host activation identity is repurposed as application-candidate identity.

## Consumption, privacy and resource boundary

Open the explicit project root by absolute lexical normalization and existing-directory component-wise no-follow traversal, retaining its descriptor for every project evidence read. Reject symlinked root/ancestor components; do not call target.resolve() and then trust the referent. Factor only the existing snapshot read/strict-parse/schema/run-ID checks into a shared internal reader accepting an already-open private store; the existing read_verify_execution wrapper keeps its public behavior and uses that helper. Inspection uses the same helper with a store anchored to the pinned descriptor, without the unbounded artifacts=True branch. Normalize a supplied envelope against the captured lexical project root once and reuse validate_verify_execution against the already-read snapshot with that normalized object and no re-resolving root parameter for canonical envelope/selection/order/check/log-reference binding. Add a narrow complete CLI receipt validator, described in docs/work-items/20261028-v0-12-publication/feature-contract.md, because digest equality alone is insufficient. Never weaken the existing reader or reinterpret historical publication evidence.

Choose an explicit final receipt first. Never fall back from a bad explicit receipt to another file. Without one, read only an available project receipt path from valid metadata. External metadata paths are intentionally absent; require the caller's explicit authorized path. not-requested/unavailable metadata does not invent a receipt. Invalid metadata is never trusted to select a path; an explicit receipt can still be validated independently. In explicit mode, compare only the selected bytes with any recorded available receipt raw hash; do not reopen, check or vouch for the original metadata project-receipt path. Report that original path was not inspected. A matching safe copy can preserve the historical receipt even if its original slot is gone; a different raw hash is a binding mismatch, independently of whether the selected receipt is itself valid.

Bound final receipt input to 1,048,576 bytes, both before and during reading; use strict UTF-8 JSON, duplicate/nonfinite rejection and closed validation. No producer size limit is added: larger existing receipts remain unchanged and inspection reports a resource-limit gap. Add an optional maximum keyword to the existing project receipt reader if reused, retaining its old default behavior. A separate safe explicit-path reader uses a pinned, component-wise no-follow existing parent and a read-only, nonblocking no-follow leaf.

Require the existing evidence leaf rules: current owner, regular file, mode 0600, one link, stable pre/post fstat signature. Keep project-store directory rules and open-directory no-follow primitives. Do not chmod, create parents, repair or clean input. Explicit external parents need not be private: the existing receipt producer allows them, but they must be traversed without symlinks. Unsupported safety primitives produce a bounded error, never an unsafe fallback.

Choose exactly one log set before hashing: a complete valid selected receipt owns its referenced logs (artifact_scope=receipt); otherwise valid metadata owns its available logs (artifact_scope=metadata); otherwise artifact_scope=none. Never union the two sets or read two conflicting identities for one check. A valid but unbound receipt retains its independently computed verdict after its own logs are checked, while metadata binding mismatch makes top-level invalid/exit 1 and historical_run_verdict=unverified. Report the metadata artifact set as not inspected when it differs; do not claim its integrity. When binding matches, the identical references let one set serve both. Hash the chosen set with a 65,536-byte buffer and at most 67,108,864 bytes per log, four logs maximum. Use pinned safe store access, exact declared count/digest and stable owner/mode/link/inode/size/mtime/ctime checks before/after. Refuse oversized declarations before reading and enforce a growth limit while reading. A valid receipt can independently select only its closed content-addressed project log references; no external log path is followed. Do not use the unbounded reader artifact branch or load all logs into memory. Limits are inspection limits, not retention limits. An unavailable selected artifact is a gap, never a verified artifact or a request to rerun QA.

Project configuration is not parsed or executed by inspection. No observe_toolchain, doctor, verify, Git or wrapper call belongs on its call graph. All findings contain bounded rule IDs and fixed schema-field paths only. No raw exception, absolute input path, command, receipt body/tail, toolchain free text, unknown key/value or log body is emitted. Output projects enums, known check names, valid run IDs, timestamps, counts and hashes only. Same-OS-principal malicious evidence forgery remains outside the existing integrity model.

## Version and later publication lifecycle

The feature source version is 0.12.0. Existing execution/verify/activation and historical publication contracts remain fixed. ADR0024 separately introduces the exact later 0.12.0 publication and closeout profiles; it supersedes the initial feature-stage restriction against adding a publication profile. Source identity is not installed-state ownership or live activation.

## Alternatives and limitations

Do not infer acceptance from metadata, automatically read latest/external paths, infer candidate identity from activation, load unbounded evidence, automatically rerun checks or retain full successful output by default. No evidence migration or repair occurs. Oversized evidence, unavailable storage, incomplete finalization, stale observations and unattested origin remain explicit limitations. The independent public review covers this adopted decision together with ADR0024 and the public feature contract.
