# Verification: Publish Vibe Kit v0.10.1

Frozen candidate: `6e523230e48fa48933eab7e680ff36284a43159c`, working tree clean
(re-checked before and after the independent run).
Verifier: independent QA subagent (Hermes, dispatched 2026-09-22 23:47, completed
in 186 s, read-only in the repository) executing a pre-written run-shaped harness
exactly once; plus the orchestrator's own read-back of the four raw result files
and its own re-derivation of the gate evidence.

## Host capability limitation

- `- limitation:` this host's subagent sessions are capped at a 600 s budget and
  analysis-shaped packets have timed out repeatedly on this repository, so the
  pre-chosen focused subset is a run-shaped harness
  (`.vibe/local/v0-10-1-gate/qa-run.sh`, sha256 `24aa0253…`, smoke-tested by the
  author in a `--quick` mode that deliberately skips the acceptance run) that an
  independent subagent executes exactly once against the frozen candidate. The
  harness is authored by the implementer, so independence covers execution,
  environment and reporting on the frozen candidate, not the authorship of the
  checks. The harness carries the complete default `verify` run, so that run is
  owned by the independent execution rather than duplicated by the orchestrator.
- `- complete run:` independent QA subagent, on the frozen candidate:
  `python3 bin/vibe verify . --format json` => `status: passed`, exit 0, summary
  `passed 1 / unconfigured 3 / failed 0 / skipped 0 / environment-limited 0`,
  default order `lint → typecheck → test → build` with only `test` configured;
  the same candidate's lane was run by the implementer as the pre-freeze gate on
  both interpreters — `Ran 127 tests … OK` on CPython 3.13.9 and `Ran 127 tests
  … OK` on CPython 3.9.6 (118 before this work item); `doctor` => `status:
  healthy`, `kit_version 0.10.1`, activation `match`, zero diagnostics.
- `- independent focused re-run:` independent QA subagent, pre-chosen subset = the
  harness's four default-CLI surfaces plus the candidate/clean-tree pins =>
  `head 6e52323…`, `tracked+untracked changes: 0` before and `changes: 0` after,
  `verify: {"status": "passed"}`, `doctor: {"status": "healthy", "errors": [],
  "warnings": []}`, `readiness: {"status": "valid"}`, `managed-agents: {"status":
  "valid"}`; no command failed and the subagent reported no repository write.
  Raw stdout: `.vibe/local/v0-10-1-gate/qa/qa-stdout.txt` (24 lines, sha256
  `9d89ff5f…`); raw results `qa/verify.json` (`dd58b43f…`), `qa/doctor.json`
  (`4ed7b2ee…`), `qa/readiness.json` (`d53f5b69…`), `qa/managed-agents.json`
  (`28084424…`); transcript `~/.hermes/cache/delegation/live/deleg_d131ec19/task-0.log`.
  The orchestrator read all four files back itself before writing this record.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | The source carries `0.10.1` coherently in `.vibe/core/version`, `.vibe/version`, `.vibe/manifest.json#framework_version` and `#source.ref`, `agent-install.json#kit_version` and the Plugin metadata; the maintenance bridge's `maximum_installed_kit_version_exclusive` is `0.10.1` with `minimum_installed_kit_version 0.2.0`, manifest schemas `[1]` and agent protocols `[0, 1, 2, 3]` unchanged; the `v0.5.0-unmanaged-agent-contracts-v1` registry entry targets `0.10.1` and its compiled digest was recomputed to `7cedd9fb…` in the checked literal and both mirrors (`test_publication_schemas_and_identity_are_mirrored_everywhere`, `test_bridge_bound_and_predecessor_migration_advance_to_the_current_target`, `test_the_compiled_registry_digest_matches_the_target`); every mirror was regenerated in the same change and 63/63 recorded checks equal a fresh recomputation including a disposable `init` cross-check, stable on a second run; `doctor` healthy with zero diagnostics. | Pass |
| AC-2 | `CHANGELOG.md` carries the `0.10.1` entry and `docs/releases/0.10.1.md` is the Release body and a payload file (present in `SHA256SUMS`, `a0d919e7…`); the entry and the note describe exactly the Hermes label raise, the version identity and the advanced bridge/registry bound, and claim no product change, no stable promotion, no live reload and no Codex refresh; the two tracked follow-ups (#14, #15) and the Codex handoff are named. Both homepages were reviewed and synchronized — nine replacements per language for the latest-published link, the two adoption prompts, the contract paragraph (publication schema 5 with a separate closeout schema 3), the `validate-release dist/vibe-kit-0.10.1` example, the release-notes link and the limitations bullet — with a reasoned record for the sections left unchanged in `implementation.md#Homepage review (reasoned record)`. | Pass |
| AC-3 | The closed schema-5 `vibe-kit-v0.10.1-prerelease` profile fixes version, annotated tag, Release title, body path, exactly five assets, the six-operation allowlist, the nine-smoke set, AC-1…AC-6 with AC-6 `not-runnable-before-publication`/`live-read-back`, the six `vibe-kit-v0.10.1-*` evidence kinds, the authorization fields and issue policy `{"mode": "none", "issues": [], "allowed_operations": []}` (`test_profile_is_closed_and_pinned`); intent, receipt and authorization acceptance are pinned (`test_profile_intent_receipt_and_authorization_acceptance`); a v0.10.1 candidate cannot pass the schema-2, schema-3 or schema-4 profiles and an unknown schema is refused while the historical profiles still accept their own fixtures (`test_historical_profiles_reject_a_v0101_candidate`, `test_historical_profiles_reject_a_v010_candidate`, `test_schema_5_rejects_a_wrong_identity`, `test_schema_5_rejects_a_wrong_release_body_or_assets_and_operations`); no schema-5 closeout exists and the CLI refuses a schema-5 parent (`test_no_schema_5_closeout_exists`). | Pass |
| AC-4 | The prepublication harness (`.vibe/local/v0-10-1-gate/upgrade-scenarios.py`, sha256 `f0989f67…`, 40/40 checks, raw output `upgrade-scenarios.out.txt` sha256 `d0378068…`) ran offline in throwaway directories: a predecessor-`init` install recorded at `0.10.0` with the combined selection upgraded through the maintenance bridge into the candidate and ended doctor-healthy with its appended project-owned `AGENTS.md` bytes and its recorded host selection preserved; a recorded `0.9.0` install upgraded the same way; fresh candidate installs were doctor-healthy for `codex` (both hosts recorded), `hermes` (no Codex payload present) and the combined selection, each reading publication schema 5 and the installed contract's Hermes label `verified`; the `v0.5.0-unmanaged-agent-contracts-v1` migration planned (`status: safe`, phase `planned`, digest `7cedd9fb…`) and applied (phase `applied`) under the advanced target and ended doctor-healthy. | Pass |
| AC-5 | On the frozen candidate: the default lane passes on CPython 3.13 and 3.9 with 127 tests each, `verify` `passed`, `doctor` healthy, `validate-readiness` valid for this brief, `inspect-managed-agents` valid, `package` valid with 36 payload files and no network use, and two independent clean builds (clones of the same commit on branch `main`, trees clean before and after) produce byte-identical five-asset sets — `release-manifest.json b3d5d3933571fbd0dae24424dbd0d71053a0c8c139cdc4d4c5e7ebd33b54921d`, `vibe-kit-0.10.1.zip ece6fbcc78338dbf7fcbe45cf0149a3854d1227b01ed99457544bd63e4244af7`, `vibe-kit-distribution-0.10.1.zip f62ca49069f45d35d1e7e3ff5d281ff18ac4326691242be9414a2e027a8395f5`, `vibe-kit-plugin-0.10.1.zip 60cb9910317b7034d509964cac60700d959df1c5ee9cc487df7744bb3d862893`, with `SHA256SUMS 3045ed79baf7da3bc53fbd26c1cd8462fdf752e832936cba7ee9bb614c617c9d` listing them; `validate-release` passed for both builds. | Pass |
| AC-6 | No GitHub write happened in this work item: `origin/main` still reads `dc88d3fd…`, no `v0.10.1` tag and no Release exist, and the work item performed no push, tag, Release, asset upload or issue mutation. The publication profile's live criteria are recorded `not-runnable-before-publication` and its post criteria are bound to `confirmed-complete` remote state; "v0.10.1 published and verified" is claimable only from a passed public verification under a separate authorization bound to the frozen intent digest. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| Project verification (`verify . --format json`) | Pass | passed 1, unconfigured 3 (lint, typecheck, build), failed 0, skipped 0, environment-limited 0 — the single acceptance run, owned by independent QA |
| Default lane, CPython 3.13.9 | Pass | 127 tests, OK, 53.3 s |
| Default lane, CPython 3.9.6 | Pass | 127 tests, OK, 52.8 s |
| `doctor . --format json` | Pass | healthy, `kit_version 0.10.1`, activation `match`, zero diagnostics |
| `validate-readiness` (this brief) | Pass | valid, findings `[]` |
| `inspect-managed-agents . --format json` | Pass | valid against `.vibe/manifest.json#agents_block_hash` |
| `package` twice into fresh independent clones | Pass | 36 payload files, network not used, five assets byte-identical across builds |
| `validate-release` | Pass | passed for both builds |
| Mirror regeneration (`rebuild-mirrors.py`) | Pass | 63 checks, `failed: none`, identity `d418a177…` / `b828663d…`, stable on a second run |

## Manual scenarios

- A real `v0.10.0` predecessor install (extracted with `git archive v0.10.0`),
  installed with its own CLI and upgraded with the candidate CLI, plus the same
  flow from `v0.9.0`: doctor healthy afterwards in both cases.
- A real `v0.5.0` checkout adopted by the candidate CLI, exercising the registry
  target `0.10.1` through `plan upgrade` and `upgrade`.
- The fresh-install matrix for the `codex`, `hermes` and combined selections,
  including the assertion that a `hermes`-only install carries no Codex payload.
- Every scenario ran in a throwaway temporary directory; nothing was installed
  over this checkout, and the harness performs no network access.
- Self-inflicted failures found and corrected while building the gate, recorded so
  they are not mistaken for candidate defects: redirecting build output into the
  clone made `--untracked-files=all` read the tree as dirty (outputs moved outside
  the trees), and a detached-HEAD clone is refused by `release_source_metadata`
  because `ref` comes from `git rev-parse --verify HEAD` against a branch (builds
  re-run on clones of `main`).

## Limitations and follow-ups

- The QA harness is authored by the implementer; independence covers execution,
  environment and reporting, not the authorship of the checks. No host telemetry,
  live isolation or token-reduction claim is made anywhere.
- Not exercised here, by design: the remote publication itself, the
  post-publication acceptance criteria and the live read-back. They require a
  separate authorization bound to the frozen publication-intent digest and are
  recorded `not-runnable-before-publication`.
- Deferred to the next iteration by the accepted decision, not skipped: feedback
  issues #14 and #15. The Codex five-stage refresh stays a delivered handoff with
  its record on the older evidence.
- The `0.9.0`-era same-version re-upgrade defect stays out of scope for a patch
  release; the admission paths exercised here contain no re-upgrade.

## Publication completion (recorded after this verification)

The candidate was published on 2026-09-23 under a separate authorization bound
to the frozen intent digest `0ed6d34f…`: main fast-forwarded `dc88d3f… → 409d67a…`
under an expected-old-OID lease, annotated tag `v0.10.1` = `2fd9de20…`, Release
`394214638` (`https://github.com/mintgao/vibe-kit/releases/tag/v0.10.1`) with the
byte-equal frozen note and exactly five assets, all five public downloads matched,
nine of nine public smokes passed, and `validate-publication` returned `valid` on
CPython 3.9.6. Full facts, operation ledger, the transport incident and resume,
and the evidence digests are in `postpublication.md`. “v0.10.1 published and
verified” is claimable from that record; platform immutability is reported
`false` and no host activation is claimed.