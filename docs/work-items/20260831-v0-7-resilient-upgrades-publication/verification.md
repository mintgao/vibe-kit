# Verification: Vibe Kit v0.7.0 — resilient upgrades and first-class prerelease publication

- QA date: 2026-08-31
- Status: **verified**
- Final verdict: **PASS — public v0.7.0 Pre-release verified and issues #1-#5 closed**
- Release URL: https://github.com/mintgao/vibe-kit/releases/tag/v0.7.0
- Release commit: `440f360524b44099b2d0d8c9a9688b91f7de6880`
- Annotated tag object: `55fb231d841f85d4fb7834e9d3fc878b337a615e`
- Evidence boundary: independent QA verified the exact clean release commit, public
  tag/Release/assets, unauthenticated downloads, controlled install/upgrade
  fixtures, and the separately authorized issue closeout. No platform-enforced
  immutability, live Linux certification, Stable promotion, public Plugin Directory
  publication, same-task reload or automatic successor claim is made.

## Acceptance evidence

| Criterion | Independent evidence | Result |
|---|---|---|
| AC-1 — Supported onboarding bridge | Exact audited v0.2 and official v0.3/v0.4 predecessors create only canonical schema-1 `pending`; public v0.3 safely upgraded to a healthy target. Missing v0.5/v0.6 onboarding blocks before control/project writes, while valid onboarding is preserved. | Pass |
| AC-2 — Onboarding preservation | Existing onboarding remains byte-identical. Malformed, conflicting, wrong-type and raced states fail closed; rollback removes a create-only bridge without leaving false success evidence. | Pass |
| AC-3 — Handled failure consistency | Faults after all 24 official-v0.3 and seven official-v0.6 visible leaf mutations, plus directory publication failure, restored the exact scoped predecessor without traceback or false success/healthy claims. | Pass |
| AC-4 — Interrupted recovery | Prepared/commit/cleanup interruption, rollback failure, tamper, symlink, unknown path and third-party divergence cases passed. Deterministic recovery preserves evidence and reports `unknown-partial` when safe classification is impossible. | Pass |
| AC-5 — Regression boundary | Managed conflict, predecessor authentication, AGENTS merge, source/channel, stale-path, symlink/race and project-preservation regressions pass in text/JSON and the full 57-test suite. | Pass |
| AC-6 — Precise trust contract | Normative and user-facing contracts distinguish exact selection, SHA-256 verification, mutable GitHub refs/assets and platform-enforced immutability without changing accepted source shapes. | Pass |
| AC-7 — Trust regression/public metadata | Contract tests reject stronger claims. GitHub's live Release API reports `immutable=false`; both publication/final receipts record that value and the limitation states that hashes do not create platform immutability. | Pass |
| AC-8 — Reviewable publication dry run | The offline no-write/no-network intent `1914fe1761cae16224a94e6f96c9dd71ecff9f2a4179848295ece1cef418a175` binds the exact commit, tag object, body, five assets, remote snapshot, six operations, authorization and recovery rules. | Pass |
| AC-9 — Consent-bound publication | Two-layer authorization, bounded ordered execution, lease/read-before-write/read-back and retry rules were honored. The original publication receipt `e18b2cd723afa6199cb0cefcd74817c3b431cf29cdd736ce6f988ed2c2b61064` validates with confirmed-complete writes and passed verification. | Pass |
| AC-10 — Public artifact verification | All five unauthenticated public downloads are byte-identical to the candidate; outer hashes, 47/47 nested checksums and Python 3.9 `validate-release` pass. Direct/Plugin and public v0.3/v0.5/v0.6 smokes end healthy. | Pass |
| AC-11 — Offline/privacy boundary | Actual `/usr/bin/python3` 3.9.6 passes all 57 tests. Local package/validation/install/upgrade remain standard-library/offline; artifacts, receipts and comments contain no credential, environment, raw-host or conversation data. | Pass |
| AC-12 — Readiness closure | The L-work author/reviewer/orchestrator/RD/QA chain is recorded. Closeout schemas, final-leaf atomicity and absent-parent directory units each paused work, amended the ADR, received distinct review and required a fresh implementation-ready confirmation before resume. | Pass |
| AC-13 — Exact candidate quality | Clean commit `440f360...` passes focused 12/12, full 57/57 on Python 3.14 and actual Python 3.9.6, default verify, healthy doctor, JSON/diff/bytecode checks and two byte-identical clean builds with dual valid release validation. | Pass |
| AC-14 — Public release and closure | Annotated tag `55fb231d...` peels to `440f360...`; Release `379394868` is one exact non-draft Pre-release with five assets. The canonical closeout posted exact marker-bound evidence, closed #1-#5 and produced final receipt `a6f9f9959442e00120f12e696a91c5df4a10d37ba147381067bfc475ba11098b`, independently matched to live API state. | Pass |

## Automated and public checks

| Check | Independent result | Notes |
|---|---|---|
| Exact focused QA | Pass, 12/12 | Leaf/directory races, rollback/recovery, onboarding and result truthfulness. |
| Full suite, Python 3.14.6 | Pass, 57/57 | Exact clean release commit. |
| Full suite, `/usr/bin/python3` 3.9.6 | Pass, 57/57 | Required runtime evidence. |
| Default `vibe verify` | Pass, 57 tests | Lint/typecheck/build are not configured and are reported as not applicable. |
| Exact-commit `vibe doctor` | Healthy, read-only | Activation `07613a6a22db6bb6454ba55dbaf12681b54e5024eff6d526f99ee45d2d2fe992`; payload `874675420e697ab9c16c35a4f2f558acc65b91dcc42464bd461cda2800116eb1`. |
| Bytecode, JSON and diff checks | Pass | Python compilation, repository JSON parsing and `git diff --check`. |
| Clean A/B prerelease builds | Pass | Byte-identical five-asset outputs; both `validate-release` calls valid. |
| Public distribution validation | Pass | Five public/local `cmp` checks, outer SHA-256, 47/47 nested checksums and Python 3.9 validation. |
| Public direct/Plugin smoke | Pass | Fresh direct init/doctor and downloaded Plugin-bundled plan/init/doctor. |
| Public predecessor smoke | Pass | Official v0.3, v0.5 and v0.6 upgrades reach healthy v0.7 doctor under the accepted onboarding rules. |

## Public Git and GitHub state

| Item | Public value |
|---|---|
| Release | ID `379394868`; `Vibe Kit v0.7.0`; public, non-draft, Pre-release; `immutable=false` |
| Release URL | `https://github.com/mintgao/vibe-kit/releases/tag/v0.7.0` |
| Published at | `2026-08-30T20:33:37Z` |
| Tag ref | `refs/tags/v0.7.0` -> annotated object `55fb231d841f85d4fb7834e9d3fc878b337a615e` |
| Peeled tag | `440f360524b44099b2d0d8c9a9688b91f7de6880` |
| Tagger time | `2026-08-30T20:27:56Z` |
| Public main before this evidence update | `440f360524b44099b2d0d8c9a9688b91f7de6880` |

The annotated tag is unsigned. Its exact object identity and verified public
asset hashes establish the recorded selection/content identity but are not an
external signature, provenance attestation or platform immutability guarantee.

## Publication assets and digests

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 6,112 | `f9c8f7e226a296a0dc8dc05bc77443d689ab1b4326439b052e24dd08853c4042` |
| `release-manifest.json` | 12,144 | `e71abe8b1611a806332849d189cd18b5c08249d104a2fbbae07c6a0e628b1c5b` |
| `vibe-kit-0.7.0.zip` | 148,972 | `1999a2c32f452371f398e8c7065fd77b93a51c9333853f4e11fdb3a80bb44390` |
| `vibe-kit-distribution-0.7.0.zip` | 461,899 | `ac308a251cc1844f859f0dc6bc2b318dc6b1e379e71501b6b88f89b2f8467cdb` |
| `vibe-kit-plugin-0.7.0.zip` | 155,914 | `1975e4714fda651c65740eabd1a54465ddcb486cbab8b02aaa9850d4f96dd831` |

The exact sorted asset-set identity is
`48725c411085ba4d5dcdbfd7208f61c59ccc3cbae39940fbe3077717c30034e5`.
All five public downloads match the candidate byte-for-byte. The public manifest
retains clean source commit `440f360...`, payload
`874675420e697ab9c16c35a4f2f558acc65b91dcc42464bd461cda2800116eb1`
and activation
`07613a6a22db6bb6454ba55dbaf12681b54e5024eff6d526f99ee45d2d2fe992`.

## Issue closeout evidence

Closeout ID:
`3426e8ff30eba84a97e4795e1b97d1bf613425acaebc1b26915611bb78c9183b`.
The canonical closeout intent SHA-256 is
`52f78a811ec57670322fd73021adeccd8efb1b3fc05bc01b81720442cbffd949`;
authorization is `v070-closeout-20260831-001`. Each issue was read before its
comment, the exact comment was read back before close, and the final closed state
was read back. Independent QA found exactly one matching marker/body per issue.

| Issue | Exact comment ID | Final state |
|---:|---:|---|
| #1 | `5471177534` | Closed |
| #2 | `5471182498` | Closed |
| #3 | `5471191865` | Closed |
| #4 | `5471197316` | Closed |
| #5 | `5471203962` | Closed |

The final receipt preserves the validated pre-closeout publication receipt and
replaces only `issue_closeout: null` with the exact ADR 0011
`confirmed-complete` object. Its SHA-256 is
`a6f9f9959442e00120f12e696a91c5df4a10d37ba147381067bfc475ba11098b`.

## Recovery and limitations

- Any uncertain future Git/GitHub action must be read back by natural key before
  retry. Never force-move the tag, delete/replace the Release or edit/delete/reopen
  issue evidence without a new explicit destructive decision.
- GitHub reports `immutable=false`; the release is exact and hash-verified, not
  platform-enforced immutable.
- macOS and actual Python 3.9.6 are executed evidence. Linux libc adapters have
  unit/errno coverage but no live Linux certification.
- Same-task reload and automatic successor remain unsupported without independent
  live host receipts; activation remains the documented manual-new-task fallback.
- The release is Pre-release, not Stable, and is not promoted to a public Plugin
  Directory.
- Transaction evidence is integrity-checked but does not defend against a
  malicious same-OS-principal process deliberately targeting random private names.

## Files changed by final evidence closeout

- `docs/work-items/20260831-v0-7-resilient-upgrades-publication/brief.md`
- `docs/work-items/20260831-v0-7-resilient-upgrades-publication/verification.md`
