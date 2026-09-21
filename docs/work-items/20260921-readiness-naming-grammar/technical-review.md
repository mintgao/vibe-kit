# Technical review: readiness decision-naming grammar

- Work item: `docs/work-items/20260921-readiness-naming-grammar/brief.md`
- Review mode: `sequential-perspective`
- Reviewer: Tech Lead reviewer pass, Hermes orchestrator session 2026-09-21 (edited no code)
- Capability limitation: identity-isolated independent reviewer unavailable — three review attempts through the host's subagent channel timed out at its 600 s budget (the channel stalls on analysis-shaped tasks after large reads while tiny write-shaped tasks complete), so the review ran as a separate sequential pass

## Pass 1 — approved

### Reviewed revision

`docs/decisions/0016-readiness-decision-naming-grammar.md` at its persisted revision with `- Status: Accepted` (5,603 bytes, 43 lines), read together with the brief's acceptance criteria and the enforcement code at `bin/vibe` lines 12459-12502.

### Findings

1. Note — the section "Decision: read a record's heading and status from its own leading identifier" states the widened rules, but its fail-closed enumeration does not restate the existing exactly-one-top-level-heading rule (`len(headings) != 1` at line 12471). Non-blocking: the record's "every fail-closed behaviour is kept" covers it, and the implementation must keep the check and cover a two-heading file in the negative tests.
2. Note — date-named decisions carry no ordering key for a future supersession index; the record scopes record renaming and migration out, and the brief already carries this as a follow-up. Non-blocking.
3. Note — alternatives appear as out-of-scope follow-ups rather than a dedicated section; the deferred repository-declared `.vibe/project.yaml` pattern is the named rejection, and a one-line rationale for not relaxing only the status line would strengthen the record without being required by the criteria. Non-blocking.

### Verdict basis

- Reference grammar: the record accepts exactly the two forms AC-1 requires; neither is preferred, aliased, or rewritten, and the existing `NNNN-slug` form plus the kit's own records stay valid.
- Heading and status: keyed on the file name's leading four- or eight-digit identifier; bullet-prefixed and plain status forms are equivalent with exactly one status line in the preamble. This closes the observed DSH Desktop Mint failure, where `docs/decisions/20260913-desktop-versioned-assembly.md` with a plain `Status: Accepted` line could not be cited.
- Fail-closed: unknown identifier widths, mismatched headings, absent, non-Accepted and duplicated status lines, and malformed references all continue to fail, with note 1 carried into the implementation.
- Boundary: no schema, protocol, enum, receipt, custody, CLI-result, or version change; the outcome and gate state machine, the takeover and verify contracts, and the two local tooling fixes in the same work item stay outside the decision.
- Compatibility: no existing record in any repository needs a rename or migration, and previously degraded `no-new-durable-decision` classifications can resolve to the durable decision the repository already holds.

### Limitations

- Structural review only: the record's claims about validator behaviour are proven by the regression tests the work item requires, not by this review.
- This pass is sequential-perspective, not identity-isolated, and must not be described as `independent-agent` review.
