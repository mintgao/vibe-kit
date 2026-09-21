# Verification: Readiness Naming Grammar

Frozen candidate: `e03e361c3220f7d9c941e9e0566716664e6a9528`, working tree clean.
Verifier: independent QA subagent (Hermes, dispatched 2026-09-21; read-only in the repository, writes confined to disposable `/tmp` projects), with the orchestrator re-running the doctor, help, and slug spot checks directly.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | In a disposable project, `docs/decisions/20260913-versioned-assembly.md` (date-named, plain `Status: Accepted` line) cited as the governing decision validated: rc 0, `status: valid`, `findings: []`. The numbered form still validates unchanged. | Pass |
| AC-2 | The grammar is stated in `.vibe/core/technical-decision-readiness.md` (bounded preimplementation evidence check) and in ADR 0016's two `## Decision` sections; `test_documented_naming_forms_and_relaxed_status_line` asserts that both documented examples (`# 0001: ...`, `# 20260913: ...`) pass and is green in the default lane. | Pass |
| AC-3 | `tests/test_readiness_doc_gates.py` covers the fail-closed set: mismatched heading, non-Accepted status, duplicate status lines, status after the first second-level heading, missing status, two top-level headings, fenced status, and five-/seven-digit identifiers, yielding `readiness.adr-not-accepted` and `readiness.adr-reference`. | Pass |
| AC-4 | `work-item 20260918-green-default-verification` created `docs/work-items/20260918-green-default-verification`; a plain slug created `docs/work-items/20260921-plain-slug` (today's prefix). `test_work_item_does_not_double_prefix_a_dated_slug` is green. | Pass |
| AC-5 | `feedback submit --help` names the `sha256:<hex>` token form, the bare-hash acceptance, and the staleness rule; `test_feedback_confirm_accepts_a_bare_hash_and_documents_the_token` is green and submits with a bare digest against a fake `gh`. | Pass |
| AC-6 | Frozen candidate clean; default lane `Ran 89 tests in 38.100s` / `OK`; `validate-readiness` valid for this brief, for the ADR-based 0015 brief, and for the 20260908 brief. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -W ignore::DeprecationWarning -m unittest discover -s tests` | Pass | 89 tests (86 pre-existing plus 3 added here), `OK` |
| `python3 bin/vibe validate-readiness . --brief docs/work-items/20260921-readiness-naming-grammar/brief.md --format json` | Pass | rc 0, `status: valid`, `findings: []` |
| `validate-readiness` for the 0015 and 20260908 briefs | Pass | both rc 0, `status: valid` — no regression for existing ADR-based records |
| `python3 bin/vibe doctor . --format json` | Pass | `status: healthy`, activation identity `18e480ea…` matches the recomputed `source_activation_identity` |
| Release identity mirrors | Pass | `payload_tree_sha256` (`998a1798…`) and `activation_set_sha256` (`18e480ea…`) recomputed and mirrored in `.vibe/manifest.json`, `agent-install.json`, and the Plugin manifest in the same change; reproduced by a disposable production `init --source-type local-payload --source-ref 0.9.0` install |

## Manual scenarios

- Issue #11 reproduction, disposable project: ADR 0016 copied to `docs/decisions/20260913-versioned-assembly.md` with its heading rewritten to `# 20260913: Versioned assembly` and its status bullet rewritten to a plain `Status: Accepted` line; the brief's governing-decision reference pointed at it; `validate-readiness` returned rc 0 with `status: valid`. Result: pass.
- Work-item slug normalization, disposable project: dated slug and plain slug both created exactly one directory with the expected name. Result: pass.
- Confirmation-token help surface: read directly from `feedback submit --help` on the frozen candidate. Result: pass.

## Limitations and follow-ups

- Structural verification only: the real DSH Desktop Mint repository was not available to the verifier, so the reproduction is of the failing form rather than of that repository; human applicability, review independence, and resolved material product decisions remain host-owned.
- The lane ran on the workstation's default CPython 3.13.9; no 3.9 interpreter is installed here, so the CPython 3.9/3.13 dual-lane requirement is carried to the release work item that will ship this change.
- Review independence: identity-isolated review was unavailable on this host (the subagent channel timed out on analysis-shaped tasks at its 600 s budget), so the review ran as a recorded `sequential-perspective` pass; the verification pass itself ran as an independent subagent.
- Date-named decisions still carry no ordering key for a future supersession index; recorded as a follow-up in the brief, not part of this work item.