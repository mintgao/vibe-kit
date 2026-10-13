# Verification observability and feedback closure

- ID: `20261010-feedback-closure`
- Size: `L`
- Status: implementing
- Created: 2026-10-10 (host-local date from work-item command)

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: verify configuration and receipt compatibility; persistent log privacy and failure consistency; upgrade no-op classification and recovery; exact publication input/output ownership
- Decision owner: read-only Tech Lead author
- Governing decision: `docs/decisions/0022-verification-observability-and-outcome-coverage.md`
- No-new-decision rationale: none
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: `docs/work-items/20261010-feedback-closure/technical-review-adoption.md`
- Material product decisions: scope and five targets accepted; no unresolved product choice
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator (/root)
- Confirmed at: 2026-10-12T22:30:51.331442+00:00
- Confirmation basis: Accepted ADR0022 (SHA256 332751f0fecd0bdbf03cdd843304fc67074d109e92247c5c9de50ce4c010bd35), distinct approved adoption review, unchanged ac549fa source baseline, healthy doctor and passed specialized context refresh (127 tests); accepted five-issue scope and no material product decisions remain.
- Readiness history: none

## Goal

Improve Vibe Kit's local verification evidence, long-running check visibility, multi-stage completion reporting, and safe repeatable maintenance without weakening existing trust, compatibility or independent QA boundaries.

## Context

Source baseline is GitHub main `ac549fa69319ef92ba859bd7a43d3607ec226e43` (0.10.1), synchronized by clean fast-forward. This is source development from a new iteration request, not an application project's installed-Kit upgrade or takeover; no installed downstream project is changed.

The five current public open issues are [#14](https://github.com/mintgao/vibe-kit/issues/14) (publication receipt input overwritten by generic result persistence), [#15](https://github.com/mintgao/vibe-kit/issues/15) (same-version upgrade no-op items prevent target-state validation), [#16](https://github.com/mintgao/vibe-kit/issues/16) (L01: complete sanitized success logs), [#17](https://github.com/mintgao/vibe-kit/issues/17) (L02: persistent verification execution progress), and [#18](https://github.com/mintgao/vibe-kit/issues/18) (L03: lightweight multi-stage outcome/next-action/role-owner continuity).

Issues #16–#18 contain the exact approved suggestion bodies. L01–L03 remain traceability aliases only; no new feedback submission or retry of denied feedback egress is part of this iteration. Source implementation, exact v0.11.0 Pre-release publication after its checks, and separately bound issue closeout after verified improvements are within the accepted scope.

Applicable existing decisions include ADR0010 (lossless recoverable upgrade), ADR0011 (offline exact-source/publication boundary), ADR0012 (risk-adaptive evidence ownership), ADR0017 (verification contract), ADR0018 (receipt artifacts and host-only takeover custody), and ADR0021 (historical exact publication profile). A new decision must preserve their unaffected semantics.

## Scope

- In: fix #14 input/output aliasing and #15 no-op classification; #16 opt-in complete sanitized success output; #17 durable local verify execution status; #18 minimal prospective multi-stage M/L brief/Close guidance; focused tests, independent review and QA; exact v0.11.0 Pre-release candidate/release gates; separately evidenced #14–#18 closeout after verified improvements and public acceptance.
- Out: changes to downstream projects; resubmitting the already published suggestions or retrying denied feedback egress; new scheduler/services/telemetry; blanket full regressions; relaxed permissions/privacy/QA; overwriting historical receipts or release objects; new credentials, payments or legal acceptance.
- The release identity is Kit `0.11.0`, publication schema `6`, and separate issue-closeout schema `4` as governed by ADR0022; no existing publication or closeout profile is repurposed.
- Only one implementation writer edits shared implementation and test files after readiness is released. The orchestrator owns preimplementation decision persistence and later acceptance evidence.

## Acceptance criteria

- [ ] AC-1 (#14): validate-publication reads its input receipt byte-for-byte without overwriting it on valid or invalid results; explicit output persistence has distinct semantics and rejects input/output aliases before any write; historical validation profiles retain their verdicts.
- [ ] AC-2 (#15): same-version upgrade is deterministic and safely repeatable; no-op entries can satisfy target validation; genuine drift, race preservation, rollback/recovery and cross-version upgrade guards stay intact.
- [ ] AC-3 (#16 / L01): explicit success-log retention preserves complete sanitized output beyond the default 16 KiB tail in a private local artifact with verifiable identity; the bounded result stays bounded and existing failure logs remain available.
- [ ] AC-4 (#16 / L01): absent/unwritable/unsafe artifact destinations report honest availability; secrets/control characters are sanitized; documented privacy and disk-retention boundaries do not silently change old configurations.
- [ ] AC-5 (#17 / L02): during both output-producing and silent slow checks, a caller can locate the current check, start time and running state through a durable local artifact without corrupting final JSON.
- [ ] AC-6 (#17 / L02): interruption leaves honest incomplete evidence; no path reports Pass for incomplete work or asserts all descendant processes were cancelled without proof; project assertions/timeouts and external permissions remain owned by their original layers.
- [ ] AC-7 (#18 / L03): prospective multi-stage M/L guidance records approved outcome references, scope/result coverage, unfinished status, next action, role owner and genuine blockers; stage Pass plus API Blocked plus unverified output cannot become overall completion.
- [ ] AC-8 (#18 / L03): S remains lightweight, existing authority/QA requirements remain, no host goal text or takeover custody is persisted to the repository, and no static fixture is claimed to prove live model behavior.
- [ ] AC-9: Python >=3.9, standard-library-only and offline operation remain; old configs/receipts/compiled profiles preserve their recorded semantics; negative unknown-field/tamper/trust cases remain fail-closed.
- [ ] AC-10: every change maps to regression evidence, independent review and one final-candidate default verification; two clean deterministic candidate builds validate; both release homepages are reviewed; public publication and issue closeout follow separately applicable exact scopes.

## Completion phases and evidence

AC-10.1 covers local review, final-candidate QA, Python/release gates, two deterministic builds, and both homepage reviews. AC-10.2 covers confirmed publication and independent public acceptance. AC-10.3 covers the separate ordered #14–#18 closeout. Overall AC-10 requires all three; publication acceptance excludes AC-10.3.

| Approved reference | This phase covers | State | Evidence | Next action | Role owner | Blocker / waiting condition |
|---|---|---|---|---|---|---|
| AC-1–AC-9, AC-10.1 | Local implementation and release-candidate verification | Unverified | `verification.md` (to be populated) | Implement, independently verify, and freeze the passing candidate | Sole RD writer; independent QA | Accepted ADR0022, approved adoption review, and orchestrator readiness confirmation |
| AC-10.2 | v0.11.0 public publication and acceptance | Unverified | `postpublication.md` (to be created) | Execute the bound publication and independently verify public assets | Host release executor; independent QA | Passing AC-10.1 and exact publication authorization binding |
| AC-10.3 | Per-issue evidence comments and closure of #14–#18 | Unverified | `closeout.md` (to be created) | Verify each issue's mapped evidence, comment, close, and read back under the separate intent | Host closeout executor; independent QA | Passing AC-10.2 and exact issue-closeout authorization binding |

Issue evidence maps #14 to AC-1, #15 to AC-2 plus the published repeat smoke, #16 to AC-3/AC-4, #17 to AC-5/AC-6, and #18 to AC-7/AC-8. Each completed closeout pair proves only its issue; AC-10.3 remains non-passing until all five are confirmed complete. The table records prospective coverage, not executed QA results, and adds no receipt field/schema or host-custody persistence.

## Design and technical notes

Read-only Tech Lead author proposes the smallest coherent architecture and alternatives; a different read-only Tech Lead reviews the exact persisted decision. Do not implement shared code before Accepted decisions, approved review and orchestrator readiness confirmation. Reopen the gate if implementation discovers a new durable boundary.

## Risks and open decisions

- Log publication must not retain raw secrets or expose local process details unnecessarily; complete logs have an explicit retention policy.
- Progress is diagnostic state, not product acceptance or a process-control guarantee.
- No-op success must not weaken lossless final-leaf recovery or classify an ambiguous drift as target.
- Publication input/output alias checks must cover relative, resolved and same-file forms without mutating input.
- Close guidance must strengthen existing rules without creating procedural overhead for S.
- New version/profile mechanics must preserve historical closed validators and exact release identities.

