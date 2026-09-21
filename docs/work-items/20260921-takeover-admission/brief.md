# Takeover admission: the public takeover object, CLI receipts and the minimal manual-transfer payload

- ID: `20260921-takeover-admission`
- Size: `L`
- Status: shaping
- Created: 2026-09-21

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: the change grows the closed takeover receipt contract that `validate-takeover` enforces and that `agent-install.json` declares (a new admission receipt kind and its fail-closed rules), publishes the takeover object as a documented contract a host can rely on, and defines the minimal manual-transfer payload the successor task validates; the receipt artifact it adds becomes a durable cross-system surface that hosts cite by path and digest, so the work is compatibility-relevant at size L
- Decision owner: Tech Lead author, `vibe_tech_lead` perspective (Hermes subagent, dispatched 2026-09-21), which authored `docs/decisions/0018-takeover-admission.md`
- Governing decision: `docs/decisions/0018-takeover-admission.md`
- No-new-decision rationale: none
- Review mode: `sequential-perspective`
- Review result: `approved`
- Review evidence: `docs/work-items/20260921-takeover-admission/technical-review.md#Pass 2 — approved`
- Material product decisions: resolved by the product owner on 2026-09-21 (iteration 0.10.0) — (a) issue #8 is fixed by an independent *existing-install admission* path whose receipt binds the current host task, the canonical project and the recomputed target identity and *references* the historical upgrade transaction as its source, never claiming a new transaction ran in this directory; (b) the takeover object's closed field sets, custody transitions, evidence ordering and blocked-state contract are published where a host can read them without the CLI source; (c) the minimal manual-transfer payload is defined as a host-neutral shape that keeps custody in host task state and never persists goal text; (d) takeover-capable commands gain a stable receipt artifact (`--receipt <path>` or equivalent) so hosts cite a framework-written file instead of scraping stdout
- Open blockers: none
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator, Hermes session 2026-09-21
- Confirmed at: 2026-09-21T13:16:35+08:00
- Confirmation basis: ADR 0018 at revision 2 was reviewed against the brief's acceptance criteria; Pass 1 returned changes-required on one blocking attribution defect (the context section swapped the F2 and F7 leads and contradicted its own metadata bullet), the author's revision corrected it, and Pass 2 approved with three non-blocking notes carried into `implementation.md` (the publication's location, the receipt artifact's byte-stability mechanism, and re-derivation of the admission evidence); the review ran as a separate sequential pass because the host's subagent channel times out on analysis-shaped review tasks at its 600 s budget
- Readiness history: 2026-09-21 the trigger scan found the closed-contract and compatibility trigger above and the record started `decision-required + blocked` with no application or shared implementation code edited; the Tech Lead author (subagent) then wrote `docs/decisions/0018-takeover-admission.md`; review Pass 1 required one attribution fix, revision 2 landed, and Pass 2 approved it as `docs/work-items/20260921-takeover-admission/technical-review.md#Pass 2 — approved` recording `Capability limitation: identity-isolated independent reviewer unavailable`; the gate then moved to `implementation-ready`

## Goal

A healthy installation restored into a new directory can be admitted to development by a new host task independently and truthfully — without claiming an upgrade that never happened there and without a user exception; the takeover object becomes a published contract instead of invariants reverse-engineered from the CLI source; a host can cite a framework-written receipt file rather than hashing captured stdout; and the minimal manual-transfer payload is defined so privacy boundaries hold.

## Context

- Issue [#8](https://github.com/mintgao/vibe-kit/issues/8): after a healthy install is restored from version control, the standard takeover still requires the original upgrade transaction to be bound to the current absolute directory; continuing in the real development directory needed an explicit user exception, which pressures a host toward redundant upgrades, extra copies, or a pointless task switch. Expected: a new host task can independently verify the current directory's target version, installation manifest and managed-block content, preserve the historical upgrade source, and admit the project.
- Issue [#13](https://github.com/mintgao/vibe-kit/issues/13) finding F2: `AGENT_INSTALL.md` defines the lifecycle, stages and reason codes but not the takeover object; producing a valid receipt required reading the 12,883-line CLI. The invariants hosts had to discover — closed field sets per layer, custody transitions, evidence ordering, allowed evidence per stage, and the blocked-state contract — must be published.
- Finding F7: the takeover object's evidence entries want `ref` plus `sha256`, but no CLI command writes a receipt file; the host scrapes stdout and hashes it, so "the receipt the host cites" is a host convention, not a framework product.
- Finding F12: the contract requires custody to live only in host task state and forbids persisting goal text on disk, yet the successor task must validate a "transfer identifier" that the receiving host has to mint itself; the minimal transfer format is undefined.
- Existing surface: `agent-install.json`'s `takeover` block (closed stage, reason-code, custody and outcome vocabularies, including `manual-transfer-required` and `manual-transfer-pending`), `AGENT_INSTALL.md` (the installed host guide), and `bin/vibe`'s takeover validation, activation adaptation and manual new-task fallback from work item 0015.
- Applicable decisions: ADR 0008 (readiness authority), ADR 0012 (capability honesty in the operating model), ADR 0015 (host-neutral manual activation), ADR 0017 (receipt artifacts: path plus digest — this work item reuses that pattern), and ADR 0002/0011 (the repo-pinned offline trust model, unchanged here).

## Scope

- In: the existing-install admission receipt kind and its validation rules in `bin/vibe` and `agent-install.json`; the published takeover-object contract (in `AGENT_INSTALL.md` or a linked contract page) and the drift test that binds the published rules to `validate-takeover`; the minimal manual-transfer payload definition and its validation; a stable receipt artifact for takeover-capable commands (`--receipt <path>` or equivalent); regression tests in `tests/`; the new decision record; this work item's records; the release-identity mirrors (same change).
- Out: the verify surfaces closed by work item 2; host adapters and per-host payloads (work item 4); the release itself and any version bump; any change to the trust model or to custody's privacy rules (goal text never persisted, custody stays in host task state); rewriting or reinterpreting historical receipts.

## Acceptance criteria

- [ ] AC-1: A healthy installation whose historical upgrade transaction is bound to a different directory is admitted by a new host task through an *existing-install admission* receipt that binds the current host task, the canonical project directory and the recomputed target identity (manifest, activation set, managed block), and *references* the historical upgrade transaction as its source; the receipt records no new transaction for this directory; after admission the project runs the default verification and continues development in that directory; historical receipts stay byte-identical.
- [ ] AC-2: Admission validation fails closed on: target content that no longer matches the recomputed identity; an admission receipt with no historical upgrade source; recorded fingerprints that disagree with a fresh recomputation; and any claim of `upgraded`, `activated` or `ready` beyond the evidence the receipt carries.
- [ ] AC-3: The takeover object's contract is published where a host can read it without the CLI source — closed field sets per layer (top-level, source, versions, target fingerprint, activation, goal, stages, evidence, next action, upgrade transaction), the custody transition table including the null-carrying `manual-transfer-required` versus the active-task-carrying `manual-transfer-pending`, the evidence ordering rules (global uniqueness, strict increase within custody, activation evidence after the apply receipt, pending before activation evidence, successor-owned after activation evidence), the evidence types each stage allows, and the blocked-state contract (exactly one blocked stage, later stages not-started, reason codes paired one-to-one with action codes) — and a test asserts the published rules and `validate-takeover` agree, so documentation drift fails the lane.
- [ ] AC-4: A takeover-capable command writes the receipt to a stable path (`--receipt <path>` or equivalent); the written file is byte-stable for a fixed outcome, self-describing, and its digest is exactly what a host cites in an evidence entry's `ref` plus `sha256`; a regression test proves the artifact and the digest.
- [ ] AC-5: The minimal manual-transfer payload is defined (opaque transfer id, goal, accepted decisions, unfinished state, evidence references) together with its validation rules and its disk boundary (goal text never persisted; custody stays in host task state); the successor validation accepts a conforming payload and rejects an incomplete or forged one.
- [ ] AC-6: Compatibility and recovery: the change is additive to the takeover contract; receipts produced under earlier contracts keep their recorded semantics and their validation outcomes; the new path is revertible with no migration; no published profile boundary moves; release-identity mirrors are regenerated in the same change.
- [ ] AC-7: For the frozen final candidate, the default lane passes, `doctor` is healthy, `validate-readiness` is valid for this brief, and every behavior change carries a regression test in `tests/` (standard-library `unittest`).

## Design and technical notes

- Receipt artifact: follow ADR 0017 and work item 2's pattern — the artifact is written under the project's local state, referenced by path plus digest, and the digest is recomputable; the artifact must be byte-stable for a fixed outcome (no timestamps that move the digest between identical runs, or the timestamp is excluded from what the host hashes).
- Admission receipt: model it as its own origin kind with its own required evidence rather than loosening the upgrade-transaction binding of the existing receipts; the historical upgrade transaction is referenced by its recorded identifier and digest, never rewritten.
- Published contract: prefer a dedicated contract page linked from `AGENT_INSTALL.md` if the guide would otherwise grow past its managed-block discipline; the drift test reads the published rules and compares them with the compiled vocabularies in `bin/vibe`, in the same spirit as the existing agent-install contract tests.
- Manual-transfer payload: keep the opaque id host-minted and meaningless to the framework; the successor validates shape, freshness and evidence references, not goal text on disk.
- Identity mirrors: this change touches payload files (`bin/vibe`, `AGENT_INSTALL.md`, `agent-install.json`), so the release-identity mirrors must be regenerated in the same change (procedure recorded in `docs/work-items/20260921-readiness-naming-grammar/verification.md` and `docs/work-items/20260921-verify-contract-closure/verification.md`).

## Risks and open decisions

- Admission could become a bypass of the upgrade machinery: the recomputed identity must be re-derived at validation time from the target content, never trusted from the receipt alone, and AC-2's negatives must stay rejected.
- Publishing the object risks documentation drift; the drift test is the mitigation, so it must assert the published rules rather than restate them.
- The transfer payload's validation surface should stay the smallest coherent one; if a new subcommand is proposed it must be justified against extending the existing manual path, and the decision is recorded before implementation.
- Recovery: the change is additive and revertible; historical receipts are never rewritten, and a failed admission leaves the target's existing install untouched.
- Review note carried from work item 2: this host's subagent channel times out on analysis-shaped tasks at its 600 s budget, so the working assumption is a sequential-perspective review unless an independent reviewer completes; the record must state whichever actually happened.