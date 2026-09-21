# 0018: Takeover admission — existing-install receipts, a published takeover contract, receipt artifacts, and a host-neutral transfer payload

- Status: Accepted
- Date: 2026-09-21
- Decision owner: read-only Tech Lead author `vibe_tech_lead`
- Work item: `docs/work-items/20260921-takeover-admission/brief.md`
- Evidence: feedback issue #8 and issue #13 findings F2, F7 and F12, and the takeover surface in bin/vibe and agent-install.json

## Context and applicable decisions

The takeover surface admits a healthy installation only through an upgrade path. A directory restored from version control, or installed on a host that never ran an upgrade here, carries no upgrade transaction in this directory, so a host that wants to take it over has to either claim an upgrade that did not happen or ask for a user exception. Neither is acceptable for an installation that is simply healthy.

F2 is the contract gap. The takeover object is a shape the CLI enforces, but its rules — the closed field sets, the custody transitions, the evidence ordering, which evidence types each stage allows, what a blocked takeover looks like — live only in the CLI source and in whatever a host can infer from a rejection. A host that must produce or validate a takeover object cannot read the contract it is being held to.

F7 is the capture gap. A command's receipt is the captured stdout a host scrapes and hashes. The citation a host records therefore rests on private host behaviour and on a stream that can carry host-specific noise, and two hosts capturing the same outcome can arrive at different digests.

F12 is the transfer gap. The manual-transfer path that carries custody between tasks has no defined minimal payload and no validation rules, so what a successor must check is left to the host that wrote it.

Issue #8 is the admission gap seen from the host side: the takeover surface in bin/vibe and the closed declaration in agent-install.json admit an installation through the upgrade path, and a host that holds a healthy installation with no upgrade in this directory has no compliant way to say so.

The four decisions below close these gaps together. The first supplies the missing receipt kind, the second makes the contract the receipt is judged by readable outside the CLI, the third gives the citation a framework-produced artifact, and the fourth defines the transfer payload the successor validates.

ADR 0008 governs readiness authority, ADR 0012 governs capability honesty in the operating model, ADR 0015 governs the host-neutral manual activation path, and ADR 0017 governs receipt artifacts addressed by path plus digest. This record extends the takeover contract under those decisions and changes none of them.

## Decision: existing-install admission is its own receipt kind with its own required evidence

Admission of an existing installation is a receipt kind of its own. It binds the current host task, the canonical project directory, and the recomputed target identity — the installation manifest, the activation set, and the managed block — and it references the historical upgrade transaction by its recorded identifier and digest as its source.

It never claims that a new upgrade transaction ran in this directory. The historical receipt is referenced, never rewritten, so the source transaction keeps exactly the semantics it recorded when it was written.

The purpose is narrow and stated: a healthy installation restored from version control must be admissible without a user exception and without falsely recording an upgrade that did not happen here.

## Decision: the takeover object becomes a published contract

The takeover object's rules are published where a host can read them without the CLI source. The publication carries the closed field sets per layer — top-level, source, versions, target fingerprint, activation, goal, stages, evidence, next action, and upgrade transaction — the custody transition table, the evidence ordering rules, the evidence types each stage allows, and the blocked-state contract.

The custody transition table is part of the published contract, including the pair that is easy to conflate: manual-transfer-required carries a null custody value, while manual-transfer-pending carries an active task. The distinction is published rather than left to inference from a rejection.

The evidence ordering rules are published as rules: global uniqueness of evidence, strict increase within a custody, activation evidence after the apply receipt, pending evidence before activation evidence, and successor-owned evidence after activation evidence.

The blocked-state contract is published as stated: exactly one blocked stage, later stages recorded as not-started, and reason codes paired one-to-one with action codes.

A drift test binds the published rules to what `validate-takeover` actually enforces, so documentation drift fails the lane rather than surfacing as a host's confusion.

## Decision: takeover-capable commands write a stable receipt artifact

Takeover-capable commands write a receipt artifact, addressed by `--receipt <path>` or an equivalent. The artifact is byte-stable for a fixed outcome and self-describing, so a reader can identify it without out-of-band context.

Its digest is exactly what a host cites in an evidence entry's ref plus sha256. A framework-written file therefore replaces the host convention of capturing and hashing stdout: the citation rests on an artifact the framework produced under a stated contract, not on private host capture behaviour.

## Decision: the minimal manual-transfer payload is a host-neutral shape

The minimal manual-transfer payload is defined as a host-neutral shape: an opaque transfer identifier, the goal, the accepted decisions, the unfinished state, and evidence references. Its validation rules are defined alongside the shape and published under the contract decision above.

Custody stays in host task state, and goal text is never persisted to disk. The successor validates the payload's shape, its freshness, and its evidence references; it does not read goal text from disk, because the contract does not put it there.

## Alternatives weighed

- Loosening the upgrade-transaction binding so a restored directory counts as upgraded. Rejected: it records a transaction that never happened in this directory, which is the exact falsehood the framework must not carry.
- Letting hosts keep scraping and hashing captured stdout. Rejected: the citation then rests on private host behaviour, and stdout can carry host-specific noise that changes the digest for the same outcome.
- Having the framework mint and persist the transfer identifier. Rejected: custody belongs to host task state, and persisting it would move the privacy boundary.
- Persisting the goal text to simplify transfer. Rejected: the contract forbids persisting goal text, and simplification is not a reason to cross that line.

## Consequences and boundaries

This record is additive to the takeover contract. No version bump is made here; the release work item owns version and profile bumps.

Receipts produced under earlier contracts keep their recorded semantics and their validation outcomes. They are never rewritten, and admission of an existing installation references a historical transaction rather than replacing it.

The repo-pinned offline trust model of ADRs 0002 and 0011 is untouched: no network access, no remote attestation, and no change to how a pinned installation resolves its source.

Custody's privacy rules are unchanged. Goal text is never persisted, custody lives in host task state, and the transfer payload's goal field is a host-supplied value the successor validates for shape and freshness rather than reads back from disk.

The change is revertible with no data migration: remove the admission receipt kind and the published contract, and the takeover surface returns to the previous contract.

## Verification

An existing installation restored from version control must be admissible with an admission receipt that binds the host task, the canonical project directory, and the recomputed target identity, and that references the historical upgrade transaction by identifier and digest. The historical receipt must remain byte-identical, and no new upgrade transaction may be recorded by the admission path.

A published contract must match `validate-takeover` in both directions: every published rule is one the validator enforces, and every rule the validator enforces is published. The drift test must fail when either side moves alone.

A takeover-capable command's receipt artifact must be byte-stable for a fixed outcome, must be self-describing, and must be the exact bytes whose sha256 a host cites in an evidence entry. Two runs of the same fixed outcome on different hosts must produce the same artifact bytes, and the digest a host records must match the bytes on disk rather than a captured stream.

The admission receipt must fail closed on the same discipline the upgrade receipts use: an unknown field, an unknown receipt kind, a target identity that does not match the recomputed manifest, activation set, or managed block, and a referenced historical transaction whose digest does not match must each fail with an actionable message. An admission that names a historical transaction must never be accepted as evidence that an upgrade ran here.

Negative cases must keep failing: an unordered or duplicated evidence entry, an activation evidence entry before the apply receipt, a pending evidence entry after activation evidence, a successor-owned evidence entry before activation evidence, a manual-transfer-required payload carrying a non-null custody value, a manual-transfer-pending payload carrying no active task, and a blocked state with more than one blocked stage or with a reason code whose action code does not pair.

A manual-transfer payload must be validated on shape, freshness, and evidence references, and no code path may read goal text from disk.

## Follow-ups out of scope

- Version and profile bumps, which belong to the release work item.
- Any rewrite, migration, or reinterpretation of historical upgrade receipts.
- Any change to the repo-pinned offline trust model or to how a pinned installation resolves its source.
- Any change to custody's privacy rules beyond defining the transfer payload's shape and validation.
- Any relaxation of the closed takeover contract beyond publishing it and binding it to the validator with a drift test.