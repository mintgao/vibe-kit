# V0 8 Publication

- ID: `20260902-v0-8-publication`
- Size: `L`
- Status: implementation-ready
- Created: 2026-09-02

## Technical decision readiness

- Outcome: `decision-accepted`
- Trigger evidence: L-sized public release changes an external version/compatibility boundary, Git/GitHub trust boundary, remote-write recovery, and the version-specific publication contract.
- Decision owner: read-only Tech Lead author `/root/v08_release_tl_author`
- Governing decision: Accepted ADRs 0004, 0011, 0012, and 0013
- Review mode: `independent-agent`
- Review result: `approved`
- Review evidence: Distinct read-only Tech Lead `/root/v08_release_tl_review`
  required two correction rounds covering closed remote snapshots, per-object
  attempt ledgers, two-phase evidence, exact gate schemas, clean-source
  causality, v0.7 closeout compatibility, checksum closure, and evidence-push
  exclusion, then approved the exact persisted ADR 0013 on 2026-09-02.
- Material product decisions: User requested publication on 2026-09-02; scope is v0.8.0 non-draft GitHub Pre-release with exactly five assets and public verification, excluding Issue closeout and Stable promotion.
- Open blockers: none for implementation. Final release QA, clean accepted
  commit, Python 3.9 evidence, deterministic dual builds, remote snapshot,
  offline intent, and exact remote-write authorization remain runtime release
  gates rather than technical-decision blockers.
- Gate: `implementation-ready`
- Gate owner: Workflow orchestrator
- Confirmed at: `2026-09-02T06:57:32Z`
- Confirmation basis: The Workflow orchestrator confirmed that the exact
  persisted Accepted ADR 0013 resolves every applicable schema, compatibility,
  trust, recovery, causality, and publication boundary; product scope is fixed
  by AC-1 through AC-12; the distinct reviewer approved; no implementation
  blocker remains.
- Readiness history: `2026-09-02 — request classified L; PM shaped the exact
  v0.8.0 Pre-release and no-Issue scope. A read-only Tech Lead authored ADR
  0013. A distinct reviewer required two correction rounds covering remote
  closure, retry proof, evidence causality, exact child schemas, pre/post-publication
  acceptance separation, and historical v0.7 CLI compatibility. The exact
  persisted amendment was approved; ADR 0013 was accepted; the Workflow
  orchestrator confirmed implementation-ready before release-tooling edits.`

## Goal

Publish the independently verified Vibe Kit `0.8.0` candidate as an exact,
non-draft GitHub Pre-release whose five public assets can be downloaded and
validated without weakening historical v0.7 publication guarantees.

## Context

- Repository: `mintgao/vibe-kit`; `v0.7.0` is the latest public Pre-release.
- The completed `20260902-token-efficient-adaptive-workflow` work item provides
  the unpublished v0.8.0/core protocol 6 product candidate and independent QA.
- ADR 0011, the release Skill, and the current publication CLI intentionally
  encode the exact v0.7.0 publication and Issue #1–#5 closeout contract. They
  cannot be used for v0.8.0 until a reviewed version boundary is implemented.
- The user's request authorizes shaping, local implementation, and offline
  release preparation. GitHub writes require one later authorization bound to
  the exact publication intent digest and frozen candidate.

## Scope

- In:
  - Repository `mintgao/vibe-kit`, version/tag `0.8.0` / annotated `v0.8.0`.
  - Fast-forward-only `main` update under expected-old-OID CAS.
  - One GitHub Release with `draft=false`, `prerelease=true`.
  - Exactly `SHA256SUMS`, `release-manifest.json`,
    `vibe-kit-0.8.0.zip`, `vibe-kit-distribution-0.8.0.zip`, and
    `vibe-kit-plugin-0.8.0.zip`.
  - Frozen source commit, annotated-tag identity, Release title/body bytes,
    five-asset names/sizes/SHA-256, remote snapshot, operation set, public
    read-back/downloads, nested validation, and installation/upgrade smokes.
  - Preserve the exact historical v0.7 publication and closeout contract.
- Out:
  - Stable or draft promotion, Plugin Directory publication, signing,
    provenance, automatic update, CLI network access, or platform-immutability
    promises.
  - Any Issue read/write, comment, close, reopen, or closeout intent.
  - Force push, tag move, Release rewrite, asset replacement/deletion, or
    automatic destructive rollback.

## Acceptance criteria

- [ ] AC-1: The final candidate is a clean accepted full-length commit at
  Vibe Kit 0.8.0/core-Codex protocol 6 and receives fresh independent release
  QA, all configured checks, and release-specific gates after publication
  tooling changes.
- [ ] AC-2: The exact final candidate passes applicable package,
  `validate-release`, publication plan/receipt validation, and scenarios under
  actual Python 3.9; the CLI remains standard-library-only, offline, and free of
  credentials.
- [ ] AC-3: Two independent clean builds from the same accepted commit produce
  byte-identical five-asset sets with identical names, sizes, and SHA-256, and
  both pass release validation.
- [ ] AC-4: The public Release asset list is exactly the five scoped names with
  one role each; missing, extra, duplicate, or divergent bytes block. Public
  assets match the intent and the distribution's nested checksum graph.
- [ ] AC-5: An offline v0.8 publication plan binds repository, version, commit,
  main CAS preimage/target, annotated tag identity, Release body/title/state,
  five assets, remote snapshot, operations, and non-destructive recovery into a
  stable intent digest; any bound-field change invalidates authorization.
- [ ] AC-6: A closed allowlisted receipt validates offline, while completion
  still requires authenticated live read-back, public downloads, and smoke
  evidence rather than structural validity alone.
- [ ] AC-7: Main uses expected-old-OID fast-forward CAS only. Existing
  tag/Release/assets are reused only on exact match; force, move, rewrite,
  delete, replace, extra, duplicate, or divergent state blocks safely.
- [ ] AC-8: Every definite or uncertain write response is read back; only a
  positively absent natural-key object may receive one bounded retry. Permission
  denial, divergence, or still-unknown state stops writes with one next action.
- [ ] AC-9: Canonical public downloads verify all five SHA-256 values, the
  distribution graph, `validate-release`, fresh direct init/doctor, Plugin
  smoke, historical critical upgrades, and healthy v0.7-to-v0.8 upgrade.
- [ ] AC-10: Historical v0.7 tag/notes/evidence/assets/markers/Skill,
  plan/receipt/closeout validators, and tests retain exact semantics; v0.8 input
  cannot pass the v0.7 profile.
- [ ] AC-11: The v0.8 executable operation set contains no Issue action, creates
  no closeout intent or authorization, and leaves every Issue unchanged.
- [ ] AC-12: Only `confirmed-complete` remote writes, `passed` public
  verification, all smokes, and a valid receipt permit the claim "v0.8.0
  published and verified". Platform immutability is reported only from live
  metadata as true, false, or unknown.

## Design and technical notes

- ADR 0004 governs deterministic offline packages. ADR 0011 governs the
  exact-source, five-asset, host-owned remote, authorization, read-back, and
  recovery model for v0.7. ADR 0012 governs the unpublished v0.8 candidate and
  historical v0.7 isolation.
- The v0.8 publication profile and no-Issue-closeout boundary require a new or
  amended Accepted decision before implementation.

## Risks and open decisions

- Extending a v0.7-specific validator could accidentally weaken its historical
  exactness or accept ambiguous cross-version receipts.
- The existing publication intent schema requires an Issue closeout policy;
  Tech Lead must decide whether v0.8 can express a closed no-closeout value
  without schema change or needs a new schema/profile.
- Partial or uncertain remote state cannot be rolled back destructively; exact
  read-back and same-intent resume are mandatory.
- The final remote write request must bind one frozen intent digest. The current
  user request is not an executable authorization for an intent that does not
  yet exist.
