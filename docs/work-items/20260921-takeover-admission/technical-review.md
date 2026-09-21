# Technical review: takeover admission

- Work item: `docs/work-items/20260921-takeover-admission/brief.md`
- Review mode: `sequential-perspective`
- Reviewer: Tech Lead reviewer pass, Hermes orchestrator session 2026-09-21 (edited no code)
- Capability limitation: identity-isolated independent reviewer unavailable — on this host every analysis-shaped subagent review attempt has timed out at its 600 s budget (four for four across this iteration), while write-shaped packets complete in about a minute; this review therefore ran as a separate sequential pass that edited no code

## Pass 1 — changes-required

### Reviewed revision

`docs/decisions/0018-takeover-admission.md` at its first persisted revision with `- Status: Accepted` (10,539 bytes, 96 lines), read against the work-item brief, the two prior decision records' layout, and the recorded findings.

### Findings

1. Blocking — "## Context and applicable decisions" swaps two finding labels: the paragraph leading `F7 is the contract gap` describes the undocumented takeover object, which is F2, and the paragraph leading `F2 is the capture gap` describes the CLI persisting no receipts, which is F7. The metadata bullet and the decision sections are correct, so the record contradicts itself. Swap the two lead labels and change nothing else.
2. Note (plan-level) — the record leaves the publication's location open (`AGENT_INSTALL.md` or a linked contract page); the implementation plan must fix one location, keep it inside the managed-block discipline, and name it in the drift test.
3. Note (plan-level) — "byte-stable for a fixed outcome" and "two runs … must produce the same artifact bytes" require the implementation to exclude host-volatile content (absolute paths, capture times) from the artifact or normalize it; the plan must state how byte-stability is achieved and a test must prove it.
4. Note (plan-level) — admission evidence must re-derive the target identity at validation time and never trust recorded fingerprints; the forged-fingerprint negative case in the record's verification section must land as a regression test.

### Verdict basis

- Decision 1 (admission kind): binds the host task, the canonical project directory and the recomputed target identity, references the historical transaction without rewriting it, and states its narrow purpose; fail-closed negatives are named. Accepted.
- Decision 2 (published contract): enumerates the closed field sets, the custody pair (`manual-transfer-required` null versus `manual-transfer-pending` active task), the evidence ordering rules, the blocked-state contract, and binds the publication to the validator with a drift test; the right level for a decision record. Accepted.
- Decision 3 (receipt artifact): replaces private host capture with a framework artifact whose digest a host cites; consistent with ADR 0017's path-plus-digest pattern. Accepted (with note 3).
- Decision 4 (transfer payload): host-neutral shape validated on shape, freshness and evidence references, with custody in host task state and goal text never persisted. Accepted.
- Alternatives and boundaries: all four alternatives are real and rejected for stated reasons; compatibility, privacy and revertibility are honest; nothing overclaims what a structural receipt can prove.
- The substantive decisions are sound; finding 1 is an attribution error inside the record, not a defect of the decisions themselves.

### Limitations

- Structural review only: the record's behavioural claims are proven by the implementation's regression tests, not by this review.
- Sequential-perspective, not identity-isolated; it must not be described as `independent-agent` review.

## Pass 2 — approved

### Reviewed revision

`docs/decisions/0018-takeover-admission.md` at revision 2 (10,539 bytes, 96 lines), re-read after the author swapped the two mislabeled finding leads. The context paragraphs now lead `F2 is the contract gap.`, `F7 is the capture gap.`, `F12 is the transfer gap.` and `Issue #8 is the admission gap…`; the metadata bullet and every other section are unchanged, and the record no longer contradicts itself.

### Findings

1. Note (carried, no action in the record) — the publication's location, the receipt artifact's byte-stability mechanism, and the admission evidence re-derivation are fixed in `implementation.md` §3–§5, which is where Pass 1 notes 2–4 belong; the decision record stays at the level of requirements.
None blocking.

### Verdict basis

The blocking finding of Pass 1 was the only defect: two finding labels were swapped while the metadata bullet and the decision sections were correct. Revision 2 corrects the attribution without touching the decisions, alternatives, boundaries, verification claims or follow-ups. Re-read against the brief's acceptance criteria (AC-1 through AC-7), the four decisions remain exact and testable, fail-closed where they must be, and honest about what a structural receipt can prove.

### Limitations

- Structural review only, as in Pass 1: behavioural claims are proven by the implementation's regression tests.
- Sequential-perspective, not identity-isolated, as recorded above.