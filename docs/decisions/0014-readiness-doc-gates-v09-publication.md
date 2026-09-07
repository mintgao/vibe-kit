# 0014: Validate bounded readiness evidence and managed documentation boundaries; publish exact v0.9.0

- Status: Accepted
- Date: 2026-09-08
- Decision owner: read-only Tech Lead author `/root/tl_author`
- Work item: `docs/work-items/20260908-readiness-doc-gates-release/brief.md`
- Evidence: that brief’s accepted criteria and `issue-snapshot.json`
- Review: approved by distinct read-only Tech Lead `/root/tl_review` after exact addenda; 2026-09-08

## Context and applicable decisions

Issue #6 demonstrates that implemented project notes can be mistaken for Accepted ADRs. Issue #7 demonstrates that healthy managed installation bytes can still fail project documentation policy. The reported budget adjustment is not established CLI behavior: current CLI has no automatic project-budget adjustment.

ADR 0001 continues to govern managed/project ownership; ADR 0004 governs deterministic packaging; ADR 0008 governs readiness authority, now extended with read-only evidence checking; ADR 0010 governs installation transaction and recovery unchanged; ADR 0011 governs host-owned network operations and exact-source trust; ADR 0012 governs bounded handoffs and verification ownership. ADR 0013 remains the exact historical v0.8 publication contract.

## Decision: bounded readiness evidence validation

Add a dependency-free, read-only `validate-readiness` command operating on one explicitly selected project-owned work-item brief. It checks the actual persisted record and referenced files. It neither changes the gate nor prevents filesystem writes.

Support a documented narrow Markdown grammar:

- Exactly one unfenced `## Technical decision readiness` section.
- Exactly one single-line bullet for each normative required field; duplicate or empty fields fail.
- Size comes from one canonical work-item `Size` field.
- Enum fields accept their documented literal value, optionally wrapped in backticks.
- `Governing decision` contains `none` or an explicit comma-separated list of backtick-quoted repository-relative `docs/decisions/NNNN-slug.md` paths. Applicability prose belongs in the confirmation basis or a linked evidence document.
- Referenced ADRs must have a matching numbered top-level heading and exactly one unfenced metadata bullet `- Status: Accepted` before their first second-level heading. A note outside `docs/decisions`, code-fenced status example, duplicate/conflicting status, or other lifecycle status cannot satisfy this rule.
- Paths must stay inside the selected project and traverse no symlink; missing, malformed, escaping, or nonregular references fail with stable rule identifiers and field/path locations.
- Check all normative enum/state combinations, mandatory review for L and triggered M, explicit blocker clearance, gate-owner evidence, and ISO-8601 confirmation.
- A no-new-decision path requires explicit rationale and the applicable review/confirmation fields; validation cannot establish the rationale’s substantive truth.

For M, treat `Trigger evidence: none` as the explicit untriggered declaration; any other value requires review. Human trigger assessment remains mandatory.

A successful exit means the requested persisted `implementation-ready` evidence passed these structural checks. A blocked record returns a blocking result even if internally well formed. Output distinguishes structural findings from the remaining human responsibility for applicability, review independence, and resolved product choices.

The orchestrator invokes this check before releasing applicable new work under v0.9, and after referenced evidence changes. QA checks the evidence used for release. Completed historical briefs are not migrated, and unsupported Markdown receives an actionable formatting error rather than speculative parsing.

## Decision: authenticated managed-region integration

Keep one physical line per managed prose paragraph in root `AGENTS.md`; preserve meaningful lists, code blocks, and project-owned bytes.

Add a read-only `inspect-managed-agents` interface. It requires exactly one ordered marker pair and authenticates the extracted region against the installed manifest’s `agents_block_hash`, using the existing installation hash convention. It reports:

- file and managed-region SHA-256;
- exact UTF-8 byte span, with start inclusive and end exclusive, including both markers;
- authentication basis;
- explicit limitations.

Authentication establishes correspondence to recorded installation state, not an independent publisher signature. A missing or invalid manifest, malformed markers, or mismatching region fails closed. Do not fall back to trusting marker presence alone.

An optional explicit `--word-policy unicode-whitespace-v1 --max-words N` check counts the **entire current merged file** using Python `str.split()` after strict UTF-8 decoding. Include markers and project-owned text. Report whole-file actual count and threshold; managed-region count may be diagnostic but never substitutes for the whole-file result.

No project configuration, checker, or ceiling is rewritten. Projects can use the authenticated byte span to exempt framework-owned prose from a project-specific formatting rule while retaining their own whole-file budget. Other counting policies must run their actual project checker; do not claim this counter implements arbitrary Markdown, linguistic, or token policies.

Installation/upgrade health retains its existing meaning. Documentation-gate success requires the configured project checks or an explicitly selected supported check against the resulting merged file.

## Version and compatibility

Select Kit `0.9.0`, core protocol `7`, and Codex adapter protocol `7`: the new evidence-check invocation changes the managed workflow conformance contract. Align core, adapter, Agent-install mirrors, Plugin metadata, documentation, packaging, and generated identities mechanically.

Keep installation manifest, release manifest, takeover, maintenance bridge, migration registry, transaction, and general CLI result schemas unchanged unless an actual shape change independently requires revision. Publish the two new command payloads with their own schema version `1`.

Do not modify the meaning or acceptance sets of historical publication schema 1/v0.7 or schema 2/v0.8. Introduce publication intent/receipt schema `3` exclusively for `vibe-kit-v0.9.0-prerelease`, and a separately closed v0.9 closeout shape. Unknown profiles and cross-profile combinations fail.

## Exact v0.9 publication implementation

Use a closed internal profile definition and parameterized shared validation helpers extracted from v0.8 where semantics are identical. Retain historical entry-point wrappers and regression fixtures. Profile-specific identities and criterion sets are explicit constants. Do not rewrite JSON/source text, substitute version strings, or pretend v0.9 evidence is v0.8.

The profile fixes:

- repository `mintgao/vibe-kit`;
- version/tag `0.9.0` / annotated `v0.9.0`;
- title `Vibe Kit v0.9.0`;
- release body `docs/releases/0.9.0.md`;
- non-draft Pre-release, no generated notes;
- the same five asset roles with exact v0.9 names;
- v0.8’s six publication operations and their ordered per-asset ledgers;
- an explicitly separate, post-public-verification #6/#7 closeout phase.

Preserve v0.8’s strict remote snapshot closure, complete asset pagination, canonical digests, source/tree binding, annotated tag identity, fast-forward compare-and-swap, public-download hashes, bounded retry, and read-back/recovery semantics. Existing `main` may advance only when its expected predecessor remains correct and the frozen source commit is a descendant. A local historical evidence commit in that ancestry is not a reason to rewrite history.

Before remote mutation, freeze the exact source commit, release bytes, five assets, remote preconditions, intent digest, and an executable authorization record. That record cites the existing user authorization and records when the host bound it to the concrete intent. It must not invent a later user message or require repeated confirmation for already authorized scope.

Changed candidate bytes invalidate the frozen intent and evidence; rebuild and rebind within the authorized scope. Changed destination, version, operation scope, destructive behavior, or other material commitment requires a new user decision.

## Issue closeout and homepage review

Only after successful public verification, freeze each issue’s exact comment, original-problem/fix/regression/public-version mapping, current state, idempotency marker, and intended closed state. Bind a separate closeout digest to the verified publication receipt and inherited authorization.

Permit only #6/#7 comment-and-close operations. Read before write, detect an existing exact marker/comment, read back each operation, and stop on divergent or uncertain state. Never edit unrelated issues or close before verification.

Every release reviews `README.md` and `README.zh-CN.md` version, links, install commands, capabilities, and limitations. Changed facts must agree; unchanged sections receive a reasoned review record. Freeze both README states before final candidate QA. Public completion facts belong in a later evidence commit without moving the release tag.

## Alternatives and trade-offs

- Prose-only readiness strengthening is insufficient for the demonstrated wrong-kind evidence failure.
- A CLI workflow state machine or file lock adds authority and migration costs without solving host compliance; excluded.
- Arbitrary Markdown/YAML parsing or automatic checker adaptation introduces ambiguity; a narrow documented grammar is deliberately chosen.
- Automatic budget increases weaken project policy; excluded.
- Marker-only masking can hide unauthenticated content; excluded.
- A copied v0.9 publisher duplicates a large trust surface; share checked helpers with exact profiles.
- A generic configurable publisher expands the accepted compatibility boundary; excluded.

The narrow helper format may require explicit formatting updates to active briefs. It does not rewrite old records or certify human judgments.

## Ownership, recovery, and verification

The orchestrator persists this proposal and distinct review, accepts the ADR, then confirms readiness. One RD writer owns implementation. Independent QA owns the unchanged final candidate’s complete configured verification; release-specific Python 3.9 and build gates remain separately identified.

Required scenarios:

1. Real Accepted ADR success; implemented note, wrong path/kind/status, fenced spoof, duplicate status, missing fields/files, path escape and symlink failure.
2. Valid no-new-decision M/L paths and invalid review, blocker, confirmation, or gate combinations.
3. Managed-region authentication/tamper/marker failures; exact project-byte preservation through install/adopt/upgrade.
4. Real merged-file counts, including managed-only success while whole-file `2858 > 2800` fails; unsupported policies never receive an equivalent-policy claim.
5. Historical v0.7/v0.8 acceptance and rejection behavior; exact v0.9 schema/profile rejection and shared-helper regressions.
6. Source/authorization/intent drift, extra or mismatching assets, uncertain writes, bounded retries, same-intent resume, and early-closeout rejection.
7. Bilingual release facts, actual CPython 3.9 configured checks, independent QA, two byte-identical clean builds, and validation of both outputs.
8. Public tag/commit/Release verification, all five unauthenticated asset hashes, direct/Plugin/upgrade smokes, and #6/#7 state read-back.

Before publication, recovery is Git revert and disposable candidate rebuild. Installation recovery remains ADR 0010. After remote writes, use same-intent reconciliation; never force push, delete, replace assets, or move the tag. Uncertain or partial state remains explicitly incomplete. Credentials and raw host output stay out of durable evidence.

No unresolved product choice remains within this accepted scope.

## Review addendum: exact readiness grammar

This addendum supersedes only ambiguous format, schema, and phase details above.

The work-item preamble runs from its single top-level heading to its first unfenced second-level heading. It contains exactly one `- Size: M` or `- Size: L` bullet, optionally backtick-wrapping the value. Missing, duplicate, or conflicting Size declarations fail. S is outside this command’s applicable input contract.

Within the readiness section:

- Add required `- No-new-decision rationale: ...`. For `no-new-durable-decision`, its value must be nonempty and not `none`; other outcomes require `none`.
- `covered-by-accepted-decision` and `decision-accepted` require at least one governing ADR. `Governing decision: none` is invalid for either.
- `no-new-durable-decision` requires `Governing decision: none`.
- An M record with `Trigger evidence: none` may release only through `no-new-durable-decision`. All other M records and every L record require approved review.
- Required approved review needs `Review mode: independent-agent|sequential-perspective`, `Review result: approved`, and nonempty, non-`none` `Review evidence`. Review evidence is one backtick-quoted repository-relative regular-file path, optionally followed by a literal `#heading` inside the backticks. Validate file existence and path safety; applicability and reviewer identity remain human checks.
- A released record requires nonempty, non-`none` `Gate owner` and `Confirmation basis`, a valid ISO-8601 `Confirmed at`, and literal `Open blockers: none`. `Confirmation basis` records the checked work item, decision/rationale, review, and product-resolution basis in prose; the validator checks presence, not truth.
- `Decision owner` must be nonempty and non-`none` for either ADR-based successful outcome.

The additional rationale field belongs to newly adopted v0.9 records/templates. Historical briefs are not rewritten automatically.

## Review addendum: exact v0.9 publication schema

ADR0013’s sections “v0.8 publication intent schema 2,” “Closed remote snapshot and operation preconditions,” “Closed operation receipt ledgers,” “Two-phase evidence and exact prepublication receipts,” “Five-asset closure,” “Source, main, and annotated-tag identity,” “Remote reconciliation and recovery,” and “Receipt schema 2 and public verification” define the inherited field sets, child shapes, typing, nullability, canonical hashing, ledgers, and validation rules.

Only these v0.9 differences apply:

1. Publication intent/receipt schema is `3`, version `0.9.0`, profile `vibe-kit-v0.9.0-prerelease`; exact tag, title, note path, and versioned asset names are those specified above. Receipt top-level fields remain ADR0013’s schema-2 fields, with these explicit identity changes.
2. The six publication operations are unchanged. Closeout is never a seventh publication operation.
3. Intent `issue_closeout_policy` has exactly:
   ```json
   {
     "mode": "after-public-verification",
     "issues": [6, 7],
     "allowed_operations": ["create-exact-evidence-comment", "close-issue"]
   }
   ```
4. Publication receipt `issue_closeout` remains exactly `null`. Closeout results are a separate receipt; publication validation never waits for issue closure.
5. Local evidence receipt schemas remain `1`, with explicitly enumerated v0.9 kinds replacing the v0.8 kinds: `vibe-kit-v0.9-prepublication-qa`, `vibe-kit-v0.9-configured-checks`, `vibe-kit-v0.9-python-3.9`, `vibe-kit-v0.9-clean-build`, `vibe-kit-v0.9-release-gate-evidence`, and `vibe-kit-v0.9-postpublication-acceptance`. Version/profile fields use v0.9. Criterion mappings and smoke names are defined below.
6. The publication authorization retains ADR0013’s seven fields and adds exactly `authorization_source_ref` and `bound_at`. The former is a nonempty sanitized host reference to existing authorization; the latter is ISO-8601. These prove structural binding, not consent authenticity. No later user-message requirement is inherited.
7. ADR0013’s historical closeout-parent exception remains v0.7-only and cannot validate a v0.9 parent.

No other inherited field becomes optional or extensible. Shared helpers receive a resolved compiled profile; input rewriting or version aliasing is prohibited.

## Review addendum: exact #6/#7 closeout

Use closeout-intent schema `2`. Inherit ADR0011’s “Issue #1–#5 closeout transaction” top-level and child field sets, types, observations, authorization scope, operation preconditions, bounded retry, duplicate rejection, and monotonic resume, with precisely these differences:

- Issues are exactly `[6,7]`, in that order.
- The closeout ID preimage uses `schema_version: 2`, version `0.9.0`, repository `mintgao/vibe-kit`, the v0.9 parent publication-intent digest, and `[6,7]`.
- Markers are exactly `<!-- vibe-kit:v0.9.0:issue-<n>:<closeout_id> -->`.
- Four operations execute in order: issue 6 comment, issue 6 close, issue 7 comment, issue 7 close; sequences are `0..3`. Existing operation ID/natural-key grammar remains unchanged.
- `publication_receipt_sha256` binds the validated schema-3 publication receipt. `verification_receipt_sha256` binds the passing v0.9 postpublication acceptance receipt defined below. Both must bind the same parent intent, source, profile, and authorization.
- Scope issues become `[6,7]`; allowed operations remain comment and close; destructive operations remain false. `requires_separate_closeout_authorization=true` means a distinct executable record, not a new user confirmation.
- The closeout authorization has ADR0011’s six exact fields plus `authorization_source_ref` and `bound_at`, with the same semantics as above.
- At most two writes per operation remain allowed; uncertainty, permission failure, mismatch, duplicate matching comments, and closed-without-exact-comment block further writes. An exact closed issue is reusable on resume.

The standalone closeout receipt has exactly:

```text
schema_version = 2
kind = vibe-kit-issue-closeout-receipt
closeout_id
closeout_intent_sha256
closeout_authorization_id
overall_state
items
```

`overall_state` retains ADR0011’s enum. `items` is exactly `[6,7]`; each item has exactly:

```text
issue_number
expected_initial_state
comment_body_sha256
comment_id
comment_url
comment_write_state
close_write_state
observed_post_state
read_back
error
```

States are `open|closed`; `observed_post_state` may be null before observation. Comment ID/URL may be null before confirmation; otherwise ID is positive and URL is the canonical matching GitHub issue-comment URL. Write states use ADR0011’s operation-outcome enum. `read_back` is boolean; `error` is null or its closed `code,message,next_action` shape. Complete requires both exact comments and closed states read back, valid IDs/URLs, successful terminal operation states, and no errors.

## Review addendum: exact phase mapping and smokes

The prepublication QA `criterion_mapping` contains these eleven IDs in brief order:

| Criterion | Required prepublication state | Postpublication requirement |
|---|---|---|
| AC-6.1 | passed | none |
| AC-6.2 | passed | none |
| AC-6.3 | passed | none |
| AC-7.1 | passed | none |
| AC-7.2 | passed | none |
| AC-7.3 | passed | none |
| AC-DOC.1 | passed | none |
| AC-REL.1 | passed | none |
| AC-REL.2 | passed | none |
| AC-REL.3 | not-runnable-before-publication | public-smoke |
| AC-CLOSE.1 | not-runnable-before-publication | issue-closeout |

`issue-closeout` is the sole added requirement-enum value. AC-REL.1’s local pass establishes tested profile/authorization boundaries; actual execution binding is additionally enforced by publication validation. Neither pending criterion may be reported passed before its phase.

All existing configured-check, actual CPython 3.9, distinct clean-build A/B, byte-identity, and dual-validation requirements must pass before publication.

The required public smoke set is exactly:

```text
public-direct-init-doctor
public-plugin-bundled-plan-init-doctor
public-upgrade-v0.3-to-v0.9
public-upgrade-v0.5-to-v0.9
public-upgrade-v0.6-to-v0.9
public-upgrade-v0.7-to-v0.9
public-upgrade-v0.8-to-v0.9
```

Each upgrade starts from a healthy authenticated installation of the named predecessor and verifies successful target installation/doctor. It does not claim host activation.

Postpublication acceptance inherits ADR0013’s closed receipt shape but contains exactly the first ten criteria above, all `passed`. AC-REL.3 must reference live metadata, five unauthenticated downloads, distribution validation, the complete smoke set, and successful offline publication validation. This passing receipt authorizes entering the already-authorized closeout phase.

AC-CLOSE.1 is completed only by the subsequent validated standalone closeout receipt plus its issue-to-fix/regression/version evidence. Final task completion requires both receipts. This separation avoids making publication acceptance depend on the closeout it must first authorize.
