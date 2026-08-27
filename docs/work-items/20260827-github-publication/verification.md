# Verification: Publish Vibe Kit v0.3.0 GitHub prerelease

## Acceptance evidence

| Criterion | Evidence | Result |
|---|---|---|
| AC-1 | Public repository `https://github.com/mintgao/vibe-kit`; MIT `LICENSE`; Git author `mintgao <154321591+mintgao@users.noreply.github.com>`; Plugin homepage/repository/license metadata validated. | Pass |
| AC-2 | Final manifest records `status=prerelease`, `source.ref=4f8a2fa8f8de9b947bbf6ea5e6e34ff1b3f0b35b`, `tree_state=clean`; tests reject dirty/uncommitted prerelease input and unknown status. | Pass |
| AC-3 | GitHub asset `vibe-kit-distribution-0.3.0.zip` contains the complete release directory; downloaded outer bundle and its unpacked directory pass SHA and release validation. | Pass |
| AC-4 | Default Python and system Python 3.9 both pass 16/16 tests; `doctor`, bytecode compile, official Plugin/Skill validators and independent QA pass. | Pass |
| AC-5 | Final reachable history is one root commit; scan reports no complete high-confidence secret, `.env`, `.vibe/local`, private absolute path, dist or cache. GitHub Push Protection also accepted the final push. | Pass |
| AC-6 | Public repo has default branch `main`; remote main and peeled annotated `v0.3.0` both resolve to `4f8a2fa8f8de9b947bbf6ea5e6e34ff1b3f0b35b`. | Pass |
| AC-7 | `https://github.com/mintgao/vibe-kit/releases/tag/v0.3.0` is published with `isPrerelease=true`, `isDraft=false`, title `Vibe Kit v0.3.0`, and five uploaded assets. | Pass |
| AC-8 | Fresh GitHub download under an isolated temp root: bundle SHA parity, all `SHA256SUMS` OK, `validate-release` pass, `plan init` safe/zero-write, `init` pass, installed `doctor` 0 warnings. | Pass |
| AC-9 | Released `.vibe/core/feedback.json` defaults to `mintgao/vibe-kit`; README states review/hash confirmation and optional `--repo` override; regression test covers the released config. | Pass |
| AC-10 | This record captures URLs, refs, hashes, limitations and rollback; close-time feedback classification is recorded below. | Pass |

## Automated checks

| Check | Result | Notes |
|---|---|---|
| `/usr/bin/python3 -m unittest discover -s tests -v` | Pass | Python 3.9.6, 16/16. |
| `python3 -m unittest discover -s tests -v` | Pass | Default workspace Python, 16/16. |
| `/usr/bin/python3 -m py_compile bin/vibe tests/test_cli.py` | Pass | Bytecode cache redirected to an isolated temporary directory. |
| `./bin/vibe doctor .` | Pass | Version integrity OK, 0 warnings. |
| `./bin/vibe validate-release dist/vibe-kit-0.3.0` | Pass | 0.3.0, 30 payload files, network not used. |
| Official Plugin validator | Pass | Final expanded `vibe-kit` Plugin accepted. |
| Official Skill quick validators | Pass | `vibe-bootstrap`, `vibe-maintain`, and repository `vibe-feedback-flow` accepted. |
| Secret detector regression | Pass | 14 detectors have 14 isolated runtime-built fixtures; reachable-history and archive scans find no complete secret. |
| Independent `vibe_qa` gate | Pass | Final HEAD, manifest, double-layer bundle, smoke install, metadata and external-safety checks signed off. |

## Manual scenarios

- GitHub rejected the first push because complete synthetic Stripe, Slack and Twilio token literals existed in test history. No bypass was used: fixtures were changed to runtime construction, unpushed history was rebuilt, detector coverage was strengthened to 14/14 isolated cases, and the final push passed Push Protection.
- Repository verification: visibility `PUBLIC`, default branch `main`, remote main and peeled annotated tag point to the accepted release commit.
- Release verification: GitHub reports five assets in `uploaded` state and digests matching local files.
- Download verification: downloaded `vibe-kit-distribution-0.3.0.zip` SHA equals the local bundle; all nested checksums pass before install smoke testing.

## Published artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `vibe-kit-distribution-0.3.0.zip` | 148408 | `46b37852e9796cebf1c23c9f58e868be0af6e568400d9a0900f2fa3f957a79ea` |
| `vibe-kit-0.3.0.zip` | 46286 | `5ce710bd9f160f15d006445de6b050f1241acdab863821c59fbeeb0ff43315c5` |
| `vibe-kit-plugin-0.3.0.zip` | 50727 | `6fd0caa4a08a1c5aace537f3cbe68b3bd4b392fe02526a078e52b421ac481fdf` |
| `release-manifest.json` | 9109 | `678013d516fa266cfe68402ed8f14ddfb7f01a7025948ed752a156836253be4e` |
| `SHA256SUMS` | 5310 | `e751bbb26f13309a7dd6f86ea88bebb53575e65d66f00df69227508e97eef5ea` |

## Limitations and follow-ups

- This is a GitHub Pre-release, not a stable release. Linux CI remains a stable-promotion gate; testing was performed on macOS with Python 3.9 and the workspace Python.
- Artifacts have SHA-256 integrity metadata but no publisher signature or external provenance attestation.
- Public Codex Plugin Directory publication, package-manager distribution and a network updater remain out of scope; consumers use the GitHub Release or repository-pinned Plugin marketplace.
- Rollback, if needed, is to remove or draft the GitHub Release and remove the remote tag after confirming the exact target. The public repository and commit should remain available unless a separate destructive decision is made.
- The publication flow exposed one remaining framework-level opportunity: first-class orchestration for GitHub prerelease creation and downloaded-asset verification. It was evaluated through `vibe-feedback-flow` as recorded below.

## Vibe Kit retrospective

- Qualifying signal: publishing required manual coordination across clean-source preflight, remote refs, release assets, digest read-back, canonical re-download, validation and install smoke testing.
- Local candidate: `fb-20260827t074230z-685dcc37`, title `Add a first-class GitHub prerelease publication workflow`, medium severity, high confidence, privacy clean.
- Review target: `mintgao/vibe-kit`; exact-payload review hash `sha256:af324f7012290ca65f298a23c81623c63cea2deee50a8cadb1d2ba98807af424`.
- Status: `review-ready`. No Issue was created because Vibe Kit requires explicit approval for this exact report ID, repository and review hash.
