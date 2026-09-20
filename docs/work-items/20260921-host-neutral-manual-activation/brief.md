# Host-neutral manual new-task activation and consistent release identity

- ID: `20260921-host-neutral-manual-activation`
- Size: `M`
- Status: shaping
- Created: 2026-09-21

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: the change alters a durable shared contract (who may own the successor task on the manual activation path, and what the managed takeover-schema reference means) and touches a compatibility boundary between the kit's contracts and a non-Codex host
- Decision owner: read-only Tech Lead author, `vibe_tech_lead` perspective (Hermes subagent, dispatched 2026-09-21)
- Governing decision: `docs/decisions/0015-host-neutral-manual-activation.md`
- No-new-decision rationale: none
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: `docs/work-items/20260921-host-neutral-manual-activation/technical-review.md#Pass 2 — approved`
- Material product decisions: none; the kit's verified-integration claim stays with the Codex adapter, and the change widens permission on the manual path only
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator, Hermes task `hermes-desktop-vibekit-20260921`
- Confirmed at: 2026-09-20T16:22:11Z
- Confirmation basis: ADR 0015 is Accepted and governs the host-neutral manual path and the managed-contract agreement; the independent Tech Lead review passed on revision 2 after a `changes-required` first pass (`technical-review.md#Pass 2 — approved`); the change stays prose and scope only, with no schema, protocol, validator or CLI-result change; no material product decision is open
- Readiness history: 2026-09-21 trigger scan during shaping found a durable shared contract and compatibility trigger, so the record started `decision-required + blocked` and no application or shared implementation code was edited; review pass 1 returned `changes-required` (four items), the decision was revised to revision 2, and review pass 2 returned `approved`

## Goal

A host that is not Codex — for example a Hermes session — can adopt, develop under, and take over a Vibe Kit project through the documented manual new-task path without having to guess whether the contract permits it, and this repository's own verification lane and release identity stay consistent on `main` for the next requirement.

## Context

The 0.9.0 contracts scope the manual fallback in three places a non-Codex host must read: the managed `AGENTS.md` block says to follow `AGENT_INSTALL.md` "for takeover schema 1" while the installed `agent-install.json` declares `takeover.schema_version: 2`; the block and `AGENT_INSTALL.md` both end the degraded path with "create a new Codex task"; and `bin/vibe` prints the same Codex-scoped instruction. A real migration recorded by a receiving host ([issue #13](https://github.com/mintgao/vibe-kit/issues/13), with #10 and #12) satisfied the manual path and validated its takeover object, but the contract never said whether a non-Codex host may use that path.

Repository evidence at the same time: `main` at `87225de` fails the default lane. The post-publication homepage commit changed `README.md`, which is a release-payload file, without regenerating the two payload-identity mirrors (`distribution/plugin-src/vibe-kit/.codex-plugin/plugin.json` and `.vibe/manifest.json#source.payload_tree_sha256`), so `./bin/vibe package` exits 2 and five packaging tests fail on both CPython 3.9 and 3.13. `doctor` reports healthy because it does not check that mirror.

Applicable decisions: ADR 0001 governs managed/project ownership; ADR 0007 governs agent-first adoption; ADR 0009 governs the post-upgrade takeover lifecycle; ADR 0011 governs exact-source trust and the host-owned publication boundary; ADR 0014 governs the managed-block documentation contract. This work changes none of their schemas, receipts, or validators.

## Scope

- In: the managed `AGENTS.md` block, `AGENT_INSTALL.md`, the bootstrap and maintain Plugin Skills, the `bin/vibe` instruction strings, both homepage files where they state the fallback action, `CHANGELOG.md`, the release-identity mirrors, the contract-consistency regression tests, ADR 0015, and this work item.
- Out: schema, protocol, enum, validator, receipt, custody, or CLI-result behavior; the Codex adapter's verified-integration claim; new host adapters; publishing the takeover object schema or adding a receipt helper (issue #13 findings F2/F7/F12); recording host capability limitations for bounded subagents (F10); an environment-limited check state (F11); configured-check ordering (issue #9); any version bump or publication.

## Acceptance criteria

- [ ] AC-1: The managed `AGENTS.md` block and `AGENT_INSTALL.md` name the takeover schema the installed `agent-install.json` declares, and no surface states a conflicting schema number; a regression test fails when the block and the installed contract disagree.
- [ ] AC-2: The manual-fallback action is host-neutral in every managed contract surface (`AGENTS.md` block, `AGENT_INSTALL.md`, both Plugin Skills, `bin/vibe` instruction output, both homepage files); no surface requires "a Codex task", and a regression test fails if a single-host name is reintroduced there.
- [ ] AC-3: `AGENT_INSTALL.md` states explicitly that the manual new-task path is available to any host that can start a new task in the same project, that adapter metadata and the activation fingerprint describe the host that installed or adopted the version rather than the host that owns the successor task, and that the receipt requirements and fail-closed rule are unchanged.
- [ ] AC-4: No schema, protocol, enum, validator, receipt, or CLI-result behavior changes: `agent-install.json` keeps its closed top-level field set and adapter capability claims, `takeover` schema 2 and core/Codex protocol 7 stay unchanged, and `validate-takeover` still accepts the same valid objects and rejects the same invalid ones.
- [ ] AC-5: Release identity is consistent with the tree: `./bin/vibe package --output <dir>` succeeds, the Plugin manifest and `.vibe/manifest.json` payload digests equal the recomputed payload-tree digest, and the activation mirrors equal `source_activation_identity`; a regression test covers the payload-digest consistency that `main` violated.
- [ ] AC-6: `CHANGELOG.md` records the published 0.9.0 release.
- [ ] AC-7: For the frozen final candidate, the default verification lane passes on CPython 3.9 and 3.13, `doctor` is healthy, and `validate-readiness` returns valid for this brief.

## Design and technical notes

`AGENT_INSTALL.md` is the normative host-facing contract; the managed block is its in-context summary; the Plugin Skills are the bootstrap and maintenance surfaces; `bin/vibe` prints the fallback instruction. All of them must carry the same host-neutral action, so the change is one decision applied to five surfaces plus the homepage pair.

The managed block keeps one physical line per prose paragraph and keeps every phrase the existing contract tests require. `agent-install.json` is deliberately not edited except for its regenerated activation mirror, because its top-level field set and adapter capability claims are closed and validated.

Identity regeneration follows the repository's own procedure: recompute `source_activation_identity(ROOT)` and `payload_tree_sha256(ROOT)`, generate the manifest through a production `init --source-type local-payload --source-ref 0.9.0` install in a disposable directory, and copy the generated manifest into the source checkout.

## Risks and open decisions

- A host-neutral action sentence could be read as widening the compatibility claim. The decision record states the opposite explicitly: the Codex adapter remains the only verified integration; only permission on the manual path is clarified.
- The regression tests added here are structural consistency checks. They cannot prove that a live host produced a conforming receipt, which stays host-owned evidence.
- `CHANGELOG.md` is a payload file; the release section and the identity mirrors must land in the same change or the lane goes red again.
