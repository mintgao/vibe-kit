# Readiness evidence, documentation gates, and v0.9.0 release

- ID: `20260908-readiness-doc-gates-release`
- Size: `L`
- Status: complete
- Created: 2026-09-08

## Goal and scope

Resolve public issues #6 and #7 (exact report snapshot: `issue-snapshot.json`), publish Vibe Kit v0.9.0 as a non-draft GitHub Pre-release after all checks pass, and institutionalize conditional bilingual GitHub homepage synchronization. The user explicitly authorized fixes, new-version publication after successful verification, and homepage release hygiene. Publication is to mintgao/vibe-kit, annotated v0.9.0, exactly five normal release assets; close only #6/#7 after public verification. No stable promotion, force push, replacement, deletion, signing claim, or Plugin Directory publication.

PM scope authored by `/root/scope`; orchestrator adopted the criteria below. The report's word count is issue evidence, not an independently reproduced project checker. Current CLI contains no automatic budget adjustment; the solution must not attribute that behavior to CLI without evidence.

## Acceptance criteria

- AC-6.1: Governing evidence must exist as an ADR with explicit Status: Accepted; implemented project notes do not qualify. A bounded read-only check provides meaningful preimplementation evidence rather than static string assertions alone.
- AC-6.2: Missing, wrong-kind, non-Accepted evidence fails closed with actionable identifiers before workflow release. Human applicability/review and orchestrator confirmation remain required; no claim of host file-write enforcement.
- AC-6.3: Negative scenarios cover implemented notes and malformed/missing evidence; positive scenarios cover real Accepted ADRs and valid no-new-durable-decision paths.
- AC-7.1: Managed AGENTS prose satisfies one physical line per paragraph; project-owned bytes and project-owned check policy are preserved.
- AC-7.2: Provide an ownership-aware integration contract and verify real merged AGENTS against an explicit counting policy and limit. Test managed-only success with whole-file failure, including the 2858 versus 2800 report shape.
- AC-7.3: No silent ceiling increases, checker removal, or omission of project-owned text. Failures report actual count and threshold. Unsupported project counting policies require the actual project checker, not an invented equivalent.
- AC-DOC.1: Each release reviews README.md and README.zh-CN.md version, links, install examples, capabilities and limitations; changed facts synchronize, unchanged content records a reasoned review. New release candidate has matching bilingual introduction and release facts.
- AC-REL.1: Reviewed exact v0.9 profile and #6/#7 closeout boundaries preserve historical v0.7/v0.8 behavior. The user's authorization is retained; freeze concrete intent before remote writes without inventing a later user approval event.
- AC-REL.2: Exact clean candidate passes independent QA, all configured checks, actual Python 3.9 compatibility, two byte-identical clean builds and release validation.
- AC-REL.3: Public release/tag/commit, all five unauthenticated asset-download hashes, and applicable direct/Plugin/upgrade smokes verified before published-and-verified claim.
- AC-CLOSE.1: Each issue maps original problem to fix, regression and public version; close #6/#7 only after successful public verification and confirm state by read-back.

## Non-goals

General Markdown linting, automatic arbitrary-project budget rewriting, CLI file-write locks, a host enforcement claim, new upgrade trust exceptions, stable promotion, and arbitrary generic publishing.

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: shared readiness and ownership contracts, version compatibility, public release and remote-write recovery require L review.
- Decision owner: read-only Tech Lead `/root/tl_author`
- Governing decision: `docs/decisions/0014-readiness-doc-gates-v09-publication.md`
- No-new-decision rationale: none
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: `docs/work-items/20260908-readiness-doc-gates-release/technical-review.md#Pass 2 — approved`
- Material product decisions: scope and conditional publication authorized; v0.9.0 Pre-release selected as next minor for new bounded validation contracts.
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-09-07T16:55:58.967963+00:00`
- Confirmation basis: Accepted ADR0014 and its exact review addenda cover this brief, issue evidence, rationale and review; distinct reviewer approved; user authorized fixes, conditional release and homepage policy; implementation and later publication gates remain separate.
- Readiness history: 2026-09-08 PM scope established; author proposed ADR0014; distinct review required exact grammar/schema/phase definitions; author addenda persisted and approved; orchestrator confirmed readiness before shared implementation edits.

## Completion

All eleven criteria passed. Vibe Kit v0.9.0 is published and independently verified; issues #6 and #7 are closed with exact evidence comments. See `verification.md` and `public-evidence.json`. The later homepage/evidence commit does not move the release tag or change the published assets.
