# 0019: Host adapters — per-host capability declarations, on-demand host payloads, a first-class Hermes entry, and per-host conformance evidence

- Status: Accepted
- Date: 2026-09-21
- Decision owner: read-only Tech Lead author `vibe_tech_lead`
- Work item: `docs/work-items/20260921-host-adapters/brief.md`
- Evidence: that brief's measured coupling (2026-09-21), iteration 0.10.0 requirement W6, ADR 0015's host-neutrality decision, and the contract, activation, install and plan surfaces in bin/vibe and agent-install.json

## Context and applicable decisions

Iteration 0.10.0 requirement W6 (product owner, 2026-09-21) requires that the design must not bind to a specific agent host: both Codex and Hermes must be usable and verifiable. The installed contract binds capability claims to one global object — `adapter` is `codex`, protocol 7, `current_claim: false` for same-task reload and automatic successor handoff, `manual_new_task` supported — and `managed_source_files()` hardcodes the `.codex/agents` path and globs `vibe-*.toml` (bin/vibe 1074–1076) while globbing `.agents/skills/vibe-*`, so `.agents/skills/vibe-feedback-flow/agents/openai.yaml` rides into every project, including one that never runs Codex.

Prose neutrality is already decided. ADR 0015 states that the adapter fields describe the installing host rather than the running one and that the manual new-task path is host-neutral. What remains is machine-declared per-host capability claims, selective payloads, and per-host evidence.

The contract is closed and pinned. `validate_agent_install_contract_shape` (bin/vibe 7933) pins the top-level field set, the exact `adapter.capabilities` object and the expected activation statics, and the activation fingerprint includes `adapter_name` and `adapter_protocol` (bin/vibe 1598–1605). Restructuring the capability object therefore cascades into the validator, the activation identity, the plugin payload mirror and the contract registry digest; every mirror must move in the same change, following the 0018 pattern.

ADR 0005 governs the bootstrap plugin's capabilities, ADR 0007 the agent-first adoption contract, ADR 0012 capability honesty in the operating model, and ADR 0015 the host-neutral manual activation path; ADRs 0002 and 0011 pin the offline trust model, which this record leaves untouched.

## Decision 1: a per-host capability registry replaces the single global capability object

`adapter` remains the installing host's provenance and keeps only `name` and `protocol` — the host that installed or adopted this version, read exactly as ADR 0015 reads it. The capability claims leave it.

A `hosts` registry keyed by host name carries, per host: `protocol`; the three capability claims (same-task reload, automatic successor handoff, manual new task — each with status, `current_claim` and `required_receipt`); a conformance label, `verified` or `supported-unverified`, with its evidence references; and the host's payload paths.

Because provenance keeps its name and shape, the takeover object's `target_fingerprint` fields and the activation fingerprint keep their meaning, and no takeover schema bump is required.

An unknown host fails closed wherever the registry is read.

## Decision 2: the managed payload is host-partitioned and the selection is explicit

`managed_source_files()` gains a host dimension. Host-neutral files (`.vibe/core/**`, `AGENT_INSTALL.md`, `agent-install.json`, `bin/vibe`, the `AGENTS.md` managed block, host-neutral skills) stay in every install; per-host files ride only with their host — `.codex/agents/vibe-*.toml` and the skill-local `agents/openai.yaml` for Codex, the Hermes entry for Hermes.

`init` and `adopt` gain a host selection, and the default `codex` carries the same managed file set as today's default install — every pre-change managed path, including the Codex payload — with content differences limited to the versioned contract change itself.

The installed copy records the selection in the contract and the manifest, and the activation identity is computed over the selected set so `doctor`'s recomputation stays coherent. Install, plan, upgrade and doctor apply the recorded selection; the release payload must contain every declared host's files — the partition defines the groups, it never shrinks the release.

Existing installs that record no selection map to `codex` additively: no data migration beyond the standard upgrade, and their files and identity are preserved. Stale files of a deselected host, and unknown or incoherent selections, fail closed with actionable diagnostics.

## Decision 3: Hermes is a first-class host entry

`hermes` is registered in the `hosts` registry with the same manual-fallback claims: its same-task reload and automatic successor handoff stay conditional and unclaimed, and manual new task is supported with the `manual-task-start` receipt.

The entry carries a role mapping from the kit's specialist roles (investigator, pm, qa, rd, tech-lead, ux) to Hermes delegation and subagents, with the approval-prompt and subagent-budget differences recorded in the capability table.

Distribution copy is neutralized wherever it implies a required host. The Codex plugin remains the Codex channel; it no longer implies a requirement.

The Hermes managed surface stays small on purpose: the registry entry plus documentation. It is not grown into new managed surfaces beyond what the role mapping needs.

## Decision 4: conformance evidence is per host, and labels follow evidence

Each supported host gets one conformance record covering five stages: upgrade, takeover, adaptation, default verification, and target re-evaluation.

`verified integration` becomes a per-host label. A host reads `verified` only where its record is complete and its evidence grade matches; Hermes stays `supported-unverified` until its record lands.

Hosts without evidence fail closed. The record states limitations — including any stage this environment cannot execute — instead of inventing a run; where a real run is impossible, the limitation is recorded and a runbook is handed over at the evidence grade that actually exists.

## Decision 5: version and evolution handling

Agent-install schema moves 3 → 4 and the agent-install protocol moves 3 → 4: the closed shape changed.

The Codex adapter protocol stays 7, because its claims are unchanged, and Hermes starts at protocol 1.

Core protocol stays 7: this change introduces no core-surface change that would require otherwise.

In the maintenance bridge, `target_agent_install_schema` and `target_agent_install_protocol` move to 4 while `supported_installed_agent_protocols` keeps the older values, so existing installs remain upgradeable.

Every mirror is regenerated in the same change: the activation identity, the plugin payload mirror, and the contract registry digest where touched.

## Alternatives weighed

- Renaming the provenance fields, or removing `adapter` entirely. Rejected: both cascade into the takeover and activation fingerprints for naming only.
- One global capability object with a note that other hosts assume the same claims. Rejected: it fails the honesty requirement — an unmentioned host's claims would be asserted rather than declared and measured.
- Auto-detecting the host at upgrade time. Rejected: a host is not detectable offline from a repository, so the selection must be explicit and preserved.
- Installing all host payloads and pruning later. Rejected: it keeps the footprint problem and invites destructive upgrades.
- Growing a Hermes-specific managed surface. Rejected: unnecessary; the entry stays minimal.
- Treating the Codex plugin as the only path. Rejected: the plugin stays the Codex channel, but it no longer implies a requirement.

## Consequences and boundaries

The change is additive where possible: existing installs keep working, map to `codex` with no migration, and stay upgradeable through the maintenance bridge. Revert is a single revert of this change.

The repo-pinned offline trust model of ADRs 0002 and 0011 is unchanged: no network access, no remote attestation, and no change to how a pinned installation resolves its source.

The boundary work item still moves the CLI into `.vibe/bin/` and owns the boundary-visibility surfaces; this record does not touch them. The release work item carries the CHANGELOG, homepage and version updates. DSH Mint is unaffected until its next upgrade.

## Verification

The closed-shape validator must pin the new structure — the `hosts` registry, the per-host claim objects and the conformance labels — and reject drift, with a drift test binding the declared claims to what the validator enforces.

Per-selection fixture installs must prove both directions: a Codex-selected install carrying the same managed file set as today's default install, with content differences limited to the versioned contract change, and a Hermes-selected install carrying no Codex payload with coherent contract, manifest, activation identity, doctor status and receipts.

An upgrade fixture from a pre-change install with no recorded selection must upgrade additively to `codex` with its files and identity preserved; unknown or incoherent selections and stale payload of a deselected host must fail closed with actionable diagnostics.

Each supported host's conformance record must cover the five stages and its label must match the evidence grade; a host without a record stays `supported-unverified` and fails closed.

For the frozen final candidate, the default lane must pass on CPython 3.13 and 3.9, `doctor` must be healthy, `validate-readiness` must be valid for the brief, and every behavior change must carry a regression test in `tests/` using the standard-library `unittest`.

## Follow-ups out of scope

- Moving the CLI into `.vibe/bin/` and the boundary-visibility surfaces, which belong to the boundary work item.
- Splitting the single-file CLI, deferred to a later iteration.
- Host re-selection as an explicit later operation.
- Revisiting the Hermes label as its conformance evidence grows.
- Hosts beyond `codex` and `hermes`.
