# Verification: Publish Vibe Kit v0.4.0 GitHub prerelease

Vibe Kit v0.4.0 is published at <https://github.com/mintgao/vibe-kit/releases/tag/v0.4.0>. The Release is non-draft and marked Pre-release.

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | README, changelog, release notes and product/architecture context consistently identify 0.4.0 as a GitHub Pre-release and exclude stable, Plugin Directory and package-manager publication. | Pass |
| AC-2 | Workspace Python and macOS Python 3.9.6 each pass 21/21 tests; `vibe verify`, `doctor`, bytecode compilation and official Skill/Plugin validators pass. Independent QA reran `doctor`, bytecode compilation and diff checks. | Pass |
| AC-3 | Manifest records `status=prerelease`, `source.ref=69ae813098335c4865cf2b6b7b36f66d52097167`, `tree_state=clean`, core protocol 2, feedback protocol 2 and Codex adapter 2. Two clean-tree builds were byte-identical. | Pass |
| AC-4 | Annotated tag object `d652752b40e81b8c46612ad3378b4576d7ab2e4f` peels to release commit `69ae813098335c4865cf2b6b7b36f66d52097167`. Remote `main` and the peeled tag both resolved to that commit at publication; only this evidence commit follows it. | Pass |
| AC-5 | GitHub reports `Vibe Kit v0.4.0`, `isPrerelease=true`, `isDraft=false`, five assets and published time `2026-08-27T13:24:19Z`. | Pass |
| AC-6 | All five remote assets report `uploaded`; their sizes and GitHub SHA-256 digests equal the local publication files listed below. | Pass |
| AC-7 | All assets were freshly downloaded into an isolated directory and compared byte-for-byte. The downloaded distribution passed all nested checksums, `validate-release`, a zero-write `plan init`, `init`, installed `doctor` and `feedback mode` with the expected project default `ask`. | Pass |
| AC-8 | This record captures the release URL, refs, artifact evidence, checks, skipped gates, residual risks and rollback boundary. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `python3 -m unittest discover -s tests -v` | Pass | 21/21 on workspace Python. |
| `/usr/bin/python3 -m unittest discover -s tests -v` | Pass | 21/21 on Python 3.9.6. |
| `python3 bin/vibe verify .` | Pass | Configured test gate passed, 21/21. |
| `python3 bin/vibe doctor .` | Pass | Version integrity 0.4.0; zero warnings. |
| `python3 -m py_compile bin/vibe tests/test_cli.py` | Pass | Release source compiles. |
| Official Skill/Plugin validators | Pass | Managed feedback Skill and source Plugin accepted using the system Python runtime. |
| Independent QA prep gate | Pass to commit | Dirty-tree prerelease packaging correctly fails; current unpublished artifact must not be uploaded. |
| `python3 bin/vibe package --status prerelease` | Pass | Clean source; 30 payload files; distribution bundle SHA-256 `695c925ca321b291299a1e71194664655f29d8e5ab92e849dca178685cdf2e37`. |
| Reproducible rebuild | Pass | Five publication files from a second empty output directory compare byte-for-byte equal. |
| `python3 bin/vibe validate-release` | Pass | Local release and fresh GitHub distribution download both accepted as 0.4.0 with 30 payload files. |
| Expanded Plugin validators | Pass | Built marketplace Plugin and both bootstrap Skills accepted. |
| GitHub ref/read-back | Pass | Public repo, `main`, annotated tag, prerelease state, five uploaded assets, sizes and digests verified after writes. |
| Downloaded `SHA256SUMS` | Pass | Every marketplace, payload, manifest and nested ZIP entry returned `OK`. |
| Fresh install smoke | Pass | `plan init` made no files; `init` installed 21 managed and 7 project-owned files; installed `doctor` had 0 warnings and feedback mode was `ask`. |

## Manual scenarios

- The ignored dirty-tree unpublished candidate was moved intact to `/private/tmp/vibe-kit-0.4-unpublished.9X2mHE/`; it was not uploaded.
- Before writing, authenticated account `mintgao`, public repository `mintgao/vibe-kit`, absent remote Release and absent remote tag were verified.
- After upload, remote `main`, annotated tag, Release state and all asset digests were read back before any further action.
- The GitHub-downloaded assets matched local files byte-for-byte before the distribution bundle was unpacked and validated.

## Published artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `vibe-kit-distribution-0.4.0.zip` | 163514 | `695c925ca321b291299a1e71194664655f29d8e5ab92e849dca178685cdf2e37` |
| `vibe-kit-0.4.0.zip` | 51293 | `676a0b2723d27f4d5fbb4bbcadd16361d3230dbd43716d6af4d74b4fa300abbf` |
| `vibe-kit-plugin-0.4.0.zip` | 55735 | `536a0e2687d049a7d3994df8b76af3aa354ca686ce2a7f324ebf1dccb40ac734` |
| `release-manifest.json` | 9135 | `2aa05ce8659ec8a15408e64e060aad4e2333586ea141ca33111f83681abc2c90` |
| `SHA256SUMS` | 5310 | `9b0efe46898520d9feb75682e5fabb14046f9ab42d1e64376237342d6b217b01` |

## Limitations and follow-ups

- Linux CI was not run, so stable promotion remains blocked. macOS was exercised with workspace Python and system Python 3.9.6.
- Artifacts have deterministic SHA-256 integrity metadata but no publisher signature or external provenance attestation.
- Public Codex Plugin Directory publication, package-manager distribution and a network updater remain out of scope.
- Rollback, if separately authorized, is limited to drafting/deleting the exact `v0.4.0` Release and removing the exact remote tag after confirming targets. The public commit and evidence should remain available unless a separate destructive decision is made.
- Close-time feedback classification found no new Vibe Kit gap beyond the already submitted first-class publication workflow issue and the separately pending, local permission-failure candidate; no additional candidate was created.
