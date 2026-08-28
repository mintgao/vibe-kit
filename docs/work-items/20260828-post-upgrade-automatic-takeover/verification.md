# Verification: Post-upgrade automatic takeover

- QA date: 2026-08-28
- Product verdict: **Ready for the unpublished 0.6.0 candidate**
- Publication verdict: **Not ready for a v0.6.0 GitHub Release**
- Scope: Accepted amended ADR 0009, all AC-1 through AC-14, the authenticated
  v0.5.0 predecessor migration, installed takeover contracts, controlled host
  conformance, one live manual-new-task continuation and local release artifacts
- Evidence boundary: CLI filesystem/process receipts, controlled host fixtures and
  positive live manual-task evidence are identified separately. Nothing here is
  evidence of Codex same-task reload or automatic successor creation.

## Acceptance evidence

| Criterion | Independent evidence | Result |
|---|---|---|
| AC-1 — Single confirmation | Installed guide, managed rules and Plugin maintenance Skill require one exact project/version decision, then read-only plan and apply without a second conversational confirmation. Fresh exact `0.5.0 -> 0.6.0` runs retained target and trusted-source identity through plan/apply. The live manual successor resumed an already confirmed upgrade rather than asking the user to confirm it again. | Pass |
| AC-2 — Read-only plan | Fresh official-v0.5.0 and real-current-project targets were snapshotted before/after target-CLI plan; both plans exited 0/`safe`, reported `files_changed=false`, and left every byte and Git state unchanged. Blocked pair, collision and mirror-drift plans also performed no project writes. | Pass |
| AC-3 — Safe ownership | Both positive applies succeeded with `write_state=project-files-written`. Official-tag project-owned files and the real-current-project application/project digest were byte-identical after apply and verification. Missing/modified/mixed predecessors, wrong version/identity, unhealthy managed state, symlink/type cases and unrelated collisions failed closed. Existing managed-conflict and `unknown-partial` meanings remain intact. | Pass |
| AC-4 — Honest stages | Positive apply receipts reported only `activation.state=not-proven`, `path=none`, manual fallback true and both reload/automatic claims false. Installed doctor proved exact version, manifest and activation health but did not claim activation or ready. | Pass |
| AC-5 — Same-task activation | A controlled host invoked the installed production validator. Same-task ready passed only with a target-bound `host-reload` receipt, equal source/active task, correct post-apply ordering and exact manifest/activation identity; wrong-task, early, missing or mutated receipts failed. This proves contract behavior only; current Codex reload is not claimed. | Pass |
| AC-6 — Automatic handoff | The controlled automatic-successor path required distinct task identity, stable idempotency key, activation plus handoff evidence, valid custody transitions and terminal successor ownership. Same-key creation returned one successor/one create attempt; an ambiguous attempt created and claimed none. Ownership/custody mutations failed. Current Codex automatic handoff is not claimed. | Pass |
| AC-7 — Portable degradation | Installed capability is `manual-fallback-only`. The valid degraded result ends at upgraded, uses `manual-new-task-required` plus exactly `create-new-project-task`, has no completion owner and cannot say ready. The live flow crossed precisely this documented one-action manual boundary. | Pass |
| AC-8 — Evidence-backed adaptation | Controlled unchanged/refreshed outcomes passed only after activation; invalid, contradicted and incomplete adaptation used their closed reason/action pairs and blocked later stages. Source-task adaptation evidence after transfer failed. Both real upgrades preserved onboarding/context bytes. The live successor independently read the installed 0.6 rules/context before continuing. | Pass |
| AC-9 — New-rule re-evaluation | Controlled maintenance-only, routable unfinished, target-rule blocker and material-decision results enforce verification/order, active-task ownership and closed outcomes. Managed Skills prohibit further application/shared edits before activation/re-evaluation. The live successor read target rules before its authorized release-note edit. | Pass |
| AC-10 — Closed verification | Root doctor is healthy 0.6.0 with zero diagnostics and activation match. Independent full tests passed 45/45. Default verify passed its required 45-test command; lint, typecheck and build were explicitly unconfigured, with zero failed/skipped configured checks. Controlled failed/skipped/error verification prevented ready. | Pass |
| AC-11 — Truthful success | Controlled same-task, automatic-successor and manual-successor ready results passed only with all dependencies, exact identities, valid receipt, single completion owner, final doctor/verify and custody. False-ready, duplicate-owner, no-write, identity and partial-verification mutations failed. Validator output remains structural-only and does not authenticate host evidence or itself assert ready. | Pass |
| AC-12 — Truthful incomplete states | Source/plan/conflict/`unknown-partial` CLI regressions passed. Controlled manual limitation, invalid/contradicted adaptation, failed/skipped/error verification, target-rule blocker and material-decision results used exact last-stage/write-state/reason/action semantics; mismatched pairs and dependencies failed with bounded code/path-only errors. | Pass |
| AC-13 — Scenario coverage | The repaired suite's fake host actually shells out to the installed `bin/vibe validate-takeover` for maintenance-only, same-task, automatic successor/idempotency, manual successor, adaptation, verification, target-rule, privacy, mutation and single-owner scenarios. Fresh intact official-v0.5.0 and real-current-project migrations, the full negative matrix and one positive live manual-new-task continuation all passed. The prior fixture gap is closed. | Pass |
| AC-14 — Cross-channel identity | Two fresh release directories were identical; both validated. Direct ZIP, Plugin payload and marketplace payload contained the same 35 payload paths with byte equality. Payload `7c152ac7...`, activation `35f16a0c...` and the exact predecessor mirror matched release/Plugin/installed channels. Drift tests reject archive, lifecycle, protocol, registry, mirror, activation and Plugin identity changes. | Pass |

## Prior findings re-test

| Prior finding | Current independent evidence | Disposition |
|---|---|---|
| F-1 — Installed contracts missing | Both real upgrade paths installed `AGENT_INSTALL.md` and `agent-install.json` as managed, activation-critical runtime roots. Installed doctor detects deletion/tamper as broken. | Closed |
| F-2 — Machine contract could not validate takeover | Installed `validate-takeover --format json` accepts valid structural objects, rejects invalid objects, authenticates installed contract/version/managed/activation/registry identity first, and fails closed on a weakened or tampered on-disk contract. Errors are bounded and value/goal-safe. | Closed |
| F-3 — Scenarios were static strings | `tests/fake_takeover_host.py` builds task/custody/evidence state and invokes the installed production validator subprocess for every positive and negative scenario. Focused and full behavioral tests pass. | Closed |
| F-4 — Work item absent from index | `docs/work-items/index.md` contains the post-upgrade work item and preserves the unrelated atomic-upgrade entry. | Closed |

## Fresh official v0.5.0 predecessor acceptance

An independent target was extracted directly from the immutable `v0.5.0` Git
tag, retaining both official predecessor contracts as regular, unmanaged files.

- The old installed doctor exited 0 and reported healthy `0.5.0`.
- The target 0.6 CLI plan exited 0/`safe`, with counts `no-op=11` and
  `update=17`. A full before/after snapshot was identical.
- `AGENT_INSTALL.md` and `agent-install.json` were paired `update` entries with
  the exact note `authenticated predecessor migration
  v0.5.0-unmanaged-agent-contracts-v1; complete set`.
- Additive migration evidence was `phase=planned` and carried registry
  `6cbee96e...`, predecessor-install identity `70dd0eac...` and contract-set
  `5ae7da78...`.
- Apply exited 0/`success`, reported `project-files-written`, changed the migration
  evidence to `phase=applied`, and retained `activation=not-proven`, `path=none`,
  manual fallback only.
- Target doctor exited 0/healthy `0.6.0`, zero diagnostics, activation match. Both
  contracts are now in installed `managed_files`, activation paths and runtime
  discovery roots. `compatibility_migrations` was not persisted into the install
  manifest.
- Eight project-owned paths were byte-identical before and after apply.

The preserved v0.5.0 project-owned product tests are not target-compatible: when
run after the successful framework migration, 31 tests ran with four failures.
Three assert the old Plugin version/identity and one constructs the old upgrade
fixture without the target contract boundary. This is reported as preserved old
project-test incompatibility, not hidden as framework-migration success or treated
as damage to project-owned files.

## Fresh real-current-project acceptance

A second independent target combined a clean official v0.5.0 managed/install
state with all current candidate application/project-owned files while leaving
the protected framework/tool/install state at 0.5.0. This did not reuse an RD- or
QA-mutated target.

- 186 current project/application files were overlaid and committed as clean
  baseline `28decf15d889506204f777f5823d8b3cb4f9f65a` at
  `/private/tmp/qa-current-project.nhjn_4jt/project`.
- Old doctor exited 0/healthy `0.5.0`.
- Plan exited 0/`safe`, was byte/Git read-only, had the same `11 no-op / 17
  update` counts and exact paired migration evidence.
- Apply and target doctor succeeded; activation remained not-proven/manual-only.
- A canonical digest over application/project-owned bytes stayed exactly
  `9f1d8b85a3d5bba818cfe114e35bd7eea023244b2bf9a34830070408a6d7ee31`
  after apply and after verification. No application/project path appeared in the
  Git diff; the 17 changed files were framework/tool/install-owned.
- Default verify exited 0 and passed 45/45 tests in 94.163 s, with zero failed or
  skipped configured checks; lint/typecheck/build were unconfigured.

## Independent compatibility and trust negatives

Each case used a fresh official-tag target or fresh target-source copy.

- Missing guide, modified guide, mixed predecessor/target pair, wrong version,
  wrong normalized install identity and an unhealthy old managed set produced a
  paired two-path conflict. No partial adoption was possible.
- A target-identical pair was ordinary no-op/no migration; target-identical plus
  absent was ordinary no-op/create. Neither gained predecessor authority.
- Modified, leaf-symlinked, broken-symlinked or directory `AGENTS.md`, plus
  representative intermediate symlink/broken/type cases at `.vibe`,
  `.agents/skills` and `.codex`, failed closed for the complete pair.
- Predecessor manifest `source` absent, null or arbitrary nested JSON produced
  identical eligibility; an official-looking source could not authorize a wrong
  version. Target source trust remained separately enforced.
- All four supported target source channels—local payload, GitHub release,
  offline bundle and Plugin-bundled—made the same paired migration decision when
  their existing trust prerequisites were satisfied.
- A pre-mutation contract change was classified as blocked conflict evidence with
  no migration claim. A post-first-write mutation was classified exit 2/error,
  `write_state=unknown-partial`, `phase=unknown-partial`, with no activation claim.
- An unrelated modified managed file retained the ordinary `local and incoming
  content both changed` collision; the migration registry did not authorize it.
- Agent/core target mirror variants with boolean `schema_version=true`, extra
  field, null protocol or wrong authority all failed before planning with
  `write_state=none`. This independently confirms exact typed/closed matching and
  avoids Python's `True == 1` pitfall.
- Schema-1 compatibility was checked by projecting a real migration plan after
  ignoring `compatibility_migrations`: existing schema `1`, status `safe`, counts
  `11/17`, actions `no-op/update`, `files_changed=false` and `recovery=null`
  retained their original meanings.

## Registry, identity and activation recomputation

Independent canonical-JSON/SHA-256 recomputation from the tag and installed bytes
produced:

| Identity | Recomputed value |
|---|---|
| Compiled predecessor registry | `6cbee96e5da8b4d4b5c87403e710aac0740041027a00466f288a670834d1967d` |
| Predecessor two-contract set | `5ae7da78e4799f23056afc16b8b1511384b12db50dfb5209a64e5b465a71b15d` |
| Official v0.5 guide raw hash | `321a2e1017a09405b1d44570f21f59e0b135c127abd81f9d8258c89b3f95a304` |
| Official v0.5 Agent-install raw hash | `3ac9c51a83f1487fb298c0fd919bca99252c8972b138ae4925d44ee1544ffb4f` |
| Normalized v0.5 install identity | `70dd0eac0f54d328a803bc71ef409f66c0a6d8dc8016ce27bb80b2fa4b410fb5` |
| Current activation-v2 identity | `35f16a0c6393560794372737dc6a32b1d24a902e0f70d40989d9ce4e04d8a37c` |

The installed Agent-install and core mirrors equal the exact closed object; both
also equal the release-manifest mirror. For activation algorithm v2, only the
embedded activation digest was replaced by the zero sentinel before canonical
hashing. The normalized Agent-install path hash is `cf961483...`; its final raw
hash is `01c7c9b8...`, which separately equals the installed manifest's managed
hash. Their inequality and the recomputed activation match demonstrate raw
managed integrity separation and no self-referential fixed point.

## Controlled and live host evidence

The controlled fake host stores synthetic goal text in memory and invokes the
installed production validator for every result. Valid results return only
`structural_only=true`, `host_evidence_authenticated=false` and
`ready_claim=false`; the validator cannot mint host evidence. Dependency,
reason/action, receipt, identity, owner, custody, privacy, bounds, unknown-field,
unknown-enum and duplicate-key mutations are rejected without echoing the goal or
secret sentinels. The synthetic original goal was absent from all repository
files and validator output.

There is also positive live evidence for the documented manual boundary from
Codex task `01a0472f-80c1-7cf2-a724-81334993a255`, a distinct task in the same
saved project:

1. The source task explicitly delegated one manual-new-task continuation and
   paused writes; it did not claim hot reload or automatic handoff.
2. The successor independently read the installed 0.6 rules, Agent-install
   contracts, project context, Accepted ADR/work item and same canonical project
   root. Initial doctor/registry/default verify were healthy and 45/45.
3. It edited only `docs/releases/0.6.0.md`. Post-edit package identity drift then
   caused four packaging tests to fail; the successor stopped fail-closed and did
   not say ready.
4. After a separate explicit recovery authorization, it mechanically refreshed
   Plugin identity, ran the target self-upgrade for the changed source receipt,
   and completed with doctor healthy, final 45/45, default verify passed and
   deterministic package parity.
5. Direct inspection confirms Plugin and installed source payload
   `7c152ac7...`, root manifest `b0389a9b...`, activation `35f16a0c...` and the
   release-note evidence. Independent QA reran the final checks below.

This establishes that the manual successor can activate and continue in practice.
It is not a live `host-reload` receipt and not automatic successor creation.

## Final regression and release evidence

| Command/check | Result |
|---|---|
| Five focused predecessor tests | Pass, 5/5 in 27.021 s. |
| `python3 -m unittest discover -s tests -v` | Pass, 45/45 in 67.392 s. |
| `./bin/vibe verify --format json` | Exit 0/`passed`; required test passed 45/45 in 78.523 s; failed 0, skipped 0, lint/typecheck/build unconfigured. |
| `./bin/vibe doctor --format json` | Exit 0/healthy 0.6.0; manifest `b0389a9b...`, activation match `35f16a0c...`, zero diagnostics, network false. |
| `./bin/vibe package --output /private/tmp/qa-release-a.vSX6ZR --status release-candidate-unpublished` and independent `...qa-release-b.cmDUF8` | Both pass; 35 payload files; payload `7c152ac7...`; distribution bundle `910f3684...`; network not used. |
| `./bin/vibe validate-release <each> --format json` | Both exit 0/valid; schema/protocol 2/2 and activation `35f16a0c...`. |
| Directory/ZIP reproducibility | `diff -qr` empty. Direct ZIP `9c63677c...`, distribution ZIP `910f3684...`, Plugin ZIP `1116c717...` identical across builds. Direct/Plugin/marketplace payload maps are 35/35/35 and byte-identical. |
| `git diff --check`; unmerged-path check; repository JSON parse | Pass; no whitespace errors, no unmerged paths, 29 JSON files parse. |
| Python 3.9 grammar projection | Six Python entry/test files parse with `ast.parse(feature_version=(3,9))` under Python 3.14.6. This is grammar evidence, not a Python 3.9 runtime run. |

## Decision and scope boundaries

- The L work item records the initial Accepted ADR, both reopened readiness gates,
  the Accepted closed predecessor amendment, independent review and Workflow
  orchestrator reconfirmation before each implementation phase. No bypassed or
  retroactively manufactured technical-decision gate was found.
- The target CLI's compiled registry is authoritative. Editable predecessor
  `source` and on-disk mirrors cannot grant migration authority; target source
  trust remains a separate prerequisite.
- The feature adds compatibility authentication and race classification around
  existing writes. It adds no whole-upgrade transaction, snapshot, backup or
  rollback claim and does not change the separate atomic-upgrade ownership.
- No network acquisition, publication, hook, MCP server, app, background process,
  reload API or task-creation API was added or exercised.
- Existing unrelated user work, including
  `20260827-permission-safe-atomic-upgrade`, was preserved and not evaluated as
  part of this feature.

## Publication blockers and limitations

All product criteria pass for the local unpublished candidate, but a GitHub
Release is still blocked:

- The 0.6.0 candidate changes are uncommitted in a dirty working tree and there is
  no `v0.6.0` tag.
- No authenticated GitHub release operation, published artifact, public Plugin
  installation or network acquisition was performed.
- The available runtime is macOS/Python 3.14.6. Actual Python 3.9 runtime and
  Linux execution were unavailable; only Python 3.9 grammar compatibility was
  checked.
- There is no positive live Codex same-task reload or automatic-successor receipt.
  Current repository/Plugin capability remains truthfully manual-fallback-only.

Therefore this record authorizes **the unpublished 0.6.0 candidate only**. It
does not authorize a GitHub Release, and it must not be presented as evidence of
current-task hot reload or automatic successor handoff.
