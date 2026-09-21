# Host adapters: per-host capability declarations, on-demand host payloads, a first-class Hermes entry and per-host conformance evidence

- ID: `20260921-host-adapters`
- Size: `L`
- Status: shaping
- Created: 2026-09-21

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: this change restructures the closed agent-install contract at a cross-system boundary — the single global adapter capability object becomes a per-host registry with conformance labels, the managed set gains a host partition so installed payloads and activation identities differ per host, and the installed copy starts recording a host selection — so it is compatibility-relevant at size L
- Decision owner: Tech Lead author, `vibe_tech_lead` perspective (Hermes subagent, dispatched 2026-09-21), which authored `docs/decisions/0019-host-adapters.md`
- Governing decision: `docs/decisions/0019-host-adapters.md`
- No-new-decision rationale: none
- Review mode: `sequential-perspective`
- Review result: `approved`
- Review evidence: `docs/work-items/20260921-host-adapters/technical-review.md#Pass 2 — approved`
- Material product decisions: resolved by the product owner on 2026-09-21 (iteration 0.10.0): (a) on-demand host payloads ship with this work item — the footprint concern merges here, while moving the CLI into `.vibe/bin/` stays in the boundary work item; (b) splitting the single-file CLI is deferred to a later iteration; (c) "verified integration" is labeled per host — Hermes only after the dual-host conformance evidence lands; until then it reads "supported, unverified" and unverified hosts stay fail closed
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator, Hermes session 2026-09-21
- Confirmed at: 2026-09-21T22:12:57+08:00
- Confirmation basis: ADR 0019 at revision 2 was reviewed against the brief's acceptance criteria; Pass 1 returned changes-required on two blocking precision defects (an unprovable byte-for-byte install claim and a release-payload filtering misstatement), the author's narrow revision corrected them, and Pass 2 approved with three non-blocking notes carried into `implementation.md` (the core-protocol re-check, the managed-text sweep, and the minimal Hermes entry); the review ran as a separate sequential pass because the host's subagent channel times out on analysis-shaped review tasks at its 600 s budget
- Readiness history: 2026-09-21 the trigger scan found the closed-contract and compatibility trigger above; the record started `decision-required + blocked` with no application or shared implementation code edited; the Tech Lead author (subagent) then wrote `docs/decisions/0019-host-adapters.md`; review Pass 1 required two precision fixes, revision 2 landed, and Pass 2 approved it as `docs/work-items/20260921-host-adapters/technical-review.md#Pass 2 — approved` recording `Capability limitation: identity-isolated independent reviewer unavailable`; the gate then moved to `implementation-ready`

## Goal

Codex and Hermes can both adopt and operate a Vibe Kit installation as first-class hosts with honest per-host capability claims: installation copies only the selected hosts' payload, the contract declares each supported host's capabilities, conformance and payload, host-specific files stop riding along into projects that did not select that host, Hermes gets a documented first-class entry with a role mapping, and "verified integration" becomes a per-host label backed by conformance evidence — while Codex keeps its existing behavior and unverified hosts stay fail closed.

## Context

- Iteration 0.10.0 requirement W6 (product owner, 2026-09-21): the design must not bind to a specific agent host; in effect both Codex and Hermes must be usable and verifiable. The footprint requirement's payload concern (host-specific payloads installed unconditionally) merges here by the product owner's decision; the boundary-visibility surfaces stay in the boundary work item.
- Measured coupling (2026-09-21 research): `agent-install.json#adapter` is a single global object (`codex`, protocol 7, `current_claim: false` for reload and handoff, manual supported); `managed_source_files()` in `bin/vibe` hardcodes `.codex/agents/vibe-*.toml` (line 1074) and globs `.agents/skills/vibe-*` so `.agents/skills/vibe-feedback-flow/agents/openai.yaml` rides along; `RUNTIME_DISCOVERY_ROOTS` includes `.codex/agents/` (line 640); the distribution plugin is Codex-only (`distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json` plus `openai.yaml` under two plugin skills).
- Prose is already host-neutral (work item 0015 / ADR 0015: "the adapter fields describe the installing host rather than the running one"; the manual new-task path is host-neutral). The remaining gap is machine-declared per-host capability claims, selective payloads and per-host evidence.
- 0.10.0 items 1–3 are closed on this repository (`readiness-naming-grammar`, `verify-contract-closure`, `takeover-admission`); this is the multi-host item the iteration plan reserves as L.
- Real Hermes runs exist under the kit's own process (this iteration: briefs, sequential reviews, QA harnesses and verification records produced by Hermes sessions on 2026-09-21) to freeze as Hermes-side conformance evidence, with the recorded capability limitations.
- Applicable decisions: ADR 0005 (bootstrap plugin capabilities), ADR 0007 (agent-first adoption contract), ADR 0012 (capability honesty in the operating model), ADR 0015 (host-neutral manual activation), ADR 0002/0011 (repo-pinned offline trust model, unchanged here).

## Scope

- In: the per-host registry in `agent-install.json` (capability claims, conformance labels with evidence references, payload partitions) replacing the single global capability object while keeping installing-host provenance; the host partition in the managed set and every consumer (`managed_source_files`, install, plan, upgrade, doctor, release payload, activation identity); host selection on `init`/`adopt` (default preserves current behavior) recorded in the installed copy; the Hermes first-class entry and role mapping (approval-prompt and subagent-budget differences in the capability table); per-host conformance records (five stages) and the per-host "verified integration" labeling rule; `AGENT_INSTALL.md` updates; regression tests in `tests/`; the new decision record; this work item's records; release-identity mirrors (same change).
- Out: moving the CLI into `.vibe/bin/` and the boundary-visibility surfaces (boundary work item); splitting the single-file CLI (deferred by the product owner); hosts beyond codex and hermes; the takeover object's shape or result schemas; the release itself and its version bump; the repo-pinned offline trust model.

## Acceptance criteria

- [ ] AC-1: The contract declares supported hosts with per-host capability claims (same-task reload, automatic successor handoff, manual new task — status, current claim and required receipt per host), per-host conformance labels with evidence references, and per-host payload partitions; installing-host provenance remains recorded; no managed text requires a specific host; `validate-takeover` accepts a target fingerprint whose host is any registered host and fails closed on an unknown host.
- [ ] AC-2: `init`/`adopt` accept a host selection; a Hermes-selected install carries no Codex payload files and its contract, manifest, activation identity, doctor status and receipts are coherent; a Codex-selected install is byte-equivalent to today's install (regression proof); the selection is recorded in the installed copy and preserved by upgrade.
- [ ] AC-3: Compatibility: existing installs (no recorded selection) upgrade to the new contract additively with no data migration beyond the standard upgrade and keep their files and identity; unknown or incoherent selections and stale payload of a deselected host fail closed with actionable diagnostics; revert is a single revert.
- [ ] AC-4: The Hermes entry is first-class and documented: the registry declares Hermes and a role mapping covers the kit's specialist roles for Hermes (delegation/subagent mapping), with approval-prompt and subagent-budget differences recorded in the capability table; routing prose does not require Codex.
- [ ] AC-5: Conformance evidence: one record per supported host covering the five stages (upgrade, takeover, adaptation, default verification, target re-evaluation), produced from real runs where the environment allows, with the host's limitations recorded rather than invented; "verified integration" is a per-host label whose evidence grade matches the records; hosts without evidence stay labeled lower and fail closed.
- [ ] AC-6: Contract evolution: the agent-install schema/protocol bump per the evolution rule, the maintenance bridge targets updated, older installed protocols remaining upgradeable, and every mirror (activation identity, plugin payload mirror, contract registry digest where touched) regenerated in the same change; the closed-shape validator pins the new structure and rejects drift.
- [ ] AC-7: For the frozen final candidate, the default lane passes on CPython 3.13 and 3.9, `doctor` is healthy, `validate-readiness` is valid for this brief, and every behavior change carries a regression test in `tests/` (standard-library `unittest`).

## Design and technical notes

- Lead shape for the registry (to be confirmed by the decision record): keep `adapter` as installing-host provenance (`name`, `protocol`) and add a `hosts` registry whose entries carry the capability claims, conformance labels and payload partitions — so the takeover object's `target_fingerprint` fields and the activation fingerprint fields keep their meaning and no takeover schema bump is needed; renaming the provenance fields is rejected as churn this iteration.
- Payload partition: host-neutral files (`.vibe/core/**`, `AGENT_INSTALL.md`, `agent-install.json`, `bin/vibe`, `AGENTS.md#managed-block`, host-neutral skills) plus per-host files (`.codex/agents/vibe-*.toml` and the skill-local `agents/openai.yaml` for Codex; the Hermes entry for Hermes). The installed copy records its selection so `doctor`'s activation-identity recomputation stays coherent; the source copy declares all hosts.
- Keep the closed-shape discipline: the validator pins the new structure; unknown hosts, unknown claim values and incoherent selections fail closed; no optional-field drift.
- Version strategy (to be fixed by the decision record): agent-install schema 3 → 4 and protocol 3 → 4 (shape change); whether the Codex adapter protocol (7) and the core protocol (7) move is argued in the record; the maintenance bridge keeps older protocols upgradeable.
- Conformance records: prefer real runs on this repository and a throwaway install upgraded to the candidate; for a host this environment cannot execute, record the capability limitation and hand a runbook — never relabel evidence.
- Review runs as `sequential-perspective` on this host (subagent analysis-shaped packets time out at the 600 s budget; write-shaped packets complete), recording the capability limitation.

## Risks and open decisions

- The contract restructuring cascades into activation identity, doctor, upgrade planning, release payload and their tests; the closed-shape validator and every mirror must move in one change (the 0018 pattern: update each mirror site in the same change, then re-run the mirror script).
- Existing installs select no host today; the additive mapping (absent selection → Codex) must be proven with an upgrade fixture.
- The Codex-side conformance run may not be executable from this environment (no `codex` on PATH here); the record must state what actually ran, where, and with which evidence grade — no overclaiming.
- Hermes-side payload is intentionally small (entry plus documentation); resist growing it into new managed surfaces beyond what the role mapping needs.
- Keep "no managed text requires a specific host" honest: the distribution plugin remains the Codex channel, so only its descriptive copy is neutralized where it implies a requirement, not its existence.