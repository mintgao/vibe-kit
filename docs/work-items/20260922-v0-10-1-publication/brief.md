# Publish Vibe Kit v0.10.1

- ID: `20260922-v0-10-1-publication`
- Size: `L`
- Status: shaping
- Created: 2026-09-22

## Technical decision readiness

- Outcome: `decision-required`
- Trigger evidence: an L-sized public release moves the external version boundary, the compatibility surface that existing installs upgrade through, and the version-specific publication contract that fixes the tag, Release, asset set and operation allowlist; the repository records such a choice once per release, and the current Accepted decisions fix only v0.10.0
- Decision owner: none
- Governing decision: none
- No-new-decision rationale: none
- Review mode: `not-required`
- Review result: `not-required`
- Review evidence: none
- Material product decisions: resolved by the product owner on 2026-09-22: (a) the host-label raise ships as the patch release `0.10.1` rather than being folded into a later iteration; (b) the release contains no product change beyond the label raise and the version identity; (c) no public GitHub operation happens in this work item until one later authorization bound to the exact frozen publication intent digest
- Open blockers: the governing decision `docs/decisions/0021-v0-10-1-publication.md` is not authored or Accepted yet
- Gate: `blocked`
- Gate owner: Workflow orchestrator, Hermes session 2026-09-22
- Confirmed at: none
- Confirmation basis: none
- Readiness history: `2026-09-22 — the trigger scan found the version/compatibility and publication-contract triggers; the record starts decision-required + blocked with no application or shared implementation code edited`

## Goal

Ship the completed host-conformance record as Vibe Kit `0.10.1`: one exact,
non-draft GitHub Pre-release whose five public assets can be downloaded and
validated offline, publishing the Hermes host-registry label `verified` — with
no weakening of the historical v0.7 through v0.10.0 publication guarantees and
no product change beyond the label raise and the version identity.

## Context

- The host-label raise landed on `main` at `3828071` with its verification
  record at `dc88d3f`: the registry reads `verified` with the five-stage
  conformance record as its evidence, the lane passes 118 tests on CPython 3.13
  and 3.9, `doctor` is healthy, `package` and `validate-release` pass, and the
  independent QA packet passed the frozen candidate.
- The published `v0.10.0` release (annotated tag `v0.10.0`, source commit
  `9628513`) is immutable — verified after publication and not to be rewritten.
  The label can therefore only reach published artifacts through a new version
  boundary, which is why this work item exists; the product owner chose a patch
  release over folding the change into a later iteration.
- The source still carries kit version `0.10.0` (`.vibe/core/version`,
  `.vibe/version`), the maintenance bridge still bounds installs at
  `maximum_installed_kit_version_exclusive` `0.10.0`, and two upgrade paths plus
  the predecessor-migration target guard compare the target's framework version
  literally against `0.10.0`.
- The schema-4 `vibe-kit-v0.10.0-prerelease` profile and the schema-3 #8–#13
  closeout are closed and keep exact semantics. The closeout has no subject
  here: this release closes no issue — #14 and #15 stay tracked defects.
- ADR 0020 fixed the six-operation, five-asset publication model this release
  reuses; the `vibe-release` Skill, `tests/test_v010_publication.py`,
  `tests/test_release_identity.py` and the guide's version drift check encode
  the current boundary.
- The Codex five-stage refresh remains a tracked follow-up (its runbook and
  host-neutral driver are delivered); this release publishes the Hermes label
  only.

## Scope

- In:
  - Version identity `0.10.1` across `.vibe/core/version`, `.vibe/version`,
    `agent-install.json#kit_version`, the installed contract, the Plugin
    metadata, the maintenance bridge's `maximum_installed_kit_version_exclusive`
    (`0.10.0` → `0.10.1`), the predecessor-migration registry's target version
    and its compiled-digest mirrors, and every generated identity, in one change.
  - A closed `vibe-kit-v0.10.1-prerelease` profile (schema `5`) fixing the
    version, annotated tag, title, release body, exactly five assets, the
    retargeted predecessor smokes plus `public-upgrade-v0.10.0-to-0.10.1`, the
    six-operation allowlist and issue policy `none` — with the historical
    profiles keeping byte-exact semantics and their tests.
  - The upgrade-path audit: the two version-literal branches and the
    predecessor-migration target guard must admit the new target so a healthy
    `0.10.0` install, and the older bridgeable installs, upgrade into the
    candidate.
  - `CHANGELOG.md` and `docs/releases/0.10.1.md` describing the label raise
    honestly; both homepages reviewed for version, links, installation commands,
    capabilities and limitations, with reasons recorded for unchanged sections.
  - Release gates on the frozen candidate: default lane on CPython 3.13 and 3.9,
    `doctor`, `validate-readiness`, `package`, `validate-release`, and two
    independent clean builds.
- Out:
  - Any GitHub write without a later explicit authorization bound to the exact
    publication intent digest: no push, tag, Release or asset upload.
  - Fixing issues #14 or #15 — tracked defects, not part of this release.
  - Stable promotion, draft Releases, Plugin Directory publication, signing,
    provenance or platform-immutability promises.
  - Force push, tag movement, Release rewrite or asset replacement.
  - Any product change beyond the label raise and the version identity.

## Acceptance criteria

- [ ] AC-1: The source advances to kit version `0.10.1` coherently — every
  identity mirror, the maintenance-bridge bound, the migration registry target
  and its compiled digests — with every mirror regenerated in the same change,
  `doctor` healthy and the recorded identity equal to a fresh recomputation.
- [ ] AC-2: `CHANGELOG.md` and `docs/releases/0.10.1.md` describe exactly the
  label raise without unearned claims; both homepages are reviewed and
  synchronized for version, links, installation commands, capabilities and
  limitations, with a reasoned record for unchanged sections.
- [ ] AC-3: A closed schema-5 `vibe-kit-v0.10.1-prerelease` profile fixes
  version, tag, title, body path, exactly five assets, the smoke set and issue
  policy `none`; the historical profiles keep exact semantics, a v0.10.1
  candidate cannot pass them, and the profile is pinned by tests.
- [ ] AC-4: A healthy install recorded at `0.10.0` upgrades into the candidate
  through the maintenance bridge with its files, recorded selection and identity
  preserved; the predecessor-migration path still admits its eligible
  predecessors; a fresh install of the candidate is doctor-healthy for a
  `codex`, a `hermes` and a combined selection, and the installed contract's
  Hermes label reads `verified`.
- [ ] AC-5: On the frozen candidate, the default lane passes on CPython 3.13 and
  3.9, `doctor` is healthy, `validate-readiness` is valid, `package` and
  `validate-release` pass, and two independent clean builds from the same commit
  produce byte-identical five-asset sets.
- [ ] AC-6: No GitHub write happens in this work item, and "v0.10.1 published
  and verified" is claimable only from `confirmed-complete` remote state plus
  passed public verification under a separate authorization bound to the frozen
  intent digest.

## Design and technical notes

- The decision record (to be authored as
  `docs/decisions/0021-v0-10-1-publication.md`) fixes: the exact schema-5
  profile contents and smoke set; how the two version-literal upgrade branches
  and the migration target guard admit `0.10.1` without changing behaviour for
  older installs; whether the publication intent/receipt schema moves to `5`
  while the closeout schema stays `3`; and what the release notes may claim
  about the label — a published `verified` label backed by the completed
  five-stage record.
- Keep the version bump and the mirror regeneration in one change; the release
  tests own the proof.
- The publication contract stays host-owned and offline: the CLI plans,
  validates and receipts; the Agent/host performs any remote operation under an
  explicit authorization.

## Risks and open decisions

- The new profile cascades into the shared publication helpers (authorization
  field set, exact asset-name closure, operation natural-key grammar, intent
  schema dispatch) and into the release tests; the historical profiles must keep
  byte-exact semantics while the new one is added.
- Advancing the bridge bound and the migration target is what lets `0.10.0` and
  older installs upgrade; getting it wrong strands installs, so AC-4's upgrade
  fixture must cover both a `0.10.0` and a pre-`0.10.0` recorded install.
- Homepage and guide version literals are prose bound partly by a drift check;
  each must move or keep exact semantics with the reason recorded.
- The final remote write request must bind one frozen intent digest; the current
  product-owner instruction is not an executable authorization for an intent
  that does not yet exist.