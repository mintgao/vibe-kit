# Technical review: host label raise (sequential-perspective pass)

Review target: `docs/work-items/20260922-host-label-raise/brief.md` (the persisted
design), against the governing decision `docs/decisions/0019-host-adapters.md`
and the current contract state.

Capability limitation: identity-isolated independent reviewer unavailable — this
pass ran sequentially on the same host and in the same session that shaped the
brief; it is a distinct read-only review phase with its own findings, not an
independent-agent review, and it must not be described as one.

## What was checked

- Coverage: ADR 0019 defines both labels, the evidence rule ("labels change only
  with recorded evidence, never by assertion") and the raise condition (a
  complete five-stage record whose evidence grade matches). The record at
  `docs/work-items/20260921-host-adapters/conformance.md` now carries all five
  stages with command results and digests; the precondition is satisfied and no
  new durable choice remains for this change.
- Boundary: the change edits one label value, one evidence list and the copies
  that state them. No schema, protocol, shape, behavior, migration, recovery or
  security change; the closed-shape validator keeps pinning the structure; the
  fail-closed rules for unknown hosts and incoherent selections are untouched
  and stay covered by existing tests.
- Touchpoint inventory: `bin/vibe` registry; `agent-install.json` mirror;
  `AGENT_INSTALL.md` table row (the general rule sentence stays); `README.md`
  (two statements); `docs/context/product.md`; the conformance record's closing
  wording; the two test pins plus the new regression assertions. Historical
  records (`docs/releases/0.10.0.md`, ADRs 0019 and 0020, the CHANGELOG 0.10.0
  entry, closed work items) are deliberately left as point-in-time records.
- Failure modes: a partially updated copy set fails the mirror-coherence check
  and the packaging tests (fail closed, not silent); the identity regeneration
  is mechanical and proven by `package` plus `validate-release`; a stale
  evidence reference cannot mislead silently because the reference is a
  committed repository path.

## Findings

1. Approved scope and boundary; no hidden durable decision found.
2. Note (non-blocking): keep the evidence reference a repository-relative path
   that stays reachable at release time; the conformance record is committed, so
   any later reorganization must migrate the reference deliberately rather than
   leaving a dangling citation.
3. Note (non-blocking): after the raise, no registered host carries
   `supported-unverified`; the fail-closed coverage therefore rests on the
   unknown-host and incoherent-selection tests, which exist and must keep
   passing — the brief's AC-2 and AC-4 already pin this.
4. Note (non-blocking): the Codex-side refresh is a handoff; the record must
   state what ran where, and the Hermes raise must not be presented as depending
   on it (the brief's AC-5 records this).

## Review pass — approved

Sequential-perspective review completed on 2026-09-22; verdict `approved` with
three non-blocking notes carried into implementation. Capability limitation:
identity-isolated independent reviewer unavailable.
