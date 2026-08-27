# Verification: Publish Vibe Kit v0.5.0 GitHub prerelease

Vibe Kit v0.5.0 is published at <https://github.com/mintgao/vibe-kit/releases/tag/v0.5.0>. GitHub reports a non-draft Pre-release with five uploaded assets.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | README, changelog, release note, product/architecture context, Plugin metadata and protocols identify 0.5.0 and include Agent-first adoption plus Technical Decision Readiness Gate. The permission-safe atomic-upgrade requirement remains explicitly shaped/unimplemented. | Pass |
| AC-2 | Independent QA passed focused 12/12, full 31/31, `verify` 31/31, compilation, diff validation, unpublished packaging, release validation, GitHub/Plugin artifact smokes and fail-closed contract cases. | Pass |
| AC-3 | JSON self-upgrade plan was safe with 24 no-op managed entries and two installation-state updates. Upgrade changed no managed content; root doctor is healthy at 0.5.0 with complete onboarding. | Pass |
| AC-4 | Clean release commit `9b32462129f791c54ef34147f0f872c5903aa73e` produced two byte-identical prerelease builds with 35 payload files, core/Codex protocol 3, Agent-install protocol 1 and feedback protocol 2. | Pass |
| AC-5 | Annotated tag object `d9edf3e0e8e0eb70b95ec0d653572ef505462944` peels to the release commit. Remote `main` and the peeled tag both resolved to that commit before this evidence update. | Pass |
| AC-6 | GitHub reports `Vibe Kit v0.5.0`, `isPrerelease=true`, `isDraft=false`, five assets, and published time `2026-08-27T15:56:28Z`. | Pass |
| AC-7 | Every remote asset reports `uploaded`; GitHub sizes/digests equal the local publication files listed below. | Pass |
| AC-8 | All assets were freshly downloaded and compared byte-for-byte. Nested checksums, release validation, GitHub init/adopt/doctor, preserved-complete receipt, Plugin init/doctor and Agent-contract identity passed. | Pass |
| AC-9 | This record captures the URL, refs, assets, validation, limitations, skipped gates and non-destructive rollback boundary. | Pass |

## Automated and release checks

| Check | Result | Evidence |
|---|---|---|
| Source independent QA | Pass | Focused 12/12; full 31/31; `./bin/vibe verify .` 31/31; py_compile and `git diff --check` passed. |
| Controlled self-upgrade/root doctor | Pass | 0 managed files updated; manifest/version advanced to 0.5.0; doctor healthy, version integrity OK, onboarding complete, no warnings. |
| Exact clean release source | Pass | Isolated local clone at `9b32462129f791c54ef34147f0f872c5903aa73e`; doctor healthy and full 31/31 suite passed. |
| Prerelease package | Pass | 35 payload files; `status=prerelease`; source ref is the clean release commit; release validation `valid`; network not used. |
| Reproducible rebuild | Pass | Five publication files from a second empty output directory compare byte-for-byte equal. |
| Git ref/read-back | Pass | Remote main, annotated tag object and peeled commit were read back after push. |
| GitHub Release/read-back | Pass | Public non-draft Pre-release, five assets, every asset state uploaded, sizes and SHA-256 digests matched. |
| Isolated re-download | Pass | All five downloads matched local bytes; distribution SHA256SUMS returned OK for every nested entry; downloaded release validation was valid. |
| GitHub release ZIP smoke | Pass | Read-only init plan reported zero writes; init/doctor healthy; adopt preserved legal complete onboarding byte-for-byte and both receipt/doctor reported complete. |
| GitHub Plugin ZIP smoke | Pass | Plugin-bundled plan/init/installed doctor healthy; packaged Agent contracts equal the direct release payload. |

## Published artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `vibe-kit-0.5.0.zip` | 68173 | `1784eb5ff07380e5950106f4da6e942247122a6f435b2d69f44cbb5565d7eb7a` |
| `vibe-kit-plugin-0.5.0.zip` | 73045 | `7ca95e1359c0f65ce6605962752925cccd416fceefde79db7d20be565f1d0117` |
| `vibe-kit-distribution-0.5.0.zip` | 214965 | `c37bf20939d1796d316edb75fd57a90f41cbba8e09960c76a6f6e57fcadfd981` |
| `release-manifest.json` | 10335 | `78fbdf81ca9c24c4aabdc729fd880acc5c7e5cd502273dc6525b4e147a9bf0cb` |
| `SHA256SUMS` | 5972 | `643bba968b5459ea71063e1ad3d24c88d46277e547cc5f9f402ac6e8a914324d` |

## Limitations and recovery boundary

- Real Linux and Python 3.9 were not run in this final release environment. Stable promotion remains blocked; the public status is Pre-release.
- A fresh live Codex task, public Plugin Directory installation, non-Codex adapter and sequential-only host were not exercised. Static and artifact evidence is not described as live-host proof.
- Install/upgrade are not whole-directory transactions. Post-mutation filesystem failures report conservative `unknown-partial` plus inspect-before-retry recovery. The separate permission-safe atomic-upgrade work remains unimplemented.
- GitHub tag identity and SHA-256 provide integrity signals, not an external publisher signature or independent provenance attestation.
- Rollback, if separately authorized, is limited to drafting/deleting the exact Release and removing the exact tag after target verification. The public release commit and evidence should otherwise remain available.
