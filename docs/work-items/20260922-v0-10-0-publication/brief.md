# Publish Vibe Kit v0.10.0

- ID: `20260922-v0-10-0-publication`
- Size: `L`
- Status: shaping
- Created: 2026-09-22

## Technical decision readiness

- Outcome: `decision-required`
- Trigger evidence: an L-sized public release moves the external version boundary, the compatibility surface that existing installs upgrade through, and the version-specific publication contract that fixes the tag, Release, asset set and operation allowlist — so it is a durable, compatibility-relevant choice at size L
- Decision owner: `vibe_tech_lead` perspective (Hermes subagent, dispatched 2026-09-22), which authors `docs/decisions/0020-v0-10-0-publication.md`
- Governing decision: none
- No-new-decision rationale: none
- Review mode: `not-required`
- Review result: `not-required`
- Review evidence: none
- Material product decisions: the product owner's iteration 0.10.0 plan reserves this item as the release of the iteration that closed the readiness grammar, verification contract, takeover admission and host adapters; the public GitHub operations stay out of scope until the product owner gives one later authorization bound to the exact publication intent digest
- Open blockers: the version-specific publication profile for v0.10.0 is undecided; no application or shared implementation code may be edited before the gate is `implementation-ready`
- Gate: `blocked`
- Gate owner: Workflow orchestrator
- Confirmed at: none
- Confirmation basis: none
- Readiness history: `2026-09-22 — the trigger scan found the version/compatibility and publication-contract triggers; the record starts decision-required + blocked with no application or shared implementation code edited`

## Goal

Ship the verified iteration 0.10.0 product as Vibe Kit `0.10.0`: one exact, non-draft GitHub Pre-release whose five public assets can be downloaded and validated offline, with the per-host registry and the schema-4 Agent-install contract published, both homepages synchronized, and no weakening of the historical v0.7/v0.8/v0.9 publication guarantees.

## Context

- Iteration 0.10.0 closed four work items on this repository: `20260921-readiness-naming-grammar`, `20260921-verify-contract-closure`, `20260921-takeover-admission` and `20260921-host-adapters` (verified at `d5fa87a`).
- `20260921-host-adapters` advanced the installed contract to Agent-install schema/protocol 4 and published the per-host registry; the source still carries kit version `0.9.0` and the maintenance bridge still bounds installs at `maximum_installed_kit_version_exclusive 0.9.0`, so a v0.9.0 install cannot yet upgrade into the candidate.
- `v0.9.0` is the latest published non-draft GitHub Pre-release; its publication profile is schema 3 and its #6/#7 closeout is schema 2.
- The `vibe-release` Skill, the publication profiles in `bin/vibe` and the release tests encode the exact v0.7/v0.8/v0.9 boundaries. A v0.10.0 publication needs its own reviewed version boundary before release tooling is edited.
- Both homepages (`README.md`, `README.zh-CN.md`) state the published version, the adoption links, the protocol/schema paragraph and the limitations; `AGENT_INSTALL.md` carries version literals that no check binds to the framework version.

## Scope

- In:
  - Version identity: `0.10.0` across `.vibe/core/version`, `.vibe/version`, the installed contract's `kit_version`, the Plugin metadata, the maintenance bridge's `maximum_installed_kit_version_exclusive`, and every mirror regenerated in the same change.
  - `CHANGELOG.md` and `docs/releases/0.10.0.md` describing the iteration honestly.
  - Both homepages reviewed for version, links, installation commands, capabilities and limitations, with reasons recorded for unchanged sections.
  - The version-specific publication profile for `0.10.0` (tag, title, body path, five assets, operation allowlist, issue policy) and its tests, with historical profiles keeping exact semantics.
  - Release gates on the frozen candidate: default lane on CPython 3.13 and 3.9, `doctor`, `validate-readiness`, `package`, `validate-release`, and two independent clean builds.
  - The bounded guide-version drift check this item's Close identified, so the managed guide cannot ship a stale version literal.
- Out:
  - Any GitHub write in this item without a later explicit authorization bound to the exact publication intent digest: no push, tag, Release, asset upload or issue operation.
  - Stable promotion, draft Releases, Plugin Directory publication, signing, provenance, automatic updates, or platform-immutability promises.
  - Force push, tag movement, Release rewrite, asset replacement or destructive rollback.
  - New product behavior beyond the version identity, documentation and publication profile.

## Acceptance criteria

- [ ] AC-1: The source advances to kit version `0.10.0` coherently — `.vibe/core/version`, `.vibe/version`, `agent-install.json#kit_version`, the Plugin metadata and the maintenance bridge's `maximum_installed_kit_version_exclusive` — with every mirror regenerated in the same change, `doctor` healthy and the recorded identity equal to a fresh recomputation.
- [ ] AC-2: `CHANGELOG.md` and `docs/releases/0.10.0.md` describe the iteration (readiness grammar, verification contract, takeover admission, host adapters with the per-host registry and the schema-4 contract) without unearned claims; both homepages are reviewed and synchronized for version, links, installation commands, capabilities and limitations, with a reasoned record for unchanged sections.
- [ ] AC-3: A closed `0.10.0` publication profile fixes version, annotated tag, Release title and body path, exactly five assets, the operation allowlist and the issue policy; historical profiles keep exact semantics, a v0.10.0 candidate cannot pass them, and the profile is pinned by tests.
- [ ] AC-4: An install recorded at `0.9.0` upgrades into the candidate through the maintenance bridge with its files, recorded selection and identity preserved, and a fresh install of the candidate is doctor-healthy for a `codex`, a `hermes` and a combined selection.
- [ ] AC-5: The managed guide's version literals agree with the framework version, bound by a drift check that fails when they diverge.
- [ ] AC-6: On the frozen candidate, the default lane passes on CPython 3.13 and 3.9, `doctor` is healthy, `validate-readiness` is valid, `package` and `validate-release` pass, and two independent clean builds from the same commit produce byte-identical five-asset sets.
- [ ] AC-7: Public completion language is reserved: no GitHub write happens in this work item, and "v0.10.0 published and verified" is claimable only from `confirmed-complete` remote state plus passed public verification under a separate authorization bound to the frozen intent digest.

## Design and technical notes

- The decision record fixes: whether the publication intent/receipt schemas move with the new profile, which historical profile entry points stay frozen, how the bridge bound advances while older installed protocols stay upgradeable, and what the release notes may claim about host conformance labels.
- The publication contract stays host-owned and offline: the CLI plans, validates and receipts; the Agent/host performs any remote operation under an explicit authorization.
- Keep the version bump and the mirror regeneration in one change; the release tests own the proof.

## Risks and open decisions

- The publication profile restructuring cascades into the intent/receipt validators and the release tests; the historical profiles must keep byte-exact semantics while the new one is added.
- Advancing the bridge bound is what makes a v0.9.0 install upgradeable; getting it wrong either strands existing installs or admits an out-of-range predecessor, so the upgrade fixture must cover it.
- The release notes must not raise the Hermes conformance label: the host registry records `supported-unverified` until its five-stage record is complete.
- Homepage facts and the guide's version literals are prose; both need the review and the drift check this item adds.
- The final remote write request must bind one frozen intent digest; the current user request is not an executable authorization for an intent that does not yet exist.
