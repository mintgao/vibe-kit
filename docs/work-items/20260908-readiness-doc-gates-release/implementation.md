# Implementation report

- Work item: `20260908-readiness-doc-gates-release`
- Role: one RD implementation writer `/root/rd`; no recursive delegation.
- Baseline: branch `codex/readiness-doc-gates-v0.9.0`, starting shared implementation at the preexisting source state; preserved preexisting `.vibe/onboarding.json`, `docs/context/product.md`, and `docs/context/architecture.md` edits and orchestrator planning artifacts.
- Governing boundary: Accepted ADR0014 including all four exact review addenda, `technical-review.md#Pass 2 — approved`, and `brief.md#Technical decision readiness` implementation-ready gate.
- No newly unresolved durable choice. Source distribution maintenance is not target runtime activation.

## Implemented boundaries

`bin/vibe` adds read-only `validate-readiness` and `inspect-managed-agents` schema-1 payloads. The first validates the narrow persisted M/L grammar, real Accepted ADR metadata, safe regular evidence paths, no-new-decision rationale, review and release confirmation. The second authenticates the installed managed hash, reports the exact UTF-8 span including markers, and optionally counts the complete merged file under explicit unicode-whitespace-v1. The 2858/2800 regression retains all project-owned words. Neither command changes a gate, budget, checker, or host filesystem authority.

The publication validators now share profile-parameterized helpers with explicit compiled profiles 2 and 3. Historical v080 wrapper entry points remain fixed to profile 2; v0.7 entry points remain separate. No input or source version alias rewriting is performed at runtime. Schema 3 fixes v0.9 identities, authorization-source/binding fields, phase criteria and seven public smokes. A separate schema-2 closeout builder and standalone receipt validator allow only ordered #6/#7, existing-authorization binding and monotonic recovery after public acceptance. Network operations remain host-owned.

Managed instructions/templates require the new evidence check and rationale; managed AGENTS prose is single-line per paragraph. Kit version is 0.9.0, core/Codex 7. The existing migration registry target/bounds and digest mirrors advanced mechanically; historical predecessor identity records are retained. Other installation/takeover/transaction/general result schemas are unchanged. Current documentation and decision/work-item indexes are updated.

## Changed file groups

- CLI and tests: `bin/vibe`, `tests/test_cli.py`, `tests/test_workflow_contract.py`, new `tests/test_readiness_doc_gates.py`.
- Managed workflow/contracts: `AGENTS.md`, `AGENT_INSTALL.md`, `agent-install.json`, `.vibe/core/{version,protocol.json,quality-gates.md,technical-decision-readiness.md,templates/work-item-brief.md}`, the feature/debug/implementation/verification/release Skills.
- Distribution state: Plugin metadata and bootstrap/maintain Skills, generated `.vibe/manifest.json` and `.vibe/version`.
- Project context/docs: both README files, `docs/releases/0.9.0.md`, product/architecture context, decision/work-item indexes and this report.

## Homepage facts review

Both homepages were reviewed for all five required fact categories before QA freeze:

| Category | Review outcome |
|---|---|
| Version | Changed to v0.9.0 and core/Codex 7; label is Release target / 发布目标, avoiding a premature public-completion claim. |
| Links | Current release links and release-note paths synchronize to v0.9.0; governing historical decision links remain applicable. |
| Installation examples | Exact Release and local validate-release examples synchronize to 0.9.0; ordinary user adoption flow remains unchanged because its behavior is unchanged. |
| Capabilities | Both languages explain real ADR validation and authenticated full-file documentation integration, with matching commands, policy and 2858/2800 example. |
| Limitations | Both retain manual activation fallback, no stable/Directory/signature claim, and explain structural evidence, unchanged budgets and unsupported counting-policy boundaries. |

Public publication evidence belongs in a later evidence commit without moving the release tag.

## Focused verification

Actual CPython 3.9.25 ran 38 focused tests successfully in 17.193s, then one additional parent-profile/authorization regression passed in 0.019s after a test-only addition. Commands selected `tests.test_readiness_doc_gates`, `tests.test_workflow_contract`, and these eight CLI scenarios:

- reproducible/installable/tamper-evident release packaging;
- historical v0.8 closed snapshot/precondition/retry;
- v0.8 two-phase Python 3.9/dual-build evidence;
- v0.8 six-ledger/five-child receipt;
- historical v0.7 exact monotonic closeout;
- historical v0.7 offline publication plan/validation;
- current candidate rejection from v0.7 publication;
- healthy v0.7 to current ordinary upgrade.

New behavioral tests cover Accepted ADR success; implemented/wrong-kind/fenced/duplicate/missing evidence failure; field/enum/state/size/rationale/review/blocker errors; escaping and symlink paths; authenticated spans and tamper/malformed-manifest failures; whole-file 2858 > 2800; unchanged project bytes through actual healthy v0.8 installation/upgrade; schema/profile/authorization/asset rejection; pre/postpublication phase mapping; seven-smoke/five-asset receipts; separate closeout scope, state, comments, read-back and parent binding.

Earlier focused failures were resolved: absent local public v0.8 tag (orchestrator fetched the exact published tag), a test's trailing-marker paragraph assumption, changed expected rationale/version mirrors, and the canonical activation-set declaration needing regeneration. Focused logs remain task-local under `/tmp/v09-py39-focused-final.log`, `/tmp/v09-new-final.log`, `/tmp/v09-integration.log`; QA should collect its own final evidence.

Final `git diff --check` passed. The actual work-item `validate-readiness` result is valid. `inspect-managed-agents . --format json` is valid. Source `doctor . --format json` is healthy; this does not prove host activation.

## Identity generation

Recomputed the migration-registry canonical digest from the compiled declaration. Computed the Agent-install activation digest using `source_activation_identity(ROOT)`, then Plugin payload identity using `payload_tree_sha256(ROOT)`. Generated installation metadata through the production `init --source-type local-payload --source-ref 0.9.0` process in a disposable directory and copied its generated manifest/version into the source checkout. No hashes were fabricated. Initial candidate Plugin payload-tree SHA-256: `6a21d1a371370e7ffb9ffb066fbaf98c263e31aedba8d08cf626a86f1546d4e3` (superseded by the QA fix below).

## QA handoff and skipped checks

Independent QA owns accepted AC-6.1 through AC-CLOSE.1 and ADR0014's exact governing boundary. The configured default check is `python3 -m unittest discover -s tests -v`; RD did **not** run the complete default `./bin/vibe verify . --format json` matrix. QA owns that unchanged final candidate run once, plus release-specific actual Python 3.9, clean A/B builds, both release validations and later public acceptance. Clone all historical tags: existing fixtures require v0.5.0/v0.7.0 and the new actual predecessor fixture requires v0.8.0.

The root orchestrator freezes the final diff/baseline and clean commit after this report. RD made no commits or network writes. Prepublication QA, release-specific full gates, public five-asset hashes/seven smokes and #6/#7 closeout are pending; RD does not declare product acceptance or publication completion.

## Host release integration recipe

Use `PUBLICATION_PROFILES[3]` with `validate_profile_intent`, `validate_profile_release_gate_bundle`, `validate_profile_authorization`, `validate_profile_postpublication_acceptance` and `validate_profile_receipt` keyword `profile=`. Generic CLI `publication-plan --phase publish --request <json> --candidate <A> --comparison-candidate <B> --release-gate-evidence <json> --format json` dispatches schema 3. Final CLI is `validate-publication --intent <json> --receipt <json> --authorization <json> --candidate <A> --format json` on CPython 3.9.

`issue-closeout --packet <json> --format json` reads exactly six repository-relative evidence paths from the packet directory: `request`, `parent_intent`, `publication_receipt`, `publication_authorization`, `acceptance_receipt`, `validation_result`. For standalone receipt validation add exactly `closeout_authorization` and `closeout_receipt`. It returns the exact intent/digest and comment bodies, never writes remotely. Programmatic entry points are `build_v090_closeout_intent(...)`, `validate_v090_closeout_parent(...)`, and `validate_v090_closeout_receipt(...)`.

Closeout `overall_state` retains `not-run|confirmed-partial|confirmed-complete|uncertain|conflict`; operation states retain ADR0011's historical enum, without v0.8's `updated` extension. Live host observation and consent authenticity remain host responsibilities, not guarantees from static contracts.


## QA correction: exact Size quoting

Independent QA reproduced malformed `- Size: `L` (unclosed quote) and doubled-backtick Size acceptance on frozen candidate `f6ab721`; its evidence is `/private/tmp/vibe-v09-qa/independent-size-negative.json`. The parser had used a stripping operation that removed any number of edge backticks. RD replaced it with one shared exact-pair literal helper: plain values pass through, exactly one complete pair is unwrapped, malformed quoting remains invalid. Existing outcome/gate/review enum parsing already used the exact-pair rule; it now shares the helper and has explicit malformed-quote regressions.

The focused regression verifies plain and singly paired M/L positives; unclosed, doubled, uneven and internally spaced Size negatives; and unclosed/doubled outcome, gate, review-mode and review-result negatives. Actual CPython 3.9.25 ran all 15 `tests.test_readiness_doc_gates` tests successfully in 1.486s. Current work-item readiness passes; source doctor is healthy; `git diff --check` passes. No full default verification was run by RD.

Canonical activation, Plugin and production-init installation identities were regenerated after the code edit. Updated Plugin payload-tree SHA-256: `0251f492a32334507a50411ec7460465350e36098397694da453c9a1aa89f5f3`. The old QA full run overlapped the authorized shared edit and must be recorded as mixed/stale, never valid final-candidate evidence. Root will commit the new candidate and independent QA must run the complete default gate on that changed state. No ADR reopening is needed: this fixes conformance to ADR0014's existing exact grammar.
