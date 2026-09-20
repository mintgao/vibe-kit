# Technical review — ADR 0015 host-neutral manual activation

## Pass 1 — changes-required (2026-09-21)

- Reviewer role and mode: independent read-only Tech Lead reviewer, `vibe_tech_lead` reviewer mode; a different instance from the decision author. No files written.
- Artifact reviewed: `docs/decisions/0015-host-neutral-manual-activation.md` (Status: Accepted; Date 2026-09-21), revision 1, read in full.
- Checked against: `docs/work-items/20260921-host-neutral-manual-activation/brief.md` (scope, AC-1..AC-7, risks) and `.vibe/core/technical-decision-readiness.md` (Trigger scan, Size policy, State and release rules, Roles and authority).
- What was checked: AC-1..AC-7 coverage and brief scope; named boundaries and the closed `agent-install.json` field set; compatibility honesty (Codex stays the only verified integration; reload and automatic handoff stay conditional and unclaimed); preserved receipt, custody, degraded-stop and fail-closed rules; abuse paths; whether any schema, enum, validator or CLI-result change is silently required; whether the consequences cover projects already installed at 0.9.0; whether the out-of-scope follow-ups block safe implementation.
- Verdict: `changes-required`.
- Required changes: (1) extend the contract-text decision past the managed block, state that no surface may declare a disagreeing schema number, and make clear the block tracks the installed contract by authored text rather than by generation; (2) name the enforcement — regression tests for schema agreement, single-host-name reintroduction, and payload-digest consistency; (3) add the consequence for projects already installed at 0.9.0, including that no in-place rewrite, migration or `validate-takeover` change is permitted; (4) state the abuse-path boundary — host-neutrality does not relax receipt content requirements, a host that cannot recompute the identities must take the degraded stop and must not supply a receipt, and structural acceptance is not authentication.
- Limitations: structural review of persisted text only; no live host, receipt, takeover object or verification lane was executed, so the claim that a non-Codex host can own the successor task remains unverified in practice.

## Revision 2 (2026-09-21)

All four required changes were applied to the persisted decision: the contract-text decision now covers every managed surface and states that the reference is authored text with no materialization or CLI change; enforcement names the three regression tests; a consequence paragraph covers already-installed 0.9.0 projects and forbids in-place rewriting, migration and `validate-takeover` changes; and the host-neutrality decision states the abuse-path boundary and that structural acceptance is not authentication.

## Pass 2 — approved (2026-09-21)

- Reviewer role and mode: a second independent read-only Tech Lead reviewer instance, distinct from the author and from the pass-1 reviewer. No files written.
- Artifact reviewed: `docs/decisions/0015-host-neutral-manual-activation.md` revision 2, read in full.
- Verdict: `approved`; required changes `none`.
- Basis: all four pass-1 items are resolved in the persisted text; AC-1..AC-7 stay governed inside the brief's scope; no schema, protocol, enum, validator, receipt, custody or CLI-result change is introduced or silently required, the only `agent-install.json` delta being the disclosed regenerated activation mirror; the compatibility claim stays honest with the Codex adapter still the only verified integration and reload and automatic handoff still conditional and unclaimed. The reviewer noted one new tension — "no managed surface declares a disagreeing schema number" against grandfathered 0.9.0 blocks — and reconciled it with the decision's explicit "until they adopt a newer version" carve-out, requiring no change.
- Limitations: structural review of persisted text only; no live host, receipt, takeover object or verification lane was executed, so the practical claim that a non-Codex host can own the successor task remains unverified. Reviewer independence is instance-level: both reviewers ran as bounded Hermes subagents on the same host, so this is `independent-agent` review in the repository's sense, not cross-vendor isolation.
