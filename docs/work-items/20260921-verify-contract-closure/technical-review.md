# Technical review: verification contract closure

- Work item: `docs/work-items/20260921-verify-contract-closure/brief.md`
- Review mode: `sequential-perspective`
- Reviewer: Tech Lead reviewer pass, Hermes orchestrator session 2026-09-21 (edited no code)
- Capability limitation: identity-isolated independent reviewer unavailable — the host's subagent channel completed four write-shaped tasks but timed out on every analysis-shaped review task at its 600 s budget (this review is the fourth attempt), so the review ran as a separate sequential pass that edited no code

## Pass 1 — changes-required

### Reviewed revision

`docs/decisions/0017-verification-contract-closure.md` at its persisted revision with `- Status: Accepted` (8,129 bytes, 75 lines), read against the work-item brief and the host-reported evidence.

### Findings

1. Blocking — "## Context and applicable decisions" mislabels the recorded gaps and contradicts its own evidence bullet: the order gap is issue #9, the truncation gap is F6, the environment gap is F11, and the host-budget gap is F10. The prose states "F6 is order" and "F10 is diagnosis", and leaves the fourth gap unlabeled, while the metadata bullet lists "#9 and #13 (findings F6, F10, F11)" correctly. Relabel the four passages so the record does not attribute findings to the wrong identifiers.
2. Note — the environment-limited state is defined by its requirements (a reason plus toolchain versions) rather than by a classification trigger; the implementation plan must define how a verdict is classified and must satisfy AC-4, including the requirement that publication and closeout treat the state as not passing.
3. Note — "machine-checkable form" for the constrained-QA record is stated without its concrete form; the implementation plan must fix the form and carry a regression test that binds it, per AC-3.

### Verdict basis

- Decision 1 (declared order): fail-closed validation for unknown names, unknown keys and dependency cycles; the undeclared default stays the degenerate form of the new path; auditability is preserved because the receipt keeps describing the effective order. Accepted.
- Decision 2 (output preservation): the 16 KB tail is stated as the floor and the referenced artifact is bound by path plus digest, so a reader can reach the same per-file verdicts without re-running the check. Accepted.
- Decision 3 (environment-limited): distinct from passed, failed, unconfigured and skipped, requiring a reason and toolchain versions, and explicitly not passing for publication and closeout, so it cannot mask a real failure (note 2 carried to the plan). Accepted.
- Decision 4 (constrained QA): orchestrator runs the complete lane, an independent bounded subagent re-runs a pre-chosen focused subset, and the limitation is recorded in a machine-checkable form; independence is preserved where the budget allows (note 3 carried to the plan). Accepted.
- Alternatives: all four are real, each with a stated reason for rejection. Boundaries: additive, no version bump, historical receipts never rewritten, trust model untouched, revertible without migration. Accepted.
- The substantive decisions are sound; the blocking finding is an attribution error inside the record, not a defect of the decisions themselves.

### Limitations

- Structural review only: the record's claims about validator and receipt behaviour are proven by the implementation's regression tests, not by this review.
- This pass is sequential-perspective, not identity-isolated, and must not be described as `independent-agent` review.

## Pass 2 — approved

### Reviewed revision

`docs/decisions/0017-verification-contract-closure.md` at revision 2 (8,147 bytes, 75 lines), re-read after the author applied the four label replacements Pass 1 required. The four context paragraphs now lead with `#9 is order.`, `F6 is diagnosis.`, `F11 is environment limits.`, and `F10 is the host-budget gap…`, and the evidence bullet plus every other section are unchanged.

### Findings

1. Note (carried, no action in the record) — the environment-limited classification trigger and the constrained-QA record form are fixed in `implementation.md` §3 and §5, which is where Pass 1 notes 2 and 3 belong; the decision record itself stays at the level of requirements.
None blocking.

### Verdict basis

The blocking finding of Pass 1 was the only defect: the record attributed the recorded gaps to the wrong identifiers and contradicted its own evidence bullet. Revision 2 corrects the attribution without touching the decisions, alternatives, boundaries, verification claims or follow-ups. Re-read against the brief's acceptance criteria, the four decisions remain exact and testable, fail-closed where they must be, and honest about what a structural receipt can prove.

### Limitations

- Structural review only, as in Pass 1: behaviour claims are proven by the implementation's regression tests.
- Sequential-perspective, not identity-isolated, as recorded above.