# Verification: Vibe Kit v0.7.0 — resilient upgrades and first-class prerelease publication

- QA date: 2026-08-31
- Status: **local candidate verified; final commit and public release pending**
- Current verdict: **PASS for implementation/local release gates**
- Release target: `mintgao/vibe-kit`, annotated `v0.7.0`, one non-draft GitHub Pre-release
- Evidence boundary: independent read-only QA has accepted the frozen working-tree implementation. Exact clean-commit build, live publication intent/receipt, public downloads and issue closeout remain separate pending gates.

## Acceptance evidence

| Criterion | Independent evidence | Result |
|---|---|---|
| AC-1 — Supported onboarding bridge | Exact audited v0.2 fixture and official v0.3/v0.4 predecessors create only canonical schema-1 `pending`, upgrade successfully and reach healthy target doctor. Missing v0.5/v0.6 onboarding blocks before control or project writes. | Pass |
| AC-2 — Onboarding preservation | Existing onboarding is byte-preserved. Malformed, wrong-type, raced file/symlink/directory state fails closed. Absent-path publication uses a retained hard-link identity and no-clobber semantics; rollback restores absence without check-then-unlink. | Pass |
| AC-3 — Handled failure consistency | Every one of 24 official-v0.3 changed leaves and seven official-v0.6 existing-parent leaves was faulted immediately after mutation; each exact rollback restored the predecessor. Directory-unit post-publication fault also rolled back. Results contain no traceback and preserve truthful write/installation state. | Pass |
| AC-4 — Interrupted recovery | Prepared evidence, durable commit marker, explicit `recover-upgrade`, symlink/tamper/unknown-member negatives, cleanup crashes and repeated recovery passed. Final-root file/symlink/directory winners, post-publication tree addition and rollback-detach recreation preserve third-party objects and return truthful unknown-partial with active evidence. | Pass |
| AC-5 — Regression boundary | Managed conflict, predecessor authentication, AGENTS merge, source/channel, stale-path, symlink/race and project-preservation regressions pass in text/JSON. Existing-parent leaves use hard-link/no-clobber or atomic exchange; absent-parent changes use adjacent prepared directory units and no-replace publication. | Pass |
| AC-6 — Precise trust contract | Normative/user-facing contracts distinguish exact selection, digest verification, mutable GitHub refs/assets and platform-enforced immutability without changing accepted source shapes. Contract searches/tests reject stronger claims. | Pass |
| AC-7 — Trust regression/public metadata | Offline terminology regression passes. Live GitHub v0.7.0 metadata and final public evidence are not yet available. | Partial — publication pending |
| AC-8 — Reviewable publication dry run | The repository contains the documented `vibe-release` Agent entry point plus closed offline publication-plan/request/intent schemas and exact five-asset contract. Final intent is deferred until the real release commit, tag identity and remote snapshot are frozen. | Partial — final intent pending |
| AC-9 — Consent-bound publication | Closed authorization, lease, read-before-write/read-back and retry rules are implemented and locally validated. No remote mutation has occurred. | Partial — live execution pending |
| AC-10 — Public artifact verification | Local direct/Plugin smoke, nested validation and temporary clean A/B candidates pass. Public re-download, GitHub parity and public smoke remain pending. | Partial — public assets pending |
| AC-11 — Offline/privacy boundary | Actual `/usr/bin/python3` 3.9.6 passes all 57 tests. Packaging, validation, install and upgrade use standard-library/offline paths; artifact/intent privacy negatives pass. | Pass |
| AC-12 — Readiness closure | The L-work author/reviewer/orchestrator/RD/QA chain is recorded. Three implementation discoveries reopened only the affected boundary before edits: closeout child schema, final-leaf atomicity and missing-parent directory units. Distinct review and fresh gate confirmation preceded each resume. | Pass |
| AC-13 — Exact candidate quality | Frozen working tree passes focused 12/12, full 57/57 on Python 3.14 and 57/57 on actual Python 3.9.6, default verify, healthy source doctor, JSON/diff/bytecode checks, direct/Plugin smoke and byte-identical temporary clean A/B builds with dual valid release validation. A real repository clean commit has not yet been frozen. | Partial — real clean commit pending |
| AC-14 — Public release and closure | No tag, Release, asset upload, public receipt, issue evidence comment or issue close has been executed. | Pending |

## Automated checks

| Check | Independent result | Notes |
|---|---|---|
| Exact focused QA | Pass, 12/12 | Replays leaf and directory races, rollback/recovery, onboarding and result truthfulness. |
| Full suite, Python 3.14.6 | Pass, 57/57 in 37.608s | Independent QA run. |
| Full suite, `/usr/bin/python3` 3.9.6 | Pass, 57/57 in 34.594s | Required runtime evidence. |
| Default `vibe verify` | Pass, 57 tests | Lint/typecheck/build are not configured and are reported as not applicable. |
| Source `vibe doctor` | Healthy, read-only | Activation `07613a6a22db6bb6454ba55dbaf12681b54e5024eff6d526f99ee45d2d2fe992`; payload `874675420e697ab9c16c35a4f2f558acc65b91dcc42464bd461cda2800116eb1`; manifest `1be5c64c834cdc5d3cefcc89e7afb1e0995308958021891471f443d3a1db830c`. These working-tree identities must be recomputed after the evidence commit. |
| Bytecode and diff check | Pass | `py_compile` and `git diff --check`. |
| Temporary clean A/B builds | Pass | Byte-identical, exact five publication assets, dual `validate-release` valid. Temporary commit identity is not reused as public evidence. |
| Direct and Plugin smoke | Pass | Healthy installs from locally built candidate. |

## Independent manual/fault scenarios

- v0.2/v0.3/v0.4 exact onboarding bridge followed by healthy target doctor.
- v0.5/v0.6 missing onboarding pre-write block; existing onboarding byte preservation.
- Post-mutation `PermissionError` at every v0.3 and v0.6 existing-parent leaf.
- Absent onboarding link publication race and existing manifest atomic-exchange race.
- Official-v0.6 absent-parent release-skill directory unit, including no-write plan, hidden-stage construction, commit/recovery and exact target modes/content.
- Final-root ordinary file, dangling symlink and external directory winners.
- Post-publication third-party tree addition and rollback-detach concurrent recreation.
- Hidden-stage member write failure with exact cleanup and predecessor snapshot equality.
- Real libc adapter plus missing-symbol and errno failure mappings.

## Pending final-release gates

1. Freeze one reviewed real repository commit containing this evidence and no unrelated files.
2. Re-run independent QA from that exact clean commit, including two byte-identical builds and dual `validate-release`.
3. Freeze release-note bytes and annotated-tag identity; obtain the live read-only remote snapshot.
4. Generate and authorize the exact offline publication intent, execute only its allowlisted operations, then read back and publicly download/hash all five assets.
5. Validate the sanitized publication receipt and public install/upgrade smoke.
6. Generate a separately authorized issue-closeout intent, post marker-bound evidence and close exactly issues #1–#5.

## Recovery and limitations

- No release/tag/asset/issue write has occurred at this stage. On an uncertain future remote response, read back the natural-key object before any retry; never force, delete, replace or rewrite.
- macOS and actual Python 3.9.6 are executed evidence. The libc adapter includes Linux `renameat2` and mocked unsupported/error coverage, but this local QA run is not Linux certification.
- Same-task reload and automatic successor remain unsupported without independent live host receipts; the release is Pre-release, not Stable or public Plugin Directory promotion.
- Transaction evidence is integrity-checked but untrusted against a malicious same-OS-principal process that deliberately targets random intent-bound private names.
- Independent QA changed no repository file; this record was persisted by the orchestrator from QA's read-only evidence before the real release commit.
