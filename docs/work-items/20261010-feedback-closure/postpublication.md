# Vibe Kit v0.11.0 public acceptance

[v0.11.0 Pre-release](https://github.com/mintgao/vibe-kit/releases/tag/v0.11.0) is published and independently verified. AC-1–AC-9, AC-10.1 and AC-10.2 passed in the exact eleven-criterion postpublication acceptance. AC-10.3 is a separate [closeout phase](closeout.md).

## Published identity

- Source commit: `f138e7df4daed1097ca6ac5d6ccb59125fb19a07`; source tree: `622512c15d7939b328fa650b21a18993eafbf265`.
- Main was advanced from `ac549fa69319ef92ba859bd7a43d3607ec226e43` to the frozen source using expected-old-OID compare-and-swap with force disabled, and read back. Later evidence commits may advance main without moving the release tag.
- Annotated tag `v0.11.0`: `afae7e4324feb9e12398cc2e60e1508e570eb523`, peeling to the source commit; exact tagger/message identity read back.
- Release ID: `411277940`; non-draft Pre-release. Exact title and frozen body hash matched; no promotion or replacement occurred.
- Publication schema/profile: `6` / `vibe-kit-v0.11.0-prerelease`. All six ordered operations and five asset ledgers are terminal and confirmed. Each remote write had one definite-success attempt, followed by read-back; no retry was needed.

## Public assets

| Asset | Bytes | SHA-256 |
|---|---:|---|
| `SHA256SUMS` | 6115 | `8497a7f901d71e0d0fabba8af82586f243da358f445b9f89267793c2ab63a150` |
| `release-manifest.json` | 12487 | `7597b103558fe3406b741ab93426a59df3f03c1040e8c71c4b55a0db9599a6c9` |
| `vibe-kit-0.11.0.zip` | 213757 | `e22ac96b078cc34e91b5603bea0363b80d705354ebbc88117627c67648797604` |
| `vibe-kit-distribution-0.11.0.zip` | 656516 | `9c0a82fe75b6a257e84f8b1026d6ad83f415c8d5fe81d656b96e6357a0efb6d7` |
| `vibe-kit-plugin-0.11.0.zip` | 220733 | `b657add52c708e088061f9b614d7dfbd847209c59fa3d713af0def70b4cb03c3` |

Five fresh canonical public downloads matched both independently built candidates byte-for-byte. A validation set was reconstructed only from the newly downloaded distribution and compared with all separately downloaded assets. The downloaded target's `validate-release` actually passed under CPython 3.9.25; no build or cached target substituted for it.

## Actual public installation and upgrade smokes

| Compiled smoke | Result | Evidence SHA-256 |
|---|---|---|
| `public-direct-init-doctor` | Pass | `ae6acb77a93b26a3932739fb9e11b5bc99b0dc6d86723ebde5e75375e69e9299` |
| `public-plugin-bundled-plan-init-doctor` | Pass | `602fbc29a8b81d6cf8f9d4f635d5871e636bbe8dc8d105aef2f5dc389e9b3bd6` |
| `public-upgrade-v0.3-to-v0.11.0` | Pass | `404d034dfaa3091a5237dab53e94852996727c2cdf1c86591b39dc920d4c2148` |
| `public-upgrade-v0.5-to-v0.11.0` | Pass | `28753e46904210695122c552b759f932fb3cace9a1661c775b4c4c116267aefe` |
| `public-upgrade-v0.6-to-v0.11.0` | Pass | `0bd81f292a9a5d0cf756566cadf82a52ef8fcfb1eab254e12d83423a80888223` |
| `public-upgrade-v0.7-to-v0.11.0` | Pass | `93dee98845b3b9900d9a60e4ebfc6bcc033409947a52520c9064b1f766194131` |
| `public-upgrade-v0.8-to-v0.11.0` | Pass | `61542096a29ac6b5b86600f3a99b69b0e5b61036ca0e14f59f58229b9ea71df3` |
| `public-upgrade-v0.9-to-v0.11.0` | Pass | `01fa9dc40ebeb731d28abe19dea45ee59dc44621448c44d2a6ca4d47bc0e2cf6` |
| `public-upgrade-v0.10.0-to-v0.11.0` | Pass | `8cd6fec8d820a2ea2850216dba259617d6a7c4d7b7a43b0c22780650de70ee9d` |
| `public-upgrade-v0.10.1-to-v0.11.0` | Pass | `b91cca6a6b5b2b506f99aaa617a340925e900fcbdc35cb5cfd72109c8a28c0fe` |
| `public-repeat-upgrade-v0.11.0` | Pass | `40c18f1e52d17c67d1f7c62a22beddf2c906fd79a93892d57059c55a547856c3` |

The direct and bundled Plugin installations, eight actual predecessor upgrades, and repeat upgrade all passed. The repeat smoke performed two actual same-version committed upgrades with healthy doctor results and no active transaction residue. Predecessor identity/checksum and project-owned context preservation were checked in disposable fixtures; no real downstream project was modified.

## Final evidence bindings

| Evidence | Canonical SHA-256 |
|---|---|
| Frozen publication intent | `da69c6ed6c312d36c199ba92da6ffdaa02b8f59fee741d13b4c2ed77c3d9a7b4` |
| Actual closed publication receipt | `3974a336fa162c2e4feaece2ba8e26eea4cec98134f08375162b1a9571ca712b` |
| Independent public verification evidence | `86a4a73ca1d55e55307d28059f287adbaae0f4b2d0694103b876c9d54697a368` |
| Final actual CPython 3.9.25 `validate-publication` result | `ccf22a6c43b4951413d64e16127718ef242005d1fbc2d7030d23bdc2bb8b5b93` |
| Independent postpublication acceptance | `3d5f28c54db60a496c7d5ea67f83bf104f85deb67cef72e7f421c29f47722677` |

Final publication validation returned valid with zero errors. Its intent, authorization and publication receipt retained their exact before/after input byte hashes. A new mode-0600 result is semantically and canonically identical to final stdout. The first output preflight refused macOS's symlinked temporary directory before the validation body or write; the same physical directory's canonical path was then used. There was no approval rejection, protected-input overwrite or repeated validation body.

GitHub authenticity is supported by actual host read-back and fresh downloads; the offline validator reports `host_evidence_authenticated=false` and `network_used=false`. GitHub reports `immutable=false`; signing or permanent platform immutability is not claimed. Installation health does not prove target-rule activation or project readiness. Static #18 evidence, diagnostic availability, sanitization and resource limits remain as recorded in [verification](verification.md).
