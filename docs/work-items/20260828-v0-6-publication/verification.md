# Verification: Publish Vibe Kit v0.6.0 GitHub prerelease

- QA date: 2026-08-28
- Status: **verified**
- Final verdict: **PASS — public v0.6.0 Pre-release verified**
- Release URL: https://github.com/mintgao/vibe-kit/releases/tag/v0.6.0
- Release commit: `e76c5b3b896f479f3a3d331c640c4bb64002d1ce`
- Annotated tag object: `189223683b1342ed7015ab97ca05185fc9c6d8ec`
- Evidence boundary: local source/build receipts, GitHub public metadata, public
  re-downloads, controlled upgrade/install fixtures and the previously verified
  manual-new-task continuation are reported separately. No same-task reload,
  automatic successor, Linux or public Plugin Directory claim is made.

## Acceptance evidence

| Criterion | Independent evidence | Result |
|---|---|---|
| AC-1 — Release-facing consistency | Clean commit source, protocol, Agent-install contracts, Plugin manifest/Skills, changelog, English/Chinese READMEs, durable context and 0.6.0 release note consistently identify `0.6.0` as a GitHub **Pre-release**. They explicitly deny stable promotion, whole-upgrade atomicity, automatic network updates and unsupported Agent/platform claims. Repository/Plugin activation remains `manual-fallback-only`; same-task reload and automatic successor require independent live receipts. | Pass |
| AC-2 — Exact-candidate QA | Python 3.9 focused predecessor tests passed 5/5; full configured tests passed 45/45; default verify passed its 45-test command with zero failed/skipped configured checks and lint/typecheck/build explicitly unconfigured. Doctor was healthy. JSON, diff, Python 3.9 bytecode, exact mirror/type checks, and missing/modified/mixed/version/identity/managed-health/AGENTS/symlink/race/source/channel negatives passed. | Pass |
| AC-3 — Upgrade acceptance and host truth | Intact official v0.5.0 and real-current-project fixtures produced safe read-only paired migration plans, successful apply and healthy target doctor. Their Git diffs contain only the 17 expected framework/tool paths; project/application-owned bytes stayed unchanged. The official old project truthfully retains four incompatible v0.5 product-test failures. The real-current project passed target default verify 45/45. Manual-new-task continuation is the only positive live host evidence; no hot reload or automatic handoff is inferred. | Pass |
| AC-4 — Python/platform evidence | Actual CPython 3.9.25 on macOS passed compilation/bytecode, focused/full/default verification, doctor, deterministic packaging and release validation. Linux was unavailable and is disclosed as an unverified Pre-release limitation rather than a compatibility claim or product failure. | Pass |
| AC-5 — Clean committed deterministic release | Clean worktree HEAD was exactly `e76c5b3...`; the commit contains the reviewed 43 candidate paths and excludes the unrelated atomic-upgrade directory and index line. The development checkout still preserves that unrelated dirty work. Two `status=prerelease` builds are directory/byte-identical, valid, and source-bound to the exact clean commit. Each exposes exactly the intended five top-level publication files. | Pass |
| AC-6 — Immutable refs | Public `refs/tags/v0.6.0` points to annotated tag object `18922368...`, whose target peels to commit `e76c5b3...`. At publication read-back, public `main` equaled the same commit; the evidence-only follow-up may advance `main` while retaining that release commit in history. | Pass |
| AC-7 — Public Release shape | GitHub API reports Release ID `378350954`, tag `v0.6.0`, name `Vibe Kit v0.6.0`, `draft=false`, `prerelease=true`, published `2026-08-28T08:30:27Z`. The public asset set is exactly the five required files and no others. | Pass |
| AC-8 — Remote read-back parity | GitHub asset size/digest metadata, fresh public downloads and local build-a bytes agree for all five assets. `cmp` passed for every public/local pair. Public manifest remains `status=prerelease`, clean-source-bound to `e76c5b3...`, payload `d6b034c4...` and activation `35f16a0c...`. | Pass |
| AC-9 — Isolated public artifact smoke | The extracted public distribution passed every nested `SHA256SUMS` entry and Python 3.9 `validate-release`. Official-v0.5 public-source upgrade, real-current-project upgrade, fresh direct init and Plugin-bundled init all ended with healthy 0.6.0 doctor and matching activation. Direct/Plugin/marketplace validation proved byte identity. Official old tests failed exactly the four documented cases; real-current target verify passed 45/45. | Pass |
| AC-10 — Durable evidence and recovery | This record contains exact commit/tag/release refs, URL, asset sizes/digests, source/payload/activation identities, commands/results, host/platform/channel limitations, unrelated-work boundary and the inspect-before-retry/non-destructive recovery rule. Uncertain remote operations require read-back before retry; Release/tag deletion or rewrite requires a separate destructive decision. | Pass |

## Public Git and GitHub state

Read-only GitHub API checks returned:

| Item | Public value |
|---|---|
| Release | ID `378350954`; `Vibe Kit v0.6.0`; public, non-draft, Pre-release |
| Release URL | `https://github.com/mintgao/vibe-kit/releases/tag/v0.6.0` |
| Published at | `2026-08-28T08:30:27Z` |
| Tag ref | `refs/tags/v0.6.0` -> annotated tag object `189223683b1342ed7015ab97ca05185fc9c6d8ec` |
| Peeled tag | `e76c5b3b896f479f3a3d331c640c4bb64002d1ce` |
| Public main before this evidence update | `e76c5b3b896f479f3a3d331c640c4bb64002d1ce` |

The annotated tag message is `Vibe Kit v0.6.0`; its public tagger timestamp is
`2026-08-28T08:29:22Z`.

## Publication assets and digests

The GitHub API asset set, public-download top-level file set and authorized upload
set are exactly:

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `release-manifest.json` | 11,191 | `1e3406b224d4999c9e713c4f4b76661a93ac10e68e838aa37e780ff3efd72610` |
| `SHA256SUMS` | 5,972 | `ba436e2ec75f452dc7f60a6cbe24e77ae0f853d75d3eafa2d931691500372ab9` |
| `vibe-kit-0.6.0.zip` | 104,996 | `7e0f48835d094b438cf4ed95585a86db97f4f3fd2e1bd44de7cb1693ee4994b2` |
| `vibe-kit-plugin-0.6.0.zip` | 111,826 | `8fce91e1bf0812179ac91162f34b25d7907e3a912fdefc2022759ea8ea1d73e4` |
| `vibe-kit-distribution-0.6.0.zip` | 329,492 | `8b9691e8d7dae612dd4197c8de7f20ecf867202e12f874912944ab19eb9c49d8` |

The expanded `marketplace/` tree in local build directories is validation input,
not a sixth uploaded asset. Build-a/build-b directory diff was empty. Both release
manifests declare:

```text
status: prerelease
source.type: git-working-tree
source.tree_state: clean
source.ref: e76c5b3b896f479f3a3d331c640c4bb64002d1ce
payload_tree_sha256: d6b034c46d4893f2f7afb6da5c8961668fcae5532d82d7b1a9f949fd5f1ae5a4
activation_set_sha256: 35f16a0c6393560794372737dc6a32b1d24a902e0f70d40989d9ce4e04d8a37c
```

The same values were parsed from the public manifest. Public/local `cmp` passed
for all five assets.

## Source, test and Python 3.9 evidence

- Exact release worktree:
  `/private/tmp/vibe-kit-0.6-release-source.vjpMvo/repo`.
- Deterministic prerelease builds:
  `/private/tmp/vibe-kit-0.6-release-source.vjpMvo/build-a/release` and
  `/private/tmp/vibe-kit-0.6-release-source.vjpMvo/build-b/release`.
- Actual runtime:
  `/Users/bytedance/.local/share/uv/python/cpython-3.9.25-macos-aarch64-none/bin/python3.9`
  reported Python 3.9.25.
- Python 3.9 bytecode compilation passed for `bin/vibe`, the two Plugin wrappers,
  fake host and both test modules.
- Focused authenticated-predecessor suite: 5/5 passed in 32.783 seconds.
- Full configured suite: 45/45 passed under Python 3.9.25. A separate default
  `verify --format json` also passed its complete 45-test command; failed/skipped
  configured checks were zero, while lint/typecheck/build were unconfigured.
- Exact-commit doctor: healthy 0.6.0, zero diagnostics, activation match
  `35f16a0c...`, manifest `c5c420fb...`, network false.
- Both prerelease packages and both explicit `validate-release --format json`
  calls passed under Python 3.9; payload count was 35.
- `git diff --check`, repository JSON parse and exact candidate path review passed.

## Public-download and installation evidence

Public re-download root:
`/private/tmp/vibe-kit-0.6-public-download.a2QdWW`.

### Distribution validation

- All nested entries in
  `distribution/vibe-kit-0.6.0/SHA256SUMS` returned `OK`.
- Python 3.9 `validate-release` on the extracted distribution returned
  `status=valid`, 35 payload files, payload `d6b034c4...`, activation
  `35f16a0c...`, schema/protocol 2/2 and `network_used=false`.
- Validation covers direct ZIP, Plugin payload, expanded marketplace, compiled
  predecessor registry/mirrors, activation identity and forbidden Plugin
  capability drift.

### Official intact v0.5.0 upgrade

Fixture: `official-v050`.

- The release flow used a safe/read-only exact public-source plan with the paired
  authenticated predecessor updates, then successful apply.
- Installed manifest binds the canonical public Release URL, direct asset
  `7e0f4883...`, payload `d6b034c4...` and activation `35f16a0c...`.
- Target doctor is healthy 0.6.0, zero diagnostics.
- Git diff contains only the 17 expected framework/tool paths; project-owned
  files and old product tests remained unchanged.
- The preserved old suite ran 31 tests and failed exactly four:
  `test_prerelease_package_requires_clean_commit_and_records_provenance`,
  `test_release_package_is_reproducible_installable_and_tamper_evident`,
  `test_release_validation_rejects_unsafe_archives_and_plugin_drift`, and
  `test_upgrade_updates_managed_files_and_preserves_project_files`.
  The first three retain old Plugin version/identity assumptions; the fourth is
  incompatible with the new installed Agent-contract boundary. These are the
  documented project-owned v0.5 incompatibilities, not hidden release failures.

### Real current-project upgrade

Fixture: `current-project-v050`.

- Baseline commit `041a0f0` combined official 0.5 installation state with current
  project/application-owned content.
- Exact public-source plan/apply and target doctor passed.
- Git diff contains the same 17 framework/tool paths only; project/application
  bytes remain preserved.
- Target default verify passed 45/45; doctor is healthy 0.6.0, source URL/artifact,
  payload and activation match the public Release.

### Fresh direct and Plugin installs

- `fresh-init` doctor is healthy 0.6.0 and binds GitHub Release source, direct
  asset `7e0f4883...`, payload `d6b034c4...` and activation `35f16a0c...`.
- The supplied `plugin-init` directory is healthy but its manifest says
  `local-payload`; it was therefore not used as proof of Plugin-channel
  provenance.
- Independent QA reran the downloaded public Plugin wrapper from
  `plugin/vibe-kit/skills/vibe-bootstrap/scripts/vibe_from_plugin.py` with exact
  `plugin-bundled`, ref `0.6.0` arguments into
  `plugin-init-provenance`. Plan was safe/read-only, init succeeded, the manifest
  records `plugin-bundled`, ref `0.6.0`, artifact `null`, payload `d6b034c4...`
  and activation `35f16a0c...`; installed doctor is healthy. This closes the
  mislabeled fixture evidence gap without changing release bytes.

## Exact commit scope and unrelated work

The release commit changes exactly the 43 reviewed candidate paths. It contains
neither:

```text
docs/work-items/20260827-permission-safe-atomic-upgrade/brief.md
docs/work-items/20260827-permission-safe-atomic-upgrade/verification.md
```

Its `docs/work-items/index.md` also omits the pending atomic-upgrade entry. The
main development checkout still preserves both untracked files and its modified
index entry. That work remains `shaped`/unimplemented with pending verification;
it did not enter the release commit, artifacts or claims.

## Host, platform and trust limitations

- There is no positive live Codex same-task reload or automatic-successor receipt.
  The current repository and Plugin remain manual-fallback-only. Controlled
  receipts prove contract conformance only; the previously verified distinct
  manual-new-task continuation is the sole positive live takeover evidence.
- No Linux runtime was available. This release is not Linux-certified; macOS and
  actual Python 3.9.25 are the executed platform/runtime evidence.
- The release is not stable and is not in a public Plugin Directory. It provides
  no automatic network updater, reload API, task-creation API, hook, MCP server or
  background process.
- Git tag identity and SHA-256 prove ref/content consistency but are not an
  external publisher signature, provenance attestation or transparency log.
- Whole-upgrade transaction/rollback behavior remains outside this release. The
  CLI retains truthful managed-conflict and `unknown-partial` recovery semantics.

## Recovery boundary

- On any uncertain Git/GitHub operation, inspect the exact remote tag, commit,
  Release and asset state before retrying. Never issue duplicate create/upload
  operations based only on an uncertain command result.
- Do not delete, rewrite or replace the public Release/tag without a separate,
  explicit destructive decision.
- Installed-project downgrade uses an explicitly selected trusted older payload
  and is semantic, not a claimed byte-for-byte transaction rollback. Preserve
  project-owned files and inspect retained stale paths.
- Keep the unrelated atomic-upgrade work in the development checkout; do not
  rewrite history or discard it as part of release recovery.

## Files changed by final QA

- `docs/work-items/20260828-v0-6-publication/verification.md` only.
