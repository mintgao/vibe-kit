# Technical review: Publish Vibe Kit v0.10.0 (ADR 0020)

- Work item: `docs/work-items/20260922-v0-10-0-publication/brief.md`
- Artifact reviewed: `docs/decisions/0020-v0-10-0-publication.md`, revision 1 (206 lines, 2026-09-22)
- Review mode: `sequential-perspective`
- Capability limitation: this host does have native subagents, but analysis-shaped review packets exceed its 600 s session budget, so an identity-isolated independent reviewer was unavailable and this review ran as a separate sequential pass by the orchestrator against the brief's acceptance criteria, the closed iteration records and the recorded contract surfaces in `bin/vibe`, `agent-install.json` and `.vibe/core/protocol.json`.
- Verdict: **changes-required** (Pass 1)

## Pass 1 — changes-required

### Blocking findings

1. **Schema-4 helper parity is unstated (record body, section "Exact v0.10.0 publication profile").** The record tells the implementation to reuse "the parameterized shared validation helpers extracted for v0.8 and v0.9", but four of those helpers still carry a schema-3-only condition: `validate_profile_authorization` gates `authorization_source_ref`/`bound_at` on `profile['schema'] == 3`, `validate_profile_intent` gates the exact asset-name closure on `profile['schema'] == 3` and the operation natural-key grammar on the same condition, and `validate_publication_intent` dispatches only `(2, 3)`. Read literally, the record permits a schema-4 profile that silently skips the authorization extra fields, the asset-name closure and the operation natural keys — exactly the checks that make the profile closed. The record must bind that a schema-4 profile receives every one of those checks and that a schema-3 profile keeps receiving exactly them.
2. **Closeout authorization parity is unstated (record body, section "Issue closeout for #8–#13").** The record gives the schema-3 closeout authorization ADR 0011's six fields plus `authorization_source_ref` and `bound_at`, but `validate_profile_closeout_authorization` adds those two fields only when `schema == 2`. As written, the record's own authorization paragraph cannot be implemented without an explicit change to that condition.

### Non-blocking notes (carried to `implementation.md`)

- Closeout graph prose: the shared builder's failure text names "issues 1 through 5" and a ten-operation graph. Under the schema-3 closeout the messages must state the actual ordered issue set and the actual operation count (twelve, sequences 0..11); a fail-closed message that misstates the graph misleads the host it stops.
- The version-identity section names `agent-install.json#kit_version` twice (once as "the installed contract's `kit_version`"). Harmless duplication; the decision is unchanged and the record was not rewritten for it.

### Facts spot-checked against the repository

- `.vibe/core/protocol.json` does carry the three schema values the record says it carries (`publication_intent_schema` 3, `publication_receipt_schema` 3, `issue_closeout_intent_schema` 2), so the mirror change the record requires is real and complete as stated.
- The maintenance bridge's checked expectation in `bin/vibe` (`maximum_installed_kit_version_exclusive` `0.9.0`, `supported_installed_agent_protocols` `[0, 1, 2, 3]`, target schema/protocol 4) matches the record's "unchanged" claims exactly.
- The predecessor-migration registry entry and its checked digest literal are as the record describes, including the v0.5.0 `predecessor` block and the two mirrors.
- The managed guide's three version-literal sites are as named: the opening identification line, the activation-notice text, and the publication-boundary paragraph naming the closed v0.9.0 schema-3 Pre-release with the #6/#7 closeout plan.
- The five publication operations and their asset roles, the six-operation graph, the `issue_closeout` null rule and the historical v0.7/v0.8/v0.9 entry points are consistent with ADR 0013/ADR 0014 as restated.
- Structural conformance: header grammar (`# 0020: ...`, exactly one `- Status: Accepted` before the first `##`), section order and tone mirror ADR 0014; no other file was touched by the author's packet.

## Pass 2 — approved

The two blocking findings were resolved by appending `## Review addendum: schema-4 helper parity and the closeout graph` to the record (revision 2, 216 lines, 2026-09-22), which binds the four helper-parity conditions, the closeout-authorization parity and the closeout graph prose; the decision text itself is unchanged, and the reviewer's addendum is recorded in the record rather than in a side note because the record is the authority the release tooling and tests are held to. Both non-blocking notes are carried into `implementation.md`. Approved for implementation gating.
