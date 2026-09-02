# V0.8 publication implementation

## Boundary

Implemented Accepted ADR 0013 inside the release CLI, package/validation tests,
release Skill, protocol/version mirrors, release notes and work-item evidence.
No GitHub operation, tag, commit, authorization, publication intent or live
receipt was produced.

## Implementation

- Added a closed schema/profile dispatcher that preserves historical v0.7
  schema 1 and accepts only the exact `vibe-kit-v0.8.0-prerelease` schema 2.
- Added exact five-asset/no-Issue intent validation, complete paginated remote
  snapshots, canonical snapshot and operation precondition digests, six parent
  operations and five child asset operations.
- Added closed prepublication QA, configured-check, CPython 3.9, clean build A/B,
  and release-gate bundle validation with complete child digest preimages.
- Added schema-2 authorization binding and closed main/tag/Release/asset attempt
  ledgers, kind-specific bounded retry proof, public downloads/smokes and offline
  final validation. Plan and validation envelopes report actual interpreter
  identity and still report host evidence as unauthenticated.
- Pinned the current CLI's unchanged v0.7 closeout request to the published
  parent intent digest without changing its command invocation or request shape.
- Preserved the exact non-self-referential checksum/distribution graph and
  advanced publication schema mirrors to 2.

## Focused verification

RD ran publication/profile unit scenarios and syntax compilation only. Independent
QA owns the canonical complete default verification and release-specific final
gates for the frozen clean candidate.

## Runtime gates still pending

Fresh independent release QA, a clean accepted commit, actual Python 3.9
execution, two clean byte-identical builds, a closed remote snapshot, exact
publication intent, adjacent executable authorization, GitHub operations, public
downloads/smokes and postpublication acceptance are intentionally not fabricated.
