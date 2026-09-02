# Verification: V0 8 Publication

- QA date: 2026-09-02
- Status: **verified**
- Final verdict: **PASS — public v0.8.0 Pre-release published and verified**
- Release URL: https://github.com/mintgao/vibe-kit/releases/tag/v0.8.0
- Release source commit: `7012ae2086cef69bd65dba0945da4d6d9c463d81`
- Annotated tag object: `b304ecea2824fa74b289192d0bbf16874b9fea77`
- Evidence boundary: independent QA verified the exact clean release source,
  authenticated Git/GitHub read-back, all five unauthenticated public downloads,
  nested checksums, target release validation, and six public install/upgrade
  smokes. No Issue operation, Stable promotion, platform-immutability, signing,
  provenance, same-task reload, or automatic-successor claim is made.

## Acceptance evidence

| Criterion | Independent evidence | Result |
|---|---|---|
| AC-1 — Exact candidate quality | Clean accepted commit `7012ae2...` received fresh independent QA after the publication tooling changes. The canonical full suite passed 65/65; lint, typecheck, and build are explicitly unconfigured rather than silently skipped. | Pass |
| AC-2 — Python 3.9 and offline boundary | CPython 3.9.25 passed the full 65-test suite, release validation, publication plan/receipt validation, and public target validation. Candidate tools remained standard-library-only and offline; credentials are not present in persisted evidence. | Pass |
| AC-3 — Deterministic clean builds | Two independent clean builds from `7012ae2...` produced byte-identical five-asset sets. Both sets passed `validate-release`; asset-set identity is `f6908b99b2abf9bab7cd26db2c0ebfe444dbfbf38e69f211f3615f99b024a1fb`. | Pass |
| AC-4 — Exact public asset closure | GitHub exposes exactly the five scoped names with the intended sizes and SHA-256 values. All five public downloads match; `SHA256SUMS` contains 47 legal, unique, sorted records and every nested digest matches. | Pass |
| AC-5 — Closed publication intent | Offline intent `2836e6558b386b28280257200a9f035e365e3c2a778191e3c2d5f2ef9b05065f` bound the repository, source/main CAS pair, annotated tag, exact Release body/state, five assets, closed remote snapshot, six operations, and non-destructive recovery. | Pass |
| AC-6 — Receipt plus live proof | Publication receipt `5f1549d613ee784014f08c1a3e41d5c17bf1932aae2b1481fdc906d91f9b8a4d` validates with `remote_write_state=confirmed-complete` and `verification_state=passed`; authenticated live read-back and independent public evidence supplement the offline validator's deliberately unauthenticated boundary. | Pass |
| AC-7 — Safe remote mutation | `main` fast-forwarded without force from `60552d3...` to `7012ae2...`; tag, Release, and assets were created/confirmed only under exact-match rules. No move, rewrite, delete, replace, duplicate, or extra object occurred. | Pass |
| AC-8 — Bounded write recovery | Each of the six terminal operations and five asset ledgers recorded one definite-success attempt followed by read-back. No retry or uncertain write occurred; divergent-state and destructive recovery paths were not entered. | Pass |
| AC-9 — Public downloads and smokes | Five unauthenticated downloads, the 48-member distribution graph, Python 3.9 target validation, fresh direct init/doctor, Plugin-bundled plan/init/doctor, and public v0.3/v0.5/v0.6/v0.7-to-v0.8 upgrades all passed. | Pass |
| AC-10 — Historical v0.7 isolation | Focused publication/package tests passed 11/11, including the historical v0.7 validators and profile separation. v0.8 evidence cannot satisfy the exact v0.7 publication/closeout profile. | Pass |
| AC-11 — No Issue operations | The executable v0.8 operation set contains no Issue action; `issue_closeout` is null in the receipt. No Issue was read, commented, closed, reopened, or otherwise changed. | Pass |
| AC-12 — Completion claim gate | Final post-publication acceptance `1f230ad2d4582097908343b95cb26686e2c99a8d862f9df78eafc5d3f4133a47` records AC-1 through AC-12 passed in order. Independent QA concluded `published-and-verified`; live metadata reports `immutable=false`. | Pass |

## Automated and public checks

| Check | Independent result | Notes |
|---|---|---|
| Canonical full suite | Pass, 65/65 | Fresh release QA on the exact release source; 87.262 seconds. |
| Full suite, CPython 3.9.25 | Pass, 65/65 | Required supported-runtime evidence; 82.443 seconds. |
| Focused publication/package suite | Pass, 11/11 | v0.8 publication profile and historical v0.7 isolation. |
| Clean A/B prerelease builds | Pass | Byte-identical exact five-asset outputs; both release validations valid. |
| Offline publication plan | Safe | Exit 0, `status=safe`, no errors; exact intent digest recorded above. |
| Publication receipt validation | Valid | Exit 0, no errors; remote writes confirmed complete and verification passed. |
| Authenticated live read-back | Pass | Canonical evidence `dac702c4b96578ea9a47185315673002a922b0b1e23e6ab74fa56db34a447333`. |
| Independent public live verification | Pass | Canonical evidence `aa24774500b774021370350e158f2e088f82a171ce42800f310a45142c40faaa`. |
| Public downloads and checksum graph | Pass | All five assets and all 47 nested checksums matched; distribution has 48 exact regular members. |
| Public direct and Plugin smokes | Pass | Fresh direct install/doctor and Plugin-bundled plan/init/doctor both exit 0. |
| Public predecessor upgrades | Pass | v0.3, v0.5, v0.6, and v0.7 upgrades preserve their business file and end with a healthy v0.8 doctor. |
| Final post-publication acceptance | Pass, AC-1 through AC-12 | Canonical acceptance digest recorded above; validation errors empty. |

## Public Git and GitHub state

| Item | Public value |
|---|---|
| Release | ID `381079578`; `Vibe Kit v0.8.0`; public, non-draft, Pre-release; `immutable=false` |
| Release URL | `https://github.com/mintgao/vibe-kit/releases/tag/v0.8.0` |
| Public `main` release source | `7012ae2086cef69bd65dba0945da4d6d9c463d81` |
| Tag ref | `refs/tags/v0.8.0` -> annotated object `b304ecea2824fa74b289192d0bbf16874b9fea77` |
| Peeled tag | `7012ae2086cef69bd65dba0945da4d6d9c463d81` |
| Tagger time | `2026-09-02T08:05:04Z` |
| Release body SHA-256 | `c95b3e379f9c42bc214785b3b42b0fa2585d89e1513d290df522cf8a54903f25` |

The annotated tag is unsigned. Its object identity and the verified public asset
digests establish the recorded selection and byte identity, not an external
signature, provenance attestation, or platform immutability guarantee.

## Publication assets and digests

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 6,112 | `674ee56741c98ea5466a2c33252039123ccd9d8ef78d3e3567423d301ae4e08f` |
| `release-manifest.json` | 12,144 | `66766a3659e52be1ef71976a7357de691cba43c7d6f9ed26f67ad27a6a3a15c3` |
| `vibe-kit-0.8.0.zip` | 169,427 | `dd8eee0a807f3e66b840f166daf12863934bbb01e5f5d7b450a3b0fb17d07467` |
| `vibe-kit-distribution-0.8.0.zip` | 523,385 | `f1a53b513c6a3d99d7ed1134558bd267dc79c72e0a1d15f69b26a089fbbd41ce` |
| `vibe-kit-plugin-0.8.0.zip` | 176,387 | `3c1bf09af1c97dc5993fe6f3deac383b0a1429d437f77594c0e1e400e4f0e957` |

All five public downloads match the frozen candidate. The exact sorted asset-set
identity is `f6908b99b2abf9bab7cd26db2c0ebfe444dbfbf38e69f211f3615f99b024a1fb`.

## Remote-write and verification evidence

- Authorization ID: `auth-v080-2836e655-20260902`; the authorization was bound
  to the exact intent digest and allowed only fast-forward main, create-or-confirm
  annotated tag, create-or-confirm Pre-release, upload-or-confirm five assets,
  read-back, and public download verification.
- Release-gate evidence:
  `01098a92f866cbb2749ec550a9a59323bce22c19d643fa1af9a77a2a345a5ffe`.
- Authenticated live read-back:
  `dac702c4b96578ea9a47185315673002a922b0b1e23e6ab74fa56db34a447333`.
- Publication receipt:
  `5f1549d613ee784014f08c1a3e41d5c17bf1932aae2b1481fdc906d91f9b8a4d`.
- Offline receipt validation result:
  `508d8ffcea095ac6cad2f3437c18dac4e58ec3aa2ddc699e70944d7760b3afa9`.
- Independent public live evidence:
  `aa24774500b774021370350e158f2e088f82a171ce42800f310a45142c40faaa`.
- Final post-publication acceptance:
  `1f230ad2d4582097908343b95cb26686e2c99a8d862f9df78eafc5d3f4133a47`.

## Recovery, limitations, and closeout boundary

- GitHub reports `immutable=false`; the release is exact and hash-verified, not
  platform-enforced immutable.
- The annotated tag is unsigned. No signing or provenance claim is made.
- An initial independent public-read attempt received an unauthenticated API
  rate-limit response before downloads and created no partial evidence. QA then
  used the authenticated orchestrator read-back for remote metadata while still
  downloading and validating all five public assets without authentication.
- Activation remains `ready=false` until the documented manual-new-task
  fallback provides host evidence. Same-task reload and automatic handoff are
  not claimed.
- This is a Pre-release, not Stable, and is not a public Plugin Directory
  publication.
- No Issue or destructive remote operation was performed. Any future uncertain
  action must read back by natural key before a bounded retry and must not force,
  move, rewrite, delete, or replace existing release state without a new decision
  and authorization.
- The release source remains the public `main` commit `7012ae2...`. This final
  evidence update is intentionally local-only and is not part of the published
  source (`evidence_pushed=false`).

## Files changed by final evidence closeout

- `docs/work-items/20260902-v0-8-publication/brief.md`
- `docs/work-items/20260902-v0-8-publication/verification.md`
