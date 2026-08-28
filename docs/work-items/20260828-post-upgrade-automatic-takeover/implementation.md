# Implementation: Post-upgrade automatic takeover

## Governing boundary

- Work item: `20260828-post-upgrade-automatic-takeover` (L)
- Gate: `implementation-ready`
- Governing decision: Accepted ADR 0009; inherited Accepted ADRs 0005, 0007 and 0008
- Writer: one RD implementation writer for shared code and managed artifacts
- Version target: unpublished Vibe Kit `0.6.0`
- Preserved boundary: no publication, network access, host API implementation, or multi-file transaction/rollback changes

## Implementation plan

1. Extend the additive CLI result-schema-1 surface with structured doctor
   diagnostics and `verify --format json`, preserving existing text behavior and
   exit meanings.
2. Bind source/apply/doctor evidence to payload-tree, manifest and actual
   activation-set identity without letting the CLI derive activation or ready.
3. Advance the human/machine Agent-install contract to schema/protocol 2 with
   maintenance bridge 1, takeover schema 1, closed lifecycle/enums, goal custody,
   privacy and current manual-fallback-only capabilities.
4. Synchronize managed workflows, Agent metadata, Plugin bootstrap/maintenance,
   release packaging/validation, documentation and the 0.6.0 unpublished identity.
5. Add scenario and regression coverage, run focused/full checks, then perform a
   controlled source-checkout self-upgrade only after a safe read-only plan.

## Implemented behavior

### CLI and installed identity

- `AGENT_INSTALL.md` and `agent-install.json` are framework-managed installed
  files. They participate in collision preflight, upgrade preservation rules,
  manifest `managed_files`, runtime discovery and activation-critical identity;
  missing, malformed or hash-drifted copies make doctor blocking.
- Activation algorithm v2 canonicalizes `agent-install.json` with only its
  activation digest replaced by 64 zeroes, avoiding a self-hash cycle. Release
  validation recomputes the same identity through a separate entries-based
  implementation and fails closed on path, algorithm or digest drift.
- Source provenance additively includes the canonical payload-tree SHA-256.
- Installation manifests remain schema 1 and add the target protocol fingerprint,
  exact activation paths/hashes, runtime discovery roots and target activation-set
  SHA-256.
- Init/adopt/upgrade JSON receipts add the target fingerprint and explicitly
  report activation as `not-proven`; they claim neither reload, automatic handoff
  nor ready.
- JSON doctor keeps `warnings`/`errors`, adds one authoritative closed diagnostic
  for every warning/error, reports the raw manifest SHA-256, compares actual and
  target activation identities, and classifies stale runtime/non-runtime paths.
- JSON verify emits the ordered lint/typecheck/test/build matrix, canonical default
  versus partial selection, configured/applicability/required fields, outcomes,
  exit/reason/provenance, and separately bounded/redacted stdout/stderr tails.
  Default mode continues independent checks after failures; process-start failure
  is a blocking skip. No network-attestation field is emitted.

### Agent and host contract

- The executable takeover contract is a compiled, closed registry whose canonical
  digest is repeated in `agent-install.json`, core protocol metadata and release
  metadata. Installed validation authenticates the manifest, raw managed Agent
  contracts, core protocol, registry and activation identity before reading a
  candidate result.
- `validate-takeover --format json` validates the exact schema-1 result shape,
  stage dependencies, outcomes, reason/action pairs, evidence placement and
  ordering, activation receipts, custody transitions and ready invariants. It is
  structural-only, never authenticates host evidence, never claims ready, rejects
  duplicate JSON keys and returns only privacy-safe error code/path pairs.
- Agent-install schema/protocol 2 declares takeover schema 1, maintenance bridge
  schema 1, stage/state/reason/action/evidence/adaptation/routing/goal enums,
  activation paths/receipts, diagnostic and verify registries, privacy and
  fail-closed evolution.
- The human contract defines one exact-version confirmation, target-CLI
  pre-execution bridge, content-bound activation, single-owner goal custody,
  adaptation → final verification → target-rule re-evaluation order, and
  stage-specific completion/recovery language.
- Same-task reload and automatic successor handoff remain conditional/unclaimed.
  The repository and Plugin declare only the one-action manual new-task fallback
  unless a running host independently supplies conforming live evidence.
- Managed AGENTS/core/Skills and RD/QA metadata prevent adaptation, resumed shared
  edits or ready language before positive activation and target-version
  re-evaluation.

### Distribution and documentation

- Core/Codex protocols advance to 4; Agent-install schema/protocol advance to 2;
  takeover and maintenance bridge are schema 1; CLI result/manifest/onboarding
  schemas and feedback protocol remain unchanged.
- Packaging records payload-tree and activation-set identities plus all schema
  versions. Release validation rejects bridge, lifecycle, capability, activation,
  diagnostic, verify, Plugin and cross-channel drift. It also executes one
  canonical valid takeover case and bounded invalid dependency, action,
  activation, custody and false-ready cases through the production validator.
- The Plugin wrapper recomputes bundled payload identity before target-CLI
  execution and exposes no MCP, hook, app, reload or task-creation capability.
- README, Chinese README, changelog, 0.6.0 candidate notes and durable product/
  architecture context distinguish published 0.5.0 from unpublished 0.6.0.

### Authenticated predecessor compatibility repair

- The target CLI compiles the Accepted exact v0.5.0 registry, independently
  recomputes its canonical digest, and requires exact closed mirrors in the
  Agent-install bridge, core protocol and release manifest. Editable predecessor
  or package metadata cannot authorize or weaken the migration.
- Eligibility is limited to the official complete two-contract set plus the
  normalized official v0.5.0 installation identity. The predecessor manifest's
  `source` field is deliberately not read as an eligibility input; target-channel
  provenance and payload identity remain independently required.
- Every predecessor identity path is authenticated through component-wise
  `lstat`, regular-file raw hashing and before/after metadata checks. Missing,
  modified, mixed, wrong-type, symlinked, broken-symlinked, malformed or unhealthy
  sets fail closed for both contract paths.
- Read-only plans expose the exact paired `update` entries and additive
  `compatibility_migrations` evidence. Apply independently repeats target and
  predecessor authentication, then reauthenticates each member before replacement.
  Pre-mutation drift produces paired conflict evidence; drift after mutation starts
  retains the existing `unknown-partial` boundary.
- Success records only target 0.6.0 hashes and activation identity. No predecessor
  hash, source value or migration history is persisted in project-owned state.
- Executable conformance uses an intact fixture archived from the local immutable
  `v0.5.0` tag and covers source exclusion, all declared negative path/install
  states, target-channel parity, mirror mutations and both race phases.

## Verification evidence

- Pre-repair full baseline: `python3 -m unittest discover -s tests -v` — 40/40
  passed before compatibility edits.
- Focused authenticated-predecessor coverage passed the intact official checkout,
  source exclusion, complete-set/install negatives, component symlinks, both race
  phases, exact mirrors, release mutations and independent registry recomputation.
  A first mirror run exposed Python boolean/integer equality; exact typed/closed
  validation was added and the failed cases passed on rerun.
- Final source suite: `python3 -m unittest discover -s tests -v` — 45/45 passed
  in 184.631 seconds. Installed root default `verify --format json` independently
  passed the same 45 tests in 56.584 seconds; lint, typecheck and build were
  explicitly unconfigured, with no failed or skipped configured check.
- Two unpublished packages at
  `/private/tmp/vibe-kit-0.6-authpred-a.tacn7X` and
  `/private/tmp/vibe-kit-0.6-authpred-b.ZOdDXa` were byte-identical throughout.
  Nested and explicit `validate-release --format json` returned `valid`, 35
  payload files and `network_used=false`. Final payload tree is
  `f71275ecd44d841cc89d043292e6b565cf4aa16d721fdd8f7c9157b13b35b835`;
  activation set is
  `35f16a0c6393560794372737dc6a32b1d24a902e0f70d40989d9ce4e04d8a37c`.
  Direct/Plugin/distribution ZIP SHA-256 values are respectively
  `67b8a69639fff4c2df5ed49c99eb9b1b5ef57c57a71418941cd50a72128ad530`,
  `a362283b4f617f534b27129caec3ba2c4362ad452306dcfe576a6ab2e3b0d3b1`
  and `f79b6a0090eab898e5e46d4ce8d83d08cf86516b8375409b7f67c8bc42fb6ad2`.
- Controlled root self-upgrade plan was safe/read-only with 27 `no-op` entries
  and only manifest metadata scheduled. Apply rewrote zero managed payload files;
  installed doctor was healthy with manifest SHA-256
  `865048c76782083f5a75cc47b800095c9ad7190c9fa608a02adc5fb636b41a6e`
  and exact activation match.
- Preserved official-source acceptance target
  `/private/tmp/vibe-kit-0.6-real-upgrade.HWPfdr/project`: clean 0.5.0 state,
  read-only safe plan with the exact paired updates/evidence, successful apply and
  healthy target doctor. Project-owned hashes were unchanged and activation was
  correctly `not-proven`/manual fallback. Its default verification truthfully
  failed four old project-owned v0.5 tests because the upgrade preserved their
  incompatible v0.5 Plugin/test source; no framework code or project-owned file
  was changed to conceal that result.
- Current-project acceptance target
  `/private/tmp/vibe-kit-0.6-current-project-upgrade.WjTQ15/project`: committed
  clean baseline `041a0f0` retained all 23 official v0.5 managed paths, the old
  managed AGENTS block, official two-contract bytes and installation state while
  overlaying 100 current project/application-owned files. Their canonical digest
  was `8136fa4f02166a3cb759f7f3b5b5f264349ae2392f5590f07cad225a013e96b1`
  before and after upgrade with zero mismatches. Old doctor, safe/read-only plan,
  apply and target doctor all passed; after adding the exact local immutable
  `v0.5.0` tag to fixture Git metadata, target default verify passed 45/45 in
  52.476 seconds. Worktree diff contained framework/tool-owned paths only.
- Actual Python 3.9 was not available locally; the final source was parsed against
  Python 3.9 grammar and executed under dependency-free Python 3.14. This is
  recorded as skipped release evidence, not promoted to a release claim.
- After the evidence-only documentation update, final `git diff --check`, Python
  3.9 grammar/JSON parsing, doctor, deterministic packaging and release validation
  passed; a final root default verify passed 45/45 in 55.850 seconds.

## Known limitations

- Controlled fixtures prove the repository contract only. They do not establish
  live Codex same-task reload or automatic task creation.
- The portable healthy path still requires one user action: create a new task in
  the same project. The new task can continue a prefilled/copyable goal without a
  second upgrade confirmation.
- Existing whole-upgrade mutation and `unknown-partial` recovery semantics are
  unchanged; transaction/rollback work remains separate.
- A framework upgrade intentionally preserves project/application-owned release
  and test sources even when their old verification suite is incompatible with
  the installed framework. Adaptation of such source is separate project work,
  never an implicit ownership expansion.
- Independent QA must re-run acceptance after this compatibility repair. The RD
  handoff does not declare product acceptance; QA-owned findings and evidence
  remain in `verification.md`.
